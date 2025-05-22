#!/usr/bin/env python3
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
Example usage for Courier Data Processing Syslog RFC5424 components.

This script demonstrates how to use the renamed SyslogRFC5424 components and
the backward compatibility provided by the old names.
"""

# Local/package imports
from ziggiz_courier_handler_core import (
    JSONEncoder,
    SyslogRFC5424Decoder,
    SyslogToCommonEventAdapter,
)

# Note: For backward compatibility, you can still use the old names:
# from ziggiz_courier_handler_core import SyslogMessage, SyslogDecoder


def parse_and_process_syslog():
    """Process a sample RFC5424 syslog message."""
    # Sample RFC5424 syslog message
    raw_syslog = (
        "<34>1 2025-05-09T12:30:00Z test-host app1 1234 ID47 "
        '[test@32473 iut="3"] This is a test message'
    )

    # Create pipeline components
    decoder = SyslogRFC5424Decoder()
    adapter = SyslogToCommonEventAdapter()
    encoder = JSONEncoder()

    # Process the message through the pipeline
    print("\nProcessing syslog message...")
    syslog_message = decoder.decode(raw_syslog)
    print(f"Decoded syslog message: {syslog_message}")

    common_event = adapter.transform(syslog_message)
    print(f"Transformed to common event: {common_event}")

    json_result = encoder.encode(common_event)
    print(f"Encoded to JSON: {json_result}")

    print("\nProcessing complete!")


if __name__ == "__main__":
    print("=== Courier Data Processing - SyslogRFC5424 Components ===")
    parse_and_process_syslog()
