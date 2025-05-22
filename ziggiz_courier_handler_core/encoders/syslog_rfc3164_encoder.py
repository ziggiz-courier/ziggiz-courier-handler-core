# -*- coding: utf-8 -*-
# SPDX-License-Identifier: BSL-1.1
# Copyright (c) 2025 Ziggiz Inc.
#
# This file is part of the ziggiz-courier-core-data-processing and is licensed under the
# Business Source License 1.1. You may not use this file except in
# compliance with the License. You may obtain a copy of the License at:
# https://github.com/ziggiz-courier/ziggiz-courier-core-data-processing/blob/main/LICENSE
#
"""Syslog RFC3164 encoder implementation."""

# Standard library imports

# Local/package imports
from ziggiz_courier_handler_core.encoders.base import Encoder
from ziggiz_courier_handler_core.models.syslog_rfc3164 import SyslogRFC3164Message


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
