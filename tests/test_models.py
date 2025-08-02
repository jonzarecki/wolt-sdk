"""
Basic tests for wolt-api models
"""

import pytest
from wolt_api.models import Restaurant


class TestRestaurant:
    """Test Restaurant model functionality."""

    def test_restaurant_creation_valid(self):
        """Test creating a valid restaurant."""
        restaurant = Restaurant(
            name="Test Restaurant",
            slug="test-restaurant",
            is_online=True,
            cuisine_types=["Italian", "Pizza"],
            rating=4.5,
            delivery_estimate="30-45 min",
            image_url="https://example.com/image.jpg"
        )
        
        assert restaurant.name == "Test Restaurant"
        assert restaurant.slug == "test-restaurant"
        assert restaurant.is_online is True
        assert restaurant.cuisine_types == ["Italian", "Pizza"]
        assert restaurant.rating == 4.5
        assert restaurant.delivery_estimate == "30-45 min"
        assert restaurant.image_url == "https://example.com/image.jpg"

    def test_restaurant_creation_minimal(self):
        """Test creating restaurant with minimal required fields."""
        restaurant = Restaurant(
            name="Test",
            slug="test",
            is_online=False,
            cuisine_types=["Fast Food"]
        )
        
        assert restaurant.name == "Test"
        assert restaurant.slug == "test"
        assert restaurant.is_online is False
        assert restaurant.cuisine_types == ["Fast Food"]
        assert restaurant.rating is None
        assert restaurant.delivery_estimate is None
        assert restaurant.image_url is None

    def test_restaurant_str_representation(self):
        """Test string representation of restaurant."""
        # Test online restaurant
        restaurant_online = Restaurant(
            name="Online Restaurant",
            slug="online",
            is_online=True,
            cuisine_types=["Test"]
        )
        assert str(restaurant_online) == "Online Restaurant (🟢 OPEN)"
        
        # Test offline restaurant
        restaurant_offline = Restaurant(
            name="Offline Restaurant", 
            slug="offline",
            is_online=False,
            cuisine_types=["Test"]
        )
        assert str(restaurant_offline) == "Offline Restaurant (🔴 CLOSED)"

    def test_restaurant_dataclass_features(self):
        """Test dataclass features like equality."""
        restaurant1 = Restaurant(
            name="Same Restaurant",
            slug="same",
            is_online=True,
            cuisine_types=["Italian"]
        )
        
        restaurant2 = Restaurant(
            name="Same Restaurant",
            slug="same", 
            is_online=True,
            cuisine_types=["Italian"]
        )
        
        # Test equality
        assert restaurant1 == restaurant2
        
        # Test that different restaurants are not equal
        restaurant3 = Restaurant(
            name="Different Restaurant",
            slug="different",
            is_online=True,
            cuisine_types=["Italian"]
        )
        
        assert restaurant1 != restaurant3