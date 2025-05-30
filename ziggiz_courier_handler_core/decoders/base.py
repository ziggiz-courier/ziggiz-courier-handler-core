# -*- coding: utf-8 -*-
# SPDX-License-Identifier: BSL-1.1
# Copyright (c) 2025 Ziggiz Inc.
#
# This file is part of the ziggiz-courier-core-data-processing and is licensed under the
# Business Source License 1.1. You may not use this file except in
# compliance with the License. You may obtain a copy of the License at:
# https://github.com/ziggiz-courier/ziggiz-courier-core-data-processing/blob/main/LICENSE
#

"""Base decoder interface for all decoders."""

# Standard library imports
from abc import ABC, abstractmethod
from typing import Any, Generic, Optional, TypeVar, cast

# Local/package imports
from ziggiz_courier_handler_core.decoders.plugins.message.base import (
    MessageDecoderPluginBase,
)
from ziggiz_courier_handler_core.models.event_envelope_base import (
    EventEnvelopeBaseModel,
)

T = TypeVar("T", bound=EventEnvelopeBaseModel)


class Decoder(Generic[T], ABC):

    def _set_trace_attributes(
        self,
        span,
        attributes: Optional[dict] = None,
        events: Optional[list] = None,
    ) -> None:
        """
        Set OpenTelemetry span attributes and add events for decoder operations.

        Args:
            span: The current OpenTelemetry span
            attributes: Additional attributes to set on the span
            events: List of events to add to the span, each as a tuple (event_name, event_attributes)
        """
        # Set any provided attributes
        if attributes:
            for key, value in attributes.items():
                span.set_attribute(key, value)
        # Add events
        if events:
            for event in events:
                if isinstance(event, tuple) and len(event) == 2:
                    event_name, event_attrs = event
                    span.add_event(event_name, event_attrs)
                elif isinstance(event, str):
                    span.add_event(event)

    """
    Abstract base class for decoders that transform raw data into model objects.

    Generic type T must be a subclass of EventEnvelopeBaseModel. All concrete decoders
    should inherit from this class and implement the decode method.

    This class provides common functionality for all decoders, including plugin execution
    for message processing.
    """

    def _run_message_decoder_plugins(
        self,
        model: EventEnvelopeBaseModel,
        message_decoder_type: type,
        parsing_cache: Optional[dict] = None,
    ) -> None:
        """
        Run message decoder plugins for the given model and message decoder type, by stage.

        Args:
            model: The model instance to decode with plugins
            message_decoder_type: The type to use for plugin lookup (e.g., SyslogRFC3164Message)
            parsing_cache: Optional dictionary for caching parsing results
        """
        # Local/package imports
        from ziggiz_courier_handler_core.decoders.message_decoder_plugins import (
            MessagePluginStage,
            get_message_decoders_by_stage,
        )

        if parsing_cache is None:
            parsing_cache = (
                self.event_parsing_cache if hasattr(self, "event_parsing_cache") else {}
            )
        plugin_groups = get_message_decoders_by_stage(message_decoder_type)
        if plugin_groups and getattr(model, "message", None):
            # Enforced stage order
            for stage in [
                MessagePluginStage.FIRST_PASS,
                MessagePluginStage.SECOND_PASS,
                MessagePluginStage.UNPROCESSED_STRUCTURED,
                MessagePluginStage.UNPROCESSED_MESSAGES,
            ]:
                for plugin_cls in plugin_groups.get(stage, []):
                    # Use issubclass to check if the plugin class is MessageDecoderPluginBase
                    # which accepts parsing_cache in __init__
                    # Create the plugin instance with or without parsing_cache
                    if issubclass(plugin_cls, MessageDecoderPluginBase):
                        plugin = plugin_cls(parsing_cache)
                    else:
                        # Use cast to tell mypy this is a MessageDecoderPlugin
                        plugin = cast(MessageDecoderPluginBase, plugin_cls())
                    if plugin.decode(model):
                        return

    def __init__(
        self,
        connection_cache: Optional[dict] = None,
        event_parsing_cache: Optional[dict] = None,
    ):
        """
        Initialize the decoder.

        Args:
            connection_cache: Optional dictionary for caching connections
            event_parsing_cache: Optional dictionary for caching event parsing results
        """
        self.connection_cache = connection_cache if connection_cache is not None else {}
        self.event_parsing_cache = (
            event_parsing_cache if event_parsing_cache is not None else {}
        )

    @abstractmethod
    def decode(self, raw_data: Any) -> Optional[T]:
        """
        Decode raw data into a model.

        Args:
            raw_data: The raw data to decode.

        Returns:
            A model instance representing the decoded data, or None if decoding fails.
        """
