# Ziggiz-Courier Plugin Development Guide

This guide explains how to develop message decoder plugins for the Ziggiz-Courier data processing framework. It outlines the architecture, requirements, and best practices to create effective plugins that conform to our project standards.

## Plugin Architecture Overview

The Ziggiz-Courier project follows a modular architecture consisting of:

1. **Decoders**: Parse raw input into structured models
2. **Models**: Structured data representations
3. **Adapters**: Transform between different model formats
4. **Encoders**: Convert models to output formats

Message decoder plugins are a critical component for handling specific message formats (e.g., syslog messages from different vendors).

## Creating a New Message Decoder Plugin

### 1. Determine Plugin Location

Plugins are organized by vendor and product:

```
core_data_processing/
  decoders/
    plugins/
      message/
        <vendor>/
          __init__.py
          <product>/
            __init__.py
            plugin.py
            field_maps.py (optional)
```

Example for a Cisco ASA plugin:
```
core_data_processing/decoders/plugins/message/cisco/asa/plugin.py
```

### 2. Basic Plugin Structure

Create a plugin.py file with the following structure:

```python
# -*- coding: utf-8 -*-
# Copyright (C) 2025 ziggiz
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
[Vendor] [Product] [Format] message plugin for Ziggiz-Courier.

This plugin provides a decoder for [Vendor] [Product] syslog messages in [Format] format.
It parses the message into structured data for downstream processing and caches results for efficiency.

References:
    - [Vendor] [Product] Syslog Message Formats:
      [URL to vendor documentation]
    - Relevant RFCs: [e.g., RFC3164, RFC5424]

Example:
    >>> msg = 'example message format...'
    >>> decoder = YourPluginClassName()
    >>> decoder.decode(model_with_msg)
    True
"""

# Standard library imports
import logging

from typing import Any, Dict, Optional

# Local/package imports
from core_data_processing.decoders.message_decoder_plugins import (
    MessagePluginStage,
    register_message_decoder,
)
from core_data_processing.decoders.plugins.message.base import MessageDecoderPluginBase
from core_data_processing.decoders.utils.xxx_parser import parse_xxx_message  # Choose appropriate parser
from core_data_processing.models.event_envelope_base import EventEnvelopeBaseModel
from core_data_processing.models.syslog_rfc_base import SyslogRFCBaseModel  # Or other appropriate model

logger = logging.getLogger(__name__)


class YourPluginClassName(MessageDecoderPluginBase):
    """
    Decoder for [Vendor] [Product] syslog messages in [Format] format.

    This decoder parses [Vendor] [Product] syslog messages in [Format] format
    and updates the event model with structured data.
    """

    def __init__(self, parsing_cache: Optional[Dict[str, Any]] = None):
        """
        Initialize the [Product] [Format] decoder.

        Args:
            parsing_cache (Optional[Dict[str, Any]]): A dictionary for caching parsed message results
        """
        super().__init__(parsing_cache)

    def decode(self, model: EventEnvelopeBaseModel) -> bool:
        """
        Parse a [Vendor] [Product] syslog message in [Format] format into event_data on the model.

        Args:
            model (EventEnvelopeBaseModel): The event model instance to parse and update.

        Returns:
            bool: True if the message was parsed as [Product] [Format] format, False otherwise.
            When returning True, the plugin should have updated the model's structure_classification
            and event_data attributes accordingly.

        Example:
            >>> msg = 'example message format...'
            >>> decoder = YourPluginClassName()
            >>> decoder.decode(model_with_msg)
            True
        """
        message = getattr(model, "message", None)
        if not isinstance(message, str):
            return False

        # Parse the message using an appropriate parser
        if "parse_xxx_message" not in self.parsing_cache:
            self.parsing_cache["parse_xxx_message"] = parse_xxx_message(message)

        parsed_data = self.parsing_cache["parse_xxx_message"]

        # Validate the parsed data matches the expected format
        if parsed_data and self._is_valid_format(parsed_data):
            # Determine message class
            msgclass = self._determine_message_class(parsed_data)

            # Use apply_field_mapping method from base class
            self.apply_field_mapping(
                model=model,
                fields=self._extract_fields(parsed_data),
                field_names=self._extract_field_names(parsed_data),
                vendor="vendor_name",
                product="product_name",
                msgclass=msgclass,
            )

            logger.debug(
                "[Product] plugin parsed event_data",
                extra={"event_data": model.event_data}
            )
            return True
        return False

    def _is_valid_format(self, parsed_data: Any) -> bool:
        """
        Determine if the parsed data matches this plugin's format.

        Args:
            parsed_data: The parsed message data

        Returns:
            bool: True if valid format, False otherwise
        """
        # Implement format validation logic
        pass

    def _determine_message_class(self, parsed_data: Any) -> str:
        """
        Determine the message class from the parsed data.

        Args:
            parsed_data: The parsed message data

        Returns:
            str: The message class identifier
        """
        # Implement message class determination
        pass

    def _extract_fields(self, parsed_data: Any) -> list:
        """
        Extract field values from parsed data.

        Args:
            parsed_data: The parsed message data

        Returns:
            list: List of field values
        """
        # Implement field extraction
        pass

    def _extract_field_names(self, parsed_data: Any) -> list:
        """
        Extract field names from parsed data.

        Args:
            parsed_data: The parsed message data

        Returns:
            list: List of field names
        """
        # Implement field name extraction
        pass


# Register the decoder for appropriate message types
register_message_decoder(SyslogRFCBaseModel, MessagePluginStage.SECOND_PASS)(
    YourPluginClassName
)
```

