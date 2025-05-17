# -*- coding: utf-8 -*-
# # SPDX-License-Identifier: BSL-1.1
# # Copyright (c) 2025 Ziggiz Inc.
# #
# # This file is part of the ziggiz-courier-core-data-processing and is licensed under the
# # Business Source License 1.1. You may not use this file except in
# # compliance with the License. You may obtain a copy of the License at:
# # https://github.com/ziggiz-courier/ziggiz-courier-core-data-processing/blob/main/LICENSE
"""Base adapter interface for transforming between model types."""

# Standard library imports
from abc import ABC, abstractmethod
from typing import Generic, TypeVar

# Local/package imports
from ziggiz_courier_handler_core.models.event_envelope_base import (
    EventEnvelopeBaseModel,
)

S = TypeVar("S", bound=EventEnvelopeBaseModel)
T = TypeVar("T", bound=EventEnvelopeBaseModel)


class Adapter(Generic[S, T], ABC):
    """Base class for all adapters that transform between model types."""

    @abstractmethod
    def transform(self, source: S) -> T:
        """
        Transform a source model into a target model.

        Args:
            source: The source model to transform.

        Returns:
            The transformed target model.
        """
