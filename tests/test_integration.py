# -*- coding: utf-8 -*-
# # SPDX-License-Identifier: BSL-1.1
# # Copyright (c) 2025 Ziggiz Inc.
# #
# # This file is part of the ziggiz-courier-core-data-processing and is licensed under the
# # Business Source License 1.1. You may not use this file except in
# # compliance with the License. You may obtain a copy of the License at:
# # https://github.com/ziggiz-courier/ziggiz-courier-core-data-processing/blob/main/LICENSE
"""Integration tests for the complete data processing pipeline."""

# Standard library imports
import json

# Third-party imports
import pytest

# Local/package imports
from ziggiz_courier_handler_core.adapters.transformers import SyslogToCommonEventAdapter
from ziggiz_courier_handler_core.decoders.syslog_rfc5424_decoder import (
    SyslogRFC5424Decoder,
)
from ziggiz_courier_handler_core.encoders.json_encoder import JSONEncoder


class TestIntegration:
    """Integration tests for the complete data processing pipeline."""

    @pytest.mark.integration
    def test_syslog_to_json_pipeline(self):
        """Test the complete pipeline from syslog to JSON."""
        # Sample syslog message
        raw_syslog = (
            "<34>1 2023-05-09T02:33:52.123Z myhostname app 1234 ID47 "
            '[exampleSDID@32473 iut="3" eventSource="Application" eventID="1011"] '
            "An application event log entry"
        )

        # Create components
        decoder = SyslogRFC5424Decoder()
        adapter = SyslogToCommonEventAdapter()
        encoder = JSONEncoder()

        # Process through the pipeline
        syslog_message = decoder.decode(raw_syslog)
        common_event = adapter.transform(syslog_message)
        json_output = encoder.encode(common_event)

        # Verify the result
        data = json.loads(json_output)

        # Check key fields
        assert data["source_system"] == "myhostname"
        assert data["message"] == "An application event log entry"
        assert data["severity"] == "CRITICAL"  # Mapped from severity 2

        # Check structured data was properly transformed
        assert "exampleSDID@32473" in data["tags"]
        assert data["attributes"]["exampleSDID@32473.iut"] == "3"
        assert data["attributes"]["exampleSDID@32473.eventSource"] == "Application"
        assert data["attributes"]["exampleSDID@32473.eventID"] == "1011"
