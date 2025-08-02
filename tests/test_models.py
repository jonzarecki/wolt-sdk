"""
Basic tests for wolt-api-mcp models
"""

import pytest
from pydantic import ValidationError

from wolt_api_mcp.models import Restaurant, SearchParams


class TestRestaurant:
    """Test Restaurant model validation."""

    def test_restaurant_creation_valid(self):
        """Test creating a valid restaurant."""
        restaurant = Restaurant(
            name="Test Restaurant",
            slug="test-restaurant",
            is_online=True,
            cuisine_types=["Italian", "Pizza"],
            rating=4.5,
            delivery_estimate="30-45 min",
            location="Test Location",
            city="test-city"
        )
        
        assert restaurant.name == "Test Restaurant"
        assert restaurant.slug == "test-restaurant"
        assert restaurant.is_online is True
        assert restaurant.is_open is True  # Test alias
        assert restaurant.cuisine_types == ["Italian", "Pizza"]
        assert restaurant.rating == 4.5

    def test_restaurant_slug_validation(self):
        """Test slug validation and normalization."""
        restaurant = Restaurant(
            name="Test",
            slug="Test-Restaurant_123",
            is_online=True
        )
        
        # Should be converted to lowercase
        assert restaurant.slug == "test-restaurant_123"

    def test_restaurant_name_validation(self):
        """Test name validation."""
        with pytest.raises(ValidationError):
            Restaurant(
                name="",  # Empty name should fail
                slug="test",
                is_online=True
            )

    def test_restaurant_invalid_slug_pattern(self):
        """Test invalid slug pattern."""
        with pytest.raises(ValidationError):
            Restaurant(
                name="Test",
                slug="invalid slug with spaces",  # Should fail pattern validation
                is_online=True
            )

    def test_restaurant_rating_bounds(self):
        """Test rating bounds validation."""
        # Valid rating
        restaurant = Restaurant(
            name="Test",
            slug="test",
            is_online=True,
            rating=4.5
        )
        assert restaurant.rating == 4.5

        # Invalid rating (too high)
        with pytest.raises(ValidationError):
            Restaurant(
                name="Test",
                slug="test",
                is_online=True,
                rating=6.0  # Should fail (max 5.0)
            )


class TestSearchParams:
    """Test SearchParams model validation."""

    def test_search_params_valid(self):
        """Test creating valid search parameters."""
        params = SearchParams(
            query="pizza",
            city="tel-aviv",
            max_results=10,
            rate_limit_delay=1.5
        )
        
        assert params.query == "pizza"
        assert params.city == "tel-aviv"
        assert params.max_results == 10
        assert params.rate_limit_delay == 1.5

    def test_search_params_defaults(self):
        """Test default values."""
        params = SearchParams(query="pizza")
        
        assert params.query == "pizza"
        assert params.city is None
        assert params.max_results == 20  # Default
        assert params.rate_limit_delay == 1.0  # Default

    def test_search_params_query_validation(self):
        """Test query validation."""
        with pytest.raises(ValidationError):
            SearchParams(query="")  # Empty query should fail

        with pytest.raises(ValidationError):
            SearchParams(query="  ")  # Whitespace-only query should fail

    def test_search_params_max_results_bounds(self):
        """Test max_results bounds."""
        # Valid bounds
        params = SearchParams(query="test", max_results=50)
        assert params.max_results == 50

        # Invalid bounds
        with pytest.raises(ValidationError):
            SearchParams(query="test", max_results=0)  # Below minimum

        with pytest.raises(ValidationError):
            SearchParams(query="test", max_results=200)  # Above maximum

    def test_search_params_rate_limit_bounds(self):
        """Test rate_limit_delay bounds."""
        # Valid bounds
        params = SearchParams(query="test", rate_limit_delay=2.0)
        assert params.rate_limit_delay == 2.0

        # Invalid bounds
        with pytest.raises(ValidationError):
            SearchParams(query="test", rate_limit_delay=0.05)  # Below minimum

        with pytest.raises(ValidationError):
            SearchParams(query="test", rate_limit_delay=10.0)  # Above maximum