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
"""Syslog RFC3164 message model (BSD-style syslog).

This module defines data models for the Syslog protocol as specified in RFC3164,
commonly known as the 'BSD syslog protocol', which uses a simpler format than RFC5424.
See: https://tools.ietf.org/html/rfc3164
"""

# Standard library imports

# Local/package imports
from core_data_processing.models.syslog_rfc_base import SyslogRFCCommonModel


class SyslogRFC3164Message(SyslogRFCCommonModel):
    """Model representing a syslog message compliant with RFC3164 standard (BSD syslog).

    The RFC3164 format has a simpler structure than RFC5424:
    <PRI>CONTENT

    Where:
    - PRI: The priority value calculated as facility * 8 + severity
    - CONTENT: The actual message content

    Note: While RFC3164 messages might not always include an explicit timestamp in the message,
    the EventEnvelopeBaseModel requires one. For RFC3164 messages without a timestamp,
    we will use the receipt time set by the decoder.
    """

    # Inherits hostname, app_name, and proc_id from SyslogRFCCommonModel


# from core_data_processing.models.base import BaseEventStructureClassification
# SyslogRFC3164Message.model_rebuild()
