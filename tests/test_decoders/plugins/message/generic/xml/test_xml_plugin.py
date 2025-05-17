# -*- coding: utf-8 -*-
# # SPDX-License-Identifier: BSL-1.1
# # Copyright (c) 2025 Ziggiz Inc.
# #
# # This file is part of the ziggiz-courier-core-data-processing and is licensed under the
# # Business Source License 1.1. You may not use this file except in
# # compliance with the License. You may obtain a copy of the License at:
# # https://github.com/ziggiz-courier/ziggiz-courier-core-data-processing/blob/main/LICENSE
"""
Unit tests for GenericXMLDecoderPlugin.
"""
# Third-party imports
import pytest

# Local/package imports
from core_data_processing.decoders.plugins.message.generic.xml.plugin import (
    GenericXMLDecoderPlugin,
)
from core_data_processing.models.syslog_rfc_base import SyslogRFCBaseModel


@pytest.mark.unit
def test_generic_xml_basic_case():
    """Test GenericXMLDecoderPlugin with basic XML message format."""
    # Create a model with a test XML message
    msg = "<event><type>login</type><user>admin</user><status>success</status></event>"
    model = SyslogRFCBaseModel(
        timestamp="2025-05-16T12:34:56.000Z",
        facility=16,  # LOCAL0
        severity=6,  # INFO
        message=msg,
    )

    # Initialize the decoder with an empty cache
    decoder = GenericXMLDecoderPlugin({})

    # Call the decode method
    result = decoder.decode(model)

    # Verify the result
    assert result is True
    assert model.structure_classification.vendor == "generic"
    assert model.structure_classification.product == "unknown_xml"
    assert model.structure_classification.msgclass == "unknown"

    # Verify specific fields in the parsed data
    assert "event" in model.event_data
    assert "type" in model.event_data["event"]
    assert model.event_data["event"]["type"] == "login"
    assert model.event_data["event"]["user"] == "admin"
    assert model.event_data["event"]["status"] == "success"


@pytest.mark.unit
def test_generic_xml_with_attributes():
    """Test GenericXMLDecoderPlugin with XML containing attributes."""
    # Create a model with a test XML message with attributes
    msg = '<event id="123"><user role="admin">John Doe</user><action type="login">User Login</action></event>'
    model = SyslogRFCBaseModel(
        timestamp="2025-05-16T12:34:56.000Z",
        facility=16,
        severity=6,
        message=msg,
    )

    # Initialize the decoder with an empty cache
    decoder = GenericXMLDecoderPlugin({})

    # Call the decode method
    result = decoder.decode(model)

    # Verify the result
    assert result is True
    assert "event" in model.event_data
    assert model.event_data["event"]["@id"] == "123"
    assert model.event_data["event"]["user"]["#text"] == "John Doe"
    assert model.event_data["event"]["user"]["@role"] == "admin"
    assert "action" in model.event_data["event"]
    assert model.event_data["event"]["action"]["#text"] == "User Login"
    assert model.event_data["event"]["action"]["@type"] == "login"


@pytest.mark.unit
def test_generic_xml_with_dtd():
    """Test GenericXMLDecoderPlugin with XML containing a DTD declaration."""
    # Create a model with a test XML message containing a DTD
    msg = """<?xml version="1.0"?>
<!DOCTYPE security_event SYSTEM "security.dtd">
<security_event>
    <timestamp>2025-05-16T12:34:56.000Z</timestamp>
    <severity>high</severity>
    <description>Unauthorized access attempt</description>
</security_event>"""
    model = SyslogRFCBaseModel(
        timestamp="2025-05-16T12:34:56.000Z",
        facility=16,
        severity=6,
        message=msg,
    )

    # Initialize the decoder with an empty cache
    decoder = GenericXMLDecoderPlugin({})

    # Call the decode method
    result = decoder.decode(model)

    # Verify the result
    assert result is True
    assert model.structure_classification.vendor == "generic"
    assert model.structure_classification.product == "unknown_xml"
    assert model.structure_classification.msgclass == "security_event"

    # Verify specific fields in the parsed data
    assert "security_event" in model.event_data
    assert model.event_data["security_event"]["severity"] == "high"
    assert (
        model.event_data["security_event"]["description"]
        == "Unauthorized access attempt"
    )


@pytest.mark.unit
def test_generic_xml_with_escaped_entities():
    """Test GenericXMLDecoderPlugin with XML containing escaped entities."""
    # Create a model with a test XML message with escaped entities
    msg = "<event><description>User &lt;admin&gt; logged in with privileges &amp; access rights</description></event>"
    model = SyslogRFCBaseModel(
        timestamp="2025-05-16T12:34:56.000Z",
        facility=16,
        severity=6,
        message=msg,
    )

    # Initialize the decoder with an empty cache
    decoder = GenericXMLDecoderPlugin({})

    # Call the decode method
    result = decoder.decode(model)

    # Verify the result
    assert result is True
    assert "event" in model.event_data
    assert "description" in model.event_data["event"]
    assert (
        model.event_data["event"]["description"]
        == "User <admin> logged in with privileges & access rights"
    )


@pytest.mark.unit
def test_generic_xml_with_incorrect_escaping():
    """Test GenericXMLDecoderPlugin with XML containing incorrectly escaped entities."""
    # Create a model with a test XML message with improperly escaped entities
    msg = "<event><description>User login with email user@example.com & password</description></event>"
    model = SyslogRFCBaseModel(
        timestamp="2025-05-16T12:34:56.000Z",
        facility=16,
        severity=6,
        message=msg,
    )

    # Initialize the decoder with an empty cache
    decoder = GenericXMLDecoderPlugin({})

    # Call the decode method
    result = decoder.decode(model)

    # Verify the result
    assert result is True
    assert "event" in model.event_data
    assert "description" in model.event_data["event"]
    assert (
        model.event_data["event"]["description"]
        == "User login with email user@example.com & password"
    )


@pytest.mark.unit
def test_generic_xml_negative_case():
    """Test GenericXMLDecoderPlugin with non-matching message format."""
    # Create a model with a message that should not match XML format
    msg = "This is not an XML formatted message"
    model = SyslogRFCBaseModel(
        timestamp="2025-05-16T12:34:56.000Z",
        facility=16,
        severity=6,
        message=msg,
    )

    # Initialize the decoder with an empty cache
    decoder = GenericXMLDecoderPlugin({})

    # Call the decode method
    result = decoder.decode(model)

    # Verify the result
    assert result is False
    # Event data should not have been populated
    assert not model.event_data
