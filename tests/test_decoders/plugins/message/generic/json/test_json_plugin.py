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

from tests.test_utils.validation import validate_source_producer

# Local/package imports
from ziggiz_courier_handler_core.decoders.plugins.message.generic.json.plugin import (
    GenericJSONDecoderPlugin,
)
from ziggiz_courier_handler_core.models.syslog_rfc_base import SyslogRFCBaseModel


@pytest.mark.unit
def test_generic_json_basic_case():
    """Test GenericJSONDecoderPlugin with basic JSON message format."""
    # Create a model with a test JSON message
    msg = '{"event": "login", "user": "admin", "status": "success"}'
    # Standard library imports
    from datetime import datetime, timezone

    model = SyslogRFCBaseModel(
        timestamp=datetime(2025, 5, 16, 12, 34, 56, tzinfo=timezone.utc),
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
    # Check handler_data for the decoder's FQCN
    key = "GenericJSONDecoderPlugin"
    assert model.handler_data is not None
    assert key in model.handler_data

    handler_info = model.handler_data[key]
    validate_source_producer(
        model,
        expected_organization="generic",
        expected_product="unknown_json",
        handler_key=key,
    )
    assert handler_info["msgclass"] == "unknown"

    # Verify specific fields in the parsed data
    assert model.event_data is not None
    assert "event" in model.event_data
    assert model.event_data["event"] == "login"
    assert "user" in model.event_data
    assert model.event_data["user"] == "admin"
    assert "status" in model.event_data
    assert model.event_data["status"] == "success"


@pytest.mark.unit
def test_generic_json_nested_data():
    """Test GenericJSONDecoderPlugin with nested JSON data."""
    # Create a model with a test JSON message with nested structure
    msg = (
        '{"user": {"id": 123, "name": "John"}, "actions": ["login", "view_dashboard"]}'
    )
    # Standard library imports
    from datetime import datetime, timezone

    model = SyslogRFCBaseModel(
        timestamp=datetime(2025, 5, 16, 12, 34, 56, tzinfo=timezone.utc),
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
    key = "GenericJSONDecoderPlugin"
    assert model.handler_data is not None
    assert key in model.handler_data
    handler_entry = model.handler_data[key]
    validate_source_producer(
        model,
        expected_organization="generic",
        expected_product="unknown_json",
        handler_key=key,
    )
    assert handler_entry["msgclass"] == "unknown"
    # Check event data
    assert model.event_data is not None
    assert "user" in model.event_data
    assert model.event_data["user"] == {"id": 123, "name": "John"}
    assert "actions" in model.event_data
    assert model.event_data["actions"] == ["login", "view_dashboard"]


@pytest.mark.unit
def test_generic_json_negative_case():
    """Test GenericJSONDecoderPlugin with non-matching message format."""
    # Create a model with a message that should not match JSON format
    msg = "This is not a JSON formatted message"
    # Standard library imports
    from datetime import datetime, timezone

    model = SyslogRFCBaseModel(
        timestamp=datetime(2025, 5, 16, 12, 34, 56, tzinfo=timezone.utc),
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
