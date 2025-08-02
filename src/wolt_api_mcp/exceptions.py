"""
Custom exceptions for Wolt API
"""


class WoltAPIError(Exception):
    """Base exception for Wolt API errors"""
    pass


class RestaurantNotFoundError(WoltAPIError):
    """Raised when a restaurant slug is not found"""
    pass


class RateLimitError(WoltAPIError):
    """Raised when rate limit is exceeded"""
    pass


class APIUnavailableError(WoltAPIError):
    """Raised when Wolt API is unavailable"""
    pass