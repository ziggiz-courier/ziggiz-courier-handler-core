# -*- coding: utf-8 -*-
# # SPDX-License-Identifier: BSL-1.1
# # Copyright (c) 2025 Ziggiz Inc.
# #
# # This file is part of the ziggiz-courier-core-data-processing and is licensed under the
# # Business Source License 1.1. You may not use this file except in
# # compliance with the License. You may obtain a copy of the License at:
# # https://github.com/ziggiz-courier/ziggiz-courier-core-data-processing/blob/main/LICENSE
"""Syslog base model for shared components between different RFC formats.

This module defines base data models for Syslog protocols that share common
elements like facility and severity.
"""

# Standard library imports
from abc import ABC
from enum import IntEnum
from typing import Optional, Union

# Local/package imports
from core_data_processing.models.event_envelope_base import BaseModel


class Facility(IntEnum):
    """Syslog facility codes as defined in RFC 5424.

    Facility values range from 0 to 23 and identify the source of a message.
    """

    KERN = 0  # kernel messages
    USER = 1  # user-level messages
    MAIL = 2  # mail system
    DAEMON = 3  # system daemons
    AUTH = 4  # security/authorization messages
    SYSLOG = 5  # messages generated internally by syslogd
    LPR = 6  # line printer subsystem
    NEWS = 7  # network news subsystem
    UUCP = 8  # UUCP subsystem
    CRON = 9  # clock daemon
    AUTHPRIV = 10  # security/authorization messages (private)
    FTP = 11  # FTP daemon
    NTP = 12  # NTP subsystem
    LOGAUDIT = 13  # log audit
    LOGALERT = 14  # log alert
    CLOCK = 15  # clock daemon
    LOCAL0 = 16  # local use 0
    LOCAL1 = 17  # local use 1
    LOCAL2 = 18  # local use 2
    LOCAL3 = 19  # local use 3
    LOCAL4 = 20  # local use 4
    LOCAL5 = 21  # local use 5
    LOCAL6 = 22  # local use 6
    LOCAL7 = 23  # local use 7

    def __str__(self) -> str:
        """Return a string representation including the name and value."""
        return f"{self.name}({self.value})"

    def __repr__(self) -> str:
        """Return a developer-friendly representation."""
        return str(self)


class Severity(IntEnum):
    """Syslog severity levels as defined in RFC 5424.

    Severity values range from 0 to 7 and indicate the urgency of a message.
    Lower numeric values represent higher severity:
    - 0 (EMERGENCY) is the most severe
    - 7 (DEBUG) is the least severe

    This enum supports intuitive severity comparisons with a custom implementation:
    - severity >= Severity.ERROR will be True for ERROR, CRITICAL, ALERT, EMERGENCY
    - severity <= Severity.WARNING will be True for WARNING, NOTICE, INFO, DEBUG

    When comparing severity levels, a lower numeric value is considered "more severe"
    than a higher numeric value. This results in intuitive comparisons:
    - EMERGENCY > ALERT (because EMERGENCY is more severe than ALERT)
    - DEBUG < INFO (because DEBUG is less severe than INFO)
    """

    EMERGENCY = 0  # System is unusable
    ALERT = 1  # Action must be taken immediately
    CRITICAL = 2  # Critical conditions
    ERROR = 3  # Error conditions
    WARNING = 4  # Warning conditions
    NOTICE = 5  # Normal but significant condition
    INFO = 6  # Informational messages
    DEBUG = 7  # Debug-level messages

    def __str__(self) -> str:
        """Return a string representation including the name and value."""
        return f"{self.name}({self.value})"

    def __repr__(self) -> str:
        """Return a developer-friendly representation."""
        return str(self)

    def __hash__(self) -> int:
        """Enable using this enum in sets and as dictionary keys."""
        return hash(self.value)

    # Custom comparison operators to make severity levels intuitively comparable
    # Lower numbers (more severe) are "greater than" higher numbers (less severe)

    def __lt__(self, other):
        if isinstance(other, Severity):
            return self.value > other.value
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, Severity):
            return self.value < other.value
        return NotImplemented

    def __le__(self, other):
        if isinstance(other, Severity):
            return self.value >= other.value
        return NotImplemented

    def __ge__(self, other):
        if isinstance(other, Severity):
            return self.value <= other.value
        return NotImplemented

    def __eq__(self, other):
        if isinstance(other, Severity):
            return self.value == other.value
        return NotImplemented


