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
"""Models for courier data processing."""

# Local/package imports
from core_data_processing.models.event_envelope_base import BaseModel
from core_data_processing.models.syslog_rfc3164 import (
    SyslogRFC3164Message,
)
from core_data_processing.models.syslog_rfc5424 import (
    SyslogRFC5424Message,
)
from core_data_processing.models.syslog_rfc_base import SyslogRFCBaseModel

__all__ = [
    "BaseModel",
    "SyslogRFCBaseModel",
    "SyslogRFC5424Message",
    "SyslogRFC3164Message",
]
