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


@pytest.mark.unit
def test_parse_json_with_escaped_control_chars():
    """Test JSON message parsing with escaped control characters."""
    # JSON with escaped control characters (\r\n)
    msg = '{\r\n  "event": "system_check",\r\n  "status": "success",\r\n  "details": {\r\n    "cpu": 0.45,\r\n    "memory": 1024,\r\n    "disk": {\r\n      "total": 500,\r\n      "used": 120\r\n    }\r\n  },\r\n  "timestamp": "2025-05-16T12:34:56.789Z"\r\n}'

    result = parse_json_message(msg)
    assert result is not None
    assert result["event"] == "system_check"
    assert result["status"] == "success"
    assert "details" in result
    assert result["details"]["cpu"] == 0.45
    assert result["details"]["disk"]["total"] == 500
    assert result["timestamp"] == "2025-05-16T12:34:56.789Z"


@pytest.mark.unit
def test_parse_json_with_escaped_quotes():
    """Test JSON message parsing with escaped quotes in string."""
    # JSON with escaped quotes - simpler example
    msg = '{"name": "test_application", "message": "User \\"admin\\" logged in", "level": "info"}'

    result = parse_json_message(msg)
    assert result is not None
    assert result["name"] == "test_application"
    assert result["message"] == 'User "admin" logged in'
    assert result["level"] == "info"


@pytest.mark.unit
def test_parse_json_with_complex_escaping():
    """Test JSON message parsing with multiple escaped characters that require special handling."""
    # Complex JSON with various escape combinations
    msg = '{"config": {"path": "C:\\\\Program Files\\\\App\\\\", "options": "--format=\\"compact\\" --verbose"}, "description": "Configuration with \\\\ and \\" characters"}'

    result = parse_json_message(msg)
    assert result is not None
    assert result["config"]["path"] == "C:\\Program Files\\App\\"
    assert result["config"]["options"] == '--format="compact" --verbose'
    assert "Configuration with \\ and " in result["description"]


@pytest.mark.unit
def test_parse_json_with_unicode_escapes():
    """Test JSON message parsing with Unicode escape sequences and special characters."""
    # Test JSON with Unicode escapes and various control characters
    msg = '{"message": "Test with Unicode \\u00A9 copyright and \\u2122 trademark", "errors": "Error at line \\t1:\\n\\tInvalid syntax", "path": "C:\\\\Users\\\\test\\\\Documents\\\\logs"}'

    result = parse_json_message(msg)
    assert result is not None
    assert result["message"] == "Test with Unicode © copyright and ™ trademark"
    assert result["errors"] == "Error at line \t1:\n\tInvalid syntax"
    assert result["path"] == "C:\\Users\\test\\Documents\\logs"


@pytest.mark.unit
def test_parse_json_recovery_scenarios():
    """Test the parser's ability to recover from common formatting issues in JSON."""
    # Test with missing escapes for backslashes in Windows paths (as raw input with r prefix)
    broken_path = r'{"path": "C:\Program Files\App\logs", "level": "debug"}'
    result = parse_json_message(broken_path)
    assert result is None  # This is invalid JSON and should return None

    # Test with properly escaped control characters that should be parsed
    valid_with_control = '{"message": "Line 1\\r\\nLine 2", "status": "complete"}'
    result = parse_json_message(valid_with_control)
    assert result is not None
    assert "message" in result
    assert "status" in result
    assert result["status"] == "complete"
    assert "Line 1" in result["message"]


@pytest.mark.unit
def test_parse_json_with_full_control_char_set():
    """Test JSON message parsing with all standard JSON control character escape sequences."""
    msg = """{"controls": {
        "tab": "Tab: \\t character",
        "newline": "Newline: \\n character",
        "carriage_return": "Carriage return: \\r character",
        "form_feed": "Form feed: \\f character",
        "backspace": "Backspace: \\b character",
        "quote": "Quote: \\" character",
        "backslash": "Backslash: \\\\ character",
        "forward_slash": "Forward slash: \\/ character"
    }}"""

    result = parse_json_message(msg)
    assert result is not None
    assert result["controls"]["tab"] == "Tab: \t character"
    assert result["controls"]["newline"] == "Newline: \n character"
    assert result["controls"]["carriage_return"] == "Carriage return: \r character"
    assert result["controls"]["form_feed"] == "Form feed: \f character"
    assert result["controls"]["backspace"] == "Backspace: \b character"
    assert result["controls"]["quote"] == 'Quote: " character'
    assert result["controls"]["backslash"] == "Backslash: \\ character"
    assert result["controls"]["forward_slash"] == "Forward slash: / character"


