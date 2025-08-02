# Wolt Restaurant Availability API

A simple Python API for programmatically checking restaurant availability on Wolt in Israel.

## Features

- **Israel-Wide Coverage**: Check any restaurant across all of Israel
- **Comprehensive Restaurant Search**: Find restaurants by name and location nationwide  
- **Bulk Restaurant Scanning**: Get nearby restaurants in any Israeli city
- **Built-in Rate Limiting**: Respects API limits with configurable delays
- **Real API Testing**: All functionality tested against live Wolt Israel endpoints
- **Geographic Coverage**: From Eilat to Kiryat Shmona - complete national coverage

## Quick Start

```python
from wolt_api import WoltAPI

api = WoltAPI()

# Check if a specific restaurant is open
is_open = api.is_restaurant_open("restaurant-slug")

# Find restaurants by name in Tel Aviv
restaurants = api.find_restaurants("pizza", lat=32.0853, lon=34.7818)

# Get all nearby restaurants
nearby = api.get_nearby_restaurants(lat=32.0853, lon=34.7818, radius=2000)
```

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Install in development mode (optional)
pip install -e .
```

## Testing

```bash
# Run all tests
pytest tests/ -v

# Run specific test
pytest tests/test_wolt_api.py::TestWoltAPI::test_get_nearby_restaurants_tel_aviv -v
```

## Examples

The `examples/` directory contains several demonstration scripts:

- **`basic_usage.py`** - Basic API functionality demo
- **`cuisine_analytics.py`** - Analyze restaurant data by cuisine type  
- **`monitoring_script.py`** - Monitor specific restaurants for status changes

Run examples:
```bash
python examples/basic_usage.py
python examples/cuisine_analytics.py
```

## Complete Demo

Run the comprehensive demo:
```bash
python demo.py
```

## API Endpoints Used

This package uses Wolt's unofficial consumer API:
- Venue status: `GET /order-catalog/api/v1/venues/{slug}/dynamic`
- Search venues: `GET /search/v2/venues`
- Nearby venues: `GET /order-catalog/api/v1/pages/restaurants`

## Rate Limits & Performance

The API respects Wolt's rate limits (~60 requests/minute) with built-in delays.

**Performance Notes:**
- **Local searches** (specific coordinates): ~1-3 seconds
- **Israel-wide restaurant lookup**: ~2-8 seconds per restaurant (searches up to 17+ areas)
- **Rate limit considerations**: May hit Wolt's limits during rapid bulk searches
- **Recommendation**: Cache results for frequently checked restaurants

**Coverage Areas:**
- Tel Aviv Metropolitan Area (Gush Dan)
- Jerusalem & surroundings
- Haifa & Northern Israel  
- Central Israel (Netanya, Rehovot, Modi'in)
- Southern Israel (Be'er Sheva, Ashkelon, Ashdod, Eilat)
- And more - complete national coverage!