"""
High-level Message class for representing MDF messages with enhanced typing.
"""

from dataclasses import dataclass, field
from typing import Any, Mapping, TypeVar, Sequence, Literal
from datetime import date, time, datetime
from .types import MessageProtocol, InstrumentSelection, MessageReference, FieldValue
from ._mappings import FIELD_TYPES, FIELD_TO_NAME
from ._constants import Field

T = TypeVar('T')






@dataclass
class Message(MessageProtocol):
    """
    Represents a message received from the MDF server with enhanced typing.
    
    Attributes:
        reference: MREF code
        instrument: Instrument reference ID
        fields: Dictionary of field_name: value pairs with typed access
        delay: Message delay type
    """
    ref: MessageReference
    instrument: InstrumentSelection
    fields: Mapping[int, FieldValue] = field(default_factory=dict)
    delay: int = 0

    def get(self, field: int, default: Any = None) -> Any:
        """
        Get field value by name.
        
        Args:
            field: Name of the field to retrieve
            default: Default value if field not found
            
        Returns:
            Field value or default
        """
        return self.fields.get(field, default)

    @property
    def parsed_fields(self) -> dict[str, str | int | float | date | time | datetime | list[str]]:
        """
        Parse and convert field values to their proper types.

        Property for "parse_fields()" method using default parameters.
        """
        return self.parse_fields()

    def parse_fields(
        self, 
        remap_keys: bool = True, 
        convert_types: Sequence[Literal['str', 'int', 'float', 'date', 'time', 'datetime', 'list']] = (
            'str', 'int', 'float', 'date', 'time', 'datetime', 'list'
        ),
        on_field_missing: Literal['raise', 'ignore', 'skip'] = 'ignore',
        list_delimiter: str = ' '
    ) -> dict[str | int, str | int | float | date | time | datetime | list[str]]:
        """
        Parse and convert field values to their proper types.
        
        Args:
            remap_keys: If True, use lowercase field names as keys; else use field IDs
            convert_types: Which types to convert ('str', 'int', 'float', 'date', 'time', 'datetime', 'list')
            on_field_missing: How to handle unmapped fields ('raise', 'ignore', 'skip')
            list_delimiter: Delimiter to split list values on
        
        Returns:
            Dictionary with converted values
        """
        result: dict[str | int, str | int | float | date | time | datetime | list[str]] = {}
        allowed_types = set(convert_types)
        
        for field_id, value in self.fields.items():
            # Get field key (string name or int ID)
            if remap_keys:
                try:
                    key = FIELD_TO_NAME.get(Field(field_id), str(field_id))
                except ValueError:
                    key = str(field_id)
            else:
                key = field_id
            
            # Get expected type
            try:
                expected_type = FIELD_TYPES.get(Field(field_id))
            except ValueError:
                expected_type = None
            
            # Handle missing type
            if expected_type is None:
                if on_field_missing == 'raise':
                    raise ValueError(f"No type mapping for field '{field_id}'!")
                elif on_field_missing == 'skip':
                    continue
                else:
                    result[key] = value
                    continue
            
            # Check if we should convert this type
            type_name = expected_type.__name__ if expected_type in (str, int, float, date, time, datetime, list) else 'str'
            
            if type_name not in allowed_types:
                result[key] = value
                continue
            
            # Convert value
            try:
                result[key] = self._convert(value, expected_type, list_delimiter)
            except (ValueError, TypeError):
                if on_field_missing == 'raise':
                    raise
                result[key] = value
        
        return result
    
    @staticmethod
    def _convert(value: Any, target_type: type, list_delimiter: str = ' ') -> FieldValue:
        """Convert value to target type."""
        if value is None or isinstance(value, target_type):
            return value
        
        if target_type == str:
            return str(value)
        elif target_type == int:
            return int(float(value)) if isinstance(value, str) else int(value)
        elif target_type == float:
            return float(value)
        elif target_type == date:
            return date.fromisoformat(value.strip()) if isinstance(value, str) else value
        elif target_type == time:
            # Handle nanosecond precision by truncating to microseconds
            if isinstance(value, str):
                v = value.strip()
                if '.' in v and v.count(':') >= 2:
                    time_part, frac = v.rsplit('.', 1)
                    v = f"{time_part}.{frac[:6]}"  # Truncate to 6 digits (microseconds)
                return time.fromisoformat(v)
            return value
        elif target_type == datetime:
            # Handle datetime with microsecond precision
            if isinstance(value, str):
                v = value.strip()
                # Handle space separator (convert to T for ISO format)
                v = v.replace(' ', 'T')
                if '.' in v:
                    dt_part, frac = v.rsplit('.', 1)
                    v = f"{dt_part}.{frac[:6]}"  # Truncate to 6 digits (microseconds)
                return datetime.fromisoformat(v)
            return value
        elif target_type == list:
            if isinstance(value, str):
                return value.split(list_delimiter)
            return value
        return value
    
    def __getitem__(self, field: int) -> Any:
        """Allow dict-like access to fields."""
        return self.fields[field]
    
    def __contains__(self, field: int) -> bool:
        """Check if field exists in message."""
        return field in self.fields
    
    def __str__(self) -> str:
        """String representation of the message."""
        field_str = ", ".join(f"{k}={v}" for k, v in self.fields.items())
        return f"Message(reference='{self.reference}', instrument={self.instrument}, fields=[{field_str}])"
    
    def __repr__(self) -> str:
        """Detailed representation of the message."""
        return (f"Message(reference='{self.reference}', instrument={self.instrument}, "
                f"delay={self.delay}, fields={self.fields})")

