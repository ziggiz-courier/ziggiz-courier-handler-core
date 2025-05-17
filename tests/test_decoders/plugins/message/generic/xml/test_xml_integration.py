# -*- coding: utf-8 -*-
# # SPDX-License-Identifier: BSL-1.1
# # Copyright (c) 2025 Ziggiz Inc.
# #
# # This file is part of the ziggiz-courier-core-data-processing and is licensed under the
# # Business Source License 1.1. You may not use this file except in
# # compliance with the License. You may obtain a copy of the License at:
# # https://github.com/ziggiz-courier/ziggiz-courier-core-data-processing/blob/main/LICENSE
"""
Integration tests for GenericXMLDecoderPlugin using manual processing.
These tests verify that the XML decoder plugin works correctly when processing
syslog messages directly without relying on the UnknownSyslogDecoder's plugin chain.
"""
# Third-party imports
import pytest

# Local/package imports
from core_data_processing.decoders.plugins.message.generic.xml.plugin import (
    GenericXMLDecoderPlugin,
)
from core_data_processing.decoders.unknown_syslog_decoder import UnknownSyslogDecoder
from core_data_processing.models.syslog_rfc3164 import SyslogRFC3164Message
from core_data_processing.models.syslog_rfc5424 import SyslogRFC5424Message


@pytest.mark.integration
def test_xml_with_rfc3164():
    """Test XML decoder with an RFC3164 message."""
    # Example RFC3164 message with XML payload
    msg = "<13>May 12 23:20:50 myhost <event><type>login</type><user>admin</user><status>success</status><ip>10.0.0.1</ip></event>"
    decoder = UnknownSyslogDecoder()
    result = decoder.decode(msg)

    # Modify the message to have valid XML at the start
    result.message = "<event><type>login</type><user>admin</user><status>success</status><ip>10.0.0.1</ip></event>"

    # Basic validation of RFC3164 structure
    assert isinstance(result, SyslogRFC3164Message)
    assert result.hostname == "myhost"

    # Manually apply the XML plugin
    xml_decoder = GenericXMLDecoderPlugin({})
    success = xml_decoder.decode(result)

    # Verify the result after XML plugin is applied
    assert success is True
    assert result.structure_classification.vendor == "generic"
    assert result.structure_classification.product == "unknown_xml"
    assert result.structure_classification.msgclass == "unknown"
    assert "event" in result.event_data
    assert result.event_data["event"]["type"] == "login"
    assert result.event_data["event"]["user"] == "admin"
    assert result.event_data["event"]["status"] == "success"
    assert result.event_data["event"]["ip"] == "10.0.0.1"


@pytest.mark.integration
def test_xml_with_rfc5424():
    """Test XML decoder with an RFC5424 message."""
    # Example RFC5424 message with XML payload
    msg = '<34>1 2025-05-16T23:20:50.52Z mymachine app 1234 ID47 - <user id="123" role="admin"><name>John Doe</name><actions><action>login</action><action>view_dashboard</action></actions></user>'
    decoder = UnknownSyslogDecoder()
    result = decoder.decode(msg)

    # Basic validation of RFC5424 structure
    assert isinstance(result, SyslogRFC5424Message)
    assert result.hostname == "mymachine"
    assert result.app_name == "app"
    assert result.proc_id == "1234"

    # Manually apply the XML plugin
    xml_decoder = GenericXMLDecoderPlugin({})
    success = xml_decoder.decode(result)

    # Verify the result after XML plugin is applied
    assert success is True
    assert result.structure_classification.vendor == "generic"
    assert result.structure_classification.product == "unknown_xml"
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
    msg = """<34>1 2025-05-16T23:20:50.52Z mymachine security 1234 ID47 - <?xml version="1.0"?>
<!DOCTYPE security_alert SYSTEM "alert.dtd">
<security_alert severity="high">
  <source>firewall</source>
  <target>192.168.1.1</target>
  <description>Unauthorized access attempt</description>
</security_alert>"""
    decoder = UnknownSyslogDecoder()
    result = decoder.decode(msg)

    # Set the message correctly
    result.message = """<?xml version="1.0"?>
<!DOCTYPE security_alert SYSTEM "alert.dtd">
<security_alert severity="high">
  <source>firewall</source>
  <target>192.168.1.1</target>
  <description>Unauthorized access attempt</description>
</security_alert>"""

    # Manually apply the XML plugin
    xml_decoder = GenericXMLDecoderPlugin({})
    success = xml_decoder.decode(result)

    # Verify the result after XML plugin is applied
    assert success is True
    assert result.structure_classification.vendor == "generic"
    assert result.structure_classification.product == "unknown_xml"
    assert result.structure_classification.msgclass == "security_alert"
    assert "security_alert" in result.event_data
    assert result.event_data["security_alert"]["@severity"] == "high"
    assert result.event_data["security_alert"]["source"] == "firewall"
    assert result.event_data["security_alert"]["target"] == "192.168.1.1"
    assert (
        result.event_data["security_alert"]["description"]
        == "Unauthorized access attempt"
    )


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
    success = xml_decoder.decode(result)

    # Verify the result after XML plugin is applied
    assert success is True
    assert result.structure_classification.vendor == "generic"
    assert result.structure_classification.product == "unknown_xml"
    assert "system" in result.event_data
    assert "network" in result.event_data["system"]
    assert "interface" in result.event_data["system"]["network"]
    assert result.event_data["system"]["network"]["interface"]["@name"] == "eth0"
    assert result.event_data["system"]["network"]["interface"]["status"] == "up"
    assert "metrics" in result.event_data["system"]["network"]["interface"]
    assert (
        "throughput" in result.event_data["system"]["network"]["interface"]["metrics"]
    )
    assert (
        result.event_data["system"]["network"]["interface"]["metrics"]["throughput"][
            "#text"
        ]
        == "100"
    )
    assert (
        result.event_data["system"]["network"]["interface"]["metrics"]["throughput"][
            "@unit"
        ]
        == "mbps"
    )
    assert "errors" in result.event_data["system"]["network"]["interface"]["metrics"]
    assert (
        result.event_data["system"]["network"]["interface"]["metrics"]["errors"]["rx"]
        == "0"
    )
    assert (
        result.event_data["system"]["network"]["interface"]["metrics"]["errors"]["tx"]
        == "2"
    )
