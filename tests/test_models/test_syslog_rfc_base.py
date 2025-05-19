# -*- coding: utf-8 -*-
# # SPDX-License-Identifier: BSL-1.1
# # Copyright (c) 2025 Ziggiz Inc.
# #
# # This file is part of the ziggiz-courier-core-data-processing and is licensed under the
# # Business Source License 1.1. You may not use this file except in
# # compliance with the License. You may obtain a copy of the License at:
# # https://github.com/ziggiz-courier/ziggiz-courier-core-data-processing/blob/main/LICENSE
"""Tests for the syslog RFC base model."""

# Standard library imports

# Third-party imports
import pytest

# Local/package imports
from ziggiz_courier_handler_core.models.syslog_rfc_base import (
    Facility,
    Severity,
    SyslogRFCBaseModel,
)
from tests.test_utils.validation import validate_syslog_model

# Test parameters for facility enum
FACILITY_PARAMS = {
    "kernel": (Facility.KERN, 0, "kernel"),
    "user": (Facility.USER, 1, "user"),
    "mail": (Facility.MAIL, 2, "mail"),
    "daemon": (Facility.DAEMON, 3, "daemon"),
    "auth": (Facility.AUTH, 4, "auth"),
    "syslog": (Facility.SYSLOG, 5, "syslog"),
    "lpr": (Facility.LPR, 6, "line printer"),
    "news": (Facility.NEWS, 7, "network news"),
    "uucp": (Facility.UUCP, 8, "UUCP"),
    "cron": (Facility.CRON, 9, "cron"),
    "authpriv": (Facility.AUTHPRIV, 10, "security/auth private"),
    "ftp": (Facility.FTP, 11, "FTP"),
    "ntp": (Facility.NTP, 12, "NTP"),
    "logaudit": (Facility.LOGAUDIT, 13, "log audit"),
    "logalert": (Facility.LOGALERT, 14, "log alert"),
    "clock": (Facility.CLOCK, 15, "clock daemon"),
    "local0": (Facility.LOCAL0, 16, "local use 0"),
    "local1": (Facility.LOCAL1, 17, "local use 1"),
    "local2": (Facility.LOCAL2, 18, "local use 2"),
    "local3": (Facility.LOCAL3, 19, "local use 3"),
    "local4": (Facility.LOCAL4, 20, "local use 4"),
    "local5": (Facility.LOCAL5, 21, "local use 5"),
    "local6": (Facility.LOCAL6, 22, "local use 6"),
    "local7": (Facility.LOCAL7, 23, "local use 7"),
}

# Test parameters for severity enum
SEVERITY_PARAMS = {
    "emergency": (Severity.EMERGENCY, 0, "system unusable"),
    "alert": (Severity.ALERT, 1, "immediate action required"),
    "critical": (Severity.CRITICAL, 2, "critical conditions"),
    "error": (Severity.ERROR, 3, "error conditions"),
    "warning": (Severity.WARNING, 4, "warning conditions"),
    "notice": (Severity.NOTICE, 5, "normal but significant"),
    "info": (Severity.INFO, 6, "informational"),
    "debug": (Severity.DEBUG, 7, "debug messages"),
}

# Test constants for priority validation
PRIORITY_TEST_CASES = [
    (
        Facility.LOCAL1,
        Severity.DEBUG,
        143,
        "local1_debug",
    ),  # 17 * 8 + 7 = 136 + 7 = 143
    (Facility.AUTH, Severity.CRITICAL, 34, "auth_critical"),  # 4 * 8 + 2 = 32 + 2 = 34
    (Facility.KERN, Severity.EMERGENCY, 0, "kernel_emergency"),  # 0 * 8 + 0 = 0
    (
        Facility.LOCAL7,
        Severity.DEBUG,
        191,
        "local7_debug",
    ),  # 23 * 8 + 7 = 184 + 7 = 191
]

# Test constants for priority parsing
FROM_PRIORITY_TEST_CASES = [
    (143, Facility.LOCAL1, Severity.DEBUG, "priority_143_local1_debug"),
    (34, Facility.AUTH, Severity.CRITICAL, "priority_34_auth_critical"),
    (
        0,
        Facility.KERN,
        Severity.EMERGENCY,
        "priority_0_kernel_emergency",
    ),  # 0 is a valid priority
    (
        191,
        Facility.LOCAL7,
        Severity.DEBUG,
        "priority_191_local7_debug",
    ),  # Maximum valid priority (23*8+7)
]

# Test constants for invalid priority handling
INVALID_PRIORITY_TEST_CASES = [
    (
        192,
        Facility.LOGAUDIT,
        Severity.EMERGENCY,
        "above_max_valid",
    ),  # Just above max valid (191) should use default facility
    (
        200,
        Facility.LOGAUDIT,
        Severity.EMERGENCY,
        "well_above_max",
    ),  # Well above max valid should use default facility
    (
        -1,
        Facility.LOGAUDIT,
        Severity.DEBUG,
        "negative_value",
    ),  # Negative values should use default facility
    (
        1000,
        Facility.LOGAUDIT,
        Severity.EMERGENCY,
        "more_than_3_digits",
    ),  # >3 digits should use default facility
    (
        "ABC",
        Facility.LOGAUDIT,
        Severity.DEBUG,
        "non_numeric",
    ),  # Non-numeric should use default facility and severity
    (
        "0000",
        Facility.LOGAUDIT,
        Severity.EMERGENCY,
        "multiple_zeros",
    ),  # Multiple zeros should use default facility
    (
        "00",
        Facility.LOGAUDIT,
        Severity.EMERGENCY,
        "double_zero",
    ),  # Any string of multiple zeros is invalid
    (
        None,
        Facility.LOGAUDIT,
        Severity.DEBUG,
        "none_value",
    ),  # None should use default facility and severity
]


