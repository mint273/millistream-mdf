"""
Low-level ctypes bindings for libmdf C library with enhanced typing.
This module handles library loading and provides raw C API access with improved type safety.
"""

import ctypes
import ctypes.util
import glob
import os
import sys
from typing import Optional, Union, Tuple, Literal, overload, Generator

# C type definitions
c_int = ctypes.c_int
c_long = ctypes.c_long
c_longlong = ctypes.c_longlong
c_uint = ctypes.c_uint
c_uint16 = ctypes.c_uint16
c_uint32 = ctypes.c_uint32
c_uint64 = ctypes.c_uint64
c_char_p = ctypes.c_char_p
c_void_p = ctypes.c_void_p
c_size_t = ctypes.c_size_t

# Opaque handle types
mdf_t = c_void_p
mdf_message_t = c_void_p

# Enums from mdf.h
class MDF_OPTION:
    FD = 0
    ERROR = 1
    RCV_BYTES = 2
    SENT_BYTES = 3
    DATA_CALLBACK_FUNCTION = 4
    DATA_CALLBACK_USERDATA = 5
    STATUS_CALLBACK_FUNCTION = 6
    STATUS_CALLBACK_USERDATA = 7
    CONNECT_TIMEOUT = 8
    HEARTBEAT_INTERVAL = 9
    HEARTBEAT_MAX_MISSED = 10
    TCP_NODELAY = 11
    NO_ENCRYPTION = 12
    TIME_DIFFERENCE = 13
    BIND_ADDRESS = 14
    TIME_DIFFERENCE_NS = 15
    CRYPT_DIGESTS = 16
    CRYPT_CIPHERS = 17
    CRYPT_DIGEST = 18
    CRYPT_CIPHER = 19
    TIMEOUT = 20
    HANDLE_DELAY = 21
    RBUF_SIZE = 22
    RBUF_MAXSIZE = 23
    CONNECTED_HOST = 24
    CONNECTED_IP = 25

class MDF_MSG_OPTION:
    UTF8 = 0
    COMPRESSION = 1
    DELAY = 2

class MDF_ERROR:
    NO_ERROR = 0
    NO_MEM = 1
    MSG_OOB = 2
    TEMPLATE_OOB = 3
    UNKNOWN_TEMPLATE = 4
    ARGUMENT = 5
    CONNECTED = 6
    NOT_CONNECTED = 7
    CONNECT = 8
    MSG_TO_LARGE = 9
    CONNECTION_IDLE = 10
    DISCONNECTED = 11
    AUTHFAIL = 12

class MDF_CONN_STATUS:
    LOOKUP = 0
    CONNECTING = 1
    CONNECTED = 2
    DISCONNECTED = 3
    READYTOLOGON = 4
    SND_HB_REQ = 5
    RCV_HB_REQ = 6
    RCV_HB_RES = 7


def _find_libmdf() -> Generator[str, None, None]:
    """Find the libmdf shared library."""
    # Check environment variable first
    if 'LIBMDF_PATH' in os.environ:
        path = os.environ['LIBMDF_PATH']
        if os.path.exists(path):
            yield path
    
    # Check common locations
    locations: list[str] = []
    
    if sys.platform == 'darwin':  # macOS
        locations.extend([
            '/usr/local/lib/libmdf.dylib',
            '/opt/homebrew/lib/libmdf.dylib',
            '/usr/lib/libmdf.dylib',
        ])
    elif sys.platform.startswith('linux'):
        # Common library directories on Linux
        lib_dirs = [
            '/usr/lib',
            '/usr/local/lib',
            '/usr/lib/x86_64-linux-gnu',
            '/usr/lib/aarch64-linux-gnu',
            '/usr/lib/i386-linux-gnu',
            '/usr/lib64',
        ]
        
        def parse_version(path: str) -> tuple[int, ...]:
            """Extract version numbers from library path for sorting."""
            basename = os.path.basename(path)
            # Remove 'libmdf.so' prefix to get version part
            if basename == 'libmdf.so':
                return ()  # No version
            version_str = basename.replace('libmdf.so.', '')
            try:
                # Parse version numbers (e.g., "0.13.0" -> (0, 13, 0))
                return tuple(int(x) for x in version_str.split('.'))
            except (ValueError, AttributeError):
                return ()
        
        # Dynamically search for libmdf.so* in each directory
        for lib_dir in lib_dirs:
            if os.path.isdir(lib_dir):
                pattern = os.path.join(lib_dir, 'libmdf.so*')
                matches = glob.glob(pattern)
                if matches:
                    # Sort by version number (highest version first)
                    matches.sort(key=lambda x: parse_version(x), reverse=True)
                    locations.extend(matches)
                    
    elif sys.platform == 'win32':
        locations.extend([
            'libmdf.dll',
            'C:\\Windows\\System32\\libmdf.dll',
        ])
    
    # Try ctypes.util.find_library
    try:
        lib_path = ctypes.util.find_library('mdf')
        if lib_path:
            locations.append(lib_path)
    except:
        pass
    
    # Check each location
    for location in locations:
        if os.path.exists(location):
            yield location


