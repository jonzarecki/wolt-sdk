"""
Wolt Restaurant Availability MCP Server

A Model Context Protocol (MCP) server that exposes Wolt restaurant availability
API for Israel, providing tools for searching restaurants and checking availability.
"""

from .server import _bulk_tools, main, mcp, search_restaurants, check_restaurant_availability, get_nearby_restaurants
from .client import WoltAPI
from .models import Restaurant
from .exceptions import WoltAPIError

__version__ = "0.2.0"
__all__ = [
    "main",
    "mcp",
    "search_restaurants",
    "check_restaurant_availability", 
    "get_nearby_restaurants",
    "call_tool_bulk",
    "call_tools_bulk",
    "WoltAPI",
    "Restaurant",
    "WoltAPIError",
]

call_tool_bulk = _bulk_tools.call_tool_bulk
call_tools_bulk = _bulk_tools.call_tools_bulk