#!/usr/bin/env python3
"""
Cuisine analytics script - analyzes restaurant data by cuisine type
"""

import sys
import os
from collections import Counter

# Add parent directory to path so we can import wolt_api
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from wolt_api import WoltAPI

def analyze_cuisine_availability():
    """Analyze availability by cuisine type"""
    api = WoltAPI()
    
    # Tel Aviv coordinates
    lat, lon = 32.0853, 34.7818
    
    print("📊 Cuisine Availability Analytics")
    print("=" * 50)
    print("Analyzing restaurants in Tel Aviv area...\n")
    
    try:
        # Get all nearby restaurants
        restaurants = api.get_nearby_restaurants(lat=lat, lon=lon, radius=5000)
        print(f"Total restaurants found: {len(restaurants)}")
        
        # Separate by availability
        online_restaurants = [r for r in restaurants if r.is_online]
        offline_restaurants = [r for r in restaurants if not r.is_online]
        
        print(f"📱 Online (accepting orders): {len(online_restaurants)}")
        print(f"⏰ Offline (closed/busy): {len(offline_restaurants)}")
        
        # Analyze cuisine types
        print(f"\n🍽️  Cuisine Type Analysis:")
        print("-" * 30)
        
        # Count all cuisine types
        all_cuisines = []
        for restaurant in restaurants:
            all_cuisines.extend(restaurant.cuisine_types)
        
        cuisine_counter = Counter(all_cuisines)
        
        print("Most common cuisine types:")
        for cuisine, count in cuisine_counter.most_common(10):
            percentage = (count / len(restaurants)) * 100
            print(f"  {cuisine:15} {count:3d} restaurants ({percentage:.1f}%)")
        
        # Availability by cuisine
        print(f"\n📈 Availability Rate by Cuisine:")
        print("-" * 35)
        
        cuisine_availability = {}
        
        for cuisine, total_count in cuisine_counter.most_common(15):
            online_count = sum(
                1 for r in online_restaurants 
                if cuisine in r.cuisine_types
            )
            availability_rate = (online_count / total_count) * 100
            cuisine_availability[cuisine] = {
                'total': total_count,
                'online': online_count,
                'rate': availability_rate
            }
        
        # Sort by availability rate
        sorted_cuisines = sorted(
            cuisine_availability.items(),
            key=lambda x: x[1]['rate'],
            reverse=True
        )
        
        for cuisine, data in sorted_cuisines:
            print(f"  {cuisine:15} {data['online']:2d}/{data['total']:2d} online ({data['rate']:5.1f}%)")
        
        # Find best rated cuisines
        print(f"\n⭐ Highest Rated Cuisine Types:")
        print("-" * 32)
        
        cuisine_ratings = {}
        
        for restaurant in restaurants:
            if restaurant.rating is not None:
                for cuisine in restaurant.cuisine_types:
                    if cuisine not in cuisine_ratings:
                        cuisine_ratings[cuisine] = []
                    cuisine_ratings[cuisine].append(restaurant.rating)
        
        # Calculate average ratings (only for cuisines with 3+ restaurants)
        cuisine_avg_ratings = {}
        for cuisine, ratings in cuisine_ratings.items():
            if len(ratings) >= 3:  # At least 3 restaurants
                avg_rating = sum(ratings) / len(ratings)
                cuisine_avg_ratings[cuisine] = {
                    'avg_rating': avg_rating,
                    'count': len(ratings)
                }
        
        # Sort by average rating
        sorted_ratings = sorted(
            cuisine_avg_ratings.items(),
            key=lambda x: x[1]['avg_rating'],
            reverse=True
        )
        
        for cuisine, data in sorted_ratings[:10]:
            print(f"  {cuisine:15} ⭐ {data['avg_rating']:.2f} ({data['count']} restaurants)")
        
        # Delivery analysis
        print(f"\n🚚 Delivery Estimates Analysis:")
        print("-" * 30)
        
        restaurants_with_estimates = [
            r for r in online_restaurants 
            if r.delivery_estimate is not None
        ]
        
        print(f"Restaurants with delivery estimates: {len(restaurants_with_estimates)}")
        
        if restaurants_with_estimates:
            estimates = [r.delivery_estimate for r in restaurants_with_estimates]
            print("Sample delivery estimates:")
            for estimate in set(estimates[:10]):
                count = estimates.count(estimate)
                print(f"  {estimate}: {count} restaurants")
        
    except Exception as e:
        print(f"❌ Error during analysis: {e}")

if __name__ == "__main__":
    analyze_cuisine_availability()