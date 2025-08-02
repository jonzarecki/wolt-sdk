# Wolt Restaurant Availability MCP

[![CI](https://github.com/jonzarecki/wolt-sdk/actions/workflows/ci.yml/badge.svg)](https://github.com/jonzarecki/wolt-sdk/actions/workflows/ci.yml)

A Model Context Protocol (MCP) server that exposes the Wolt restaurant availability API for Israel. It provides tools for searching restaurants, checking availability, and gathering delivery information across Israeli cities, designed to work seamlessly with Claude and other MCP clients.

## Installation

```bash
pip install git+https://github.com/jonzarecki/wolt-sdk
```

You can also run the server via `npx` without installing it system-wide:

```bash
npx --yes github:jonzarecki/wolt-sdk
```

or clone the repository and install in editable mode:

```bash
git clone https://github.com/jonzarecki/wolt-sdk
cd wolt-sdk
pip install -e .
```

## Usage

Run the server directly (stdout/stdin transport):

```bash
wolt-mcp
```

The server exposes three main tools:

- `search_restaurants(...)`: search for restaurants by name across Israel
- `check_restaurant_availability(...)`: check if a specific restaurant is open  
- `get_nearby_restaurants(...)`: get restaurants near a specific location

With FastMCP 2.9+ you can batch tool calls for efficiency using `call_tools_bulk` or `call_tool_bulk` from this package.

See the docstrings in `wolt_api_mcp.server` for full parameter details.

For more examples see [docs/examples.md](docs/examples.md). A quick Python usage snippet:

```python
from wolt_api_mcp import search_restaurants
print(search_restaurants.fn(query="Pizza Hut", city="tel-aviv", max_results=10))
```

## Features

- 🔍 **Restaurant Search**: Find restaurants by name with city filtering
- ✅ **Availability Checking**: Real-time restaurant open/closed status
- 🏙️ **Location-Based Discovery**: Get restaurants near specific cities
- 🍕 **Cuisine Filtering**: Filter results by cuisine type  
- ⚡ **Bulk Operations**: Efficient batch processing of multiple requests
- 🛡️ **Input Validation**: Comprehensive parameter validation with Pydantic
- ⏱️ **Rate Limiting**: Built-in rate limiting to respect API usage
- 🚫 **Error Handling**: Graceful error handling with user-friendly messages
- 📊 **Rich Formatting**: Well-formatted output with status indicators

## MCP Client Configuration

If your MCP client supports automatic server installation, add the following JSON to your `mcp.json` file. The client will fetch the package via `npx` and launch the server for you:

```json
{
  "mcpServers": {
    "wolt-api-mcp": {
      "command": "npx --yes github:jonzarecki/wolt-sdk",
      "env": {}
    }
  }
}
```

For local development or direct installation:

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

## Development

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for details. After cloning the repository run:

```bash
pip install -e .[test,dev]
```

Install the pre-commit hooks as well:

```bash
pre-commit install
```

Then run the test suite with coverage:

```bash
pytest --cov=wolt_api_mcp --cov-report=term-missing
```

### Code Quality

The project uses modern Python tooling:

```bash
# Formatting
black src/ tests/

# Linting  
ruff check src/ tests/

# Type checking
mypy src/

# Security scanning
bandit -r src/
safety check
```

## API Reference

### Tools

#### `search_restaurants`
Search for restaurants by name across Israel.

**Parameters:**
- `query` (str): Restaurant name or search term (2-100 chars)
- `city` (str, optional): City filter (max 50 chars)
- `max_results` (int): Maximum results (1-50, default: 20)
- `rate_limit_delay` (float): Request delay (0.1-5.0s, default: 1.0)

#### `check_restaurant_availability`
Check if a specific restaurant is currently open.

**Parameters:**
- `slug` (str): Restaurant slug from Wolt URL (3-200 chars)
- `rate_limit_delay` (float): Request delay (0.1-5.0s, default: 1.0)

#### `get_nearby_restaurants`  
Get restaurants near a specific location.

**Parameters:**
- `city` (str): City name in Israel (2-50 chars)
- `cuisine_filter` (str, optional): Cuisine type filter (max 50 chars)
- `max_results` (int): Maximum results (1-100, default: 20)
- `only_open` (bool): Only return open restaurants (default: false)
- `rate_limit_delay` (float): Request delay (0.1-5.0s, default: 1.0)

## Examples

### Basic Restaurant Search
```python
# Search for pizza places in Tel Aviv
result = search_restaurants.fn("pizza", city="tel-aviv", max_results=10)
```

### Check Availability
```python
# Check if a specific restaurant is open
result = check_restaurant_availability.fn("pizza-hut-tel-aviv-central")
```

### Get Nearby Restaurants
```python
# Get sushi restaurants in Jerusalem that are currently open
result = get_nearby_restaurants.fn(
    city="jerusalem", 
    cuisine_filter="sushi", 
    only_open=True,
    max_results=15
)
```

### Bulk Operations
```python
from wolt_api_mcp import call_tools_bulk
from fastmcp.contrib.bulk_tool_caller import CallToolRequest
import asyncio

requests = [
    CallToolRequest(tool="search_restaurants", arguments={"query": "burger", "city": "tel-aviv"}),
    CallToolRequest(tool="search_restaurants", arguments={"query": "sushi", "city": "jerusalem"}),
]

results = asyncio.run(call_tools_bulk(requests))
```

## Rate Limiting Best Practices

- Use 1.0-2.0 second delays for comprehensive searches
- Use 0.5 second delays for bulk availability checks
- Respect the API and avoid excessive requests

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This library is for educational and research purposes. Please respect Wolt's terms of service and use the API responsibly.