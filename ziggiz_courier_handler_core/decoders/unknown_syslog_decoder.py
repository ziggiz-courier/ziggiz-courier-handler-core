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
import logging

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

logger = logging.getLogger(__name__)
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
        parsing_cache: dict = {}
        span = trace.get_current_span()
        logger.debug(
            "Attempting to decode syslog message with all known decoders",
            extra={"input_length": len(str(raw_data))},
        )
        for decoder, rfc in zip(
            (self._rfc5424, self._rfc3164, self._rfcbase), ("5424", "3164", "base")
        ):
            decoder_name = decoder.__class__.__name__
            logger.debug("Trying decoder", extra={"decoder": decoder_name})
            result = decoder.decode(raw_data, parsing_cache=parsing_cache)
            if result is not None:
                logger.debug("Decoder succeeded", extra={"decoder": decoder_name})
                self._set_trace_attributes(
                    span,
                    raw_data=raw_data,
                    rfc=rfc,
                    decoder_name=decoder_name,
                    events=[("decode_success", {"decoder": decoder_name})],
                )
                return result

        # If all decoders fail, return EventEnvelopeBaseModel with message and timestamp
        # Standard library imports
        from datetime import datetime

        logger.warning(
            "All decoders failed, returning EventEnvelopeBaseModel fallback",
            extra={"input_sample": str(raw_data)[:100]},
        )
        self._set_trace_attributes(
            span,
            raw_data=raw_data,
            rfc="unknown",
            decoder_name="fallback",
            events=[("decode_failed", {"input_sample": str(raw_data)[:100]})],
        )
        return EventEnvelopeBaseModel(
            message=str(raw_data), timestamp=datetime.now().astimezone()
        )
