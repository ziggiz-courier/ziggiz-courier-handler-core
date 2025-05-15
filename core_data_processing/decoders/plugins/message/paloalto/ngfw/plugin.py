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

# Local/package imports
from core_data_processing.decoders.utils.csv_parser import parse_quoted_csv_message
from core_data_processing.models.event_envelope_base import EventEnvelopeBaseModel
from core_data_processing.models.event_structure_classification import (
    StructuredEventStructureClassification,
)
from core_data_processing.models.message_decoder_plugins import (
    register_message_decoder,
)
from core_data_processing.models.syslog_rfc3164 import SyslogRFC3164Message
from core_data_processing.models.syslog_rfc5424 import SyslogRFC5424Message
from .field_maps import PAN_TYPE_FIELD_MAP

logger = logging.getLogger(__name__)


@register_message_decoder(SyslogRFC3164Message)
@register_message_decoder(SyslogRFC5424Message)
def paloalto_ngfw_csv(model: EventEnvelopeBaseModel, **kwargs) -> bool:
    """
    Parse a PaloAlto NGFW syslog message in CSV format into event_data on the model.

    Args:
        model (EventEnvelopeBaseModel): The event model instance to parse and update.
        **kwargs: Additional keyword arguments (may include 'parsing_cache').

    Returns:
        bool: True if the message was parsed as PaloAlto NGFW CSV, False otherwise.

    Example:
        >>> msg = '2024/05/13 12:34:56,001801000000,TRAFFIC,...'
        >>> paloalto_ngfw_csv(msg)
        ['2024/05/13 12:34:56', '001801000000', 'TRAFFIC', ...]
    """
    message = getattr(model, "message", None)
    if not isinstance(message, str):
        return False
    if "parsing_cache" in kwargs and isinstance(kwargs["parsing_cache"], dict):
        if "paloalto_ngfw_csv" not in kwargs["parsing_cache"]:
            kwargs["parsing_cache"]["parse_quoted_csv_message"] = (
                parse_quoted_csv_message(message)
            )
        fields = kwargs["parsing_cache"]["parse_quoted_csv_message"]
    else:
        fields = parse_quoted_csv_message(message)
    if fields and isinstance(fields, list) and len(fields) > 3:
        type_field = fields[3] if len(fields) > 3 else None
        field_names = None
        if type_field:
            field_names = PAN_TYPE_FIELD_MAP.get(type_field.upper())
        if field_names:
            model.structure_classification = StructuredEventStructureClassification(
                vendor="paloalto",
                product="ngfw",
                msgclass=type_field.lower(),
                fields=field_names,
            )
            model.event_data = {k: v for k, v in zip(field_names, fields)}

            logger.debug(
                "PaloAlto NGFW plugin parsed event_data",
                extra={"event_data": model.event_data},
            )
            return True
    return False
