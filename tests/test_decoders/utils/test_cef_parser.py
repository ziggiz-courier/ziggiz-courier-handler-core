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
Unit tests for the CEF parser utility (parse_cef_message).
Covers ArcSight Common Event Format messages.
"""
# Third-party imports
import pytest

# Local/package imports
from ziggiz_courier_handler_core.decoders.utils.cef_parser import parse_cef_message


@pytest.mark.unit
class TestCEFParser:
    """Unit tests for the CEF parser utility (parse_cef_message)."""

    def test_parse_cef_message_basic(self):
        """Test basic CEF message parsing with standard header and extension fields."""
        msg = "CEF:0|Security|threatmanager|1.0|100|worm successfully stopped|10|src=10.0.0.1 dst=2.1.2.2 spt=1232"
        result = parse_cef_message(msg)
        assert result["cef_version"] == "0"
        assert result["device_vendor"] == "Security"
        assert result["device_product"] == "threatmanager"
        assert result["device_version"] == "1.0"
        assert result["signature_id"] == "100"
        assert result["name"] == "worm successfully stopped"
        assert result["severity"] == "10"
        assert result["src"] == "10.0.0.1"
        assert result["dst"] == "2.1.2.2"
        assert result["spt"] == "1232"

    def test_parse_cef_message_with_pipes_in_content(self):
        """Test CEF message parsing with pipe characters in the content."""
        # In CEF format, pipes in values must be escaped with a backslash: \|
        msg = "CEF:0|Security|threatmanager|1.0|100|command: cat /var/log/messages \\| grep error|10|src=10.0.0.1 dst=2.1.2.2"
        result = parse_cef_message(msg)
        assert result["name"] == "command: cat /var/log/messages | grep error"
        assert result["src"] == "10.0.0.1"
        assert result["dst"] == "2.1.2.2"

    def test_parse_cef_message_with_escapes(self):
        """Test CEF message with escaped characters in extension fields."""
        msg = "CEF:0|Security|threatmanager|1.0|100|detected\\|blocked|10|src=10.0.0.1 message=Multiple\\ spaces\\ in\\ value"
        result = parse_cef_message(msg)
        assert result["message"] == "Multiple spaces in value"
        assert result["src"] == "10.0.0.1"

    def test_parse_cef_message_with_user_labels(self):
        """Test CEF message with user-defined labels for custom fields."""
        msg = "CEF:0|Security|threatmanager|1.0|100|detected|10|src=10.0.0.1 deviceCustomNumber1=5 deviceCustomNumber1Label=ImportantMetric"
        result = parse_cef_message(msg)
        assert result["deviceCustomNumber1"] == "5"
        assert result["deviceCustomNumber1Label"] == "ImportantMetric"
        assert (
            result["ImportantMetric"] == "5"
        )  # The user-defined label should map to the original value

    def test_parse_cef_message_with_spaces_in_values(self):
        """Test CEF message with spaces in values."""
        msg = "CEF:0|Security|threatmanager|1.0|100|detected|10|src=10.0.0.1 msg=This is a message with spaces dvc=mydevice"
        result = parse_cef_message(msg)
        assert result["msg"] == "This is a message with spaces"
        assert result["dvc"] == "mydevice"

    def test_parse_cef_invalid_format(self):
        """Test handling of invalid CEF formats."""
        # Not starting with CEF:
        assert parse_cef_message("Something else") is None

        # Empty message
        assert parse_cef_message("") is None

        # Incomplete header (fewer than 7 pipes)
        assert parse_cef_message("CEF:0|Vendor|Product|1.0|100|name") is None
