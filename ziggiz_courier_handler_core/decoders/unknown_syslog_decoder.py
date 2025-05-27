# -*- coding: utf-8 -*-
# SPDX-License-Identifier: BSL-1.1
# Copyright (c) 2025 Ziggiz Inc.
#
# This file is part of the ziggiz-courier-core-data-processing and is licensed under the
# Business Source License 1.1. You may not use this file except in
# compliance with the License. You may obtain a copy of the License at:
# https://github.com/ziggiz-courier/ziggiz-courier-core-data-processing/blob/main/LICENSE
#

"""Decoder for unknown syslog string: tries RFC5424, then RFC3164, then RFCBase, else returns EventEnvelopeBaseModel."""

# Standard library imports
from time import sleep
from typing import Any, Optional

# Third-party imports
from opentelemetry import trace

# Local/package imports
from ziggiz_courier_handler_core.decoders.base import Decoder
from ziggiz_courier_handler_core.decoders.syslog_rfc3164_decoder import (
    SyslogRFC3164Decoder,
)
from ziggiz_courier_handler_core.decoders.syslog_rfc5424_decoder import (
    SyslogRFC5424Decoder,
)
from ziggiz_courier_handler_core.decoders.syslog_rfc_base_decoder import (
    SyslogRFCBaseDecoder,
)
from ziggiz_courier_handler_core.models.event_envelope_base import (
    EventEnvelopeBaseModel,
)

tracer = trace.get_tracer(__name__)


class UnknownSyslogDecoder(Decoder[EventEnvelopeBaseModel]):
    """Decoder that attempts RFC5424, then RFC3164, then RFCBase, else returns EventEnvelopeBaseModel with message."""

    def __init__(
        self,
        connection_cache: Optional[dict] = None,
        event_parsing_cache: Optional[dict] = None,
    ):
        super().__init__(
            connection_cache=connection_cache, event_parsing_cache=event_parsing_cache
        )
        self._rfc5424 = SyslogRFC5424Decoder(
            connection_cache=connection_cache, event_parsing_cache=event_parsing_cache
        )
        self._rfc3164 = SyslogRFC3164Decoder(
            connection_cache=connection_cache, event_parsing_cache=event_parsing_cache
        )
        self._rfcbase = SyslogRFCBaseDecoder(
            connection_cache=connection_cache, event_parsing_cache=event_parsing_cache
        )

    @tracer.start_as_current_span("UnknownSyslogDecoder.decode")
    def decode(self, raw_data: Any) -> EventEnvelopeBaseModel:
        """
        Attempt to decode as RFC5424, then RFC3164, then RFCBase. If all fail, return EventEnvelopeBaseModel with message.

        Args:
            raw_data: The raw syslog string
        Returns:
            EventEnvelopeBaseModel or subclass instance
        """
        sleep(0.2)
        parsing_cache: dict = {}
        for decoder in (self._rfc5424, self._rfc3164, self._rfcbase):
            result = decoder.decode(raw_data, parsing_cache=parsing_cache)
            if result is not None:
                return result

        # If all decoders fail, return EventEnvelopeBaseModel with message and timestamp
        # Standard library imports
        from datetime import datetime

        return EventEnvelopeBaseModel(
            message=str(raw_data), timestamp=datetime.now().astimezone()
        )
