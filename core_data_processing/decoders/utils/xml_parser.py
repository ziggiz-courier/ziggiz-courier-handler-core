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
Utility for parsing XML messages.

This module provides a parser that handles XML formatted messages using xmltodict.
It attempts to parse XML data and handles common issues like improper
escaping of special characters.
"""
# Standard library imports
import logging
import re

from typing import Any, Dict, Optional

# Third-party imports
import xmltodict

logger = logging.getLogger(__name__)


def _extract_dtd_name(message: str) -> Optional[str]:
    """
    Extract the DTD name from an XML document with a DOCTYPE declaration.

    Args:
        message: The XML message containing a DOCTYPE declaration

    Returns:
        The name of the DTD or None if not found
    """
    if "<!DOCTYPE" in message:
        # Use regex to extract the DTD name from the DOCTYPE declaration
        match = re.search(r"<!DOCTYPE\s+(\w+)", message)
        if match:
            return match.group(1)
    return None


def parse_xml_message(message: str) -> Optional[Dict[str, Any]]:
    """
    Parse an XML message into a dictionary structure using xmltodict.

    This function attempts to parse the given string as XML and convert it to a
    dictionary. It checks if the message appears to be XML (starts with < and contains
    a valid XML tag structure) before attempting to parse. If initial parsing fails,
    it attempts to fix common escaping issues before trying again.

    Args:
        message: The raw message that should be in XML format

    Returns:
        Dictionary representing the parsed XML structure, or None if
        parsing fails or if the input is not valid XML.

    Example:
        >>> message = '<root><user id="123">John</user><status>active</status></root>'
        >>> parse_xml_message(message)
        {'root': {'user': 'John', '@id': '123', 'status': 'active'}}
    """
    if not message:
        return None

    # Quick check if the message appears to be XML (starts with < and contains >)
    message = message.strip()
    if not (message.startswith("<") and ">" in message):
        return None

    # Extract DTD name if present
    dtd_name = _extract_dtd_name(message)

    # Attempt XML parsing
    try:
        result = xmltodict.parse(
            message, attr_prefix="@", cdata_key="#text", dict_constructor=dict
        )
    except Exception:
        # First attempt failed, try fixing common issues
        try:
            # Fix common XML escaping issues
            fixed_message = message.replace("&", "&amp;")
            # Don't double-escape already properly escaped entities
            fixed_message = fixed_message.replace("&amp;amp;", "&amp;")
            fixed_message = fixed_message.replace("&amp;lt;", "&lt;")
            fixed_message = fixed_message.replace("&amp;gt;", "&gt;")
            fixed_message = fixed_message.replace("&amp;quot;", "&quot;")
            fixed_message = fixed_message.replace("&amp;apos;", "&apos;")

            result = xmltodict.parse(
                fixed_message, attr_prefix="@", cdata_key="#text", dict_constructor=dict
            )
        except Exception as e:
            # If that fails too, log the error and return None
            logger.debug("Failed to parse XML message", extra={"error": str(e)})
            return None

    # Add DTD information if available
    if dtd_name and result:
        result["_dtd_name"] = dtd_name

    return result
