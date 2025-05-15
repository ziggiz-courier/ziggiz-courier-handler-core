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
"""Decoders for courier data processing."""

# Local/package imports
from core_data_processing.decoders.base import Decoder
from core_data_processing.decoders.syslog_rfc3164_decoder import SyslogRFC3164Decoder
from core_data_processing.decoders.syslog_rfc5424_decoder import SyslogRFC5424Decoder
from core_data_processing.decoders.unknown_syslog_decoder import UnknownSyslogDecoder
from core_data_processing.decoders.utils import *

__all__ = [
    "Decoder",
    "SyslogRFC5424Decoder",
    "SyslogRFC3164Decoder",
    "UnknownSyslogDecoder",
]
