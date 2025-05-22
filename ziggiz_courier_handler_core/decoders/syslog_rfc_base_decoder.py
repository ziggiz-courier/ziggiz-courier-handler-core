# -*- coding: utf-8 -*-
# SPDX-License-Identifier: BSL-1.1
# Copyright (c) 2025 Ziggiz Inc.
#
# This file is part of the ziggiz-courier-core-data-processing and is licensed under the
# Business Source License 1.1. You may not use this file except in
# compliance with the License. You may obtain a copy of the License at:
# https://github.com/ziggiz-courier/ziggiz-courier-core-data-processing/blob/main/LICENSE
#

"""Syslog RFC Base decoder implementation for basic PRI extraction."""

# Standard library imports
from typing import Optional, Tuple

# Local/package imports
from ziggiz_courier_handler_core.decoders.base import Decoder
from ziggiz_courier_handler_core.models.syslog_rfc_base import SyslogRFCBaseModel


class SyslogRFCBaseDecoder(Decoder[SyslogRFCBaseModel]):
    """Decoder for basic syslog messages with only PRI field extraction.

    This decoder handles the simple format: <PRI>MESSAGE and extracts only the
    priority value and the message content, returning a basic SyslogRFCBaseModel.

    Unlike more specific RFC format decoders (RFC3164, RFC5424), this decoder
    makes no attempt to parse timestamp, hostname, or other structured fields,
    and simply returns the message starting after the first non-space following
    the closing angle bracket.

    This implementation uses character-by-character parsing for optimized performance
    compared to regex-based parsing.
    """

    @staticmethod
    def extract_pri_and_content(raw_data: str) -> Tuple[Optional[str], str]:
        """
        Extract the PRI value and remaining message content from a syslog message.

        Args:
            raw_data: The raw syslog message as string

        Returns:
            Tuple of (pri, message_content)

        Raises:
            ValueError: If the raw_data does not match basic syslog format
        """
        if not raw_data or len(raw_data) < 3:  # Needs at least <>x
            raise ValueError(f"Invalid syslog format: {raw_data}")

        # Ensure the message starts with <
        if raw_data[0] != "<":
            raise ValueError(f"Invalid syslog format: {raw_data}")

        # Find closing bracket
        close_bracket_pos = raw_data.find(">")
        if close_bracket_pos == -1:
            raise ValueError(f"Invalid syslog format: {raw_data}")

        # Extract PRI value (everything between < and >)
        pri = raw_data[1:close_bracket_pos]

        # Check for malformed PRI with spaces (like "< >" case)
        if " " in pri:
            raise ValueError(f"Invalid syslog format: {raw_data}")

        # Handle empty PRI
        if pri.strip() == "":
            pri = None

        # Find first non-whitespace after closing bracket
        message_start = close_bracket_pos + 1
        message_len = len(raw_data)

        while message_start < message_len and raw_data[message_start].isspace():
            message_start += 1

        # Extract message (everything after the closing > and any whitespace)
        message = raw_data[message_start:] if message_start < message_len else ""
        return pri, message

    def decode(
        self, raw_data: str, parsing_cache: Optional[dict] = None
    ) -> SyslogRFCBaseModel:
        """
        Decode a syslog message by extracting the PRI field and remaining message.

        This optimized decoder extracts the priority value and returns the message
        content starting with the first non-space character after the closing
        angle bracket, using character-by-character parsing instead of regex.

        Args:
            raw_data: The raw syslog message as string
            parsing_cache: Optional dictionary for caching parsing data

        Returns:
            A SyslogRFCBaseModel instance representing the decoded data

        Raises:
            ValueError: If the raw_data does not match basic syslog format
        """
        if parsing_cache is None:
            parsing_cache = self.event_parsing_cache

        pri, message = self.extract_pri_and_content(raw_data)

        # Create the model using from_priority which handles validation
        model = SyslogRFCBaseModel.from_priority(pri, message=message)

        self._run_message_decoder_plugins(model, SyslogRFCBaseModel, parsing_cache)
        return model
