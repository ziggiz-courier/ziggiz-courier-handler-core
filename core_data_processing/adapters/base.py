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
"""Base adapter interface for transforming between model types."""

# Standard library imports
from abc import ABC, abstractmethod
from typing import Generic, TypeVar

# Local/package imports
from core_data_processing.models.event_envelope_base import EventEnvelopeBaseModel

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
