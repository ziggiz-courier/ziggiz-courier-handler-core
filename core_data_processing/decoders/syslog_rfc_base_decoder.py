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
"""Syslog RFC Base decoder implementation for basic PRI extraction."""

# Local/package imports
from core_data_processing.decoders.base import Decoder
from core_data_processing.decoders.message_decoder_plugins import get_message_decoders
from core_data_processing.models.syslog_rfc_base import SyslogRFCBaseModel


class SyslogRFCBaseDecoder(Decoder[SyslogRFCBaseModel]):
    """Decoder for basic syslog messages with only PRI field extraction.

    This decoder handles the simple format: <PRI>MESSAGE and extracts only the
    priority value and the message content, returning a basic SyslogRFCBaseModel.

    Unlike more specific RFC format decoders (RFC3164, RFC5424), this decoder
    makes no attempt to parse timestamp, hostname, or other structured fields,
    and simply returns the message starting after the first non-space following
    the closing angle bracket.

    This implementation uses character-by-character parsing for optimized performance
    compared to regex-based parsing.
    """

    def decode(self, raw_data: str, parsing_cache: dict = None) -> SyslogRFCBaseModel:
        """
        Decode a syslog message by extracting the PRI field and remaining message.

        This optimized decoder extracts the priority value and returns the message
        content starting with the first non-space character after the closing
        angle bracket, using character-by-character parsing instead of regex.

        Args:
            raw_data: The raw syslog message as string
            parsing_cache: Optional dictionary for caching parsing data

        Returns:
            A SyslogRFCBaseModel instance representing the decoded data

        Raises:
            ValueError: If the raw_data does not match basic syslog format
        """
        if parsing_cache is None:
            parsing_cache = self.event_parsing_cache

        if not raw_data or len(raw_data) < 3:  # Needs at least <>x
            raise ValueError(f"Invalid syslog format: {raw_data}")

        # Ensure the message starts with <
        if raw_data[0] != "<":
            raise ValueError(f"Invalid syslog format: {raw_data}")

        # Find closing bracket
        close_bracket_pos = raw_data.find(">")
        if close_bracket_pos == -1:
            raise ValueError(f"Invalid syslog format: {raw_data}")

        # Extract PRI value (everything between < and >)
        pri = raw_data[1:close_bracket_pos]

        # Check for malformed PRI with spaces (like "< >" case)
        if " " in pri:
            raise ValueError(f"Invalid syslog format: {raw_data}")

        # Handle empty PRI
        if pri.strip() == "":
            pri = None

        # Find first non-whitespace after closing bracket
        message_start = close_bracket_pos + 1
        message_len = len(raw_data)

        while message_start < message_len and raw_data[message_start].isspace():
            message_start += 1

        # Extract message (everything after the closing > and any whitespace)
        message = raw_data[message_start:] if message_start < message_len else ""

        # Create the model using from_priority which handles validation
        model = SyslogRFCBaseModel.from_priority(pri, message=message)

        # --- Plugin-based event_data decoding ---
        if self.__class__ is SyslogRFCBaseDecoder:
            plugins = get_message_decoders(SyslogRFCBaseModel)
            if plugins and model.message:
                for plugin in plugins:
                    if hasattr(plugin, "decode"):  # Class-based plugin
                        if plugin.decode(model):
                            break
                    else:  # Function-based plugin (for backward compatibility)
                        if plugin(model, parsing_cache=parsing_cache):
                            break

        return model
