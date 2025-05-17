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
