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
"""Event structure classification models for courier data processing."""

# Standard library imports

# Third-party imports
from pydantic import BaseModel as PydanticBaseModel


class BaseEventStructureClassification(PydanticBaseModel):
    """Base model for event structure classification.

    This model provides common fields for describing the structure of an event for classification purposes:
    - vendor: The vendor or originator of the event (default: 'unknown')
    - product: The product or system that generated the event (default: 'unknown')
    Subclasses should define additional structure-specific fields.
    """

    vendor: str = "unknown"
    product: str = "unknown"
    msgclass: str = "unknown"

    model_config = {
        "frozen": False,
        "arbitrary_types_allowed": True,
    }

    def __init__(
        self,
        vendor: str = "unknown",
        product: str = "unknown",
        msgclass: str = "unknown",
        **kwargs
    ):
        super().__init__(vendor=vendor, product=product, msgclass=msgclass, **kwargs)


class StringEventStructureClassification(BaseEventStructureClassification):
    """Event classification model for string-based event structure classification.

    Attributes:
        value: The string value representing the event structure classification.
    """

    punct: str = ""

    def __init__(
        self,
        vendor: str = "unknown",
        product: str = "unknown",
        msgclass: str = "unknown",
        punct: str = "",
        **kwargs
    ):
        super().__init__(vendor=vendor, product=product, msgclass=msgclass, **kwargs)
        super(StringEventStructureClassification, self).__setattr__("punct", punct)


class StructuredEventStructureClassification(BaseEventStructureClassification):
    """Event classification model for structured (dict-based) event structure classification.

    Attributes:
        fields: The list of fields representing the structured event classification.
    """

    fields: list[str] = []

    def __init__(
        self,
        vendor: str = "unknown",
        product: str = "unknown",
        msgclass: str = "unknown",
        fields: list[str] = None,
        **kwargs
    ):
        if fields is None:
            fields = []
        super().__init__(vendor=vendor, product=product, msgclass=msgclass, **kwargs)
        super(StructuredEventStructureClassification, self).__setattr__(
            "fields", fields
        )


class FormatStringEventStructureClassification(
    StructuredEventStructureClassification, StringEventStructureClassification
):
    """Event classification model for format string-based event structure classification.

    This model combines both structured and string-based classification.
    """

    def __init__(
        self,
        vendor: str = "unknown",
        product: str = "unknown",
        fields: list[str] = None,
        punct: str = "",
        msgclass: str = "unknown",
        **kwargs
    ):
        StructuredEventStructureClassification.__init__(
            self,
            vendor=vendor,
            product=product,
            msgclass=msgclass,
            fields=fields,
            **kwargs
        )
        StringEventStructureClassification.__init__(
            self,
            vendor=vendor,
            product=product,
            msgclass=msgclass,
            punct=punct,
            **kwargs
        )
