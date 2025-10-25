"""
Unit tests for complex validation logic.
Tests edge cases and complex validation rules.
"""

from utils.validators import (
    validate_capability_format,
    validate_coordinates,
    validate_cost_amount,
    validate_cost_format,
    validate_cost_id,
    validate_esf_id,
    validate_model_format,
)


class TestValidators:
    """Unit tests for complex validation logic."""

    def test_coordinate_validation_valid_cases(self):
        """Test coordinate validation with valid coordinates."""
        # Test normal coordinates
        assert validate_coordinates("33.7490", "-84.3880") is True
        assert validate_coordinates("0.0", "0.0") is True
        assert validate_coordinates("45.123456", "-90.654321") is True

        # Test negative coordinates
        assert validate_coordinates("-33.7490", "-84.3880") is True
        assert validate_coordinates("33.7490", "-84.3880") is True

    def test_coordinate_validation_edge_cases(self):
        """Test coordinate validation edge cases."""
        # Test poles
        assert validate_coordinates("90.0", "0.0") is True
        assert validate_coordinates("-90.0", "0.0") is True

        # Test international date line
        assert validate_coordinates("0.0", "180.0") is True
        assert validate_coordinates("0.0", "-180.0") is True

        # Test equator
        assert validate_coordinates("0.0", "0.0") is True

    def test_coordinate_validation_invalid_cases(self):
        """Test coordinate validation with invalid coordinates."""
        # Test invalid latitude ranges
        assert validate_coordinates("91.0", "0.0") is False
        assert validate_coordinates("-91.0", "0.0") is False
        assert validate_coordinates("90.1", "0.0") is False
        assert validate_coordinates("-90.1", "0.0") is False

        # Test invalid longitude ranges
        assert validate_coordinates("0.0", "181.0") is False
        assert validate_coordinates("0.0", "-181.0") is False
        assert validate_coordinates("0.0", "180.1") is False
        assert validate_coordinates("0.0", "-180.1") is False

    def test_coordinate_validation_precision_limits(self):
        """Test coordinate validation precision limits."""
        # Test valid precision (6 decimal places)
        assert validate_coordinates("33.749000", "-84.388000") is True

        # Test invalid precision (7+ decimal places)
        assert validate_coordinates("33.7490000", "-84.3880000") is False
        assert validate_coordinates("33.74900000", "-84.38800000") is False

    def test_coordinate_validation_format_edge_cases(self):
        """Test coordinate validation format edge cases."""
        # Test leading zeros
        assert validate_coordinates("01.0", "01.0") is False
        assert validate_coordinates("1.0", "1.0") is True

        # Test no decimal places
        assert validate_coordinates("33", "-84") is False
        assert validate_coordinates("33.0", "-84.0") is True

        # Test empty strings
        assert validate_coordinates("", "") is False
        assert validate_coordinates("33.7490", "") is False
        assert validate_coordinates("", "-84.3880") is False

    def test_cost_format_validation(self):
        """Test cost format validation."""
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
        """Test cost amount validation."""
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

    def test_model_format_validation(self):
        """Test model format validation."""
        # Valid formats
        assert validate_model_format("Ford") is True
        assert validate_model_format("Ford F-150") is True
        assert validate_model_format("Ford F-150 Super Duty") is True
        assert validate_model_format("Model-123") is True
        assert validate_model_format("Model 123") is True

        # Invalid formats
        assert validate_model_format("Ford@F150") is False  # Special characters
        assert validate_model_format("Ford#F150") is False
        assert validate_model_format("Ford$F150") is False
        assert validate_model_format("") is False

    def test_esf_id_validation(self):
        """Test ESF ID validation."""
        # Valid ESF IDs
        valid_esfs = [(1, "Transportation"), (2, "Communications")]

        assert validate_esf_id("1", valid_esfs) is True
        assert validate_esf_id("2", valid_esfs) is True

        # Invalid ESF IDs
        assert validate_esf_id("3", valid_esfs) is False
        assert validate_esf_id("0", valid_esfs) is False
        assert validate_esf_id("abc", valid_esfs) is False
        assert validate_esf_id("", valid_esfs) is False
        assert validate_esf_id("-1", valid_esfs) is False

    def test_cost_id_validation(self):
        """Test cost ID validation."""
        # Valid cost IDs
        valid_costs = [(1, "Per Hour"), (2, "Per Day")]

        assert validate_cost_id("1", valid_costs) is True
        assert validate_cost_id("2", valid_costs) is True

        # Invalid cost IDs
        assert validate_cost_id("3", valid_costs) is False
        assert validate_cost_id("0", valid_costs) is False
        assert validate_cost_id("abc", valid_costs) is False
        assert validate_cost_id("", valid_costs) is False
        assert validate_cost_id("-1", valid_costs) is False

    def test_capability_format_validation(self):
        """Test capability format validation."""
        # Valid formats
        assert validate_capability_format("Medical Transport") is True
        assert validate_capability_format("Emergency Response") is True
        assert validate_capability_format("Capability-123") is True
        assert validate_capability_format("Capability 123") is True

        # Invalid formats
        assert validate_capability_format("Capability@123") is False
        assert validate_capability_format("Capability#123") is False
        assert validate_capability_format("") is False