def _load_libmdf(max_attempts: int = 3) -> ctypes.CDLL:
    """Load the libmdf shared library."""
    # Check if --install-deps flag is present
    if '--install-deps' in sys.argv:
        # Run the installer
        try:
            from .install_deps import main as install_main
            install_main()
        except Exception as e:
            print(f"Installation failed: {e}")
        finally:
            sys.exit(1)
    
    for attempts, lib_path in enumerate(_find_libmdf()):
        print(f"Attempting to load libmdf from '{lib_path}'")
        try:
            lib = ctypes.CDLL(lib_path)
            return lib

        except OSError as e:
            if attempts > max_attempts:
                raise ImportError(f"Failed to load libmdf from '{lib_path}': {e}")

    raise ImportError(
            "Could not find libmdf shared library. "
            "Please ensure libmdf is installed and accessible, "
            "or set 'LIBMDF_PATH' environment variable."
        )

# Load the library
_lib = _load_libmdf(max_attempts=3)

# Function signatures
_lib.mdf_create.restype = mdf_t
_lib.mdf_create.argtypes = []

_lib.mdf_destroy.restype = None
_lib.mdf_destroy.argtypes = [mdf_t]

_lib.mdf_connect.restype = c_int
_lib.mdf_connect.argtypes = [mdf_t, c_char_p]

_lib.mdf_disconnect.restype = None
_lib.mdf_disconnect.argtypes = [mdf_t]

_lib.mdf_extract.restype = c_void_p
_lib.mdf_extract.argtypes = [mdf_t, ctypes.POINTER(c_uint16), ctypes.POINTER(c_uint64), ctypes.POINTER(c_size_t)]

_lib.mdf_inject.restype = c_int
_lib.mdf_inject.argtypes = [mdf_t, c_void_p, c_size_t]

_lib.mdf_consume.restype = c_int
_lib.mdf_consume.argtypes = [mdf_t, c_int]

_lib.mdf_get_next_message2.restype = c_int
_lib.mdf_get_next_message2.argtypes = [mdf_t, ctypes.POINTER(c_uint16), ctypes.POINTER(c_uint64)]

_lib.mdf_get_mclass.restype = c_uint64
_lib.mdf_get_mclass.argtypes = [mdf_t]

_lib.mdf_get_delay.restype = ctypes.c_uint8
_lib.mdf_get_delay.argtypes = [mdf_t]

_lib.mdf_get_next_field.restype = c_int
_lib.mdf_get_next_field.argtypes = [mdf_t, ctypes.POINTER(c_uint32), ctypes.POINTER(c_char_p)]

_lib.mdf_get_property.restype = c_int
_lib.mdf_get_property.argtypes = [mdf_t, c_int]

_lib.mdf_set_property.restype = c_int
_lib.mdf_set_property.argtypes = [mdf_t, c_int, c_void_p]

_lib.mdf_message_create.restype = mdf_message_t
_lib.mdf_message_create.argtypes = []

_lib.mdf_message_destroy.restype = None
_lib.mdf_message_destroy.argtypes = [mdf_message_t]

_lib.mdf_message_add.restype = c_int
_lib.mdf_message_add.argtypes = [mdf_message_t, c_uint64, c_int]

_lib.mdf_message_add2.restype = c_int
_lib.mdf_message_add2.argtypes = [mdf_message_t, c_uint64, c_uint16, ctypes.c_uint8]

_lib.mdf_message_del.restype = c_int
_lib.mdf_message_del.argtypes = [mdf_message_t]

_lib.mdf_message_reset.restype = None
_lib.mdf_message_reset.argtypes = [mdf_message_t]

_lib.mdf_message_serialize.restype = c_int
_lib.mdf_message_serialize.argtypes = [mdf_message_t, ctypes.POINTER(c_char_p)]

_lib.mdf_message_deserialize.restype = c_int
_lib.mdf_message_deserialize.argtypes = [mdf_message_t, c_char_p]

