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
"""Encoders for courier data processing."""

# Local/package imports
from core_data_processing.encoders.base import Encoder
from core_data_processing.encoders.json_encoder import JSONEncoder
from core_data_processing.encoders.otel_encoder import OtelSpanEncoder
from core_data_processing.encoders.syslog_rfc3164_encoder import SyslogRFC3164Encoder

__all__ = ["Encoder", "JSONEncoder", "OtelSpanEncoder", "SyslogRFC3164Encoder"]
