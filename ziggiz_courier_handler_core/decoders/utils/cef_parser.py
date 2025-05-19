# -*- coding: utf-8 -*-
# # SPDX-License-Identifier: BSL-1.1
# # Copyright (c) 2025 Ziggiz Inc.
# #
# # This file is part of the ziggiz-courier-core-data-processing and is licensed under the
# # Business Source License 1.1. You may not use this file except in
# # compliance with the License. You may obtain a copy of the License at:
# # https://github.com/ziggiz-courier/ziggiz-courier-core-data-processing/blob/main/LICENSE
"""
Utility for parsing Common Event Format (CEF) log message strings.

CEF is an ArcSight-defined format with a specific structure:
CEF:Version|Device Vendor|Device Product|Device Version|Signature ID|Name|Severity|Extension

The Extension part contains key-value pairs in the format key=value.
"""
# Standard library imports
from typing import Dict, List, Optional

# Local/package imports
from ziggiz_courier_handler_core.models.source_producer import SourceProducer


def parse_cef_message(message: str) -> Optional[Dict[str, str]]:
    """
    High-performance parser for Common Event Format (CEF) message strings.
    Handles CEF header and extension fields with proper escaping rules.

    The CEF format is:
    CEF:Version|Device Vendor|Device Product|Device Version|Signature ID|Name|Severity|Extension

    Where Extension contains key=value pairs which may include custom field labels.

    Args:
        message: The raw CEF message string

    Returns:
        Dictionary of parsed key-value pairs from both header and extension fields,
        or None if not a valid CEF format. Uses user-defined labels when available.
    """
    if not message or not message.startswith("CEF:"):
        return None

    # Split the message for initial processing
    try:
        # Split the initial format to get the extension
        parts = _safe_split_header(message[4:])  # Skip "CEF:" prefix

        if len(parts) < 8:
            return None  # Not enough fields

        # Extract header fields
        header_fields = [
            "cef_version",
            "device_vendor",
            "device_product",
            "device_version",
            "signature_id",
            "name",
            "severity",
        ]

        result = {}
        for i, field in enumerate(header_fields):
            result[field] = parts[i]
            
        # Add SourceProducer instance
        result["SourceProducer"] = SourceProducer(
            organization=result["device_vendor"], 
            product=result["device_product"]
        )

        # Process extension (key=value pairs)
        extension = parts[7]
        if extension:
            extension_dict = _parse_extension(extension)
            result.update(extension_dict)

            # Process custom labels
            labels = {}
            for key, value in result.items():
                if key.endswith("Label"):
                    base_field = key[:-5]  # Remove 'Label' suffix
                    if base_field in result:
                        labels[value] = base_field

            # Apply custom labels
            for label, field in labels.items():
                result[label] = result[field]

        return result

    except Exception:
        # Fall back to None if any errors occur
        return None


def _safe_split_header(text: str) -> List[str]:
    """
    Safely split CEF header by pipe character, respecting escape sequences.

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

            # Stop after the 7th pipe (we expect 7 pipes for CEF header)
            if pipe_count == 7:
                result.append(text[i + 1 :])  # Rest is extension
                break

            i += 1
        else:
            current += text[i]
            i += 1

    # Add final part if we haven't reached 7 pipes
    if pipe_count < 7:
        result.append(current)

    return result


def _parse_extension(extension: str) -> Dict[str, str]:
    """
    Parse CEF extension format (key=value pairs).

    Args:
        extension: The extension string

    Returns:
        Dictionary of parsed key-value pairs
    """
    result = {}

    # State variables for parsing
    i = 0

    while i < len(extension):
        # Skip whitespace before key
        while i < len(extension) and extension[i].isspace():
            i += 1

        if i >= len(extension):
            break

        # Parse key
        key_start = i
        while i < len(extension) and extension[i] != "=" and not extension[i].isspace():
            i += 1

        if i >= len(extension) or extension[i] != "=":
            # Not a valid key
            while i < len(extension) and not extension[i].isspace():
                i += 1
            continue

        key = extension[key_start:i]
        i += 1  # Skip '='

        # Parse value
        value = ""
        while i < len(extension):
            # Check for spaces followed by a key=value pattern
            if extension[i].isspace():
                # Save current position
                pos = i
                # Skip spaces
                while i < len(extension) and extension[i].isspace():
                    i += 1

                if i < len(extension):
                    # Look for possible key=value pattern
                    found_key = False
                    j = i
                    while j < len(extension) and not extension[j].isspace():
                        if extension[j] == "=":
                            found_key = True
                            break
                        j += 1

                    if found_key:
                        # This is a new key=value pair, end current value
                        break
                    else:
                        # Not a new key, space is part of the value
                        value += extension[pos:i]
                else:
                    # End of string
                    break
            elif extension[i] == "\\" and i + 1 < len(extension):
                # Handle escape sequences
                if extension[i + 1] == "\\":
                    value += "\\"
                elif extension[i + 1] == "=":
                    value += "="
                elif extension[i + 1] == "|":
                    value += "|"
                elif extension[i + 1] == "n":
                    value += "\n"
                elif extension[i + 1] == "r":
                    value += "\r"
                elif extension[i + 1] == "t":
                    value += "\t"
                elif extension[i + 1] == " " or extension[i + 1] == "s":
                    value += " "
                else:
                    value += extension[i + 1]
                i += 2
            else:
                value += extension[i]
                i += 1

        result[key] = value

    return result
