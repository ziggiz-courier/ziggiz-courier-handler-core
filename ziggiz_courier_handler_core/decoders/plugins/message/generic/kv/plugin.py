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
Generic KV (Key-Value) message plugin for Ziggiz-Courier.

This plugin provides a decoder for key-value formatted messages. It processes
messages in the format "key1=value1 key2=value2" and parses them into structured
data for downstream processing.

Example:
    >>> msg = 'src=10.0.0.1 dst=8.8.8.8 action=allow service=https'
    >>> decoder = GenericKVDecoderPlugin()
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
from ziggiz_courier_handler_core.decoders.utils.message.kv_parser import KVParser
from ziggiz_courier_handler_core.models.event_envelope_base import (
    EventEnvelopeBaseModel,
)
from ziggiz_courier_handler_core.models.syslog_rfc3164 import SyslogRFC3164Message
from ziggiz_courier_handler_core.models.syslog_rfc5424 import SyslogRFC5424Message
from ziggiz_courier_handler_core.models.syslog_rfc_base import SyslogRFCBaseModel

logger = logging.getLogger(__name__)


class GenericKVDecoderPlugin(MessageDecoderPluginBase):
    """
    Decoder for key-value formatted messages.

    This decoder parses messages with a key=value format and updates the event model with structured data.
    It extracts fields from key-value pairs and uses them directly for event data.

    Example:
        >>> msg = 'src=10.0.0.1 dst=8.8.8.8 action=allow service=https'
        >>> decoder = GenericKVDecoderPlugin()
        >>> decoder.decode(model_with_msg)
        True
    """

    def __init__(self, parsing_cache: Optional[Dict[str, Any]] = None):
        """
        Initialize the KV decoder.

        Args:
            parsing_cache (Optional[Dict[str, Any]]): A dictionary for caching parsed message results
        """
        super().__init__(parsing_cache)

    def decode(self, model: EventEnvelopeBaseModel) -> bool:
        """
        Parse a key-value formatted message into event_data on the model.

        Args:
            model (EventEnvelopeBaseModel): The event model instance to parse and update.

        Returns:
            bool: True if the message was parsed as KV format, False otherwise.

        Example:
            >>> msg = 'src=10.0.0.1 dst=8.8.8.8 action=allow service=https'
            >>> decoder = GenericKVDecoderPlugin()
            >>> decoder.decode(model_with_msg)
            True
        """
        message = getattr(model, "message", None)
        if not isinstance(message, str):
            return False

        # Use parsing cache if available
        if "kv_parser" not in self.parsing_cache:
            self.parsing_cache["kv_parser"] = KVParser.parse(message)

        parsed_data = self.parsing_cache["kv_parser"]

        if parsed_data:
            # Set generic classification values
            organization = "generic"
            product = "unknown_kv"
            msgclass = "unknown"

            # Apply parsed data to model
            self.apply_field_mapping(
                model=model,
                event_data=parsed_data,
                organization=organization,
                product=product,
                msgclass=msgclass,
            )

            logger.debug(
                "KV plugin parsed event_data",
                extra={"event_data": model.event_data},
            )
            return True
        return False


# Register for SyslogRFCBaseModel
register_message_decoder(SyslogRFCBaseModel, MessagePluginStage.UNPROCESSED_STRUCTURED)(
    GenericKVDecoderPlugin
)

# Register for SyslogRFC3164Message
register_message_decoder(
    SyslogRFC3164Message, MessagePluginStage.UNPROCESSED_STRUCTURED
)(GenericKVDecoderPlugin)

# Register for SyslogRFC5424Message
register_message_decoder(
    SyslogRFC5424Message, MessagePluginStage.UNPROCESSED_STRUCTURED
)(GenericKVDecoderPlugin)
