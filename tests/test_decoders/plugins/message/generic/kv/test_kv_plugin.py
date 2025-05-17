# -*- coding: utf-8 -*-
# # SPDX-License-Identifier: BSL-1.1
# # Copyright (c) 2025 Ziggiz Inc.
# #
# # This file is part of the ziggiz-courier-core-data-processing and is licensed under the
# # Business Source License 1.1. You may not use this file except in
# # compliance with the License. You may obtain a copy of the License at:
# # https://github.com/ziggiz-courier/ziggiz-courier-core-data-processing/blob/main/LICENSE
"""
Unit tests for GenericKVDecoderPlugin.
"""
# Standard library imports
from datetime import datetime, timezone

# Third-party imports
import pytest

# Local/package imports
from ziggiz_courier_handler_core.decoders.plugins.message.generic.kv.plugin import (
    GenericKVDecoderPlugin,
)
from ziggiz_courier_handler_core.models.syslog_rfc_base import SyslogRFCBaseModel


@pytest.mark.unit
def test_generic_kv_basic_case():
    """Test GenericKVDecoderPlugin with basic key-value message format."""
    # Create a model with a test key-value message
    msg = "src=10.0.0.1 dst=8.8.8.8 action=allow service=https"
    model = SyslogRFCBaseModel(
        timestamp=datetime(2025, 5, 16, 12, 34, 56, tzinfo=timezone.utc),
        facility=16,  # LOCAL0
        severity=6,  # INFO
        message=msg,
    )

    # Initialize the decoder with an empty cache
    decoder = GenericKVDecoderPlugin()

    # Call the decode method
    result = decoder.decode(model)

    # Verify the result
    assert result is True
    assert model.structure_classification.vendor == "generic"
    assert model.structure_classification.product == "unknown_kv"
    assert model.structure_classification.msgclass == "unknown"

    # Verify specific fields in the parsed data
    assert "src" in model.event_data
    assert model.event_data["src"] == "10.0.0.1"
    assert model.event_data["dst"] == "8.8.8.8"
    assert model.event_data["action"] == "allow"
    assert model.event_data["service"] == "https"


@pytest.mark.unit
def test_generic_kv_quoted_values():
    """Test GenericKVDecoderPlugin with quoted values in key-value pairs."""
    # Create a model with a test key-value message with quoted values
    msg = 'user="john doe" action=login status=success path="/var/log/test"'
    model = SyslogRFCBaseModel(
        timestamp=datetime(2025, 5, 16, 12, 34, 56, tzinfo=timezone.utc),
        facility=16,
        severity=6,
        message=msg,
    )

    # Initialize the decoder
    decoder = GenericKVDecoderPlugin()

    # Call the decode method
    result = decoder.decode(model)

    # Verify the result
    assert result is True
    assert "user" in model.event_data
    assert model.event_data["user"] == "john doe"
    assert model.event_data["action"] == "login"
    assert model.event_data["status"] == "success"
    assert model.event_data["path"] == "/var/log/test"


@pytest.mark.unit
def test_generic_kv_escaped_quotes():
    """Test GenericKVDecoderPlugin with escaped quotes in key-value pairs."""
    # Create a model with a test key-value message with escaped quotes
    msg = 'user="admin" path="/var/log/\\"test\\"" action=read'
    model = SyslogRFCBaseModel(
        timestamp=datetime(2025, 5, 16, 12, 34, 56, tzinfo=timezone.utc),
        facility=16,
        severity=6,
        message=msg,
    )

    # Initialize the decoder
    decoder = GenericKVDecoderPlugin()

    # Call the decode method
    result = decoder.decode(model)

    # Verify the result
    assert result is True
    assert "user" in model.event_data
    assert model.event_data["user"] == "admin"
    assert model.event_data["path"] == '/var/log/"test"'
    assert model.event_data["action"] == "read"


@pytest.mark.unit
def test_generic_kv_negative_case():
    """Test GenericKVDecoderPlugin with non-matching message format."""
    # Create a model with a message that should not match key-value format
    msg = "This is not a key-value formatted message"
    model = SyslogRFCBaseModel(
        timestamp=datetime(2025, 5, 16, 12, 34, 56, tzinfo=timezone.utc),
        facility=16,
        severity=6,
        message=msg,
    )

    # Initialize the decoder
    decoder = GenericKVDecoderPlugin()

    # Call the decode method
    result = decoder.decode(model)

    # Verify the result is False (no match)
    assert result is False
