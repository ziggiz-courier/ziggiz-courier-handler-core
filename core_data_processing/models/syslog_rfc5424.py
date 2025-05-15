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
"""Syslog RFC5424 message model.

This module defines data models for the Syslog protocol as specified in RFC5424.
See: https://tools.ietf.org/html/rfc5424
"""

# Standard library imports
from datetime import datetime
from typing import Dict, Optional

# Local/package imports
from core_data_processing.models.syslog_rfc_base import SyslogRFCCommonModel


class SyslogRFC5424Message(SyslogRFCCommonModel):
    """Model representing a syslog message compliant with RFC5424 standard.

    The RFC5424 format specifies the following structure:
    <PRI>VERSION TIMESTAMP HOSTNAME APP-NAME PROCID MSGID STRUCTURED-DATA MSG

    Where PRI is calculated as (facility * 8) + severity
    """

    # Core syslog message fields
    timestamp: (
        datetime  # Required message timestamp (overrides optional BaseModel.timestamp)
    )
    # hostname, app_name, and proc_id are inherited from SyslogRFCCommonModel
    msg_id: Optional[str] = None  # Identifies the message type
    # Structured data as defined in RFC5424 section 6.3
    # Format: {SD_ID: {PARAM_NAME: PARAM_VALUE, ...}, ...}
    structured_data: Optional[Dict[str, Dict[str, str]]] = None
