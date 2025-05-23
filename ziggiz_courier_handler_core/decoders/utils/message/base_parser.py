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
Base abstract class for all message parsers.

This module defines the common interface that all message parsers must implement.
"""
# Standard library imports
from abc import ABC, abstractmethod
from typing import Generic, Optional, TypeVar

# Define a generic type for the return value of parse methods
T = TypeVar("T")


class BaseMessageParser(Generic[T], ABC):
    """
    Abstract base class for all message parsers.

    All message parsers should inherit from this class and implement
    the parse method according to their specific format requirements.
    """

    @staticmethod
    @abstractmethod
    def parse(message: str) -> Optional[T]:
        """
        Parse a message string into a structured dictionary.

        Args:
            message: The raw message string to parse

        Returns:
            Dictionary of parsed data, or None if parsing fails or
            the message format is not valid for this parser
        """
