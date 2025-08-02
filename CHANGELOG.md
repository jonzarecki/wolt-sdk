# Changelog

All notable changes to the Wolt Restaurant Availability API will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2025-08-02

### Added
- **Israel-Wide Coverage**: Complete restaurant availability checking across all of Israel
- **Geographic Search**: 17+ major population centers from Eilat to Kiryat Shmona
- **Real-Time Data**: Live restaurant availability status from Wolt Israel APIs
- **Comprehensive API Client**: 
  - `is_restaurant_open(slug)` - Check specific restaurant status
  - `get_nearby_restaurants(lat, lon, radius)` - Find restaurants by location
  - `find_restaurants(query, lat, lon)` - Search restaurants by name/cuisine
- **Built-in Rate Limiting**: Respects Wolt's API limits with configurable delays
- **Robust Error Handling**: Specific exceptions for different error scenarios
- **Complete Test Suite**: 9 comprehensive tests against real Wolt APIs
- **Example Scripts**: 
  - Basic usage demonstration
  - Restaurant monitoring script
  - Cuisine analytics tool
- **Documentation**: Complete API documentation and usage examples

### Technical Implementation
- **Smart Geographic Coverage**: Strategic search points across Israeli cities
- **Automatic Retry Logic**: Handles rate limits with intelligent backoff
- **Restaurant Data Models**: Structured dataclasses for restaurant information
- **Performance Optimized**: Early termination when restaurants found

### Supported Locations
- **Tel Aviv Metropolitan Area** (Gush Dan)
- **Jerusalem & Surroundings**
- **Haifa & Northern Israel**
- **Central Israel** (Netanya, Rehovot, Modi'in)
- **Southern Israel** (Be'er Sheva, Ashkelon, Ashdod, Eilat)
- **Additional Coverage** (Nazareth, Tiberias, Kiryat Shmona)

### Performance
- **Local searches**: 1-3 seconds
- **Israel-wide lookups**: 2-8 seconds per restaurant
- **Rate limit compliance**: Built-in delays and retry logic

### Testing
- **Real API Testing**: All functionality tested against live Wolt Israel endpoints
- **Comprehensive Coverage**: Tests for availability, search, error handling, and performance
- **Regression Prevention**: Specific tests for known restaurant slugs
- **Geographic Validation**: Tests across multiple Israeli cities

## [Future Releases]

### Planned Features
- **Caching Layer**: Optional result caching for improved performance
- **Webhook Support**: Real-time notifications for restaurant status changes
- **Batch Operations**: Efficient checking of multiple restaurants
- **Analytics Dashboard**: Restaurant availability analytics and insights
- **Menu Integration**: Access to restaurant menus and pricing
- **Delivery Time Estimation**: Real-time delivery estimates

---

## Development Notes

This project was built using Test-Driven Development (TDD) with emphasis on:
- **Real API Integration**: No mocked tests - everything tested against live Wolt APIs
- **Simplicity**: Clean, readable code over complex abstractions  
- **Reliability**: Comprehensive error handling and rate limiting
- **Performance**: Optimized search patterns for Israeli geographic coverage

## API Discovery Journey

During development, we investigated Wolt's API landscape:
- **Official APIs**: Require merchant credentials (not suitable for consumer use)
- **Direct Venue APIs**: Listed in documentation but return 404 for Israeli venues
- **Geographic Search**: Most reliable method using Wolt's restaurant listing endpoints

Our implementation uses the most stable and comprehensive approach for Israeli restaurant availability.