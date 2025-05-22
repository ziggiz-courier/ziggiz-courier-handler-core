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

"""Example application demonstrating the ziggiz-courier-handler-core library.

This script processes a sample syslog message through the pipeline and outputs it in different formats.
"""

# Standard library imports
import json
import logging

# Third-party imports
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter

# Local/package imports
from ziggiz_courier_handler_core.adapters.transformers import SyslogToCommonEventAdapter
from ziggiz_courier_handler_core.decoders.syslog_rfc5424_decoder import (
    SyslogRFC5424Decoder,
)
from ziggiz_courier_handler_core.encoders.json_encoder import JSONEncoder
from ziggiz_courier_handler_core.encoders.otel_encoder import OtelSpanEncoder


def configure_logging():
    """Configure basic logging."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )


def configure_opentelemetry():
    """Configure OpenTelemetry with console exporter."""
    # Create a tracer provider
    tracer_provider = TracerProvider()

    # Create a console exporter
    console_exporter = ConsoleSpanExporter()

    # Add the exporter to the tracer provider
    tracer_provider.add_span_processor(BatchSpanProcessor(console_exporter))

    return tracer_provider


def process_syslog_to_json(raw_syslog):
    """Process a syslog message to JSON."""
    # Create components
    decoder = SyslogRFC5424Decoder()
    adapter = SyslogToCommonEventAdapter()
    encoder = JSONEncoder()

    # Process through the pipeline
    syslog_message = decoder.decode(raw_syslog)
    common_event = adapter.transform(syslog_message)
    json_output = encoder.encode(common_event)

    return json_output


def process_syslog_to_otel(raw_syslog, tracer_provider):
    """Process a syslog message to OpenTelemetry."""
    # Create components
    decoder = SyslogRFC5424Decoder()
    adapter = SyslogToCommonEventAdapter()
    encoder = OtelSpanEncoder(tracer_provider)

    # Process through the pipeline
    syslog_message = decoder.decode(raw_syslog)
    common_event = adapter.transform(syslog_message)
    span = encoder.encode(common_event)

    return span


def main():
    """Run the example application."""
    configure_logging()
    logger = logging.getLogger(__name__)

    # Sample syslog message
    raw_syslog = (
        "<34>1 2023-05-09T02:33:52.123Z myhostname app 1234 ID47 "
        '[exampleSDID@32473 iut="3" eventSource="Application" eventID="1011"] '
        "An application event log entry"
    )

    logger.info("Processing syslog message to JSON")
    json_output = process_syslog_to_json(raw_syslog)
    print("\nJSON Output:")
    print(json.dumps(json.loads(json_output), indent=2))

    logger.info("Processing syslog message to OpenTelemetry")
    tracer_provider = configure_opentelemetry()
    process_syslog_to_otel(raw_syslog, tracer_provider)
    print("\nOpenTelemetry span exported to console")


if __name__ == "__main__":
    main()
