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
"""Tests for the syslog RFC3164 model."""

# Standard library imports
from datetime import datetime

# Third-party imports
import pytest

# Local/package imports
from core_data_processing.models.syslog_rfc3164 import SyslogRFC3164Message


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
