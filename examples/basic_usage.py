#!/usr/bin/env python3
"""
Basic usage example for Wolt Restaurant Availability API
"""

import sys
import os
# Add parent directory to path so we can import wolt_api
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from wolt_api import WoltAPI

def main():
    # Initialize the API client
    api = WoltAPI()
    
    # Tel Aviv coordinates
    tel_aviv_lat = 32.0853
    tel_aviv_lon = 34.7818
    
    print("🍕 Wolt Restaurant Availability API - Basic Usage Example")
    print("=" * 60)
    
    # Example 1: Get nearby restaurants
    print("\n1. Getting nearby restaurants in Tel Aviv...")
    restaurants = api.get_nearby_restaurants(
        lat=tel_aviv_lat,
        lon=tel_aviv_lon,
        radius=2000
    )
    
    print(f"Found {len(restaurants)} restaurants nearby")
    print("\nFirst 5 restaurants:")
    for i, restaurant in enumerate(restaurants[:5]):
        status = "🟢 OPEN" if restaurant.is_online else "🔴 CLOSED"
        cuisine = ", ".join(restaurant.cuisine_types[:3]) if restaurant.cuisine_types else "N/A"
        print(f"  {i+1}. {restaurant.name} ({status}) - {cuisine}")
    
    # Example 2: Search for specific cuisine
    print(f"\n2. Searching for pizza restaurants...")
    pizza_restaurants = api.find_restaurants(
        query="pizza",
        lat=tel_aviv_lat,
        lon=tel_aviv_lon
    )
    
    print(f"Found {len(pizza_restaurants)} pizza restaurants")
    for restaurant in pizza_restaurants[:3]:
        status = "🟢 OPEN" if restaurant.is_online else "🔴 CLOSED"
        print(f"  • {restaurant.name} ({status})")
    
    # Example 3: Check specific restaurant status
    if restaurants:
        first_restaurant = restaurants[0]
        print(f"\n3. Checking specific restaurant status...")
        is_open = api.is_restaurant_open(first_restaurant.slug)
        status = "🟢 OPEN" if is_open else "🔴 CLOSED"
        print(f"Restaurant '{first_restaurant.name}' is currently {status}")
    
    # Example 4: Filter by online status
    print(f"\n4. Online restaurants only...")
    online_restaurants = [r for r in restaurants if r.is_online]
    print(f"Found {len(online_restaurants)} restaurants currently accepting orders")
    
    for restaurant in online_restaurants[:3]:
        print(f"  • {restaurant.name}")
        if restaurant.rating:
            print(f"    Rating: {restaurant.rating}/5")
        if restaurant.delivery_estimate:
            print(f"    Delivery: {restaurant.delivery_estimate}")

if __name__ == "__main__":
    main()