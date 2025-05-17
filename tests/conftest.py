# -*- coding: utf-8 -*-
# # SPDX-License-Identifier: BSL-1.1
# # Copyright (c) 2025 Ziggiz Inc.
# #
# # This file is part of the ziggiz-courier-core-data-processing and is licensed under the
# # Business Source License 1.1. You may not use this file except in
# # compliance with the License. You may obtain a copy of the License at:
# # https://github.com/ziggiz-courier/ziggiz-courier-core-data-processing/blob/main/LICENSE
"""
Reusable pytest fixtures for Ziggiz-Courier tests.
"""
# Standard library imports
from datetime import datetime

# Third-party imports
import pytest


@pytest.fixture(scope="function")
def now_aware():
    """Return a timezone-aware datetime for use in test strings."""
    return datetime.now().astimezone()


@pytest.fixture(
    params=[
        "192.168.1.1",  # IPv4
        "2001:db8::1",  # IPv6
        "fortigate-host",  # simple hostname
        "fortigate.example.com",  # FQDN
    ]
)
def host(request):
    """Return a host string (IPv4, IPv6, hostname, or FQDN)."""
    return request.param
