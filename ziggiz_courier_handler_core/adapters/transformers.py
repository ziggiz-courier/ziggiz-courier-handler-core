# -*- coding: utf-8 -*-
# SPDX-License-Identifier: BSL-1.1
# Copyright (c) 2025 Ziggiz Inc.
#
# This file is part of the ziggiz-courier-core-data-processing and is licensed under the
# Business Source License 1.1. You may not use this file except in
# compliance with the License. You may obtain a copy of the License at:
# https://github.com/ziggiz-courier/ziggiz-courier-core-data-processing/blob/main/LICENSE
#
"""Adapter for transforming syslog messages to common event format."""

# Standard library imports
import uuid

from typing import Dict

# Local/package imports
from ziggiz_courier_handler_core.adapters.base import Adapter
from ziggiz_courier_handler_core.models.common import CommonEvent
from ziggiz_courier_handler_core.models.syslog_rfc5424 import SyslogRFC5424Message


class SyslogToCommonEventAdapter(Adapter[SyslogRFC5424Message, CommonEvent]):
    """Adapter that transforms syslog messages to common events."""

    # Mapping from syslog severity to common event severity
    SEVERITY_MAP = {
        0: "EMERGENCY",  # Emergency: system is unusable
        1: "ALERT",  # Alert: action must be taken immediately
        2: "CRITICAL",  # Critical: critical conditions
        3: "ERROR",  # Error: error conditions
        4: "WARNING",  # Warning: warning conditions
        5: "NOTICE",  # Notice: normal but significant condition
        6: "INFO",  # Informational: informational messages
        7: "DEBUG",  # Debug: debug-level messages
    }

    # Mapping from syslog facility to common event source component
    FACILITY_MAP = {
        0: "kernel",
        1: "user",
        2: "mail",
        3: "system",
        4: "system",  # Auth messages also map to system
        # Add more as needed
    }

    def transform(self, source: SyslogRFC5424Message) -> CommonEvent:
        """
        Transform a SyslogRFC5424Message into a CommonEvent.

        Args:
            source: The source SyslogRFC5424Message to transform

        Returns:
            The transformed CommonEvent
        """
        # Generate a unique event ID
        event_id = str(uuid.uuid4())

        # Map severity
        severity = self.SEVERITY_MAP.get(source.severity, "UNKNOWN")

        # Map facility to source component
        source_component = self.FACILITY_MAP.get(
            source.facility, f"facility-{source.facility}"
        )

        # Extract tags and attributes from structured data if available
        tags = []
        attributes: Dict[str, str] = {}

        if source.structured_data:
            for sd_id, params in source.structured_data.items():
                # Use structured data IDs as tags
                tags.append(sd_id)

                # Use parameters as attributes with prefixed keys to avoid collisions
                for key, value in params.items():
                    attributes[f"{sd_id}.{key}"] = value

        return CommonEvent(
            event_id=event_id,
            timestamp=source.timestamp,
            event_type="syslog",
            source_system=source.hostname,
            source_component=source_component,
            message=source.message,
            severity=severity,
            tags=tags,
            attributes=attributes,
        )
