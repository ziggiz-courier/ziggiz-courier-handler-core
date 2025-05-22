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
Utility for parsing Log Event Extended Format (LEEF) 1.0 log message strings.

LEEF is an IBM QRadar-defined format with a specific structure:
LEEF:Version|Vendor|Product|Version|EventID|Extension

The Extension part contains key-value pairs in the format key=value.
"""
# Standard library imports
from typing import Dict, List, Optional, Union, cast

# Local/package imports
from ziggiz_courier_handler_core.decoders.utils.message.base_parser import (
    BaseMessageParser,
)
from ziggiz_courier_handler_core.models.source_producer import SourceProducer


class LEEF1Parser(BaseMessageParser):
    """
    Parser for Log Event Extended Format (LEEF) 1.0 message strings.
    Handles LEEF header and extension fields with proper escaping rules.
    """

    @staticmethod
    def parse(message: str) -> Optional[Dict[str, Union[str, SourceProducer]]]:
        """
        High-performance parser for Log Event Extended Format (LEEF) 1.0 message strings.
        Handles LEEF header and extension fields with proper escaping rules.

        The LEEF 1.0 format is:
        LEEF:Version|Vendor|Product|Version|EventID|Extension

        Where Extension contains key=value pairs.

        Args:
            message: The raw LEEF message string

        Returns:
            Dictionary of parsed key-value pairs from both header and extension fields,
            or None if not a valid LEEF format.
        """
        if not message or not message.startswith("LEEF:"):
            return None

        # Split the message for initial processing
        try:
            # Split the initial format to get the extension
            parts = LEEF1Parser._safe_split_header(message[5:])  # Skip "LEEF:" prefix

            if len(parts) < 6:
                return None  # Not enough fields

            # Extract header fields
            header_fields = [
                "leef_version",
                "vendor",
                "product",
                "version",
                "event_id",
            ]

            result = {}
            for i, field in enumerate(header_fields):
                result[field] = parts[i]

            # Add SourceProducer instance
            source_producer = SourceProducer(
                organization=result["vendor"], product=result["product"]
            )
            result["source_producer"] = source_producer

            # Process extension (key=value pairs)
            extension = parts[5]
            if extension:
                extension_dict = LEEF1Parser._parse_extension(extension)
                result.update(extension_dict)

            return cast(Dict[str, Union[str, SourceProducer]], result)

        except Exception:
            # Fall back to None if any errors occur
            return None

    @staticmethod
    def _safe_split_header(text: str) -> List[str]:
        """
        Safely split LEEF header by pipe character, respecting escape sequences.

        Args:
            text: Text to split

        Returns:
            List of split values
        """
        result = []
        current = ""
        i = 0
        pipe_count = 0

        while i < len(text):
            # Handle escaped pipes
            if text[i] == "\\" and i + 1 < len(text) and text[i + 1] == "|":
                current += "|"  # Keep the pipe character
                i += 2
            elif text[i] == "|":
                # Normal pipe - field delimiter
                result.append(current)
                current = ""
                pipe_count += 1

                # Stop after the 5th pipe (we expect 5 pipes for LEEF header)
                if pipe_count == 5:
                    result.append(text[i + 1 :])  # Rest is extension
                    break

                i += 1
            else:
                current += text[i]
                i += 1

        # Add final part if we haven't reached 5 pipes
        if pipe_count < 5:
            result.append(current)

        return result

    @staticmethod
    def _parse_extension(extension: str) -> Dict[str, str]:
        """
        Parse LEEF extension format (key=value pairs).

        In LEEF 1.0, key-value pairs in the extension are typically tab-delimited
        but can also be separated by spaces.

        Args:
            extension: The extension string

        Returns:
            Dictionary of parsed key-value pairs
        """
        result = {}

        # Tab is the default delimiter in LEEF 1.0
        delimiter = "\t"
        # If there are no tabs, try using spaces
        if delimiter not in extension:
            delimiter = " "

        pairs = extension.split(delimiter)
        for pair in pairs:
            if not pair.strip():
                continue

            # Find the first equals sign
            equals_pos = pair.find("=")
            if equals_pos > 0:
                key = pair[:equals_pos].strip()
                value = pair[equals_pos + 1 :].strip()

                # Handle escape sequences in values
                value = LEEF1Parser._process_escapes(value)

                result[key] = value

        return result

    @staticmethod
    def _process_escapes(value: str) -> str:
        r"""
        Process escape sequences in LEEF values.

        LEEF escape sequences include:
        - \= for equals sign
        - \| for pipe
        - \\ for backslash
        - \n for newline
        - \r for carriage return
        - \t for tab

        Args:
            value: The value string to process

        Returns:
            String with escape sequences resolved
        """
        i = 0
        result = ""

        while i < len(value):
            if value[i] == "\\" and i + 1 < len(value):
                # Handle escape sequences
                if value[i + 1] == "\\":
                    result += "\\"
                elif value[i + 1] == "=":
                    result += "="
                elif value[i + 1] == "|":
                    result += "|"
                elif value[i + 1] == "n":
                    result += "\n"
                elif value[i + 1] == "r":
                    result += "\r"
                elif value[i + 1] == "t":
                    result += "\t"
                else:
                    # Unknown escape sequence, keep as is
                    result += value[i + 1]
                i += 2
            else:
                result += value[i]
                i += 1

        return result


# For backwards compatibility
def parse_leef1_message(
    message: str,
) -> Optional[Dict[str, Union[str, SourceProducer]]]:
    """Backwards compatibility wrapper for LEEF1Parser.parse()"""
    return LEEF1Parser.parse(message)
