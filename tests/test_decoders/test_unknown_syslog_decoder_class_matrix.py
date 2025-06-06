# -*- coding: utf-8 -*-
# SPDX-License-Identifier: BSL-1.1
# Copyright (c) 2025 Ziggiz Inc.
#
# This file is part of the ziggiz-courier-core-data-processing and is licensed under the
# Business Source License 1.1. You may not use this file except in
# compliance with the License. You may obtain a copy of the License at:
# https://github.com/ziggiz-courier/ziggiz-courier-core-data-processing/blob/main/LICENSE
#

"""Class detection tests for UnknownSyslogDecoder using RFC3164 test matrix."""
# Third-party imports
import pytest

from tests.test_decoders.test_syslog_rfc3164_decoder import (
    HOSTNAME_NORMALIZATION_TEST_CASES,
    PARSE_HOSTNAME_TAG_TEST_CASES,
)
from tests.test_decoders.utils.test_timestamp_parser import TIMESTAMP_PARSE_CASES
from tests.test_models.test_syslog_rfc_base import FROM_PRIORITY_TEST_CASES
from tests.test_utils.validation import validate_syslog_model

# Local/package imports
from ziggiz_courier_handler_core.decoders.unknown_syslog_decoder import (
    UnknownSyslogDecoder,
)
from ziggiz_courier_handler_core.models.syslog_rfc3164 import SyslogRFC3164Message


@pytest.mark.unit
@pytest.mark.rfc3164
class TestUnknownSyslogDecoderClassMatrixRFC3164:
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
    def test_unknown_decoder_returns_rfc3164_class_matrix(
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
        expected_app_name: str,
        expected_proc_id: str,
        expected_message: str,
    ):
        """Test UnknownSyslogDecoder returns SyslogRFC3164Message for valid RFC3164 messages using the full parameter matrix."""
        decoder = UnknownSyslogDecoder()
        # Simulate message with hostname prefix if input_hostname is not None
        if input_hostname is not None:
            tag_str = f"{input_hostname} {message}"
        else:
            tag_str = message
        raw_syslog = f"<{pri}>{timestamp_str} {tag_str}"
        result = decoder.decode(raw_syslog)
        # First assert the correct instance type
        assert isinstance(result, SyslogRFC3164Message), f"Failed for: {raw_syslog}"
        # Now use the validation utility for deeper validation
        expected_hostname = (
            expected_func(input_hostname) if input_hostname is not None else None
        )
        if expected_hostname is not None:
            expected_hostname = expected_hostname.lower()
        validate_syslog_model(
            result,
            facility=int(expected_facility),
            severity=int(expected_severity),
            hostname=expected_hostname,
            app_name=expected_app_name,
            proc_id=expected_proc_id,
            message=expected_message,
        )


