"""
Unit tests for complex validation logic.
Tests edge cases and complex validation rules.
"""

from utils.validators import (
    validate_alphanumeric_format,
    validate_coordinates,
    validate_cost_amount,
    validate_cost_format,
    validate_id_in_list,
)


class TestValidators:
    """Unit tests for complex validation logic."""

    def test_coordinate_validation_valid_cases(self):
        assert validate_coordinates("33.7490", "-84.3880") is True
        assert validate_coordinates("0.0", "0.0") is True
        assert validate_coordinates("45.123456", "-90.654321") is True
        assert validate_coordinates("-33.7490", "-84.3880") is True

    def test_coordinate_validation_edge_cases(self):
        # Test poles
        assert validate_coordinates("90.0", "0.0") is True
        assert validate_coordinates("-90.0", "0.0") is True

        # Test international date line
        assert validate_coordinates("0.0", "180.0") is True
        assert validate_coordinates("0.0", "-180.0") is True

        # Test equator
        assert validate_coordinates("0.0", "0.0") is True

    def test_coordinate_validation_invalid_cases(self):
        # Invalid latitude ranges
        assert validate_coordinates("91.0", "0.0") is False
        assert validate_coordinates("-91.0", "0.0") is False
        assert validate_coordinates("90.1", "0.0") is False
        assert validate_coordinates("-90.1", "0.0") is False

        # Invalid longitude ranges
        assert validate_coordinates("0.0", "181.0") is False
        assert validate_coordinates("0.0", "-181.0") is False
        assert validate_coordinates("0.0", "180.1") is False
        assert validate_coordinates("0.0", "-180.1") is False

    def test_coordinate_validation_precision_limits(self):
        # Valid precision (6 decimal places)
        assert validate_coordinates("33.749000", "-84.388000") is True

        # Invalid precision (7+ decimal places)
        assert validate_coordinates("33.7490000", "-84.3880000") is False
        assert validate_coordinates("33.74900000", "-84.38800000") is False

    def test_coordinate_validation_format_edge_cases(self):
        # Leading zeros
        assert validate_coordinates("01.0", "01.0") is False
        assert validate_coordinates("1.0", "1.0") is True

        # No decimal places
        assert validate_coordinates("33", "-84") is False
        assert validate_coordinates("33.0", "-84.0") is True

        # Empty strings
        assert validate_coordinates("", "") is False
        assert validate_coordinates("33.7490", "") is False
        assert validate_coordinates("", "-84.3880") is False

    def test_cost_format_validation(self):
        # Valid formats
        assert validate_cost_format("100") is True
        assert validate_cost_format("100.00") is True
        assert validate_cost_format("0") is True
        assert validate_cost_format("0.00") is True
        assert validate_cost_format("1234.56") is True

        # Invalid formats
        assert validate_cost_format("100.0") is False  # Only 1 decimal place
        assert validate_cost_format("100.000") is False  # More than 2 decimal places
        assert validate_cost_format("abc") is False
        assert validate_cost_format("100.") is False
        assert validate_cost_format(".50") is False
        assert validate_cost_format("") is False

    def test_cost_amount_validation(self):
        # Valid amounts
        assert validate_cost_amount("0") is True
        assert validate_cost_amount("0.0") is True
        assert validate_cost_amount("100") is True
        assert validate_cost_amount("100.50") is True

        # Invalid amounts (negative)
        assert validate_cost_amount("-1") is False
        assert validate_cost_amount("-0.01") is False

        # Invalid formats
        assert validate_cost_amount("abc") is False
        assert validate_cost_amount("") is False

    def test_alphanumeric_format_validation(self):
        # Valid formats
        assert validate_alphanumeric_format("Ford") is True
        assert validate_alphanumeric_format("Ford F-150") is True
        assert validate_alphanumeric_format("Ford F-150 Super Duty") is True
        assert validate_alphanumeric_format("Model-123") is True
        assert validate_alphanumeric_format("Model 123") is True
        assert validate_alphanumeric_format("Medical Transport") is True
        assert validate_alphanumeric_format("Emergency Response") is True
        assert validate_alphanumeric_format("Capability-123") is True
        assert validate_alphanumeric_format("Capability 123") is True

        # Invalid formats
        assert validate_alphanumeric_format("Ford@F150") is False
        assert validate_alphanumeric_format("Ford#F150") is False
        assert validate_alphanumeric_format("Ford$F150") is False
        assert validate_alphanumeric_format("Capability@123") is False
        assert validate_alphanumeric_format("Capability#123") is False
        assert validate_alphanumeric_format("") is False

    def test_id_in_list_validation(self):
        valid_esfs = [(1, "Transportation"), (2, "Communications")]
        valid_costs = [(1, "Per Hour"), (2, "Per Day")]

        # Valid cases
        assert validate_id_in_list("1", valid_esfs) is True
        assert validate_id_in_list("2", valid_esfs) is True
        assert validate_id_in_list("1", valid_costs) is True
        assert validate_id_in_list("2", valid_costs) is True

        # Invalid cases
        assert validate_id_in_list("3", valid_esfs) is False
        assert validate_id_in_list("0", valid_esfs) is False
        assert validate_id_in_list("abc", valid_esfs) is False
        assert validate_id_in_list("", valid_esfs) is False
        assert validate_id_in_list("-1", valid_esfs) is False
        assert validate_id_in_list("3", valid_costs) is False
        assert validate_id_in_list("0", valid_costs) is False
        assert validate_id_in_list("abc", valid_costs) is False
        assert validate_id_in_list("", valid_costs) is False
        assert validate_id_in_list("-1", valid_costs) is False
