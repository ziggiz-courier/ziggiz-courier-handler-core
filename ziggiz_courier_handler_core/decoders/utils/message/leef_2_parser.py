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
    def parse(message: str) -> Optional[Dict[str, Any]]:
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

            # Strict LEEF 2.0: must have 8 fields (LEEF:2.0|Vendor|Product|Version|EventID|Category|Delim|Extension)
            parts = message.split("|", 7)
            if len(parts) != 8:
                return None  # Not a valid LEEF 2.0 message

            result = {
                "leef_version": parts[0][5:],  # Skip "LEEF:"
                "vendor": parts[1],
                "product": parts[2],
                "version": parts[3],
                "event_id": parts[4],
                "event_category": parts[5],
            }
            # Add SourceProducer instance
            source_producer = SourceProducer(organization=parts[1], product=parts[2])
            result["source_producer"] = source_producer
            result["SourceProducer"] = source_producer

            delim = parts[6]
            extension = parts[7]
            if not extension:
                return None  # Extension cannot be empty

            # Split extension using the delimiter
            pairs = extension.split(delim)
            for pair in pairs:
                if not pair or "=" not in pair:
                    continue
                key, value = pair.split("=", 1)
                value = LEEF2Parser._process_escapes(value)
                result[key] = value

            # Remove legacy event_cat if present (for test compatibility)
            if "event_cat" in result:
                result["event_category"] = result.pop("event_cat")

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