@pytest.mark.rfc5424
@pytest.mark.parametrize(
    "pri, expected_facility, expected_severity, test_id",
    FROM_PRIORITY_TEST_CASES,
    ids=lambda test_id: test_id if isinstance(test_id, str) else str(test_id),
)
@pytest.mark.parametrize(
    "timestamp, is_nil_timestamp",
    [
        ("2025-05-09T12:30:00Z", False),
        ("-", True),
    ],
    ids=["standard_timestamp", "nil_timestamp"],
)
@pytest.mark.parametrize(
    "hostname, expected_hostname",
    [
        ("test-host", "test-host"),
        ("server.example.com", "server.example.com"),
        ("SERVER.EXAMPLE.COM", "server.example.com"),
        ("192.168.0.1", "192.168.0.1"),
        ("2001:db8::1", "2001:db8::1"),
        ("-", None),
    ],
    ids=["hostname", "fqdn", "mixed_case", "ipv4", "ipv6", "nil"],
)
@pytest.mark.parametrize(
    "app_name, expected_app_name",
    [
        ("app1", "app1"),
        ("-", None),
    ],
    ids=["app_name", "nil_app_name"],
)
@pytest.mark.parametrize(
    "proc_id, expected_proc_id",
    [
        ("1234", "1234"),
        ("-", None),
    ],
    ids=["proc_id", "nil_proc_id"],
)
@pytest.mark.parametrize(
    "msg_id, expected_msg_id",
    [
        ("ID47", "ID47"),
        ("-", None),
    ],
    ids=["msg_id", "nil_msg_id"],
)
def test_unknown_decoder_returns_rfc5424_class_matrix(
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
    """Test UnknownSyslogDecoder returns SyslogRFC5424Message for valid RFC5424 messages using the full parameter matrix."""
    # Local/package imports
    from ziggiz_courier_handler_core.models.syslog_rfc5424 import SyslogRFC5424Message

    decoder = UnknownSyslogDecoder()
    raw_syslog = f'<{pri}>1 {timestamp} {hostname} {app_name} {proc_id} {msg_id} [test@32473 iut="3"] This is a test message with {test_id}'
    result = decoder.decode(raw_syslog)

    # First assert the correct instance type
    assert isinstance(result, SyslogRFC5424Message), f"Failed for: {raw_syslog}"

    # Use validation utility instead of separate assertions
    validate_syslog_model(
        result,
        facility=int(expected_facility),
        severity=int(expected_severity),
        hostname=expected_hostname,
        app_name=expected_app_name,
        proc_id=expected_proc_id,
        msg_id=expected_msg_id,
        message=f"This is a test message with {test_id}",
        structured_data={"test@32473": {"iut": "3"}},
    )

    # Check timestamp specifically as it needs custom validation logic
    assert result.timestamp is not None
    assert result.timestamp.tzinfo is not None
    if is_nil_timestamp:
        # Standard library imports
        from datetime import datetime

        local_now = datetime.now().astimezone()
        assert result.timestamp.tzinfo == local_now.tzinfo
        time_diff = abs((result.timestamp - local_now).total_seconds())
        assert time_diff < 5, f"Timestamp difference too large: {time_diff} seconds"
    else:
        assert result.timestamp.year == 2025
        assert result.timestamp.month == 5
        assert result.timestamp.day == 9


def benchmark_unknown_syslog_decoder_rfc3164():
    """Benchmark UnknownSyslogDecoder.decode() with a constant RFC3164 message 100,000 times, reporting CPU usage."""
    # Standard library imports
    import logging
    import resource
    import time

    # Local/package imports
    from ziggiz_courier_handler_core.decoders.unknown_syslog_decoder import (
        UnknownSyslogDecoder,
    )

    logger = logging.getLogger(__name__)
    logging.basicConfig(
        level=logging.INFO,
    )

    message_field = "A" * 800
    raw_syslog = f"<34>Oct 11 22:14:15 mymachine su: {message_field}"
    decoder = UnknownSyslogDecoder()
    iterations = 200000
    start = time.perf_counter()
    usage_start = resource.getrusage(resource.RUSAGE_SELF)
    iteration = 0
    while iteration < iterations:
        decoder.decode(raw_syslog)
        iteration += 1
    elapsed = time.perf_counter() - start
    usage_end = resource.getrusage(resource.RUSAGE_SELF)
    user_cpu = usage_end.ru_utime - usage_start.ru_utime
    sys_cpu = usage_end.ru_stime - usage_start.ru_stime
    total_cpu = user_cpu + sys_cpu
    cpu_util = (total_cpu / elapsed * 100) if elapsed > 0 else None
    measured = {
        "iterations": iterations,
        "elapsed_seconds": elapsed,
        "user_cpu_seconds": round(user_cpu, 4),
        "sys_cpu_seconds": round(sys_cpu, 4),
        "cpu_util_percent": round(cpu_util, 2) if cpu_util is not None else None,
        "msg_per_sec": int(iterations / elapsed) if elapsed > 0 else None,
        "Mi_per_sec": (
            round((iterations * 800) / (1024 * 1024) / elapsed, 2)
            if elapsed > 0
            else None
        ),
    }
    logger.info(f"Benchmark completed for UnknownSyslogDecoder.decode() {measured}")


def benchmark_unknown_syslog_decoder_rfc5424():
    """Benchmark UnknownSyslogDecoder.decode() with a constant RFC5424 message 100,000 times, reporting CPU usage."""
    # Standard library imports
    import logging
    import resource
    import time

    # Local/package imports
    from ziggiz_courier_handler_core.decoders.unknown_syslog_decoder import (
        UnknownSyslogDecoder,
    )

    logger = logging.getLogger(__name__)
    logging.basicConfig(
        level=logging.INFO,
    )

    message_field = "A" * 800
    raw_syslog = f'<34>1 2025-05-09T12:30:00Z test-host app1 1234 ID47 [test@32473 iut="3"] {message_field}'
    decoder = UnknownSyslogDecoder()
    iterations = 200000
    start = time.perf_counter()
    usage_start = resource.getrusage(resource.RUSAGE_SELF)
    iteration = 0
    while iteration < iterations:
        decoder.decode(raw_syslog)
        iteration += 1
    elapsed = time.perf_counter() - start
    usage_end = resource.getrusage(resource.RUSAGE_SELF)
    user_cpu = usage_end.ru_utime - usage_start.ru_utime
    sys_cpu = usage_end.ru_stime - usage_start.ru_stime
    total_cpu = user_cpu + sys_cpu
    cpu_util = (total_cpu / elapsed * 100) if elapsed > 0 else None
    measured = {
        "iterations": iterations,
        "elapsed_seconds": elapsed,
        "user_cpu_seconds": round(user_cpu, 4),
        "sys_cpu_seconds": round(sys_cpu, 4),
        "cpu_util_percent": round(cpu_util, 2) if cpu_util is not None else None,
        "msg_per_sec": int(iterations / elapsed) if elapsed > 0 else None,
        "Mi_per_sec": (
            round((iterations * 800) / (1024 * 1024) / elapsed, 2)
            if elapsed > 0
            else None
        ),
    }
    logger.info(f"Benchmark completed for UnknownSyslogDecoder.decode() {measured}")


if __name__ == "__main__":
    # Standard library imports
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "rfc5424":
        benchmark_unknown_syslog_decoder_rfc5424()
    else:
        benchmark_unknown_syslog_decoder_rfc3164()
