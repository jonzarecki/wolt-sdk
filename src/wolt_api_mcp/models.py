"""
Data models for Wolt API with comprehensive validation
"""

from typing import List, Optional
from pydantic import BaseModel, Field, validator


class Restaurant(BaseModel):
    """Represents a restaurant from Wolt API with comprehensive validation."""
    
    name: str = Field(
        ...,
        description="Restaurant name",
        min_length=1,
        max_length=200,
    )
    
    slug: str = Field(
        ...,
        description="Restaurant slug identifier for URLs",
        min_length=3,
        max_length=200,
        pattern=r"^[a-z0-9\-_]+$",
    )
    
    is_online: bool = Field(
        ...,
        description="Whether the restaurant is currently online",
    )
    
    cuisine_types: List[str] = Field(
        default_factory=list,
        description="List of cuisine types served",
    )
    
    rating: Optional[float] = Field(
        None,
        description="Restaurant rating",
        ge=0.0,
        le=5.0,
    )
    
    delivery_estimate: Optional[str] = Field(
        None,
        description="Estimated delivery time",
        max_length=50,
    )
    
    image_url: Optional[str] = Field(
        None,
        description="URL to restaurant image",
        max_length=500,
    )
    
    location: Optional[str] = Field(
        None,
        description="Restaurant location/address",
        max_length=200,
    )
    
    city: Optional[str] = Field(
        None,
        description="City where the restaurant is located",
        max_length=100,
    )
    
    # Alias for compatibility with MCP server
    @property
    def is_open(self) -> bool:
        """Alias for is_online for compatibility."""
        return self.is_online
    
    @validator("slug")
    def validate_slug(cls, v: str) -> str:
        """Validate that slug contains only lowercase letters, numbers, hyphens, and underscores."""
        return v.lower()
    
    @validator("name")
    def validate_name(cls, v: str) -> str:
        """Validate restaurant name."""
        if not v.strip():
            raise ValueError("Restaurant name cannot be empty")
        return v.strip()
    
    @validator("cuisine_types")
    def validate_cuisine_types(cls, v: List[str]) -> List[str]:
        """Validate cuisine types list."""
        return [cuisine.strip() for cuisine in v if cuisine.strip()]
    
    def __str__(self) -> str:
        """String representation of the restaurant."""
        status = "🟢 OPEN" if self.is_online else "🔴 CLOSED"
        return f"{self.name} ({status})"
    
    class Config:
        """Pydantic configuration."""
        validate_assignment = True
        extra = "forbid"
        schema_extra = {
            "example": {
                "name": "Pizza Hut",
                "slug": "pizza-hut-tel-aviv-central",
                "is_online": True,
                "cuisine_types": ["Pizza", "Fast Food"],
                "rating": 4.2,
                "delivery_estimate": "30-45 min",
                "image_url": "https://example.com/image.jpg",
                "location": "Tel Aviv Central",
                "city": "tel-aviv",
            }
        }


class SearchParams(BaseModel):
    """Parameters for restaurant search with validation."""
    
    query: str = Field(
        ...,
        description="Search query for restaurant name",
        min_length=2,
        max_length=100,
    )
    
    city: Optional[str] = Field(
        None,
        description="City filter for search",
        max_length=50,
    )
    
    max_results: int = Field(
        20,
        description="Maximum number of results to return",
        ge=1,
        le=100,
    )
    
    rate_limit_delay: float = Field(
        1.0,
        description="Delay between requests in seconds",
        ge=0.1,
        le=5.0,
    )
    
    @validator("query")
    def validate_query(cls, v: str) -> str:
        """Validate search query."""
        query = v.strip()
        if not query:
            raise ValueError("Search query cannot be empty")
        return query
    
    @validator("city")
    def validate_city(cls, v: Optional[str]) -> Optional[str]:
        """Validate city name."""
        if v is not None:
            city = v.strip().lower()
            if not city:
                return None
            return city
        return v
    
    class Config:
        """Pydantic configuration."""
        validate_assignment = True
        extra = "forbid"