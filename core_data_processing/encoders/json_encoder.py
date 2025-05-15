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
"""JSON encoder implementation."""

# Standard library imports
import json

from datetime import datetime
from typing import Any

# Local/package imports
from core_data_processing.encoders.base import Encoder
from core_data_processing.models.common import CommonEvent


class JSONEncoder(Encoder[CommonEvent, str]):
    """Encoder that serializes CommonEvent to JSON string."""

    def encode(self, model: CommonEvent) -> str:
        """
        Encode a CommonEvent model to a JSON string.

        Args:
            model: The CommonEvent model to encode

        Returns:
            A JSON string representation of the model
        """
        # Convert the model to a dictionary using the new Pydantic v2 method
        data = model.model_dump()

        # Custom JSON serialization to handle datetime objects
        return json.dumps(data, default=self._json_serializer, ensure_ascii=False)

    def _json_serializer(self, obj: Any) -> Any:
        """
        Custom serializer for JSON encoding to handle special types.

        Args:
            obj: The object to serialize

        Returns:
            A JSON serializable representation of the object
        """
        if isinstance(obj, datetime):
            return obj.isoformat()
        raise TypeError(f"Type {type(obj)} not serializable")
