# -*- coding: utf-8 -*-
# SPDX-License-Identifier: BSL-1.1
# Copyright (c) 2025 Ziggiz Inc.
#
# This file is part of the ziggiz-courier-core-data-processing and is licensed under the
# Business Source License 1.1. You may not use this file except in
# compliance with the License. You may obtain a copy of the License at:
# https://github.com/ziggiz-courier/ziggiz-courier-core-data-processing/blob/main/LICENSE
"""Models for representing metadata about data source connections."""

# Standard library imports
from abc import ABC
from enum import Enum
from typing import Optional

# Third-party imports
from pydantic import BaseModel as PydanticBaseModel


# Well-known IP protocol enumeration
class IPProtocol(int, Enum):
    """
    Enum for well-known IP protocol numbers (IANA assigned, see RFC 5237).
    """

    TCP = 6
    UDP = 17


class MetaDataConnection(PydanticBaseModel, ABC):
    """
    Abstract base class for metadata about a data source connection.

    This class should be subclassed for specific connection types.
    """

    class Config:
        arbitrary_types_allowed = True
        frozen = False


class MetaDataConnectionNetwork(MetaDataConnection):
    """
    Metadata for a network-based connection.

    Args:
        ip_proto (str): IP protocol (e.g., 'tcp', 'udp').
        source_port (int): Source port number.
        source_ip (str): Source IP address.
    """

    ip_proto: IPProtocol
    source_port: int
    source_ip: str


class MetaDataConnectionUnix(MetaDataConnection):
    """
    Metadata for a Unix domain socket connection.

    Args:
        socket_path (str): Path to the Unix socket file.
        user (Optional[str]): User owning the socket.
        group (Optional[str]): Group owning the socket.
    """

    socket_path: str
    user: Optional[str] = None
    group: Optional[str] = None


class MetaDataConnectionFile(MetaDataConnection):
    """
    Metadata for a file-based connection.

    Args:
        file_path (str): Path to the file.
    """

    file_path: str
