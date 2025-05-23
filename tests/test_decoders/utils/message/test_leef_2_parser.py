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
Unit tests for the LEEF 2.0 parser utility.
Covers IBM QRadar Log Event Extended Format 2.0 messages.
"""
# Third-party imports
import pytest

# Local/package imports
from ziggiz_courier_handler_core.decoders.utils.message.leef_2_parser import LEEF2Parser


@pytest.mark.unit
class TestLEEF2Parser:
    """Unit tests for the LEEF 2.0 parser utility."""

    def test_parse_leef_2_message_basic(self):
        """Test basic LEEF 2.0 message parsing with standard header and extension fields."""
        delim = "\t"
        msg = (
            "LEEF:2.0|IBM|QRadar|2.0|12345|Alert|"
            + delim
            + "|"
            + "src=10.0.0.1"
            + delim
            + "dst=2.1.2.2"
            + delim
            + "spt=1232"
        )
        result = LEEF2Parser.parse(msg)
        assert result is not None
        assert result["leef_version"] == "2.0"
        assert result["vendor"] == "IBM"
        assert result["product"] == "QRadar"
        assert result["version"] == "2.0"
        assert result["event_id"] == "12345"
        assert result["event_category"] == "Alert"
        assert result["src"] == "10.0.0.1"
        assert result["dst"] == "2.1.2.2"
        assert result["spt"] == "1232"

    def test_parse_leef_2_message_with_category(self):
        """Test LEEF 2.0 message parsing with event category."""
        delim = "\t"
        msg = (
            "LEEF:2.0|IBM|QRadar|2.0|12345|Authentication|"
            + delim
            + "|"
            + "src=10.0.0.1"
            + delim
            + "dst=2.1.2.2"
        )
        result = LEEF2Parser.parse(msg)
        assert result is not None
        assert result["leef_version"] == "2.0"
        assert result["vendor"] == "IBM"
        assert result["product"] == "QRadar"
        assert result["version"] == "2.0"
        assert result["event_id"] == "12345"
        assert result["event_category"] == "Authentication"
        assert result["src"] == "10.0.0.1"
        assert result["dst"] == "2.1.2.2"

    def test_parse_leef_2_message_with_space_delimiter(self):
        """Test LEEF 2.0 message parsing with space-delimited extension fields."""
        delim = " "
        msg = (
            "LEEF:2.0|IBM|QRadar|2.0|12345|Alert|"
            + delim
            + "|"
            + "src=10.0.0.1"
            + delim
            + "dst=2.1.2.2"
            + delim
            + "spt=1232"
        )
        result = LEEF2Parser.parse(msg)
        assert result is not None
        assert result["leef_version"] == "2.0"
        assert result["vendor"] == "IBM"
        assert result["product"] == "QRadar"
        assert result["version"] == "2.0"
        assert result["event_id"] == "12345"
        assert result["event_category"] == "Alert"
        assert result["src"] == "10.0.0.1"
        assert result["dst"] == "2.1.2.2"
        assert result["spt"] == "1232"

    def test_parse_leef_2_message_with_pipes_in_content(self):
        """Test LEEF message parsing with pipe characters in the content."""
        # In LEEF 2.0 format, pipes in values must be escaped with a backslash
        delim = "\t"
        msg = (
            "LEEF:2.0|IBM|QRadar|2.0|12345|Alert|"
            + delim
            + "|"
            + "src=10.0.0.1"
            + delim
            + "dst=2.1.2.2"
            + delim
            + "command=cat /var/log/messages \\| grep error"
        )
        result = LEEF2Parser.parse(msg)
        assert result is not None
        assert result["command"] == "cat /var/log/messages | grep error"
        assert result["src"] == "10.0.0.1"
        assert result["dst"] == "2.1.2.2"

    def test_parse_leef_2_message_with_escapes(self):
        """Test LEEF message with escaped characters in extension fields."""
        delim = "\t"
        msg = (
            "LEEF:2.0|IBM|QRadar|2.0|12345|Alert|"
            + delim
            + "|"
            + "src=10.0.0.1"
            + delim
            + "message=Multiple\\=value\\thas\\=escapes"
        )
        result = LEEF2Parser.parse(msg)
        assert result is not None
        assert result["message"] == "Multiple=value\thas=escapes"
        assert result["src"] == "10.0.0.1"

    def test_parse_leef_2_message_with_source_producer(self):
        """Test LEEF message with source producer information."""
        delim = "\t"
        msg = (
            "LEEF:2.0|IBM|QRadar|2.0|12345|Alert|"
            + delim
            + "|"
            + "src=10.0.0.1"
            + delim
            + "dst=2.1.2.2"
        )
        result = LEEF2Parser.parse(msg)
        assert result is not None
        # This is a unit test for the parser, not for MetaDataProduct validation.
        # Just check the parsed fields.
        assert result["vendor"] == "IBM"
        assert result["product"] == "QRadar"
        assert result["src"] == "10.0.0.1"
        assert result["dst"] == "2.1.2.2"

    def test_parse_leef_2_invalid_format(self):
        """Test handling of invalid LEEF formats."""
        # Not starting with LEEF:
        assert LEEF2Parser.parse("Something else") is None
        # Empty message
        assert LEEF2Parser.parse("") is None
        # Incomplete header (fewer than 5 pipes)
        assert LEEF2Parser.parse("LEEF:2.0|IBM|QRadar|2.0") is None
