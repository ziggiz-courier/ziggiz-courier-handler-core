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
"""Tests for the syslog RFC3164 encoder."""

# Standard library imports

# Third-party imports
import pytest

# Local/package imports
from core_data_processing.encoders.syslog_rfc3164_encoder import SyslogRFC3164Encoder
from core_data_processing.models.syslog_rfc3164 import SyslogRFC3164Message


@pytest.mark.unit
@pytest.mark.rfc3164
class TestSyslogRFC3164Encoder:
    """Test suite for the SyslogRFC3164Encoder class."""

    def test_encode_syslog_message(self):
        """Test encoding a SyslogRFC3164Message."""
        # Create an encoder
        encoder = SyslogRFC3164Encoder()

        # Create test messages
        # Import datetime for timestamp
        # Standard library imports
        from datetime import datetime

        test_cases = [
            (
                SyslogRFC3164Message(
                    facility=13,
                    severity=7,
                    message="This is a message",
                    timestamp=datetime.now(),
                ),
                "<111>This is a message",
            ),
            (
                SyslogRFC3164Message(
                    facility=13,
                    severity=7,
                    message="That is another message",
                    timestamp=datetime.now(),
                ),
                "<111>That is another message",
            ),
            (
                SyslogRFC3164Message(
                    facility=4,
                    severity=2,
                    message="Debug info",
                    timestamp=datetime.now(),  # 4 * 8 + 2 = 34
                ),
                "<34>Debug info",
            ),
        ]

        # Test each case
        for syslog_message, expected_output in test_cases:
            result = encoder.encode(syslog_message)
            assert result == expected_output
