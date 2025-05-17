# -*- coding: utf-8 -*-
# # SPDX-License-Identifier: BSL-1.1
# # Copyright (c) 2025 Ziggiz Inc.
# #
# # This file is part of the ziggiz-courier-core-data-processing and is licensed under the
# # Business Source License 1.1. You may not use this file except in
# # compliance with the License. You may obtain a copy of the License at:
# # https://github.com/ziggiz-courier/ziggiz-courier-core-data-processing/blob/main/LICENSE
"""Tests for the syslog RFC3164 model."""

# Standard library imports
from datetime import datetime

# Third-party imports
import pytest

# Local/package imports
from ziggiz_courier_handler_core.models.syslog_rfc3164 import SyslogRFC3164Message


@pytest.mark.unit
@pytest.mark.rfc3164
class TestSyslogRFC3164Message:
    """Test suite for the SyslogRFC3164Message class."""

    def test_model_creation(self):
        """Test creating a SyslogRFC3164Message instance."""
        # Create with required fields
        now = datetime.now()
        message = SyslogRFC3164Message(
            facility=13, severity=7, message="This is a message", timestamp=now
        )

        assert message.facility == 13
        assert message.severity == 7
        assert (
            message.message == "This is a message"
        )  # message is now from EventEnvelopeBaseModel
        assert message.timestamp == now  # timestamp is now required

        # Create with all fields
        now = datetime.now()
        message = SyslogRFC3164Message(
            facility=13, severity=7, message="This is a message", timestamp=now
        )

        assert message.facility == 13
        assert message.severity == 7
        assert message.message == "This is a message"
        assert message.timestamp == now

    def test_inherited_methods(self):
        """Test methods inherited from SyslogRFCBaseModel."""
        now = datetime.now()
        message = SyslogRFC3164Message(
            facility=13, severity=7, message="This is a message", timestamp=now
        )

        # Calculate priority
        assert message.get_priority() == 111  # 13 * 8 + 7 = 111

        # Create from priority
        new_message = SyslogRFC3164Message.from_priority(
            pri=34, message="Another message"  # Facility 4, Severity 2
        )

        assert new_message.facility == 4
        assert new_message.severity == 2
        assert new_message.message == "Another message"