### 3. Common Parser Types

Choose the appropriate parser based on your message format:

1. **Key-Value Parser** (for key=value formats like Fortinet):
   ```python
   from core_data_processing.decoders.utils.kv_parser import parse_kv_message
   ```

2. **CSV Parser** (for comma-separated formats like PaloAlto):
   ```python
   from core_data_processing.decoders.utils.csv_parser import parse_quoted_csv_message
   ```

3. **Custom Parser** (if needed):
   - Create a new parser in `core_data_processing/decoders/utils/` for unique formats

### 4. Field Mapping

There are two primary approaches to field mapping:

#### Dynamic Field Mapping (FortiGate approach)

For formats with key=value pairs where field names are known at runtime:

```python
# Extract field names and values directly from the parsed data
self.apply_field_mapping(
    model=model,
    fields=list(event_data.values()),
    field_names=list(event_data.keys()),
    vendor="vendor_name",
    product="product_name",
    msgclass=msgclass,
)
```

#### Dynamic Field Mapping with Values from Parsed Data (CEF approach)

For formats where vendor, product, and message class information is contained within the data:

```python
# Extract vendor, product, and msgclass from the parsed data
vendor = parsed_data.get("device_vendor", "unknown").lower()
product = parsed_data.get("device_product", "unknown").lower()
msgclass = parsed_data.get("name", "unknown").lower()

# Use dynamic values from the parsed data
self.apply_field_mapping(
    model=model,
    fields=list(parsed_data.values()),
    field_names=list(parsed_data.keys()),
    vendor=vendor,
    product=product,
    msgclass=msgclass,
)
```

#### Static Field Mapping (PaloAlto approach)

For formats with predefined field positions (like CSV):

1. Create a field_maps.py file:
   ```python
   # Field name lists for each message type
   MESSAGE_TYPE_A_FIELDS = [
       "field1",
       "field2",
       "field3",
       # ...
   ]

   MESSAGE_TYPE_B_FIELDS = [
       "field1",
       "field2",
       "field3",
       # ...
   ]

   TYPE_FIELD_MAP = {
       "TYPE_A": MESSAGE_TYPE_A_FIELDS,
       "TYPE_B": MESSAGE_TYPE_B_FIELDS,
   }
   ```

2. Use the field map in your plugin:
   ```python
   from .field_maps import TYPE_FIELD_MAP

   # ...

   type_field = determine_type_from_message(parsed_data)
   field_names = TYPE_FIELD_MAP.get(type_field.upper())

   if field_names:
       self.apply_field_mapping(
           model=model,
           fields=parsed_data,
           field_names=field_names,
           vendor="vendor_name",
           product="product_name",
           msgclass=type_field.lower(),
       )
   ```

### 5. Plugin Registration

Register your plugin with appropriate message types and processing stage:

```python
register_message_decoder(SyslogRFCBaseModel, MessagePluginStage.SECOND_PASS)(
    YourPluginClassName
)
```

#### Processing Stages

The framework executes plugins in a specific order based on their registered stage:

1. **FIRST_PASS**: Initial processing of the message, typically used for very basic or high-priority format detection
2. **SECOND_PASS**: Main processing stage for most vendor-specific message formats
3. **UNPROCESSED_STRUCTURED**: Used for structured formats (like CEF, JSON) that may appear in any syslog message
4. **UNPROCESSED_MESSAGES**: Final fallback for any messages not processed by earlier stages

Choose the appropriate stage based on when your plugin should execute in the pipeline:

