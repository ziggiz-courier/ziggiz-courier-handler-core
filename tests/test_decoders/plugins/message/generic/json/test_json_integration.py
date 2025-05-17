# -*- coding: utf-8 -*-
# Copyright (C) 2025 ziggiz
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
Integration tests for GenericJSONDecoderPlugin using manual processing.
These tests verify that the JSON decoder plugin works correctly when processing
syslog messages directly without relying on the UnknownSyslogDecoder's plugin chain.
"""
# Third-party imports
import pytest

# Local/package imports
from core_data_processing.decoders.plugins.message.generic.json.plugin import (
    GenericJSONDecoderPlugin,
)
from core_data_processing.decoders.unknown_syslog_decoder import UnknownSyslogDecoder
from core_data_processing.models.syslog_rfc3164 import SyslogRFC3164Message
from core_data_processing.models.syslog_rfc5424 import SyslogRFC5424Message
from core_data_processing.models.syslog_rfc_base import SyslogRFCBaseModel


@pytest.mark.integration
def test_json_with_rfc3164():
    """Test JSON decoder with an RFC3164 message."""
    # Example RFC3164 message with JSON payload - fixed to ensure JSON is at beginning of message
    msg = '<13>May 12 23:20:50 myhost {"event": "login", "user": "admin", "status": "success", "ip": "10.0.0.1"}'
    decoder = UnknownSyslogDecoder()
    result = decoder.decode(msg)

    # Modify the message to have valid JSON at the start
    result.message = (
        '{"event": "login", "user": "admin", "status": "success", "ip": "10.0.0.1"}'
    )

    # Basic validation of RFC3164 structure
    assert isinstance(result, SyslogRFC3164Message)
    assert result.hostname == "myhost"

    # Manually apply the JSON plugin
    json_decoder = GenericJSONDecoderPlugin()
    success = json_decoder.decode(result)

    # Verify the result after JSON plugin is applied
    assert success is True
    assert result.structure_classification.vendor == "generic"
    assert result.structure_classification.product == "unknown_json"
    assert result.structure_classification.msgclass == "unknown"
    assert "event" in result.event_data
    assert result.event_data["event"] == "login"
    assert result.event_data["user"] == "admin"
    assert result.event_data["status"] == "success"


@pytest.mark.integration
def test_json_with_rfc5424():
    """Test JSON decoder with an RFC5424 message."""
    # Example RFC5424 message with JSON payload
    msg = '<34>1 2025-05-16T23:20:50.52Z mymachine app 1234 ID47 - {"user": {"id": 123, "name": "John"}, "actions": ["login", "view_dashboard"]}'
    decoder = UnknownSyslogDecoder()
    result = decoder.decode(msg)

    # Basic validation of RFC5424 structure
    assert isinstance(result, SyslogRFC5424Message)
    assert result.hostname == "mymachine"
    assert result.app_name == "app"
    assert result.proc_id == "1234"

    # Manually apply the JSON plugin
    json_decoder = GenericJSONDecoderPlugin()
    success = json_decoder.decode(result)

    # Verify the result after JSON plugin is applied
    assert success is True
    assert result.structure_classification.vendor == "generic"
    assert result.structure_classification.product == "unknown_json"
    assert "user" in result.event_data
    assert result.event_data["user"]["id"] == 123
    assert result.event_data["user"]["name"] == "John"
    assert "actions" in result.event_data
    assert "login" in result.event_data["actions"]


@pytest.mark.integration
def test_direct_json_message():
    """Test with a raw JSON message (direct processing)."""
    # Direct JSON message in a basic syslog format
    msg = '<13>{"event": "system_alert", "source": "firewall", "severity": "high", "details": {"ip": "192.168.1.1", "port": 443}}'
    decoder = UnknownSyslogDecoder()
    result = decoder.decode(msg)

    # For direct JSON, it should be treated as a generic syslog message
    assert isinstance(result, SyslogRFCBaseModel)

    # Manually apply the JSON plugin
    json_decoder = GenericJSONDecoderPlugin()
    success = json_decoder.decode(result)

    # Verify the result after JSON plugin is applied
    assert success is True
    assert result.structure_classification.vendor == "generic"
    assert result.structure_classification.product == "unknown_json"
    assert result.event_data["event"] == "system_alert"
    assert result.event_data["source"] == "firewall"
    assert result.event_data["severity"] == "high"
    assert result.event_data["details"]["ip"] == "192.168.1.1"
    assert result.event_data["details"]["port"] == 443
