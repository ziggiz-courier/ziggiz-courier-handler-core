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
"""Example usage of the courier data processing package."""

# Standard library imports
import logging

# Third-party imports
from opentelemetry.sdk.trace import TracerProvider

# Local/package imports
from core_data_processing.adapters.transformers import SyslogToCommonEventAdapter
from core_data_processing.decoders.syslog_rfc5424_decoder import SyslogRFC5424Decoder
from core_data_processing.encoders.json_encoder import JSONEncoder
from core_data_processing.encoders.otel_encoder import OtelSpanEncoder


def process_syslog_message(raw_syslog: str) -> str:
    """
    Process a raw syslog message through the pipeline.

    Args:
        raw_syslog: A raw syslog message string

    Returns:
        A JSON string of the processed event
    """
    # Create instances of the components
    syslog_decoder = SyslogRFC5424Decoder()
    adapter = SyslogToCommonEventAdapter()
    json_encoder = JSONEncoder()

    # Process through the pipeline
    try:
        # Decode the raw syslog message
        syslog_message = syslog_decoder.decode(raw_syslog)

        # Transform to common event
        common_event = adapter.transform(syslog_message)

        # Encode to JSON
        json_output = json_encoder.encode(common_event)

        return json_output
    except Exception as e:
        logging.error(f"Error processing syslog message: {e}")
        raise


def process_syslog_to_otel(raw_syslog: str, tracer_provider: TracerProvider) -> None:
    """
    Process a raw syslog message and export as OpenTelemetry span.

    Args:
        raw_syslog: A raw syslog message string
        tracer_provider: An OpenTelemetry tracer provider
    """
    # Create instances of the components
    syslog_decoder = SyslogRFC5424Decoder()
    adapter = SyslogToCommonEventAdapter()
    otel_encoder = OtelSpanEncoder(tracer_provider)

    try:
        # Decode the raw syslog message
        syslog_message = syslog_decoder.decode(raw_syslog)

        # Transform to common event
        common_event = adapter.transform(syslog_message)

        # Encode to OTel span and export it
        _ = otel_encoder.encode(common_event)

        # The span will be automatically exported based on the tracer provider configuration
    except Exception as e:
        logging.error(f"Error processing syslog message to OTel: {e}")
        raise
