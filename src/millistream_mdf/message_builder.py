"""
MessageBuilder class for constructing outgoing MDF messages.
"""

from typing import Optional, Literal
from datetime import date, datetime

from ._libmdf import (
    mdf_message_create, mdf_message_destroy, mdf_message_add, mdf_message_add2,
    mdf_message_add_string, mdf_message_add_string2, mdf_message_add_numeric, 
    mdf_message_add_int, mdf_message_add_uint,
    mdf_message_add_list, mdf_message_add_date, mdf_message_add_date2,
    mdf_message_add_time, mdf_message_add_time2, mdf_message_add_time3,
    mdf_message_send, mdf_message_reset,
    mdf_t, mdf_message_t
)
from .exceptions import MDFMessageError
from .types import FieldValue








class MessageBuilder:
    """
    Builder class for constructing outgoing MDF messages with a clean API.
    
    This class handles the low-level message creation and field addition,
    providing a high-level interface for sending data to the MDF server.
    
    Example:
        with MessageBuilder() as builder:
            builder.add_message(MessageReference.QUOTE, instrument=12345)
            builder.add_field(Field.BIDPRICE, 100.50)
            builder.add_field(Field.ASKPRICE, 100.55)
            builder.send(mdf_handle)
    """
    
    def __init__(self):
        """Initialize a new message builder."""
        self._handle: Optional[mdf_message_t] = None
        self._message_count = 0
    
    def __enter__(self):
        """Context manager entry."""
        self._handle = mdf_message_create()
        if not self._handle:
            raise MDFMessageError("Failed to create message handle!")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        if self._handle:
            mdf_message_destroy(self._handle)
            self._handle = None
    
    def add_message(self, mref: int, instrument: int, delay: int = 0) -> 'MessageBuilder':
        """
        Add a new message to the builder.
        
        Args:
            mref: Message reference (e.g., MessageReference.QUOTE, MessageReference.TRADE)
            instrument: Instrument reference
            delay: Optional delay parameter (default: 0)
            
        Returns:
            Self for method chaining
            
        Raises:
            MDFMessageError: If message addition fails
        """
        if not self._handle:
            raise MDFMessageError("MessageBuilder not initialized. Use as context manager.")
        
        # Add message to chain
        if delay > 0:
            success = mdf_message_add2(self._handle, instrument, mref, delay)
        else:
            success = mdf_message_add(self._handle, instrument, mref)
        
        if not success:
            raise MDFMessageError(f"Failed to add message (class={mref}, instrument={instrument})")
        
        self._message_count += 1
        return self
    
    def add_field(self, field: int, value: Literal[str, int, float, date, datetime, list[str]]) -> 'MessageBuilder':
        """
        Add a field to the current message.
        
        Args:
            field: Field Tag (e.g., Field.BIDPRICE, Field.ASKPRICE, Field.SYMBOL)
            value: Field value - can be:
                - Simple types: str, int, float (auto-detected)
                - Typed dict: NumericField, StringField, IntegerField, DateField, TimeField, ListField
                
        Returns:
            Self for method chaining
            
        Raises:
            MDFMessageError: If field addition fails
        """
        if not self._handle:
            raise MDFMessageError("MessageBuilder not initialized. Use as context manager.")
        
        if self._message_count == 0:
            raise MDFMessageError("No message added. Call add_message() first.")
        
        success = self._add_field_value(field, value)
        
        if not success:
            raise MDFMessageError(f"Failed to add field {field}={value}")
        
        return self
    
    def _add_field_value(self, field: int, value: FieldValue) -> bool:
        """Add a field value using the appropriate low-level function."""
        # Handle simple types (auto-detect)
        if isinstance(value, str):
            # String values - use string type
            return mdf_message_add_string(self._handle, field, value)
        
        elif isinstance(value, (int, float)):
            # Numeric values - use numeric field type for compression
            return mdf_message_add_numeric(self._handle, field, str(value))

        elif isinstance(value, date):
            # Date values - use date field type
            return mdf_message_add_date(self._handle, field, f"{value.year}-{value.month}-{value.day}")
        
        elif isinstance(value, datetime):
            # Time values - use time field type
            return mdf_message_add_time(self._handle, field, f"{value.hour}:{value.minute}:{value.second}.{value.microsecond}")
        
        elif isinstance(value, list):
            # List values - use list field type
            return mdf_message_add_list(self._handle, field, ' '.join(str(item) for item in value))
        
        return False
    
    def send(self, handle: mdf_t) -> bool:
        """
        Send all messages in the builder to the server.
        
        Args:
            handle: MDF connection handle
            
        Returns:
            True if messages were sent successfully
            
        Raises:
            MDFMessageError: If sending fails
        """
        if not self._handle:
            raise MDFMessageError("MessageBuilder not initialized. Use as context manager.")
        
        if self._message_count == 0:
            raise MDFMessageError("No messages to send. Call add_message() first.")
        
        success = mdf_message_send(handle, self._handle)
        if not success:
            raise MDFMessageError("Failed to send messages")
        
        return True
    
    def reset(self) -> 'MessageBuilder':
        """
        Reset the builder for reuse (clears all messages but keeps memory allocated).
        
        Returns:
            Self for method chaining
        """
        if self._handle:
            mdf_message_reset(self._handle)
            self._message_count = 0
        return self
    
    def get_message_count(self) -> int:
        """Get the number of messages currently in the builder."""
        return self._message_count

