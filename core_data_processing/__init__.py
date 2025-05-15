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