class SyslogRFCBaseModel(BaseModel):
    """Base model for all syslog RFC formats with common priority field components.

    The priority (PRI) field is common across syslog formats, calculated as:
    PRI = facility * 8 + severity

    Where:
    - facility: value between 0-23 representing the message source
    - severity: value between 0-7 representing the message urgency
    """

    # Syslog priority field components common across formats
    facility: int  # Facility code (0-23) indicating the source of the message
    severity: int  # Severity code (0-7) indicating the urgency of the message

    def get_priority(self) -> int:
        """Calculate the priority value from facility and severity.

        Returns:
            The calculated priority (PRI) value
        """
        # Use the positive severity value (0-7) for priority calculation
        severity_value = self.severity & 0x07
        return (self.facility << 3) | severity_value

    def get_facility_enum(self) -> Facility:
        """Get the facility as an enum value.

        Returns:
            The facility as a Facility enum
        """
        try:
            return Facility(self.facility)
        except ValueError:
            # Default to LOGAUDIT (13) if facility is out of range
            return Facility.LOGAUDIT

    def get_severity_enum(self) -> Severity:
        """Get the severity as an enum value.

        Returns:
            The severity as a Severity enum
        """
        try:
            return Severity(self.severity)
        except ValueError:
            # Default to DEBUG (7) if severity is out of range
            return Severity.DEBUG

    @classmethod
    def from_priority(cls, pri: Union[int, str, None], **kwargs):
        """Create a new instance from a priority value.

        According to RFC specifications, when priority values are invalid
        (zeros, >3 digits, non-numeric), use a default facility value of 13
        (log audit) while preserving the severity if possible.

        Args:
            pri: The priority value from a syslog message
            **kwargs: Additional fields for the model including required timestamp
                      (if not provided, current time will be used)

        Returns:
            A new instance of the model
        """
        # Add current timestamp if not provided
        if "timestamp" not in kwargs:
            # Standard library imports
            from datetime import datetime

            kwargs["timestamp"] = datetime.now()
        # Default facility for invalid inputs as per RFC
        DEFAULT_FACILITY = Facility.LOGAUDIT

        # Validate priority value
        # Non-numeric values should have been filtered before this point
        # but handling it here for robustness
        try:
            pri_int = int(pri)

            # Check for invalid values (negative, too large values, or string of multiple zeros)
            if pri_int < 0:  # Negative values are invalid
                facility = int(DEFAULT_FACILITY)
                severity = int(
                    Severity.DEBUG
                )  # Use default severity for negative values
            elif pri_int >= 1000:  # >3 digits
                facility = int(DEFAULT_FACILITY)
                severity = pri_int & 0x07  # Still extract severity if possible
            elif isinstance(pri, str) and pri.startswith("0") and len(pri) > 1:
                # Handle case of multiple zeros like "000" or "0000" as invalid
                facility = int(DEFAULT_FACILITY)
                severity = int(
                    Severity.EMERGENCY
                )  # Extract severity (always 0 for multiple zeros)
            else:
                # Valid priority value (including single digit "0")
                facility = pri_int >> 3  # Standard calculation
                severity = pri_int & 0x07

            # Cap facility at 23 (max valid facility)
            if facility > 23:
                facility = int(DEFAULT_FACILITY)
        except (ValueError, TypeError):
            # Handle any conversion issues
            facility = int(DEFAULT_FACILITY)
            severity = int(
                Severity.DEBUG
            )  # Use debug severity as default for completely invalid inputs

        return cls(facility=facility, severity=severity, **kwargs)


class SyslogRFCCommonModel(SyslogRFCBaseModel, ABC):
    """Abstract base class for syslog message models with common fields.

    This class extends SyslogRFCBaseModel with commonly shared fields between
    different syslog formats (RFC3164 and RFC5424) to reduce code duplication.

    Common fields included:
    - hostname: machine that originated the message
    - app_name: application that originated the message
    - proc_id: process that originated the message
    """

    hostname: Optional[str] = None  # Identifies the machine that sent the message
    app_name: Optional[str] = None  # Identifies the application that sent the message
    proc_id: Optional[str] = None  # Identifies the process that sent the message