_lib.mdf_message_add_list.restype = c_int
_lib.mdf_message_add_list.argtypes = [mdf_message_t, c_uint32, c_char_p]

_lib.mdf_message_add_numeric.restype = c_int
_lib.mdf_message_add_numeric.argtypes = [mdf_message_t, c_uint32, c_char_p]

_lib.mdf_message_add_string.restype = c_int
_lib.mdf_message_add_string.argtypes = [mdf_message_t, c_uint32, c_char_p]

_lib.mdf_message_add_int.restype = c_int
_lib.mdf_message_add_int.argtypes = [mdf_message_t, c_uint32, c_longlong, c_int]

_lib.mdf_message_add_uint.restype = c_int
_lib.mdf_message_add_uint.argtypes = [mdf_message_t, c_uint32, c_uint64, c_int]

_lib.mdf_message_add_string2.restype = c_int
_lib.mdf_message_add_string2.argtypes = [mdf_message_t, c_uint32, c_char_p, c_size_t]

_lib.mdf_message_add_date.restype = c_int
_lib.mdf_message_add_date.argtypes = [mdf_message_t, c_uint32, c_char_p]

_lib.mdf_message_add_date2.restype = c_int
_lib.mdf_message_add_date2.argtypes = [mdf_message_t, c_uint32, c_int, c_int, c_int]

_lib.mdf_message_add_time.restype = c_int
_lib.mdf_message_add_time.argtypes = [mdf_message_t, c_uint32, c_char_p]

_lib.mdf_message_add_time2.restype = c_int
_lib.mdf_message_add_time2.argtypes = [mdf_message_t, c_uint32, c_int, c_int, c_int, c_int]

_lib.mdf_message_add_time3.restype = c_int
_lib.mdf_message_add_time3.argtypes = [mdf_message_t, c_uint32, c_int, c_int, c_int, c_int]

_lib.mdf_message_get_num.restype = c_int
_lib.mdf_message_get_num.argtypes = [mdf_message_t]

_lib.mdf_message_get_num_active.restype = c_int
_lib.mdf_message_get_num_active.argtypes = [mdf_message_t]

_lib.mdf_message_get_num_fields.restype = c_int
_lib.mdf_message_get_num_fields.argtypes = [mdf_message_t]

_lib.mdf_message_move.restype = c_int
_lib.mdf_message_move.argtypes = [mdf_message_t, mdf_message_t, c_uint64, c_uint64]

_lib.mdf_message_send.restype = c_int
_lib.mdf_message_send.argtypes = [mdf_t, mdf_message_t]

_lib.mdf_message_set_property.restype = c_int
_lib.mdf_message_set_property.argtypes = [mdf_message_t, c_int, c_int]


# Enhanced function signatures with better return types
def mdf_create() -> Optional[mdf_t]:
    """Create a new MDF handle. Returns None on failure."""
    result = _lib.mdf_create()
    return result if result else None


def mdf_destroy(handle: mdf_t) -> None:
    """Destroy an MDF handle."""
    _lib.mdf_destroy(handle)


def mdf_connect(handle: mdf_t, servers: str) -> bool:
    """Connect to MDF server(s). Returns True on success, False on failure."""
    return bool(_lib.mdf_connect(handle, servers.encode('utf-8')))


def mdf_disconnect(handle: mdf_t) -> None:
    """Disconnect from MDF server."""
    _lib.mdf_disconnect(handle)


def mdf_extract(handle: mdf_t) -> Tuple[Optional[bytes], int, int]:
    """
    Extract the next message from the stream for later injection.
    
    Returns:
        Tuple of (message_data, mref, insref)
        message_data is None if no more messages or an error occurred
    """
    mref = c_uint16()
    insref = c_uint64()
    length = c_size_t()
    
    ptr = _lib.mdf_extract(handle, mref, insref, ctypes.byref(length))
    
    if not ptr:
        return None, 0, 0
    
    # Copy the data before it gets overwritten
    data = ctypes.string_at(ptr, length.value)
    return data, mref.value, insref.value


def mdf_inject(handle: mdf_t, data: bytes) -> bool:
    """
    Inject a previously extracted message into the handle.
    
    Args:
        handle: MDF handle to inject into
        data: Message data from mdf_extract()
        
    Returns:
        True on success, False on failure
    """
    return bool(_lib.mdf_inject(handle, data, len(data)))


def mdf_consume(handle: mdf_t, timeout: int) -> Literal[-1, 0, 1]:
    """
    Consume data from server.
    
    Returns:
        -1: Error occurred
         0: Timeout (no data available)
         1: Messages available
    """
    return _lib.mdf_consume(handle, timeout)


