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
Unit tests for the Generic LEEF 2.0 Decoder Plugin.
"""
# Standard library imports
from typing import Dict, Optional

# Third-party imports
import pytest

# Local/package imports
from core_data_processing.decoders.plugins.message.generic.leef_2.plugin import (
    GenericLEEF2DecoderPlugin,
)
from core_data_processing.models.syslog_rfc3164 import SyslogRFC3164Message


@pytest.mark.unit
class TestGenericLEEF2DecoderPlugin:
    """Tests for the GenericLEEF2DecoderPlugin class."""

    def test_basic_leef_2_message(self):
        """Test basic LEEF 2.0 message decoding."""
        # Create a model with a LEEF 2.0 message
        model = SyslogRFC3164Message(
            facility=1,
            severity=1,
            message="LEEF:2.0|IBM|QRadar|2.0|12345|src=10.0.0.1\tdst=2.1.2.2\tspt=1232",
        )

        # Create the decoder plugin
        decoder = GenericLEEF2DecoderPlugin(parsing_cache={})

        # Decode the message
        result = decoder.decode(model)

        # Check that the message was decoded correctly
        assert result is True
        assert model.event_data.get("src") == "10.0.0.1"
        assert model.event_data.get("dst") == "2.1.2.2"
        assert model.event_data.get("spt") == "1232"
        assert model.structure_classification.vendor == "ibm"
        assert model.structure_classification.product == "qradar"
        assert model.structure_classification.msgclass == "12345"

    def test_leef_2_message_with_category(self):
        """Test LEEF 2.0 message with category field decoding."""
        # Create a model with a LEEF 2.0 message that includes a category
        model = SyslogRFC3164Message(
            facility=1,
            severity=1,
            message="LEEF:2.0|IBM|QRadar|2.0|12345|SecurityAlert|src=10.0.0.1\tdst=2.1.2.2\tspt=1232",
        )

        # Create the decoder plugin
        decoder = GenericLEEF2DecoderPlugin(parsing_cache={})

        # Decode the message
        result = decoder.decode(model)

        # Check that the message was decoded correctly with category incorporated into msgclass
        assert result is True
        assert model.event_data.get("src") == "10.0.0.1"
        assert model.event_data.get("dst") == "2.1.2.2"
        assert model.event_data.get("spt") == "1232"
        assert model.event_data.get("event_category") == "SecurityAlert"
        assert model.structure_classification.vendor == "ibm"
        assert model.structure_classification.product == "qradar"
        assert model.structure_classification.msgclass == "securityalert_12345"

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
            "parse_leef2_message": {
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
        assert model.event_data.get("src") == "192.168.1.1"  # From cache
        assert model.event_data.get("dst") == "192.168.1.2"  # From cache
        assert model.structure_classification.vendor == "mockvendor"  # From cache
        assert model.structure_classification.product == "mockproduct"  # From cache
        assert model.structure_classification.msgclass == "mockeventid"  # From cache
