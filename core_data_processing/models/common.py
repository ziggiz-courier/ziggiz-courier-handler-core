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
"""Common event models."""

# Standard library imports
from typing import Dict, List

# Local/package imports
from core_data_processing.models.event_envelope_base import BaseModel


class CommonEvent(BaseModel):
    """Common event model that can be used across different systems.

    This model stores both the timestamp when the event was recorded (timestamp)
    and when the event actually occurred (event_time) if they differ.

    The timestamp field is required for all events. In many cases,
    the timestamp and event_time will be the same.
    """

    event_id: str
    event_type: str
    source_system: str
    source_component: str
    severity: str
    tags: List[str] = []
    attributes: Dict[str, str] = {}
