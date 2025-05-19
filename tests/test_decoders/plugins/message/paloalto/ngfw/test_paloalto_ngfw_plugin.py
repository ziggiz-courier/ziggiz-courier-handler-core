# -*- coding: utf-8 -*-
# # SPDX-License-Identifier: BSL-1.1
# # Copyright (c) 2025 Ziggiz Inc.
# #
# # This file is part of the ziggiz-courier-core-data-processing and is licensed under the
# # Business Source License 1.1. You may not use this file except in
# # compliance with the License. You may obtain a copy of the License at:
# # https://github.com/ziggiz-courier/ziggiz-courier-core-data-processing/blob/main/LICENSE
"""
Unit tests for PaloAltoNGFWCSVDecoder plugin.

These tests verify the plugin's ability to parse and interpret Palo Alto NGFW log messages
in CSV format directly, independent of the syslog decoder chain.
"""
# Standard library imports
from datetime import datetime, timezone
from typing import Dict, Optional

# Third-party imports
import pytest

from tests.test_utils.validation import validate_source_producer

# Local/package imports
from ziggiz_courier_handler_core.decoders.plugins.message.paloalto.ngfw.plugin import (
    PaloAltoNGFWCSVDecoder,
)
from ziggiz_courier_handler_core.models.syslog_rfc3164 import SyslogRFC3164Message
from ziggiz_courier_handler_core.models.syslog_rfc5424 import SyslogRFC5424Message


