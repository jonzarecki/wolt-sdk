# Usage Examples for Wolt Restaurant Availability MCP Tools

This document provides usage examples for the tools provided by the Wolt Restaurant Availability MCP server. It demonstrates how to search for restaurants, check availability, and make bulk tool calls using the `search_restaurants`, `check_restaurant_availability`, `get_nearby_restaurants`, and bulk calling functions.

## Basic Usage Examples

### Search Restaurants by Name

```python
from wolt_api_mcp import search_restaurants
print(search_restaurants.fn("Pizza Hut", city="tel-aviv", max_results=10))
```

### Check Restaurant Availability

```python  
from wolt_api_mcp import check_restaurant_availability
print(check_restaurant_availability.fn("pizza-hut-tel-aviv-central"))
```

### Get Nearby Restaurants

```python
from wolt_api_mcp import get_nearby_restaurants  
print(get_nearby_restaurants.fn("tel-aviv", cuisine_filter="pizza", only_open=True))
```

## Bulk Tool Calling Examples

### Multiple Restaurant Searches

```python
from wolt_api_mcp import call_tools_bulk
from fastmcp.contrib.bulk_tool_caller import CallToolRequest
import asyncio

reqs = [
    CallToolRequest(
        tool="search_restaurants",
        arguments={"query": "Pizza Hut", "city": "tel-aviv", "max_results": 5},
    ),
    CallToolRequest(
        tool="search_restaurants", 
        arguments={"query": "McDonald's", "city": "jerusalem", "max_results": 5},
    ),
    CallToolRequest(
        tool="get_nearby_restaurants",
        arguments={"city": "haifa", "cuisine_filter": "sushi", "max_results": 10},
    ),
]

results = asyncio.run(call_tools_bulk(reqs))
for result in results:
    print(f"Tool: {result.tool}")
    print(f"Result: {result.result}")
    print("---")
```

### Bulk Availability Checks

```python
from wolt_api_mcp import call_tool_bulk
from fastmcp.contrib.bulk_tool_caller import CallToolRequest
import asyncio

# Check availability for multiple restaurants
restaurant_slugs = [
    "pizza-hut-tel-aviv-central",
    "mcdonalds-jerusalem-center", 
    "sushi-bar-haifa-downtown"
]

reqs = [
    CallToolRequest(
        tool="check_restaurant_availability",
        arguments={"slug": slug, "rate_limit_delay": 0.5},
    )
    for slug in restaurant_slugs
]

results = asyncio.run(call_tool_bulk(reqs))
for result in results:
    print(result.result)
```

## Advanced Usage Patterns

### Search with Rate Limiting

```python
# For comprehensive searches, use slower rate limiting
from wolt_api_mcp import search_restaurants

result = search_restaurants.fn(
    query="burger",
    city=None,  # Search all cities
    max_results=50,
    rate_limit_delay=2.0  # Slower to be respectful to the API
)
print(result)
```

### City-Specific Restaurant Discovery

```python
from wolt_api_mcp import get_nearby_restaurants

# Get top-rated restaurants in Tel Aviv
tel_aviv_restaurants = get_nearby_restaurants.fn(
    city="tel-aviv",
    max_results=30,
    only_open=False,  # Include closed restaurants too
    rate_limit_delay=1.0
)

# Get only open pizza places in Jerusalem
jerusalem_pizza = get_nearby_restaurants.fn(
    city="jerusalem", 
    cuisine_filter="pizza",
    only_open=True,
    max_results=15,
    rate_limit_delay=1.5
)

print("Tel Aviv Restaurants:")
print(tel_aviv_restaurants)
print("\nJerusalem Pizza (Open):")
print(jerusalem_pizza)
```

### Error Handling Example

```python
from wolt_api_mcp import check_restaurant_availability, WoltAPIError

try:
    result = check_restaurant_availability.fn("invalid-restaurant-slug")
    print(result)
except Exception as e:
    print(f"Error occurred: {e}")
    # The MCP server handles errors gracefully and returns user-friendly messages
```

## Integration with MCP Clients

### Claude Desktop Configuration

Add this to your `mcp.json` file:

```json
{
  "mcpServers": {
    "wolt-api-mcp": {
      "command": "python",
      "args": ["-m", "wolt_api_mcp.server"],
      "env": {}
    }
  }
}
```

### Direct Server Usage

```python
from wolt_api_mcp.server import main

# Run the MCP server directly
if __name__ == "__main__":
    main()
```

## Parameter Reference

### search_restaurants

- `query` (required): Restaurant name or search term (2-100 chars)
- `city` (optional): City filter (max 50 chars)  
- `max_results` (optional): Max results to return (1-50, default: 20)
- `rate_limit_delay` (optional): Delay between requests (0.1-5.0s, default: 1.0)

### check_restaurant_availability

- `slug` (required): Restaurant slug from Wolt URL (3-200 chars, lowercase alphanumeric with hyphens)
- `rate_limit_delay` (optional): Delay between requests (0.1-5.0s, default: 1.0)

### get_nearby_restaurants

- `city` (required): City name in Israel (2-50 chars)
- `cuisine_filter` (optional): Cuisine type filter (max 50 chars)
- `max_results` (optional): Max results to return (1-100, default: 20)
- `only_open` (optional): Only return open restaurants (default: false)
- `rate_limit_delay` (optional): Delay between requests (0.1-5.0s, default: 1.0)

## Best Practices

1. **Rate Limiting**: Use appropriate rate limiting delays (1.0-2.0s) for comprehensive searches
2. **Error Handling**: The server provides user-friendly error messages for common issues
3. **Bulk Operations**: Use bulk tool calling for multiple operations to improve efficiency
4. **City Names**: Use lowercase city names (e.g., "tel-aviv", "jerusalem", "haifa")
5. **Slug Format**: Restaurant slugs should be lowercase with hyphens (e.g., "pizza-hut-tel-aviv-central")

KEY TERMS:
* Wolt API MCP
* search_restaurants  
* check_restaurant_availability
* get_nearby_restaurants
* call_tools_bulk
* call_tool_bulk
* CallToolRequest
* bulk tool calls
* restaurant search
* availability check
* wolt_api_mcp.server
* fastmcp.contrib.bulk_tool_caller
* MCP client integration