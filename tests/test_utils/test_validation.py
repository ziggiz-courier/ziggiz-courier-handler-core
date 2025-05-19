#!/usr/bin/env python
# -*- coding: utf-8 -*-
# # SPDX-License-Identifier: BSL-1.1
# # Copyright (c) 2025 Ziggiz Inc.
# #
# # This file is part of the ziggiz-courier-core-data-processing and is licensed under the
# # Business Source License 1.1. You may not use this file except in
# # compliance with the License. You may obtain a copy of the License at:
# # https://github.com/ziggiz-courier/ziggiz-courier-core-data-processing/blob/main/LICENSE
"""Tests for the Syslog model validation utility."""

# Standard library imports
from datetime import datetime

# Third-party imports
import pytest

# Local/package imports
from ziggiz_courier_handler_core.models.syslog_rfc_base import Facility, Severity
from ziggiz_courier_handler_core.models.syslog_rfc3164 import SyslogRFC3164Message
from ziggiz_courier_handler_core.models.syslog_rfc5424 import SyslogRFC5424Message
from tests.test_utils.validation import InvalidArgumentException, validate_syslog_model


@pytest.mark.unit
class TestSyslogModelValidation:
    """Test suite for the syslog model validation utility."""

    def test_validate_rfc3164_model(self):
        """Test validating a RFC3164 model instance."""
        # Create a test model
        timestamp = datetime.now()
        model = SyslogRFC3164Message(
            facility=13,
            severity=7,
            message="Test message",
            timestamp=timestamp,
            hostname="test-host",
            app_name="test-app",
            proc_id="123",
        )

        # Full validation
        validate_syslog_model(
            model,
            facility=13,
            severity=7,
            message="Test message",
            timestamp=timestamp,
            hostname="test-host",
            app_name="test-app",
            proc_id="123",
            priority=111,  # 13*8 + 7 = 111
        )

        # Partial validation (only some fields)
        validate_syslog_model(model, facility=13, severity=7)
        validate_syslog_model(model, message="Test message")
        validate_syslog_model(model, hostname="test-host", app_name="test-app")
        validate_syslog_model(model, priority=111)

        # Using Facility/Severity enums
        validate_syslog_model(
            model, facility=Facility.LOGAUDIT, severity=Severity.DEBUG
        )

    def test_validate_rfc5424_model(self):
        """Test validating a RFC5424 model instance."""
        # Create a test model
        timestamp = datetime.now()
        structured_data = {"origin": {"ip": "192.168.1.1", "software": "test-app"}}
        
        model = SyslogRFC5424Message(
            facility=13,
            severity=7,
            message="Test message",
            timestamp=timestamp,
            hostname="test-host",
            app_name="test-app",
            proc_id="123",
            msg_id="ID47",
            structured_data=structured_data,
        )

        # Full validation
        validate_syslog_model(
            model,
            facility=13,
            severity=7,
            message="Test message",
            timestamp=timestamp,
            hostname="test-host",
            app_name="test-app",
            proc_id="123",
            msg_id="ID47",
            structured_data=structured_data,
            priority=111,  # 13*8 + 7 = 111
        )

        # Partial validation (only RFC5424 specific fields)
        validate_syslog_model(model, msg_id="ID47")
        validate_syslog_model(model, structured_data=structured_data)

    def test_invalid_arguments(self):
        """Test that an exception is raised when no expected values are provided."""
        model = SyslogRFC3164Message(
            facility=13, severity=7, message="Test message", timestamp=datetime.now()
        )

        with pytest.raises(InvalidArgumentException):
            validate_syslog_model(model)
            
    def test_failed_validation(self):
        """Test that assertions fail when expected values don't match."""
        model = SyslogRFC3164Message(
            facility=13, severity=7, message="Test message", timestamp=datetime.now()
        )

        with pytest.raises(AssertionError):
            validate_syslog_model(model, facility=10)  # Wrong facility

        with pytest.raises(AssertionError):
            validate_syslog_model(model, message="Wrong message")  # Wrong message
            
    def test_validate_with_none_values(self):
        """Test validating fields that are explicitly set to None."""
        # Create a test model with some None values
        timestamp = datetime.now()
        model = SyslogRFC3164Message(
            facility=13,
            severity=7,
            message="Test message",
            timestamp=timestamp,
            # hostname, app_name, and proc_id are None by default
        )

        # Explicitly validate that some fields are None
        validate_syslog_model(
            model,
            facility=13,
            severity=7,
            message="Test message",
            timestamp=timestamp,
            hostname=None,
            app_name=None,
            proc_id=None
        )

        # Create a model with None values for RFC5424 specific fields
        model_5424 = SyslogRFC5424Message(
            facility=13,
            severity=7,
            message="Test message",
            timestamp=timestamp,
            # hostname, app_name, proc_id, msg_id, and structured_data are None by default
        )

        # Validate that RFC5424 specific fields are None
        validate_syslog_model(
            model_5424,
            facility=13,
            severity=7,
            message="Test message",
            msg_id=None,
            structured_data=None
        )
