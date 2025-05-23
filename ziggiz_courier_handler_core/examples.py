# -*- coding: utf-8 -*-
# SPDX-License-Identifier: BSL-1.1
# Copyright (c) 2025 Ziggiz Inc.
#
# This file is part of the ziggiz-courier-core-data-processing and is licensed under the
# Business Source License 1.1. You may not use this file except in
# compliance with the License. You may obtain a copy of the License at:
# https://github.com/ziggiz-courier/ziggiz-courier-core-data-processing/blob/main/LICENSE
#
"""Example usage of the courier data processing package."""

# Standard library imports
import logging

# Third-party imports
from opentelemetry.sdk.trace import TracerProvider

# Local/package imports
from ziggiz_courier_handler_core.adapters.transformers import SyslogToCommonEventAdapter
from ziggiz_courier_handler_core.decoders.syslog_rfc5424_decoder import (
    SyslogRFC5424Decoder,
)
from ziggiz_courier_handler_core.encoders.json_encoder import JSONEncoder
from ziggiz_courier_handler_core.encoders.otel_encoder import OtelSpanEncoder


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
        if syslog_message is None:
            raise ValueError(
                "Decoded syslog message is None and cannot be transformed."
            )
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
        if syslog_message is None:
            raise ValueError(
                "Decoded syslog message is None and cannot be transformed."
            )
        common_event = adapter.transform(syslog_message)

        # Encode to OTel span and export it
        _ = otel_encoder.encode(common_event)

        # The span will be automatically exported based on the tracer provider configuration
    except Exception as e:
        logging.error(f"Error processing syslog message to OTel: {e}")
        raise
