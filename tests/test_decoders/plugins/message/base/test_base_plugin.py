# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
# SPDX-License-Identifier: BSL-1.1
# Copyright (c) 2025 Ziggiz Inc.
#
# This file is part of the ziggiz-courier-core-data-processing and is licensed under the
# Business Source License 1.1. You may not use this file except in
# compliance with the License. You may obtain a copy of the License at:
# https://github.com/ziggiz-courier/ziggiz-courier-core-data-processing/blob/main/LICENSE
"""
Unit tests for MessageDecoderPluginBase caching logic.
"""

# Standard library imports
from typing import Dict, Optional

# Third-party imports
import pytest

# Local/package imports
from ziggiz_courier_handler_core.decoders.plugins.message.base import (
    MessageDecoderPluginBase,
)
from ziggiz_courier_handler_core.decoders.utils.message.base_parser import (
    BaseMessageParser,
)


class DummyParser(BaseMessageParser):
    """Dummy parser for testing MessageDecoderPluginBase caching."""

    called = 0

    @staticmethod
    def parse(message: str) -> Optional[Dict[str, str]]:
        """Simulate parsing logic for test purposes."""
        DummyParser.called += 1
        if message == "valid":
            return {"result": "ok"}
        return None


class DummyPlugin(MessageDecoderPluginBase):
    """Dummy plugin for testing MessageDecoderPluginBase."""

    def decode(self, model):
        """Not implemented (not needed for these tests)."""
        raise NotImplementedError


def test_get_or_parse_message_caches_result():
    """Test that result is cached after first parse."""
    plugin = DummyPlugin(parsing_cache={})
    DummyParser.called = 0
    # First call parses
    result1 = plugin._get_or_parse_message("valid", DummyParser)
    assert result1 == {"result": "ok"}
    assert DummyParser.called == 1
    # Second call uses cache
    result2 = plugin._get_or_parse_message("valid", DummyParser)
    assert result2 == {"result": "ok"}
    assert DummyParser.called == 1


def test_get_or_parse_message_type_error():
    """Test that a TypeError is raised for invalid parser class."""
    plugin = DummyPlugin(parsing_cache={})

    class NotAParser:
        pass

    with pytest.raises(TypeError):
        plugin._get_or_parse_message("valid", NotAParser)


@pytest.mark.unit
def test_get_or_parse_message_none_result():
    """Test that None is returned and parse is called for invalid input."""
    plugin = DummyPlugin(parsing_cache={})
    DummyParser.called = 0
    result = plugin._get_or_parse_message("invalid", DummyParser)
    assert result is None
    assert DummyParser.called == 1
