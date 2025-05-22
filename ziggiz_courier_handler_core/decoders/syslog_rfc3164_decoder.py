# -*- coding: utf-8 -*-
# SPDX-License-Identifier: BSL-1.1
# Copyright (c) 2025 Ziggiz Inc.
#
# This file is part of the ziggiz-courier-core-data-processing and is licensed under the
# Business Source License 1.1. You may not use this file except in
# compliance with the License. You may obtain a copy of the License at:
# https://github.com/ziggiz-courier/ziggiz-courier-core-data-processing/blob/main/LICENSE
#
"""Syslog RFC3164 (BSD-style) decoder implementation."""

# Standard library imports
import re

from datetime import datetime
from typing import List, Optional, Pattern, Tuple, TypedDict

# Local/package imports
from ziggiz_courier_handler_core.decoders.base import Decoder
from ziggiz_courier_handler_core.decoders.message_decoder_plugins import (
    get_message_decoders,
)
from ziggiz_courier_handler_core.decoders.syslog_rfc_base_decoder import (
    SyslogRFCBaseDecoder,
)
from ziggiz_courier_handler_core.decoders.utils.timestamp_parser import TimestampParser
from ziggiz_courier_handler_core.models.syslog_rfc3164 import SyslogRFC3164Message

# Compile the regex pattern for parsing hostname, app name, proc id and message at module level
TAG_PATTERN = re.compile(
    r"^(?:(?P<host>[A-Fa-f0-9:]{6,}|[A-Za-z0-9\-\.]+) )?(?:(?P<app_name>[^\[ ]+)?(?:\[(?P<procid>[^\]]+)\])?: )?(?P<remaining>.*)"
)

plugins = get_message_decoders(SyslogRFC3164Message)


class DateFormatSpec(TypedDict):
    """Type definition for date format specifications."""

    strpfmt: List[str]
    regex: Pattern


