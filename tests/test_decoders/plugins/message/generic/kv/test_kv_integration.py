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
Integration tests for GenericKVDecoderPlugin using manual processing.
These tests verify that the KV decoder plugin works correctly when processing
syslog messages directly without relying on the UnknownSyslogDecoder's plugin chain.
"""
# Standard library imports

# Third-party imports
import pytest

from tests.test_utils.validation import validate_meta_data_product

# Local/package imports
from ziggiz_courier_handler_core.decoders.plugins.message.generic.kv.plugin import (
    GenericKVDecoderPlugin,
)
from ziggiz_courier_handler_core.decoders.unknown_syslog_decoder import (
    UnknownSyslogDecoder,
)
from ziggiz_courier_handler_core.models.syslog_rfc3164 import SyslogRFC3164Message
from ziggiz_courier_handler_core.models.syslog_rfc5424 import SyslogRFC5424Message
from ziggiz_courier_handler_core.models.syslog_rfc_base import SyslogRFCBaseModel


@pytest.mark.integration
def test_kv_with_rfc3164():
    """Test KV decoder with an RFC3164 message."""
    # Example RFC3164 message with KV payload
    msg = (
        "<13>May 12 23:20:50 myhost src=10.0.0.1 dst=8.8.8.8 action=allow service=https"
    )
    decoder = UnknownSyslogDecoder()
    result = decoder.decode(msg)

    # Basic validation of RFC3164 structure
    assert isinstance(result, SyslogRFC3164Message)
    assert result.hostname == "myhost"

    # Manually apply the KV plugin
    kv_decoder = GenericKVDecoderPlugin()
    success = kv_decoder.decode(result)

    # Verify the result after KV plugin is applied
    assert success is True
    key = "GenericKVDecoderPlugin"
    assert result.handler_data is not None
    assert key in result.handler_data
    handler_entry = result.handler_data[key]
    validate_meta_data_product(
        result,
        expected_organization="generic",
        expected_product="unknown_kv",
        handler_key=key,
    )
    assert handler_entry["msgclass"] == "unknown"
    assert result.event_data is not None
    assert "src" in result.event_data
    assert result.event_data["src"] == "10.0.0.1"
    assert "dst" in result.event_data
    assert result.event_data["dst"] == "8.8.8.8"
    assert "action" in result.event_data
    assert result.event_data["action"] == "allow"
    assert "service" in result.event_data
    assert result.event_data["service"] == "https"


@pytest.mark.integration
def test_kv_with_rfc5424():
    """Test KV decoder with an RFC5424 message."""
    # Example RFC5424 message with KV payload
    msg = '<34>1 2025-05-16T23:20:50.52Z mymachine app 1234 ID47 - user="admin" action=login status=success ip=192.168.1.1'
    decoder = UnknownSyslogDecoder()
    result = decoder.decode(msg)

    # Basic validation of RFC5424 structure
    assert isinstance(result, SyslogRFC5424Message)
    assert result.hostname == "mymachine"
    assert result.app_name == "app"
    assert result.proc_id == "1234"

    # Manually apply the KV plugin
    kv_decoder = GenericKVDecoderPlugin()
    success = kv_decoder.decode(result)

    # Verify the result after KV plugin is applied
    assert success is True
    key = "GenericKVDecoderPlugin"
    assert result.handler_data is not None
    assert key in result.handler_data
    validate_meta_data_product(
        result,
        expected_organization="generic",
        expected_product="unknown_kv",
        handler_key=key,
    )
    assert result.event_data is not None
    assert "user" in result.event_data
    assert result.event_data["user"] == "admin"
    assert "action" in result.event_data
    assert result.event_data["action"] == "login"
    assert "status" in result.event_data
    assert result.event_data["status"] == "success"
    assert "ip" in result.event_data
    assert result.event_data["ip"] == "192.168.1.1"


@pytest.mark.integration
def test_direct_kv_message():
    """Test with a raw KV message (direct processing)."""
    # Direct KV message in a basic syslog format
    msg = '<13>src=firewall dst=10.0.0.5 action=block proto=tcp port=22 reason="Invalid authentication"'
    decoder = UnknownSyslogDecoder()
    result = decoder.decode(msg)

    # For direct KV, it should be treated as a generic syslog message
    assert isinstance(result, SyslogRFCBaseModel)

    # Manually apply the KV plugin
    kv_decoder = GenericKVDecoderPlugin()
    success = kv_decoder.decode(result)

    # Verify the result after KV plugin is applied
    assert success is True
    key = "GenericKVDecoderPlugin"
    assert result.handler_data is not None
    assert key in result.handler_data
    validate_meta_data_product(
        result,
        expected_organization="generic",
        expected_product="unknown_kv",
        handler_key=key,
    )
    assert result.event_data is not None
    assert "src" in result.event_data
    assert result.event_data["src"] == "firewall"
    assert "dst" in result.event_data
    assert result.event_data["dst"] == "10.0.0.5"
    assert "action" in result.event_data
    assert result.event_data["action"] == "block"
    assert "proto" in result.event_data
    assert result.event_data["proto"] == "tcp"
    assert "port" in result.event_data
    assert result.event_data["port"] == "22"
    assert "reason" in result.event_data
    assert result.event_data["reason"] == "Invalid authentication"
