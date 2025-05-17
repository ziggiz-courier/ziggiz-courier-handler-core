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
Unit tests for XML parser utilities.
"""
# Third-party imports
import pytest

# Local/package imports
from core_data_processing.decoders.utils.xml_parser import parse_xml_message


@pytest.mark.unit
def test_parse_xml_message_simple():
    """Test XML parsing with a simple XML message."""
    xml = "<root><item>value</item></root>"
    result = parse_xml_message(xml)
    assert result is not None
    assert "root" in result
    assert "item" in result["root"]
    assert result["root"]["item"] == "value"


@pytest.mark.unit
def test_parse_xml_message_with_attributes():
    """Test XML parsing with a message containing attributes."""
    xml = '<root><item id="123" type="test">value</item></root>'
    result = parse_xml_message(xml)
    assert result is not None
    assert "root" in result
    assert "item" in result["root"]
    assert "@id" in result["root"]["item"]
    assert "@type" in result["root"]["item"]
    assert result["root"]["item"]["@id"] == "123"
    assert result["root"]["item"]["@type"] == "test"
    assert "#text" in result["root"]["item"]
    assert result["root"]["item"]["#text"] == "value"


@pytest.mark.unit
def test_parse_xml_message_with_nested_elements():
    """Test XML parsing with nested elements."""
    xml = """
    <root>
        <parent>
            <child>value1</child>
            <child>value2</child>
        </parent>
    </root>
    """
    result = parse_xml_message(xml)
    assert result is not None
    assert "root" in result
    assert "parent" in result["root"]
    assert "child" in result["root"]["parent"]
    assert isinstance(result["root"]["parent"]["child"], list)
    assert len(result["root"]["parent"]["child"]) == 2
    assert "value1" in result["root"]["parent"]["child"]
    assert "value2" in result["root"]["parent"]["child"]


@pytest.mark.unit
def test_parse_xml_message_with_dtd():
    """Test XML parsing with a DTD declaration."""
    xml = """<?xml version="1.0"?>
    <!DOCTYPE note SYSTEM "note.dtd">
    <note>
        <to>User</to>
        <from>System</from>
        <body>Test message</body>
    </note>
    """
    result = parse_xml_message(xml)
    assert result is not None
    assert "_dtd_name" in result
    assert result["_dtd_name"] == "note"
    assert "note" in result
    assert result["note"]["to"] == "User"
    assert result["note"]["from"] == "System"
    assert result["note"]["body"] == "Test message"


@pytest.mark.unit
def test_parse_xml_message_with_broken_entities():
    """Test XML parsing with broken/unescaped entities."""
    xml = "<root><item>Value with & ampersand</item></root>"
    result = parse_xml_message(xml)
    assert result is not None
    assert "root" in result
    assert "item" in result["root"]
    assert result["root"]["item"] == "Value with & ampersand"


@pytest.mark.unit
def test_parse_xml_message_with_cdata():
    """Test XML parsing with CDATA sections."""
    xml = "<root><item><![CDATA[Value with <special> characters & entities]]></item></root>"
    result = parse_xml_message(xml)
    assert result is not None
    assert "root" in result
    assert "item" in result["root"]
    assert result["root"]["item"] == "Value with <special> characters & entities"


@pytest.mark.unit
def test_parse_xml_message_with_multiple_root_attributes():
    """Test XML parsing with attributes on the root element."""
    xml = '<root id="1" version="2.0"><item>value</item></root>'
    result = parse_xml_message(xml)
    assert result is not None
    assert "root" in result
    assert "@id" in result["root"]
    assert "@version" in result["root"]
    assert result["root"]["@id"] == "1"
    assert result["root"]["@version"] == "2.0"
    assert "item" in result["root"]
    assert result["root"]["item"] == "value"


@pytest.mark.unit
def test_parse_xml_message_invalid_xml():
    """Test XML parsing with invalid XML."""
    xml = "<root><item>value</wrong_tag></root>"
    result = parse_xml_message(xml)
    assert result is None


@pytest.mark.unit
def test_parse_xml_message_not_xml():
    """Test XML parsing with non-XML content."""
    not_xml = "This is not XML content"
    result = parse_xml_message(not_xml)
    assert result is None


@pytest.mark.unit
def test_parse_xml_message_empty():
    """Test XML parsing with empty content."""
    result = parse_xml_message("")
    assert result is None
    result = parse_xml_message(None)
    assert result is None
