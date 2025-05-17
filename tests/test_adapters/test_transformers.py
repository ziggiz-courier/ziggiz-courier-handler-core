# -*- coding: utf-8 -*-
# # SPDX-License-Identifier: BSL-1.1
# # Copyright (c) 2025 Ziggiz Inc.
# #
# # This file is part of the ziggiz-courier-core-data-processing and is licensed under the
# # Business Source License 1.1. You may not use this file except in
# # compliance with the License. You may obtain a copy of the License at:
# # https://github.com/ziggiz-courier/ziggiz-courier-core-data-processing/blob/main/LICENSE
# # SPDX-License-Identifier: BSL-1.1
# # Copyright (c) 2025 Ziggiz Inc.
# #
# # This file is part of the ziggiz-courier-ziggiz-courier-handler-core and is licensed under the
# # Business Source License 1.1. You may not use this file except in
# # compliance with the License. You may obtain a copy of the License at:
# # https://github.com/ziggiz-courier/ziggiz-courier-ziggiz-courier-handler-core/blob/main/LICENSE
"""Tests for the model adapters."""

# Standard library imports
from datetime import datetime, timezone

# Third-party imports
import pytest

# Local/package imports
from ziggiz_courier_handler_core.adapters.transformers import SyslogToCommonEventAdapter
from ziggiz_courier_handler_core.models.syslog_rfc5424 import SyslogRFC5424Message


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
