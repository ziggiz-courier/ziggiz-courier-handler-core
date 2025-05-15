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
Unit tests for parse_quoted_csv_message utility.
"""
# Third-party imports
import pytest

# Local/package imports
from core_data_processing.decoders.utils.csv_parser import parse_quoted_csv_message


@pytest.mark.unit
def test_parse_quoted_csv_message_simple():
    message = "field1,field2,field3"
    assert parse_quoted_csv_message(message) == ["field1", "field2", "field3"]


@pytest.mark.unit
def test_parse_quoted_csv_message_quoted():
    message = 'field1,"field 2, with comma",field3'
    assert parse_quoted_csv_message(message) == [
        "field1",
        "field 2, with comma",
        "field3",
    ]


@pytest.mark.unit
def test_parse_quoted_csv_message_escaped_quote():
    # The csv module expects double quotes to escape quotes inside quoted fields
    message = 'field1,"field with ""quote"" inside",field3'
    assert parse_quoted_csv_message(message) == [
        "field1",
        'field with "quote" inside',
        "field3",
    ]


@pytest.mark.unit
def test_parse_quoted_csv_message_empty():
    assert parse_quoted_csv_message("") is None


@pytest.mark.unit
def test_parse_quoted_csv_message_invalid():
    # Not a valid CSV, but csv.reader will return a single field
    assert parse_quoted_csv_message("not_a_csv") == ["not_a_csv"]


@pytest.mark.unit
def test_parse_quoted_csv_message_whitespace():
    message = '  field1 ,  "field 2" , field3  '
    # The csv module preserves spaces inside quoted fields
    assert parse_quoted_csv_message(message) == ["field1 ", "field 2 ", "field3  "]
