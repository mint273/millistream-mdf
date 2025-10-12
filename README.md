# millistream-mdf

<div align="center">

<strong>Python wrapper for the Millistream Data Feed (MDF) C SDK</strong>

[![PyPI][pypi-badge]][pypi-url]
[![Python Version][python-badge]][python-url]
[![Documentation][docs-badge]][docs-url]

[pypi-badge]: https://img.shields.io/pypi/v/millistream-mdf.svg
[pypi-url]: https://pypi.org/project/millistream-mdf/
[python-badge]: https://img.shields.io/badge/python-3.13+-blue.svg
[python-url]: https://pypi.org/project/millistream-mdf/
[docs-badge]: https://img.shields.io/badge/docs-latest-blue.svg
[docs-url]: https://packages.millistream.com/documents/

</div>

## Table of Contents

- [Overview](#overview)
- [Installation](#installation)
  - [Install Package](#1-install-package)
  - [Install Prerequisites](#2-install-prerequisites)
- [Quick Start](#quick-start)
- [API Reference](#api-reference)
    - [MDF Class](#mdf-class)
    - [Message Class](#message-class)
- [Usage Examples](#usage-examples)
    - [News Streaming](#news-streaming)
    - [Sending Data](#sending-data)
    - [Manual Connection Control](#manual-connection-control)
- [Available Data Types](#available-data-types)
    - [Request Classes](#request-classes)
    - [Subscription Modes](#subscription-modes)
- [Error Handling](#error-handling)
- [Documentation](#documentation)
- [License](#license)
- [Support](#support)

## Overview

A high-level Python wrapper for the libmdf C SDK, providing access to the Millistream Data Feed (MDF) for real-time financial data streaming.

## Installation

### 1. Install Package

Install with **[uv](https://docs.astral.sh/uv/)**:

```bash
uv add millistream-mdf
```

Or with **[pip](https://pip.pypa.io/)**:

```bash
pip install millistream-mdf
```

### 2. Install Prerequisites

**Ubuntu/Debian**
```bash
python -m millistream_mdf --install-deps
```

For manual installation, refer to the [official documentation](https://packages.millistream.com/Linux/).

**macOS**

It is recommended to use the latest [libmdf installer](https://packages.millistream.com/macOS/) to install the necessary dependencies for macOS.

> **Note:** Will most likely be named `libmdf-x.x.x.pkg`.

**Windows**

It is recommended to use the latest [libmdf installer](https://packages.millistream.com/Windows/) to install the necessary dependencies for Windows.

>**Note:** Will most likely be named `libmdf-x.x.x.exe`.

## Quick Start

```python
from millistream_mdf import MDF, RequestClass


with MDF(
    url='sandbox.millistream.com',
    port=9100,
    username='sandbox',
    password='sandbox'
) as session:
    
    for message in session.subscribe(
        request_classes=[RequestClass.QUOTE],                       # Subscrive to 'quote' data
        instruments=[1146],                                         # Volvo B
        timeout=1
    ):
        print('raw:', message.fields)                               # unformatted fields 
        print('parsed:', message.parse_fields(remap_keys=True))     # convert types and/or format keys
    
    print('---')
```

or using the **asyncio** API:

```python
from millistream_mdf import AsyncMDF, RequestClass
import asyncio


async def main():

    async with AsyncMDF(
        url='sandbox.millistream.com',
        port=9100,
        username='sandbox',
        password='sandbox'
    ) as session:
        
        async for message in session.subscribe(
            request_classes=[RequestClass.QUOTE],                       # Subscrive to 'quote' data
            instruments=[1146],                                         # Volvo B
            timeout=1
        ):
            print('raw:', message.fields)                               # unformatted fields 
            print('parsed:', message.parse_fields(remap_keys=True))     # convert types and/or format keys
            
        print('---')

asyncio.run(main())
```

> **Tip:** You can use `sandbox.millistream.com:9100` for free to test the MDF with username: `sandbox` and password: `sandbox`. The data will be delayed and might not have access to the full offering.

> **Tip:** If you only want to convert the types you can use `parse_fields(remap_keys=False, convert_types=[...])`

**Example Output:**
```
raw: {5: '272.60', 6: '272.80', 19: '1559', 20: '1988', 7: '272.80', 10: '2139312', 11: '584322621.58', 37: '7116', 8: '275.10', 9: '271.80', 39: '275', 123: '273.07232827', 367: '105139', 368: '28856646.78', 369: None, 370: None, 3: '2025-10-11', 4: '15:29:40'}
parsed: {'bidprice': 272.6, 'askprice': 272.8, 'bidquantity': 1559.0, 'askquantity': 1988.0, 'lastprice': 272.8, 'quantity': 2139312.0, 'turnover': 584322621.58, 'numtrades': 7116, 'dayhighprice': 275.1, 'daylowprice': 271.8, 'openprice': 275.0, 'vwap': 273.07232827, 'offbookquantity': '105139', 'offbookturnover': '28856646.78', 'darkquantity': None, 'darkturnover': None, 'date': datetime.date(2025, 10, 11), 'time': datetime.time(15, 29, 40)}
---
raw: {20: '31', 4: '15:29:45'}
parsed: {'askquantity': 31.0, 'time': datetime.time(15, 29, 45)}
---
raw: {19: '4796', 4: '15:29:57'}
parsed: {'bidquantity': 4796.0, 'time': datetime.time(15, 29, 57)}
---
raw: {19: '3173', 20: '1432', 4: '15:30:02'}
parsed: {'bidquantity': 3173.0, 'askquantity': 1432.0, 'time': datetime.time(15, 30, 2)}
```

> **Note:** Only the differences are broadcasted for efficacy. In the example above a full image is broadcasted at the beginning since [`subscription_mode`](#subcriptions-modes) defaults to `full` (`image` + `stream`).
 

## API Reference

### MDF Class

The main client class for connecting to MDF servers.

#### Constructor Parameters

| Name                | Type            | Description                                      | Default    |
|---------------------|-----------------|--------------------------------------------------|------------|
| `url`               | `str`           | Server URL                                       |            |
| `port`              | `int`           | Server port                                      | 9100       |
| `username`          | `str`           | Username for authentication                      |            |
| `password`          | `str`           | Password for authentication                      |            |
| `heartbeat_interval`| `int`, `float`  | Heartbeat interval in seconds                    | 30         |
| `connect_timeout`   | `int`, `float`  | Connection timeout in seconds                    | 10         |
| `tcp_nodelay`       | `bool`          | Disable TCP Nagle algorithm                      | True       |
| `no_encryption`     | `bool`          | Disable encryption                               | False      |

#### Attributes

All [constructor parameters](#constructor-parameters)

#### Properties

| Name                | Type            | Description                                      | Default    |
|---------------------|-----------------|--------------------------------------------------|------------|
| `is_connected`      | `bool`          | Whether the client is connected to the server    | False      |
| `is_authenticated`  | `bool`          | Whether the client is authenticated to the server| False      |

#### Methods

##### `connect()`
Connect to the MDF server and authenticate.

**Raises:**
- [`MDFConnectionError`](#exception-types): If connection fails
- [`MDFAuthenticationError`](#exception-types): If authentication fails

##### `disconnect()`
Disconnect from the MDF server.

##### `subscribe(request_classes, instruments='*', subscription_mode='full', timeout=1)`
Subscribe to data streams and yield messages.

**Parameters:**
- `request_classes`: List of request classes to subscribe to (e.g., `[RequestClass.QUOTE, RequestClass.TRADE, RequestClass.BASICDATA]`). Can be string names or integer MREF codes
- `instruments`: Instrument references to subscribe to. Can be `'*'` for all, or numeric IDs (e.g., `[1146, 1147]`)
- `subscription_mode`: Subscription mode (`'image'`, `'stream'`, or `'full'`). See [`Subscription Modes`](#subcriptions-modes) for more information.
- `timeout`: Timeout in seconds for consume operations

**Returns:** Generator yielding [`Message`](#message-class) objects

##### `stream(timeout=1)`
Stream messages from the server.

**Parameters:**
- `timeout`: Timeout in seconds for consume operations

**Returns:** Generator yielding [`Message`](#message-class) objects

##### `send(mref, instrument, fields, delay=0)`
Send a single message to the server with specified fields.

**Parameters:**
- `mref`: Message reference (e.g., `MessageReference.QUOTE`, `MessageReference.TRADE`)
- `instrument`: Instrument reference
- `fields`: Dictionary mapping field names to values
- `delay`: Optional delay parameter (default: `0`)

**Returns:** `True` if the message was sent successfully

**Raises:**
- [`MDFError`](#exception-types): If not connected or authenticated
- [`MDFMessageError`](#exception-types): If message construction or sending fails

**Example:**
```python
client.send(
    mref=MessageReference.QUOTE,
    instrument=12345,
    fields={
        Field.BIDPRICE: 100.50,
        Field.ASKPRICE: 100.55,
        Field.BIDQUANTITY: 1000,
        Field.ASKQUANTITY: 500
    }
)
```

##### `send_batch(messages)`
Send multiple messages in a single batch for better efficiency.

**Parameters:**
- `messages`: List of message dictionaries with `'mref'`, `'instrument'`, `'fields'`, and optionally `'delay'`

**Returns:** `True` if all messages were sent successfully

**Example:**
```python
client.send_batch([
    {
        'mref': MessageReference.QUOTE,
        'instrument': 12345,
        'fields': {Field.BIDPRICE: 100.50, Field.ASKPRICE: 100.55},
    },
    {
        'mref': MessageReference.TRADE,
        'instrument': 12345,
        'fields': {Field.TRADEPRICE: 100.52, Field.TRADEQUANTITY: 1000},
    }
])
```

##### `create_message_builder()`
Create a new `MessageBuilder` for advanced message construction.

**Returns:** A new `MessageBuilder` instance (must be used as context manager)

**Example:**
```python
with client.create_message_builder() as builder:
    builder.add_message(mref=MessageReference.QUOTE, instrument=12345)
    builder.add_field(Field.BIDPRICE, 100.50)
    builder.add_field(Field.ASKPRICE, 100.55)
    builder.send(client._handle)
```

### Message Class

Represents a message received from the MDF server.

#### Attributes

| Name            | Type                                   | Description                                                            | Default   | Example                                          |
|-----------------|----------------------------------------|------------------------------------------------------------------------|-----------|--------------------------------------------------|
| `ref`           | `int`                                  | What type of message it is (e.g. `MessageReference.NEWSHEADLINE`)      |           | `MessageReference.QUOTE`                         |
| `instrument`    | `int`                                  | Instrument reference ID                                                |           | `12345`                                          |
| `fields`        | `dict[int, str \| None]`               | Dictionary of field: value pairs (raw values)                          | `{}`      | `{Field.BIDPRICE: "100.50", Field.ASKPRICE: "100.55"}` |
| `delay`         | `int`                                  | Message delay type                                                     | `0`       | `0`                                              |

#### Properties

| Name            | Type                                   | Description                                                            | Default   | Example                                          |
|-----------------|----------------------------------------|------------------------------------------------------------------------|-----------|--------------------------------------------------|
| `parsed_fields` | `dict[str \| int, str \| int \| float \| date \| time \| datetime \| list[str]]` | Dictionary of field: value pairs with parsed types |           | `{'bidprice': 100.50, 'askprice': 100.55}`       |

> **Note:** For a list items are always `str`. The type of each item in the list is not guaranteed. For general type casting the type will have to be guessed.

#### Methods

##### `parse_fields(remap_keys=True, convert_types=['str', 'int', 'float', 'date', 'time', 'datetime', 'list'], on_field_missing='ignore', list_delimiter=' ')`
Parse and convert field values to their proper types.

**Parameters:**
- `remap_keys`: If `True`, use lowercase field names as keys; else use field IDs
- `convert_types`: Which types to convert (`str`, `int`, `float`, `date`, `time`, `datetime`, `list`)
- `on_field_missing`: How to handle unmapped fields (`'raise'`, `'ignore'`, `'skip'`)
- `list_delimiter`: Delimiter to split list values on

**Returns:** Dictionary with converted values

##### `get(field, default=None)`
Get field value by name with optional default.

##### `__getitem__(field)`
Allow dict-like access to fields: `message[Field.BIDPRICE]`

##### `__contains__(field)`
Check if field exists: `Field.BIDPRICE in message`

## Usage Examples

### News Streaming

```python
from millistream_mdf import MDF, RequestClass, MessageReference, Field

with MDF(
    url='sandbox.millistream.com',
    port=9100,
    username='sandbox',
    password='sandbox'
) as session:
    
    for message in session.subscribe(
        request_classes=[RequestClass.NEWSHEADLINE, RequestClass.NEWSCONTENT],
        subscription_mode='stream',
        instruments='*',
        timeout=1
    ):
        if message.ref == MessageReference.NEWSHEADLINE:
            print(f"Headline: {message.get(Field.HEADLINE)}")
            print(f"Date: {message.get(Field.DATE)}")

        elif message.ref == MessageReference.NEWSCONTENT:
            print(f'Content: {message.get(Field.TEXTBODY, 'N/A')[:100]}...')
            print('---')
```

> **Tip:** You can use `'*'` for all available instruments.

> **Note:** [`RequestClass`](#request-classes) and [`MessageReference`](#message-reference) have overlapping names but serve different purposes and have different integer values.

**Example Output:**

```
Headline: Antibiotics Market Size to Surpass USD 55.26 Billion by 2033, Report by DataM Intelligence
Date: 2025-10-10
Content: <?xml version="1.0" encoding="UTF-8"?><NewsItem><NewsEnvelope><TransmissionId>202509221001PR_NEWS_EU...
---
Headline: Aventis Energy Confirms Strong Radioactivity at Corvo Uranium Project
Date: 2025-10-10
Content: <?xml version="1.0" encoding="UTF-8"?><NewsItem><NewsEnvelope><TransmissionId>A3462546</Transmission...
---
```

> **Note:** Headlines and content are sent in different messages so that the headline can be recieved as quick as possible. You can pair them together using the `Field.NEWSID` field.

### Sending Data

```python
from millistream_mdf import MDF, MessageReference, Field

# Simple message sending
with MDF(
    url='server.example.com',
    port=9100,
    username='user',
    password='pass'
) as client:
    
    # Send a single quote message
    client.send(
        mref=MessageReference.QUOTE,
        instrument=12345,
        fields={
            Field.BIDPRICE: 100.50,
            Field.ASKPRICE: 100.55,
            Field.BIDQUANTITY: 1000,
            Field.ASKQUANTITY: 500,
        }
    )
    
    # Send multiple messages in a batch (more efficient)
    client.send_batch([
        {
            'mref': MessageReference.QUOTE,
            'instrument': 12345,
            'fields': {Field.BIDPRICE: 100.50, Field.ASKPRICE: 100.55},
        },
        {
            'mref': MessageReference.TRADE,
            'instrument': 12345,
            'fields': {Field.TRADEPRICE: 100.52, Field.TRADEQUANTITY: 1000},
        }
    ])
```

### Manual Connection Control

```python
from millistream_mdf import MDF, MDFError

session = MDF(
    url='sandbox.millistream.com',
    port=9100,
    username='sandbox',
    password='sandbox'
)

try:
    session.connect()
    print("Connected!")
    
    # Subscribe to quote data
    session.subscribe(request_classes=[RequestClass.QUOTE], instruments='*')

    # Stream subscribed data
    for message in session.stream(timeout=1):
        print(message.fields)
        print("---")
        
except MDFError as e:
    print(f"Error: {e}")
finally:
    session.disconnect()
```

## Available Data Types

### Request Classes

- `NEWSHEADLINE`: News headlines
- `NEWSCONTENT`: Full news content
- `QUOTE`: Market quotes (bid/ask)
- `TRADE`: Trade executions
- `ORDER`: Order book data
- `BASICDATA`: Instrument basic information
- `PRICEHISTORY`: Historical price data
- `CORPORATEACTION`: Corporate actions
- `FUNDAMENTALS`: Financial fundamentals
- `PERFORMANCE`: Performance metrics
- `KEYRATIOS`: Key financial ratios
- `ESTIMATES`: Analyst estimates
- `MIFID`: MiFID II data
- `GREEKS`: Options Greeks
- And more...

### Message Reference

- `MESSAGESREFERENCE`: Message reference
- `LOGON`: Logon
- `LOGOFF`: Logoff
- `LOGONGREETING`: Logon greeting
- `NEWSHEADLINE`: News headline
- `QUOTE`: Quote
- `TRADE`: Trade
- `BIDLEVELINSERT`: Bid level insert
- `ASKLEVELINSERT`: Ask level insert
- `BIDLEVELDELETE`: Bid level delete
- `ASKLEVELDELETE`: Ask level delete
- `BIDLEVELUPDATE`: Bid level update
- `ASKLEVELUPDATE`: Ask level update
- `INSTRUMENTRESET`: Instrument reset
- And [more](https://packages.millistream.com/documents/MDF%20Messages%20Reference.pdf)...


### Subscription Modes

- `image`: Snapshot of current values
- `stream`: Streaming data only
- `full`: Both image and stream

## Error Handling

The wrapper provides a comprehensive exception hierarchy:

```python
from millistream_mdf import (
    MDFError,
    MDFConnectionError,
    MDFAuthenticationError,
    RequestClass
)

try:
    with MDF(
        url='sandbox.millistream.com',
        port=9100,
        username='sandbox',
        password='sandbox'
    ) as session:
        for message in session.subscribe(request_classes=[RequestClass.QUOTE], instruments='*'):
            print(message)

except MDFConnectionError as e:
    print(f"Connection failed: {e}")
except MDFAuthenticationError as e:
    print(f"Authentication failed: {e}")
except MDFError as e:
    print(f"MDF error: {e}")
```

### Exception Types

- `MDFError`: Base exception for all MDF-related errors
- `MDFConnectionError`: Connection failures
- `MDFAuthenticationError`: Login failures
- `MDFTimeoutError`: Timeout errors
- `MDFMessageError`: Message operation failures
- `MDFConfigurationError`: Invalid configuration
- `MDFLibraryError`: Underlying library errors


## Documentation

For more detailed documentation, visit the [official documentation](https://packages.millistream.com/documents/) or the [millistream sandbox](https://sandbox.millistream.com/sandbox/mdf).


## License

This wrapper is provided under the LGPL v3 license, the same as the underlying libmdf library.

## Support

For issues with this Python wrapper:

1. Check this documentation
2. Check error messages and exception types
3. [Open an issue](https://github.com/mint273/millistream-mdf/issues) on GitHub

For *libmdf* library issues, refer to the official Millistream documentation or contact tech@millistream.com.