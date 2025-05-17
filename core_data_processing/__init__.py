# -*- coding: utf-8 -*-
# # SPDX-License-Identifier: BSL-1.1
# # Copyright (c) 2025 Ziggiz Inc.
# #
# # This file is part of the ziggiz-courier-core-data-processing and is licensed under the
# # Business Source License 1.1. You may not use this file except in
# # compliance with the License. You may obtain a copy of the License at:
# # https://github.com/ziggiz-courier/ziggiz-courier-core-data-processing/blob/main/LICENSE
"""Courier Data Processing package for decoding, transforming, and encoding data."""

# Standard library imports
from typing import Dict, List, Type

# Local/package imports
from core_data_processing.adapters.base import Adapter
from core_data_processing.decoders import plugins
from core_data_processing.decoders.base import Decoder
from core_data_processing.decoders.syslog_rfc3164_decoder import (
    SyslogRFC3164Decoder,
)
from core_data_processing.decoders.syslog_rfc5424_decoder import (
    SyslogRFC5424Decoder,
)
from core_data_processing.encoders.base import Encoder
from core_data_processing.encoders.json_encoder import JSONEncoder
from core_data_processing.encoders.otel_encoder import OtelSpanEncoder
from core_data_processing.encoders.syslog_rfc3164_encoder import SyslogRFC3164Encoder
from core_data_processing.models.common import CommonEvent
from core_data_processing.models.event_envelope_base import BaseModel
from core_data_processing.models.syslog_rfc3164 import SyslogRFC3164Message
from core_data_processing.models.syslog_rfc5424 import (
    SyslogRFC5424Message,
)
from core_data_processing.models.syslog_rfc_base import SyslogRFCBaseModel

__version__ = "0.2.0"

# Export public interfaces
__all__ = [
    # Base classes
    "Adapter",
    "BaseModel",
    "Decoder",
    "Encoder",
    # Models
    "CommonEvent",
    "SyslogRFC5424Message",
    "SyslogRFCBaseModel",
    "SyslogRFC3164Message",
    # Decoders
    "SyslogRFC5424Decoder",
    "SyslogRFC3164Decoder",
    # Adapters
    # Encoders
    "JSONEncoder",
    "OtelSpanEncoder",
    "SyslogRFC3164Encoder",
]
