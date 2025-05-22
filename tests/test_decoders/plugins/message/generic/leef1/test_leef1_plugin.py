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
Unit tests for the Generic LEEF 1.0 Decoder Plugin.
"""
# Standard library imports
from typing import Dict, Optional

# Third-party imports
import pytest

from tests.test_utils.validation import validate_source_producer

# Local/package imports
from ziggiz_courier_handler_core.decoders.plugins.message.generic.leef1.plugin import (
    GenericLEEFDecoderPlugin,
)
from ziggiz_courier_handler_core.models.syslog_rfc3164 import SyslogRFC3164Message


@pytest.mark.unit
class TestGenericLEEFDecoderPlugin:
    """Tests for the GenericLEEFDecoderPlugin class."""

    def test_basic_leef_message(self):
        """Test basic LEEF 1.0 message decoding."""
        # Create a model with a LEEF 1.0 message
        model = SyslogRFC3164Message(
            facility=1,
            severity=1,
            message="LEEF:1.0|IBM|QRadar|1.0|12345|src=10.0.0.1\tdst=2.1.2.2\tspt=1232",
        )

        # Create the decoder plugin
        decoder = GenericLEEFDecoderPlugin(parsing_cache={})

        # Decode the message
        result = decoder.decode(model)

        # Check that the message was decoded correctly
        assert result is True
        assert model.event_data is not None
        assert model.event_data.get("src") == "10.0.0.1"
        assert model.event_data.get("dst") == "2.1.2.2"
        assert model.event_data.get("spt") == "1232"
        key = "GenericLEEFDecoderPlugin"
        assert model.handler_data is not None
        assert key in model.handler_data
        handler_entry = model.handler_data[key]
        validate_source_producer(
            model,
            expected_organization="ibm",
            expected_product="qradar",
            handler_key=key,
        )
        assert handler_entry["msgclass"] == "12345"

    def test_leef_message_with_space_delimiter(self):
        """Test LEEF 1.0 message with space-delimited extension fields."""
        # Create a model with a LEEF message using spaces as delimiters
        model = SyslogRFC3164Message(
            facility=1,
            severity=1,
            message="LEEF:1.0|IBM|QRadar|1.0|12345|src=10.0.0.1 dst=2.1.2.2 spt=1232",
        )

        # Create the decoder plugin
        decoder = GenericLEEFDecoderPlugin(parsing_cache={})

        # Decode the message
        result = decoder.decode(model)

        # Check that the message was decoded correctly
        assert result is True
        assert model.event_data is not None
        assert model.event_data.get("src") == "10.0.0.1"
        assert model.event_data.get("dst") == "2.1.2.2"
        assert model.event_data.get("spt") == "1232"
        key = "GenericLEEFDecoderPlugin"
        assert model.handler_data is not None
        assert key in model.handler_data
        handler_entry = model.handler_data[key]
        validate_source_producer(
            model,
            expected_organization="ibm",
            expected_product="qradar",
            handler_key=key,
        )
        assert handler_entry["msgclass"] == "12345"

    def test_leef_message_with_pipes_in_content(self):
        """Test LEEF message with pipe characters in the content."""
        # Create a model with a LEEF message containing escaped pipes
        model = SyslogRFC3164Message(
            facility=1,
            severity=1,
            message="LEEF:1.0|IBM|QRadar|1.0|12345|src=10.0.0.1\tcommand=cat /var/log/messages \\| grep error",
        )

        # Create the decoder plugin
        decoder = GenericLEEFDecoderPlugin(parsing_cache={})

        # Decode the message
        result = decoder.decode(model)

        # Check that the message was decoded correctly
        assert result is True
        assert model.event_data is not None
        assert model.event_data.get("src") == "10.0.0.1"
        assert model.event_data.get("command") == "cat /var/log/messages | grep error"
        key = "GenericLEEFDecoderPlugin"
        assert model.handler_data is not None
        assert key in model.handler_data
        handler_entry = model.handler_data[key]
        validate_source_producer(
            model,
            expected_organization="ibm",
            expected_product="qradar",
            handler_key=key,
        )
        assert handler_entry["msgclass"] == "12345"

    def test_leef_message_with_escapes(self):
        """Test LEEF message with escaped characters in extension fields."""
        # Create a model with a LEEF message containing escaped characters
        model = SyslogRFC3164Message(
            facility=1,
            severity=1,
            message="LEEF:1.0|IBM|QRadar|1.0|12345|src=10.0.0.1\tmessage=Multiple\\=value\\thas\\=escapes",
        )

        # Create the decoder plugin
        decoder = GenericLEEFDecoderPlugin(parsing_cache={})

        # Decode the message
        result = decoder.decode(model)

        # Check that the message was decoded correctly
        assert result is True
        assert model.event_data is not None
        assert model.event_data.get("src") == "10.0.0.1"
        assert model.event_data.get("message") == "Multiple=value\thas=escapes"
        key = "GenericLEEFDecoderPlugin"
        assert model.handler_data is not None
        assert key in model.handler_data
        handler_entry = model.handler_data[key]
        validate_source_producer(
            model,
            expected_organization="ibm",
            expected_product="qradar",
            handler_key=key,
        )
        assert handler_entry["msgclass"] == "12345"

    def test_non_leef_message(self):
        """Test that non-LEEF messages are not decoded."""
        # Create a model with a non-LEEF message
        model = SyslogRFC3164Message(
            facility=1, severity=1, message="This is not a LEEF message"
        )

        # Create the decoder plugin
        decoder = GenericLEEFDecoderPlugin(parsing_cache={})

        # Decode the message
        result = decoder.decode(model)

        # Check that the message was not decoded
        assert result is False
        key = "GenericLEEFDecoderPlugin"
        assert model.handler_data is None or key not in model.handler_data
        assert not getattr(model, "event_data", None)

    def test_leef_2_message_not_decoded(self):
        """Test that LEEF 2.0 messages are not decoded by the LEEF 1.0 decoder."""
        # Create a model with a LEEF 2.0 message
        model = SyslogRFC3164Message(
            facility=1,
            severity=1,
            message="LEEF:2.0|IBM|QRadar|2.0|12345|src=10.0.0.1\tdst=2.1.2.2\tspt=1232",
        )

        # Create the decoder plugin
        decoder = GenericLEEFDecoderPlugin(parsing_cache={})

        # Decode the message
        result = decoder.decode(model)

        # Check that the LEEF 2.0 message was not decoded by the LEEF 1.0 decoder
        assert result is False

    def test_caching_mechanism(self):
        """Test that the caching mechanism works correctly."""
        # Create a model with a LEEF 1.0 message
        model = SyslogRFC3164Message(
            facility=1,
            severity=1,
            message="LEEF:1.0|IBM|QRadar|1.0|12345|src=10.0.0.1\tdst=2.1.2.2\tspt=1232",
        )

        # Create a mock cache that simulates a previous parsing result
        mock_cache: Dict[str, Optional[Dict[str, str]]] = {
            "parse_leef1_message": {
                "leef_version": "1.0",
                "vendor": "MockVendor",
                "product": "MockProduct",
                "version": "1.0",
                "event_id": "MockEventID",
                "src": "192.168.1.1",
                "dst": "192.168.1.2",
                "spt": "8080",
            }
        }

        # Create the decoder plugin with the mock cache
        decoder = GenericLEEFDecoderPlugin(parsing_cache=mock_cache)

        # Decode the message
        result = decoder.decode(model)

        # Check that the cached values were used (not the actual message content)
        assert result is True
        assert model.event_data is not None
        assert model.event_data.get("src") == "192.168.1.1"  # From cache
        assert model.event_data.get("dst") == "192.168.1.2"  # From cache
        assert model.event_data.get("spt") == "8080"  # From cache
        key = "GenericLEEFDecoderPlugin"
        assert model.handler_data is not None
        assert key in model.handler_data
        handler_entry = model.handler_data[key]
        validate_source_producer(
            model,
            expected_organization="mockvendor",
            expected_product="mockproduct",
            handler_key=key,
        )
        assert handler_entry["msgclass"] == "mockeventid"
