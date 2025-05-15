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