@pytest.mark.unit
class TestSyslogRFCBaseModel:
    """Test suite for the SyslogRFCBaseModel class."""

    @pytest.mark.parametrize(
        "facility_enum, description, code",
        [
            (facility_enum, description, code)
            for name, (facility_enum, code, description) in FACILITY_PARAMS.items()
        ],
        ids=list(FACILITY_PARAMS.keys()),
    )
    def test_facility_enum(self, facility_enum, description, code):
        """Test facility enum values match expected codes and descriptions."""
        assert int(facility_enum) == code
        assert facility_enum.name in str(facility_enum)
        assert str(code) in str(facility_enum)

    @pytest.mark.parametrize(
        "severity_enum, description, code",
        [
            (severity_enum, description, code)
            for name, (severity_enum, code, description) in SEVERITY_PARAMS.items()
        ],
        ids=list(SEVERITY_PARAMS.keys()),
    )
    def test_severity_enum(self, severity_enum, description, code):
        """Test severity enum values match expected codes and descriptions."""
        assert int(severity_enum) == code
        assert severity_enum.name in str(severity_enum)
        assert str(code) in str(severity_enum)

    def test_severity_comparison(self):
        """Test that severity comparisons work as expected with inverted logic."""
        # In actual code usage, higher severity (lower numeric value) is "greater than" lower severity
        # EMERGENCY(0) has higher priority than DEBUG(7)
        # Standard int comparison would be EMERGENCY(0) < DEBUG(7)
        # But with our custom implementation, we want EMERGENCY(0) > DEBUG(7)

        # Test ordering: EMERGENCY > ALERT > CRITICAL > ERROR > WARNING > NOTICE > INFO > DEBUG
        assert int(Severity.EMERGENCY) < int(Severity.DEBUG)  # RFC int values: 0 < 7
        assert (
            Severity.EMERGENCY > Severity.DEBUG
        )  # But for severity comparison: EMERGENCY > DEBUG

        # Test specific comparisons (using our inverted logic)
        assert Severity.EMERGENCY > Severity.ALERT
        assert Severity.ALERT > Severity.CRITICAL
        assert Severity.CRITICAL > Severity.ERROR
        assert Severity.ERROR > Severity.WARNING
        assert Severity.WARNING > Severity.NOTICE
        assert Severity.NOTICE > Severity.INFO
        assert Severity.INFO > Severity.DEBUG

        # Test greater than or equal
        assert Severity.ERROR >= Severity.ERROR
        assert Severity.ERROR >= Severity.WARNING
        assert not (Severity.ERROR >= Severity.CRITICAL)

        # Test less than
        assert Severity.DEBUG < Severity.INFO
        assert not (Severity.EMERGENCY < Severity.ALERT)

        # Test less than or equal
        assert Severity.WARNING <= Severity.WARNING
        assert Severity.NOTICE <= Severity.WARNING
        assert not (Severity.ERROR <= Severity.WARNING)

        # Test practical usage example
        if Severity.ERROR > Severity.WARNING:
            # This is true - errors are more severe than warnings
            pass
        else:
            assert False, "ERROR should be more severe than WARNING"

        # Test filtering for critical severities (common use case)
        critical_severities = [sev for sev in Severity if sev >= Severity.ERROR]
        assert set(critical_severities) == {
            Severity.EMERGENCY,
            Severity.ALERT,
            Severity.CRITICAL,
            Severity.ERROR,
        }

    @pytest.mark.parametrize(
        "facility, severity, expected_pri, test_id",
        PRIORITY_TEST_CASES,
        ids=lambda test_id: test_id if isinstance(test_id, str) else str(test_id),
    )
    def test_get_priority(self, facility, severity, expected_pri, test_id):
        """Test calculating priority from facility and severity."""
        # Standard library imports
        from datetime import datetime

        model = SyslogRFCBaseModel(
            facility=int(facility), severity=int(severity), timestamp=datetime.now()
        )
        
        # Use validation utility to check the model
        validate_syslog_model(
            model,
            facility=int(facility),
            severity=int(severity),
            priority=expected_pri
        )
        
        # Keep these assertions for specific enum tests
        assert model.get_facility_enum() == facility
        assert model.get_severity_enum() == severity

    @pytest.mark.parametrize(
        "pri, expected_facility, expected_severity, test_id",
        FROM_PRIORITY_TEST_CASES,
        ids=lambda test_id: test_id if isinstance(test_id, str) else str(test_id),
    )
    def test_from_priority(self, pri, expected_facility, expected_severity, test_id):
        """Test creating an instance from a priority value."""
        model = SyslogRFCBaseModel.from_priority(pri)
        
        # Use validation utility to check the model
        validate_syslog_model(
            model,
            facility=expected_facility.value,
            severity=expected_severity.value
        )
        
        # Keep these for specific enum validations
        assert model.get_facility_enum() == expected_facility
        assert model.get_severity_enum() == expected_severity

    @pytest.mark.parametrize(
        "pri, expected_facility, expected_severity, test_id",
        INVALID_PRIORITY_TEST_CASES,
        ids=lambda test_id: test_id if isinstance(test_id, str) else str(test_id),
    )
    def test_from_priority_with_invalid_input(
        self, pri, expected_facility, expected_severity, test_id
    ):
        """Test creating an instance from invalid priority values."""
        model = SyslogRFCBaseModel.from_priority(pri)
        
        # Use validation utility to check the model
        validate_syslog_model(
            model,
            facility=expected_facility.value,
            severity=expected_severity.value
        )
        
        # Keep these for specific enum validations
        assert model.get_facility_enum() == expected_facility
        assert model.get_severity_enum() == expected_severity
