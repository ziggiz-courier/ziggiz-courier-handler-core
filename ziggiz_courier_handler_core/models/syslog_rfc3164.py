# -*- coding: utf-8 -*-
# SPDX-License-Identifier: BSL-1.1
# Copyright (c) 2025 Ziggiz Inc.
#
# This file is part of the ziggiz-courier-core-data-processing and is licensed under the
# Business Source License 1.1. You may not use this file except in
# compliance with the License. You may obtain a copy of the License at:
# https://github.com/ziggiz-courier/ziggiz-courier-core-data-processing/blob/main/LICENSE
#
"""Syslog RFC3164 message model (BSD-style syslog).

This module defines data models for the Syslog protocol as specified in RFC3164,
commonly known as the 'BSD syslog protocol', which uses a simpler format than RFC5424.
See: https://tools.ietf.org/html/rfc3164
"""

# Standard library imports

# Local/package imports
from ziggiz_courier_handler_core.models.syslog_rfc_base import SyslogRFCCommonModel


class SyslogRFC3164Message(SyslogRFCCommonModel):
    """Model representing a syslog message compliant with RFC3164 standard (BSD syslog).

    The RFC3164 format has a simpler structure than RFC5424:
    <PRI>CONTENT

    Where:
    - PRI: The priority value calculated as facility * 8 + severity
    - CONTENT: The actual message content

    Note: While RFC3164 messages might not always include an explicit timestamp in the message,
    the EventEnvelopeBaseModel requires one. For RFC3164 messages without a timestamp,
    we will use the receipt time set by the decoder.
    """

    # Inherits hostname, app_name, and proc_id from SyslogRFCCommonModel

    def __init__(
        self,
        facility: int,
        severity: int,
        message=None,
        timestamp=None,
        hostname=None,
        app_name=None,
        proc_id=None,
        **kwargs
    ):
        super().__init__(
            facility=facility,
            severity=severity,
            message=message,
            timestamp=timestamp,
            hostname=hostname,
            app_name=app_name,
            proc_id=proc_id,
            **kwargs
        )

    @classmethod
    def from_priority(cls, pri, **kwargs):
        base = super().from_priority(pri, **kwargs)
        return cls(
            facility=base.facility,
            severity=base.severity,
            message=base.message,
            timestamp=getattr(base, "timestamp", None),
            hostname=getattr(base, "hostname", None),
            app_name=getattr(base, "app_name", None),
            proc_id=getattr(base, "proc_id", None),
        )


# from core_data_processing.models.base import BaseEventStructureClassification
# SyslogRFC3164Message.model_rebuild()
