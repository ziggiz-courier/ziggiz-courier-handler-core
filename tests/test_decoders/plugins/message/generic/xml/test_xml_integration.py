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
Integration tests for GenericXMLDecoderPlugin using manual processing.

These tests verify that the XML decoder plugin works correctly when processing
syslog messages directly without relying on the UnknownSyslogDecoder's plugin chain.
"""
# Third-party imports
import pytest

from tests.test_utils.validation import validate_source_producer

# Local/package imports
from ziggiz_courier_handler_core.decoders.plugins.message.generic.xml.plugin import (
    GenericXMLDecoderPlugin,
)
from ziggiz_courier_handler_core.decoders.unknown_syslog_decoder import (
    UnknownSyslogDecoder,
)
from ziggiz_courier_handler_core.models.syslog_rfc3164 import SyslogRFC3164Message
from ziggiz_courier_handler_core.models.syslog_rfc5424 import SyslogRFC5424Message


@pytest.mark.integration
def test_xml_with_rfc3164():
    """Test XML decoder with an RFC3164 message."""
    # Example RFC3164 message with XML payload
    msg = (
        "<13>May 12 23:20:50 myhost "
        "<event><type>login</type><user>admin</user>"
        "<status>success</status><ip>10.0.0.1</ip></event>"
    )
    decoder = UnknownSyslogDecoder()
    result = decoder.decode(msg)

    # Modify the message to have valid XML at the start
    result.message = (
        "<event><type>login</type><user>admin</user>"
        "<status>success</status><ip>10.0.0.1</ip></event>"
    )

    # Basic validation of RFC3164 structure
    assert isinstance(result, SyslogRFC3164Message)
    assert result.hostname == "myhost"

    # Manually apply the XML plugin
    xml_decoder = GenericXMLDecoderPlugin({})
    assert xml_decoder.decode(result) is True
    # Verify the result after XML plugin is applied
    key = "GenericXMLDecoderPlugin"
    assert result.handler_data is not None
    assert key in result.handler_data
    validate_source_producer(
        result,
        expected_organization="generic",
        expected_product="unknown_xml",
        handler_key=key,
    )
    handler = result.handler_data.get(key)
    assert handler is not None
    assert handler["msgclass"] == "unknown"
    assert result.event_data is not None
    assert "event" in result.event_data
    assert result.event_data["event"]["type"] == "login"
    assert result.event_data["event"]["user"] == "admin"
    assert result.event_data["event"]["status"] == "success"
    assert result.event_data["event"]["ip"] == "10.0.0.1"


@pytest.mark.integration
def test_xml_with_rfc5424():
    """Test XML decoder with an RFC5424 message."""
    # Example RFC5424 message with XML payload
    msg = (
        "<34>1 2025-05-16T23:20:50.52Z mymachine app 1234 ID47 - "
        '<user id="123" role="admin">'
        "<name>John Doe</name><actions><action>login</action>"
        "<action>view_dashboard</action></actions></user>"
    )
    decoder = UnknownSyslogDecoder()
    result = decoder.decode(msg)

    # Basic validation of RFC5424 structure
    assert isinstance(result, SyslogRFC5424Message)
    assert result.hostname == "mymachine"
    assert result.app_name == "app"
    assert result.proc_id == "1234"

    # Manually apply the XML plugin
    xml_decoder = GenericXMLDecoderPlugin({})
    assert xml_decoder.decode(result) is True
    # Verify the result after XML plugin is applied
    key = "GenericXMLDecoderPlugin"
    assert result.handler_data is not None
    assert key in result.handler_data
    validate_source_producer(
        result,
        expected_organization="generic",
        expected_product="unknown_xml",
        handler_key=key,
    )
    assert result.event_data is not None
    assert "user" in result.event_data
    assert result.event_data["user"]["@id"] == "123"
    assert result.event_data["user"]["@role"] == "admin"
    assert result.event_data["user"]["name"] == "John Doe"
    assert "actions" in result.event_data["user"]
    assert "action" in result.event_data["user"]["actions"]


@pytest.mark.integration
def test_xml_with_dtd_integration():
    """Test XML decoder with a message containing DTD."""
    # Example RFC5424 message with XML payload containing DTD
    msg = (
        '<34>1 2025-05-16T23:20:50.52Z mymachine security 1234 ID47 - <?xml version="1.0"?>\n'
        '<!DOCTYPE security_alert SYSTEM "alert.dtd">\n'
        '<security_alert severity="high">\n'
        "  <source>firewall</source>\n"
        "  <target>192.168.1.1</target>\n"
        "  <description>Unauthorized access attempt</description>\n"
        "</security_alert>"
    )
    decoder = UnknownSyslogDecoder()
    result = decoder.decode(msg)

    # Set the message correctly
    result.message = (
        '<?xml version="1.0"?>\n'
        '<!DOCTYPE security_alert SYSTEM "alert.dtd">\n'
        '<security_alert severity="high">\n'
        "  <source>firewall</source>\n"
        "  <target>192.168.1.1</target>\n"
        "  <description>Unauthorized access attempt</description>\n"
        "</security_alert>"
    )

    # Manually apply the XML plugin
    xml_decoder = GenericXMLDecoderPlugin({})
    assert xml_decoder.decode(result) is True
    # Verify the result after XML plugin is applied
    assert result.handler_data is not None
    key = "GenericXMLDecoderPlugin"
    handler = result.handler_data.get(key)
    assert handler is not None
    validate_source_producer(
        result,
        expected_organization="generic",
        expected_product="unknown_xml",
        handler_key=key,
    )
    assert handler["msgclass"] == "security_alert"
    assert result.event_data is not None
    event_data = result.event_data
    assert "security_alert" in event_data
    sec_alert = event_data["security_alert"]
    assert sec_alert is not None
    assert sec_alert["@severity"] == "high"
    assert sec_alert["source"] == "firewall"
    assert sec_alert["target"] == "192.168.1.1"
    assert sec_alert["description"] == "Unauthorized access attempt"


@pytest.mark.integration
def test_deep_xml_structure():
    """Test XML decoder with a deeply nested XML structure."""
    # Example RFC3164 message with deeply nested XML
    msg = """<13>May 12 23:20:50 myhost <system>
  <network>
    <interface name="eth0">
      <status>up</status>
      <metrics>
        <throughput unit="mbps">100</throughput>
        <errors>
          <rx>0</rx>
          <tx>2</tx>
        </errors>
      </metrics>
    </interface>
  </network>