def mdf_get_next_message2(handle: mdf_t) -> Tuple[bool, int, int]:
    """
    Get next message from stream.
    
    Returns:
        Tuple of (has_message, mref, insref)
    """
    mref = c_uint16()
    insref = c_uint64()
    result = _lib.mdf_get_next_message2(handle, mref, insref)
    return bool(result), mref.value, insref.value


def mdf_get_mclass(handle: mdf_t) -> int:
    """Get message class."""
    return _lib.mdf_get_mclass(handle)


def mdf_get_delay(handle: mdf_t) -> int:
    """Get message delay."""
    return _lib.mdf_get_delay(handle)


def mdf_get_next_field(handle: mdf_t) -> Tuple[bool, int, Optional[str]]:
    """
    Get next field from current message.
    
    Returns:
        Tuple of (has_field, tag, value)
        Note: value is None when the field is NULL (which is a valid MDF value)
    """
    tag = c_uint32()
    value = c_char_p()
    result = _lib.mdf_get_next_field(handle, tag, value)
    return bool(result), tag.value, value.value.decode('utf-8') if value.value is not None else None


@overload
def mdf_get_property(handle: mdf_t, option: Literal[
    MDF_OPTION.BIND_ADDRESS, MDF_OPTION.CRYPT_CIPHERS, MDF_OPTION.CRYPT_DIGESTS, 
    MDF_OPTION.CRYPT_CIPHER, MDF_OPTION.CRYPT_DIGEST, MDF_OPTION.CONNECTED_HOST, 
    MDF_OPTION.CONNECTED_IP
]) -> Optional[str]: ...

@overload
def mdf_get_property(handle: mdf_t, option: int) -> Optional[Union[int, str]]: ...

def mdf_get_property(handle: mdf_t, option: int) -> Optional[Union[int, str]]:
    """
    Get MDF property with type-safe return values.
    
    Returns:
        String for string properties, int for integer properties, None on failure
    """
    if option in [MDF_OPTION.BIND_ADDRESS, MDF_OPTION.CRYPT_CIPHERS, MDF_OPTION.CRYPT_DIGESTS, 
                  MDF_OPTION.CRYPT_CIPHER, MDF_OPTION.CRYPT_DIGEST, MDF_OPTION.CONNECTED_HOST, 
                  MDF_OPTION.CONNECTED_IP]:
        # String properties
        value = c_char_p()
        if _lib.mdf_get_property(handle, option, ctypes.byref(value)):
            return value.value.decode('utf-8') if value.value else None
    elif option in [MDF_OPTION.RCV_BYTES, MDF_OPTION.SENT_BYTES, MDF_OPTION.TIME_DIFFERENCE_NS]:
        # uint64_t properties
        value = c_uint64()
        if _lib.mdf_get_property(handle, option, ctypes.byref(value)):
            return value.value
    else:
        # Integer properties (int or uint32)
        value = c_int()
        if _lib.mdf_get_property(handle, option, ctypes.byref(value)):
            return value.value
    return


def mdf_set_property(handle: mdf_t, option: int, value: Union[int, str, None]) -> bool:
    """Set MDF property. Returns True on success, False on failure."""
    if value is None:
        return bool(_lib.mdf_set_property(handle, option, None))
    elif isinstance(value, str):
        return bool(_lib.mdf_set_property(handle, option, value.encode('utf-8')))
    else:
        return bool(_lib.mdf_set_property(handle, option, ctypes.byref(c_int(value))))


def mdf_message_create() -> mdf_message_t:
    """Create a new message handle."""
    return _lib.mdf_message_create()


def mdf_message_destroy(message: mdf_message_t) -> None:
    """Destroy a message handle."""
    _lib.mdf_message_destroy(message)


def mdf_message_add(message: mdf_message_t, insref: int, mref: int) -> bool:
    """Add message to chain."""
    return bool(_lib.mdf_message_add(message, insref, mref))


def mdf_message_add2(message: mdf_message_t, insref: int, mref: int, delay: int) -> bool:
    """Add message to chain with delay."""
    return bool(_lib.mdf_message_add2(message, insref, mref, delay))


def mdf_message_del(message: mdf_message_t) -> bool:
    """Delete current message from chain."""
    return bool(_lib.mdf_message_del(message))


def mdf_message_reset(message: mdf_message_t) -> None:
    """Reset message chain."""
    _lib.mdf_message_reset(message)