class SyslogRFC3164Decoder(Decoder[SyslogRFC3164Message]):
    """Decoder for syslog messages following RFC3164 format (BSD-style syslog).

    This decoder handles the simple format: <PRI>MESSAGE and the standard format:
    <PRI>TIMESTAMP HOSTNAME TAG MESSAGE

    It can also handle variations where there are spaces after the priority bracket.

    This implementation reuses SyslogRFCBaseDecoder for optimized PRI extraction.
    """

    # strpfmt for known date formats used in RFC3164 and similar logs
    # The regex patterns are pre-compiled to improve performance
    # The strptime formats are used to parse the date strings
    DATE_FORMATS: List[DateFormatSpec] = [
        {
            "strpfmt": ["%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%dT%H:%M:%SZ"],
            "regex": re.compile(
                r"^(?P<ts>(?P<date>(?P<year>2\d{3})-(?P<month>\d{2})-(?P<day>\d{2}))T(?P<time>(?P<hour>[0-2]\d):(?P<minute>[0-5]\d):(?P<second>[0-5]\d)(?:\.(?P<microsecond>\d{6}))?(?P<tz>[Zz0-9+\-:]+))) (?P<remaining>.*)"
            ),
        },
        {
            "strpfmt": ["%Y %b %d %H:%M:%S.%f", "%Y %b %d %H:%M:%S"],
            "regex": re.compile(
                r"^(?P<ts>(?P<date>(?P<year>2\d{3}) (?P<month>[JFMASOND][a-z]{2}) (?P<day>[ 0-3]\d)) (?P<time>(?P<hour>[0-2]\d):(?P<minute>[0-5]\d):(?P<second>[0-5]\d)(?:\.(?P<microsecond>\d{6}))?)) (?P<remaining>.*)"
            ),
        },
        {
            "strpfmt": ["%b %d %H:%M:%S.%f %Y", "%b %d %H:%M:%S %Y"],
            "regex": re.compile(
                r"^(?P<ts>(?P<date>(?P<month>[JFMASOND][a-z]{2}) (?P<day>[ 0-3]\d)) (?P<time>(?P<hour>[0-2]\d):(?P<minute>[0-5]\d):(?P<second>[0-5]\d)(?:\.(?P<microsecond>\d{6}))?) (?P<year>2\d{3})) (?P<remaining>.*)"
            ),
        },
        {
            "strpfmt": [
                "%b %d %Y %H:%M:%S.%f",
                "%b %d %Y %H:%M:%S",
                "%b %d %H:%M:%S.%f",
                "%b %d %H:%M:%S",
            ],
            "regex": re.compile(
                r"^(?P<ts>(?P<date>(?P<month>[JFMASOND][a-z]{2}) (?P<day>[ 0-3]\d)(?: (?P<year>20\d{2}))?) (?P<time>(?P<hour>[0-2]\d):(?P<minute>[0-5]\d):(?P<second>[0-5]\d)(?:\.(?P<microsecond>\d{6}))?)) (?P<remaining>.*)"
            ),
        },
        # Unix epoch formats - seconds, milliseconds, microseconds, nanoseconds
        # Format is special and handled directly in parse_timestamp for epoch formats
        {
            "strpfmt": [
                "epoch_seconds",
                "epoch_milliseconds",
                "epoch_microseconds",
                "epoch_nanoseconds",
            ],
            "regex": re.compile(
                r"^(?P<ts>(?P<epoch>\d{10,19})(?:(?P<sep>[.,])(?P<frac>\d{1,9}))?) (?P<remaining>.*)"
            ),
        },
    ]

    # Common English words that shouldn't be considered hostnames when appearing at the start
    COMMON_WORDS = {
        "this",
        "these",
        "that",
        "those",
        "the",
        "test",
        "testing",
        "invalid",
        "error",
        "warning",
        "trace",
        "debug",
        "info",
        "notice",
        "alert",
        "critical",
        "emergency",
        "panic",
    }

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

    def _parse_timestamp(
        self,
        timestamp_str: str,
        formats: List[str],
        reference_time: Optional[datetime] = None,
    ) -> Optional[datetime]:
        """
        Parse timestamp using the TimestampParser utility class.

        This method is a wrapper around the TimestampParser utility
        to maintain backward compatibility with test cases.

        Args:
            timestamp_str: The timestamp string to parse
            formats: List of strptime format strings or format specifier
            reference_time: Optional reference time for relative date calculations

        Returns:
            A datetime object or None if parsing fails
        """
        return TimestampParser.parse_timestamp(timestamp_str, formats, reference_time)

    def _try_parse_timestamp(
        self, message_content: str
    ) -> Tuple[Optional[datetime], Optional[str]]:
        """Try to parse a timestamp from the message content.

        This method tries all available timestamp formats and stops at the first successful parse.
        The function uses regex patterns in format_spec to extract the timestamp string and
        remaining message, then parses the timestamp string using the format specification.

        Args:
            message_content: The message content to parse

        Returns:
            Tuple of (timestamp, remaining message after timestamp)
            If no timestamp is found, returns (None, original message_content)
        """
        # Try to parse timestamp using all available formats
        for format_spec in self.DATE_FORMATS:
            # Extract timestamp and remaining content using regex
            regex: Pattern = format_spec["regex"]
            match = regex.match(message_content)
            if match:
                # Get timestamp string and remaining content
                timestamp_str = match.group("ts")
                remaining = match.group("remaining")

                # Parse the timestamp using format from specification
                strpfmt: List[str] = format_spec["strpfmt"]
                timestamp = self._parse_timestamp(timestamp_str, strpfmt)
                if timestamp is not None:
                    return timestamp, remaining

        return None, message_content

    def _parse_hostname_tag(
        self, message: str
    ) -> Tuple[Optional[str], Optional[str], Optional[str], str]:
        """Parse hostname, app name (tag), and proc_id from the message.

        Args:
            message: The message content after timestamp extraction

        Returns:
            Tuple of (hostname, app_name, proc_id, remaining message)
        """
        match = TAG_PATTERN.match(message)
        if not match:
            return None, None, None, message

        hostname = match.group("host").lower() if match.group("host") else None
        app_name = match.group("app_name")
        proc_id = match.group("procid")
        message_content = match.group("remaining")

        # Basic validation - if hostname is a common word, it's probably not a hostname
        # this is a naive check and should be improved for production use
        if (
            app_name is None
            and proc_id is None
            and hostname is not None
            and message.startswith(f"{hostname} {message_content}")
        ):
            if hostname.lower() in self.COMMON_WORDS:
                return None, None, None, message

        return hostname, app_name, proc_id, message_content

    def decode(
        self, raw_data: str, parsing_cache: Optional[dict] = None
    ) -> Optional[SyslogRFC3164Message]:  # Updated return type to include None
        """
        Decode a syslog RFC3164 message from raw string data.

        The decoder supports the following format variations:
        - <PRI>MESSAGE
        - <PRI> MESSAGE (with space after the priority)
        - <PRI>TIMESTAMP HOSTNAME TAG MESSAGE
        - <PRI> TIMESTAMP HOSTNAME TAG MESSAGE (with space after the priority)

        Args:
            raw_data: The raw syslog message as string
            parsing_cache: A dictionary for caching parsing results
            **kwargs: Additional keyword arguments for extensibility

        Returns:
            A SyslogRFC3164Message instance representing the decoded data, or None if decoding fails
        """

        # Initialize default values for the model
        timestamp = None
        hostname = None
        app_name = None  # tag in RFC3164 terminology
        proc_id = None  # content after tag in RFC3164 terminology

        try:
            # Extract PRI and message content using the reusable method
            pri, message_content = SyslogRFCBaseDecoder.extract_pri_and_content(
                raw_data
            )

            # Try to parse timestamp
            timestamp, remaining = self._try_parse_timestamp(message_content)

            if timestamp is not None and remaining is not None:
                hostname, app_name, proc_id, message_content = self._parse_hostname_tag(
                    remaining
                )
            else:
                hostname = app_name = proc_id = None

            # Create the RFC3164 message model
            if (
                timestamp is None
                and hostname is None
                and app_name is None
                and proc_id is None
            ):
                # This is a simple <PRI>MESSAGE format that doesn't match RFC3164
                return None

            model: SyslogRFC3164Message = SyslogRFC3164Message.from_priority(
                pri,
                message=message_content,
                timestamp=timestamp,
                hostname=hostname,
                app_name=app_name,
                proc_id=proc_id,
            )

            # --- Plugin-based event_data decoding ---
            self._run_message_decoder_plugins(
                model, SyslogRFC3164Message, parsing_cache
            )

            return model
        except ValueError:
            # Return None instead of raising an exception
            return None
        except Exception:
            # Return None for any other exceptions
            return None
