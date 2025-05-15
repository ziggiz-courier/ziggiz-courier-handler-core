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
"""Tests for the syslog RFC base decoder."""

# Standard library imports

# Third-party imports
import pytest

from tests.test_models.test_syslog_rfc_base import (
    FROM_PRIORITY_TEST_CASES,
    INVALID_PRIORITY_TEST_CASES,
)

# Local/package imports
from core_data_processing.decoders.syslog_rfc_base_decoder import (
    SyslogRFCBaseDecoder,
)
from core_data_processing.models.syslog_rfc_base import Facility, Severity


@pytest.mark.unit
class TestSyslogRFCBaseDecoder:
    """Test suite for the SyslogRFCBaseDecoder class."""

    @pytest.mark.parametrize(
        "pri, expected_facility, expected_severity, test_id",
        FROM_PRIORITY_TEST_CASES,
        ids=lambda test_id: test_id if isinstance(test_id, str) else str(test_id),
    )
    def test_decode_valid_pri(self, pri, expected_facility, expected_severity, test_id):
        """Test decoding valid priority values."""
        # Create a decoder
        decoder = SyslogRFCBaseDecoder()

        # Sample syslog message with just PRI and message
        raw_syslog = f"<{pri}>This is a test message with {test_id}"

        # Decode the message
        result = decoder.decode(raw_syslog)

        # Verify the decoder correctly extracted PRI components
        assert result.get_facility_enum() == expected_facility
        assert result.get_severity_enum() == expected_severity
        assert result.message == f"This is a test message with {test_id}"

    @pytest.mark.parametrize(
        "pri, expected_facility, expected_severity, test_id",
        INVALID_PRIORITY_TEST_CASES,
        ids=lambda test_id: test_id if isinstance(test_id, str) else str(test_id),
    )
    def test_decode_invalid_pri(
        self, pri, expected_facility, expected_severity, test_id
    ):
        """Test decoding invalid priority values."""
        # Create a decoder
        decoder = SyslogRFCBaseDecoder()

        # Skip None which can't be used in a string format
        if pri is None:
            raw_syslog = "<>Test message with invalid priority"
        else:
            raw_syslog = f"<{pri}>Test message with {test_id}"

        # Decode the message
        result = decoder.decode(raw_syslog)

        # Verify the decoder handles invalid PRI correctly
        assert result.get_facility_enum() == expected_facility
        assert result.get_severity_enum() == expected_severity

        # Verify message is captured correctly
        if pri is None:
            assert result.message == "Test message with invalid priority"
        else:
            assert result.message == f"Test message with {test_id}"

    def test_decode_spaces_after_pri(self):
        """Test decoding with spaces after the PRI bracket."""
        decoder = SyslogRFCBaseDecoder()

        # Test with different amounts of spaces after PRI
        test_cases = [
            ("<13>   Message with spaces", "Message with spaces"),
            ("<13> Message with one space", "Message with one space"),
            ("<13>\tMessage with tab", "Message with tab"),
            ("<13>\n\rMessage with newlines", "Message with newlines"),
        ]

        for raw_syslog, expected_message in test_cases:
            result = decoder.decode(raw_syslog)
            assert result.message == expected_message
            # Verify facility and severity (13 = 1 << 3 | 5 = USER.NOTICE)
            assert result.get_facility_enum() == Facility.USER
            assert result.get_severity_enum() == Severity.NOTICE

    @pytest.mark.parametrize(
        "invalid_message",
        [
            "No PRI field at all",
            "Incomplete <13",
            "< >Empty PRI field",
        ],
        ids=[
            "no_pri_field",
            "incomplete_pri",
            "empty_pri_field",
        ],
    )
    def test_invalid_format(self, invalid_message):
        """Test decoding messages with invalid syslog format."""
        decoder = SyslogRFCBaseDecoder()

        with pytest.raises(ValueError, match="Invalid syslog format"):
            decoder.decode(invalid_message)
