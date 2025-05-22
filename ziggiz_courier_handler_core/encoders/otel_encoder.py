# -*- coding: utf-8 -*-
# SPDX-License-Identifier: BSL-1.1
# Copyright (c) 2025 Ziggiz Inc.
#
# This file is part of the ziggiz-courier-core-data-processing and is licensed under the
# Business Source License 1.1. You may not use this file except in
# compliance with the License. You may obtain a copy of the License at:
# https://github.com/ziggiz-courier/ziggiz-courier-core-data-processing/blob/main/LICENSE
#
"""OpenTelemetry encoder implementation."""

# Standard library imports

# Standard library imports
from typing import cast

# Third-party imports
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import Span
from opentelemetry.trace import Status, StatusCode

# Local/package imports
from ziggiz_courier_handler_core.encoders.base import Encoder
from ziggiz_courier_handler_core.models.common import CommonEvent


class OtelSpanEncoder(Encoder[CommonEvent, Span]):
    """Encoder that converts a CommonEvent to an OpenTelemetry Span."""

    # Mapping from common event severity to OTel status code
    SEVERITY_TO_STATUS = {
        "EMERGENCY": StatusCode.ERROR,
        "ALERT": StatusCode.ERROR,
        "CRITICAL": StatusCode.ERROR,
        "ERROR": StatusCode.ERROR,
        "WARNING": StatusCode.ERROR,
        "NOTICE": StatusCode.OK,
        "INFO": StatusCode.OK,
        "DEBUG": StatusCode.OK,
        "UNKNOWN": StatusCode.UNSET,
    }

    def __init__(self, tracer_provider):
        """
        Initialize the OTel encoder with a tracer provider.

        Args:
            tracer_provider: An OpenTelemetry tracer provider
        """
        self.tracer_provider = tracer_provider

    def encode(self, model: CommonEvent) -> Span:
        """
        Encode a CommonEvent to an OpenTelemetry Span.

        Args:
            model: The CommonEvent to encode

        Returns:
            An OpenTelemetry Span
        """
        # Create a tracer with the source system as the name
        tracer = self.tracer_provider.get_tracer(model.source_system)

        # Create resource attributes
        resource_attributes = {
            "service.name": model.source_system,
            "service.namespace": "courier",
            "service.version": "1.0.0",
        }
        # Create resource which is automatically used by the tracer via the resource provider
        Resource.create(resource_attributes)

        # Start a span with the event type as the name
        with tracer.start_as_current_span(
            model.event_type,
            start_time=model.timestamp,
        ) as span:
            # Set span attributes
            span.set_attribute("event.id", model.event_id)
            if model.timestamp:
                span.set_attribute("event.timestamp", model.timestamp.isoformat())
            # Also add event_time if it's different from timestamp
            if (
                model.event_time
                and model.timestamp
                and model.event_time != model.timestamp
            ):
                span.set_attribute("event.time", model.event_time.isoformat())
            span.set_attribute("source.component", model.source_component)
            span.set_attribute("severity.text", model.severity)

            # Add all custom attributes
            for key, value in model.attributes.items():
                span.set_attribute(key, value)

            # Set status based on severity
            status_code = self.SEVERITY_TO_STATUS.get(model.severity, StatusCode.UNSET)
            if status_code == StatusCode.ERROR:
                span.set_status(Status(status_code, model.message))
            else:
                span.set_status(Status(status_code))

            # Add tags as events
            for tag in model.tags:
                span.add_event(f"tag:{tag}")

            # Add message as an event
            span.add_event("message", {"content": model.message})

            return cast(Span, span)
