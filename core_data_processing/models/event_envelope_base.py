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
"""Base models for courier data processing."""

# Standard library imports
from datetime import datetime
from typing import Optional

# Third-party imports
from pydantic import BaseModel as PydanticBaseModel

# Local/package imports
# Import BaseEventStructureClassification from the new event_structure_classification.py file
from core_data_processing.models.event_structure_classification import (
    BaseEventStructureClassification,
)


class EventEnvelopeBaseModel(PydanticBaseModel):
    """Base model for all data models.

    This base model provides common fields that are shared across all derived models:
    - timestamp: The timestamp when the event was recorded (often in syslog header or Time Created for Windows events)
                Required field that must be populated by subclasses
    - event_time: An optional timestamp within the event data, used when the event occurred at a time prior to being recorded
                Will only be set if it differs from the timestamp
    - courier_timestamp: When the event was first received by a Courier receiver
                This value should not be modified during processing
    - source_id: An identifier for the source of the data
    - message: The actual message or content (moved from subclasses for consistency)
    """

    timestamp: Optional[
        datetime
    ]  # Optional: When the event was recorded (e.g., in syslog header)
    event_time: Optional[datetime] = (
        None  # Optional: Time when event actually happened if different from timestamp
    )
    courier_timestamp: datetime = (
        datetime.now().astimezone()
    )  # First touch by a Courier receiver, don't modify during processing
    message: Optional[str] = None  # Common message field for all models
    event_data: Optional[dict] = None  # Optional: Additional event data
    structure_classification: Optional[BaseEventStructureClassification] = (
        None  # Optional: Event structure classification metadata
    )

    # Use model_config instead of Config class (Pydantic v2)
    model_config = {
        "frozen": False,  # Make models immutable
        "arbitrary_types_allowed": True,
    }


# For backward compatibility, you may want to add:
BaseModel = EventEnvelopeBaseModel
