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
Unit tests for the LEEF 2.0 parser utility (parse_leef_message).
Covers IBM QRadar Log Event Extended Format 2.0 messages.
"""
# Third-party imports
import pytest

# Local/package imports
from core_data_processing.decoders.utils.leef_2_parser import parse_leef_message


@pytest.mark.unit
def test_parse_leef_2_message_basic():
    """Test basic LEEF 2.0 message parsing with standard header and extension fields."""
    msg = "LEEF:2.0|IBM|QRadar|2.0|12345|src=10.0.0.1\tdst=2.1.2.2\tspt=1232"
    result = parse_leef_message(msg)
    assert result["leef_version"] == "2.0"
    assert result["vendor"] == "IBM"
    assert result["product"] == "QRadar"
    assert result["version"] == "2.0"
    assert result["event_id"] == "12345"
    assert result["src"] == "10.0.0.1"
    assert result["dst"] == "2.1.2.2"
    assert result["spt"] == "1232"


@pytest.mark.unit
def test_parse_leef_2_message_with_category():
    """Test LEEF 2.0 message parsing with event category field."""
    msg = "LEEF:2.0|IBM|QRadar|2.0|12345|SecurityAlert|src=10.0.0.1\tdst=2.1.2.2\tspt=1232"
    result = parse_leef_message(msg)
    assert result["leef_version"] == "2.0"
    assert result["vendor"] == "IBM"
    assert result["product"] == "QRadar"
    assert result["version"] == "2.0"
    assert result["event_id"] == "12345"
    assert result["event_category"] == "SecurityAlert"
    assert result["src"] == "10.0.0.1"
    assert result["dst"] == "2.1.2.2"
    assert result["spt"] == "1232"


@pytest.mark.unit
def test_parse_leef_2_message_with_space_delimiter():
    """Test LEEF 2.0 message parsing with space-delimited extension fields."""
    msg = "LEEF:2.0|IBM|QRadar|2.0|12345|src=10.0.0.1 dst=2.1.2.2 spt=1232"
    result = parse_leef_message(msg)
    assert result["leef_version"] == "2.0"
    assert result["vendor"] == "IBM"
    assert result["product"] == "QRadar"
    assert result["version"] == "2.0"
    assert result["event_id"] == "12345"
    assert result["src"] == "10.0.0.1"
    assert result["dst"] == "2.1.2.2"
    assert result["spt"] == "1232"


@pytest.mark.unit
def test_parse_leef_2_message_with_pipes_in_content():
    """Test LEEF 2.0 message parsing with pipe characters in the content."""
    # In LEEF format, pipes in values must be escaped with a backslash: \|
    msg = "LEEF:2.0|IBM|QRadar|2.0|12345|src=10.0.0.1\tdst=2.1.2.2\tcommand=cat /var/log/messages \\| grep error"
    result = parse_leef_message(msg)
    assert result["command"] == "cat /var/log/messages | grep error"
    assert result["src"] == "10.0.0.1"
    assert result["dst"] == "2.1.2.2"


@pytest.mark.unit
def test_parse_leef_2_message_with_escapes():
    """Test LEEF 2.0 message with escaped characters in extension fields."""
    msg = "LEEF:2.0|IBM|QRadar|2.0|12345|src=10.0.0.1\tmessage=Multiple\\=value\\thas\\=escapes"
    result = parse_leef_message(msg)
    assert result["message"] == "Multiple=value\thas=escapes"
    assert result["src"] == "10.0.0.1"


@pytest.mark.unit
def test_parse_leef_2_message_with_spaces_in_values():
    """Test LEEF 2.0 message with spaces in values."""
    msg = "LEEF:2.0|IBM|QRadar|2.0|12345|src=10.0.0.1\tmsg=This is a message with spaces\tdvc=mydevice"
    result = parse_leef_message(msg)
    assert result["msg"] == "This is a message with spaces"
    assert result["dvc"] == "mydevice"


@pytest.mark.unit
def test_parse_leef_2_message_with_custom_labels():
    """Test LEEF 2.0 message with custom field labels."""
    msg = "LEEF:2.0|IBM|QRadar|2.0|12345|sourceAddress=10.0.0.1\tsourceAddressLabel=SourceIP\tdestAddress=2.1.2.2\tdestAddressLabel=DestIP"
    result = parse_leef_message(msg)
    assert result["sourceAddress"] == "10.0.0.1"
    assert result["destAddress"] == "2.1.2.2"
    assert result["SourceIP"] == "10.0.0.1"
    assert result["DestIP"] == "2.1.2.2"


@pytest.mark.unit
def test_parse_leef_2_invalid_format():
    """Test handling of invalid LEEF 2.0 formats."""
    # Not starting with LEEF:2.
    assert parse_leef_message("LEEF:1.0|IBM|QRadar|1.0|12345") is None
    assert parse_leef_message("Something else") is None

    # Empty message
    assert parse_leef_message("") is None

    # Incomplete header (fewer than 5 pipes)
    assert parse_leef_message("LEEF:2.0|IBM|QRadar|2.0") is None


@pytest.mark.unit
def test_parse_leef_2_with_special_chars():
    """Test LEEF 2.0 message with special characters in values."""
    msg = r"LEEF:2.0|IBM|QRadar|2.0|12345|data=Special\sChars\nNew\tLine\rReturn"
    result = parse_leef_message(msg)
    assert result["data"] == "Special Chars\nNew\tLine\rReturn"
