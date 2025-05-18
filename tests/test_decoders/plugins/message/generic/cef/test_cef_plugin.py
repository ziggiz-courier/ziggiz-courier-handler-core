# -*- coding: utf-8 -*-
# # SPDX-License-Identifier: BSL-1.1
# # Copyright (c) 2025 Ziggiz Inc.
# #
# # This file is part of the ziggiz-courier-core-data-processing and is licensed under the
# # Business Source License 1.1. You may not use this file except in
# # compliance with the License. You may obtain a copy of the License at:
# # https://github.com/ziggiz-courier/ziggiz-courier-core-data-processing/blob/main/LICENSE
"""
Unit tests for GenericCEFDecoderPlugin.
"""
# Third-party imports
import pytest

# Local/package imports
from ziggiz_courier_handler_core.decoders.plugins.message.generic.cef.plugin import (
    GenericCEFDecoderPlugin,
)
from ziggiz_courier_handler_core.models.syslog_rfc_base import SyslogRFCBaseModel


@pytest.mark.unit
def test_generic_cef_basic_case():
    """Test GenericCEFDecoderPlugin with basic CEF message format."""
    # Create a model with a test CEF message
    msg = "CEF:1|Security|threatmanager|1.0|100|worm successfully stopped|10|src=10.0.0.1 dst=2.1.2.2 spt=1232"
    model = SyslogRFCBaseModel(
        timestamp="2025-05-13T12:34:56.000Z",
        facility=16,  # LOCAL0
        severity=6,  # INFO
        message=msg,
    )

    # Initialize the decoder with an empty cache
    decoder = GenericCEFDecoderPlugin()

    # Call the decode method
    result = decoder.decode(model)

    # Verify the result

    assert result is True
    key = "GenericCEFDecoderPlugin"
    assert model.handler_data is not None
    assert key in model.handler_data
    handler_entry = model.handler_data[key]
    assert handler_entry["vendor"] == "security"
    assert handler_entry["product"] == "threatmanager"
    assert handler_entry["msgclass"] == "worm successfully stopped"

    # Verify specific fields in the parsed data
    assert model.event_data is not None
    assert "cef_version" in model.event_data
    assert model.event_data["cef_version"] == "1"
    assert model.event_data["src"] == "10.0.0.1"
    assert model.event_data["dst"] == "2.1.2.2"
    assert model.event_data["spt"] == "1232"


@pytest.mark.unit
def test_generic_cef_with_custom_fields():
    """Test GenericCEFDecoderPlugin with custom fields."""
    # Create a model with a test CEF message with custom fields
    msg = "CEF:1|Vendor|Product|1.0|100|Name|10|src=10.0.0.1 customField=customValue"
    model = SyslogRFCBaseModel(
        timestamp="2025-05-13T12:34:56.000Z",
        facility=16,
        severity=6,
        message=msg,
    )

    # Initialize the decoder
    decoder = GenericCEFDecoderPlugin()

    # Call the decode method
    result = decoder.decode(model)

    # Verify the result

    assert result is True
    key = "GenericCEFDecoderPlugin"
    assert model.handler_data is not None
    assert key in model.handler_data
    handler_entry = model.handler_data[key]
    assert handler_entry["vendor"] == "vendor"
    assert handler_entry["product"] == "product"
    assert model.event_data is not None
    assert "customField" in model.event_data
    assert model.event_data["customField"] == "customValue"


@pytest.mark.unit
def test_generic_cef_negative_case():
    """Test GenericCEFDecoderPlugin with non-matching message format."""
    # Create a model with a message that should not match CEF format
    msg = "This is not a CEF format message"
    model = SyslogRFCBaseModel(
        timestamp="2025-05-13T12:34:56.000Z",
        facility=16,
        severity=6,
        message=msg,
    )

    # Initialize the decoder
    decoder = GenericCEFDecoderPlugin()

    # Call the decode method
    result = decoder.decode(model)

    # Verify the result is False (no match)
    assert result is False


@pytest.mark.unit
def test_generic_cef_with_wrong_version():
    """Test GenericCEFDecoderPlugin with wrong CEF version."""
    # Create a model with a CEF message with a wrong version
    msg = "CEF:0|Vendor|Product|1.0|100|Name|10|src=10.0.0.1"
    model = SyslogRFCBaseModel(
        timestamp="2025-05-13T12:34:56.000Z",
        facility=16,
        severity=6,
        message=msg,
    )

    # Initialize the decoder
    decoder = GenericCEFDecoderPlugin()

    # Call the decode method
    result = decoder.decode(model)

    # Verify the result is False (wrong version)
    assert result is False
