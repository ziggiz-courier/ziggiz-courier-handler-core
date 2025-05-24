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
Benchmark for SyslogRFC5424Decoder using pytest-benchmark.
Run with: pytest -m benchmark --benchmark-only
"""

# Third-party imports
import pytest

# Local/package imports
from ziggiz_courier_handler_core.decoders.syslog_rfc5424_decoder import (
    SyslogRFC5424Decoder,
)

RFC5424_SAMPLE = '<34>1 2025-05-12T23:20:50.52Z mymachine app 1234 ID47 [exampleSDID@32473 iut="3" eventSource="Application"] BOMAn application event log entry...'


@pytest.mark.benchmark
def test_benchmark_syslog_rfc5424_decode(benchmark):
    decoder = SyslogRFC5424Decoder()
    benchmark(lambda: decoder.decode(RFC5424_SAMPLE))
