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
Utility for parsing key=value log message strings (e.g., FortiGate, generic log formats).
"""
# Standard library imports
from typing import Dict, Optional


def parse_kv_message(message: str) -> Optional[Dict[str, str]]:
    """
    High-performance parser for key=value message strings.
    Avoids regex for speed. Handles quoted values and escaped characters.

    Args:
        message: The raw message string (key1=val1 key2="val 2" ...)
    Returns:
        Dictionary of parsed key-value pairs, or None if not a key=value format.
    """
    if not message or "=" not in message:
        return None
    result = {}
    length = len(message)
    i = 0
    while i < length:
        # Skip whitespace
        while i < length and message[i].isspace():
            i += 1
        # Parse key
        key_start = i
        while i < length and message[i] != "=" and not message[i].isspace():
            i += 1
        key = message[key_start:i]
        if not key or i >= length or message[i] != "=":
            # Not a valid key=value
            while i < length and message[i] != " ":
                i += 1
            continue
        i += 1  # skip '='
        # Parse value
        if i < length and message[i] == '"':
            # Quoted value
            i += 1
            value = ""
            while i < length:
                if message[i] == '"':
                    break
                if message[i] == "\\" and i + 1 < length:
                    value += message[i + 1]
                    i += 2
                else:
                    value += message[i]
                    i += 1
            i += 1  # skip closing quote
        else:
            value_start = i
            while i < length and not message[i].isspace():
                i += 1
            value = message[value_start:i]
        result[key] = value
    return result if result else None
