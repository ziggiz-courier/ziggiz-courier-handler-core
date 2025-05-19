# -*- coding: utf-8 -*-
# # SPDX-License-Identifier: BSL-1.1
# # Copyright (c) 2025 Ziggiz Inc.
# #
# # This file is part of the ziggiz-courier-core-data-processing and is licensed under the
# # Business Source License 1.1. You may not use this file except in
# # compliance with the License. You may obtain a copy of the License at:
# # https://github.com/ziggiz-courier/ziggiz-courier-core-data-processing/blob/main/LICENSE
"""Tests for the validation utilities."""

# Third-party imports
import pytest

from tests.test_utils.validation import (
    validate_source_producer,
)

# Local/package imports
from ziggiz_courier_handler_core.models.source_producer import SourceProducer


class MockModel:
    """Mock model class with handler_data for testing."""

    def __init__(self, handler_data=None):
        self.handler_data = handler_data


@pytest.mark.unit
class TestSourceProducerValidation:
    def test_validate_source_producer_direct(self):
        """Test validating a SourceProducer directly."""
        sp = SourceProducer(
            organization="testorg", product="testprod", module="testmodule"
        )
        # Should pass validation with correct values
        validate_source_producer(
            sp,
            expected_organization="testorg",
            expected_product="testprod",
            expected_module="testmodule",
        )
        # Should pass validation without checking module
        validate_source_producer(
            sp, expected_organization="testorg", expected_product="testprod"
        )
        # Should fail validation with incorrect values
        with pytest.raises(AssertionError, match="Expected organization 'wrongorg'"):
            validate_source_producer(
                sp, expected_organization="wrongorg", expected_product="testprod"
            )
        with pytest.raises(AssertionError, match="Expected product 'wrongprod'"):
            validate_source_producer(
                sp, expected_organization="testorg", expected_product="wrongprod"
            )
        with pytest.raises(AssertionError, match="Expected module 'wrongmodule'"):
            validate_source_producer(
                sp,
                expected_organization="testorg",
                expected_product="testprod",
                expected_module="wrongmodule",
            )

    def test_validate_source_producer_in_model(self):
        """Test validating a SourceProducer in a model's handler_data."""
        sp = SourceProducer(organization="testorg", product="testprod")
        handler_data = {"SourceProducer": sp, "TestPlugin": {"some": "data"}}
        model = MockModel(handler_data=handler_data)
        # Should pass validation with correct values
        validate_source_producer(
            model, expected_organization="testorg", expected_product="testprod"
        )
        # Should pass validation with handler_key
        validate_source_producer(
            model,
            expected_organization="testorg",
            expected_product="testprod",
            handler_key="TestPlugin",
        )
        # Should fail validation with incorrect handler_key
        with pytest.raises(
            AssertionError, match="Handler key 'NonExistentPlugin' not found"
        ):
            validate_source_producer(
                model,
                expected_organization="testorg",
                expected_product="testprod",
                handler_key="NonExistentPlugin",
            )

    def test_validate_source_producer_in_dict(self):
        """Test validating a SourceProducer in a dictionary."""
        sp = SourceProducer(organization="testorg", product="testprod")
        handler_data = {"SourceProducer": sp, "TestPlugin": {"some": "data"}}
        # Should pass validation with correct values
        validate_source_producer(
            handler_data, expected_organization="testorg", expected_product="testprod"
        )
        # Should fail validation with missing SourceProducer
        with pytest.raises(
            AssertionError, match="SourceProducer not found in dictionary"
        ):
            validate_source_producer(
                {}, expected_organization="testorg", expected_product="testprod"
            )

    def test_validate_source_producer_invalid_input(self):
        """Test validating a SourceProducer with invalid input types."""
        # Should fail validation with string input
        with pytest.raises(
            AssertionError, match="Input of type <class 'str'> cannot be validated"
        ):
            validate_source_producer(
                "not a valid input",
                expected_organization="testorg",
                expected_product="testprod",
            )
        # Should fail validation with None input
        with pytest.raises(
            AssertionError, match="Input of type <class 'NoneType'> cannot be validated"
        ):
            validate_source_producer(
                None, expected_organization="testorg", expected_product="testprod"
            )