def mdf_message_serialize(message: mdf_message_t) -> str:
    """Serialize message to base64 string."""
    result = c_char_p()
    if _lib.mdf_message_serialize(message, ctypes.byref(result)):
        return result.value.decode('utf-8') if result.value else ""
    return ""


def mdf_message_deserialize(message: mdf_message_t, data: str) -> bool:
    """Deserialize message from base64 string."""
    return bool(_lib.mdf_message_deserialize(message, data.encode('utf-8')))


def mdf_message_add_list(message: mdf_message_t, tag: int, value: str) -> bool:
    """Add list field to message."""
    return bool(_lib.mdf_message_add_list(message, tag, value.encode('utf-8')))


def mdf_message_add_numeric(message: mdf_message_t, tag: int, value: str) -> bool:
    """Add numeric field to message."""
    return bool(_lib.mdf_message_add_numeric(message, tag, value.encode('utf-8')))


def mdf_message_add_string(message: mdf_message_t, tag: int, value: str) -> bool:
    """Add string field to message."""
    return bool(_lib.mdf_message_add_string(message, tag, value.encode('utf-8')))


def mdf_message_add_int(message: mdf_message_t, tag: int, value: int, decimals: int) -> bool:
    """Add signed integer field to message with decimal places."""
    return bool(_lib.mdf_message_add_int(message, tag, value, decimals))


def mdf_message_add_uint(message: mdf_message_t, tag: int, value: int, decimals: int) -> bool:
    """Add unsigned integer field to message with decimal places."""
    return bool(_lib.mdf_message_add_uint(message, tag, value, decimals))


def mdf_message_add_string2(message: mdf_message_t, tag: int, value: str, length: int) -> bool:
    """Add string field to message with specified length (useful for substrings or binary data)."""
    return bool(_lib.mdf_message_add_string2(message, tag, value.encode('utf-8'), length))


def mdf_message_add_date(message: mdf_message_t, tag: int, value: str) -> bool:
    """Add date field to message."""
    return bool(_lib.mdf_message_add_date(message, tag, value.encode('utf-8')))


def mdf_message_add_date2(message: mdf_message_t, tag: int, year: int, month: int, day: int) -> bool:
    """Add date field to message."""
    return bool(_lib.mdf_message_add_date2(message, tag, year, month, day))


def mdf_message_add_time(message: mdf_message_t, tag: int, value: str) -> bool:
    """Add time field to message."""
    return bool(_lib.mdf_message_add_time(message, tag, value.encode('utf-8')))


def mdf_message_add_time2(message: mdf_message_t, tag: int, hour: int, minute: int, second: int, msec: int) -> bool:
    """Add time field to message."""
    return bool(_lib.mdf_message_add_time2(message, tag, hour, minute, second, msec))


def mdf_message_add_time3(message: mdf_message_t, tag: int, hour: int, minute: int, second: int, nsec: int) -> bool:
    """Add time field to message."""
    return bool(_lib.mdf_message_add_time3(message, tag, hour, minute, second, nsec))


def mdf_message_get_num(message: mdf_message_t) -> int:
    """Get total number of messages in chain."""
    return _lib.mdf_message_get_num(message)


def mdf_message_get_num_active(message: mdf_message_t) -> int:
    """Get number of active messages in chain."""
    return _lib.mdf_message_get_num_active(message)


def mdf_message_get_num_fields(message: mdf_message_t) -> int:
    """Get number of fields in the current active message."""
    return _lib.mdf_message_get_num_fields(message)


def mdf_message_move(src: mdf_message_t, dst: Optional[mdf_message_t], insref_src: int, insref_dst: int) -> bool:
    """
    Move messages from src to dst, changing insref from insref_src to insref_dst.
    
    Args:
        src: Source message handle
        dst: Destination message handle (or None to modify in-place)
        insref_src: Source instrument reference to match (or UINT64_MAX for all)
        insref_dst: Destination instrument reference to set (or UINT64_MAX to keep unchanged)
        
    Returns:
        True on success, False on failure
    """
    dst_handle = dst if dst is not None else src
    return bool(_lib.mdf_message_move(src, dst_handle, insref_src, insref_dst))


def mdf_message_send(handle: mdf_t, message: mdf_message_t) -> bool:
    """Send message to server."""
    return bool(_lib.mdf_message_send(handle, message))


def mdf_message_set_property(message: mdf_message_t, option: int, value: int) -> bool:
    """Set message property."""
    return bool(_lib.mdf_message_set_property(message, option, value))
