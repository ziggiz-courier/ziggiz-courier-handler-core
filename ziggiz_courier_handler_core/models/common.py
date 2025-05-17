# -*- coding: utf-8 -*-
# # SPDX-License-Identifier: BSL-1.1
# # Copyright (c) 2025 Ziggiz Inc.
# #
# # This file is part of the ziggiz-courier-core-data-processing and is licensed under the
# # Business Source License 1.1. You may not use this file except in
# # compliance with the License. You may obtain a copy of the License at:
# # https://github.com/ziggiz-courier/ziggiz-courier-core-data-processing/blob/main/LICENSE
"""Common event models."""

# Standard library imports
from typing import Dict, List

# Local/package imports
from ziggiz_courier_handler_core.models.event_envelope_base import BaseModel


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
