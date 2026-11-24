"""Unit tests that run without libmdf: constants, lookups, request building and the receive loop."""

import ctypes
import sys

import pytest

import millistream_mdf
from millistream_mdf import (
    MDF, Field, MessageClass, MessageReference, RequestClass, RequestType, MDFConnectionError,
)
from millistream_mdf import _libmdf, sync_client
from millistream_mdf._mappings import server_address


def test_import_does_not_load_libmdf():
    assert 'millistream_mdf' in sys.modules
    # Nothing in these tests calls into C, so the library must still be unloaded.
    assert _libmdf._LazyLib._loaded is None


@pytest.mark.parametrize('value, expected', [
    ('quote', MessageReference.QUOTE),
    ('MDF_M_QUOTE', MessageReference.QUOTE),
    (' basicdata ', MessageReference.BASICDATA),
    (5, MessageReference.QUOTE),
    ('5', MessageReference.QUOTE),
    (MessageReference.TPT, MessageReference.TPT),
])
def test_message_reference_parse(value, expected):
    assert MessageReference.parse(value) is expected


@pytest.mark.parametrize('value', ['nope', 999, True, None, 1.5])
def test_parse_rejects_unknown(value):
    with pytest.raises(ValueError):
        MessageReference.parse(value)


def test_other_enum_lookups():
    assert Field.parse('mdf_f_closeprice') is Field.CLOSEPRICE
    assert RequestClass.parse('MDF_RC_PRIIP') is RequestClass.PRIIP
    assert RequestType.parse('stream') is RequestType.STREAM
    assert MessageClass.parse('MDF_MC_QUOTE') is MessageClass.QUOTE
    assert Field.name_of(Field.CLOSEPRICE) == 'CLOSEPRICE'
    assert Field.name_of(99999) == '99999'
    assert MessageReference.name_of(99, default='?') == '?'


def test_constants_match_libmdf_1_0_30():
    assert Field.C_I_RATIO == 2631
    assert Field.MORNINGSTARATING is Field.MORNINGSTARRATING  # old misspelling stays an alias
    assert MessageReference.EET == 45 and MessageReference.TPT == 46
    assert RequestClass.EET == 28 and RequestClass.TPT == 29
    assert RequestType.DELETES == 4 and RequestType.CONTINUE == 5
    assert MessageClass.QUOTEEX == 33554432
    assert MessageClass(MessageClass.QUOTE | MessageClass.BASICDATA) & MessageClass.QUOTE


@pytest.mark.parametrize('url, expected', [
    ('host', 'host:9100'),
    ('host:9000', 'host:9000'),
    (['a', 'b:1'], 'a:9100,b:1'),
    ('a, b', 'a:9100,b:9100'),
    ('[::1]', '[::1]:9100'),
    ('[::1]:9000', '[::1]:9000'),
    ('::1', '[::1]:9100'),
])
def test_server_address(url, expected):
    assert server_address(url, 9100) == expected


def test_server_address_needs_a_server():
    with pytest.raises(ValueError):
        server_address([' ', ''], 9100)


class FakeLib:
    """Stands in for libmdf behind the lazy loader."""

    def __init__(self, raw_value: bytes):
        self.raw_value = raw_value

    def mdf_get_next_field(self, handle, tag, value):
        tag.value = 3
        value.value = self.raw_value
        return 1


def test_field_decode_replaces_invalid_utf8(monkeypatch):
    monkeypatch.setattr(_libmdf, '_lib', FakeLib(b'caf\xe9'))
    ok, tag, value = _libmdf.mdf_get_next_field(None)
    assert ok and tag == 3
    assert value == 'caf�'


class Recorder:
    """Replaces the message-building C calls in sync_client and records what is sent."""

    def __init__(self, monkeypatch):
        self.calls = []
        for name in ('mdf_message_add', 'mdf_message_add_list', 'mdf_message_add_numeric', 'mdf_message_add_string'):
            monkeypatch.setattr(sync_client, name, self._record(name))
        monkeypatch.setattr(sync_client, 'mdf_message_create', lambda: object())
        monkeypatch.setattr(sync_client, 'mdf_message_destroy', lambda message: None)
        monkeypatch.setattr(sync_client, 'mdf_message_send', lambda handle, message: True)

    def _record(self, name):
        def call(message, *args):
            self.calls.append((name, *args))
            return True
        return call


def connected_client() -> MDF:
    client = MDF('host', username='u', password='p')
    client._handle = object()
    client._connected = client._authenticated = True
    return client


def test_request_stream_with_id(monkeypatch):
    recorder = Recorder(monkeypatch)
    connected_client().request(['quote', RequestClass.BASICDATA, 21], '*', 'stream', request_id='r1')
    assert recorder.calls == [
        ('mdf_message_add', 0, MessageReference.REQUEST),
        ('mdf_message_add_list', Field.REQUESTCLASS, '1 4 21'),
        ('mdf_message_add_numeric', Field.REQUESTTYPE, '2'),
        ('mdf_message_add_string', Field.REQUESTID, 'r1'),
        ('mdf_message_add_list', Field.INSREFLIST, '*'),
    ]


def test_request_all_classes_by_request_type(monkeypatch):
    recorder = Recorder(monkeypatch)
    connected_client().request('*', [1146, 1147], RequestType.IMAGE)
    assert ('mdf_message_add_list', Field.REQUESTCLASS, '*') in recorder.calls
    assert ('mdf_message_add_numeric', Field.REQUESTTYPE, '1') in recorder.calls
    assert ('mdf_message_add_list', Field.INSREFLIST, '1146 1147') in recorder.calls


def test_stream_yields_pending_then_messages_with_mclass(monkeypatch):
    client = connected_client()
    pending = millistream_mdf.Message(ref=MessageReference.MESSAGESREFERENCE, instrument=1)
    client._pending.append(pending)

    consume_results = iter([1, -1])
    messages = iter([(True, MessageReference.QUOTE, 42), (False, 0, 0)])
    fields = iter([(True, Field.BIDPRICE, '1.5'), (True, Field.ASKPRICE, None), (False, 0, None)])
    monkeypatch.setattr(sync_client, 'mdf_consume', lambda handle, timeout: next(consume_results))
    monkeypatch.setattr(sync_client, 'mdf_get_next_message2', lambda handle: next(messages))
    monkeypatch.setattr(sync_client, 'mdf_get_next_field', lambda handle: next(fields))
    monkeypatch.setattr(sync_client, 'mdf_get_delay', lambda handle: 0)
    monkeypatch.setattr(sync_client, 'mdf_get_mclass', lambda handle: int(MessageClass.QUOTE))
    monkeypatch.setattr(sync_client, 'mdf_get_property', lambda handle, option: 11)  # disconnected

    received = []
    with pytest.raises(MDFConnectionError):
        for message in client.stream():
            received.append(message)
    assert received[0] is pending
    quote = received[1]
    assert (quote.ref, quote.instrument, quote.mclass) == (MessageReference.QUOTE, 42, MessageClass.QUOTE)
    assert quote.fields == {Field.BIDPRICE: '1.5', Field.ASKPRICE: None}


def test_set_property_accepts_float(monkeypatch):
    seen = []

    class Lib:
        def mdf_set_property(self, handle, option, value):
            seen.append(ctypes.cast(value, ctypes.POINTER(ctypes.c_int)).contents.value)
            return 1

    monkeypatch.setattr(_libmdf, '_lib', Lib())
    assert _libmdf.mdf_set_property(None, _libmdf.MDF_OPTION.HEARTBEAT_INTERVAL, 30.0)
    assert seen == [30]
