# -*- coding: utf-8 -*-
# # SPDX-License-Identifier: BSL-1.1
# # Copyright (c) 2025 Ziggiz Inc.
# #
# # This file is part of the ziggiz-courier-core-data-processing and is licensed under the
# # Business Source License 1.1. You may not use this file except in
# # compliance with the License. You may obtain a copy of the License at:
# # https://github.com/ziggiz-courier/ziggiz-courier-core-data-processing/blob/main/LICENSE
"""
Base classes for message decoder plugins.

This module provides common functionality for message decoder plugins,
including caching and common utility methods.
"""

# Standard library imports
import logging

from typing import Any, Dict, List, Optional

# Local/package imports
from ziggiz_courier_handler_core.decoders.message_decoder_plugins import (
    MessageDecoderPlugin,
)
from ziggiz_courier_handler_core.models.event_envelope_base import (
    EventEnvelopeBaseModel,
)
from ziggiz_courier_handler_core.models.event_structure_classification import (
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
