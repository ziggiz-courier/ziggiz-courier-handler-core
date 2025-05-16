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
# (Removed duplicate/empty get_message_decoders definition)
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
from typing import Dict, Type

# Local/package imports
from core_data_processing.models.event_envelope_base import EventEnvelopeBaseModel


# Backward compatibility: get all plugins for a model class, all stages, in stage order
def get_message_decoders(model_cls):
    """
    Retrieve all message decoder plugin classes for a given model class, in stage order.
    Args:
        model_cls: The subclass of EventEnvelopeBaseModel.
    Returns:
        List of plugin classes (all stages, in order).
    """
    plugins_by_stage = _message_decoder_plugins.get(model_cls, {})
    ordered = []
    for stage in [
        MessagePluginStage.FIRST_PASS,
        MessagePluginStage.SECOND_PASS,
        MessagePluginStage.UNPROCESSED_STRUCTURED,
        MessagePluginStage.UNPROCESSED_MESSAGES,
    ]:
        ordered.extend(plugins_by_stage.get(stage, []))

    return ordered


# Plugin stages/groups
class MessagePluginStage:
    FIRST_PASS = "FIRST_PASS"
    SECOND_PASS = "SECOND_PASS"
    UNPROCESSED_STRUCTURED = "UNPROCESSED_STRUCTURED"
    UNPROCESSED_MESSAGES = "UNPROCESSED_MESSAGES"


# Registry: model class -> stage -> list of plugin class types
_message_decoder_plugins: Dict[
    Type[EventEnvelopeBaseModel],
    Dict[str, list[Type["MessageDecoderPlugin"]]],
] = {}


class MessageDecoderPlugin(ABC):
    """
    Abstract base class for message decoder plugins.
    All message decoder plugins should inherit from this class and implement the decode method.
    """

    @abstractmethod
    def decode(self, model: EventEnvelopeBaseModel) -> bool:
        """
        Decode a message into the model.
        Args:
            model: The EventEnvelopeBaseModel instance to populate.
        Returns:
            bool: True if decoding was successful, False otherwise.
        """


def register_message_decoder(model_cls: Type[EventEnvelopeBaseModel], stage: str):
    """
    Decorator to register a message decoder plugin class for a specific EventEnvelopeBaseModel subclass and stage.

    Args:
        model_cls: The subclass of EventEnvelopeBaseModel this plugin handles.
        stage: The stage/group for plugin execution.

    Returns:
        Decorator that registers the plugin class.
    """

    def decorator(plugin_cls: Type[MessageDecoderPlugin]):
        if model_cls not in _message_decoder_plugins:
            _message_decoder_plugins[model_cls] = {}
        _message_decoder_plugins[model_cls].setdefault(stage, []).append(plugin_cls)
        return plugin_cls

    return decorator


def get_message_decoders_by_stage(
    model_cls: Type[EventEnvelopeBaseModel],
) -> Dict[str, list[Type[MessageDecoderPlugin]]]:
    """
    Retrieve the message decoder plugin classes for a given model class, grouped by stage.
    Args:
        model_cls: The subclass of EventEnvelopeBaseModel.
    Returns:
        Dict of stage -> list of plugin classes.
    """
    return _message_decoder_plugins.get(model_cls, {})
