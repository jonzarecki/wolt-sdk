"""MCP server exposing Wolt restaurant availability functions."""

import logging
from typing import Annotated, List, Literal, Optional

from fastmcp import FastMCP
from fastmcp.contrib.bulk_tool_caller import BulkToolCaller
from pydantic import Field

from .client import WoltAPI
from .models import Restaurant
from .exceptions import WoltAPIError, RestaurantNotFoundError

logger = logging.getLogger(__name__)

mcp = FastMCP("wolt-api-mcp", dependencies=["requests", "pydantic"])

# Register bulk tool calling utilities
_bulk_tools = BulkToolCaller()
_bulk_tools.register_tools(mcp)


@mcp.tool(
    name="search_restaurants",
    description="Search for restaurants by name across all of Israel with comprehensive filtering options",
    tags={"restaurants", "food", "search", "israel"},
    annotations={
        "title": "Restaurant Search",
        "readOnlyHint": True,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
def search_restaurants(
    query: Annotated[
        str,
        Field(
            description="Restaurant name or search term (e.g., 'Pizza Hut', 'sushi', 'burger')",
            min_length=2,
            max_length=100,
        ),
    ],
    city: Annotated[
        Optional[str],
        Field(
            description="City name to filter results (e.g., 'tel-aviv', 'jerusalem', 'haifa'). Leave empty for all cities",
            max_length=50,
        ),
    ] = None,
    max_results: Annotated[
        int,
        Field(
            description="Maximum number of restaurants to return",
            ge=1,
            le=50,
        ),
    ] = 20,
    rate_limit_delay: Annotated[
        float,
        Field(
            description="Delay between requests in seconds to avoid rate limiting (0.5-3.0 recommended)",
            ge=0.1,
            le=5.0,
        ),
    ] = 1.0,
) -> str:
    """
    Search for restaurants by name across Israel using the Wolt platform.

    This tool searches for restaurants using the Wolt API and returns a formatted list
    of available restaurants with details including:
    - Restaurant name and basic info
    - Location (city/area)
    - Availability status (open/closed)
    - Delivery information
    - Cuisine type

    The results are automatically filtered and sorted by relevance.

    Args:
        query: Restaurant name or search term to find
        city: Optional city filter to narrow results
        max_results: Maximum number of restaurants to return (1-50)
        rate_limit_delay: Delay between API requests to avoid rate limiting

    Returns:
        Formatted string with restaurant search results, including availability
        status and up to max_results matching restaurants with details.

    Raises:
        ValueError: If parameters are invalid
        RuntimeError: If Wolt API service is unavailable

    Example:
        search_restaurants(
            query="Pizza Hut",
            city="tel-aviv",
            max_results=10,
            rate_limit_delay=1.0
        )
    """
    try:
        api = WoltAPI(rate_limit_delay=rate_limit_delay)
        restaurants = api.find_restaurants_by_name(query, city_filter=city, max_results=max_results)

        if not restaurants:
            return f"No restaurants found matching '{query}'{f' in {city}' if city else ''}. Try adjusting your search terms."

        # Format results
        lines = [f"Found {len(restaurants)} restaurant(s) matching '{query}'{f' in {city}' if city else ''}:", ""]

        for i, restaurant in enumerate(restaurants, 1):
            status = "🟢 Open" if restaurant.is_open else "🔴 Closed"
            line = f"{i}. {restaurant.name} - {status}"
            if restaurant.location:
                line += f" - {restaurant.location}"
            lines.append(line)

        return "\n".join(lines)

    except ValueError as e:
        logger.error(f"Invalid search parameters: {e}")
        return f"Search error: {e}"
    except WoltAPIError as e:
        logger.error(f"Wolt API error: {e}")
        return f"Wolt API temporarily unavailable: {e}"
    except Exception as e:
        logger.error(f"Unexpected error during restaurant search: {e}")
        return "An unexpected error occurred during restaurant search. Please try again."


@mcp.tool(
    name="check_restaurant_availability",
    description="Check if a specific restaurant is currently open for orders",
    tags={"restaurants", "availability", "status"},
    annotations={
        "title": "Restaurant Availability Check",
        "readOnlyHint": True,
        "idempotentHint": False,  # Status can change
        "openWorldHint": False,
    },
)
def check_restaurant_availability(
    slug: Annotated[
        str,
        Field(
            description="Restaurant slug from Wolt URL (e.g., 'pizza-hut-tel-aviv-central')",
            min_length=3,
            max_length=200,
            pattern=r"^[a-z0-9\-]+$",
        ),
    ],
    rate_limit_delay: Annotated[
        float,
        Field(
            description="Delay between requests in seconds to avoid rate limiting",
            ge=0.1,
            le=5.0,
        ),
    ] = 1.0,
) -> str:
    """
    Check if a specific restaurant is currently open for orders.

    This tool checks the real-time availability status of a restaurant using its
    unique slug identifier from the Wolt platform.

    Args:
        slug: Restaurant slug from Wolt URL (e.g., 'pizza-hut-tel-aviv-central')
        rate_limit_delay: Delay between API requests to avoid rate limiting

    Returns:
        String indicating whether the restaurant is open or closed for orders,
        with additional details if available.

    Raises:
        RestaurantNotFoundError: If the slug is invalid or restaurant doesn't exist
        WoltAPIError: For other API errors

    Example:
        check_restaurant_availability(
            slug="pizza-hut-tel-aviv-central",
            rate_limit_delay=1.0
        )
    """
    try:
        api = WoltAPI(rate_limit_delay=rate_limit_delay)
        is_open = api.is_restaurant_open(slug)

        status = "🟢 OPEN" if is_open else "🔴 CLOSED"
        return f"Restaurant '{slug}' is currently {status} for orders."

    except RestaurantNotFoundError as e:
        logger.error(f"Restaurant not found: {e}")
        return f"Restaurant with slug '{slug}' not found. Please verify the slug is correct."
    except WoltAPIError as e:
        logger.error(f"Wolt API error: {e}")
        return f"Could not check restaurant availability: {e}"
    except Exception as e:
        logger.error(f"Unexpected error checking restaurant availability: {e}")
        return "An unexpected error occurred while checking restaurant availability. Please try again."


@mcp.tool(
    name="get_nearby_restaurants",
    description="Get restaurants near a specific location in Israel",
    tags={"restaurants", "location", "nearby", "delivery"},
    annotations={
        "title": "Nearby Restaurants",
        "readOnlyHint": True,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
def get_nearby_restaurants(
    city: Annotated[
        str,
        Field(
            description="City name in Israel (e.g., 'tel-aviv', 'jerusalem', 'haifa', 'beer-sheva')",
            min_length=2,
            max_length=50,
        ),
    ],
    cuisine_filter: Annotated[
        Optional[str],
        Field(
            description="Filter by cuisine type (e.g., 'pizza', 'sushi', 'burger', 'italian')",
            max_length=50,
        ),
    ] = None,
    max_results: Annotated[
        int,
        Field(
            description="Maximum number of restaurants to return",
            ge=1,
            le=100,
        ),
    ] = 20,
    only_open: Annotated[
        bool,
        Field(
            description="Only return restaurants that are currently open for orders",
        ),
    ] = False,
    rate_limit_delay: Annotated[
        float,
        Field(
            description="Delay between requests in seconds to avoid rate limiting",
            ge=0.1,
            le=5.0,
        ),
    ] = 1.0,
) -> str:
    """
    Get restaurants near a specific location in Israel.

    This tool finds restaurants in or around a specific city, with optional
    filtering by cuisine type and availability status.

    Args:
        city: City name in Israel to search in
        cuisine_filter: Optional cuisine type filter
        max_results: Maximum number of restaurants to return (1-100)
        only_open: Only return restaurants currently open for orders
        rate_limit_delay: Delay between API requests to avoid rate limiting

    Returns:
        Formatted string with nearby restaurant results, including availability
        status and restaurant details.

    Example:
        get_nearby_restaurants(
            city="tel-aviv",
            cuisine_filter="pizza",
            max_results=15,
            only_open=True,
            rate_limit_delay=1.0
        )
    """
    try:
        api = WoltAPI(rate_limit_delay=rate_limit_delay)
        restaurants = api.get_nearby_restaurants(city, max_results=max_results)

        if not restaurants:
            return f"No restaurants found in {city}. Please check the city name or try a different location."

        # Apply filters
        filtered_restaurants = restaurants
        if cuisine_filter:
            filtered_restaurants = [r for r in filtered_restaurants if cuisine_filter.lower() in r.name.lower()]

        if only_open:
            # Check availability for each restaurant (this will be slower)
            open_restaurants = []
            for restaurant in filtered_restaurants:
                try:
                    if api.is_restaurant_open(restaurant.slug):
                        restaurant.is_open = True
                        open_restaurants.append(restaurant)
                except:
                    # Skip restaurants we can't check
                    continue
            filtered_restaurants = open_restaurants

        if not filtered_restaurants:
            filters_text = []
            if cuisine_filter:
                filters_text.append(f"cuisine '{cuisine_filter}'")
            if only_open:
                filters_text.append("currently open")
            filter_str = " and ".join(filters_text)
            return f"No restaurants found in {city} matching {filter_str}. Try adjusting your filters."

        # Format results
        lines = [
            f"Found {len(filtered_restaurants)} restaurant(s) in {city}"
            + (f" serving {cuisine_filter}" if cuisine_filter else "")
            + (" (open only)" if only_open else "")
            + ":",
            "",
        ]

        for i, restaurant in enumerate(filtered_restaurants, 1):
            status = "🟢 Open" if getattr(restaurant, "is_open", None) else "⚪ Status unknown"
            if only_open:  # If we filtered for open restaurants, they're definitely open
                status = "🟢 Open"

            line = f"{i}. {restaurant.name} - {status}"
            if restaurant.location and restaurant.location != city:
                line += f" - {restaurant.location}"
            lines.append(line)

        if len(filtered_restaurants) >= max_results:
            lines.append(f"\n... showing first {max_results} results")

        return "\n".join(lines)

    except ValueError as e:
        logger.error(f"Invalid parameters: {e}")
        return f"Parameter error: {e}"
    except WoltAPIError as e:
        logger.error(f"Wolt API error: {e}")
        return f"Wolt API temporarily unavailable: {e}"
    except Exception as e:
        logger.error(f"Unexpected error getting nearby restaurants: {e}")
        return "An unexpected error occurred while getting nearby restaurants. Please try again."


@mcp.resource("wolt://cities")
def get_supported_cities() -> str:
    """Get list of supported cities in Israel for restaurant searches."""
    cities = [
        "tel-aviv", "jerusalem", "haifa", "beer-sheva", "petah-tikva",
        "rishon-lezion", "ashdod", "netanya", "ramat-gan", "holon",
        "herzliya", "kfar-saba", "modiin", "rehovot", "beit-shemesh"
    ]
    
    return f"""# Supported Cities in Israel

The following cities are supported for restaurant searches on Wolt:

{chr(10).join(f'- {city.replace("-", " ").title()}' for city in cities)}

## Usage Notes

- Use lowercase, hyphenated format for API calls (e.g., "tel-aviv")
- Some suburbs and neighborhoods may also work
- If a city isn't listed, try the nearest major city
"""


@mcp.resource("wolt://cuisine-types")
def get_cuisine_types() -> str:
    """Get common cuisine types available on Wolt in Israel."""
    cuisines = [
        "pizza", "burger", "sushi", "italian", "asian", "mediterranean",
        "mexican", "indian", "thai", "chinese", "american", "fast-food",
        "healthy", "vegan", "vegetarian", "kosher", "breakfast", "dessert",
        "coffee", "bakery", "seafood", "grill", "salad", "sandwich"
    ]
    
    return f"""# Common Cuisine Types on Wolt Israel

The following cuisine types are commonly available:

{chr(10).join(f'- {cuisine.title()}' for cuisine in cuisines)}

## Search Tips

- Use cuisine filters to narrow down restaurant searches
- Combine with city filters for best results
- Some restaurants may serve multiple cuisine types
"""


@mcp.prompt("restaurant-search-prompt")
def restaurant_search_prompt(
    city: str = "tel-aviv",
    cuisine: str = "any",
    occasion: str = "casual dining"
) -> str:
    """Generate a comprehensive restaurant search prompt."""
    return f"""I'm looking for restaurant recommendations in {city.replace('-', ' ').title()}, Israel.

Search Parameters:
- City: {city}
- Cuisine preference: {cuisine}
- Occasion: {occasion}

Please search for restaurants that match these criteria and provide:
1. Restaurant names and availability status
2. Cuisine types and specialties  
3. Estimated delivery times if available
4. Any notable features or ratings

Use the Wolt MCP tools to find the best options and format the results in a user-friendly way."""


def main() -> None:
    """Run the MCP server."""
    logging.basicConfig(level=logging.INFO)
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()