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
Benchmark for SyslogRFCBaseDecoder using pytest-benchmark.
Run with: pytest -m benchmark --benchmark-only
"""

# Third-party imports
import pytest

# Local/package imports
from ziggiz_courier_handler_core.decoders.syslog_rfc_base_decoder import (
    SyslogRFCBaseDecoder,
)

RFCBASE_SAMPLE = "<34>This is a test message with priority_34_auth_critical"


@pytest.mark.benchmark
def test_benchmark_syslog_rfc_base_decode(benchmark):
    decoder = SyslogRFCBaseDecoder()
    benchmark(lambda: decoder.decode(RFCBASE_SAMPLE))
