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
Integration tests for GenericLEEF2DecoderPlugin using manual processing.
These tests verify that the LEEF 2.0 decoder plugin works correctly when processing
syslog messages directly without relying on the UnknownSyslogDecoder's plugin chain.
"""
# Third-party imports
import pytest

# Local/package imports
from core_data_processing.decoders.plugins.message.generic.leef2.plugin import (
    GenericLEEF2DecoderPlugin,
)
from core_data_processing.decoders.unknown_syslog_decoder import UnknownSyslogDecoder
from core_data_processing.models.syslog_rfc3164 import SyslogRFC3164Message
from core_data_processing.models.syslog_rfc5424 import SyslogRFC5424Message
from core_data_processing.models.syslog_rfc_base import SyslogRFCBaseModel


@pytest.mark.integration
def test_leef2_with_rfc3164():
    """Test LEEF 2.0 decoder with an RFC3164 message."""
    # Example RFC3164 message with LEEF 2.0 payload
    msg = "<13>May 12 23:20:50 myhost LEEF:2.0|IBM|QRadar|2.0|12345|src=10.0.0.1\tdst=2.1.2.2\tspt=1232"
    decoder = UnknownSyslogDecoder()
    result = decoder.decode(msg)

    # Basic validation of RFC3164 structure
    assert isinstance(result, SyslogRFC3164Message)
    assert result.hostname == "myhost"

    # Manually apply the LEEF 2.0 plugin
    leef_decoder = GenericLEEF2DecoderPlugin()
    success = leef_decoder.decode(result)

    # Verify the result after LEEF 2.0 plugin is applied
    assert success is True
    assert result.structure_classification.vendor == "ibm"
    assert result.structure_classification.product == "qradar"
    assert result.structure_classification.msgclass == "12345"
    assert "src" in result.event_data
    assert result.event_data["src"] == "10.0.0.1"


@pytest.mark.integration
def test_leef2_with_rfc5424():
    """Test LEEF 2.0 decoder with an RFC5424 message."""
    # Example RFC5424 message with LEEF 2.0 payload
    msg = "<34>1 2025-05-12T23:20:50.52Z mymachine app 1234 ID47 - LEEF:2.0|IBM|QRadar|2.0|12345|src=192.168.1.1\tdst=10.0.0.1\tact=blocked"
    decoder = UnknownSyslogDecoder()
    result = decoder.decode(msg)

    # Basic validation of RFC5424 structure
    assert isinstance(result, SyslogRFC5424Message)
    assert result.hostname == "mymachine"
    assert result.app_name == "app"
    assert result.proc_id == "1234"

    # Manually apply the LEEF 2.0 plugin
    leef_decoder = GenericLEEF2DecoderPlugin()
    success = leef_decoder.decode(result)

    # Verify the result after LEEF 2.0 plugin is applied
    assert success is True
    assert result.structure_classification.vendor == "ibm"
    assert result.structure_classification.product == "qradar"
    assert result.structure_classification.msgclass == "12345"
    assert "src" in result.event_data
    assert result.event_data["src"] == "192.168.1.1"
    assert result.event_data["act"] == "blocked"


@pytest.mark.integration
def test_direct_leef2_message():
    """Test with a raw LEEF 2.0 message (direct processing)."""
    # Direct LEEF 2.0 message in a basic syslog format
    msg = "<13>LEEF:2.0|IBM|QRadar|2.0|12345|src=10.0.0.1\tdst=2.1.2.2\trt=May 12 2025 10:30:00"
    decoder = UnknownSyslogDecoder()
    result = decoder.decode(msg)

    # For direct LEEF, it should be treated as a generic syslog message
    assert isinstance(result, SyslogRFCBaseModel)

    # Manually apply the LEEF 2.0 plugin
    leef_decoder = GenericLEEF2DecoderPlugin()
    success = leef_decoder.decode(result)

    # Verify the result after LEEF 2.0 plugin is applied
    assert success is True
    assert result.structure_classification.vendor == "ibm"
    assert result.structure_classification.product == "qradar"
    assert result.structure_classification.msgclass == "12345"
    assert "src" in result.event_data
    assert result.event_data["src"] == "10.0.0.1"
    assert "rt" in result.event_data
    assert result.event_data["rt"] == "May 12 2025 10:30:00"


@pytest.mark.integration
def test_leef2_with_category():
    """Test LEEF 2.0 decoder with event category field."""
    # Example with event category
    msg = "<13>May 12 23:20:50 myhost LEEF:2.0|IBM|QRadar|2.0|12345|SecurityAlert|src=10.0.0.1\tdst=2.1.2.2\tspt=1232"
    decoder = UnknownSyslogDecoder()
    result = decoder.decode(msg)

    # Basic validation of RFC3164 structure
    assert isinstance(result, SyslogRFC3164Message)
    assert result.hostname == "myhost"

    # Manually apply the LEEF 2.0 plugin
    leef_decoder = GenericLEEF2DecoderPlugin()
    success = leef_decoder.decode(result)

    # Verify the result after LEEF 2.0 plugin is applied
    assert success is True
    assert result.structure_classification.vendor == "ibm"
    assert result.structure_classification.product == "qradar"
    # Check that category is incorporated into msgclass (lowercase)
    assert result.structure_classification.msgclass == "securityalert_12345"
    assert "src" in result.event_data
    assert result.event_data["src"] == "10.0.0.1"
    assert "event_category" in result.event_data
    assert result.event_data["event_category"] == "SecurityAlert"


@pytest.mark.integration
def test_leef2_with_custom_labels():
    """Test LEEF 2.0 decoder with custom field labels."""
    # Example with custom field labels (a LEEF 2.0 feature)
    msg = "<13>May 12 23:20:50 myhost LEEF:2.0|IBM|QRadar|2.0|12345|sourceAddress=10.0.0.1\tsourceAddressLabel=SourceIP\tdestAddress=2.1.2.2\tdestAddressLabel=DestIP"
    decoder = UnknownSyslogDecoder()
    result = decoder.decode(msg)

    # Basic validation of RFC3164 structure
    assert isinstance(result, SyslogRFC3164Message)
    assert result.hostname == "myhost"

    # Manually apply the LEEF 2.0 plugin
    leef_decoder = GenericLEEF2DecoderPlugin()
    success = leef_decoder.decode(result)

    # Verify the result after LEEF 2.0 plugin is applied
    assert success is True
    assert result.structure_classification.vendor == "ibm"
    assert result.structure_classification.product == "qradar"
    assert result.structure_classification.msgclass == "12345"
    assert "sourceAddress" in result.event_data
    assert result.event_data["sourceAddress"] == "10.0.0.1"
    assert "destAddress" in result.event_data
    assert result.event_data["destAddress"] == "2.1.2.2"
    # Check that custom labels are also included
    assert "SourceIP" in result.event_data
    assert result.event_data["SourceIP"] == "10.0.0.1"
    assert "DestIP" in result.event_data
    assert result.event_data["DestIP"] == "2.1.2.2"