- Use **SECOND_PASS** for most vendor-specific format parsers (default for most plugins)
- Use **UNPROCESSED_STRUCTURED** for format parsers that should run across all message types (e.g., CEF, JSON)
- Use **FIRST_PASS** only for critical pre-processing that must happen before other plugins
- Use **UNPROCESSED_MESSAGES** for fallback parsers that should run only if other plugins don't match

#### Registering for Multiple Message Types

For plugins that can handle multiple message formats, register them separately for each type:

```python
# Register for base syslog messages
register_message_decoder(SyslogRFCBaseModel, MessagePluginStage.SECOND_PASS)(
    YourPluginClassName
)

# Register for specific formats
register_message_decoder(SyslogRFC3164Message, MessagePluginStage.SECOND_PASS)(
    YourPluginClassName
)
register_message_decoder(SyslogRFC5424Message, MessagePluginStage.SECOND_PASS)(
    YourPluginClassName
)
```

#### Model Type Selection Guidelines

Consider these guidelines when choosing which model types to register your plugin for:

1. **SyslogRFCBaseModel**:
   - Register for this type when your plugin can process any type of syslog message
   - Used for generic formats that could appear in any syslog message
   - Example: CEF format appears in various syslog message types

2. **SyslogRFC3164Message**:
   - Register for this type when your plugin is specifically for BSD-style syslog format
   - Has fields like hostname, app_name, and proc_id
   - Example: Legacy firewall logs with BSD syslog format

3. **SyslogRFC5424Message**:
   - Register for this type when your plugin is specifically for modern syslog format
   - Has additional structured fields like msg_id and structured_data
   - Example: Modern application logs using structured syslog

If your plugin needs fields specific to RFC3164 or RFC5424 (like structured_data), register only for those types. If it works with any syslog message format, register for all three types.

#### Registration Order and Plugin Chain

Important notes about plugin registration and execution:

1. Plugins are executed in the order they are registered within each stage
2. When a plugin successfully decodes a message (returns `True`), it updates the model's structure and event data
3. Multiple plugins may run on the same message if they all return `True` (accumulating fields)
4. Later plugins can see and build upon the results of earlier plugins
5. The plugin chain continues even after successful matches, allowing multiple plugins to contribute to the final result

### 6. Understanding the Parsing Cache

The `parsing_cache` is a critical component for plugin performance optimization:

```python
def decode(self, model: EventEnvelopeBaseModel) -> bool:
    message = getattr(model, "message", None)
    if not isinstance(message, str):
        return False

    # Use parsing cache if available
    if "parse_xxx_message" not in self.parsing_cache:
        self.parsing_cache["parse_xxx_message"] = parse_xxx_message(message)

    parsed_data = self.parsing_cache["parse_xxx_message"]

    # Use the parsed data...
```

#### Parsing Cache Best Practices

1. **Unique Cache Keys**: Use descriptive, unique cache keys prefixed with the parsing function name
2. **Expensive Operations Only**: Cache results of expensive operations like regex parsing
3. **Check Before Parsing**: Always check if data exists in the cache before parsing
4. **Cache Raw Results**: Store the full parsing result, not just parts of it
5. **Don't Cache Transformations**: Only cache the original parsing result, not derived data

#### Cache Persistence

The `parsing_cache` dictionary:
- Is passed to the plugin constructor
- Is shared across multiple decode() calls within the same decoder instance
- May be shared across multiple plugins in a chain
- Persists for the lifetime of the decoder but not across process restarts

This allows efficient processing of large batches of similar messages without redundant parsing.

## Testing Your Plugin

### 1. Create Test File

Create a test file in the appropriate location:
```
tests/test_decoders/plugins/message/<vendor>/<product>/test_<product>_<format>.py
```

### 2. Write Test Cases

```python
# -*- coding: utf-8 -*-
# Copyright (C) 2025 ziggiz
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
Unit tests for YourPluginClassName.
"""
# Standard library imports

# Third-party imports
import pytest

# Local/package imports
from core_data_processing.decoders.plugins.message.vendor.product.plugin import YourPluginClassName
from core_data_processing.models.syslog_rfc_base import SyslogRFCBaseModel
# Import other models as needed


@pytest.mark.unit
def test_your_plugin_basic_case():
    """Test YourPluginClassName with basic message format."""
    # Create a model with a test message
    msg = "your test message here"
    model = SyslogRFCBaseModel(
        timestamp="2025-05-13T12:34:56.000Z",
        facility=16,  # LOCAL0
        severity=6,  # INFO
        message=msg,
    )

    # Initialize the decoder with an empty cache
    decoder = YourPluginClassName()

    # Call the decode method
    result = decoder.decode(model)

    # Verify the result
    assert result is True
    assert model.structure_classification.vendor == "vendor_name"
    assert model.structure_classification.product == "product_name"
    assert model.structure_classification.msgclass == "expected_msgclass"

    # Verify specific fields in the parsed data
    assert "field1" in model.event_data
    assert model.event_data["field1"] == "expected_value"


@pytest.mark.unit
def test_your_plugin_negative_case():
    """Test YourPluginClassName with non-matching message format."""
    # Create a model with a message that should not match
    msg = "non-matching message format"
    model = SyslogRFCBaseModel(
        timestamp="2025-05-13T12:34:56.000Z",
        facility=16,
        severity=6,
        message=msg,
    )

    # Initialize the decoder
    decoder = YourPluginClassName()

    # Call the decode method
    result = decoder.decode(model)

    # Verify the result is False (no match)
    assert result is False
```

