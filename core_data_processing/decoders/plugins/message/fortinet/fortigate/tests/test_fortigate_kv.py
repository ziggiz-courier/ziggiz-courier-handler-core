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
Unit tests for UnknownSyslogDecoder covering all supported output classes for FortiGate plugin context.
"""
# Standard library imports
import random

from datetime import datetime

# Third-party imports
import pytest

# Local/package imports
from core_data_processing.decoders.unknown_syslog_decoder import UnknownSyslogDecoder
from core_data_processing.models.syslog_rfc_base import SyslogRFCBaseModel


@pytest.mark.unit
def test_decode_unknown_fortigate():
    dt = datetime.now().astimezone()
    date = dt.strftime("%Y-%m-%d")
    time = dt.strftime("%H:%M:%S")
    eventtime_epoch = int(dt.timestamp())
    host_options = [
        "192.168.1.1",
        "2001:db8::1",
        "fortigate-host",
        "fortigate.example.com",
    ]
    host = random.choice(host_options)
    msg = (
        f"<111>date={date} time={time} devname={host} devid=FG800C3912801080 "
        f"eventtime={eventtime_epoch} logid=0004000017 type=traffic subtype=sniffer level=notice vd=root "
        f'srcip=fe80::20c:29ff:fe77:20d4 srcintf="port3" dstip=ff02::1:ff77:20d4 dstintf="port3" sessionid=408903 '
        f'proto=58 action=accept policyid=2 dstcountry="Reserved" srccountry="Reserved" trandisp=snat transip=:: '
        f'transport=0 service="icmp6/131/0" duration=36 sentbyte=0 rcvdbyte=40 sentpkt=0 rcvdpkt=0 appid=16321 '
        f'app="IPv6.ICMP" appcat="Network.Service" apprisk=elevated applist="sniffer-profile" appact=detected '
        f"utmaction=allow countapp=1"
    )
    decoder = UnknownSyslogDecoder()
    result = decoder.decode(msg)
    assert isinstance(result, SyslogRFCBaseModel)
    syslog_result = SyslogRFCBaseModel.model_validate(result)
    assert syslog_result.structure_classification.vendor == "fortinet"
    assert syslog_result.structure_classification.product == "fortigate"
    assert "utmaction" in syslog_result.event_data
    # assert syslog_result.message == msg
