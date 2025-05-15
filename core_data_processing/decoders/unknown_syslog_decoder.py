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
"""Decoder for unknown syslog string: tries RFC5424, then RFC3164, then RFCBase, else returns EventEnvelopeBaseModel."""

# Standard library imports
from typing import Any

# Local/package imports
from core_data_processing.decoders.base import Decoder
from core_data_processing.decoders.syslog_rfc3164_decoder import SyslogRFC3164Decoder
from core_data_processing.decoders.syslog_rfc5424_decoder import SyslogRFC5424Decoder
from core_data_processing.decoders.syslog_rfc_base_decoder import (
    SyslogRFCBaseDecoder,
)
from core_data_processing.models.event_envelope_base import EventEnvelopeBaseModel


class UnknownSyslogDecoder(Decoder[EventEnvelopeBaseModel]):
    """Decoder that attempts RFC5424, then RFC3164, then RFCBase, else returns EventEnvelopeBaseModel with message."""

    def __init__(self):
        self._rfc5424 = SyslogRFC5424Decoder()
        self._rfc3164 = SyslogRFC3164Decoder()
        self._rfcbase = SyslogRFCBaseDecoder()

    def decode(self, raw_data: Any) -> EventEnvelopeBaseModel:
        """
        Attempt to decode as RFC5424, then RFC3164, then RFCBase. If all fail, return EventEnvelopeBaseModel with message.

        Args:
            raw_data: The raw syslog string
        Returns:
            EventEnvelopeBaseModel or subclass instance
        """
        parsing_cache = {}
        for decoder in (self._rfc5424, self._rfc3164, self._rfcbase):
            try:
                return decoder.decode(raw_data, parsing_cache=parsing_cache)
            except Exception:
                continue
        # If all decoders fail, return EventEnvelopeBaseModel with message and timestamp
        # Standard library imports
        from datetime import datetime

        return EventEnvelopeBaseModel(
            message=str(raw_data), timestamp=datetime.now().astimezone()
        )
