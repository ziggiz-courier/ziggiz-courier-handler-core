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
Base classes for message decoder plugins.

This module provides common functionality for message decoder plugins,
including caching and common utility methods.
"""

# Standard library imports
import logging

from typing import Any, Dict, List, Optional

# Local/package imports
from core_data_processing.decoders.message_decoder_plugins import MessageDecoderPlugin
from core_data_processing.models.event_envelope_base import EventEnvelopeBaseModel
from core_data_processing.models.event_structure_classification import (
    StructuredEventStructureClassification,
)

logger = logging.getLogger(__name__)


class MessageDecoderPluginBase(MessageDecoderPlugin):
    """
    Base class for all message decoder plugins with common functionality.

    This class extends the MessageDecoderPlugin abstract base class with
    functionality common to all message decoder plugins, such as caching
    and utility methods for field mapping.
    """

    def __init__(self, parsing_cache: Optional[Dict[str, Any]] = None):
        """
        Initialize the message decoder plugin.

        Args:
            parsing_cache (Optional[Dict[str, Any]]): A dictionary for caching parsed message results
        """
        self.parsing_cache = parsing_cache if parsing_cache is not None else {}

    def apply_field_mapping(
        self,
        model: EventEnvelopeBaseModel,
        fields: List[Any],
        field_names: List[str],
        vendor: str,
        product: str,
        msgclass: str,
    ) -> None:
        """
        Apply field mapping to the model.

        Args:
            model (EventEnvelopeBaseModel): The model to update with parsed fields
            fields (List[Any]): The parsed field values
            field_names (List[str]): The field names corresponding to the values
            vendor (str): Vendor name for structure classification
            product (str): Product name for structure classification
            msgclass (str): Message class for structure classification
        """
        model.structure_classification = StructuredEventStructureClassification(
            vendor=vendor,
            product=product,
            msgclass=msgclass,
            fields=field_names,
        )
        model.event_data = {k: v for k, v in zip(field_names, fields)}
        logger.debug(
            f"{vendor} {product} plugin parsed event_data",
            extra={"event_data": model.event_data},
        )
