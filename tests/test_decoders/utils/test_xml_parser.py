# -*- coding: utf-8 -*-
# # SPDX-License-Identifier: BSL-1.1
# # Copyright (c) 2025 Ziggiz Inc.
# #
# # This file is part of the ziggiz-courier-core-data-processing and is licensed under the
# # Business Source License 1.1. You may not use this file except in
# # compliance with the License. You may obtain a copy of the License at:
# # https://github.com/ziggiz-courier/ziggiz-courier-core-data-processing/blob/main/LICENSE
"""
Unit tests for XML parser utilities.
"""
# Third-party imports
import pytest

# Local/package imports
from ziggiz_courier_handler_core.decoders.utils.xml_parser import parse_xml_message



@pytest.mark.unit
class TestXMLParser:
    """Unit tests for XML parser utilities."""

    def test_parse_xml_message_simple(self):
        xml = "<root><item>value</item></root>"
        result = parse_xml_message(xml)
        assert result is not None
        assert "root" in result
        assert "item" in result["root"]
        assert result["root"]["item"] == "value"

    def test_parse_xml_message_with_attributes(self):
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

    def test_parse_xml_message_with_nested_elements(self):
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

    def test_parse_xml_message_with_dtd(self):
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

    def test_parse_xml_message_with_broken_entities(self):
        xml = "<root><item>Value with & ampersand</item></root>"
        result = parse_xml_message(xml)
        assert result is not None
        assert "root" in result
        assert "item" in result["root"]
        assert result["root"]["item"] == "Value with & ampersand"

    def test_parse_xml_message_with_cdata(self):
        xml = "<root><item><![CDATA[Value with <special> characters & entities]]></item></root>"
        result = parse_xml_message(xml)
        assert result is not None
        assert "root" in result
        assert "item" in result["root"]
        assert result["root"]["item"] == "Value with <special> characters & entities"

    def test_parse_xml_message_with_multiple_root_attributes(self):
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

    def test_parse_xml_message_invalid_xml(self):
        xml = "<root><item>value</wrong_tag></root>"
        result = parse_xml_message(xml)
        assert result is None

    def test_parse_xml_message_not_xml(self):
        not_xml = "This is not XML content"
        result = parse_xml_message(not_xml)
        assert result is None

    def test_parse_xml_message_empty(self):
        result = parse_xml_message("")
        assert result is None
        result = parse_xml_message(None)
        assert result is None
