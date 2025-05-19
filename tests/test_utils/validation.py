#!/usr/bin/env python
# -*- coding: utf-8 -*-
# # SPDX-License-Identifier: BSL-1.1
# # Copyright (c) 2025 Ziggiz Inc.
# #
# # This file is part of the ziggiz-courier-core-data-processing and is licensed under the
# # Business Source License 1.1. You may not use this file except in
# # compliance with the License. You may obtain a copy of the License at:
# # https://github.com/ziggiz-courier/ziggiz-courier-core-data-processing/blob/main/LICENSE
"""Validation utilities for testing Syslog models and common components."""

# Standard library imports
from typing import Any, Dict, Optional, Type, TypeVar, Union, cast

# Third-party imports
import pytest

# Local/package imports
from ziggiz_courier_handler_core.models.syslog_rfc_base import (
    Facility,
    Severity,
    SyslogRFCBaseModel,
    SyslogRFCCommonModel,
)
from ziggiz_courier_handler_core.models.syslog_rfc3164 import SyslogRFC3164Message
from ziggiz_courier_handler_core.models.syslog_rfc5424 import SyslogRFC5424Message
from ziggiz_courier_handler_core.models.source_producer import SourceProducer


# Type variable for the syslog model types
T = TypeVar("T", bound=SyslogRFCBaseModel)


class InvalidArgumentException(Exception):
    """Raised when invalid arguments are passed to the validation function."""

    pass


def validate_syslog_model(
    model_instance: T,
    *,
    # Common fields for all syslog models
    facility: Optional[Union[Facility, int]] = None,
    severity: Optional[Union[Severity, int]] = None,
    message: Optional[str] = None,
    timestamp: Optional[Any] = None,
    priority: Optional[int] = None,
    # SyslogRFCCommonModel fields
    hostname: Optional[str] = None,
    app_name: Optional[str] = None,
    proc_id: Optional[str] = None,
    # RFC5424 specific fields
    msg_id: Optional[str] = None,
    structured_data: Optional[Dict[str, Dict[str, str]]] = None,
    **kwargs
) -> None:
    """Validate a Syslog model instance against expected values.

    This function validates that the provided Syslog model instance has the expected values for
    each field. It only validates fields for which expected values are provided.

    Args:
        model_instance: The syslog model instance to validate.
        facility: Expected facility value (either Facility enum or int).
        severity: Expected severity value (either Severity enum or int).
        message: Expected message content.
        timestamp: Expected timestamp.
        priority: Expected priority (calculated as facility*8 + severity).
        hostname: Expected hostname (can be explicitly set to None to test None value).
        app_name: Expected application name (can be explicitly set to None to test None value).
        proc_id: Expected process ID (can be explicitly set to None to test None value).
        msg_id: Expected message ID (RFC5424 only, can be explicitly set to None to test None value).
        structured_data: Expected structured data (RFC5424 only, can be explicitly set to None).
        **kwargs: Additional keyword arguments for future expansion.

    Raises:
        InvalidArgumentException: If no expected values are provided for the specific model type.
        AssertionError: If the model instance doesn't match the expected values.
    """
    # Track which arguments were explicitly provided using an inspection approach
    call_params = {
        "facility": "facility" in kwargs or facility is not None,
        "severity": "severity" in kwargs or severity is not None,
        "message": "message" in kwargs or message is not None,
        "timestamp": "timestamp" in kwargs or timestamp is not None,
        "priority": "priority" in kwargs or priority is not None,
        "hostname": "hostname" in kwargs or hostname is not None,
        "app_name": "app_name" in kwargs or app_name is not None,
        "proc_id": "proc_id" in kwargs or proc_id is not None,
        "msg_id": "msg_id" in kwargs or msg_id is not None,
        "structured_data": "structured_data" in kwargs or structured_data is not None,
    }
    
    # Check if any arguments were explicitly provided
    if not any(call_params.values()):
        model_type = type(model_instance).__name__
        raise InvalidArgumentException(
            f"No expected values provided for {model_type} validation"
        )

    # Perform common validations for all SyslogRFCBaseModel instances
    if call_params["facility"]:
        assert model_instance.facility == (
            facility.value if isinstance(facility, Facility) else facility
        ), f"Expected facility {facility}, got {model_instance.facility}"

    if call_params["severity"]:
        assert model_instance.severity == (
            severity.value if isinstance(severity, Severity) else severity
        ), f"Expected severity {severity}, got {model_instance.severity}"

    if call_params["message"]:
        assert (
            model_instance.message == message
        ), f"Expected message '{message}', got '{model_instance.message}'"

    if call_params["timestamp"]:
        assert (
            model_instance.timestamp == timestamp
        ), f"Expected timestamp {timestamp}, got {model_instance.timestamp}"

    if call_params["priority"]:
        actual_priority = model_instance.get_priority()
        assert (
            actual_priority == priority
        ), f"Expected priority {priority}, got {actual_priority}"

    # Perform validations for common model fields (hostname, app_name, proc_id)
    if isinstance(model_instance, SyslogRFCCommonModel):
        if call_params["hostname"]:
            assert (
                model_instance.hostname == hostname
            ), f"Expected hostname {hostname}, got {model_instance.hostname}"

        if call_params["app_name"]:
            assert (
                model_instance.app_name == app_name
            ), f"Expected app_name {app_name}, got {model_instance.app_name}"

        if call_params["proc_id"]:
            assert (
                model_instance.proc_id == proc_id
            ), f"Expected proc_id {proc_id}, got {model_instance.proc_id}"

    # Perform RFC5424-specific validations
    if isinstance(model_instance, SyslogRFC5424Message):
        if call_params["msg_id"]:
            assert (
                model_instance.msg_id == msg_id
            ), f"Expected msg_id {msg_id}, got {model_instance.msg_id}"

        if call_params["structured_data"]:
            assert (
                model_instance.structured_data == structured_data
            ), f"Expected structured_data {structured_data}, got {model_instance.structured_data}"


