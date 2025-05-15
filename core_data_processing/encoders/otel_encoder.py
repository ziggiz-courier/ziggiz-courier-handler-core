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
"""OpenTelemetry encoder implementation."""

# Standard library imports

# Third-party imports
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import Span
from opentelemetry.trace import Status, StatusCode

# Local/package imports
from core_data_processing.encoders.base import Encoder
from core_data_processing.models.common import CommonEvent


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
            span.set_attribute("event.timestamp", model.timestamp.isoformat())
            # Also add event_time if it's different from timestamp
            if model.event_time and model.event_time != model.timestamp:
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

            return span
