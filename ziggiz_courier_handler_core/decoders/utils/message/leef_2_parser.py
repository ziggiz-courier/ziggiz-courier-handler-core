# -*- coding: utf-8 -*-
# SPDX-License-Identifier: BSL-1.1
# Copyright (c) 2025 Ziggiz Inc.
#
# This file is part of the ziggiz-courier-core-data-processing and is licensed under the
# Business Source License 1.1. You may not use this file except in
# compliance with the License. You may obtain a copy of the License at:
# https://github.com/ziggiz-courier/ziggiz-courier-core-data-processing/blob/main/LICENSE
"""
Utility for parsing Log Event Extended Format (LEEF) 2.0 log message strings.

LEEF 2.0 is an IBM QRadar-defined format with a specific structure:
LEEF:Version|Vendor|Product|Version|EventID|[EventCategory]|Extension

The Extension part contains key=value pairs in the format key=value.
LEEF 2.0 allows for more format flexibility and encoding options than LEEF 1.0.
"""

# Standard library imports
import logging
import re

from typing import Any, Dict, Optional, Union, cast

# Local/package imports
from ziggiz_courier_handler_core.decoders.utils.message.base_parser import (
    BaseMessageParser,
)
from ziggiz_courier_handler_core.models.source_producer import SourceProducer

logger = logging.getLogger(__name__)


class LEEF2Parser(BaseMessageParser):
    """
    Parser for Log Event Extended Format (LEEF) 2.0 message strings.
    Handles LEEF header and extension fields with proper escaping rules.
    """

    @staticmethod
    def parse(message: str) -> Optional[Dict[str, Union[str, SourceProducer, Any]]]:
        """
        High-performance parser for Log Event Extended Format (LEEF) 2.0 message strings.
        Handles LEEF header and extension fields with proper escaping rules.

        The LEEF 2.0 format is:
        LEEF:Version|Vendor|Product|Version|EventID|[EventCategory]|Extension

        Where Extension contains key=value pairs delimited by tab or another character specified
        in the header, and can include labels for custom field mapping.

        Args:
            message: The raw LEEF message string

        Returns:
            Dictionary of parsed key-value pairs from both header and extension fields,
            or None if not a valid LEEF format.
        """
        if not message or not message.startswith("LEEF:2."):
            return None

        try:
            # Handle all other cases
            # First, split by pipe and handle basic header
            parts = message.split("|", 5)  # Split for main header fields

            if len(parts) < 5:
                return None  # Not enough fields

            result = {
                "leef_version": parts[0][5:],  # Skip "LEEF:"
                "version": parts[3],
                "event_id": parts[4],
            }
            # Store vendor and product in result dict
            result["vendor"] = parts[1]
            result["product"] = parts[2]

            # Add SourceProducer instance
            source_producer = SourceProducer(organization=parts[1], product=parts[2])
            result["source_producer"] = source_producer

            # The rest is either event_category + extension or just extension
            if len(parts) >= 6:
                rest = parts[5]

                # Check if it starts with a key=value pattern (indicating extension with no category)
                if re.match(r"^[^=]+=", rest):
                    # No category, just extension
                    extension = rest
                else:
                    # There might be a category - find the divider between category and extension
                    match = re.search(r"\|([^=]+=)", rest)
                    if match:
                        category_end = match.start()
                        result["event_cat"] = rest[:category_end]
                        extension = rest[category_end + 1 :]  # Skip the pipe
                    else:
                        # No extension found, assume everything is either category or extension
                        if "=" in rest:
                            extension = rest  # Treat as extension
                        else:
                            result["event_cat"] = rest
                            extension = ""

                # Process extension part
                if extension:
                    # Handle tab-delimited key-value pairs
                    if "\t" in extension:
                        pairs = extension.split("\t")
                    else:
                        pairs = extension.split(" ")

                    for pair in pairs:
                        if not pair or "=" not in pair:
                            continue

                        key, value = pair.split("=", 1)
                        # Process escapes
                        value = LEEF2Parser._process_escapes(value)
                        result[key] = value

            # Process custom labels
            labels = {}
            for key, value in list(result.items()):
                if isinstance(value, str) and key.endswith("Label"):
                    base_field = key[:-5]  # Remove 'Label' suffix
                    if base_field in result:
                        labels[value] = base_field

            # Apply custom labels
            for label, field in labels.items():
                result[label] = result[field]

            return cast(Dict[str, Union[str, SourceProducer, Any]], result)

        except Exception as e:
            logger.debug("Error parsing LEEF 2.0 message", extra={"error": str(e)})
            return None

    @staticmethod
    def _process_escapes(value: str) -> str:
        """Process escape sequences in LEEF 2.0 values."""
        value = value.replace("\\\\", "@BACKSLASH@")
        value = value.replace("\\|", "|")
        value = value.replace("\\=", "=")
        value = value.replace("\\n", "\n")
        value = value.replace("\\r", "\r")
        value = value.replace("\\t", "\t")
        value = value.replace("\\s", " ")
        value = value.replace("@BACKSLASH@", "\\")
        return value
