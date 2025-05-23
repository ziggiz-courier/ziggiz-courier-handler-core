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
Integration tests for PaloAlto NGFW decoders using manual processing.
These tests verify that the PaloAlto NGFW decoder plugin works correctly when processing
syslog messages directly without relying on the UnknownSyslogDecoder's plugin chain.
"""
# Standard library imports
import random

from datetime import datetime

# Third-party imports
import pytest

from tests.test_utils.validation import validate_meta_data_product

# Local/package imports
from ziggiz_courier_handler_core.decoders.plugins.message.paloalto.ngfw.plugin import (
    PaloAltoNGFWCSVDecoder,
)
from ziggiz_courier_handler_core.decoders.unknown_syslog_decoder import (
    UnknownSyslogDecoder,
)
from ziggiz_courier_handler_core.models.syslog_rfc3164 import SyslogRFC3164Message
from ziggiz_courier_handler_core.models.syslog_rfc5424 import SyslogRFC5424Message
from ziggiz_courier_handler_core.models.syslog_rfc_base import SyslogRFCBaseModel


@pytest.mark.integration
def test_paloalto_traffic_with_rfc3164():
    """Test PaloAlto NGFW TRAFFIC decode with an RFC3164 message."""
    # Generate a timestamp in RFC3164 format
    dt = datetime.now().astimezone()
    date = dt.strftime("%b %d %H:%M:%S")

    # Select a random hostname from options
    host_options = [
        "10.0.0.1",
        "palo-ngfw",
        "paloalto.example.com",
    ]
    host = random.choice(host_options)

    # Create an RFC3164 message with a PaloAlto TRAFFIC payload
    msg = f"<134>{date} {host} 1,2025/05/13 12:34:56,001122334455,TRAFFIC,drop,1,2025/05/13,12:34:56,10.1.1.1,10.2.2.2,0.0.0.0,0.0.0.0,Allow-All,ethernet1/1,ethernet1/2,ethernet1/1,ethernet1/2,Test-Rule,2025/05/13 12:34:56,1,1,0,0,0,0,0x0,udp,deny,0,0,0,0,,paloalto,from-policy"

    # Decode the message using the UnknownSyslogDecoder
    unknown_decoder = UnknownSyslogDecoder()
    result = unknown_decoder.decode(msg)

    # Basic validation of RFC3164 structure
    assert isinstance(result, SyslogRFC3164Message)
    assert result.hostname == host

    # Manually apply the PaloAlto NGFW CSV decoder
    pa_decoder = PaloAltoNGFWCSVDecoder()
    success = pa_decoder.decode(result)

    # Verify the result after PaloAlto plugin is applied
    assert success is True
    key = "PaloAltoNGFWCSVDecoder"
    assert result.handler_data is not None
    assert key in result.handler_data
    handler_entry = result.handler_data[key]
    validate_meta_data_product(
        result,
        expected_organization="paloalto",
        expected_product="ngfw",
        handler_key=key,
    )
    assert handler_entry["msgclass"] == "traffic"
    assert result.event_data is not None
    assert result.event_data["serial_number"] == "001122334455"
    assert result.event_data["type"] == "TRAFFIC"


@pytest.mark.integration
def test_paloalto_threat_with_rfc5424():
    """Test PaloAlto NGFW THREAT decode with an RFC5424 message."""
    # Generate a timestamp in RFC5424 format
    dt = datetime.now().astimezone()
    date = dt.strftime("%Y-%m-%dT%H:%M:%S.%f%z")

    # Create an RFC5424 message with a PaloAlto THREAT payload
    msg = f"<134>1 {date} paloalto-ngfw - - - - 1,2025/05/13 12:34:56,001122334455,THREAT,vulnerability,1,2025/05/13,12:34:56,10.1.1.1,10.2.2.2,0.0.0.0,0.0.0.0,Threat-Rule,user1,user2,web-browsing,vsys1,untrust,trust,ethernet1/1,ethernet1/2,Threat-Log,1234,5678,1,80,443,1,2,0x0,tcp,reset-both,example.com/malicious.php,12345,malware,critical,client-to-server,9876543,0x2"

    # Decode the message using the UnknownSyslogDecoder
    unknown_decoder = UnknownSyslogDecoder()
    result = unknown_decoder.decode(msg)

    # Basic validation of RFC5424 structure
    assert isinstance(result, SyslogRFC5424Message)
    assert result.hostname == "paloalto-ngfw"

    # Manually apply the PaloAlto NGFW CSV decoder
    pa_decoder = PaloAltoNGFWCSVDecoder()
    success = pa_decoder.decode(result)

    # Verify the result after PaloAlto plugin is applied
    assert success is True
    key = "PaloAltoNGFWCSVDecoder"
    assert result.handler_data is not None
    assert key in result.handler_data
    handler_entry = result.handler_data[key]
    validate_meta_data_product(
        result,
        expected_organization="paloalto",
        expected_product="ngfw",
        handler_key=key,
    )
    assert handler_entry["msgclass"] == "threat"
    assert result.event_data is not None
    assert result.event_data["serial_number"] == "001122334455"
    assert result.event_data["type"] == "THREAT"
    assert result.event_data["threat_content_type"] == "vulnerability"
    handler_entry = result.handler_data[key]
    validate_meta_data_product(
        result,
        expected_organization="paloalto",
        expected_product="ngfw",
        handler_key=key,
    )
    assert handler_entry["msgclass"] == "threat"


@pytest.mark.integration
def test_paloalto_system_log_with_rfc3164():
    """Test PaloAlto NGFW SYSTEM decode with an RFC3164 message."""
    # Generate a timestamp in RFC3164 format
    dt = datetime.now().astimezone()
    date = dt.strftime("%b %d %H:%M:%S")

    # Create an RFC3164 message with a PaloAlto SYSTEM payload
    msg = f"<134>{date} paloalto-ngfw 1,2025/05/13 12:34:56,001122334455,SYSTEM,general,0001,2025/05/13,12:34:56,system,1,0,general,info,auth-success,Authentication successful for user admin from 10.1.1.1"

    # Decode the message using the UnknownSyslogDecoder
    unknown_decoder = UnknownSyslogDecoder()
    result = unknown_decoder.decode(msg)

    # Basic validation of RFC3164 structure
    assert isinstance(result, SyslogRFC3164Message)
    assert result.hostname == "paloalto-ngfw"

    # Manually apply the PaloAlto NGFW CSV decoder
    pa_decoder = PaloAltoNGFWCSVDecoder()
    success = pa_decoder.decode(result)

    # Verify the result after PaloAlto plugin is applied
    assert success is True
    key = "PaloAltoNGFWCSVDecoder"
    assert result.handler_data is not None
    assert key in result.handler_data
    handler_entry = result.handler_data[key]
    validate_meta_data_product(
        result,
        expected_organization="paloalto",
        expected_product="ngfw",
        handler_key=key,
    )
    assert handler_entry["msgclass"] == "system"
    assert result.event_data is not None
    assert result.event_data["serial_number"] == "001122334455"
    assert result.event_data["type"] == "SYSTEM"
    assert result.handler_data is not None
    assert key in result.handler_data
    handler_entry = result.handler_data[key]
    validate_meta_data_product(
        result,
        expected_organization="paloalto",
        expected_product="ngfw",
        handler_key=key,
    )
    assert handler_entry["msgclass"] == "system"


@pytest.mark.integration
def test_paloalto_config_log_with_rfc5424():
    """Test PaloAlto NGFW CONFIG decode with an RFC5424 message."""
    # Generate a timestamp in RFC5424 format
    dt = datetime.now().astimezone()
    date = dt.strftime("%Y-%m-%dT%H:%M:%S.%f%z")

    # Create an RFC5424 message with a PaloAlto CONFIG payload
    msg = f"<134>1 {date} paloalto-ngfw - - - - 1,2025/05/13 12:34:56,001122334455,CONFIG,0,0,2025/05/13,12:34:56,admin,10.1.1.1,Web,0,0,set,vsys1,policy,rules,Test-Rule,action,allow"

    # Decode the message using the UnknownSyslogDecoder
    unknown_decoder = UnknownSyslogDecoder()
    result = unknown_decoder.decode(msg)

    # Basic validation of RFC5424 structure
    assert isinstance(result, SyslogRFC5424Message)
    assert result.hostname == "paloalto-ngfw"

    # Manually apply the PaloAlto NGFW CSV decoder
    pa_decoder = PaloAltoNGFWCSVDecoder()
    success = pa_decoder.decode(result)

    # Verify the result after PaloAlto plugin is applied
    assert success is True
    key = "PaloAltoNGFWCSVDecoder"
    assert result.handler_data is not None
    assert key in result.handler_data
    handler_entry = result.handler_data[key]
    validate_meta_data_product(
        result,
        expected_organization="paloalto",
        expected_product="ngfw",
        handler_key=key,
    )
    assert handler_entry["msgclass"] == "config"
    assert result.event_data is not None
    assert result.event_data["serial_number"] == "001122334455"
    assert result.event_data["type"] == "CONFIG"
    assert result.handler_data is not None
    assert key in result.handler_data
    handler_entry = result.handler_data[key]
    validate_meta_data_product(
        result,
        expected_organization="paloalto",
        expected_product="ngfw",
        handler_key=key,
    )
    assert handler_entry["msgclass"] == "config"


@pytest.mark.integration
def test_unknown_syslog_decoder_chain_for_paloalto():
    """Test PaloAlto NGFW decoding using the full UnknownSyslogDecoder plugin chain."""
    # Generate a timestamp in RFC3164 format
    dt = datetime.now().astimezone()
    date = dt.strftime("%b %d %H:%M:%S")

    # Create an RFC3164 message with a PaloAlto TRAFFIC payload
    msg = f"<134>{date} paloalto-ngfw 1,2025/05/13 12:34:56,001122334455,TRAFFIC,drop,1,2025/05/13,12:34:56,10.1.1.1,10.2.2.2,0.0.0.0,0.0.0.0,Allow-All,ethernet1/1,ethernet1/2,ethernet1/1,ethernet1/2,Test-Rule,2025/05/13 12:34:56,1,1,0,0,0,0,0x0,udp,deny,0,0,0,0,,paloalto,from-policy"

    # Use the UnknownSyslogDecoder to automatically detect and process the message
    decoder = UnknownSyslogDecoder()
    result = decoder.decode(msg)

    # The result should already have PaloAlto handler_data from the plugin chain
    assert isinstance(result, SyslogRFCBaseModel)
    key = "PaloAltoNGFWCSVDecoder"
    assert result.handler_data is not None
    assert key in result.handler_data
    handler_entry = result.handler_data[key]
    validate_meta_data_product(
        result,
        expected_organization="paloalto",
        expected_product="ngfw",
        handler_key=key,
    )
    assert handler_entry["msgclass"] == "traffic"
    assert result.event_data is not None
    assert result.event_data.get("type", "").lower() == "traffic"