@pytest.mark.unit
def test_parse_json_with_multi_char_unicode_escapes():
    """Test JSON message parsing with 4-digit and 8-digit Unicode escape sequences."""
    # Test with both 4-digit and surrogate pair (8-digit) Unicode escapes
    msg = """{"unicode": {
        "basic_latin": "ASCII: \\u0041\\u0042\\u0043",
        "latin1_supplement": "Latin-1: \\u00A1\\u00A3\\u00A9",
        "emoji": "Emoji: \\ud83d\\ude04\\ud83d\\udc4d",
        "cjk": "CJK: \\u4e2d\\u56fd\\u8bed",
        "mixed": "Mixed: A\\u00A9\\ud83d\\ude00Z"
    }}"""

    result = parse_json_message(msg)
    assert result is not None
    assert result["unicode"]["basic_latin"] == "ASCII: ABC"
    assert result["unicode"]["latin1_supplement"] == "Latin-1: ¡£©"
    assert "Emoji: " in result["unicode"]["emoji"]
    assert "CJK: " in result["unicode"]["cjk"]
    assert result["unicode"]["mixed"].startswith("Mixed: A©")
    assert result["unicode"]["mixed"].endswith("Z")


@pytest.mark.unit
def test_parse_json_with_nested_escape_sequences():
    """Test JSON message parsing with nested and adjacent escape sequences."""
    msg = """{"nested_escapes": {
        "adjacent_controls": "Controls: \\n\\t\\r\\n\\t",
        "escaped_json": "{\\"key\\":\\"value\\",\\"nested\\":{\\"another\\":\\"value\\"}}"
    }}"""

    result = parse_json_message(msg)
    assert result is not None
    assert result["nested_escapes"]["adjacent_controls"] == "Controls: \n\t\r\n\t"
    assert (
        result["nested_escapes"]["escaped_json"]
        == '{"key":"value","nested":{"another":"value"}}'
    )


@pytest.mark.unit
def test_parse_json_recovery_with_missing_quotes():
    """Test recovery from JSON with missing quotes."""
    # With one missing quote that might be recoverable by standard JSON parser fallback
    invalid_json = '{"key": value", "status": "error"}'
    result = parse_json_message(invalid_json)
    assert result is None  # Invalid JSON should return None

    # Valid JSON with quoted values
    valid_json = '{"key": "value", "status": "error"}'
    result = parse_json_message(valid_json)
    assert result is not None
    assert result["key"] == "value"
    assert result["status"] == "error"


@pytest.mark.unit
def test_parse_json_with_numeric_escape_sequences():
    """Test JSON message parsing with numeric escape sequences.

    Note: Standard JSON doesn't support \\0xx (octal) or \\xhh (hex) escapes like JavaScript.
    This test verifies the current behavior of rejecting invalid escape sequences.
    """
    # Invalid JSON with non-standard escape sequences
    invalid_msg = '{"octal_like": "File mode: \\060\\064\\064", "hex_like": "Bytes: \\x48\\x65\\x6c\\x6c\\x6f"}'
    result = parse_json_message(invalid_msg)
    assert result is None  # Our parser correctly rejects invalid escape sequences

    # Valid JSON with standard escape sequences only
    valid_msg = '{"unicode_hex": "Unicode hex: \\u0048\\u0065\\u006c\\u006c\\u006f", "text": "Plain text"}'
    result = parse_json_message(valid_msg)
    assert result is not None
    assert result["unicode_hex"] == "Unicode hex: Hello"
    assert result["text"] == "Plain text"


@pytest.mark.unit
def test_parse_json_recovery_with_trailing_comma():
    """Test recovery from JSON with trailing commas (which are invalid in standard JSON)."""
    # JSON with trailing commas at different nesting levels
    invalid_json = '{"array": [1, 2, 3,], "object": {"a": 1, "b": 2,}}'
    result = parse_json_message(invalid_json)
    assert result is None  # Standard JSON parsers should reject this

    # Corrected version
    valid_json = '{"array": [1, 2, 3], "object": {"a": 1, "b": 2}}'
    result = parse_json_message(valid_json)
    assert result is not None
    assert result["array"] == [1, 2, 3]
    assert result["object"]["a"] == 1
    assert result["object"]["b"] == 2


@pytest.mark.unit
def test_parse_json_with_escaped_slashes():
    """Test JSON message parsing with escaped forward slashes."""
    # JSON with escaped forward slashes (valid in JSON)
    msg = '{"url": "http:\\/\\/example.com\\/path\\/to\\/resource"}'

    result = parse_json_message(msg)
    assert result is not None
    assert result["url"] == "http://example.com/path/to/resource"


@pytest.mark.unit
def test_parse_json_recovery_from_malformed_unicode():
    """Test recovery from JSON with malformed Unicode escape sequences."""
    # JSON with invalid Unicode escape sequences
    invalid_unicode = (
        '{"bad_escape": "Invalid unicode: \\u123Z", "valid": "This is valid"}'
    )
    result = parse_json_message(invalid_unicode)
    assert result is None  # This is invalid JSON and should return None

    # JSON with valid Unicode escape sequences
    valid_unicode = (
        '{"good_escape": "Valid unicode: \\u1234", "valid": "This is valid"}'
    )
    result = parse_json_message(valid_unicode)
    assert result is not None
    assert "Valid unicode: " in result["good_escape"]
    assert result["valid"] == "This is valid"
