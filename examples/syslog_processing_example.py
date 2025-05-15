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
"""Example application demonstrating the core-data-processing library.

This script processes a sample syslog message through the pipeline and outputs it in different formats.
"""

# Standard library imports
import json
import logging

# Third-party imports
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter

# Local/package imports
from core_data_processing.adapters.transformers import SyslogToCommonEventAdapter
from core_data_processing.decoders.syslog_rfc5424_decoder import SyslogRFC5424Decoder
from core_data_processing.encoders.json_encoder import JSONEncoder
from core_data_processing.encoders.otel_encoder import OtelSpanEncoder


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
