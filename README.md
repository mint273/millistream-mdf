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
    - [Unsubscribing from Data Streams](#unsubscribing-from-data-streams)
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

With **uv**:
```bash
uv run python -m millistream_mdf --install-deps
```

Or:
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

##### `unsubscribe(request_classes='*', instruments='*')`
Unsubscribe from data streams to stop receiving realtime data.

**Parameters:**
- `request_classes`: List of request classes to unsubscribe from (e.g., `[RequestClass.QUOTE, RequestClass.TRADE]`), or `'*'` for all
- `instruments`: Instrument references to unsubscribe from. Can be `'*'` for all, or numeric IDs (e.g., `[1146, 1147]`)

**Raises:**
- [`MDFError`](#exception-types): If not connected or authenticated
- [`MDFMessageError`](#exception-types): If unsubscription request fails

**Note:** You can unsubscribe from a subset of your active subscriptions - the lists don't have to match previous subscription requests exactly.

**Example:**
```python
# Unsubscribe from specific instruments
client.unsubscribe(
    request_classes=[RequestClass.QUOTE],
    instruments=[1146, 1147]
)

# Unsubscribe from all quotes
client.unsubscribe(request_classes=[RequestClass.QUOTE], instruments='*')

# Unsubscribe from everything
client.unsubscribe()
```

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
| `instrument`    | `