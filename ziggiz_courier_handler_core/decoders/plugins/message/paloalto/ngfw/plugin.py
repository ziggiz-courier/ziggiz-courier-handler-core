# -*- coding: utf-8 -*-
# SPDX-License-Identifier: BSL-1.1
# Copyright (c) 2025 Ziggiz Inc.
#
# This file is part of the ziggiz-courier-core-data-processing and is licensed under the
# Business Source License 1.1. You may not use this file except in
# compliance with the License. You may obtain a copy of the License at:
# https://github.com/ziggiz-courier/ziggiz-courier-core-data-processing/blob/main/LICENSE
#
"""
PaloAlto NGFW CSV message plugin for Ziggiz-Courier.

This plugin provides a decoder for PaloAlto NGFW syslog messages in CSV format (RFC3164 and RFC5424).
It parses the message into a list of fields for downstream processing and caches results for efficiency.

References:
    - PaloAlto Networks Syslog Formats:
      https://docs.paloaltonetworks.com/pan-os/latest/pan-os-admin/monitoring/syslog-field-descriptions
    - RFC3164: https://datatracker.ietf.org/doc/html/rfc3164
    - RFC5424: https://datatracker.ietf.org/doc/html/rfc5424
"""

# Standard library imports
import logging

from typing import Any, Dict, Optional

# Local/package imports
from ziggiz_courier_handler_core.decoders.message_decoder_plugins import (
    MessagePluginStage,
    register_message_decoder,
)
from ziggiz_courier_handler_core.decoders.plugins.message.base import (
    MessageDecoderPluginBase,
)
from ziggiz_courier_handler_core.decoders.utils.csv_parser import (
    parse_quoted_csv_message,
)
from ziggiz_courier_handler_core.models.event_envelope_base import (
    EventEnvelopeBaseModel,
)
from ziggiz_courier_handler_core.models.syslog_rfc3164 import SyslogRFC3164Message
from ziggiz_courier_handler_core.models.syslog_rfc5424 import SyslogRFC5424Message
from .field_maps import PAN_TYPE_FIELD_MAP

logger = logging.getLogger(__name__)


class PaloAltoNGFWCSVDecoder(MessageDecoderPluginBase):
    """
    Decoder for PaloAlto NGFW syslog messages in CSV format.

    This decoder parses PaloAlto NGFW syslog messages in CSV format and
    updates the event model with structured data.
    """

    def __init__(self, parsing_cache: Optional[Dict[str, Any]] = None):
        """
        Initialize the PaloAlto NGFW CSV decoder.

        Args:
            parsing_cache (Optional[Dict[str, Any]]): A dictionary for caching parsed message results
        """
        super().__init__(parsing_cache)

    def decode(self, model: EventEnvelopeBaseModel) -> bool:
        """
        Parse a PaloAlto NGFW syslog message in CSV format into event_data on the model.

        Args:
            model (EventEnvelopeBaseModel): The event model instance to parse and update.

        Returns:
            bool: True if the message was parsed as PaloAlto NGFW CSV, False otherwise.

        Example:
            >>> msg = '2024/05/13 12:34:56,001801000000,TRAFFIC,...'
            >>> decoder = PaloAltoNGFWCSVDecoder()
            >>> decoder.decode(model_with_msg)
            True
        """
        message = getattr(model, "message", None)
        if not isinstance(message, str):
            return False

        if "parse_quoted_csv_message" not in self.parsing_cache:
            self.parsing_cache["parse_quoted_csv_message"] = parse_quoted_csv_message(
                message
            )

        fields = self.parsing_cache["parse_quoted_csv_message"]

        if fields and isinstance(fields, list) and len(fields) > 3:
            type_field = fields[3] if len(fields) > 3 else None
            field_names = None

            if type_field is not None:
                field_names = PAN_TYPE_FIELD_MAP.get(type_field.upper())

            if field_names:
                # Create event_data dictionary from fields and field_names
                event_data = dict(zip(field_names, fields))
                self.apply_field_mapping(
                    model=model,
                    event_data=event_data,
                    organization="paloalto",
                    product="ngfw",
                    msgclass=(
                        type_field.lower() if type_field is not None else "unknown"
                    ),
                )
                logger.debug(
                    "PaloAlto NGFW plugin parsed event_data",
                    extra={"event_data": model.event_data},
                )
                return True

        return False


# Register the class type directly (thread-safe)
register_message_decoder(SyslogRFC3164Message, MessagePluginStage.SECOND_PASS)(
    PaloAltoNGFWCSVDecoder
)
register_message_decoder(SyslogRFC5424Message, MessagePluginStage.SECOND_PASS)(
    PaloAltoNGFWCSVDecoder
)
