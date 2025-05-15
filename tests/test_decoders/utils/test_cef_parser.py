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
Unit tests for the CEF parser utility (parse_cef_message).
Covers ArcSight Common Event Format messages.
"""
# Third-party imports
import pytest

# Local/package imports
from core_data_processing.decoders.utils.cef_parser import parse_cef_message


@pytest.mark.unit
def test_parse_cef_message_basic():
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


@pytest.mark.unit
def test_parse_cef_message_with_pipes_in_content():
    """Test CEF message parsing with pipe characters in the content."""
    # In CEF format, pipes in values must be escaped with a backslash: \|
    msg = "CEF:0|Security|threatmanager|1.0|100|command: cat /var/log/messages \\| grep error|10|src=10.0.0.1 dst=2.1.2.2"
    result = parse_cef_message(msg)
    assert result["name"] == "command: cat /var/log/messages | grep error"
    assert result["src"] == "10.0.0.1"
    assert result["dst"] == "2.1.2.2"


@pytest.mark.unit
def test_parse_cef_message_with_escapes():
    """Test CEF message with escaped characters in extension fields."""
    msg = "CEF:0|Security|threatmanager|1.0|100|detected\\|blocked|10|src=10.0.0.1 message=Multiple\\ spaces\\ in\\ value"
    result = parse_cef_message(msg)
    assert result["message"] == "Multiple spaces in value"
    assert result["src"] == "10.0.0.1"


@pytest.mark.unit
def test_parse_cef_message_with_user_labels():
    """Test CEF message with user-defined labels for custom fields."""
    msg = "CEF:0|Security|threatmanager|1.0|100|detected|10|src=10.0.0.1 deviceCustomNumber1=5 deviceCustomNumber1Label=ImportantMetric"
    result = parse_cef_message(msg)
    assert result["deviceCustomNumber1"] == "5"
    assert result["deviceCustomNumber1Label"] == "ImportantMetric"
    assert (
        result["ImportantMetric"] == "5"
    )  # The user-defined label should map to the original value


@pytest.mark.unit
def test_parse_cef_message_with_spaces_in_values():
    """Test CEF message with spaces in values."""
    msg = "CEF:0|Security|threatmanager|1.0|100|detected|10|src=10.0.0.1 msg=This is a message with spaces dvc=mydevice"
    result = parse_cef_message(msg)
    assert result["msg"] == "This is a message with spaces"
    assert result["dvc"] == "mydevice"


@pytest.mark.unit
def test_parse_cef_invalid_format():
    """Test handling of invalid CEF formats."""
    # Not starting with CEF:
    assert parse_cef_message("Something else") is None

    # Empty message
    assert parse_cef_message("") is None

    # Incomplete header (fewer than 7 pipes)
    assert parse_cef_message("CEF:0|Vendor|Product|1.0|100|name") is None
