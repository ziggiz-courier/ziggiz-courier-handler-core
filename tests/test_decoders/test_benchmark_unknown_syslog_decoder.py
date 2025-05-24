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
Benchmark for UnknownSyslogDecoder using pytest-benchmark.
Run with: pytest -m benchmark --benchmark-only
"""

# Third-party imports
import pytest

# Local/package imports
from ziggiz_courier_handler_core.decoders.unknown_syslog_decoder import (
    UnknownSyslogDecoder,
)

UNKNOWN_SAMPLE = '<34>1 2025-05-12T23:20:50.52Z mymachine app 1234 ID47 [exampleSDID@32473 iut="3" eventSource="Application"] BOMAn application event log entry...'


@pytest.mark.benchmark
def test_benchmark_unknown_syslog_decode(benchmark):
    decoder = UnknownSyslogDecoder()
    benchmark(lambda: decoder.decode(UNKNOWN_SAMPLE))
