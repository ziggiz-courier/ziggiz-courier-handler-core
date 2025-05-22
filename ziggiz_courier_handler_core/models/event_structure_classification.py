# -*- coding: utf-8 -*-
# SPDX-License-Identifier: BSL-1.1
# Copyright (c) 2025 Ziggiz Inc.
#
# This file is part of the ziggiz-courier-core-data-processing and is licensed under the
# Business Source License 1.1. You may not use this file except in
# compliance with the License. You may obtain a copy of the License at:
# https://github.com/ziggiz-courier/ziggiz-courier-core-data-processing/blob/main/LICENSE
#
"""Event structure classification models for courier data processing."""

# Standard library imports
from typing import List, Optional

# Third-party imports
from pydantic import BaseModel as PydanticBaseModel


class BaseEventStructureClassification(PydanticBaseModel):
    """Base model for event structure classification.

    This model provides common fields for describing the structure of an event for classification purposes:
    - organization: The organization or originator of the event (default: 'unknown')
    - product: The product or system that generated the event (default: 'unknown')
    Subclasses should define additional structure-specific fields.
    """

    organization: str = "unknown"
    product: str = "unknown"
    msgclass: str = "unknown"

    model_config = {
        "frozen": False,
        "arbitrary_types_allowed": True,
    }

    def __init__(
        self,
        organization: str = "unknown",
        product: str = "unknown",
        msgclass: str = "unknown",
        **kwargs
    ):
        super().__init__(
            organization=organization, product=product, msgclass=msgclass, **kwargs
        )


class StringEventStructureClassification(BaseEventStructureClassification):
    """Event classification model for string-based event structure classification.

    Attributes:
        value: The string value representing the event structure classification.
    """

    punct: str = ""

    def __init__(
        self,
        organization: str = "unknown",
        product: str = "unknown",
        msgclass: str = "unknown",
        punct: str = "",
        **kwargs
    ):
        super().__init__(
            organization=organization, product=product, msgclass=msgclass, **kwargs
        )
        super(StringEventStructureClassification, self).__setattr__("punct", punct)


class StructuredEventStructureClassification(BaseEventStructureClassification):
    """Event classification model for structured (dict-based) event structure classification.

    Attributes:
        fields: The list of fields representing the structured event classification.
    """

    fields: List[str] = []

    def __init__(
        self,
        organization: str = "unknown",
        product: str = "unknown",
        msgclass: str = "unknown",
        fields: Optional[List[str]] = None,
        **kwargs
    ):
        if fields is None:
            fields = []
        super().__init__(
            organization=organization, product=product, msgclass=msgclass, **kwargs
        )
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
        organization: str = "unknown",
        product: str = "unknown",
        fields: Optional[List[str]] = None,
        punct: str = "",
        msgclass: str = "unknown",
        **kwargs
    ):
        StructuredEventStructureClassification.__init__(
            self,
            organization=organization,
            product=product,
            msgclass=msgclass,
            fields=fields,
            **kwargs
        )
        StringEventStructureClassification.__init__(
            self,
            organization=organization,
            product=product,
            msgclass=msgclass,
            punct=punct,
            **kwargs
        )
