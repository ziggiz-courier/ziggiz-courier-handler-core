# -*- coding: utf-8 -*-
# SPDX-License-Identifier: BSL-1.1
# Copyright (c) 2025 Ziggiz Inc.
#
# This file is part of the ziggiz-courier-core-data-processing and is licensed under the
# Business Source License 1.1. You may not use this file except in
# compliance with the License. You may obtain a copy of the License at:
# https://github.com/ziggiz-courier/ziggiz-courier-core-data-processing/blob/main/LICENSE
#
"""
Integration tests for GenericLEEF2DecoderPlugin using manual processing.
These tests verify that the LEEF 2.0 decoder plugin works correctly when processing
syslog messages directly without relying on the UnknownSyslogDecoder's plugin chain.
"""
# Third-party imports
import pytest

from tests.test_utils.validation import validate_meta_data_product

# Local/package imports
from ziggiz_courier_handler_core.decoders.plugins.message.generic.leef2.plugin import (
    GenericLEEF2DecoderPlugin,
)
from ziggiz_courier_handler_core.decoders.unknown_syslog_decoder import (
    UnknownSyslogDecoder,
)
from ziggiz_courier_handler_core.models.syslog_rfc3164 import SyslogRFC3164Message
from ziggiz_courier_handler_core.models.syslog_rfc5424 import SyslogRFC5424Message
from ziggiz_courier_handler_core.models.syslog_rfc_base import SyslogRFCBaseModel


@pytest.mark.integration
def test_leef2_with_rfc3164():
    """Test LEEF 2.0 decoder with an RFC3164 message."""
    # Example RFC3164 message with LEEF 2.0 payload
    delim = "\t"
    msg = (
        f"<13>May 12 23:20:50 myhost LEEF:2.0|IBM|QRadar|2.0|12345|Alert|{delim}|"
        f"src=10.0.0.1{delim}dst=2.1.2.2{delim}spt=1232"
    )
    decoder = UnknownSyslogDecoder()
    result = decoder.decode(msg)

    # Basic validation of RFC3164 structure
    assert isinstance(result, SyslogRFC3164Message)
    assert result.hostname == "myhost"

    # Manually apply the LEEF 2.0 plugin
    leef_decoder = GenericLEEF2DecoderPlugin()
    success = leef_decoder.decode(result)

    # Verify the result after LEEF 2.0 plugin is applied
    assert success is True
    key = "GenericLEEF2DecoderPlugin"
    assert result.handler_data is not None
    assert key in result.handler_data
    handler_info = result.handler_data[key]
    validate_meta_data_product(
        result, expected_organization="ibm", expected_product="qradar", handler_key=key
    )
    assert handler_info["msgclass"] == "12345"
    assert result.event_data is not None
    assert "src" in result.event_data
    assert result.event_data["src"] == "10.0.0.1"


@pytest.mark.integration
def test_leef2_with_rfc5424():
    """Test LEEF 2.0 decoder with an RFC5424 message."""
    # Example RFC5424 message with LEEF 2.0 payload
    delim = "\t"
    msg = (
        f"<34>1 2025-05-12T23:20:50.52Z mymachine app 1234 ID47 - LEEF:2.0|IBM|QRadar|2.0|12345|Alert|{delim}|"
        f"src=192.168.1.1{delim}dst=10.0.0.1{delim}act=blocked"
    )
    decoder = UnknownSyslogDecoder()
    result = decoder.decode(msg)

    # Basic validation of RFC5424 structure
    assert isinstance(result, SyslogRFC5424Message)
    assert result.hostname == "mymachine"
    assert result.app_name == "app"
    assert result.proc_id == "1234"

    # Manually apply the LEEF 2.0 plugin
    leef_decoder = GenericLEEF2DecoderPlugin()
    success = leef_decoder.decode(result)

    # Verify the result after LEEF 2.0 plugin is applied
    assert success is True
    key = "GenericLEEF2DecoderPlugin"
    assert result.handler_data is not None
    assert key in result.handler_data
    handler_info = result.handler_data[key]
    validate_meta_data_product(
        result, expected_organization="ibm", expected_product="qradar", handler_key=key
    )
    assert handler_info["msgclass"] == "12345"
    assert result.event_data is not None
    assert "src" in result.event_data
    assert result.event_data["src"] == "192.168.1.1"
    assert "act" in result.event_data
    assert result.event_data["act"] == "blocked"


