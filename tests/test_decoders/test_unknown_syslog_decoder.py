# -*- coding: utf-8 -*-
# SPDX-License-Identifier: BSL-1.1
# Copyright (c) 2025 Ziggiz Inc.
#
# This file is part of the ziggiz-courier-core-data-processing and is licensed under the
# Business Source License 1.1. You may not use this file except in
# compliance with the License. You may obtain a copy of the License at:
# https://github.com/ziggiz-courier/ziggiz-courier-core-data-processing/blob/main/LICENSE
#

"""Unit tests for UnknownSyslogDecoder."""
# Third-party imports
import pytest

from tests.test_utils.validation import validate_syslog_model

# Local/package imports
from ziggiz_courier_handler_core.decoders.unknown_syslog_decoder import (
    UnknownSyslogDecoder,
)
from ziggiz_courier_handler_core.models.event_envelope_base import (
    EventEnvelopeBaseModel,
)
from ziggiz_courier_handler_core.models.syslog_rfc3164 import SyslogRFC3164Message
from ziggiz_courier_handler_core.models.syslog_rfc5424 import SyslogRFC5424Message
from ziggiz_courier_handler_core.models.syslog_rfc_base import SyslogRFCBaseModel


@pytest.mark.unit
class TestUnknownSyslogDecoder:
    """Unit tests for UnknownSyslogDecoder."""

    def test_decode_rfc5424(self):
        # Example RFC5424 message
        msg = '<34>1 2025-05-12T23:20:50.52Z mymachine app 1234 ID47 [exampleSDID@32473 iut="3" eventSource="Application"] BOMAn application event log entry...'
        decoder = UnknownSyslogDecoder()
        result = decoder.decode(msg)
        assert isinstance(result, SyslogRFC5424Message)

        # Use the validation utility instead of separate assertions
        validate_syslog_model(
            result,
            facility=4,  # 34 = 4*8 + 2
            severity=2,
            hostname="mymachine",
            app_name="app",
            proc_id="1234",
            msg_id="ID47",
            message="BOMAn application event log entry...",
            structured_data={
                "exampleSDID@32473": {"iut": "3", "eventSource": "Application"}
            },
        )

    def test_decode_rfc3164(self):
        # Example RFC3164 message
        msg = "<13>May 12 23:20:50 mymachine su: " "This is a BSD syslog message."
        decoder = UnknownSyslogDecoder()
        result = decoder.decode(msg)
        assert isinstance(result, SyslogRFC3164Message)

        # Use the validation utility instead of separate assertions
        validate_syslog_model(
            result,
            facility=1,  # 13 = 1*8 + 5
            severity=5,
            hostname="mymachine",
            app_name="su",
            message="This is a BSD syslog message.",
        )

    def test_decode_rfcbase(self):
        # Example RFCBase message (PRI only)
        msg = "<13>This is a base syslog message."
        decoder = UnknownSyslogDecoder()
        result = decoder.decode(msg)
        assert isinstance(result, SyslogRFCBaseModel)

        # Use the validation utility instead of separate assertions
        validate_syslog_model(
            result,
            facility=1,  # 13 = 1*8 + 5
            severity=5,
            message="This is a base syslog message.",
        )

    def test_decode_unknown(self):
        # Not a syslog message
        msg = "Completely unknown message format."
        decoder = UnknownSyslogDecoder()
        result = decoder.decode(msg)
        assert isinstance(result, EventEnvelopeBaseModel)
        assert result.message == msg
