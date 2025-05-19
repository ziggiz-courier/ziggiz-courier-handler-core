# -*- coding: utf-8 -*-
# # SPDX-License-Identifier: BSL-1.1
# # Copyright (c) 2025 Ziggiz Inc.
# #
# # This file is part of the ziggiz-courier-core-data-processing and is licensed under the
# # Business Source License 1.1. You may not use this file except in
# # compliance with the License. You may obtain a copy of the License at:
# # https://github.com/ziggiz-courier/ziggiz-courier-core-data-processing/blob/main/LICENSE
"""
Generic XML message plugin for Ziggiz-Courier.

This plugin provides a decoder for XML-formatted messages. It processes
XML data by parsing it into structured data for downstream processing.
It handles common XML escaping issues and provides fallback parsing.

References:
    - XML 1.0 specification: https://www.w3.org/TR/xml/
    - Related RFCs: RFC3164, RFC5424 (as transport mechanisms for XML data)

Example:
    >>> msg = '<event><type>login</type><user>admin</user><status>success</status></event>'
    >>> decoder = GenericXMLDecoderPlugin()
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
from ziggiz_courier_handler_core.decoders.utils.xml_parser import parse_xml_message
from ziggiz_courier_handler_core.models.event_envelope_base import (
    EventEnvelopeBaseModel,
)
from ziggiz_courier_handler_core.models.syslog_rfc3164 import SyslogRFC3164Message
from ziggiz_courier_handler_core.models.syslog_rfc5424 import SyslogRFC5424Message
from ziggiz_courier_handler_core.models.syslog_rfc_base import SyslogRFCBaseModel

logger = logging.getLogger(__name__)


class GenericXMLDecoderPlugin(MessageDecoderPluginBase):
    """
    Decoder for XML-formatted messages.

    This decoder parses XML formatted messages and updates the event model with structured data.
    It extracts elements and attributes from XML objects and uses them directly for event data.
    If a DTD is present in the XML, it will be used as the message class.
    """

    def __init__(self, parsing_cache: Optional[Dict[str, Any]] = None):
        """
        Initialize the XML decoder.

        Args:
            parsing_cache (Optional[Dict[str, Any]]): A dictionary for caching parsed message results
        """
        super().__init__(parsing_cache)

    def decode(self, model: EventEnvelopeBaseModel) -> bool:
        """
        Parse an XML message into event_data on the model.

        Args:
            model (EventEnvelopeBaseModel): The event model instance to parse and update.

        Returns:
            bool: True if the message was parsed as XML format, False otherwise.

        Example:
            >>> msg = '<event><type>login</type><user>admin</user><status>success</status></event>'
            >>> decoder = GenericXMLDecoderPlugin()
            >>> decoder.decode(model_with_msg)
            True
        """
        message = getattr(model, "message", None)
        if not isinstance(message, str):
            return False

        # Use parsing cache if available
        if "parse_xml_message" not in self.parsing_cache:
            self.parsing_cache["parse_xml_message"] = parse_xml_message(message)

        parsed_data = self.parsing_cache["parse_xml_message"]

        if parsed_data:
            # Set generic classification values
            organization = "generic"
            product = "unknown_xml"

            # Check if we have a DTD name to use as msgclass
            msgclass = "unknown"
            if "_dtd_name" in parsed_data:
                msgclass = parsed_data["_dtd_name"]
                # Remove _dtd_name from parsed_data to avoid including it in event_data
                del parsed_data["_dtd_name"]

            # Apply parsed data to model
            self.apply_field_mapping(
                model=model,
                event_data=parsed_data,
                organization=organization,
                product=product,
                msgclass=msgclass,
            )

            logger.debug(
                "XML plugin parsed event_data",
                extra={"event_data": model.event_data},
            )
            return True
        return False


# Register for SyslogRFCBaseModel
register_message_decoder(SyslogRFCBaseModel, MessagePluginStage.UNPROCESSED_STRUCTURED)(
    GenericXMLDecoderPlugin
)

# Register for SyslogRFC3164Message
register_message_decoder(
    SyslogRFC3164Message, MessagePluginStage.UNPROCESSED_STRUCTURED
)(GenericXMLDecoderPlugin)

# Register for SyslogRFC5424Message
register_message_decoder(
    SyslogRFC5424Message, MessagePluginStage.UNPROCESSED_STRUCTURED
)(GenericXMLDecoderPlugin)
