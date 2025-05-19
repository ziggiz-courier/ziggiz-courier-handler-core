# -*- coding: utf-8 -*-
# # SPDX-License-Identifier: BSL-1.1
# # Copyright (c) 2025 Ziggiz Inc.
# #
# # This file is part of the ziggiz-courier-core-data-processing and is licensed under the
# # Business Source License 1.1. You may not use this file except in
# # compliance with the License. You may obtain a copy of the License at:
# # https://github.com/ziggiz-courier/ziggiz-courier-core-data-processing/blob/main/LICENSE
"""Tests for the syslog RFC3164 encoder."""

# Standard library imports
from datetime import datetime

# Third-party imports
import pytest

# Local/package imports
from ziggiz_courier_handler_core.encoders.syslog_rfc3164_encoder import (
    SyslogRFC3164Encoder,
)
from ziggiz_courier_handler_core.models.syslog_rfc3164 import SyslogRFC3164Message
from tests.test_utils.validation import validate_syslog_model


@pytest.mark.unit
@pytest.mark.rfc3164
class TestSyslogRFC3164Encoder:
    """Test suite for the SyslogRFC3164Encoder class."""

    def test_encode_syslog_message(self):
        """Test encoding a SyslogRFC3164Message."""
        # Create an encoder
        encoder = SyslogRFC3164Encoder()

        # Create test messages
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
            # Validate the model before encoding
            if syslog_message.facility == 13 and syslog_message.severity == 7:
                validate_syslog_model(
                    syslog_message,
                    facility=13,
                    severity=7,
                    priority=111  # 13 * 8 + 7 = 111
                )
            elif syslog_message.facility == 4 and syslog_message.severity == 2:
                validate_syslog_model(
                    syslog_message,
                    facility=4,
                    severity=2,
                    priority=34  # 4 * 8 + 2 = 34
                )
            
            # Test encoding
            result = encoder.encode(syslog_message)
            assert result == expected_output
