# -*- coding: utf-8 -*-
# # SPDX-License-Identifier: BSL-1.1
# # Copyright (c) 2025 Ziggiz Inc.
# #
# # This file is part of the ziggiz-courier-core-data-processing and is licensed under the
# # Business Source License 1.1. You may not use this file except in
# # compliance with the License. You may obtain a copy of the License at:
# # https://github.com/ziggiz-courier/ziggiz-courier-core-data-processing/blob/main/LICENSE
"""Tests for timestamp parsing utilities."""

# Standard library imports
from datetime import datetime, timezone

# Third-party imports
import pytest

# Local/package imports
from core_data_processing.decoders.utils.timestamp_parser import TimestampParser

# Module-level test cases for timestamp parsing
TIMESTAMP_PARSE_CASES = [
    # (timestamp_str, formats, expected_attrs, id, reference_time)
    (
        "2023-04-15T10:30:45Z",
        ["%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%dT%H:%M:%SZ"],
        {
            "year": 2023,
            "month": 4,
            "day": 15,
            "hour": 10,
            "minute": 30,
            "second": 45,
            "microsecond": 0,
            "tzinfo": True,
        },
        "with_year",
        None,
    ),
    (
        "2023-04-15T10:30:45.123456Z",
        ["%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%dT%H:%M:%SZ"],
        {
            "year": 2023,
            "month": 4,
            "day": 15,
            "hour": 10,
            "minute": 30,
            "second": 45,
            "microsecond": 123456,
            "tzinfo": True,
        },
        "with_microseconds",
        None,
    ),
    (
        "2023 Apr 15 10:30:45",
        ["%Y %b %d %H:%M:%S.%f", "%Y %b %d %H:%M:%S"],
        {
            "year": 2023,
            "month": 4,
            "day": 15,
            "hour": 10,
            "minute": 30,
            "second": 45,
            "tzinfo": True,
        },
        "year_first",
        None,
    ),
    (
        "2023 Apr 15 10:30:45.123456",
        ["%Y %b %d %H:%M:%S.%f", "%Y %b %d %H:%M:%S"],
        {
            "year": 2023,
            "month": 4,
            "day": 15,
            "hour": 10,
            "minute": 30,
            "second": 45,
            "microsecond": 123456,
            "tzinfo": True,
        },
        "year_first_microseconds",
        None,
    ),
    (
        "Apr 15 10:30:45 2023",
        ["%b %d %H:%M:%S.%f %Y", "%b %d %H:%M:%S %Y"],
        {
            "year": 2023,
            "month": 4,
            "day": 15,
            "hour": 10,
            "minute": 30,
            "second": 45,
            "tzinfo": True,
        },
        "year_last",
        None,
    ),
    (
        "Apr 15 10:30:45.123456 2023",
        ["%b %d %H:%M:%S.%f %Y", "%b %d %H:%M:%S %Y"],
        {
            "year": 2023,
            "month": 4,
            "day": 15,
            "hour": 10,
            "minute": 30,
            "second": 45,
            "microsecond": 123456,
            "tzinfo": True,
        },
        "year_last_microseconds",
        None,
    ),
    (
        "Apr 15 2023 10:30:45",
        ["%b %d %Y %H:%M:%S.%f", "%b %d %Y %H:%M:%S"],
        {
            "year": 2023,
            "month": 4,
            "day": 15,
            "hour": 10,
            "minute": 30,
            "second": 45,
            "tzinfo": True,
        },
        "month_first_with_year",
        None,
    ),
    (
        "Apr 15 2023 10:30:45.123456",
        ["%b %d %Y %H:%M:%S.%f", "%b %d %Y %H:%M:%S"],
        {
            "year": 2023,
            "month": 4,
            "day": 15,
            "hour": 10,
            "minute": 30,
            "second": 45,
            "microsecond": 123456,
            "tzinfo": True,
        },
        "month_first_with_year_microseconds",
        None,
    ),
    # Without year, using current year
    (
        "Apr 15 10:30:45",
        ["%b %d %H:%M:%S.%f", "%b %d %H:%M:%S"],
        {"year": 2025, "month": 4, "day": 15, "hour": 10, "minute": 30, "second": 45},
        "without_year_current_year",
        datetime(2025, 5, 15, 12, 0, 0),
    ),
    # Without year, using previous year
    (
        "Dec 15 10:30:45",
        ["%b %d %H:%M:%S.%f", "%b %d %H:%M:%S"],
        {"year": 2024, "month": 12, "day": 15, "hour": 10, "minute": 30, "second": 45},
        "without_year_previous_year",
        datetime(2025, 1, 15, 12, 0, 0),
    ),
    # Unix epoch seconds
    (
        "1683800645",
        ["epoch_seconds"],
        {
            "year": 2023,
            "month": 5,
            "day": 11,
            "hour": 10,
            "minute": 24,
            "second": 5,
            "tzinfo": timezone.utc,
        },
        "epoch_seconds",
        None,
    ),
    (
        "1683800645.123",
        ["epoch_seconds"],
        {
            "year": 2023,
            "month": 5,
            "day": 11,
            "hour": 10,
            "minute": 24,
            "second": 5,
            "microsecond": 123000,
            "tzinfo": timezone.utc,
        },
        "epoch_seconds_fraction",
        None,
    ),
    (
        "1683800645,123",
        ["epoch_seconds"],
        {
            "year": 2023,
            "month": 5,
            "day": 11,
            "hour": 10,
            "minute": 24,
            "second": 5,
            "microsecond": 123000,
            "tzinfo": timezone.utc,
        },
        "epoch_seconds_comma",
        None,
    ),
    (
        "1683800645123",
        ["epoch_milliseconds"],
        {
            "year": 2023,
            "month": 5,
            "day": 11,
            "hour": 10,
            "minute": 24,
            "second": 5,
            "microsecond": 123000,
            "tzinfo": timezone.utc,
        },
        "epoch_milliseconds",
        None,
    ),
    (
        "1683800645123.456",
        ["epoch_milliseconds"],
        {
            "year": 2023,
            "month": 5,
            "day": 11,
            "hour": 10,
            "minute": 24,
            "second": 5,
            "microsecond": 123456,
            "tzinfo": timezone.utc,
        },
        "epoch_milliseconds_fraction",
        None,
    ),
    (
        "1683800645123456",
        ["epoch_microseconds"],
        {
            "year": 2023,
            "month": 5,
            "day": 11,
            "hour": 10,
            "minute": 24,
            "second": 5,
            "microsecond": 123456,
            "tzinfo": timezone.utc,
        },
        "epoch_microseconds",
        None,
    ),
    (
        "1683800645123456789",
        ["epoch_nanoseconds"],
        {
            "year": 2023,
            "month": 5,
            "day": 11,
            "hour": 10,
            "minute": 24,
            "second": 5,
            "microsecond": 123457,
            "tzinfo": timezone.utc,
        },
        "epoch_nanoseconds",
        None,
    ),
]