</system>"""
    decoder = UnknownSyslogDecoder()
    result = decoder.decode(msg)

    # Set the message correctly
    result.message = """<system>
  <network>
    <interface name="eth0">
      <status>up</status>
      <metrics>
        <throughput unit="mbps">100</throughput>
        <errors>
          <rx>0</rx>
          <tx>2</tx>
        </errors>
      </metrics>
    </interface>
  </network>
</system>"""

    # Manually apply the XML plugin
    xml_decoder = GenericXMLDecoderPlugin({})
    assert xml_decoder.decode(result) is True

    assert result.event_data is not None
    event_data = result.event_data
    assert "system" in event_data
    system = event_data["system"]
    assert system is not None
    assert "network" in system
    network = system["network"]
    assert network is not None
    assert "interface" in network
    interface = network["interface"]
    assert interface is not None
    assert interface["@name"] == "eth0"
    assert interface["status"] == "up"
    assert "metrics" in interface
    metrics = interface["metrics"]
    assert metrics is not None
    assert "throughput" in metrics
    throughput = metrics["throughput"]
    assert throughput is not None
    assert throughput["#text"] == "100"
    assert throughput["@unit"] == "mbps"
    assert "errors" in metrics
    errors = metrics["errors"]
    assert errors is not None
    assert errors["rx"] == "0"
    assert errors["tx"] == "2"
