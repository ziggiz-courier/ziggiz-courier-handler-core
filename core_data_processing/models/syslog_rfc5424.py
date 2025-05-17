# -*- coding: utf-8 -*-
# # SPDX-License-Identifier: BSL-1.1
# # Copyright (c) 2025 Ziggiz Inc.
# #
# # This file is part of the ziggiz-courier-core-data-processing and is licensed under the
# # Business Source License 1.1. You may not use this file except in
# # compliance with the License. You may obtain a copy of the License at:
# # https://github.com/ziggiz-courier/ziggiz-courier-core-data-processing/blob/main/LICENSE
"""Syslog RFC5424 message model.

This module defines data models for the Syslog protocol as specified in RFC5424.
See: https://tools.ietf.org/html/rfc5424
"""

# Standard library imports
from datetime import datetime
from typing import Dict, Optional

# Local/package imports
from core_data_processing.models.syslog_rfc_base import SyslogRFCCommonModel


class SyslogRFC5424Message(SyslogRFCCommonModel):
    """Model representing a syslog message compliant with RFC5424 standard.

    The RFC5424 format specifies the following structure:
    <PRI>VERSION TIMESTAMP HOSTNAME APP-NAME PROCID MSGID STRUCTURED-DATA MSG

    Where PRI is calculated as (facility * 8) + severity
    """

    # Core syslog message fields
    timestamp: (
        datetime  # Required message timestamp (overrides optional BaseModel.timestamp)
    )
    # hostname, app_name, and proc_id are inherited from SyslogRFCCommonModel
    msg_id: Optional[str] = None  # Identifies the message type
    # Structured data as defined in RFC5424 section 6.3
    # Format: {SD_ID: {PARAM_NAME: PARAM_VALUE, ...}, ...}
    structured_data: Optional[Dict[str, Dict[str, str]]] = None

    @classmethod
    def from_priority(cls, pri, **kwargs):
        base = super().from_priority(pri, **kwargs)
        return cls(
            facility=base.facility,
            severity=base.severity,
            message=getattr(base, "message", None),
            timestamp=getattr(base, "timestamp", None),
            hostname=getattr(base, "hostname", None),
            app_name=getattr(base, "app_name", None),
            proc_id=getattr(base, "proc_id", None),
            msg_id=getattr(base, "msg_id", None),
            structured_data=getattr(base, "structured_data", None),
        )
