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
Unit tests for the Generic LEEF 2.0 Decoder Plugin.
"""
# Standard library imports
from typing import Dict, Optional

# Third-party imports
import pytest

from tests.test_utils.validation import validate_source_producer

# Local/package imports
from ziggiz_courier_handler_core.decoders.plugins.message.generic.leef2.plugin import (
    GenericLEEF2DecoderPlugin,
)
from ziggiz_courier_handler_core.models.syslog_rfc3164 import SyslogRFC3164Message


@pytest.mark.unit
class TestGenericLEEF2DecoderPlugin:
    """Tests for the GenericLEEF2DecoderPlugin class."""

    def test_basic_leef_2_message(self):
        """Test basic LEEF 2.0 message decoding."""
        delim = "\t"
        message = (
            "LEEF:2.0|IBM|QRadar|2.0|12345|Alert|"
            + delim
            + "|"
            + "src=10.0.0.1"
            + delim
            + "dst=2.1.2.2"
            + delim
            + "spt=1232"
        )
        model = SyslogRFC3164Message(
            facility=1,
            severity=1,
            message=message,
        )

        decoder = GenericLEEF2DecoderPlugin(parsing_cache={})
        result = decoder.decode(model)
        assert result is True
        assert model.event_data is not None
        assert model.event_data.get("src") == "10.0.0.1"
        assert model.event_data.get("dst") == "2.1.2.2"
        assert model.event_data.get("spt") == "1232"
        key = "GenericLEEF2DecoderPlugin"
        assert model.handler_data is not None
        assert key in model.handler_data
        handler_info = model.handler_data[key]
        validate_source_producer(
            model,
            expected_organization="ibm",
            expected_product="qradar",
            handler_key=key,
        )
        assert handler_info["msgclass"] == "12345"

    def test_leef_2_message_with_category(self):
        """Test LEEF 2.0 message with category field decoding."""
        delim = "\t"
        message = (
            "LEEF:2.0|IBM|QRadar|2.0|12345|SecurityAlert|"
            + delim
            + "|"
            + "src=10.0.0.1"
            + delim
            + "dst=2.1.2.2"
            + delim
            + "spt=1232"
        )
        model = SyslogRFC3164Message(
            facility=1,
            severity=1,
            message=message,
        )

        decoder = GenericLEEF2DecoderPlugin(parsing_cache={})
        result = decoder.decode(model)
        assert result is True
        assert model.event_data is not None
        assert model.event_data.get("src") == "10.0.0.1"
        assert model.event_data.get("dst") == "2.1.2.2"
        assert model.event_data.get("spt") == "1232"
        assert model.event_data.get("event_category") == "SecurityAlert"
        key = "GenericLEEF2DecoderPlugin"
        assert model.handler_data is not None
        assert key in model.handler_data
        handler_info = model.handler_data[key]
        validate_source_producer(
            model,
            expected_organization="ibm",
            expected_product="qradar",
            handler_key=key,
        )
        assert handler_info["msgclass"] == "securityalert_12345"

    def test_non_leef_2_message(self):
        """Test that non-LEEF 2.0 messages are not decoded."""
        # Create a model with a non-LEEF message
        model = SyslogRFC3164Message(
            facility=1, severity=1, message="This is not a LEEF message"
        )

        # Create the decoder plugin
        decoder = GenericLEEF2DecoderPlugin(parsing_cache={})

        # Decode the message
        result = decoder.decode(model)

        # Check that the message was not decoded
        assert result is False
        assert not hasattr(model, "event_data") or not model.event_data

    def test_leef_1_message_not_decoded(self):
        """Test that LEEF 1.0 messages are not decoded by the LEEF 2.0 decoder."""
        # Create a model with a LEEF 1.0 message
        model = SyslogRFC3164Message(
            facility=1,
            severity=1,
            message="LEEF:1.0|IBM|QRadar|1.0|12345|src=10.0.0.1\tdst=2.1.2.2\tspt=1232",
        )

        # Create the decoder plugin
        decoder = GenericLEEF2DecoderPlugin(parsing_cache={})

        # Decode the message
        result = decoder.decode(model)

        # Check that the LEEF 1.0 message was not decoded by the LEEF 2.0 decoder
        assert result is False

    def test_caching_mechanism(self):
        """Test that the caching mechanism works correctly."""
        # Create a model with a LEEF 2.0 message
        model = SyslogRFC3164Message(
            facility=1,
            severity=1,
            message="LEEF:2.0|IBM|QRadar|2.0|12345|src=10.0.0.1\tdst=2.1.2.2\tspt=1232",
        )

        # Create a mock cache that simulates a previous parsing result
        mock_cache: Dict[str, Optional[Dict[str, str]]] = {
            "leef2_parser": {
                "leef_version": "2.0",
                "vendor": "MockVendor",
                "product": "MockProduct",
                "version": "2.0",
                "event_id": "MockEventID",
                "src": "192.168.1.1",
                "dst": "192.168.1.2",
                "spt": "8080",
            }
        }

        # Create the decoder plugin with the mock cache
        decoder = GenericLEEF2DecoderPlugin(parsing_cache=mock_cache)

        # Decode the message
        result = decoder.decode(model)

        # Check that the cached values were used (not the actual message content)
        assert result is True
        assert model.event_data is not None
        assert model.event_data.get("src") == "192.168.1.1"  # From cache
        assert model.event_data.get("dst") == "192.168.1.2"  # From cache
        key = "GenericLEEF2DecoderPlugin"
        assert model.handler_data is not None
        assert key in model.handler_data
        handler_info = model.handler_data[key]
        validate_source_producer(
            model,
            expected_organization="mockvendor",  # From cache
            expected_product="mockproduct",  # From cache
            handler_key=key,
        )
        assert handler_info["msgclass"] == "mockeventid"  # From cache
