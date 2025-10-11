"""
Type definitions for MDF client using Literal types and advanced typing features.

This module provides strict typing for main MDF parameters with enhanced type safety.
"""

from typing import Literal, TypeVar, Protocol, runtime_checkable, Sequence, TypedDict, NotRequired
from datetime import date, datetime


# Type Variables for generic typing
T = TypeVar('T')
T_co = TypeVar('T_co', covariant=True)




class BatchItem(TypedDict):
    """
    Batch item for sending a batch of messages. Same parameters as for the "send()" method.
    
    The 'delay' field is optional and defaults to 0 if not provided.
    """
    mref: int
    instrument: int
    fields: dict[str, str | int | float | date | datetime | list[str]]
    delay: NotRequired[int]



type Insref = int
type InstrumentSelection = Sequence[Insref] | Literal['*']
type MessageReference = int
type FieldItem = str | int | float | date | datetime
type FieldValue = FieldItem | list[FieldItem]

    

# Protocol definitions for interface typing
@runtime_checkable
class MessageProtocol(Protocol):
    """Protocol for message-like objects."""
    reference: MessageReference
    instrument: InstrumentSelection
    fields: dict[str, FieldValue]
    
    def get(self, field_name: str, default: FieldValue = None) -> FieldValue: ...
    def __getitem__(self, field_name: str) -> FieldValue: ...
    def __contains__(self, field_name: str) -> bool: ...
