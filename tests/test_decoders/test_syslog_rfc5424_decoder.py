# -*- coding: utf-8 -*-
# # SPDX-License-Identifier: BSL-1.1
# # Copyright (c) 2025 Ziggiz Inc.
# #
# # This file is part of the ziggiz-courier-core-data-processing and is licensed under the
# # Business Source License 1.1. You may not use this file except in
# # compliance with the License. You may obtain a copy of the License at:
# # https://github.com/ziggiz-courier/ziggiz-courier-core-data-processing/blob/main/LICENSE
"""Tests for the syslog RFC5424 decoder."""

# Standard library imports
from datetime import datetime

# Third-party imports
import pytest

from tests.test_models.test_syslog_rfc_base import (
    FROM_PRIORITY_TEST_CASES,
    INVALID_PRIORITY_TEST_CASES,
)

# Local/package imports
from core_data_processing.decoders.syslog_rfc5424_decoder import SyslogRFC5424Decoder


@pytest.mark.unit
@pytest.mark.rfc5424
class TestSyslogRFC5424Decoder:
    """Test suite for the SyslogRFC5424Decoder class."""

    @pytest.mark.parametrize(
        "pri, expected_facility, expected_severity, test_id",
        FROM_PRIORITY_TEST_CASES,
        ids=lambda test_id: test_id if isinstance(test_id, str) else str(test_id),
    )
    @pytest.mark.parametrize(
        "timestamp, is_nil_timestamp",
        [
            ("2025-05-09T12:30:00Z", False),  # Standard timestamp
            ("-", True),  # Nil timestamp
        ],
        ids=["standard_timestamp", "nil_timestamp"],
    )
    @pytest.mark.parametrize(
        "hostname, expected_hostname",
        [
            ("test-host", "test-host"),  # Basic hostname
            ("server.example.com", "server.example.com"),  # FQDN
            (
                "SERVER.EXAMPLE.COM",
                "server.example.com",
            ),  # Mixed case FQDN, should be lowercase
            ("192.168.0.1", "192.168.0.1"),  # IPv4 address
            ("2001:db8::1", "2001:db8::1"),  # IPv6 address
            ("-", None),  # Nil value
        ],
        ids=["hostname", "fqdn", "mixed_case", "ipv4", "ipv6", "nil"],
    )
    @pytest.mark.parametrize(
        "app_name, expected_app_name",
        [
            ("app1", "app1"),  # Valid app name
            ("-", None),  # Nil value
        ],
        ids=["app_name", "nil_app_name"],
    )
    @pytest.mark.parametrize(
        "proc_id, expected_proc_id",
        [
            ("1234", "1234"),  # Valid proc id
            ("-", None),  # Nil value
        ],
        ids=["proc_id", "nil_proc_id"],
    )
    @pytest.mark.parametrize(
        "msg_id, expected_msg_id",
        [
            ("ID47", "ID47"),  # Valid message id
            ("-", None),  # Nil value
        ],
        ids=["msg_id", "nil_msg_id"],
    )
    def test_decode_valid_syslog(
        self,
        pri,
        expected_facility,
        expected_severity,
        test_id,
        timestamp,
        is_nil_timestamp,
        hostname,
        expected_hostname,
        app_name,
        expected_app_name,
        proc_id,
        expected_proc_id,
        msg_id,
        expected_msg_id,
    ):
        """Test decoding a valid syslog message with different priority values, timestamps and hostnames."""
        # Create a decoder
        decoder = SyslogRFC5424Decoder()

        # Sample syslog message (RFC5424 format) using the test parameters
        raw_syslog = f'<{pri}>1 {timestamp} {hostname} {app_name} {proc_id} {msg_id} [test@32473 iut="3"] This is a test message with {test_id}'

        # Decode the message
        result = decoder.decode(raw_syslog)

        # Verify the parsed message
        assert result.facility == int(expected_facility)
        assert result.severity == int(expected_severity)
        assert result.hostname == expected_hostname
        assert result.app_name == expected_app_name
        assert result.proc_id == expected_proc_id
        assert result.msg_id == expected_msg_id
        assert result.message == f"This is a test message with {test_id}"
        assert result.structured_data == {"test@32473": {"iut": "3"}}

        # Verify timestamp handling
        assert result.timestamp is not None
        assert result.timestamp.tzinfo is not None  # Should be timezone-aware

        if is_nil_timestamp:
            # For nil timestamps, verify it's close to current time
            local_now = datetime.now().astimezone()
            assert result.timestamp.tzinfo == local_now.tzinfo
            time_diff = abs((result.timestamp - local_now).total_seconds())
            assert time_diff < 5, f"Timestamp difference too large: {time_diff} seconds"
        else:
            # For standard timestamps, verify the parsed date
            assert result.timestamp.year == 2025
            assert result.timestamp.month == 5
            assert result.timestamp.day == 9

    def test_decode_invalid_syslog(self):
        """Test decoding an invalid syslog message."""
        # Create a decoder
        decoder = SyslogRFC5424Decoder()

        # Invalid syslog message
        invalid_syslog = "This is not a valid syslog message"

        # Decoding should raise an error
        with pytest.raises(ValueError):
            decoder.decode(invalid_syslog)

    @pytest.mark.parametrize(
        "pri, expected_facility, expected_severity, test_id",
        INVALID_PRIORITY_TEST_CASES,
        ids=lambda test_id: test_id if isinstance(test_id, str) else str(test_id),
    )
    def test_decode_with_invalid_priority(
        self, pri, expected_facility, expected_severity, test_id
    ):
        """Test decoding syslog messages with invalid priority values."""
        # Create a decoder
        decoder = SyslogRFC5424Decoder()

        # Create a syslog message with the test priority
        raw_syslog = f"<{pri}>1 2025-05-09T12:30:00Z test-host app1 1234 ID47 - Test with {test_id}"

        # Decode the message
        result = decoder.decode(raw_syslog)

        # Verify proper handling of invalid priority
        assert result.facility == int(expected_facility)
        assert result.severity == int(expected_severity)

        # The message should contain meaningful content
        assert result.message is not None
        assert len(result.message) > 0
