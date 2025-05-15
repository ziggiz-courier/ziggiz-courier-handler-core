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
Unit tests for UnknownSyslogDecoder covering Palo Alto NGFW TRAFFIC log types in RFC3164 and RFC5424 formats.
"""
# Standard library imports
import random

from datetime import datetime

# Third-party imports
import pytest

# Local/package imports
from core_data_processing.decoders.unknown_syslog_decoder import UnknownSyslogDecoder
from core_data_processing.models.syslog_rfc_base import SyslogRFCBaseModel


@pytest.mark.integration
def test_decode_unknown_paloalto_traffic_rfc3164():
    dt = datetime.now().astimezone()
    date = dt.strftime("%b %d %H:%M:%S")
    host_options = [
        "10.0.0.1",
        "palo-ngfw",
        "paloalto.example.com",
    ]
    host = random.choice(host_options)
    # Example RFC3164 syslog message for Palo Alto NGFW TRAFFIC log
    msg = f"<134>{date} {host} 1,2025/05/13 12:34:56,001122334455,TRAFFIC,drop,1,2025/05/13,12:34:56,10.1.1.1,10.2.2.2,0.0.0.0,0.0.0.0,Allow-All,ethernet1/1,ethernet1/2,ethernet1/1,ethernet1/2,Test-Rule,2025/05/13 12:34:56,1,1,0,0,0,0,0x0,udp,deny,0,0,0,0,,paloalto,from-policy"
    decoder = UnknownSyslogDecoder()
    result = decoder.decode(msg)
    assert isinstance(result, SyslogRFCBaseModel)
    syslog_result = SyslogRFCBaseModel.model_validate(result)
    assert syslog_result.structure_classification.vendor == "paloalto"
    assert syslog_result.structure_classification.product == "ngfw"
    assert syslog_result.event_data.get("type", "").lower() == "traffic"


@pytest.mark.integration
def test_decode_unknown_paloalto_traffic_rfc5424():
    dt = datetime.now().astimezone()
    date = dt.strftime("%Y-%m-%dT%H:%M:%S.%f%z")
    host = "paloalto-ngfw"
    # Example RFC5424 syslog message for Palo Alto NGFW TRAFFIC log
    # app_name, proc_id, msg_id are set to - (None)
    msg = f"<134>1 {date} {host} - - - - 1,2025/05/13 12:34:56,001122334455,TRAFFIC,allow,1,2025/05/13,12:34:56,10.1.1.1,10.2.2.2,0.0.0.0,0.0.0.0,Allow-All,ethernet1/1,ethernet1/2,ethernet1/1,ethernet1/2,Test-Rule,2025/05/13 12:34:56,1,1,0,0,0,0,0x0,tcp,allow,0,0,0,0,,paloalto,from-policy"
    decoder = UnknownSyslogDecoder()
    result = decoder.decode(msg)
    assert isinstance(result, SyslogRFCBaseModel)
    syslog_result = SyslogRFCBaseModel.model_validate(result)
    assert syslog_result.structure_classification.vendor == "paloalto"
    assert syslog_result.structure_classification.product == "ngfw"
    assert syslog_result.event_data.get("type", "").lower() == "traffic"
