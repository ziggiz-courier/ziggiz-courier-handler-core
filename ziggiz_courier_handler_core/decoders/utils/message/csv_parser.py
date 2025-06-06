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
Utility for parsing quoted CSV log message strings.
"""
# Standard library imports
import csv
import io

from typing import Optional

# Third-party imports
# OpenTelemetry imports for tracing
from opentelemetry import trace

# Local/package imports
from ziggiz_courier_handler_core.decoders.utils.message.base_parser import (
    BaseMessageParser,
)

tracer = trace.get_tracer(__name__)


class CSVParser(BaseMessageParser[list[str]]):
    """
    Parser for quoted CSV message strings.
    Handles quoted values and escaped characters.
    """

    @tracer.start_as_current_span("CSVParser.parse")
    @staticmethod
    def parse(message: str) -> Optional[list[str]]:
        """
        High-performance parser for quoted CSV message strings.
        Handles quoted values and escaped characters using the csv module.

        Args:
            message: The raw message string (e.g., 'field1,"field 2, with comma",field3')
        Returns:
            List of parsed fields, or None if the message is empty or not valid CSV.
        """
        if not message:
            return None
        try:
            # Use csv.reader to handle quoted fields and escapes
            reader = csv.reader(io.StringIO(message), skipinitialspace=True)
            fields = next(reader)
            return fields if fields else None
        except Exception:
            return None


# The old function has been removed in favor of the class method
# Use CSVParser.parse() directly
