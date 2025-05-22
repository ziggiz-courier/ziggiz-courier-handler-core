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
Utility for parsing key=value log message strings (e.g., FortiGate, generic log formats).
"""
# Standard library imports
from typing import Dict, Optional

# Local/package imports
from ziggiz_courier_handler_core.decoders.utils.message.base_parser import (
    BaseMessageParser,
)


class KVParser(BaseMessageParser):
    """
    Parser for key=value message strings.
    Handles quoted values and escaped characters.
    """

    @staticmethod
    def parse(message: str) -> Optional[Dict[str, str]]:
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
