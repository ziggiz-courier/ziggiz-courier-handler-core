# -*- coding: utf-8 -*-
# # SPDX-License-Identifier: BSL-1.1
# # Copyright (c) 2025 Ziggiz Inc.
# #
# # This file is part of the ziggiz-courier-core-data-processing and is licensed under the
# # Business Source License 1.1. You may not use this file except in
# # compliance with the License. You may obtain a copy of the License at:
# # https://github.com/ziggiz-courier/ziggiz-courier-core-data-processing/blob/main/LICENSE
"""
Unit tests for GenericJSONDecoderPlugin.
"""
# Third-party imports
import pytest

# Local/package imports
from core_data_processing.decoders.plugins.message.generic.json.plugin import (
    GenericJSONDecoderPlugin,
)
from core_data_processing.models.syslog_rfc_base import SyslogRFCBaseModel


@pytest.mark.unit
def test_generic_json_basic_case():
    """Test GenericJSONDecoderPlugin with basic JSON message format."""
    # Create a model with a test JSON message
    msg = '{"event": "login", "user": "admin", "status": "success"}'
    model = SyslogRFCBaseModel(
        timestamp="2025-05-16T12:34:56.000Z",
        facility=16,  # LOCAL0
        severity=6,  # INFO
        message=msg,
    )

    # Initialize the decoder with an empty cache
    decoder = GenericJSONDecoderPlugin()

    # Call the decode method
    result = decoder.decode(model)

    # Verify the result
    assert result is True
    assert model.structure_classification.vendor == "generic"
    assert model.structure_classification.product == "unknown_json"
    assert model.structure_classification.msgclass == "unknown"

    # Verify specific fields in the parsed data
    assert "event" in model.event_data
    assert model.event_data["event"] == "login"
    assert model.event_data["user"] == "admin"
    assert model.event_data["status"] == "success"


@pytest.mark.unit
def test_generic_json_nested_data():
    """Test GenericJSONDecoderPlugin with nested JSON data."""
    # Create a model with a test JSON message with nested structure
    msg = (
        '{"user": {"id": 123, "name": "John"}, "actions": ["login", "view_dashboard"]}'
    )
    model = SyslogRFCBaseModel(
        timestamp="2025-05-16T12:34:56.000Z",
        facility=16,
        severity=6,
        message=msg,
    )

    # Initialize the decoder
    decoder = GenericJSONDecoderPlugin()

    # Call the decode method
    result = decoder.decode(model)

    # Verify the result
    assert result is True
    assert "user" in model.event_data
    assert model.event_data["user"] == {"id": 123, "name": "John"}
    assert "actions" in model.event_data
    assert model.event_data["actions"] == ["login", "view_dashboard"]


@pytest.mark.unit
def test_generic_json_negative_case():
    """Test GenericJSONDecoderPlugin with non-matching message format."""
    # Create a model with a message that should not match JSON format
    msg = "This is not a JSON formatted message"
    model = SyslogRFCBaseModel(
        timestamp="2025-05-16T12:34:56.000Z",
        facility=16,
        severity=6,
        message=msg,
    )

    # Initialize the decoder
    decoder = GenericJSONDecoderPlugin()

    # Call the decode method
    result = decoder.decode(model)

    # Verify the result is False (no match)
    assert result is False
