# -*- coding: utf-8 -*-
# # SPDX-License-Identifier: BSL-1.1
# # Copyright (c) 2025 Ziggiz Inc.
# #
# # This file is part of the ziggiz-courier-core-data-processing and is licensed under the
# # Business Source License 1.1. You may not use this file except in
# # compliance with the License. You may obtain a copy of the License at:
# # https://github.com/ziggiz-courier/ziggiz-courier-core-data-processing/blob/main/LICENSE
"""JSON encoder implementation."""

# Standard library imports
import json

from datetime import datetime
from typing import Any

# Local/package imports
from ziggiz_courier_handler_core.encoders.base import Encoder
from ziggiz_courier_handler_core.models.common import CommonEvent


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
