# -*- coding: utf-8 -*-
# # SPDX-License-Identifier: BSL-1.1
# # Copyright (c) 2025 Ziggiz Inc.
# #
# # This file is part of the ziggiz-courier-core-data-processing and is licensed under the
# # Business Source License 1.1. You may not use this file except in
# # compliance with the License. You may obtain a copy of the License at:
# # https://github.com/ziggiz-courier/ziggiz-courier-core-data-processing/blob/main/LICENSE
"""
Generic LEEF 2.0 message plugin for Ziggiz-Courier.

This plugin provides a decoder for Log Event Extended Format (LEEF) 2.0 messages. It processes
LEEF-formatted messages by parsing them into structured data for downstream processing
and uses the vendor, product, and event_id fields from the LEEF header for classification.

References:
    - IBM QRadar Log Event Extended Format (LEEF) Guide
    - Related RFCs: RFC3164, RFC5424 (as transport mechanisms for LEEF)

Example:
    >>> msg = 'LEEF:2.0|IBM|QRadar|2.0|12345|SecurityAlert|src=10.0.0.1\tdst=2.1.2.2'
    >>> decoder = GenericLEEF2DecoderPlugin()
    >>> decoder.decode(model_with_msg)
    True
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
from ziggiz_courier_handler_core.decoders.utils.leef_2_parser import parse_leef_message
from ziggiz_courier_handler_core.models.event_envelope_base import (
    EventEnvelopeBaseModel,
)
from ziggiz_courier_handler_core.models.syslog_rfc3164 import SyslogRFC3164Message
from ziggiz_courier_handler_core.models.syslog_rfc5424 import SyslogRFC5424Message
from ziggiz_courier_handler_core.models.syslog_rfc_base import SyslogRFCBaseModel

logger = logging.getLogger(__name__)


class GenericLEEF2DecoderPlugin(MessageDecoderPluginBase):
    """
    Decoder for Log Event Extended Format (LEEF) 2.0 messages.

    This decoder parses LEEF 2.0 messages and updates the event model with structured data.
    It extracts vendor, product, event_id and optionally event_category information from
    LEEF headers to use for classification rather than using static values.
    """

    def __init__(self, parsing_cache: Optional[Dict[str, Any]] = None):
        """
        Initialize the LEEF 2.0 decoder.

        Args:
            parsing_cache (Optional[Dict[str, Any]]): A dictionary for caching parsed message results
        """
        super().__init__(parsing_cache)

    def decode(self, model: EventEnvelopeBaseModel) -> bool:
        """
        Parse a LEEF 2.0 message into event_data on the model.

        Args:
            model (EventEnvelopeBaseModel): The event model instance to parse and update.

        Returns:
            bool: True if the message was parsed as LEEF 2.0 format, False otherwise.

        Example:
            >>> msg = 'LEEF:2.0|IBM|QRadar|2.0|12345|SecurityAlert|src=10.0.0.1\tdst=2.1.2.2'
            >>> decoder = GenericLEEF2DecoderPlugin()
            >>> decoder.decode(model_with_msg)
            True
        """
        message = getattr(model, "message", None)
        if not isinstance(message, str) or not message.startswith("LEEF:2."):
            return False

        # Use parsing cache if available
        if "parse_leef2_message" not in self.parsing_cache:
            self.parsing_cache["parse_leef2_message"] = parse_leef_message(message)

        parsed_data = self.parsing_cache["parse_leef2_message"]

        if parsed_data:
            # Support both new (SourceProducer) and legacy (vendor/product) cache/test dicts
            if "SourceProducer" in parsed_data:
                sp = parsed_data["SourceProducer"]
                organization = getattr(sp, "organization", "unknown").lower()
                product = getattr(sp, "product", "unknown").lower()
            elif "vendor" in parsed_data and "product" in parsed_data:
                organization = parsed_data.get("vendor", "unknown").lower()
                product = parsed_data.get("product", "unknown").lower()
            else:
                return False

            msgclass = parsed_data.get("event_id", "unknown").lower()

            # Add category if available (LEEF 2.0 specific)
            if "event_category" in parsed_data:
                category = parsed_data.get("event_category", "").lower()
                if category:
                    msgclass = f"{category}_{msgclass}"

            self.apply_field_mapping(
                model=model,
                event_data=parsed_data,
                organization=organization,
                product=product,
                msgclass=msgclass,
            )

            logger.debug(
                "LEEF 2.0 plugin parsed event_data",
                extra={"event_data": model.event_data},
            )
            return True
        return False


# Register for SyslogRFCBaseModel
register_message_decoder(SyslogRFCBaseModel, MessagePluginStage.UNPROCESSED_STRUCTURED)(
    GenericLEEF2DecoderPlugin
)

# Register for SyslogRFC3164Message
register_message_decoder(
    SyslogRFC3164Message, MessagePluginStage.UNPROCESSED_STRUCTURED
)(GenericLEEF2DecoderPlugin)

# Register for SyslogRFC5424Message
register_message_decoder(
    SyslogRFC5424Message, MessagePluginStage.UNPROCESSED_STRUCTURED
)(GenericLEEF2DecoderPlugin)
