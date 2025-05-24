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
Benchmark for SyslogRFC3164Decoder using pytest-benchmark.
Run with: pytest -m benchmark --benchmark-only
"""

# Third-party imports
import pytest

# Local/package imports
from ziggiz_courier_handler_core.decoders.syslog_rfc3164_decoder import (
    SyslogRFC3164Decoder,
)

RFC3164_SAMPLE = "<34>May 12 23:20:50 mymachine su: This is a BSD syslog message."


@pytest.mark.benchmark
def test_benchmark_syslog_rfc3164_decode(benchmark):
    decoder = SyslogRFC3164Decoder()
    benchmark(lambda: decoder.decode(RFC3164_SAMPLE))
