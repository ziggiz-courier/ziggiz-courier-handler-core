# -*- coding: utf-8 -*-
# SPDX-License-Identifier: BSL-1.1
# Copyright (c) 2025 Ziggiz Inc.
#
# This file is part of the ziggiz-courier-core-data-processing and is licensed under the
# Business Source License 1.1. You may not use this file except in
# compliance with the License. You may obtain a copy of the License at:
# https://github.com/ziggiz-courier/ziggiz-courier-core-data-processing/blob/main/LICENSE
#

"""Tests for the syslog RFC3164 decoder."""

# Standard library imports
import ipaddress
import random
import string

from datetime import datetime
from typing import Optional

# Third-party imports
import pytest

from tests.test_decoders.utils.test_timestamp_parser import TIMESTAMP_PARSE_CASES
from tests.test_models.test_syslog_rfc_base import FROM_PRIORITY_TEST_CASES
from tests.test_utils.validation import validate_syslog_model

# Local/package imports
from ziggiz_courier_handler_core.decoders.syslog_rfc3164_decoder import (
    SyslogRFC3164Decoder,
)


def _random_mixed_case_hostname():
    base = "".join(random.choices(string.ascii_letters, k=8))
    return base[:4].lower() + base[4:].upper()


def _random_mixed_case_fqdn():
    parts = [
        "".join(random.choices(string.ascii_letters, k=5)),
        "".join(random.choices(string.ascii_letters, k=3)),
        "".join(random.choices(string.ascii_letters, k=2)),
    ]
    fqdn = ".".join(parts)
    # Randomly mix case
    return "".join(
        c.upper() if random.choice([True, False]) else c.lower() for c in fqdn
    )


def _random_mixed_case_ipv4():
    ip = ipaddress.IPv4Address(random.randint(0, 2**32 - 1))
    return str(ip)


def _random_mixed_case_ipv6():
    ip = ipaddress.IPv6Address(random.getrandbits(128))
    # Mix case in hex digits
    return "".join(
        c.upper() if c.isalpha() and random.choice([True, False]) else c
        for c in str(ip)
    )


HOSTNAME_NORMALIZATION_TEST_CASES = [
    # (input, expected, test_id)
    (_random_mixed_case_hostname(), lambda h: h.lower(), "random_mixed_case_hostname"),
    (_random_mixed_case_fqdn(), lambda f: f.lower(), "random_mixed_case_fqdn"),
    (_random_mixed_case_ipv4(), lambda i: i.lower(), "random_mixed_case_ipv4"),
    (_random_mixed_case_ipv6(), lambda i: i.lower(), "random_mixed_case_ipv6"),
    (None, lambda n: n, "none_hostname"),
]

# Test cases for _parse_hostname_tag
PARSE_HOSTNAME_TAG_TEST_CASES = [
    # Standard format: app[proc]: message
    ("app[123]: message", "app", "123", "message"),
    ("app[Abc]: message", "app", "Abc", "message"),
    ("app: message", "app", None, "message"),
    (": message", None, None, "message"),
    ("message", None, None, "message"),
    ("info message", None, None, "info message"),
]

# Sample timestamp formats for testing
TIMESTAMP_FORMATS = [
    # ISO format
    ("2023-05-11T10:24:05Z", "%Y-%m-%dT%H:%M:%SZ", "iso_basic"),
    # ISO with microseconds
    (
        "2023-05-11T10:24:05.123456Z",
        "%Y-%m-%dT%H:%M:%S.%fZ",
        "iso_with_microseconds",
    ),
    # RFC3164 standard format
    ("May 11 10:24:05", "%b %d %H:%M:%S", "rfc3164_standard"),
    # RFC3164 with year
    ("May 11 2023 10:24:05", "%b %d %Y %H:%M:%S", "rfc3164_with_year"),
    # Year first
    ("2023 May 11 10:24:05", "%Y %b %d %H:%M:%S", "year_first"),
    # Unix epoch seconds
    ("1683800645", "epoch_seconds", "unix_epoch_seconds"),
]


