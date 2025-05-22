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
Generic CEF message plugin for Ziggiz-Courier.

This plugin provides a decoder for Common Event Format (CEF) messages. It processes
CEF-formatted messages by parsing them into structured data for downstream processing
and uses the vendor, product, and name fields from the CEF header for classification.

References:
    - ArcSight Common Event Format (CEF) Guide:
      https://docs.broadcom.com/doc/implementing-arcsight-common-event-format
    - Related RFCs: RFC3164, RFC5424 (as transport mechanisms for CEF)

Example:
    >>> msg = 'CEF:1|Vendor|Product|1.0|100|Name|Severity|src=10.0.0.1 dst=2.1.2.2'
    >>> decoder = GenericCEFDecoderPlugin()
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
from ziggiz_courier_handler_core.decoders.plugins.message.generic.const import (
    ORGANIZATION,
)
from ziggiz_courier_handler_core.decoders.utils.message.cef_parser import (
    CEFParser,
)
from ziggiz_courier_handler_core.models.event_envelope_base import (
    EventEnvelopeBaseModel,
)
from ziggiz_courier_handler_core.models.syslog_rfc3164 import SyslogRFC3164Message
from ziggiz_courier_handler_core.models.syslog_rfc5424 import SyslogRFC5424Message
from ziggiz_courier_handler_core.models.syslog_rfc_base import SyslogRFCBaseModel

logger = logging.getLogger(__name__)


class GenericCEFDecoderPlugin(MessageDecoderPluginBase):
    """
    Decoder for Common Event Format (CEF) messages.

    This decoder parses CEF messages and updates the event model with structured data.
    It extracts vendor, product, and name information from CEF headers to use for
    classification rather than using static values.
    """

    def __init__(self, parsing_cache: Optional[Dict[str, Any]] = None):
        """
        Initialize the CEF decoder.

        Args:
            parsing_cache (Optional[Dict[str, Any]]): A dictionary for caching parsed message results
        """
        super().__init__(parsing_cache)

    def decode(self, model: EventEnvelopeBaseModel) -> bool:
        """
        Parse a CEF message into event_data on the model.

        Args:
            model (EventEnvelopeBaseModel): The event model instance to parse and update.

        Returns:
            bool: True if the message was parsed as CEF format, False otherwise.

        Example:
            >>> msg = 'CEF:1|Vendor|Product|1.0|100|Name|Severity|src=10.0.0.1 dst=2.1.2.2'
            >>> decoder = GenericCEFDecoderPlugin()
            >>> decoder.decode(model_with_msg)
            True
        """
        message = getattr(model, "message", None)
        if not isinstance(message, str) or not message.startswith("CEF:1"):
            return False

        parsed_data = self._get_or_parse_message(message, CEFParser)

        if (
            parsed_data
            and "device_vendor" in parsed_data
            and "device_product" in parsed_data
        ):
            # Organization and product from parsed_data
            organization = parsed_data.get("device_vendor", ORGANIZATION).lower()
            product = parsed_data.get("device_product", "unknown").lower()
            msgclass = parsed_data.get("name", "unknown").lower()

            self.apply_field_mapping(
                model=model,
                event_data=parsed_data,
                msgclass=msgclass,
            )
            self._set_source_producer_handler_data(
                model=model,
                organization=organization,
                product=product,
            )

            logger.debug(
                "CEF plugin parsed event_data",
                extra={"event_data": model.event_data},
            )
            return True
        return False


# Register for SyslogRFCBaseModel
register_message_decoder(SyslogRFCBaseModel, MessagePluginStage.UNPROCESSED_STRUCTURED)(
    GenericCEFDecoderPlugin
)

# Register for SyslogRFC3164Message
register_message_decoder(
    SyslogRFC3164Message, MessagePluginStage.UNPROCESSED_STRUCTURED
)(GenericCEFDecoderPlugin)

# Register for SyslogRFC5424Message
register_message_decoder(
    SyslogRFC5424Message, MessagePluginStage.UNPROCESSED_STRUCTURED
)(GenericCEFDecoderPlugin)
