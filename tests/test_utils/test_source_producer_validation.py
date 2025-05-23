# -*- coding: utf-8 -*-
# SPDX-License-Identifier: BSL-1.1
# Copyright (c) 2025 Ziggiz Inc.
#
# This file is part of the ziggiz-courier-core-data-processing and is licensed under the
# Business Source License 1.1. You may not use this file except in
# compliance with the License. You may obtain a copy of the License at:
# https://github.com/ziggiz-courier/ziggiz-courier-core-data-processing/blob/main/LICENSE
#
"""Tests for the validation utilities."""

# Third-party imports
import pytest

from tests.test_utils.validation import (
    validate_meta_data_product,
)

# Local/package imports
from ziggiz_courier_handler_core.models.meta_data_product import MetaDataProduct


class MockModel:
    """Mock model class with handler_data for testing."""

    def __init__(self, handler_data=None):
        self.handler_data = handler_data


@pytest.mark.unit
class TestMetaDataProductValidation:
    def test_validate_meta_data_product_direct(self):
        """Test validating a MetaDataProduct directly."""
        mdp = MetaDataProduct(
            organization="testorg", product="testprod", module="testmodule"
        )
        # Should pass validation with correct values
        validate_meta_data_product(
            mdp,
            expected_organization="testorg",
            expected_product="testprod",
            expected_module="testmodule",
        )
        # Should pass validation without checking module
        validate_meta_data_product(
            mdp, expected_organization="testorg", expected_product="testprod"
        )
        # Should fail validation with incorrect values
        with pytest.raises(AssertionError, match="Expected organization 'wrongorg'"):
            validate_meta_data_product(
                mdp, expected_organization="wrongorg", expected_product="testprod"
            )
        with pytest.raises(AssertionError, match="Expected product 'wrongprod'"):
            validate_meta_data_product(
                mdp, expected_organization="testorg", expected_product="wrongprod"
            )
        with pytest.raises(AssertionError, match="Expected module 'wrongmodule'"):
            validate_meta_data_product(
                mdp,
                expected_organization="testorg",
                expected_product="testprod",
                expected_module="wrongmodule",
            )

    def test_validate_meta_data_product_in_model(self):
        """Test validating a MetaDataProduct in a model's handler_data."""
        mdp = MetaDataProduct(organization="testorg", product="testprod")
        handler_data = {"MetaDataProduct": mdp, "TestPlugin": {"some": "data"}}
        model = MockModel(handler_data=handler_data)
        # Should pass validation with correct values
        validate_meta_data_product(
            model, expected_organization="testorg", expected_product="testprod"
        )
        # Should pass validation with handler_key
        validate_meta_data_product(
            model,
            expected_organization="testorg",
            expected_product="testprod",
            handler_key="TestPlugin",
        )
        # Should fail validation with incorrect handler_key
        with pytest.raises(
            AssertionError, match="Handler key 'NonExistentPlugin' not found"
        ):
            validate_meta_data_product(
                model,
                expected_organization="testorg",
                expected_product="testprod",
                handler_key="NonExistentPlugin",
            )

    def test_validate_meta_data_product_in_dict(self):
        """Test validating a MetaDataProduct in a dictionary."""
        mdp = MetaDataProduct(organization="testorg", product="testprod")
        handler_data = {"MetaDataProduct": mdp, "TestPlugin": {"some": "data"}}
        # Should pass validation with correct values
        validate_meta_data_product(
            handler_data, expected_organization="testorg", expected_product="testprod"
        )
        # Should fail validation with missing MetaDataProduct
        with pytest.raises(
            AssertionError, match="MetaDataProduct not found in dictionary"
        ):
            validate_meta_data_product(
                {}, expected_organization="testorg", expected_product="testprod"
            )

    def test_validate_meta_data_product_invalid_input(self):
        """Test validating a MetaDataProduct with invalid input types."""
        # Should fail validation with string input
        with pytest.raises(
            AssertionError, match="Input of type <class 'str'> cannot be validated"
        ):
            validate_meta_data_product(
                "not a valid input",
                expected_organization="testorg",
                expected_product="testprod",
            )
        # Should fail validation with None input
        with pytest.raises(
            AssertionError, match="Input of type <class 'NoneType'> cannot be validated"
        ):
            validate_meta_data_product(
                None, expected_organization="testorg", expected_product="testprod"
            )
