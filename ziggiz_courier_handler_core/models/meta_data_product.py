# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: BSL-1.1
# Copyright (c) 2025 Ziggiz Inc.
#
# This file is part of the ziggiz-courier-core-data-processing and is licensed under the
# Business Source License 1.1. You may not use this file except in
# compliance with the License. You may obtain a copy of the License at:
# https://github.com/ziggiz-courier/ziggiz-courier-core-data-processing/blob/main/LICENSE
"""Model for representing the product metadata of an event source."""

# Standard library imports
from typing import Optional

# Third-party imports
from pydantic import BaseModel as PydanticBaseModel


class MetaDataProduct(PydanticBaseModel):
    """
    Model representing the product metadata of an event source.

    Args:
        organization (str): The organization responsible for the event source. Required.
        product (str): The product generating the event. Required.
        module (Optional[str]): The module or subcomponent, if applicable. Optional.
    """

    organization: str
    product: str
    module: Optional[str] = None
