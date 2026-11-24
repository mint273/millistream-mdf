"""
Python wrapper for libmdf C SDK.

This package provides a high-level, intuitive Python API for connecting to
Millistream Data Feed servers and consuming real-time financial data.

Example:
    from millistream_mdf import MDF
    
    from millistream_mdf import MDF, RequestClass

    with MDF(url=['server1:9100', 'server2:9100'], username='user', password='pass') as session:
        for message in session.subscribe([RequestClass.QUOTE, RequestClass.TRADE], '*', 'stream'):
            print(f"{MessageReference.name_of(message.ref)} {message.instrument}: {message.fields}")

The constants (MessageReference, Field, RequestClass, ...) import without libmdf; the C
library is loaded on first use.
"""

from .sync_client import MDF
from .async_client import AsyncMDF
from .message import Message
from .exceptions import (
    MDFError,
    MDFConnectionError,
    MDFAuthenticationError,
    MDFTimeoutError,
    MDFMessageError,
    MDFConfigurationError,
    MDFLibraryError,
)
from ._constants import (
    # Main enums for user API
    MessageReference,
    Field,
    RequestClass,
    RequestType,
    MessageClass,
    DelayType,
)
from ._libmdf import load_libmdf
from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version('millistream-mdf')
except PackageNotFoundError:
    __version__ = '0.0.0.dev0'

__author__ = "Gustav Frison"
__email__ = "gustav.frison@millistream.com"

__all__ = [
    'MDF', 'AsyncMDF', 'RequestType', 'RequestClass', 'MessageReference', 'MessageClass', 'DelayType',
    'Field', 'Message', 'load_libmdf',
    'MDFError', 'MDFConnectionError', 'MDFAuthenticationError', 'MDFTimeoutError', 'MDFMessageError',
    'MDFConfigurationError', 'MDFLibraryError',
]