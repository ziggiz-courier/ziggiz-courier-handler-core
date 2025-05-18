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
from ziggiz_courier_handler_core.models.source_producer import SourceProducer


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
        handler_metadata: Optional[dict] = None,
    ) -> None:
        """
        Apply field mapping to the model and update handler_data.

        Args:
            model (EventEnvelopeBaseModel): The model to update with parsed fields
            fields (List[Any]): The parsed field values
            field_names (List[str]): The field names corresponding to the values
            vendor (str): Vendor name for handler_data
            product (str): Product name for handler_data
            msgclass (str): Message class for handler_data
            handler_metadata (Optional[dict]): Additional metadata for this handler entry
        """
        # Set event_data as before
        model.event_data = {k: v for k, v in zip(field_names, fields)}

        # Use only the class name as key for first-party, or package..Type for third-party plugins
        cls = self.__class__
        module = cls.__module__
        typename = cls.__name__
        if module.startswith("ziggiz_courier_handler_core."):
            key = typename
        else:
            # Abbreviated: package..Type (e.g., vendorpkg..PluginType)
            pkg = module.split(".")[0]
            key = f"{pkg}..{typename}"

        entry = {
            "msgclass": msgclass,
            "fields": field_names,
            "vendor": vendor,
            "product": product,
        }
        if handler_metadata:
            entry.update(handler_metadata)

        # Maintain insertion order (Python 3.7+ dicts are ordered)
        if model.handler_data is None:
            model.handler_data = {}
        model.handler_data[key] = entry

        model.handler_data["SourceProducer"] = SourceProducer(organization=vendor, product=product)
        logger.debug(
            "plugin parsed event_data",
            extra={
                "event_data": model.event_data,
                "handler_data": model.handler_data,
            },
        )
