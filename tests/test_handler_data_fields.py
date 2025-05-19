# -*- coding: utf-8 -*-
# # SPDX-License-Identifier: BSL-1.1
# # Copyright (c) 2025 Ziggiz Inc.
# #
# # This file is part of the ziggiz-courier-core-data-processing and is licensed under the
# # Business Source License 1.1. You may not use this file except in
# # compliance with the License. You may obtain a copy of the License at:
# # https://github.com/ziggiz-courier/ziggiz-courier-core-data-processing/blob/main/LICENSE
"""
Tests for verifying handler_data structure in MessageDecoderPluginBase.
"""
from typing import Any

# Third-party imports
import pytest

# Local/package imports
from ziggiz_courier_handler_core.decoders.plugins.message.base import MessageDecoderPluginBase
from ziggiz_courier_handler_core.models.syslog_rfc3164 import SyslogRFC3164Message


# Test implementation of MessageDecoderPluginBase to make it instantiable
class TestMessageDecoderPlugin(MessageDecoderPluginBase):
    """Test implementation of MessageDecoderPluginBase."""
    
    def decode(self, model: Any) -> bool:
        """Implement required abstract method."""
        return True


@pytest.mark.unit
class TestHandlerDataFields:
    """Tests for the handler_data structure."""

    def test_handler_data_structure(self):
        """Test to verify the structure of handler_data after apply_field_mapping."""
        # Create a concrete plugin instance
        plugin = TestMessageDecoderPlugin()
        
        # Create a model
        model = SyslogRFC3164Message(
            facility=16,  # LOCAL0
            severity=6,   # INFO
        )
        
        # Sample event data
        event_data = {"field1": "value1", "field2": "value2"}
        
        # Apply field mapping
        plugin.apply_field_mapping(
            model=model,
            event_data=event_data,
            organization="test_org",
            product="test_product",
            msgclass="test_class"
        )
        
        # Check the structure of handler_data
        assert model.handler_data is not None
        
        # Tests..TestMessageDecoderPlugin because it's a third-party plugin
        key = "tests..TestMessageDecoderPlugin"
        assert key in model.handler_data
        handler_entry = model.handler_data[key]
        
        # Assert expected keys
        assert "msgclass" in handler_entry
        assert handler_entry["msgclass"] == "test_class"
        
        # Check that 'fields' key is NOT present
        assert "fields" not in handler_entry
        
        # Print the full handler_data for inspection
        print(f"Handler data: {model.handler_data}")
        
        # Verify SourceProducer
        assert "SourceProducer" in model.handler_data
        sp = model.handler_data["SourceProducer"]
        assert sp.organization == "test_org"
        assert sp.product == "test_product"
