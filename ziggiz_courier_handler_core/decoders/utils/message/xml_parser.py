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
Utility for parsing XML messages.

This module provides a parser that handles XML formatted messages using xmltodict.
It attempts to parse XML data and handles common issues like improper
escaping of special characters.
"""
# Standard library imports
import logging
import re

from typing import Any, Optional

# Third-party imports
import xmltodict

# Local/package imports
from ziggiz_courier_handler_core.decoders.utils.message.base_parser import (
    BaseMessageParser,
)

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


class XMLParser(BaseMessageParser[dict[str, Any]]):
    """
    Parser for XML message strings.
    Handles XML formatted messages and common escaping issues.
    """

    @staticmethod
    def parse(message: Optional[str]) -> Optional[dict[str, Any]]:
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
            >>> XMLParser.parse(message)
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
                    fixed_message,
                    attr_prefix="@",
                    cdata_key="#text",
                    dict_constructor=dict,
                )
            except Exception as e:
                # If that fails too, log the error and return None
                logger.debug("Failed to parse XML message", extra={"error": str(e)})
                return None

        # Add DTD information if available
        if dtd_name and result:
            result["_dtd_name"] = dtd_name

        return result


# The old function has been removed in favor of the class method
# Use XMLParser.parse() directly
