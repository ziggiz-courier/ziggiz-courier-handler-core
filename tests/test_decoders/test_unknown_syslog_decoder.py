# -*- coding: utf-8 -*-
# # SPDX-License-Identifier: BSL-1.1
# # Copyright (c) 2025 Ziggiz Inc.
# #
# # This file is part of the ziggiz-courier-core-data-processing and is licensed under the
# # Business Source License 1.1. You may not use this file except in
# # compliance with the License. You may obtain a copy of the License at:
# # https://github.com/ziggiz-courier/ziggiz-courier-core-data-processing/blob/main/LICENSE
"""Unit tests for UnknownSyslogDecoder."""
# Third-party imports
import pytest

# Local/package imports
from core_data_processing.decoders.unknown_syslog_decoder import UnknownSyslogDecoder
from core_data_processing.models.event_envelope_base import EventEnvelopeBaseModel
from core_data_processing.models.syslog_rfc3164 import SyslogRFC3164Message
from core_data_processing.models.syslog_rfc5424 import SyslogRFC5424Message
from core_data_processing.models.syslog_rfc_base import SyslogRFCBaseModel


@pytest.mark.unit
def test_decode_rfc5424():
    # Example RFC5424 message
    msg = '<34>1 2025-05-12T23:20:50.52Z mymachine app 1234 ID47 [exampleSDID@32473 iut="3" eventSource="Application"] BOMAn application event log entry...'
    decoder = UnknownSyslogDecoder()
    result = decoder.decode(msg)
    assert isinstance(result, SyslogRFC5424Message)
    assert result.hostname == "mymachine"
    assert result.app_name == "app"
    assert result.proc_id == "1234"
    assert result.msg_id == "ID47"
    assert result.message.endswith("BOMAn application event log entry...")


@pytest.mark.unit
def test_decode_rfc3164():
    # Example RFC3164 message
    msg = "<13>May 12 23:20:50 mymachine su: " "This is a BSD syslog message."
    decoder = UnknownSyslogDecoder()
    result = decoder.decode(msg)
    assert isinstance(result, SyslogRFC3164Message)
    assert result.hostname == "mymachine"
    assert result.message.endswith("This is a BSD syslog message.")


@pytest.mark.unit
def test_decode_rfcbase():
    # Example RFCBase message (PRI only)
    msg = "<13>This is a base syslog message."
    decoder = UnknownSyslogDecoder()
    result = decoder.decode(msg)
    assert isinstance(result, SyslogRFCBaseModel)
    assert result.message.endswith("This is a base syslog message.")


@pytest.mark.unit
def test_decode_unknown():
    # Not a syslog message
    msg = "Completely unknown message format."
    decoder = UnknownSyslogDecoder()
    result = decoder.decode(msg)
    assert isinstance(result, EventEnvelopeBaseModel)
    assert result.message == msg
