#!/usr/bin/env python3
"""
Restaurant monitoring script - tracks availability of specific restaurants
"""

import sys
import os
import time
from datetime import datetime

# Add parent directory to path so we can import wolt_api
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from wolt_api import WoltAPI

# List of restaurant slugs to monitor
RESTAURANTS_TO_MONITOR = [
    "hamosad",  # Replace with actual restaurant slugs you want to monitor
]

# Israeli city coordinates
CITIES = {
    "tel_aviv": (32.0853, 34.7818),
    "jerusalem": (31.7683, 35.2137),
    "haifa": (32.7940, 34.9896),
}

def monitor_restaurants():
    """Monitor restaurants and report status changes"""
    api = WoltAPI(rate_limit_delay=2.0)  # Slower rate to be respectful
    
    print("🔍 Restaurant Availability Monitor")
    print("=" * 50)
    print(f"Monitoring {len(RESTAURANTS_TO_MONITOR)} restaurants...")
    print(f"Check frequency: Every 5 minutes")
    print("Press Ctrl+C to stop\n")
    
    previous_status = {}
    
    try:
        while True:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{current_time}] Checking restaurant status...")
            
            for slug in RESTAURANTS_TO_MONITOR:
                try:
                    is_open = api.is_restaurant_open(slug)
                    
                    # Check if status changed
                    if slug in previous_status:
                        if previous_status[slug] != is_open:
                            status_change = "🟢 OPENED" if is_open else "🔴 CLOSED"
                            print(f"  ⚡ STATUS CHANGE: {slug} is now {status_change}")
                        else:
                            status = "🟢 OPEN" if is_open else "🔴 CLOSED"
                            print(f"  ➖ {slug}: {status} (no change)")
                    else:
                        status = "🟢 OPEN" if is_open else "🔴 CLOSED"
                        print(f"  📍 {slug}: {status} (initial check)")
                    
                    previous_status[slug] = is_open
                    
                except Exception as e:
                    print(f"  ❌ Error checking {slug}: {e}")
            
            print(f"  Next check in 5 minutes...\n")
            time.sleep(300)  # Wait 5 minutes
            
    except KeyboardInterrupt:
        print("\n👋 Monitoring stopped by user")

def find_popular_restaurants():
    """Find popular restaurants in major Israeli cities"""
    api = WoltAPI()
    
    print("🏆 Finding Popular Restaurants")
    print("=" * 50)
    
    for city_name, (lat, lon) in CITIES.items():
        print(f"\n📍 {city_name.replace('_', ' ').title()}:")
        
        try:
            restaurants = api.get_nearby_restaurants(lat=lat, lon=lon, radius=3000)
            
            # Filter to only open restaurants with ratings
            rated_restaurants = [
                r for r in restaurants 
                if r.is_online and r.rating is not None
            ]
            
            # Sort by rating
            rated_restaurants.sort(key=lambda x: x.rating, reverse=True)
            
            print(f"  Found {len(rated_restaurants)} open restaurants with ratings")
            
            for i, restaurant in enumerate(rated_restaurants[:5]):
                print(f"    {i+1}. {restaurant.name} (⭐ {restaurant.rating})")
                print(f"       Cuisine: {', '.join(restaurant.cuisine_types[:3])}")
                
        except Exception as e:
            print(f"  ❌ Error getting restaurants: {e}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "popular":
        find_popular_restaurants()
    else:
        monitor_restaurants()