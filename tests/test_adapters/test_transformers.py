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
"""Tests for the model adapters."""

# Standard library imports
from datetime import datetime, timezone

# Third-party imports
import pytest

# Local/package imports
from core_data_processing.adapters.transformers import SyslogToCommonEventAdapter
from core_data_processing.models.syslog_rfc5424 import SyslogRFC5424Message


@pytest.mark.unit
class TestSyslogToCommonEventAdapter:
    """Test suite for the SyslogToCommonEventAdapter."""

    def test_transform(self):
        """Test transforming a SyslogRFC5424Message to CommonEvent."""
        # Create a sample syslog message
        syslog = SyslogRFC5424Message(
            facility=4,
            severity=2,
            timestamp=datetime(2025, 5, 9, 12, 30, 0, tzinfo=timezone.utc),
            hostname="test-host",
            app_name="test-app",
            proc_id="12345",
            msg_id="ID123",
            message="Test syslog message",
            structured_data={"test@12345": {"key1": "value1", "key2": "value2"}},
        )

        # Create the adapter
        adapter = SyslogToCommonEventAdapter()

        # Transform the message
        event = adapter.transform(syslog)

        # Verify the transformation
        assert event.timestamp == syslog.timestamp
        assert (
            event.event_time is None
        )  # Should be None since we're not setting it specifically
        assert event.event_type == "syslog"
        assert event.source_system == syslog.hostname
        assert event.source_component == "system"  # Based on FACILITY_MAP[4]
        assert event.message == syslog.message
        assert event.severity == "CRITICAL"  # Based on SEVERITY_MAP[2]
        assert "test@12345" in event.tags
        assert event.attributes["test@12345.key1"] == "value1"
        assert event.attributes["test@12345.key2"] == "value2"
