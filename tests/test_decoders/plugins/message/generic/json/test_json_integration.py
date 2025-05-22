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
Integration tests for GenericJSONDecoderPlugin using manual processing.
These tests verify that the JSON decoder plugin works correctly when processing
syslog messages directly without relying on the UnknownSyslogDecoder's plugin chain.
"""
# Third-party imports
import pytest

from tests.test_utils.validation import validate_source_producer

# Local/package imports
from ziggiz_courier_handler_core.decoders.plugins.message.generic.json.plugin import (
    GenericJSONDecoderPlugin,
)
from ziggiz_courier_handler_core.decoders.unknown_syslog_decoder import (
    UnknownSyslogDecoder,
)
from ziggiz_courier_handler_core.models.syslog_rfc3164 import SyslogRFC3164Message
from ziggiz_courier_handler_core.models.syslog_rfc5424 import SyslogRFC5424Message
from ziggiz_courier_handler_core.models.syslog_rfc_base import SyslogRFCBaseModel


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
    plugin_key = "GenericJSONDecoderPlugin"
    assert result.handler_data is not None
    assert plugin_key in result.handler_data
    handler_entry = result.handler_data[plugin_key]
    validate_source_producer(
        result,
        expected_organization="generic",
        expected_product="unknown_json",
        handler_key=plugin_key,
    )
    assert handler_entry["msgclass"] == "unknown"
    assert result.event_data is not None
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
    plugin_key = "GenericJSONDecoderPlugin"
    assert result.handler_data is not None
    assert plugin_key in result.handler_data
    handler_entry = result.handler_data[plugin_key]
    validate_source_producer(
        result,
        expected_organization="generic",
        expected_product="unknown_json",
        handler_key=plugin_key,
    )
    assert handler_entry["msgclass"] == "unknown"
    assert result.event_data is not None
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
    plugin_key = "GenericJSONDecoderPlugin"
    assert result.handler_data is not None
    assert plugin_key in result.handler_data
    handler_entry = result.handler_data[plugin_key]
    validate_source_producer(
        result,
        expected_organization="generic",
        expected_product="unknown_json",
        handler_key=plugin_key,
    )
    assert handler_entry["msgclass"] == "unknown"
    assert result.event_data is not None
    assert result.event_data["event"] == "system_alert"
    assert result.event_data["source"] == "firewall"
    assert result.event_data["severity"] == "high"
    assert result.event_data["details"]["ip"] == "192.168.1.1"
    assert result.event_data["details"]["port"] == 443
