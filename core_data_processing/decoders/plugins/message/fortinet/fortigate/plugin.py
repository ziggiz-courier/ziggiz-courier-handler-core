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
FortiGate key=value message plugin for Ziggiz-Courier.

This plugin provides a decoder for Fortinet FortiGate syslog messages in key=value format, as seen in RFC3164 syslog payloads. It parses the message into a dictionary of key-value pairs for downstream processing.

References:
    - Fortinet FortiGate Syslog Message Formats:
      https://docs.fortinet.com/document/fortigate/latest/administration-guide/333255/syslog-message-formats
    - RFC3164: https://datatracker.ietf.org/doc/html/rfc3164
"""

# Standard library imports
import logging

from typing import Any, Dict, Optional

# Local/package imports
from core_data_processing.decoders.message_decoder_plugins import (
    register_message_decoder,
)
from core_data_processing.decoders.plugins.message.base import MessageDecoderPluginBase
from core_data_processing.decoders.utils.kv_parser import parse_kv_message
from core_data_processing.models.event_envelope_base import EventEnvelopeBaseModel
from core_data_processing.models.event_structure_classification import (
    StructuredEventStructureClassification,
)
from core_data_processing.models.syslog_rfc_base import SyslogRFCBaseModel

logger = logging.getLogger(__name__)


class FortigateKVDecoderPlugin(MessageDecoderPluginBase):
    """
    Message decoder plugin for FortiGate key=value syslog messages.
    Implements the MessageDecoderPluginBase.
    """

    def __init__(self, parsing_cache: Optional[Dict[str, Any]] = None):
        """
        Initialize the FortiGate KV decoder.

        Args:
            parsing_cache (Optional[Dict[str, Any]]): A dictionary for caching parsed message results
        """
        super().__init__(parsing_cache)

    def decode(self, model: EventEnvelopeBaseModel) -> bool:
        message = getattr(model, "message", None)
        if not isinstance(message, str):
            return False

        # Use parsing cache if available
        if "parse_kv_message" not in self.parsing_cache:
            self.parsing_cache["parse_kv_message"] = parse_kv_message(message)

        event_data = self.parsing_cache["parse_kv_message"]

        if (
            event_data
            and "eventtime" in event_data
            and "type" in event_data
            and "subtype" in event_data
            and "logid" in event_data
            and len(event_data["logid"]) == 10
        ):
            model.structure_classification = StructuredEventStructureClassification(
                vendor="fortinet",
                product="fortigate",
                msgclass="_".join(
                    [event_data.get("type", ""), event_data.get("subtype", "")]
                ),
                fields=sorted(list(event_data.keys())),
            )
            model.event_data = event_data.copy()
            logger.debug(
                "FortiGate plugin parsed event_data", extra={"event_data": event_data}
            )
            return True
        return False


# Register the class type directly (thread-safe)
register_message_decoder(SyslogRFCBaseModel)(FortigateKVDecoderPlugin)
