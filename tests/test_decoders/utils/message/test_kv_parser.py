# -*- coding: utf-8 -*-
# SPDX-License-Identifier: BSL-1.1
# Copyright (c) 2025 Ziggiz Inc.
#
# This file is part of the ziggiz-courier-core-data-processing and is licensed under the
# Business Source License 1.1. You may not use this file except in
# compliance with the License. You may obtain a copy of the License at:
# https://github.com/ziggiz-courier/ziggiz-courier-core-data-processing/blob/main/LICENSE
#
"""
Unit tests for the generic key=value parser utility (KVParser).
Covers FortiGate and generic log formats.
"""
# Third-party imports
import pytest

# Local/package imports
from ziggiz_courier_handler_core.decoders.utils.message.kv_parser import KVParser


@pytest.mark.unit
class TestKVParser:
    """Unit tests for the generic key=value parser utility (KVParser)."""

    def test_parse_kv_message_basic(self):
        msg = 'date=2025-05-12 time=12:34:56 devname=FGT1 devid=FG100E logid=000000001 type=event subtype=system level=notice msg="System rebooted"'
        result = KVParser.parse(msg)
        assert result is not None
        assert result["date"] == "2025-05-12"
        assert result["time"] == "12:34:56"
        assert result["devname"] == "FGT1"
        assert result["devid"] == "FG100E"
        assert result["logid"] == "000000001"
        assert result["type"] == "event"
        assert result["subtype"] == "system"
        assert result["level"] == "notice"
        assert result["msg"] == "System rebooted"

    def test_parse_kv_message_quoted_and_escaped(self):
        msg = 'user="john doe" action=login status=success path="/var/log/\\"test\\""'
        result = KVParser.parse(msg)
        assert result is not None
        assert result["user"] == "john doe"
        assert result["action"] == "login"
        assert result["status"] == "success"
        assert result["path"] == '/var/log/"test"'

    def test_parse_kv_message_invalid(self):
        msg = "not_a_kv_message"
        result = KVParser.parse(msg)
        assert result is None

    def test_parse_kv_message_empty(self):
        assert KVParser.parse("") is None
        # mypy: ignore[arg-type]
        assert KVParser.parse(None) is None  # type: ignore[arg-type]
