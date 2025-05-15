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
"""Integration tests for the complete data processing pipeline."""

# Standard library imports
import json

# Third-party imports
import pytest

# Local/package imports
from core_data_processing.adapters.transformers import SyslogToCommonEventAdapter
from core_data_processing.decoders.syslog_rfc5424_decoder import SyslogRFC5424Decoder
from core_data_processing.encoders.json_encoder import JSONEncoder


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
