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
"""Syslog RFC3164 encoder implementation."""

# Standard library imports

# Local/package imports
from core_data_processing.encoders.base import Encoder
from core_data_processing.models.syslog_rfc3164 import SyslogRFC3164Message


class SyslogRFC3164Encoder(Encoder[SyslogRFC3164Message, str]):
    """Encoder for syslog messages in RFC3164 format (BSD-style syslog)."""

    def encode(self, data: SyslogRFC3164Message) -> str:
        """
        Encode a SyslogRFC3164Message into a string following RFC3164 format.

        This method implements a simplified encoding of RFC3164 messages, focusing on the
        priority and message content. For a more complete implementation, additional
        components like timestamp, hostname, and TAG could be included in the following format:
        <PRI>TIMESTAMP HOSTNAME APP-NAME[PROCID]: MESSAGE

        Args:
            data: The SyslogRFC3164Message to encode

        Returns:
            A string representing the encoded syslog message in the format <PRI>MESSAGE
        """
        # Calculate priority
        pri = data.get_priority()

        # Return formatted string with just priority and message
        # A more complete implementation would include timestamp, hostname, etc.
        return f"<{pri}>{data.message}"
