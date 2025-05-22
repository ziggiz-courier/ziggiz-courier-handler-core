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
Base classes for message decoder plugins.

This module provides common functionality for message decoder plugins,
including caching and common utility methods.
"""


# Standard library imports
import logging

from typing import Any, Dict, Optional, Type

# Local/package imports
from ziggiz_courier_handler_core.decoders.message_decoder_plugins import (
    MessageDecoderPlugin,
)
from ziggiz_courier_handler_core.decoders.utils.message.base_parser import (
    BaseMessageParser,
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

    def _get_or_parse_message(
        self,
        message: str,
        parser_cls: "Type[BaseMessageParser]",
    ) -> Any:
        """
        Retrieve a parsed message from cache or parse and cache it.

        Args:
            message (str): The raw message string to parse
            parser_cls (Type[BaseMessageParser]):
                The BaseMessageParser subclass to use for parsing.

        Returns:
            The parsed result (usually a dict or None).

        Raises:
            TypeError: If parser_cls does not inherit from BaseMessageParser.
        """
        if not hasattr(parser_cls, "parse"):
            raise TypeError(
                f"parser_cls must implement a staticmethod 'parse', got {parser_cls}"
            )
        key = parser_cls.__name__
        if key not in self.parsing_cache:
            self.parsing_cache[key] = parser_cls.parse(message)
        return self.parsing_cache[key]

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
            parsing_cache (Optional[Dict[str, Any]]):
                A dictionary for caching parsed message results
        """
        self.parsing_cache = parsing_cache if parsing_cache is not None else {}

    def apply_field_mapping(
        self,
        model: EventEnvelopeBaseModel,
        event_data: Dict[str, Any],
        msgclass: str = "unknown",
        handler_metadata: Optional[dict] = None,
    ) -> None:
        """
        Apply field mapping to the model and update handler_data.

        Args:
            model (EventEnvelopeBaseModel): The model to update with parsed fields
            event_data (Dict[str, Any]): Dictionary containing event data to be stored
            msgclass (str): Message class for handler_data
            handler_metadata (Optional[dict]):
                Additional metadata for this handler entry
        """
        # Set event_data directly
        model.event_data = event_data

        # Use only the class name as key for first-party, or package..Type for
        # third-party plugins
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
        }
        if handler_metadata:
            entry.update(handler_metadata)

        # Maintain insertion order (Python 3.7+ dicts are ordered)
        if model.handler_data is None:
            model.handler_data = {}
        model.handler_data[key] = entry

        # NOTE: The plugin should call _set_source_producer_handler_data(model, organization, product) separately if needed.

        logger.debug(
            "plugin parsed event_data",
            extra={
                "event_data": model.event_data,
                "handler_data": model.handler_data,
            },
        )

    def _set_source_producer_handler_data(
        self,
        model: EventEnvelopeBaseModel,
        organization: str,
        product: str,
    ) -> None:
        """
        Set the SourceProducer object in the handler_data dict using the string version of the type as key.

        Args:
            model (EventEnvelopeBaseModel): The model whose handler_data will be updated
            organization (str): Organization name
            product (str): Product name
        """
        if model.handler_data is None:
            model.handler_data = {}
        key = SourceProducer.__name__
        model.handler_data[key] = SourceProducer(
            organization=organization, product=product
        )
