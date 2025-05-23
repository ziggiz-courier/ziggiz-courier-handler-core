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
Integration tests for Fortinet FortiGate decoders using manual processing.
These tests verify that the Fortinet FortiGate decoder plugin works correctly when processing
syslog messages directly without relying on the UnknownSyslogDecoder's plugin chain.
"""
# Standard library imports
import random

from datetime import datetime

# Third-party imports
import pytest

from tests.test_utils.validation import validate_meta_data_product

# Local/package imports
from ziggiz_courier_handler_core.decoders.plugins.message.fortinet.fortigate.plugin import (
    FortinetFortiGateKVDecoderPlugin,
)
from ziggiz_courier_handler_core.decoders.unknown_syslog_decoder import (
    UnknownSyslogDecoder,
)
from ziggiz_courier_handler_core.models.syslog_rfc3164 import SyslogRFC3164Message
from ziggiz_courier_handler_core.models.syslog_rfc5424 import SyslogRFC5424Message
from ziggiz_courier_handler_core.models.syslog_rfc_base import SyslogRFCBaseModel


@pytest.mark.integration
def test_fortigate_traffic_with_rfc3164():
    """Test Fortinet FortiGate traffic log decode with an RFC3164 message."""
    # Generate a timestamp
    dt = datetime.now().astimezone()
    date = dt.strftime("%Y-%m-%d")
    time = dt.strftime("%H:%M:%S")
    eventtime_epoch = int(dt.timestamp())

    # Select a random hostname from options
    host_options = [
        "192.168.1.1",
        "fortigate-fw",
        "fortigate.example.com",
    ]
    host = random.choice(host_options)

    # Create an RFC3164 message with a FortiGate traffic payload
    msg = (
        f"<111>{dt.strftime('%b %d %H:%M:%S')} {host} date={date} time={time} "
        f"devname=fortigate-1 devid=FG800C3912801080 eventtime={eventtime_epoch} "
        f"logid=0004000017 type=traffic subtype=sniffer level=notice vd=root "
        f'srcip=fe80::20c:29ff:fe77:20d4 srcintf="port3" dstip=ff02::1:ff77:20d4 dstintf="port3" '
        f'sessionid=408903 proto=58 action=accept policyid=2 dstcountry="Reserved" srccountry="Reserved" '
        f'trandisp=snat transip=:: transport=0 service="icmp6/131/0" duration=36 sentbyte=0 rcvdbyte=40 '
        f'sentpkt=0 rcvdpkt=0 appid=16321 app="IPv6.ICMP" appcat="Network.Service" apprisk=elevated '
        f'applist="sniffer-profile" appact=detected utmaction=allow countapp=1'
    )

    # Decode the message using the UnknownSyslogDecoder
    unknown_decoder = UnknownSyslogDecoder()
    result = unknown_decoder.decode(msg)

    # Basic validation of RFC3164 structure
    assert isinstance(result, SyslogRFC3164Message)
    assert result.hostname == host

    # Manually apply the FortiGate KV decoder
    fortigate_decoder = FortinetFortiGateKVDecoderPlugin()
    success = fortigate_decoder.decode(result)

    # Verify the result after FortiGate plugin is applied
    assert success is True
    key = "FortinetFortiGateKVDecoderPlugin"
    assert result.handler_data is not None
    assert key in result.handler_data
    handler_entry = result.handler_data[key]

    # Validate SourceProducer using the utility function
    validate_meta_data_product(
        result,
        expected_organization="fortinet",
        expected_product="fortigate",
        handler_key=key,
    )

    assert handler_entry["msgclass"] == "traffic_sniffer"
    assert result.event_data is not None
    assert result.event_data["type"] == "traffic"
    assert result.event_data["subtype"] == "sniffer"
    assert result.event_data["action"] == "accept"
    assert result.event_data["utmaction"] == "allow"


@pytest.mark.integration
def test_fortigate_utm_with_rfc5424():
    """Test Fortinet FortiGate UTM log decode with an RFC5424 message."""
    # Generate a timestamp
    dt = datetime.now().astimezone()
    date = dt.strftime("%Y-%m-%d")
    time = dt.strftime("%H:%M:%S")
    eventtime_epoch = int(dt.timestamp())

    # Create an RFC5424 message with a FortiGate UTM payload
    msg = (
        f"<110>1 {dt.strftime('%Y-%m-%dT%H:%M:%S.%f%z')} fortigate-2 - - - - "
        f"date={date} time={time} devname=fortigate-2 devid=FG200D3915800001 "
        f"eventtime={eventtime_epoch} logid=0419016384 type=utm subtype=webfilter level=warning vd=root "
        f'srcip=192.168.1.100 srcport=52125 srcintf="internal" dstip=93.184.216.34 dstport=443 dstintf="wan1" '
        f'sessionid=12345 proto=6 action=blocked service=HTTPS hostname="example.com" profile="default-profile" '
        f'status=blocked urlcat="Information Technology" reason=blocked category=52 catdesc="Information Technology"'
    )

    # Decode the message using the UnknownSyslogDecoder
    unknown_decoder = UnknownSyslogDecoder()
    result = unknown_decoder.decode(msg)

    # Basic validation of RFC5424 structure
    assert isinstance(result, SyslogRFC5424Message)
    assert result.hostname == "fortigate-2"

    # Manually apply the FortiGate KV decoder
    fortigate_decoder = FortinetFortiGateKVDecoderPlugin()
    success = fortigate_decoder.decode(result)

    # Verify the result after FortiGate plugin is applied
    assert success is True
    key = "FortinetFortiGateKVDecoderPlugin"
    assert result.handler_data is not None
    assert key in result.handler_data
    handler_entry = result.handler_data[key]

    # Validate SourceProducer using the utility function
    validate_meta_data_product(
        result,
        expected_organization="fortinet",
        expected_product="fortigate",
        handler_key=key,
    )

    assert handler_entry["msgclass"] == "utm_webfilter"
    assert result.event_data is not None
    assert result.event_data["type"] == "utm"
    assert result.event_data["subtype"] == "webfilter"
    assert result.event_data["action"] == "blocked"
    assert result.event_data["hostname"] == "example.com"


@pytest.mark.integration
def test_fortigate_event_log():
    """Test Fortinet FortiGate event log decode with a raw message."""
    # Generate a timestamp
    dt = datetime.now().astimezone()
    date = dt.strftime("%Y-%m-%d")
    time = dt.strftime("%H:%M:%S")
    eventtime_epoch = int(dt.timestamp())

    # Create a basic syslog message with a FortiGate event payload
    msg = (
        f"<14>date={date} time={time} devname=fortigate-3 devid=FG100D3G16800000 "
        f"eventtime={eventtime_epoch} logid=0100032003 type=event subtype=system level=information vd=root "
        f'msg="Admin admin logged in from 10.1.1.100"'
    )

    # Decode the message using the UnknownSyslogDecoder
    unknown_decoder = UnknownSyslogDecoder()
    result = unknown_decoder.decode(msg)

    # Verify the message was processed as a basic syslog message
    assert isinstance(result, SyslogRFCBaseModel)

    # Manually apply the FortiGate KV decoder
    fortigate_decoder = FortinetFortiGateKVDecoderPlugin()
    success = fortigate_decoder.decode(result)

    # Verify the result after FortiGate plugin is applied
    assert success is True
    key = "FortinetFortiGateKVDecoderPlugin"
    assert result.handler_data is not None
    assert key in result.handler_data
    handler_entry = result.handler_data[key]

    # Validate SourceProducer using the utility function
    validate_meta_data_product(
        result,
        expected_organization="fortinet",
        expected_product="fortigate",
        handler_key=key,
    )

    assert handler_entry["msgclass"] == "event_system"
    assert result.event_data is not None
    assert result.event_data["type"] == "event"
    assert result.event_data["subtype"] == "system"
    assert result.event_data["msg"] == "Admin admin logged in from 10.1.1.100"


@pytest.mark.integration
def test_unknown_syslog_decoder_and_plugin_for_fortigate():
    """Test Fortinet FortiGate decoding using decode and explicit plugin."""
    # Generate a timestamp
    dt = datetime.now().astimezone()
    date = dt.strftime("%Y-%m-%d")
    time = dt.strftime("%H:%M:%S")
    eventtime_epoch = int(dt.timestamp())

    # Create a syslog message with a FortiGate payload
    msg = (
        f"<111>{dt.strftime('%b %d %H:%M:%S')} fortigate-fw date={date} time={time} "
        f"devname=fortigate-1 devid=FG800C3912801080 eventtime={eventtime_epoch} "
        f"logid=0004000017 type=traffic subtype=sniffer level=notice vd=root "
        f'srcip=fe80::20c:29ff:fe77:20d4 srcintf="port3" dstip=ff02::1:ff77:20d4 dstintf="port3" '
        f"sessionid=408903 proto=58 action=accept policyid=2 utmaction=allow"
    )

    # Use the UnknownSyslogDecoder to decode the message
    decoder = UnknownSyslogDecoder()
    result = decoder.decode(msg)

    # Verify the message was processed as a syslog message
    assert isinstance(result, SyslogRFCBaseModel)

    # Apply the FortiGate KV decoder explicitly
    fortigate_decoder = FortinetFortiGateKVDecoderPlugin()
    success = fortigate_decoder.decode(result)
    key = "FortinetFortiGateKVDecoderPlugin"
    assert result.handler_data is not None
    assert key in result.handler_data
    handler_entry = result.handler_data[key]

    # Validate SourceProducer using the utility function
    validate_meta_data_product(
        result,
        expected_organization="fortinet",
        expected_product="fortigate",
        handler_key=key,
    )

    assert handler_entry["msgclass"] == "traffic_sniffer"
    assert result.event_data is not None
    assert result.event_data["type"] == "traffic"
    assert result.event_data["subtype"] == "sniffer"
    assert result.event_data["action"] == "accept"
    assert result.event_data["utmaction"] == "allow"

    # Verify the result after FortiGate plugin is applied
    assert success is True
    # Already checked handler_data and event_data above
