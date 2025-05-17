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
from core_data_processing.decoders.message_decoder_plugins import (
    MessagePluginStage,
    register_message_decoder,
)
from core_data_processing.decoders.plugins.message.base import MessageDecoderPluginBase
from core_data_processing.models.event_envelope_base import EventEnvelopeBaseModel
from core_data_processing.models.syslog_rfc3164 import SyslogRFC3164Message
from core_data_processing.models.syslog_rfc5424 import SyslogRFC5424Message
from core_data_processing.models.syslog_rfc_base import SyslogRFCBaseModel
from core_data_processing.utils.kv_parser import parse_kv_message

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
        if "parse_kv_message" not in self.parsing_cache:
            self.parsing_cache["parse_kv_message"] = parse_kv_message(message)

        parsed_data = self.parsing_cache["parse_kv_message"]

        if parsed_data:
            # Set generic classification values
            vendor = "generic"
            product = "unknown_kv"
            msgclass = "unknown"

            # Apply parsed data to model
            self.apply_field_mapping(
                model=model,
                fields=list(parsed_data.values()),
                field_names=list(parsed_data.keys()),
                vendor=vendor,
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
