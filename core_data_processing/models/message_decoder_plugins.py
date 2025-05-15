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
"""Plugin registry for message decoders for EventEnvelopeBaseModel subclasses."""

# Standard library imports
from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, Optional, Type

# Local/package imports
from core_data_processing.models.event_envelope_base import EventEnvelopeBaseModel

# Registry: model class -> plugin function
_message_decoder_plugins: Dict[
    Type[EventEnvelopeBaseModel], list[Callable[[EventEnvelopeBaseModel, Any], bool]]
] = {}


class MessageDecoderPlugin(ABC):
    """
    Abstract base class for message decoder plugins.
    All message decoder plugins should inherit from this class and implement the decode method.
    """

    @abstractmethod
    def decode(self, model: EventEnvelopeBaseModel, raw: Any) -> bool:
        """
        Decode a message into the model.
        Args:
            model: The EventEnvelopeBaseModel instance to populate.
            raw: The raw message data to decode.
        Returns:
            bool: True if decoding was successful, False otherwise.
        """


def register_message_decoder(model_cls: Type[EventEnvelopeBaseModel]):
    """
    Decorator to register a message decoder plugin for a specific EventEnvelopeBaseModel subclass.
    Args:
        model_cls: The subclass of EventEnvelopeBaseModel this plugin handles.
    Returns:
        Decorator that registers the function as a plugin.
    """

    def decorator(func: Callable[[EventEnvelopeBaseModel, Any], bool]):
        _message_decoder_plugins.setdefault(model_cls, []).append(func)
        return func

    return decorator


def get_message_decoders(
    model_cls: Type[EventEnvelopeBaseModel],
) -> Optional[list[Callable[[EventEnvelopeBaseModel, Any], bool]]]:
    """
    Retrieve the message decoder plugins for a given model class.
    Args:
        model_cls: The subclass of EventEnvelopeBaseModel.
    Returns:
        List of plugin functions or None if not registered.
    """
    return _message_decoder_plugins.get(model_cls, [])
