# -*- coding: utf-8 -*-
# Copyright (C) 2025 ziggiz
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
Utility for parsing quoted CSV log message strings.
"""
# Standard library imports
import csv
import io

from typing import List, Optional


def parse_quoted_csv_message(message: str) -> Optional[List[str]]:
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
