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
Unit tests for CSVParser utility.
"""
# Third-party imports
import pytest

# Local/package imports
from ziggiz_courier_handler_core.decoders.utils.message.csv_parser import CSVParser


@pytest.mark.unit
class TestCSVParser:
    """Unit tests for CSVParser utility."""

    def test_parse_simple(self):
        """Test parsing a simple CSV message."""
        message = "field1,field2,field3"
        assert CSVParser.parse(message) == ["field1", "field2", "field3"]

    def test_parse_quoted(self):
        """Test parsing a CSV message with quoted fields containing commas."""
        message = 'field1,"field 2, with comma",field3'
        assert CSVParser.parse(message) == [
            "field1",
            "field 2, with comma",
            "field3",
        ]

    def test_parse_escaped_quote(self):
        """Test parsing a CSV message with escaped quotes inside quoted fields."""
        # The csv module expects double quotes to escape quotes inside quoted fields
        message = 'field1,"field with ""quote"" inside",field3'
        assert CSVParser.parse(message) == [
            "field1",
            'field with "quote" inside',
            "field3",
        ]

    def test_parse_empty(self):
        """Test parsing an empty message."""
        assert CSVParser.parse("") is None

    def test_parse_invalid(self):
        """Test parsing an invalid CSV message."""
        # Not a valid CSV, but csv.reader will return a single field
        message = "not_a_csv"
        assert CSVParser.parse(message) == ["not_a_csv"]

    def test_parse_whitespace(self):
        """Test parsing a CSV message with whitespace around values."""
        message = '  field1 ,  "field 2" , field3  '
        # The csv module preserves spaces inside quoted fields and around unquoted fields
        assert CSVParser.parse(message) == ["field1 ", "field 2 ", "field3  "]
