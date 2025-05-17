# -*- coding: utf-8 -*-
# # SPDX-License-Identifier: BSL-1.1
# # Copyright (c) 2025 Ziggiz Inc.
# #
# # This file is part of the ziggiz-courier-core-data-processing and is licensed under the
# # Business Source License 1.1. You may not use this file except in
# # compliance with the License. You may obtain a copy of the License at:
# # https://github.com/ziggiz-courier/ziggiz-courier-core-data-processing/blob/main/LICENSE
"""Base encoder interface for all encoders."""

# Standard library imports
from abc import ABC, abstractmethod
from typing import Generic, TypeVar

# Local/package imports
from core_data_processing.models.event_envelope_base import BaseModel

T = TypeVar("T", bound=BaseModel)
U = TypeVar("U")


class Encoder(Generic[T, U], ABC):
    """Base class for all encoders."""

    @abstractmethod
    def encode(self, model: T) -> U:
        """
        Encode a model into a different format.

        Args:
            model: The model to encode.

        Returns:
            The encoded data.
        """
