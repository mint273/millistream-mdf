"""
User-friendly exception classes for MDF operations with enhanced typing.
"""

from typing import Optional, Dict, Any, Literal
from dataclasses import dataclass


# Error code types
ErrorCode = Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
ConnectionErrorCode = Literal[6, 7, 8, 10, 11]
AuthenticationErrorCode = Literal[12]
LibraryErrorCode = Literal[1, 2, 3, 4, 5, 9]






@dataclass
class ErrorContext:
    """Context information for errors."""
    operation: str
    details: Optional[Dict[str, Any]] = None
    timestamp: Optional[float] = None


class MDFError(Exception):
    """Base exception for all MDF-related errors with enhanced context."""
    
    def __init__(self, message: str, context: Optional[ErrorContext] = None):
        super().__init__(message)
        self.context = context


class MDFConnectionError(MDFError):
    """Raised when connection to MDF server fails."""
    
    def __init__(self, message: str, error_code: Optional[ConnectionErrorCode] = None, 
                 context: Optional[ErrorContext] = None):
        super().__init__(message, context)
        self.error_code = error_code


class MDFAuthenticationError(MDFError):
    """Raised when authentication with MDF server fails."""
    
    def __init__(self, message: str, error_code: Optional[AuthenticationErrorCode] = None,
                 context: Optional[ErrorContext] = None):
        super().__init__(message, context)
        self.error_code = error_code


class MDFTimeoutError(MDFError):
    """Raised when operations timeout."""
    
    def __init__(self, message: str, timeout_duration: Optional[float] = None,
                 context: Optional[ErrorContext] = None):
        super().__init__(message, context)
        self.timeout_duration = timeout_duration


class MDFMessageError(MDFError):
    """Raised when message operations fail."""
    
    def __init__(self, message: str, message_type: Optional[str] = None,
                 context: Optional[ErrorContext] = None):
        super().__init__(message, context)
        self.message_type = message_type


class MDFConfigurationError(MDFError):
    """Raised when configuration is invalid."""
    
    def __init__(self, message: str, config_key: Optional[str] = None,
                 context: Optional[ErrorContext] = None):
        super().__init__(message, context)
        self.config_key = config_key


class MDFLibraryError(MDFError):
    """Raised when the underlying libmdf library encounters an error."""
    
    def __init__(self, message: str, error_code: Optional[LibraryErrorCode] = None,
                 context: Optional[ErrorContext] = None):
        super().__init__(message, context)
        self.error_code = error_code


# Error code mappings from MDF_ERROR enum
ERROR_CODE_MESSAGES = {
    0: "No error",
    1: "Out of memory",
    2: "Message out of bounds",
    3: "Template out of bounds", 
    4: "Unknown template",
    5: "Invalid argument",
    6: "Already connected",
    7: "Not connected",
    8: "Connection failed",
    9: "Message too large",
    10: "Connection idle",
    11: "Disconnected",
    12: "Authentication failed",
}


def get_error_message(error_code: ErrorCode) -> str:
    """Get human-readable error message for MDF error code."""
    return ERROR_CODE_MESSAGES.get(error_code, f"Unknown error (code: {error_code})")


def raise_for_error(error_code: ErrorCode, context: Optional[str] = None) -> None:
    """
    Raise appropriate exception based on MDF error code with enhanced typing.
    
    Args:
        error_code: The MDF error code
        context: Optional context string for the error
        
    Raises:
        MDFConnectionError: For connection-related errors
        MDFAuthenticationError: For authentication errors
        MDFLibraryError: For other library errors
    """
    if error_code == 0:  # No error
        return
    
    message = get_error_message(error_code)
    if context:
        message = f"{context}: {message}"
    
    error_context = ErrorContext(operation=context or "unknown") if context else None
    
    if error_code in [6, 7, 8, 10, 11]:  # Connection-related errors
        raise MDFConnectionError(message, error_code, error_context)
    elif error_code == 12:  # Authentication failed
        raise MDFAuthenticationError(message, error_code, error_context)
    elif error_code == 1:  # Out of memory
        raise MDFLibraryError(message, error_code, error_context)
    else:
        raise MDFLibraryError(message, error_code, error_context)