def validate_source_producer(
    result_or_handler_data: Any,
    *,
    expected_organization: str,
    expected_product: str,
    expected_module: Optional[str] = None,
    handler_key: Optional[str] = None
) -> None:
    """Validate a SourceProducer instance against expected values.

    This function validates that the SourceProducer in a result or handler data has the expected values.
    It can validate a SourceProducer directly or one stored in a model's handler_data dictionary.

    Args:
        result_or_handler_data: Either a model with handler_data containing a SourceProducer, 
                                a dictionary containing a SourceProducer, or a SourceProducer instance.
        expected_organization: Expected organization value.
        expected_product: Expected product value.
        expected_module: Expected module value (if any).
        handler_key: If provided, the key in handler_data where to find handler-specific data.

    Raises:
        AssertionError: If the SourceProducer doesn't match the expected values or can't be found.
    """
    # Get the SourceProducer instance from the input
    sp = None
    
    # Case 1: Direct SourceProducer instance
    if isinstance(result_or_handler_data, SourceProducer):
        sp = result_or_handler_data
    
    # Case 2: Model with handler_data attribute
    elif hasattr(result_or_handler_data, "handler_data") and result_or_handler_data.handler_data is not None:
        # Verify handler_data contains SourceProducer
        assert "SourceProducer" in result_or_handler_data.handler_data, "SourceProducer not found in handler_data"
        sp = result_or_handler_data.handler_data["SourceProducer"]
        
        # If handler_key is provided, verify it exists in handler_data
        if handler_key is not None:
            assert handler_key in result_or_handler_data.handler_data, f"Handler key '{handler_key}' not found in handler_data"
    
    # Case 3: Dictionary potentially containing SourceProducer
    elif isinstance(result_or_handler_data, dict):
        # Verify dictionary contains SourceProducer
        assert "SourceProducer" in result_or_handler_data, "SourceProducer not found in dictionary"
        sp = result_or_handler_data["SourceProducer"]
        
        # If handler_key is provided, verify it exists in the dictionary
        if handler_key is not None:
            assert handler_key in result_or_handler_data, f"Handler key '{handler_key}' not found in dictionary"
    
    # None of the above
    else:
        assert False, f"Input of type {type(result_or_handler_data)} cannot be validated for SourceProducer"
    
    # Validate SourceProducer fields
    assert sp.organization == expected_organization, f"Expected organization '{expected_organization}', got '{sp.organization}'"
    assert sp.product == expected_product, f"Expected product '{expected_product}', got '{sp.product}'"
    
    if expected_module is not None:
        assert sp.module == expected_module, f"Expected module '{expected_module}', got '{sp.module}'"
