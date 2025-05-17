# -*- coding: utf-8 -*-
# # SPDX-License-Identifier: BSL-1.1
# # Copyright (c) 2025 Ziggiz Inc.
# #
# # This file is part of the ziggiz-courier-core-data-processing and is licensed under the
# # Business Source License 1.1. You may not use this file except in
# # compliance with the License. You may obtain a copy of the License at:
# # https://github.com/ziggiz-courier/ziggiz-courier-core-data-processing/blob/main/LICENSE
"""Tests for the JSON encoder."""

# Standard library imports
import json

from datetime import datetime, timezone

# Third-party imports
import pytest

# Local/package imports
from ziggiz_courier_handler_core.encoders.json_encoder import JSONEncoder
from ziggiz_courier_handler_core.models.common import CommonEvent


@pytest.mark.unit
class TestJSONEncoder:
    """Test suite for the JSONEncoder class."""

    def test_encode_common_event(self):
        """Test encoding a CommonEvent to JSON."""
        # Create a sample event
        event = CommonEvent(
            event_id="test-123",
            timestamp=datetime(2025, 5, 9, 12, 30, 0, tzinfo=timezone.utc),
            event_type="test",
            source_system="test-system",
            source_component="test-component",
            message="Test message",
            severity="INFO",
            tags=["tag1", "tag2"],
            attributes={"attr1": "value1", "attr2": "value2"},
        )

        # Create encoder
        encoder = JSONEncoder()

        # Encode the event
        json_str = encoder.encode(event)

        # Verify it's valid JSON
        data = json.loads(json_str)

        # Verify the fields were encoded correctly
        assert data["event_id"] == "test-123"
        assert data["timestamp"] == "2025-05-09T12:30:00+00:00"
        assert data["event_type"] == "test"
        assert data["source_system"] == "test-system"
        assert data["source_component"] == "test-component"
        assert data["message"] == "Test message"
        assert data["severity"] == "INFO"
        assert "tag1" in data["tags"]
        assert "tag2" in data["tags"]
        assert data["attributes"]["attr1"] == "value1"
        assert data["attributes"]["attr2"] == "value2"
