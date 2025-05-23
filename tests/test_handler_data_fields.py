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
Tests for verifying handler_data structure in MessageDecoderPluginBase.
"""
# Standard library imports
from typing import Any

# Third-party imports
import pytest

# Local/package imports
from ziggiz_courier_handler_core.decoders.plugins.message.base import (
    MessageDecoderPluginBase,
)
from ziggiz_courier_handler_core.models.syslog_rfc3164 import SyslogRFC3164Message


# Implementation of MessageDecoderPluginBase for testing purposes
class MockMessageDecoderPlugin(MessageDecoderPluginBase):
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
        plugin = MockMessageDecoderPlugin()

        # Create a model
        model = SyslogRFC3164Message(
            facility=16,  # LOCAL0
            severity=6,  # INFO
        )

        # Sample event data
        event_data = {"field1": "value1", "field2": "value2"}

        # Apply field mapping (no organization/product)
        plugin.apply_field_mapping(
            model=model,
            event_data=event_data,
            msgclass="test_class",
        )
        # Set SourceProducer handler data
        plugin._set_meta_data_product_handler_data(model, "test_org", "test_product")

        # Check the structure of handler_data
        assert model.handler_data is not None

        # Tests..MockMessageDecoderPlugin because it's a third-party plugin
        plugin_key = "tests..MockMessageDecoderPlugin"
        assert plugin_key in model.handler_data
        handler_entry = model.handler_data[plugin_key]

        # Assert expected keys
        assert "msgclass" in handler_entry
        assert handler_entry["msgclass"] == "test_class"

        # Check that 'fields' key is NOT present
        assert "fields" not in handler_entry

        # Print the full handler_data for inspection
        print(f"Handler data: {model.handler_data}")

        # Verify SourceProducer (now keyed by "SourceProducer")
        sp_key = "SourceProducer"
        assert sp_key in model.handler_data
        sp = model.handler_data[sp_key]
        assert sp.organization == "test_org"
        assert sp.product == "test_product"
