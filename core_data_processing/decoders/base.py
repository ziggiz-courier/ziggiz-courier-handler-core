# -*- coding: utf-8 -*-
# # SPDX-License-Identifier: BSL-1.1
# # Copyright (c) 2025 Ziggiz Inc.
# #
# # This file is part of the ziggiz-courier-core-data-processing and is licensed under the
# # Business Source License 1.1. You may not use this file except in
# # compliance with the License. You may obtain a copy of the License at:
# # https://github.com/ziggiz-courier/ziggiz-courier-core-data-processing/blob/main/LICENSE
"""Base decoder interface for all decoders."""

# Standard library imports
from abc import ABC, abstractmethod
from typing import Any, Generic, Optional, TypeVar

# Local/package imports
from core_data_processing.models.event_envelope_base import EventEnvelopeBaseModel

T = TypeVar("T", bound=EventEnvelopeBaseModel)


class Decoder(Generic[T], ABC):

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
        from core_data_processing.decoders.message_decoder_plugins import (
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
                    plugin = plugin_cls(parsing_cache)
                    if plugin.decode(model):
                        return

    """Base class for all decoders."""

    def __init__(self, connection_cache: dict = None, event_parsing_cache: dict = None):
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
    def decode(self, raw_data: Any) -> T:
        """
        Decode raw data into a model.

        Args:
            raw_data: The raw data to decode.

        Returns:
            A model instance representing the decoded data.
        """