@pytest.mark.unit
@pytest.mark.rfc3164
class TestSyslogRFC3164Decoder:
    """Test suite for the SyslogRFC3164Decoder class."""

    @pytest.mark.parametrize(
        "input_hostname, expected_func, normalization_test_id",
        HOSTNAME_NORMALIZATION_TEST_CASES,
        ids=[tc[2] for tc in HOSTNAME_NORMALIZATION_TEST_CASES],
    )
    @pytest.mark.parametrize(
        "message, expected_app_name, expected_proc_id, expected_message",
        PARSE_HOSTNAME_TAG_TEST_CASES,
        ids=[
            "standard_format",
            "nondigitproc_standard_format",
            "no_proc_standard_format",
            "host_colon_format",
            "message",
            "info_message",
        ],
    )
    def test_parse_hostname_tag(
        self,
        input_hostname,
        expected_func,
        normalization_test_id,
        message: str,
        expected_app_name: Optional[str],
        expected_proc_id: Optional[str],
        expected_message: str,
    ):
        """Test parsing hostname, tag, and proc_id from different message formats and hostname normalization."""
        decoder = SyslogRFC3164Decoder()
        # Simulate message with hostname prefix if input_hostname is not None
        if input_hostname is not None:
            test_message = f"{input_hostname} {message}"
        else:
            test_message = message
        hostname, app_name, proc_id, content = decoder._parse_hostname_tag(test_message)
        expected_hostname = (
            expected_func(input_hostname) if input_hostname is not None else None
        )
        if expected_hostname is not None:
            expected_hostname = expected_hostname.lower()
            assert hostname == expected_hostname
        else:
            assert hostname is None
        assert app_name == expected_app_name
        assert proc_id == expected_proc_id
        assert content == expected_message

    @pytest.mark.parametrize(
        "pri, expected_facility, expected_severity, test_id",
        FROM_PRIORITY_TEST_CASES,
        ids=lambda test_id: test_id if isinstance(test_id, str) else str(test_id),
    )
    @pytest.mark.parametrize(
        "timestamp_str, _ts_formats, _ts_expected_attrs, _ts_id, _ts_reference_time",
        TIMESTAMP_PARSE_CASES,
        ids=[tc[3] for tc in TIMESTAMP_PARSE_CASES],
    )
    @pytest.mark.parametrize(
        "input_hostname, expected_func, normalization_test_id",
        HOSTNAME_NORMALIZATION_TEST_CASES,
        ids=[tc[2] for tc in HOSTNAME_NORMALIZATION_TEST_CASES],
    )
    @pytest.mark.parametrize(
        "message, expected_app_name, expected_proc_id, expected_message",
        PARSE_HOSTNAME_TAG_TEST_CASES,
        ids=[
            "standard_format",
            "nondigitproc_standard_format",
            "no_proc_standard_format",
            "host_colon_format",
            "message",
            "info_message",
        ],
    )
    def test_decode_combinations(
        self,
        pri,
        expected_facility,
        expected_severity,
        test_id,
        timestamp_str,
        _ts_formats,
        _ts_expected_attrs,
        _ts_id,
        _ts_reference_time,
        input_hostname,
        expected_func,
        normalization_test_id,
        message: str,
        expected_app_name: Optional[str],
        expected_proc_id: Optional[str],
        expected_message: str,
    ):
        """Test decoding full RFC3164 messages with various combinations of PRI, timestamp, and tag formats, using hostname normalization matrix, all valid PRI values, and all accepted timestamp formats."""
        decoder = SyslogRFC3164Decoder()
        # Simulate message with hostname prefix if input_hostname is not None
        if input_hostname is not None:
            tag_str = f"{input_hostname} {message}"
        else:
            tag_str = message
        raw_syslog = f"<{pri}>{timestamp_str} {tag_str}"
        result = decoder.decode(raw_syslog)

        expected_hostname = (
            expected_func(input_hostname) if input_hostname is not None else None
        )
        if expected_hostname is not None:
            expected_hostname = expected_hostname.lower()

        # Use validate_syslog_model utility for consistent validation
        validate_syslog_model(
            result,
            facility=expected_facility.value,
            severity=expected_severity.value,
            hostname=expected_hostname,
            app_name=expected_app_name,
            proc_id=expected_proc_id,
            message=expected_message,
        )

        # Validate timestamp which is specific to this test
        assert isinstance(result.timestamp, datetime)

    # def test_decode_minimal_message(self):
    #     """Test decoding a minimal RFC3164 message (just PRI and content)."""
    #     decoder = SyslogRFC3164Decoder()
    #     raw_syslog = "<13>Simple test message"

    #     result = decoder.decode(raw_syslog)

    #     assert result.facility == 1  # 13 // 8 = 1 (USER)
    #     assert result.severity == 5  # 13 % 8 = 5 (NOTICE)
    #     assert result.message == "Simple test message"
    #     assert result.timestamp is None
    #     assert result.hostname is None
    #     assert result.app_name is None
    #     assert result.proc_id is None

    def test_decode_invalid_format(self):
        """Test that the decoder raises ValueError for invalid format."""
        decoder = SyslogRFC3164Decoder()

        with pytest.raises(ValueError, match="Invalid BSD-style syslog format"):
            decoder.decode("This is not a valid syslog message")

    def test_decode_with_space_after_pri(self):
        """Test decoding a message with space after PRI."""
        decoder = SyslogRFC3164Decoder()
        raw_syslog = "<13> May 11 10:24:05 host1 app[123]: Test with space after PRI"

        result = decoder.decode(raw_syslog)

        # Use validate_syslog_model for consistent validation
        validate_syslog_model(
            result,
            facility=1,
            severity=5,
            hostname="host1",
            app_name="app",
            proc_id="123",
            message="Test with space after PRI",
        )
        assert isinstance(result.timestamp, datetime)

    def test_common_words_hostname_filtering(self):
        """Test how common words are treated in hostname field."""
        decoder = SyslogRFC3164Decoder()

        # Create a message where the first word is in COMMON_WORDS list
        message = "error this is an error message"
        hostname, app_name, proc_id, content = decoder._parse_hostname_tag(message)

        # Based on current implementation behavior
        assert hostname is None
        assert app_name is None
        assert proc_id is None
        assert content == "error this is an error message"

    # def test_decode_with_malformed_pri(self):
    #     """Test decoding a message with malformed PRI value."""
    #     decoder = SyslogRFC3164Decoder()

    #     # Test a message with invalid PRI format (non-digit)
    #     # The implementation handles malformed PRI values by assigning default values
    #     result = decoder.decode("<abc>This is a test message")

    #     # Based on actual implementation, it assigns default values
    #     assert result.message == "This is a test message"
    #     assert result.timestamp is None
    #     assert result.hostname is None
    #     assert result.app_name is None
    #     assert result.proc_id is None
    #     # Default values for facility and severity
    #     assert result.facility == 13  # Default facility
    #     assert result.severity == 7  # Default severity

    # @pytest.mark.unit
    # def test_decode_non_json_message_event_data_none(self):
    #     """
    #     Test that a non-JSON message results in event_data=None.
    #     """
    #     decoder = SyslogRFC3164Decoder()
    #     raw_syslog = "<111>not a json string"
    #     result = decoder.decode(raw_syslog)
    #     assert result.message == "not a json string"
    #     assert result.event_data is None
