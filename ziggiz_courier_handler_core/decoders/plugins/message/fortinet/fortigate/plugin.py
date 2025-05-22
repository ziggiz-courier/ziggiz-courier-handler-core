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
FortiGate key=value message plugin for Ziggiz-Courier.

This plugin provides a decoder for Fortinet FortiGate syslog messages in key=value format, as seen in RFC3164 syslog payloads. It parses the message into a dictionary of key-value pairs for downstream processing and caches results for efficiency.

References:
    - Fortinet FortiGate Syslog Message Formats:
      https://docs.fortinet.com/document/fortigate/latest/administration-guide/333255/syslog-message-formats
    - RFC3164: https://datatracker.ietf.org/doc/html/rfc3164

Example:
    >>> msg = 'date=2025-05-13 time=12:34:56 devname=fortigate devid=FG100D3G12345678 logid=0100032003 type=event...'
    >>> decoder = FortinetFortiGateKVDecoderPlugin()
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
from ziggiz_courier_handler_core.models.syslog_rfc_base import SyslogRFCBaseModel

logger = logging.getLogger(__name__)


class FortinetFortiGateKVDecoderPlugin(MessageDecoderPluginBase):
    """
    Decoder for Fortinet FortiGate syslog messages in key=value format.

    This decoder parses Fortinet FortiGate syslog messages in key=value format
    and updates the event model with structured data.
    """

    def __init__(self, parsing_cache: Optional[Dict[str, Any]] = None):
        """
        Initialize the FortiGate KV decoder.

        Args:
            parsing_cache (Optional[Dict[str, Any]]): A dictionary for caching parsed message results
        """
        super().__init__(parsing_cache)

    def decode(self, model: EventEnvelopeBaseModel) -> bool:
        """
        Parse a Fortinet FortiGate syslog message in key=value format into event_data on the model.

        Args:
            model (EventEnvelopeBaseModel): The event model instance to parse and update.

        Returns:
            bool: True if the message was parsed as FortiGate key=value format, False otherwise.

        Example:
            >>> msg = 'date=2025-05-13 time=12:34:56 devname=fortigate devid=FG100D3G12345678 logid=0100032003 type=event...'
            >>> decoder = FortinetFortiGateKVDecoderPlugin()
            >>> decoder.decode(model_with_msg)
            True
        """
        message = getattr(model, "message", None)
        if not isinstance(message, str):
            return False

        event_data = self._get_or_parse_message(message, KVParser)

        if (
            event_data
            and "eventtime" in event_data
            and "type" in event_data
            and "subtype" in event_data
            and "logid" in event_data
            and len(event_data["logid"]) == 10
        ):
            # Get message class by joining type and subtype
            msgclass = "_".join(
                [event_data.get("type", ""), event_data.get("subtype", "")]
            )

            # Use apply_field_mapping method from base class
            self.apply_field_mapping(
                model=model,
                event_data=event_data,
                organization="fortinet",
                product="fortigate",
                msgclass=msgclass,
            )

            logger.debug(
                "FortiGate plugin parsed event_data",
                extra={"event_data": model.event_data},
            )
            return True
        return False


# Register the class type directly (thread-safe)
register_message_decoder(SyslogRFCBaseModel, MessagePluginStage.SECOND_PASS)(
    FortinetFortiGateKVDecoderPlugin
)
