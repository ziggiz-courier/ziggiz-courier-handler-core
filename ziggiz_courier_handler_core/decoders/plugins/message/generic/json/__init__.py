# -*- coding: utf-8 -*-
# SPDX-License-Identifier: BSL-1.1
# Copyright (c) 2025 Ziggiz Inc.
#
# This file is part of the ziggiz-courier-core-data-processing and is licensed under the
# Business Source License 1.1. You may not use this file except in
# compliance with the License. You may obtain a copy of the License at:
# https://github.com/ziggiz-courier/ziggiz-courier-core-data-processing/blob/main/LICENSE
#
"""Generic JSON message decoder plugin package."""

# Local/package imports
from ziggiz_courier_handler_core.decoders.plugins.message.generic.json.plugin import (
    GenericJSONDecoderPlugin,
)

__all__ = ["GenericJSONDecoderPlugin"]
