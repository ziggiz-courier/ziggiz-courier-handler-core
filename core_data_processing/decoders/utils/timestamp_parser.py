# -*- coding: utf-8 -*-
# # SPDX-License-Identifier: BSL-1.1
# # Copyright (c) 2025 Ziggiz Inc.
# #
# # This file is part of the ziggiz-courier-core-data-processing and is licensed under the
# # Business Source License 1.1. You may not use this file except in
# # compliance with the License. You may obtain a copy of the License at:
# # https://github.com/ziggiz-courier/ziggiz-courier-core-data-processing/blob/main/LICENSE
"""Timestamp parsing utilities for various log formats."""

# Standard library imports
import re

from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple


class TimestampParser:
    """Parser for timestamps in various formats.

    This class provides methods to parse timestamps from strings in various formats
    commonly found in log files, including:
    - ISO8601 formats (YYYY-MM-DDThh:mm:ss.sssZ)
    - Common date formats with and without year information
    - Unix epoch timestamps in seconds, milliseconds, microseconds and nanoseconds

    It handles both complete timestamps and timestamps that need to be completed with
    contextual information (like adding the year to timestamps that don't include it).
    """

    @classmethod
    def parse_timestamp(
        cls,
        timestamp_str: str,
        formats: List[str],
        reference_time: Optional[datetime] = None,
    ) -> Optional[datetime]:
        """
        Parse timestamp from input string using specified formats.

        Args:
            timestamp_str: The timestamp string to parse
            formats: List of strptime format strings or format specifier from DATE_FORMATS
            reference_time: Optional reference time for relative date calculations (default: current time)

        Returns:
            A datetime object or None if parsing fails
        """

        # Use current time as reference if not provided
        if reference_time is None:
            reference_time = datetime.now()

        # Handle epoch formats
        if any(fmt.startswith("epoch_") for fmt in formats):
            return cls._parse_epoch_timestamp(timestamp_str)

        # For regular date formats, try each format
        for fmt in formats:
            try:
                # Skip if this is an epoch format (already handled above)
                if fmt.startswith("epoch_"):
                    continue

                dt = datetime.strptime(timestamp_str, fmt)

                # Handle timestamps without year (common in RFC3164 format)
                if "%Y" not in fmt and "%y" not in fmt:
                    # Determine appropriate year (current or previous)
                    month = dt.month
                    current_month = reference_time.month

                    if month > current_month:
                        # If parsed month is later than current, use previous year
                        dt = dt.replace(year=reference_time.year - 1)
                    else:
                        dt = dt.replace(year=reference_time.year)

                # Ensure timestamp has timezone
                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=reference_time.tzinfo or timezone.utc)

                return dt
            except ValueError:
                continue

        return None

    @classmethod
    def _parse_epoch_timestamp(cls, timestamp_str: str) -> Optional[datetime]:
        """
        Parse epoch timestamp formats (seconds, milliseconds, microseconds, nanoseconds).

        Args:
            timestamp_str: The timestamp string in epoch format

        Returns:
            A datetime object in UTC timezone or None if parsing fails
        """
        try:
            # Handle fractional seconds with period or comma separator
            if "." in timestamp_str:
                epoch_str, frac_str = timestamp_str.split(".")

                # Check for epoch_milliseconds format with decimal (1683800645123.456)
                if len(epoch_str) >= 13:
                    # For millisecond timestamps with fraction
                    seconds_val = int(epoch_str[:10])
                    millis = int(epoch_str[10:13])
                    # Convert full fraction to microseconds
                    micros = millis * 1000
                    # Add any additional precision from the fractional part (if needed)
                    micros += int(frac_str[:3].ljust(3, "0"))
                    return datetime.fromtimestamp(seconds_val, tz=timezone.utc).replace(
                        microsecond=micros
                    )
                else:
                    # Normal case for epoch_seconds with fraction
                    epoch_val = int(epoch_str)
                    frac_val = int(
                        frac_str[:6].ljust(6, "0")
                    )  # Normalize to microseconds
                    dt = datetime.fromtimestamp(epoch_val, tz=timezone.utc)
                    return dt.replace(microsecond=frac_val)
            elif "," in timestamp_str:
                epoch_str, frac_str = timestamp_str.split(",")
                epoch_val = int(epoch_str)
                frac_val = int(frac_str[:6].ljust(6, "0"))  # Normalize to microseconds
                dt = datetime.fromtimestamp(epoch_val, tz=timezone.utc)
                return dt.replace(microsecond=frac_val)

            # Handle different epoch precisions
            if len(timestamp_str) >= 19:  # nanoseconds
                epoch_val = int(timestamp_str[:10])
                micros = int(timestamp_str[10:16])
                # For nanosecond precision, round to microsecond
                # The test expects 123457 for 123456789 (rounding up)
                nano_fraction = int(timestamp_str[16:19])
                if nano_fraction >= 500:
                    micros += 1
                return datetime.fromtimestamp(epoch_val, tz=timezone.utc).replace(
                    microsecond=micros
                )
            elif len(timestamp_str) >= 16:  # microseconds
                epoch_val = int(timestamp_str[:10])
                micros = int(timestamp_str[10:16])
                return datetime.fromtimestamp(epoch_val, tz=timezone.utc).replace(
                    microsecond=micros
                )
            elif len(timestamp_str) >= 13:  # milliseconds
                epoch_val = int(timestamp_str[:10])
                millis = int(timestamp_str[10:13])
                return datetime.fromtimestamp(epoch_val, tz=timezone.utc).replace(
                    microsecond=millis * 1000
                )
            else:  # seconds
                epoch_val = int(timestamp_str)
                return datetime.fromtimestamp(epoch_val, tz=timezone.utc)
        except (ValueError, OverflowError):
            return None

    @classmethod
    def try_parse_timestamp(
        cls, message_content: str, format_spec: Dict
    ) -> Tuple[Optional[datetime], Optional[str]]:
        """
        Try to parse a timestamp from the message content using a specific format.

        Args:
            message_content: The message content to parse
            format_spec: Format specification from DATE_FORMATS

        Returns:
            Tuple of (parsed datetime or None, remaining message after timestamp or None)
        """
        if "regex" not in format_spec:
            return None, None

        # Extract timestamp and remaining content using regex
        # Support both string patterns and pre-compiled regex objects
        regex_pattern = format_spec["regex"]
        if isinstance(regex_pattern, str):
            match = re.match(regex_pattern, message_content)
        else:
            match = regex_pattern.match(message_content)

        if not match:
            return None, None

        # Get timestamp string and remaining content
        timestamp_str = match.group("ts")
        remaining = match.group("remaining")

        # Parse the timestamp using format from specification
        timestamp = cls.parse_timestamp(timestamp_str, format_spec["strpfmt"])

        return timestamp, remaining
