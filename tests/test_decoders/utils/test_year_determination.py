# -*- coding: utf-8 -*-
# SPDX-License-Identifier: BSL-1.1
# Copyright (c) 2025 Ziggiz Inc.
#
# This file is part of the ziggiz-courier-core-data-processing and is licensed under the
# Business Source License 1.1. You may not use this file except in
# compliance with the License. You may obtain a copy of the License at:
# https://github.com/ziggiz-courier/ziggiz-courier-core-data-processing/blob/main/LICENSE
#
"""Tests for timestamp year determination logic."""

# Standard library imports
from datetime import datetime, timezone

# Third-party imports
import pytest

# Local/package imports
from ziggiz_courier_handler_core.decoders.utils.timestamp_parser import TimestampParser


@pytest.mark.unit
class TestYearDetermination:
    """Test suite for the year determination logic in TimestampParser."""

    def test_current_year_past_date(self):
        """Test that past dates in current year are correctly identified."""
        # Reference time is May 19, 2025
        reference_time = datetime(2025, 5, 19, 12, 0, 0, tzinfo=timezone.utc)

        # Test date is January 15, no year specified
        timestamp_str = "Jan 15 10:30:45"

        # Should use current year since Jan 15 is before May 19 in the same year
        result = TimestampParser.parse_timestamp(
            timestamp_str, ["%b %d %H:%M:%S"], reference_time
        )

        assert result is not None
        assert result.year == 2025
        assert result.month == 1
        assert result.day == 15

    def test_previous_year_future_date(self):
        """Test that future dates are assigned to previous year."""
        # Reference time is May 19, 2025
        reference_time = datetime(2025, 5, 19, 12, 0, 0, tzinfo=timezone.utc)

        # Test date is December 15, no year specified
        timestamp_str = "Dec 15 10:30:45"

        # Should use previous year since Dec 15 is after May 19 in the calendar
        result = TimestampParser.parse_timestamp(
            timestamp_str, ["%b %d %H:%M:%S"], reference_time
        )

        assert result is not None
        assert result.year == 2024
        assert result.month == 12
        assert result.day == 15

    def test_same_day_slightly_earlier(self):
        """Test timestamp from earlier on the same day."""
        # Reference time is May 19, 2025, 12:00
        reference_time = datetime(2025, 5, 19, 12, 0, 0, tzinfo=timezone.utc)

        # Test date is May 19, 10:30:45, no year specified
        timestamp_str = "May 19 10:30:45"

        # Should use current year since it's the same day
        result = TimestampParser.parse_timestamp(
            timestamp_str, ["%b %d %H:%M:%S"], reference_time
        )

        assert result is not None
        assert result.year == 2025
        assert result.month == 5
        assert result.day == 19
        assert result.hour == 10
        assert result.minute == 30
        assert result.second == 45

    def test_near_month_boundary(self):
        """Test timestamp near month boundary."""
        # Reference time is June 1, 2025, 00:30
        reference_time = datetime(2025, 6, 1, 0, 30, 0, tzinfo=timezone.utc)

        # Test date is May 31, 23:45, no year specified (less than 1 hour before reference)
        timestamp_str = "May 31 23:45:00"

        # Should use current year since it's less than 24 hours ago despite month difference
        result = TimestampParser.parse_timestamp(
            timestamp_str, ["%b %d %H:%M:%S"], reference_time
        )

        assert result is not None
        assert result.year == 2025
        assert result.month == 5
        assert result.day == 31
        assert result.hour == 23
        assert result.minute == 45

    def test_dst_transition_spring_forward(self):
        """Test timestamp handling around DST spring forward transition."""
        # Reference time is right after DST spring forward
        reference_time = datetime(2025, 3, 9, 3, 30, 0)

        # Test date is from before the transition
        timestamp_str = "Mar 9 01:30:00"

        result = TimestampParser.parse_timestamp(
            timestamp_str, ["%b %d %H:%M:%S"], reference_time
        )

        assert result is not None
        assert result.year == 2025
        assert result.month == 3
        assert result.day == 9
        assert result.hour == 1
        assert result.minute == 30

    def test_dst_transition_fall_back(self):
        """Test timestamp handling around DST fall back transition."""
        # Reference time is right after DST fall back
        reference_time = datetime(2025, 11, 2, 2, 30, 0)

        # Test date from earlier on the same day, could be ambiguous in standard time handling
        timestamp_str = "Nov 2 01:30:00"

        result = TimestampParser.parse_timestamp(
            timestamp_str, ["%b %d %H:%M:%S"], reference_time
        )

        assert result is not None
        assert result.year == 2025
        assert result.month == 11
        assert result.day == 2
        assert result.hour == 1
        assert result.minute == 30
