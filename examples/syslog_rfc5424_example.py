#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2025 ziggiz
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
Example usage for Courier Data Processing Syslog RFC5424 components.

This script demonstrates how to use the renamed SyslogRFC5424 components and
the backward compatibility provided by the old names.
"""

# Local/package imports
from core_data_processing import (
    JSONEncoder,
    SyslogRFC5424Decoder,
    SyslogToCommonEventAdapter,
)

# Note: For backward compatibility, you can still use the old names:
# from core_data_processing import SyslogMessage, SyslogDecoder


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