@pytest.mark.unit
class TestTimestampParser:
    """Test suite for the TimestampParser utility."""

    @pytest.mark.parametrize(
        "timestamp_str, formats, expected_attrs, _id, reference_time",
        TIMESTAMP_PARSE_CASES,
        ids=[tc[3] for tc in TIMESTAMP_PARSE_CASES],
    )
    def test_parse_timestamp_common(
        self, timestamp_str, formats, expected_attrs, _id, reference_time
    ):
        if reference_time is not None:
            result = TimestampParser.parse_timestamp(
                timestamp_str, formats, reference_time=reference_time
            )
        else:
            result = TimestampParser.parse_timestamp(timestamp_str, formats)
        if expected_attrs is None:
            assert result is None
        else:
            assert result is not None
            for attr, expected in expected_attrs.items():
                if attr == "tzinfo":
                    if expected is timezone.utc:
                        assert result.tzinfo == timezone.utc
                    else:
                        assert (result.tzinfo is not None) == expected
                elif attr == "microsecond_rounded":
                    # Special case for millisecond rounding
                    assert (
                        round(result.microsecond, -3) == expected_attrs["microsecond"]
                    )
                else:
                    assert getattr(result, attr) == expected

    def test_try_parse_timestamp(self):
        """Test the try_parse_timestamp method."""
        message = "2023-04-15T10:30:45Z This is the rest of the message"
        format_spec = {
            "strpfmt": ["%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%dT%H:%M:%SZ"],
            "regex": r"^(?P<ts>(?P<date>(?P<year>2\d{3})-(?P<month>\d{2})-(?P<day>\d{2}))T(?P<time>(?P<hour>[0-2]\d):(?P<minute>[0-5]\d):(?P<second>[0-5]\d)(?:\.(?P<microsecond>\d{6}))?(?P<tz>[Zz0-9+\-:]+))) (?P<remaining>.*)",
        }

        timestamp, remaining = TimestampParser.try_parse_timestamp(message, format_spec)

        assert timestamp is not None
        assert timestamp.year == 2023
        assert timestamp.month == 4
        assert timestamp.day == 15
        assert timestamp.hour == 10
        assert timestamp.minute == 30
        assert timestamp.second == 45
        assert remaining == "This is the rest of the message"
