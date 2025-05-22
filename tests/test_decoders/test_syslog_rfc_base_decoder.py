# -*- coding: utf-8 -*-
# SPDX-License-Identifier: BSL-1.1
# Copyright (c) 2025 Ziggiz Inc.
#
# This file is part of the ziggiz-courier-core-data-processing and is licensed under the
# Business Source License 1.1. You may not use this file except in
# compliance with the License. You may obtain a copy of the License at:
# https://github.com/ziggiz-courier/ziggiz-courier-core-data-processing/blob/main/LICENSE
#

"""Tests for the syslog RFC base decoder."""

# Standard library imports

# Third-party imports
import pytest

from tests.test_models.test_syslog_rfc_base import (
    FROM_PRIORITY_TEST_CASES,
    INVALID_PRIORITY_TEST_CASES,
)
from tests.test_utils.validation import validate_syslog_model

# Local/package imports
from ziggiz_courier_handler_core.decoders.syslog_rfc_base_decoder import (
    SyslogRFCBaseDecoder,
)
from ziggiz_courier_handler_core.models.syslog_rfc_base import Facility, Severity


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

        # Validate using our shared utility
        validate_syslog_model(
            result,
            facility=expected_facility.value,
            severity=expected_severity.value,
            message=f"This is a test message with {test_id}",
            priority=pri,
        )

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

        # Use validate_syslog_model for facility and severity validation
        validate_syslog_model(
            result, facility=expected_facility, severity=expected_severity
        )

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
            # Use validate_syslog_model for consistent validation
            validate_syslog_model(
                result,
                message=expected_message,
                facility=Facility.USER,
                severity=Severity.NOTICE,
            )

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

        # Decoding should return None
        result = decoder.decode(invalid_message)
        assert result is None