@pytest.mark.integration
def test_direct_leef2_message():
    """Test with a raw LEEF 2.0 message (direct processing)."""
    # Direct LEEF 2.0 message in a basic syslog format
    delim = "\t"
    msg = (
        f"<13>LEEF:2.0|IBM|QRadar|2.0|12345|Alert|{delim}|"
        f"src=10.0.0.1{delim}dst=2.1.2.2{delim}rt=May 12 2025 10:30:00"
    )
    decoder = UnknownSyslogDecoder()
    result = decoder.decode(msg)

    # For direct LEEF, it should be treated as a generic syslog message
    assert isinstance(result, SyslogRFCBaseModel)

    # Manually apply the LEEF 2.0 plugin
    leef_decoder = GenericLEEF2DecoderPlugin()
    success = leef_decoder.decode(result)

    # Verify the result after LEEF 2.0 plugin is applied
    assert success is True
    key = "GenericLEEF2DecoderPlugin"
    assert result.handler_data is not None
    assert key in result.handler_data
    handler_info = result.handler_data[key]
    validate_meta_data_product(
        result, expected_organization="ibm", expected_product="qradar", handler_key=key
    )
    assert handler_info["msgclass"] == "12345"
    assert result.event_data is not None
    assert "src" in result.event_data
    assert result.event_data["src"] == "10.0.0.1"
    assert "rt" in result.event_data
    assert result.event_data["rt"] == "May 12 2025 10:30:00"


@pytest.mark.integration
def test_leef2_with_category():
    """Test LEEF 2.0 decoder with event category field."""
    # Example with event category
    delim = "\t"
    msg = (
        f"<13>May 12 23:20:50 myhost LEEF:2.0|IBM|QRadar|2.0|12345|SecurityAlert|{delim}|"
        f"src=10.0.0.1{delim}dst=2.1.2.2{delim}spt=1232"
    )
    decoder = UnknownSyslogDecoder()
    result = decoder.decode(msg)

    # Basic validation of RFC3164 structure
    assert isinstance(result, SyslogRFC3164Message)
    assert result.hostname == "myhost"

    # Manually apply the LEEF 2.0 plugin
    leef_decoder = GenericLEEF2DecoderPlugin()
    success = leef_decoder.decode(result)

    # Verify the result after LEEF 2.0 plugin is applied
    assert success is True
    key = "GenericLEEF2DecoderPlugin"
    assert result.handler_data is not None
    assert key in result.handler_data
    handler_info = result.handler_data[key]
    validate_meta_data_product(
        result, expected_organization="ibm", expected_product="qradar", handler_key=key
    )
    # Check that category is incorporated into msgclass (lowercase)
    assert handler_info["msgclass"] == "securityalert_12345"
    assert result.event_data is not None
    assert "src" in result.event_data
    assert result.event_data["src"] == "10.0.0.1"
    assert "event_category" in result.event_data
    assert result.event_data["event_category"] == "SecurityAlert"


@pytest.mark.integration
def test_leef2_with_custom_labels():
    """Test LEEF 2.0 decoder with custom field labels."""
    # Example with custom field labels (a LEEF 2.0 feature)
    delim = "\t"
    msg = (
        f"<13>May 12 23:20:50 myhost LEEF:2.0|IBM|QRadar|2.0|12345|Alert|{delim}|"
        f"sourceAddress=10.0.0.1{delim}sourceAddressLabel=SourceIP{delim}destAddress=2.1.2.2{delim}destAddressLabel=DestIP"
    )
    decoder = UnknownSyslogDecoder()
    result = decoder.decode(msg)

    # Basic validation of RFC3164 structure
    assert isinstance(result, SyslogRFC3164Message)
    assert result.hostname == "myhost"

    # Manually apply the LEEF 2.0 plugin
    leef_decoder = GenericLEEF2DecoderPlugin()
    success = leef_decoder.decode(result)

    # Verify the result after LEEF 2.0 plugin is applied
    assert success is True
    key = "GenericLEEF2DecoderPlugin"
    assert result.handler_data is not None
    assert key in result.handler_data
    handler_info = result.handler_data[key]
    validate_meta_data_product(
        result, expected_organization="ibm", expected_product="qradar", handler_key=key
    )
    assert handler_info["msgclass"] == "12345"
    assert result.event_data is not None
    assert "sourceAddress" in result.event_data
    assert result.event_data["sourceAddress"] == "10.0.0.1"
    assert "destAddress" in result.event_data
    assert result.event_data["destAddress"] == "2.1.2.2"
    # Check that custom labels are also included
    assert "SourceIP" in result.event_data
    assert result.event_data["SourceIP"] == "10.0.0.1"
    assert "DestIP" in result.event_data
    assert result.event_data["DestIP"] == "2.1.2.2"
