# -*- coding: utf-8 -*-
# SPDX-License-Identifier: BSL-1.1
# Copyright (c) 2025 Ziggiz Inc.
#
# This file is part of the ziggiz-courier-core-data-processing and is licensed under the
# Business Source License 1.1. You may not use this file except in
# compliance with the License. You may obtain a copy of the License at:
# https://github.com/ziggiz-courier/ziggiz-courier-core-data-processing/blob/main/LICENSE
#
"""Decoders for courier data processing."""

# Local/package imports
from ziggiz_courier_handler_core.decoders.base import Decoder
from ziggiz_courier_handler_core.decoders.message_decoder_plugins import (
    MessageDecoderPlugin,
    get_message_decoders,
    register_message_decoder,
)
from ziggiz_courier_handler_core.decoders.syslog_rfc3164_decoder import (
    SyslogRFC3164Decoder,
)
from ziggiz_courier_handler_core.decoders.syslog_rfc5424_decoder import (
    SyslogRFC5424Decoder,
)
from ziggiz_courier_handler_core.decoders.unknown_syslog_decoder import (
    UnknownSyslogDecoder,
)
from ziggiz_courier_handler_core.decoders.utils import *

__all__ = [
    "Decoder",
    "MessageDecoderPlugin",
    "register_message_decoder",
    "get_message_decoders",
    "SyslogRFC5424Decoder",
    "SyslogRFC3164Decoder",
    "UnknownSyslogDecoder",
]
