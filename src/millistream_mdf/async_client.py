"""
Async MDF client for connecting to Millistream servers with asyncio support.
"""

import asyncio
from typing import AsyncGenerator, Optional, Literal, Mapping
from datetime import date, datetime
from collections.abc import Sequence
import os

from ._libmdf import (
    mdf_create, mdf_destroy, mdf_connect, mdf_disconnect, mdf_consume,
    mdf_get_next_message2, mdf_get_delay, mdf_get_next_field,
    mdf_get_property, mdf_set_property, mdf_message_create, mdf_message_destroy,
    mdf_message_add, mdf_message_add_string, mdf_message_add_numeric, 
    mdf_message_add_list, mdf_message_send,
    MDF_OPTION, mdf_t
)
from ._constants import MessageReference, RequestClass, Field
from ._mappings import SUB_TYPES
from .types import BatchItem

from .exceptions import (
    MDFError, MDFConnectionError, MDFAuthenticationError, MDFTimeoutError,
    MDFMessageError, raise_for_error
)
from .message import Message
from .message_builder import MessageBuilder








class AsyncMDF:
    """
    Async client for connecting to Millistream Data Feed servers.
    
    Provides an async/await API for non-blocking I/O operations. All blocking
    operations (connect, consume, send) are executed in a thread pool executor
    to avoid blocking the event loop.
    
    Example:
        async with AsyncMDF(url='server', username='user', password='pass') as session:
            async for message in session.subscribe(request_classes=[RequestClass.QUOTE], instruments='*'):
                print(f"{message.type}: {message.fields}")
    """
    
    def __init__(
        self, 
        url: str, 
        port: int = 9100, 
        username: Optional[str] = None, 
        password: Optional[str] = None, 
        heartbeat_interval: int | float = 30, 
        connect_timeout: int | float = 10, 
        tcp_nodelay: bool = True, 
        no_encryption: bool = False,
        executor: Optional[asyncio.AbstractEventLoop] = None
    ):
        """
        Initialize async MDF client.
        
        Args:
            url: Server URL
            port: Server port (default: 9100)
            username: Username for authentication
            password: Password for authentication
            heartbeat_interval: Heartbeat interval in seconds (default: 30)
            connect_timeout: Connection timeout in seconds (default: 10)
            tcp_nodelay: Disable TCP Nagle algorithm (default: True)
            no_encryption: Disable encryption (default: False)
            executor: Optional executor for blocking operations (default: ThreadPoolExecutor)
        """
        self.url = url
        self.port = port
        self.username = username or os.environ.get('MDF_USERNAME')
        self.password = password or os.environ.get('MDF_PASSWORD')

        if not self.username or not self.password:
            raise MDFError(
                "Username and password are required. Either provide them as arguments "
                "or set the 'MDF_USERNAME' and 'MDF_PASSWORD' environment variables."
            )
        
        # Default options
        self.heartbeat_interval = heartbeat_interval
        self.connect_timeout = connect_timeout
        self.tcp_nodelay = tcp_nodelay
        self.no_encryption = no_encryption
        
        # Internal state
        self._handle: Optional[mdf_t] = None
        self._connected = False
        self._authenticated = False
        self._executor = executor
        self._loop: Optional[asyncio.AbstractEventLoop] = None
    
    async def __aenter__(self):
        """Async context manager entry."""
        await self.connect()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.disconnect()
    
    async def connect(self) -> None:
        """
        Connect to the MDF server and authenticate.
        
        Raises:
            MDFConnectionError: If connection fails
            MDFAuthenticationError: If authentication fails
        """
        if self._connected:
            return
        
        self._loop = asyncio.get_event_loop()
        
        try:
            # Run blocking operations in executor
            self._handle = await self._run_in_executor(mdf_create)
            if not self._handle:
                raise MDFConnectionError("Failed to create MDF handle")
            
            # Set connection options
            self._set_connection_options()
            
            # Connect to server (blocking operation)
            success = await self._run_in_executor(
                mdf_connect, self._handle, f"{self.url}:{self.port}"
            )
            if not success:
                raise MDFConnectionError(f"Failed to connect to '{self.url}:{self.port}'")
            
            self._connected = True
            
            # Authenticate
            await self._authenticate()
            self._authenticated = True
            
        except Exception as e:
            await self._cleanup()
            if isinstance(e, MDFError):
                raise
            raise MDFConnectionError(f"Connection failed: {e}")
    
    async def disconnect(self) -> None:
        """Disconnect from the MDF server."""
        if not self._connected:
            return
        
        try:
            # Send logoff if authenticated
            if self._authenticated:
                await self._send_logoff()
            
            # Disconnect (blocking operation)
            await self._run_in_executor(mdf_disconnect, self._handle)
            
        except Exception:
            pass  # Ignore errors during disconnect
        finally:
            await self._cleanup()
    
    async def subscribe(
        self, 
        request_classes: Sequence[int], 
        instruments: Sequence[int] | Literal['*'] = '*', 
        subscription_mode: Literal['image', 'stream', 'full'] = 'full', 
        timeout: int = 1,
        unsubscribe_on_exit: bool = False
    ) -> AsyncGenerator[Message, None]:
        """
        Subscribe to data streams and yield messages asynchronously.
        
        This sends a REQUEST message (MessageReference.REQUEST) to the server with the
        specified RequestClass values in the REQUESTCLASS field.
        
        Args:
            request_classes: List of RequestClass values to subscribe to 
                (e.g., [RequestClass.QUOTE, RequestClass.TRADE, RequestClass.BASICDATA])
                These specify WHAT DATA you want to receive.
            instruments: Instrument references to subscribe to. Can be:
                - '*': All instruments
                - Sequence of integers: Numeric instrument IDs (e.g., [1146, 1147])
            subscription_mode: Subscription mode ('image', 'stream', or 'full')
            timeout: Timeout in seconds for consume operations
            unsubscribe_on_exit: Unsubscribe from all streams when the context manager is exited (only relevant if the call is iterated).
            
        Yields:
            Message objects containing the received data. Each message will have a
            MessageReference type (e.g., MessageReference.QUOTE) corresponding to the
            type of data received.
            
        Raises:
            MDFError: If subscription fails
            
        Note:
            RequestClass values specify what to subscribe to (e.g., RequestClass.QUOTE).
            Received messages will have MessageReference types (e.g., MessageReference.QUOTE).
        """
        if not self._connected or not self._authenticated:
            raise MDFError("Not connected or authenticated")
        
        # Send subscription request
        await self._send_subscription_request(request_classes, instruments, subscription_mode)
        
        # Stream messages
        async for message in self.stream(timeout, unsubscribe_on_exit):
            yield message
    
    async def unsubscribe(self, request_classes: Sequence[int] | Literal['*'] = '*', instruments: Sequence[int] | Literal['*'] = '*') -> None:
        """
        Unsubscribe from data streams asynchronously.
        
        This sends an UNSUBSCRIBE message (MessageReference.UNSUBSCRIBE) to the server
        to stop receiving realtime data for the specified request classes and instruments.
        
        You can unsubscribe from a subset of your active subscriptions - the lists don't
        have to match previous subscription requests exactly.

        Args:
            request_classes: List of RequestClass values to unsubscribe from, or '*' for all.
                Examples: [RequestClass.QUOTE, RequestClass.TRADE] or '*'
            instruments: List of instrument references to unsubscribe from, or '*' for all.
                Examples: [1146, 1147] or '*'
                
        Raises:
            MDFError: If not connected or authenticated
            MDFMessageError: If unsubscription request fails
            
        Example:
            # Unsubscribe from specific instruments
            await client.unsubscribe(
                request_classes=[RequestClass.QUOTE],
                instruments=[1146, 1147]
            )
            
            # Unsubscribe from all quotes
            await client.unsubscribe(request_classes=[RequestClass.QUOTE], instruments='*')
            
            # Unsubscribe from everything
            await client.unsubscribe()
        """
        if not self._connected or not self._authenticated:
            raise MDFError("Not connected or authenticated")
        
        await self._send_unsubscription_request(request_classes, instruments)
    
    async def send(
        self, 
        mref: int, 
        instrument: int, 
        fields: Mapping[int, str | int | float | date | datetime | list[str]], 
        delay: int = 0
    ) -> bool:
        """
        Send a message to the server with the specified fields.
        
        This is a convenience method that creates a message, adds fields, sends it,
        and cleans up automatically.
        
        Args:
            mref: Message reference (e.g., MessageReference.QUOTE, MessageReference.TRADE)
            instrument: Instrument reference
            fields: Dictionary mapping field names to values
            delay: Optional delay parameter (default: 0)
            
        Returns:
            True if the message was sent successfully
            
        Raises:
            MDFError: If not connected or authenticated
            MDFMessageError: If message construction or sending fails
            
        Example:
            await client.send(
                mref=MessageReference.QUOTE,
                instrument=12345,
                fields={
                    Field.BIDPRICE: '100.50',
                    Field.ASKPRICE: '100.55',
                    Field.BIDQUANTITY: 1000,
                    Field.ASKQUANTITY: 500,
                }
            )
        """
        if not self._connected or not self._authenticated:
            raise MDFError("Not connected or authenticated")
        
        # Build message synchronously (fast, no I/O)
        with MessageBuilder() as builder:
            builder.add_message(mref, instrument, delay)
            
            for field_name, value in fields.items():
                builder.add_field(field_name, value)
            
            # Send in executor (blocking I/O)
            return await self._run_in_executor(builder.send, self._handle)
    
    async def send_batch(self, messages: Sequence[BatchItem]) -> bool:
        """
        Send multiple messages in a single batch.
        
        This is more efficient than calling send() multiple times as it reuses
        the message handle and sends all messages together.
        
        Args:
            messages: List of message dictionaries with 'mref', 'instrument', 
                     'fields', and optionally 'delay'
                     
        Returns:
            True if all messages were sent successfully
            
        Raises:
            MDFError: If not connected or authenticated
            MDFMessageError: If message construction or sending fails
            
        Example:
            await client.send_batch([
                {
                    'mref': MessageReference.QUOTE,
                    'instrument': 12345,
                    'fields': {Field.BIDPRICE: '100.50', Field.ASKPRICE: '100.55'},
                },
                {
                    'mref': MessageReference.TRADE,
                    'instrument': 12345,
                    'fields': {Field.TRADEPRICE: '100.52', Field.TRADEQUANTITY: 1000},
                }
            ])
        """
        if not self._connected or not self._authenticated:
            raise MDFError("Not connected or authenticated")
        
        with MessageBuilder() as builder:
            for msg in messages:
                # Add the message
                builder.add_message(
                    msg['mref'], 
                    msg['instrument'], 
                    msg.get('delay', 0)
                )

                # Add all fields
                for field, value in msg['fields'].items():
                    builder.add_field(field, value)
            
            # Send in executor (blocking I/O)
            return await self._run_in_executor(builder.send, self._handle)
    
    def create_message_builder(self) -> MessageBuilder:
        """
        Create a new MessageBuilder for advanced message construction.
        
        Use this when you need more control over message construction,
        such as building messages incrementally or reusing the builder.
        
        Returns:
            A new MessageBuilder instance (must be used as context manager)
            
        Example:
            with client.create_message_builder() as builder:
                builder.add_message(mref=MessageReference.QUOTE, instrument=12345)
                builder.add_field('bidprice', '100.50')
                builder.add_field('askprice', '100.55')
                # Send with await
                await asyncio.get_event_loop().run_in_executor(
                    None, builder.send, client._handle
                )
        """
        return MessageBuilder()
    
    async def stream(self, timeout: int = 1, unsubscribe_on_exit: bool = False) -> AsyncGenerator[Message, None]:
        """
        Stream messages from the server asynchronously.
        
        Args:
            timeout: Timeout in seconds for consume operations
            unsubscribe_on_exit: Unsubscribe from all streams when the generator exits
            
        Yields:
            Message objects containing the received data
        """
        if not self._connected:
            raise MDFError("Not connected!")
        
        try:
            while True:
                try:
                    # Consume data from server (blocking operation)
                    result = await self._run_in_executor(mdf_consume, self._handle, timeout)
                    
                    if result == -1:  # Error
                        error_code = mdf_get_property(self._handle, MDF_OPTION.ERROR)
                        raise_for_error(error_code, "Consume operation failed!")
                    
                    if result == 1:  # Messages available
                        # Process all available messages
                        while True:
                            has_message, mref, instrument_id = mdf_get_next_message2(self._handle)
                            if not has_message:
                                break
                            
                            delay = mdf_get_delay(self._handle)
                            
                            # Collect all fields for this message
                            fields: dict[int, Optional[str]] = {}
                            while True:
                                has_field, tag, value = mdf_get_next_field(self._handle)
                                if not has_field:
                                    break
                                fields[tag] = value
                            
                            yield Message(
                                ref=mref,
                                instrument=instrument_id,
                                fields=fields,
                                delay=delay
                            )
                    
                    elif result == 0:  # Timeout
                        # Yield control to event loop
                        await asyncio.sleep(0)
                        continue
                        
                except asyncio.CancelledError:
                    break
                except Exception as e:
                    if isinstance(e, MDFError):
                        raise
                    raise MDFError(f"Streaming error: {e}")
        finally:
            if unsubscribe_on_exit:
                await self.unsubscribe()
    
    def _set_connection_options(self) -> None:
        """Set connection options on the MDF handle."""
        if self.heartbeat_interval:
            mdf_set_property(self._handle, MDF_OPTION.HEARTBEAT_INTERVAL, self.heartbeat_interval)
        
        if self.connect_timeout:
            mdf_set_property(self._handle, MDF_OPTION.CONNECT_TIMEOUT, self.connect_timeout)
        
        if self.tcp_nodelay:
            mdf_set_property(self._handle, MDF_OPTION.TCP_NODELAY, 1)
        
        if self.no_encryption:
            mdf_set_property(self._handle, MDF_OPTION.NO_ENCRYPTION, 1)
    
    async def _authenticate(self) -> None:
        """Send authentication (logon) message and wait for response."""
        # Create logon message
        message = mdf_message_create()
        if not message:
            raise MDFAuthenticationError("Failed to create logon message!")
        
        try:
            # Add logon message
            mdf_message_add(message, 0, MessageReference.LOGON)
            mdf_message_add_string(message, Field.USERNAME, self.username)
            mdf_message_add_string(message, Field.PASSWORD, self.password)
            mdf_message_add_string(message, Field.S1, f"Python MDF Client")
            
            # Send logon (blocking operation in executor)
            success = await self._run_in_executor(mdf_message_send, self._handle, message)
            if not success:
                raise MDFAuthenticationError("Failed to send logon message!")
            
            # Wait for logon greeting
            await self._wait_for_logon_greeting()
            
        finally:
            mdf_message_destroy(message)
    
    async def _wait_for_logon_greeting(self, timeout: int = 10) -> None:
        """Wait for LOGONGREETING response."""
        start_time = asyncio.get_event_loop().time()
        
        while asyncio.get_event_loop().time() - start_time < timeout:
            result = await self._run_in_executor(mdf_consume, self._handle, 1)
            
            if result == -1:  # Error
                error_code = mdf_get_property(self._handle, MDF_OPTION.ERROR)
                raise_for_error(error_code, "Authentication failed!")
            
            if result == 1:  # Messages available
                while True:
                    has_message, mref, _ = mdf_get_next_message2(self._handle)
                    if not has_message:
                        break
                    
                    if mref == MessageReference.LOGONGREETING:
                        return  # Success
                    elif mref == MessageReference.LOGOFF:
                        raise MDFAuthenticationError("Server sent logoff during authentication!")
            
            # Small delay to avoid tight loop
            await asyncio.sleep(0.1)
        
        raise MDFTimeoutError("Authentication timeout")
    
    async def _send_subscription_request(self, request_classes: Sequence[RequestClass], instruments: Sequence[int] | Literal['*'], subscription_mode: Literal['image', 'stream', 'full']) -> None:
        """Send subscription request message."""
        message = mdf_message_create()
        if not message:
            raise MDFMessageError("Failed to create subscription message!")
        
        try:
            # Add request message
            mdf_message_add(message, 0, MessageReference.REQUEST)            
            mdf_message_add_list(message, Field.REQUESTCLASS, ' '.join(str(mc) for mc in request_classes))
            
            # Add subscription mode (request type)
            if subscription_mode in SUB_TYPES:
                request_type = SUB_TYPES[subscription_mode]
                mdf_message_add_numeric(message, Field.REQUESTTYPE, str(request_type))
            else:
                raise MDFMessageError(f"Unknown subscription mode: {subscription_mode}")
            
            # Add instrument references
            insref_str = ' '.join(str(ref) for ref in instruments) if instruments != '*' else '*'
            
            mdf_message_add_list(message, Field.INSREFLIST, insref_str)
            
            # Send request (blocking operation in executor)
            success = await self._run_in_executor(mdf_message_send, self._handle, message)
            if not success:
                raise MDFMessageError("Failed to send subscription request!")
            
        finally:
            mdf_message_destroy(message)
    
    async def _send_unsubscription_request(self, request_classes: Sequence[RequestClass] | Literal['*'], instruments: Sequence[int] | Literal['*']) -> None:
        """Send unsubscription request message."""
        message = mdf_message_create()
        if not message:
            raise MDFMessageError("Failed to create unsubscription message!")
        
        try:
            # Add unsubscribe message
            mdf_message_add(message, 0, MessageReference.UNSUBSCRIBE)
            
            # Add request classes
            if request_classes == '*':
                rc_str = '*'
            else:
                rc_str = ' '.join(str(rc) for rc in request_classes)
            mdf_message_add_list(message, Field.REQUESTCLASS, rc_str)
            
            # Add instrument references
            if instruments == '*':
                insref_str = '*'
            else:
                insref_str = ' '.join(str(ref) for ref in instruments)
            mdf_message_add_list(message, Field.INSREFLIST, insref_str)
            
            # Send unsubscribe request (blocking operation in executor)
            success = await self._run_in_executor(mdf_message_send, self._handle, message)
            if not success:
                raise MDFMessageError("Failed to send unsubscription request!")
            
        finally:
            mdf_message_destroy(message)
    
    async def _send_logoff(self) -> None:
        """Send logoff message."""
        message = mdf_message_create()
        if not message:
            return
        
        try:
            mdf_message_add(message, 0, MessageReference.LOGOFF)
            await self._run_in_executor(mdf_message_send, self._handle, message)
        finally:
            mdf_message_destroy(message)
    
    async def _cleanup(self) -> None:
        """Clean up resources."""
        if self._handle:
            await self._run_in_executor(mdf_destroy, self._handle)
            self._handle = None
        
        self._connected = False
        self._authenticated = False
    
    async def _run_in_executor(self, func, *args):
        """Run a blocking function in the executor."""
        if self._loop is None:
            self._loop = asyncio.get_event_loop()
        return await self._loop.run_in_executor(self._executor, func, *args)
    
    @property
    def is_connected(self) -> bool:
        """Check if connected to server."""
        return self._connected
    
    @property
    def is_authenticated(self) -> bool:
        """Check if authenticated with server."""
        return self._authenticated