## Best Practices

### 1. Code Style

- Follow PEP 8 standards for Python code
- Use comprehensive docstrings with Args, Returns, and Examples
- Include type hints for all methods and parameters
- Use raw strings for regex patterns: `r"pattern"`
- Use meaningful variable names

### 2. Error Handling

- Use proper validation before accessing dictionary keys
- Handle potential exceptions in parsers
- Use proper error logging with the `extra` parameter
- Avoid using f-strings in logging; use structured logging instead

### 3. Performance

- Use caching for expensive parsing operations
- Consider performance for large message volumes
- Use compiled regex patterns for frequently used expressions

### 4. Documentation

- Document all public methods and classes
- Include example messages in docstrings
- Add references to vendor documentation
- Explain message format specifics

### 5. Testing

- Write tests for positive and negative cases
- Use parameterized tests for multiple message formats
- Test edge cases and malformed messages
- Mark tests with appropriate markers (`@pytest.mark.unit`)

## Examples from Existing Plugins

### FortiGate Key-Value Plugin Example

The FortiGate plugin parses key-value pairs from syslog messages:

```python
def decode(self, model: EventEnvelopeBaseModel) -> bool:
    """
    Parse a Fortinet FortiGate syslog message in key=value format into event_data.
    """
    message = getattr(model, "message", None)
    if not isinstance(message, str):
        return False

    # Use parsing cache if available
    if "parse_kv_message" not in self.parsing_cache:
        self.parsing_cache["parse_kv_message"] = parse_kv_message(message)

    event_data = self.parsing_cache["parse_kv_message"]

    if (
        event_data
        and "eventtime" in event_data
        and "type" in event_data
        and "subtype" in event_data
        and "logid" in event_data
        and len(event_data["logid"]) == 10
    ):
        # Get message class by joining type and subtype
        msgclass = "_".join(
            [event_data.get("type", ""), event_data.get("subtype", "")]
        )

        # Use apply_field_mapping method from base class
        self.apply_field_mapping(
            model=model,
            fields=list(event_data.values()),
            field_names=list(event_data.keys()),
            vendor="fortinet",
            product="fortigate",
            msgclass=msgclass,
        )

        logger.debug(
            "FortiGate plugin parsed event_data",
            extra={"event_data": model.event_data}
        )
        return True
    return False
```

### PaloAlto CSV Plugin Example

The PaloAlto plugin parses CSV-formatted messages with mapped fields:

```python
def decode(self, model: EventEnvelopeBaseModel) -> bool:
    """
    Parse a PaloAlto NGFW syslog message in CSV format into event_data.
    """
    message = getattr(model, "message", None)
    if not isinstance(message, str):
        return False

    if "parse_quoted_csv_message" not in self.parsing_cache:
        self.parsing_cache["parse_quoted_csv_message"] = parse_quoted_csv_message(
            message
        )

    fields = self.parsing_cache["parse_quoted_csv_message"]

    if fields and isinstance(fields, list) and len(fields) > 3:
        type_field = fields[3] if len(fields) > 3 else None
        field_names = None

        if type_field:
            field_names = PAN_TYPE_FIELD_MAP.get(type_field.upper())

        if field_names:
            self.apply_field_mapping(
                model=model,
                fields=fields,
                field_names=field_names,
                vendor="paloalto",
                product="ngfw",
                msgclass=type_field.lower(),
            )
            logger.debug(
                "PaloAlto NGFW plugin parsed event_data",
                extra={"event_data": model.event_data}
            )
            return True

    return False
```

## Conclusion

By following this guide, you can create consistent, high-quality plugins that integrate well with the Ziggiz-Courier data processing framework. Please refer to existing plugins as models of best practices, and ensure your implementation meets the project's quality standards.
