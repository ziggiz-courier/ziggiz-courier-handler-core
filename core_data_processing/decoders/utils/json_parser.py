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
Utility for parsing native JSON objects.

This module provides a parser that handles only native JSON objects, not stringified JSON.
"""
# Standard library imports
from typing import Any, Dict, Optional

# Third-party imports
import orjson


def parse_json_message(message: str) -> Optional[Dict[str, Any]]:
    """
    Parse a native JSON message.

    This function attempts to parse the given string as a native JSON object.
    It only processes messages that are already in valid JSON format
    (starting with { and ending with }).

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
        return None
