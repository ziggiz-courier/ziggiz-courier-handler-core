# -*- coding: utf-8 -*-
# SPDX-License-Identifier: BSL-1.1
# Copyright (c) 2025 Ziggiz Inc.
#
# This file is part of the ziggiz-courier-core-data-processing and is licensed under the
# Business Source License 1.1. You may not use this file except in
# compliance with the License. You may obtain a copy of the License at:
# https://github.com/ziggiz-courier/ziggiz-courier-core-data-processing/blob/main/LICENSE
#
"""Models for courier data processing."""

# Local/package imports
from ziggiz_courier_handler_core.models.event_envelope_base import BaseModel
from ziggiz_courier_handler_core.models.source_producer import SourceProducer
from ziggiz_courier_handler_core.models.syslog_rfc3164 import (
    SyslogRFC3164Message,
)
from ziggiz_courier_handler_core.models.syslog_rfc5424 import (
    SyslogRFC5424Message,
)
from ziggiz_courier_handler_core.models.syslog_rfc_base import SyslogRFCBaseModel

__all__ = [
    "BaseModel",
    "SyslogRFCBaseModel",
    "SyslogRFC5424Message",
    "SyslogRFC3164Message",
    "SourceProducer",
]
