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
Integration tests for GenericCEFDecoderPlugin using manual processing.
These tests verify that the CEF decoder plugin works correctly when processing
syslog messages directly without relying on the UnknownSyslogDecoder's plugin chain.
"""
# Third-party imports
import pytest

from tests.test_utils.validation import validate_meta_data_product

# Local/package imports
from ziggiz_courier_handler_core.decoders.plugins.message.generic.cef.plugin import (
    GenericCEFDecoderPlugin,
)
from ziggiz_courier_handler_core.decoders.unknown_syslog_decoder import (
    UnknownSyslogDecoder,
)
from ziggiz_courier_handler_core.models.syslog_rfc3164 import SyslogRFC3164Message
from ziggiz_courier_handler_core.models.syslog_rfc5424 import SyslogRFC5424Message
from ziggiz_courier_handler_core.models.syslog_rfc_base import SyslogRFCBaseModel


@pytest.mark.integration
def test_cef_with_rfc3164():
    """Test CEF decoder with an RFC3164 message."""
    # Example RFC3164 message with CEF payload
    msg = "<13>May 12 23:20:50 myhost CEF:1|Vendor|Product|1.0|100|Security Alert|10|src=10.0.0.1 dst=2.1.2.2"
    decoder = UnknownSyslogDecoder()
    result = decoder.decode(msg)

    # Basic validation of RFC3164 structure
    assert isinstance(result, SyslogRFC3164Message)
    assert result.hostname == "myhost"

    # Manually apply the CEF plugin
    cef_decoder = GenericCEFDecoderPlugin()
    success = cef_decoder.decode(result)

    # Verify the result after CEF plugin is applied

    assert success is True
    key = "GenericCEFDecoderPlugin"
    assert result.handler_data is not None
    assert key in result.handler_data
    handler_entry = result.handler_data[key]
    validate_meta_data_product(
        result,
        expected_organization="vendor",
        expected_product="product",
        handler_key=key,
    )
    assert handler_entry["msgclass"] == "security alert"
    assert result.event_data is not None
    assert result.event_data is not None
    assert "src" in result.event_data
    assert result.event_data["src"] == "10.0.0.1"


@pytest.mark.integration
def test_cef_with_rfc5424():
    """Test CEF decoder with an RFC5424 message."""
    # Example RFC5424 message with CEF payload
    msg = "<34>1 2025-05-12T23:20:50.52Z mymachine app 1234 ID47 - CEF:1|Security|Product|1.0|100|Intrusion Detected|10|src=192.168.1.1 dst=10.0.0.1 act=blocked"
    decoder = UnknownSyslogDecoder()
    result = decoder.decode(msg)

    # Basic validation of RFC5424 structure
    assert isinstance(result, SyslogRFC5424Message)
    assert result.hostname == "mymachine"
    assert result.app_name == "app"
    assert result.proc_id == "1234"

    # Manually apply the CEF plugin
    cef_decoder = GenericCEFDecoderPlugin()
    success = cef_decoder.decode(result)

    # Verify the result after CEF plugin is applied

    assert success is True
    key = "GenericCEFDecoderPlugin"
    assert result.handler_data is not None
    assert key in result.handler_data
    handler_entry = result.handler_data[key]
    validate_meta_data_product(
        result,
        expected_organization="security",
        expected_product="product",
        handler_key=key,
    )
    assert handler_entry["msgclass"] == "intrusion detected"
    assert result.event_data is not None
    assert result.event_data is not None
    assert "src" in result.event_data
    assert result.event_data["src"] == "192.168.1.1"
    assert result.event_data["act"] == "blocked"


@pytest.mark.integration
def test_direct_cef_message():
    """Test with a raw CEF message (direct processing)."""
    # Direct CEF message in a basic syslog format
    msg = "<13>CEF:1|Vendor|Product|1.0|100|System Alert|10|src=10.0.0.1 dst=2.1.2.2 rt=May 12 2025 10:30:00"
    decoder = UnknownSyslogDecoder()
    result = decoder.decode(msg)

    # For direct CEF, it should be treated as a generic syslog message
    assert isinstance(result, SyslogRFCBaseModel)

    # Manually apply the CEF plugin
    cef_decoder = GenericCEFDecoderPlugin()
    success = cef_decoder.decode(result)

    # Verify the result after CEF plugin is applied

    assert success is True
    key = "GenericCEFDecoderPlugin"
    assert result.handler_data is not None
    assert key in result.handler_data
    handler_entry = result.handler_data[key]
    validate_meta_data_product(
        result,
        expected_organization="vendor",
        expected_product="product",
        handler_key=key,
    )
    assert handler_entry["msgclass"] == "system alert"
    assert result.event_data is not None
    assert result.event_data is not None
    assert "src" in result.event_data
    assert result.event_data["src"] == "10.0.0.1"
    assert "rt" in result.event_data
    assert result.event_data["rt"] == "May 12 2025 10:30:00"
