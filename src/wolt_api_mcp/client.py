"""
Main Wolt API client
"""
import time
import requests
from typing import List, Optional
from .models import Restaurant
from .exceptions import WoltAPIError, RestaurantNotFoundError, RateLimitError, APIUnavailableError


class WoltAPI:
    """Client for accessing Wolt restaurant availability API"""
    
    BASE_URL = "https://consumer-api.wolt.com"
    
    def __init__(self, rate_limit_delay: float = 1.0):
        """
        Initialize Wolt API client
        
        Args:
            rate_limit_delay: Delay between requests in seconds (default: 1.0)
                             Note: For comprehensive Israel-wide searches, consider using 0.5-2.0 seconds
        """
        self.rate_limit_delay = rate_limit_delay
        self.last_request_time = 0.0
        self.session = requests.Session()
        
        # Set required headers based on the cheat sheet
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Origin": "https://wolt.com",
            "x-platform": "web",
            "Accept-Language": "en"
        })
    
    def _rate_limit(self):
        """Apply rate limiting between requests"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < self.rate_limit_delay:
            sleep_time = self.rate_limit_delay - time_since_last
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()
    
    def _make_request(self, url: str, params: dict = None, retry_on_rate_limit: bool = True) -> dict:
        """
        Make HTTP request with rate limiting and error handling
        
        Args:
            url: Full URL to request
            params: Query parameters
            retry_on_rate_limit: Whether to retry once on rate limit (default: True)
            
        Returns:
            JSON response as dict
            
        Raises:
            WoltAPIError: For various API errors
        """
        self._rate_limit()
        
        try:
            response = self.session.get(url, params=params, timeout=10)
            
            if response.status_code == 404:
                raise RestaurantNotFoundError("Restaurant not found (404)")
            elif response.status_code == 429:
                if retry_on_rate_limit:
                    # Wait longer and retry once
                    import time
                    time.sleep(5.0)
                    return self._make_request(url, params, retry_on_rate_limit=False)
                else:
                    raise RateLimitError("Rate limit exceeded (429)")
            elif response.status_code == 430:
                raise APIUnavailableError("API unavailable - check headers or endpoint (430)")
            elif response.status_code >= 500:
                raise APIUnavailableError(f"Server error ({response.status_code})")
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            raise WoltAPIError(f"Request failed: {e}")
    
    def is_restaurant_open(self, slug: str) -> bool:
        """
        Check if a restaurant is open for orders
        
        Args:
            slug: Restaurant slug (from URL or venue search)
            
        Returns:
            True if restaurant is open for orders, False otherwise
            
        Raises:
            RestaurantNotFoundError: If slug is invalid
            WoltAPIError: For other API errors
        """
        # Since the dynamic endpoint doesn't work for Israeli venues,
        # we'll search for the restaurant by slug in the nearby restaurants
        # This is less efficient but provides comprehensive coverage across all of Israel
        
        # Comprehensive search across ALL of Israel
        # Using major population centers with large search radii for complete coverage
        israeli_locations = [
            # Tel Aviv Metropolitan Area (Gush Dan) - Optimized for complete coverage
            ("Tel Aviv Center", 32.0853, 34.7818, 8000),       # Central Tel Aviv core
            ("Tel Aviv Dizengoff", 32.0740, 34.7749, 8000),    # Dizengoff Center area (vitrina-ibn-gvirol location)
            ("North Tel Aviv", 32.1200, 34.8000, 12000),       # Ramat Aviv, Herzliya, Ra'anana area
            ("South Tel Aviv", 32.0300, 34.7500, 10000),       # Jaffa, Bat Yam area
            ("East Tel Aviv", 32.0800, 34.8500, 12000),        # Ramat Gan, Givatayim, Bnei Brak, Petah Tikva
            
            # Jerusalem Area  
            ("Jerusalem Center", 31.7683, 35.2137, 15000),     # Jerusalem + surrounding settlements
            ("Jerusalem North", 31.8500, 35.2000, 12000),      # Northern Jerusalem area
            
            # Haifa & North
            ("Haifa", 32.7940, 34.9896, 12000),               # Haifa + Carmel area
            ("Haifa Bay", 32.8200, 35.0700, 10000),           # Acre, Nahariya area
            ("Nazareth", 32.7022, 35.2973, 8000),             # Nazareth area
            
            # Central Israel
            ("Netanya", 32.3215, 34.8532, 10000),             # Netanya + coastal plain
            ("Kfar Saba", 32.1743, 34.9077, 8000),            # Kfar Saba, Ra'anana area
            ("Rehovot", 31.8969, 34.8186, 10000),             # Rehovot, Ness Ziona area
            
            # South
            ("Be'er Sheva", 31.2587, 34.8008, 15000),         # Be'er Sheva + Negev region
            ("Ashkelon", 31.6688, 34.5742, 8000),             # Ashkelon + coastal south
            ("Ashdod", 31.7940, 34.6440, 8000),               # Ashdod area
            
            # Additional Coverage Areas
            ("Modi'in", 31.8970, 35.0098, 8000),              # Modi'in area
            ("Eilat", 29.5581, 34.9482, 5000),                # Eilat (southern tip)
            ("Tiberias", 32.7922, 35.5311, 6000),             # Tiberias + Sea of Galilee
            ("Kiryat Shmona", 33.2074, 35.5692, 5000),        # Northern border area
        ]
        
        try:
            # Search across all major Israeli population centers
            for location_name, lat, lon, radius in israeli_locations:
                restaurants = self.get_nearby_restaurants(
                    lat=lat, 
                    lon=lon, 
                    radius=radius
                )
                
                for restaurant in restaurants:
                    if restaurant.slug == slug:
                        return restaurant.is_online
            
            # If still not found after comprehensive search, raise error
            raise WoltAPIError(f"Unknown slug: {slug}")
            
        except WoltAPIError:
            raise
        except Exception as e:
            raise WoltAPIError(f"Error checking restaurant status: {e}")
    
    def get_nearby_restaurants(self, lat: float, lon: float, radius: int = 2000) -> List[Restaurant]:
        """
        Get all restaurants near a location
        
        Args:
            lat: Latitude
            lon: Longitude  
            radius: Search radius in meters (default: 2000)
            
        Returns:
            List of Restaurant objects
            
        Raises:
            WoltAPIError: For API errors
        """
        # Using the working endpoint found during testing
        url = f"{self.BASE_URL}/v1/pages/restaurants"
        params = {
            "lat": lat,
            "lon": lon,
            "radius": radius
        }
        
        data = self._make_request(url, params=params)
        
        restaurants = []
        
        # Parse the response structure - sections contain venue lists
        sections = data.get("sections", [])
        for section in sections:
            items = section.get("items", [])
            for item in items:
                venue = item.get("venue", {})
                if venue:
                    restaurant = self._parse_restaurant(venue)
                    restaurants.append(restaurant)
        
        return restaurants
    
    def find_restaurants(self, query: str, lat: float, lon: float) -> List[Restaurant]:
        """
        Search for restaurants by name/keyword
        
        Args:
            query: Search term (restaurant name, cuisine type, etc.)
            lat: Latitude for location-based results
            lon: Longitude for location-based results
            
        Returns:
            List of Restaurant objects matching the query
            
        Raises:
            WoltAPIError: For API errors
        """
        # Since the search endpoint also returns 404, we'll implement search
        # by filtering nearby restaurants by name/keyword
        restaurants = self.get_nearby_restaurants(lat=lat, lon=lon, radius=5000)
        
        # Filter restaurants by query
        query_lower = query.lower()
        matching_restaurants = []
        
        for restaurant in restaurants:
            # Check if query matches name
            if query_lower in restaurant.name.lower():
                matching_restaurants.append(restaurant)
                continue
            
            # Check if query matches any cuisine type
            for cuisine in restaurant.cuisine_types:
                if query_lower in cuisine.lower():
                    matching_restaurants.append(restaurant)
                    break
        
        return matching_restaurants
    
    def _parse_restaurant(self, venue_data: dict) -> Restaurant:
        """
        Parse venue data into Restaurant object
        
        Args:
            venue_data: Raw venue data from API
            
        Returns:
            Restaurant object
        """
        # Extract cuisine types from tags (tags are just strings)
        tags = venue_data.get("tags", [])
        cuisine_types = [tag for tag in tags if isinstance(tag, str)]
        
        # Get delivery estimate
        delivery_estimate = None
        estimate = venue_data.get("estimate")
        if estimate and isinstance(estimate, dict):
            delivery_estimate = estimate.get("estimate")
        
        # Get image URL - try multiple possible locations
        image_url = None
        
        # Try main image field
        image = venue_data.get("image")
        if image and isinstance(image, dict):
            image_url = image.get("url")
        
        # Try venue_preview_items for image
        if not image_url:
            preview_items = venue_data.get("venue_preview_items", [])
            if preview_items and len(preview_items) > 0:
                first_item = preview_items[0]
                if isinstance(first_item, dict) and "image" in first_item:
                    item_image = first_item["image"]
                    if isinstance(item_image, dict):
                        image_url = item_image.get("url")
        
        # Get rating
        rating = None
        rating_data = venue_data.get("rating")
        if rating_data and isinstance(rating_data, dict):
            rating = rating_data.get("score")
        
        return Restaurant(
            name=venue_data.get("name", ""),
            slug=venue_data.get("slug", ""),
            is_online=venue_data.get("online", False),
            cuisine_types=cuisine_types,
            rating=rating,
            delivery_estimate=delivery_estimate,
            image_url=image_url
        )