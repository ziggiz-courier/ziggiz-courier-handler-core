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
Unit tests for parse_quoted_csv_message utility.
"""
# Third-party imports
import pytest

# Local/package imports
from ziggiz_courier_handler_core.decoders.utils.message.csv_parser import (
    parse_quoted_csv_message,
)


@pytest.mark.unit
class TestCSVParser:
    """Unit tests for parse_quoted_csv_message utility."""

    def test_parse_quoted_csv_message_simple(self):
        message = "field1,field2,field3"
        assert parse_quoted_csv_message(message) == ["field1", "field2", "field3"]

    def test_parse_quoted_csv_message_quoted(self):
        message = 'field1,"field 2, with comma",field3'
        assert parse_quoted_csv_message(message) == [
            "field1",
            "field 2, with comma",
            "field3",
        ]

    def test_parse_quoted_csv_message_escaped_quote(self):
        # The csv module expects double quotes to escape quotes inside quoted fields
        message = 'field1,"field with ""quote"" inside",field3'
        assert parse_quoted_csv_message(message) == [
            "field1",
            'field with "quote" inside',
            "field3",
        ]

    def test_parse_quoted_csv_message_empty(self):
        assert parse_quoted_csv_message("") is None

    def test_parse_quoted_csv_message_invalid(self):
        # Not a valid CSV, but csv.reader will return a single field
        assert parse_quoted_csv_message("not_a_csv") == ["not_a_csv"]

    def test_parse_quoted_csv_message_whitespace(self):
        message = '  field1 ,  "field 2" , field3  '
        # The csv module preserves spaces inside quoted fields
        assert parse_quoted_csv_message(message) == ["field1 ", "field 2 ", "field3  "]
