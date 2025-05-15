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
