# -*- coding: utf-8 -*-
# SPDX-License-Identifier: BSL-1.1
# Copyright (c) 2025 Ziggiz Inc.
#
# This file is part of the ziggiz-courier-core-data-processing and is licensed under the
# Business Source License 1.1. You may not use this file except in
# compliance with the License. You may obtain a copy of the License at:
# https://github.com/ziggiz-courier/ziggiz-courier-core-data-processing/blob/main/LICENSE
#

"""Syslog RFC5424 decoder implementation."""

# Standard library imports
import re

from datetime import datetime
from typing import Dict, Optional

# Local/package imports
from ziggiz_courier_handler_core.decoders.base import Decoder
from ziggiz_courier_handler_core.decoders.syslog_rfc_base_decoder import (
    SyslogRFCBaseDecoder,
)
from ziggiz_courier_handler_core.models.syslog_rfc5424 import SyslogRFC5424Message


class SyslogRFC5424Decoder(Decoder[SyslogRFC5424Message]):
    """Decoder for syslog messages following RFC5424 format."""

    # Regex for parsing standard syslog format (after PRI extraction)
    # This pattern starts after the PRI field has been extracted
    MESSAGE_PATTERN = re.compile(
        r"^(?P<version>1) (?P<timestamp>\S+) "
        r"(?P<hostname>\S+) (?P<app_name>\S+) (?P<proc_id>\S+) "
        r"(?P<msg_id>\S+) (?P<structured_data>(?:\[.+?\])+|-) (?P<message>.*)"
    )

    def __init__(
        self,
        connection_cache: Optional[dict] = None,
        event_parsing_cache: Optional[dict] = None,
    ):
        """
        Initialize the decoder.

        Args:
            connection_cache: Optional dictionary for caching connections
            event_parsing_cache: Optional dictionary for caching event parsing results
        """
        super().__init__(
            connection_cache=connection_cache, event_parsing_cache=event_parsing_cache
        )
        self._base_decoder = SyslogRFCBaseDecoder(
            connection_cache=connection_cache, event_parsing_cache=event_parsing_cache
        )

    def decode(
        self, raw_data: str, parsing_cache: Optional[dict] = None
    ) -> Optional[SyslogRFC5424Message]:
        """
        Decode a syslog RFC5424 message from raw string data.

        Args:
            raw_data: The raw syslog message as string
            parsing_cache: Optional dictionary for caching parsing data

        Returns:
            A SyslogRFC5424Message instance representing the decoded data, or None if decoding fails
        """
        try:
            # Extract PRI and message content using the reusable method
            pri, message_content = SyslogRFCBaseDecoder.extract_pri_and_content(
                raw_data
            )

            # Parse the rest of the message using the message pattern
            match = self.MESSAGE_PATTERN.match(message_content)
            if not match:
                # Return None instead of raising an exception
                return None

            data = match.groupdict()
            structured_data = self._parse_structured_data(data["structured_data"])

            # Create RFC5424 message with extracted data using from_priority
            model: SyslogRFC5424Message = SyslogRFC5424Message.from_priority(
                pri,
                timestamp=self._parse_timestamp(data["timestamp"]),
                hostname=self._normalize_hostname(data["hostname"]),
                app_name=None if data["app_name"] == "-" else data["app_name"],
                proc_id=None if data["proc_id"] == "-" else data["proc_id"],
                msg_id=None if data["msg_id"] == "-" else data["msg_id"],
                message=data["message"],
                structured_data=structured_data,
            )

            # --- Plugin-based event_data decoding ---
            self._run_message_decoder_plugins(
                model, SyslogRFC5424Message, parsing_cache
            )
            return model
        except ValueError:
            # Return None instead of raising an exception
            return None

    def _parse_timestamp(self, timestamp: str) -> datetime:
        """
        Parse the timestamp from a syslog message.

        Args:
            timestamp: The timestamp string from syslog message

        Returns:
            A datetime object
        """
        # Handle nil value "-" by using current time in local timezone
        if timestamp == "-":
            return datetime.now().astimezone()

        # For standard ISO8601 format timestamps
        return datetime.fromisoformat(timestamp)

    def _normalize_hostname(self, hostname: str) -> Optional[str]:
        """
        Normalize hostname values according to RFC5424 requirements.

        Args:
            hostname: The hostname from syslog message

        Returns:
            Normalized hostname or None for nil value
        """
        # Handle nil value
        if hostname == "-":
            return None

        # Convert hostname to lowercase as per RFC
        return hostname.lower()

    def _parse_structured_data(
        self, structured_data: str
    ) -> Optional[Dict[str, Dict[str, str]]]:
        """
        Parse structured data from a syslog message.

        Args:
            structured_data: The structured_data part of the syslog message

        Returns:
            A dictionary of structured data or None if no structured data
        """
        if structured_data == "-":
            return None

        # This is a simplified parser and would need to be more robust for production
        result = {}
        # Remove outer brackets and split by closing bracket
        elements = structured_data.strip("[]").split("][")

        for element in elements:
            if not element:
                continue

            # First word is the id
            parts = element.split(" ", 1)
            if len(parts) < 2:
                continue

            sd_id = parts[0]
            sd_params_str = parts[1]

            # Parse params
            params = {}
            param_matches = re.finditer(r'(\S+)="([^"]*)"', sd_params_str)
            for match in param_matches:
                params[match.group(1)] = match.group(2)

            result[sd_id] = params

        return result