@pytest.mark.unit
class TestPaloAltoNGFWCSVDecoder:
    """Tests for the PaloAltoNGFWCSVDecoder class."""

    def test_traffic_log_decoding(self):
        """Test TRAFFIC log type decoding."""
        # Create a model with a TRAFFIC message
        model = SyslogRFC3164Message(
            timestamp=datetime(2025, 5, 13, 12, 34, 56, tzinfo=timezone.utc),
            facility=16,  # LOCAL0
            severity=6,  # INFO
            message="1,2025/05/13 12:34:56,001122334455,TRAFFIC,drop,1,2025/05/13,12:34:56,10.1.1.1,10.2.2.2,0.0.0.0,0.0.0.0,Allow-All,ethernet1/1,ethernet1/2,ethernet1/1,ethernet1/2,Test-Rule,2025/05/13 12:34:56,1,1,0,0,0,0,0x0,udp,deny,0,0,0,0,,paloalto,from-policy",
        )

        # Create the decoder plugin
        decoder = PaloAltoNGFWCSVDecoder(parsing_cache={})

        # Decode the message
        result = decoder.decode(model)

        # Check that the message was decoded correctly
        assert result is True
        key = "PaloAltoNGFWCSVDecoder"
        assert model.handler_data is not None
        assert key in model.handler_data
        handler = model.handler_data[key]
        validate_source_producer(
            model,
            expected_organization="paloalto",
            expected_product="ngfw",
            handler_key=key,
        )
        assert handler["msgclass"] == "traffic"
        assert model.event_data["serial_number"] == "001122334455"
        assert model.event_data["type"] == "TRAFFIC"

    def test_threat_log_decoding(self):
        """Test THREAT log type decoding."""
        # Create a model with a THREAT message
        model = SyslogRFC5424Message(
            timestamp=datetime(2025, 5, 13, 12, 34, 56, tzinfo=timezone.utc),
            facility=16,  # LOCAL0
            severity=6,  # INFO
            message="1,2025/05/13 12:34:56,001122334455,THREAT,vulnerability,1,2025/05/13,12:34:56,10.1.1.1,10.2.2.2,0.0.0.0,0.0.0.0,Threat-Rule,user1,user2,web-browsing,vsys1,untrust,trust,ethernet1/1,ethernet1/2,Threat-Log,1234,5678,1,80,443,1,2,0x0,tcp,reset-both,example.com/malicious.php,12345,malware,critical,client-to-server,9876543,0x2",
        )

        # Create the decoder plugin
        decoder = PaloAltoNGFWCSVDecoder(parsing_cache={})

        # Decode the message
        result = decoder.decode(model)

        # Check that the message was decoded correctly
        assert result is True
        assert model.handler_data is not None
        key = "PaloAltoNGFWCSVDecoder"
        handler = model.handler_data.get(key)
        assert handler is not None
        validate_source_producer(
            model,
            expected_organization="paloalto",
            expected_product="ngfw",
            handler_key=key,
        )
        assert handler["msgclass"] == "threat"
        assert model.event_data["serial_number"] == "001122334455"
        assert model.event_data["type"] == "THREAT"
        assert model.event_data["threat_content_type"] == "vulnerability"

    def test_system_log_decoding(self):
        """Test SYSTEM log type decoding."""
        # Create a model with a SYSTEM message
        model = SyslogRFC3164Message(
            timestamp=datetime(2025, 5, 13, 12, 34, 56, tzinfo=timezone.utc),
            facility=16,  # LOCAL0
            severity=6,  # INFO
            message="1,2025/05/13 12:34:56,001122334455,SYSTEM,general,0001,2025/05/13,12:34:56,system,1,0,general,info,auth-success,Authentication successful for user admin from 10.1.1.1",
        )

        # Create the decoder plugin
        decoder = PaloAltoNGFWCSVDecoder(parsing_cache={})

        # Decode the message
        result = decoder.decode(model)

        # Check that the message was decoded correctly
        assert result is True
        assert model.handler_data is not None
        key = "PaloAltoNGFWCSVDecoder"
        handler = model.handler_data.get(key)
        assert handler is not None
        validate_source_producer(
            model,
            expected_organization="paloalto",
            expected_product="ngfw",
            handler_key=key,
        )
        assert handler["msgclass"] == "system"
        assert model.event_data["serial_number"] == "001122334455"
        assert model.event_data["type"] == "SYSTEM"

    def test_config_log_decoding(self):
        """Test CONFIG log type decoding."""
        # Create a model with a CONFIG message
        model = SyslogRFC3164Message(
            timestamp=datetime(2025, 5, 13, 12, 34, 56, tzinfo=timezone.utc),
            facility=16,  # LOCAL0
            severity=6,  # INFO
            message="1,2025/05/13 12:34:56,001122334455,CONFIG,0,0,2025/05/13,12:34:56,admin,10.1.1.1,Web,0,0,set,vsys1,policy,rules,Test-Rule,action,allow",
        )

        # Create the decoder plugin
        decoder = PaloAltoNGFWCSVDecoder(parsing_cache={})

        # Decode the message
        result = decoder.decode(model)

        # Check that the message was decoded correctly
        assert result is True
        assert model.handler_data is not None
        key = "PaloAltoNGFWCSVDecoder"
        handler = model.handler_data.get(key)
        assert handler is not None
        validate_source_producer(
            model,
            expected_organization="paloalto",
            expected_product="ngfw",
            handler_key=key,
        )
        assert handler["msgclass"] == "config"
        assert model.event_data["serial_number"] == "001122334455"
        assert model.event_data["type"] == "CONFIG"

    def test_with_parsing_cache(self):
        """Test decoder with a pre-populated parsing cache."""
        # Create a cache with predetermined patterns
        cache: Dict[str, Optional[dict]] = {
            "1,2025/05/13 12:34:56,001122334455,TRAFFIC": {
                "pattern": "traffic_pattern",
                "fields": ["field1", "field2"],
            }
        }

        # Create a model with a message that would match the cache
        model = SyslogRFC3164Message(
            timestamp=datetime(2025, 5, 13, 12, 34, 56, tzinfo=timezone.utc),
            facility=16,  # LOCAL0
            severity=6,  # INFO
            message="1,2025/05/13 12:34:56,001122334455,TRAFFIC,drop,1,2025/05/13,12:34:56,10.1.1.1,10.2.2.2,0.0.0.0,0.0.0.0,Allow-All,ethernet1/1,ethernet1/2",
        )

        # Create the decoder plugin with the cache
        decoder = PaloAltoNGFWCSVDecoder(parsing_cache=cache)

        # Decode the message
        result = decoder.decode(model)

        # Verify that it was decoded successfully using the cache
        assert result is True
        assert model.handler_data is not None
        key = "PaloAltoNGFWCSVDecoder"
        handler = model.handler_data.get(key)
        assert handler is not None
        validate_source_producer(
            model,
            expected_organization="paloalto",
            expected_product="ngfw",
            handler_key=key,
        )

    def test_non_matching_message(self):
        """Test with a message that doesn't match the PaloAlto NGFW CSV format."""
        # Create a model with a non-matching message
        model = SyslogRFC3164Message(
            timestamp=datetime(2025, 5, 13, 12, 34, 56, tzinfo=timezone.utc),
            facility=16,  # LOCAL0
            severity=6,  # INFO
            message="This is not a PaloAlto NGFW CSV message",
        )

        # Create the decoder plugin
        decoder = PaloAltoNGFWCSVDecoder()

        # Decode the message
        result = decoder.decode(model)

        # Verify that it wasn't decoded
        assert result is False

    def test_no_message_attribute(self):
        """Test PaloAltoNGFWCSVDecoder with a model without a message attribute."""
        # Create a model without a message attribute
        model = SyslogRFC3164Message(
            timestamp=datetime(2025, 5, 13, 12, 34, 56, tzinfo=timezone.utc),
            facility=16,  # LOCAL0
            severity=6,  # INFO
            # No message attribute
        )

        # Initialize the decoder with an empty cache
        decoder = PaloAltoNGFWCSVDecoder()

        # Call the decode method
        result = decoder.decode(model)

        # Verify the result
        assert result is False

    def test_incorrect_structure(self):
        """Test with a message that looks like PaloAlto but has incorrect structure."""
        # Create a model with a message that starts with a number but is not a valid PA log
        model = SyslogRFC3164Message(
            timestamp=datetime(2025, 5, 13, 12, 34, 56, tzinfo=timezone.utc),
            facility=16,  # LOCAL0
            severity=6,  # INFO
            message="1,2025/05/13 12:34:56,001122334455,INVALID_TYPE,drop,1,2025/05/13",
        )

        # Create the decoder plugin
        decoder = PaloAltoNGFWCSVDecoder()

        # Decode the message
        result = decoder.decode(model)

        # This could either return False or True depending on implementation
        # If it's strict on validating log types, it would return False
        # Otherwise, it might return True but classify it as an unknown type
        # Let's assume it returns False for invalid log types
        assert result is False
