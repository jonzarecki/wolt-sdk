"""
Wolt Restaurant Availability API

A simple Python API for checking restaurant availability on Wolt in Israel.
"""

from .client import WoltAPI
from .models import Restaurant
from .exceptions import WoltAPIError

__version__ = "0.1.0"
__all__ = ["WoltAPI", "Restaurant", "WoltAPIError"]