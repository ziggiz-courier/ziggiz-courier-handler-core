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
Unit tests for FortinetFortiGateKVDecoderPlugin.

These tests verify the plugin's ability to parse and interpret Fortinet FortiGate logs
in key-value format directly, independent of the syslog decoder chain.
"""

# Standard library imports
from datetime import datetime, timezone

# Third-party imports
import pytest

from tests.test_utils.validation import validate_meta_data_product

# Local/package imports
from ziggiz_courier_handler_core.decoders.plugins.message.fortinet.fortigate.plugin import (
    FortinetFortiGateKVDecoderPlugin,
)
from ziggiz_courier_handler_core.models.syslog_rfc3164 import SyslogRFC3164Message
from ziggiz_courier_handler_core.models.syslog_rfc5424 import SyslogRFC5424Message
from ziggiz_courier_handler_core.models.syslog_rfc_base import SyslogRFCBaseModel


@pytest.mark.unit
class TestFortinetFortiGateKVDecoderPlugin:
    """Tests for the FortinetFortiGateKVDecoderPlugin class."""

    def test_traffic_log_decoding(self):
        """Test traffic log type decoding."""
        # Create timestamp
        dt = datetime.now().astimezone()
        date = dt.strftime("%Y-%m-%d")
        time = dt.strftime("%H:%M:%S")
        eventtime_epoch = int(dt.timestamp())

        # Create a model with a traffic message
        message = (
            f"date={date} time={time} devname=fortigate-1 devid=FG800C3912801080 "
            f"eventtime={eventtime_epoch} logid=0004000017 type=traffic subtype=sniffer level=notice vd=root "
            f'srcip=fe80::20c:29ff:fe77:20d4 srcintf="port3" dstip=ff02::1:ff77:20d4 dstintf="port3" sessionid=408903 '
            f'proto=58 action=accept policyid=2 dstcountry="Reserved" srccountry="Reserved" trandisp=snat transip=:: '
            f'transport=0 service="icmp6/131/0" duration=36 sentbyte=0 rcvdbyte=40 sentpkt=0 rcvdpkt=0 appid=16321 '
            f'app="IPv6.ICMP" appcat="Network.Service" apprisk=elevated applist="sniffer-profile" appact=detected '
            f"utmaction=allow countapp=1"
        )
        model = SyslogRFC3164Message(
            timestamp=datetime(2025, 5, 13, 12, 34, 56, tzinfo=timezone.utc),
            facility=14,  # LOG_ALERT
            severity=3,  # LOG_ERR
            message=message,
        )

        # Create the decoder plugin
        decoder = FortinetFortiGateKVDecoderPlugin(parsing_cache={})

        # Decode the message
        result = decoder.decode(model)

        # Check that the message was decoded correctly

        assert result is True
        key = "FortinetFortiGateKVDecoderPlugin"
        assert model.handler_data is not None
        assert key in model.handler_data
        handler_entry = model.handler_data[key]
        # Validate SourceProducer entry
        validate_meta_data_product(
            model,
            expected_organization="fortinet",
            expected_product="fortigate",
            handler_key=key,
        )
        assert handler_entry["msgclass"] == "traffic_sniffer"

        # Verify specific fields
        assert model.event_data is not None
        assert model.event_data["logid"] == "0004000017"
        assert model.event_data["type"] == "traffic"
        assert model.event_data["subtype"] == "sniffer"
        assert model.event_data["action"] == "accept"
        assert model.event_data["utmaction"] == "allow"

    def test_utm_log_decoding(self):
        """Test UTM log type decoding."""
        # Create timestamp
        dt = datetime.now().astimezone()
        date = dt.strftime("%Y-%m-%d")
        time = dt.strftime("%H:%M:%S")
        eventtime_epoch = int(dt.timestamp())

        # Create a model with a UTM message
        message = (
            f"date={date} time={time} devname=fortigate-2 devid=FG200D3915800001 "
            f"eventtime={eventtime_epoch} logid=0419016384 type=utm subtype=webfilter level=warning vd=root "
            f'srcip=192.168.1.100 srcport=52125 srcintf="internal" dstip=93.184.216.34 dstport=443 dstintf="wan1" '
            f'sessionid=12345 proto=6 action=blocked service=HTTPS hostname="example.com" profile="default-profile" '
            f'status=blocked urlcat="Information Technology" reason=blocked category=52 catdesc="Information Technology"'
        )
        model = SyslogRFC5424Message(
            timestamp=datetime(2025, 5, 13, 12, 34, 56, tzinfo=timezone.utc),
            facility=14,
            severity=4,  # WARNING
            message=message,
        )

        # Create the decoder plugin
        decoder = FortinetFortiGateKVDecoderPlugin(parsing_cache={})

        # Decode the message
        result = decoder.decode(model)

        # Check that the message was decoded correctly

        assert result is True
        key = "FortinetFortiGateKVDecoderPlugin"
        assert model.handler_data is not None
        assert key in model.handler_data
        handler_entry = model.handler_data[key]
        # Validate SourceProducer entry
        validate_meta_data_product(
            model,
            expected_organization="fortinet",
            expected_product="fortigate",
            handler_key=key,
        )
        assert handler_entry["msgclass"] == "utm_webfilter"

        # Verify specific fields
        assert model.event_data is not None
        assert model.event_data["logid"] == "0419016384"
        assert model.event_data["type"] == "utm"
        assert model.event_data["subtype"] == "webfilter"
        assert model.event_data["action"] == "blocked"
        assert model.event_data["hostname"] == "example.com"

    def test_event_log_decoding(self):
        """Test event log type decoding."""
        # Create timestamp
        dt = datetime.now().astimezone()
        date = dt.strftime("%Y-%m-%d")
        time = dt.strftime("%H:%M:%S")
        eventtime_epoch = int(dt.timestamp())

        # Create a model with an event message
        message = (
            f"date={date} time={time} devname=fortigate-3 devid=FG100D3G16800000 "
            f"eventtime={eventtime_epoch} logid=0100032003 type=event subtype=system level=information vd=root "
            f'msg="Admin admin logged in from 10.1.1.100"'
        )
        model = SyslogRFCBaseModel(
            timestamp=datetime(2025, 5, 13, 12, 34, 56, tzinfo=timezone.utc),
            facility=14,
            severity=6,  # INFO
            message=message,
        )

        # Create the decoder plugin
        decoder = FortinetFortiGateKVDecoderPlugin(parsing_cache={})

        # Decode the message
        result = decoder.decode(model)

        # Check that the message was decoded correctly
        assert result is True
        key = "FortinetFortiGateKVDecoderPlugin"
        assert model.handler_data is not None
        assert key in model.handler_data
        handler_entry = model.handler_data[key]
        # Validate SourceProducer entry
        validate_meta_data_product(
            model,
            expected_organization="fortinet",
            expected_product="fortigate",
            handler_key=key,
        )
        assert handler_entry["msgclass"] == "event_system"

        # Verify specific fields
        assert model.event_data is not None
        assert model.event_data["logid"] == "0100032003"
        assert model.event_data["type"] == "event"
        assert model.event_data["subtype"] == "system"
        assert model.event_data["msg"] == "Admin admin logged in from 10.1.1.100"

    def test_non_matching_message(self):
        """Test with a message that doesn't match the Fortinet FortiGate format."""
        # Create a model with a non-matching message
        model = SyslogRFC3164Message(
            timestamp="2025-05-13T12:34:56.000Z",
            facility=14,
            severity=3,
            message="This is not a FortiGate key-value message",
        )

        # Create the decoder plugin
        decoder = FortinetFortiGateKVDecoderPlugin()

        # Decode the message
        result = decoder.decode(model)

        # Verify that it wasn't decoded
        assert result is False
        key = "FortinetFortiGateKVDecoderPlugin"
        # handler_data should be None or not contain the key
        assert model.handler_data is None or key not in model.handler_data
        # event_data should be None or empty
        assert not getattr(model, "event_data", None)

    def test_no_message_attribute(self):
        """Test FortinetFortiGateKVDecoderPlugin with a model without a message attribute."""
        # Create a model without a message attribute
        model = SyslogRFC3164Message(
            timestamp="2025-05-13T12:34:56.000Z",
            facility=14,
            severity=3,
            # No message attribute
        )

        # Initialize the decoder with an empty cache
        decoder = FortinetFortiGateKVDecoderPlugin()

        # Call the decode method
        result = decoder.decode(model)

        # Verify the result
        assert result is False
        key = "FortinetFortiGateKVDecoderPlugin"
        assert model.handler_data is None or key not in model.handler_data
        assert not getattr(model, "event_data", None)

    def test_incomplete_fortigate_message(self):
        """Test with a message that looks like FortiGate but missing required fields."""
        # Create a model with a partial FortiGate-like message missing required fields
        model = SyslogRFC3164Message(
            timestamp="2025-05-13T12:34:56.000Z",
            facility=14,
            severity=3,
            message="date=2025-05-13 time=12:34:56 devname=fortigate-1 devid=FG800C3912801080",
        )

        # Create the decoder plugin
        decoder = FortinetFortiGateKVDecoderPlugin()

        # Decode the message
        result = decoder.decode(model)

        # This should return False since it's missing required fields like logid, type, subtype
        assert result is False
        key = "FortinetFortiGateKVDecoderPlugin"
        assert model.handler_data is None or key not in model.handler_data
