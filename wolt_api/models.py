"""
Data models for Wolt API responses
"""
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Restaurant:
    """Represents a restaurant from Wolt API"""
    name: str
    slug: str
    is_online: bool
    cuisine_types: List[str]
    rating: Optional[float] = None
    delivery_estimate: Optional[str] = None
    image_url: Optional[str] = None
    
    def __str__(self) -> str:
        status = "🟢 OPEN" if self.is_online else "🔴 CLOSED"
        return f"{self.name} ({status})"