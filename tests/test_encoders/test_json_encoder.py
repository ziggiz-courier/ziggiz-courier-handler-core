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
"""Tests for the JSON encoder."""

# Standard library imports
import json

from datetime import datetime, timezone

# Third-party imports
import pytest

# Local/package imports
from core_data_processing.encoders.json_encoder import JSONEncoder
from core_data_processing.models.common import CommonEvent


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
