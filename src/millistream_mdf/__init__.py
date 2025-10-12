"""
Python wrapper for libmdf C SDK.

This package provides a high-level, intuitive Python API for connecting to
Millistream Data Feed servers and consuming real-time financial data.

Example:
    from millistream_mdf import MDF
    
    with MDF(url='server:port', username='user', password='pass') as session:
        for message in session.subscribe(message_classes=['quote', 'trade'], insrefs='*'):
            print(f"{message.type}: {message.fields}")
"""

from .sync_client import MDF
from .async_client import AsyncMDF
from .message_builder import MessageBuilder
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
    RequestType
)

__version__ = "0.1.4"
__author__ = "Gustav Frison"
__email__ = "gustav.frison@millistream.com"

__all__ = [
    'MDF', 'MDFAsync', 'RequestType', 'RequestClass', 'MessageReference', 'Field', 'BatchItem'
]
