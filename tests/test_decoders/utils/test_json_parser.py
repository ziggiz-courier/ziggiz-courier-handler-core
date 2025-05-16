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
Unit tests for the JSON parser utility (parse_json_message).
Covers parsing of JSON formats.
"""
# Third-party imports
import pytest

# Local/package imports
from core_data_processing.decoders.utils.json_parser import parse_json_message


@pytest.mark.unit
def test_parse_json_message_basic():
    """Test basic JSON message parsing with standard JSON object."""
    msg = '{"event": "login", "user": "admin", "status": "success"}'
    result = parse_json_message(msg)
    assert result["event"] == "login"
    assert result["user"] == "admin"
    assert result["status"] == "success"


@pytest.mark.unit
def test_parse_json_message_nested():
    """Test JSON message parsing with nested structures."""
    msg = (
        '{"user": {"id": 123, "name": "John"}, "actions": ["login", "view_dashboard"]}'
    )
    result = parse_json_message(msg)
    assert result["user"]["id"] == 123
    assert result["user"]["name"] == "John"
    assert "login" in result["actions"]
    assert "view_dashboard" in result["actions"]


@pytest.mark.unit
def test_parse_json_message_with_whitespace():
    """Test JSON message parsing with extra whitespace."""
    msg = '  {  "event"  :  "login"  ,  "user"  :  "admin"  }  '
    result = parse_json_message(msg)
    assert result["event"] == "login"
    assert result["user"] == "admin"


@pytest.mark.unit
def test_parse_json_invalid_format():
    """Test handling of invalid JSON formats."""
    # Not a JSON object
    assert parse_json_message("not json") is None

    # Empty message
    assert parse_json_message("") is None

    # Array instead of object (we're enforcing objects with key-value pairs)
    assert parse_json_message("[1, 2, 3]") is None

    # Malformed JSON
    assert parse_json_message('{"key": "value"') is None

    # Not starting with { and ending with }
    assert parse_json_message('"string value"') is None
