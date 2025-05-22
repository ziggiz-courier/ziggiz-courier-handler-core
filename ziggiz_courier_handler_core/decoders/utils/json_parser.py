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
Utility for parsing native JSON objects.

This module provides a parser that handles only native JSON objects, not stringified JSON.
It also handles JSON with escaped control characters that might break standard parsing.
"""
# Standard library imports
import json

from typing import Any, Dict, Optional

# Third-party imports
import orjson


def parse_json_message(message: str) -> Optional[Dict[str, Any]]:
    """
    Parse a native JSON message.

    This function attempts to parse the given string as a native JSON object.
    It only processes messages that are already in valid JSON format
    (starting with { and ending with }). It can also handle JSON with escaped
    control characters like \\r\\n, and escaped quotes.

    Args:
        message: The raw message that must be a native JSON object

    Returns:
        Dictionary representing the parsed JSON structure, or None if
        parsing fails or if the input is not valid JSON
    """
    if not message:
        return None

    # Check if the message appears to be a native JSON object (starts with { and ends with })
    message = message.strip()
    if not (message.startswith("{") and message.endswith("}")):
        return None

    # Attempt JSON parsing
    try:
        return orjson.loads(message)
    except (orjson.JSONDecodeError, ValueError, TypeError):
        # First attempt failed, try fixing common issues
        try:
            # Try using the standard library json which is more forgiving
            return json.loads(message)
        except (json.JSONDecodeError, ValueError, TypeError):
            # If that fails too, try replacing literal \r\n with actual line breaks
            # and handle escaped quotes by using a raw string equivalent
            try:
                # Handle \r\n and other control chars
                fixed_message = message.replace("\\r\\n", "\r\n")
                fixed_message = fixed_message.replace("\\n", "\n")
                fixed_message = fixed_message.replace('\\"', '"')
                fixed_message = fixed_message.replace("\\/", "/")
                fixed_message = fixed_message.replace("\\\\", "\\")
                return orjson.loads(fixed_message)
            except (orjson.JSONDecodeError, ValueError, TypeError):
                return None
