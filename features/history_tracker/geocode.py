"""
Geocoding Module for Weather Application

This module provides geocoding functionality to convert city names to 
latitude and longitude coordinates using the Nominatim service from OpenStreetMap.
Includes intelligent caching, error handling, and validation features.

"""

import logging
import time
from typing import Tuple, Optional, Dict, Any
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError, GeocoderUnavailable

# Configure logging for debugging geocoding issues
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global cache for storing geocoding results
# Structure: {city_key: {'coords': (lat, lon), 'timestamp': unix_timestamp, 'full_name': str}}
_geocode_cache: Dict[str, Dict[str, Any]] = {}

# Configuration constants
CACHE_EXPIRY_HOURS = 24  # Cache entries expire after 24 hours
DEFAULT_TIMEOUT = 10     # Default timeout for geocoding requests
MAX_RETRIES = 3         # Maximum retry attempts for failed requests
USER_AGENT = "WeatherApp_Geocoder_v1.0"  # User agent for API requests


def get_lat_lon(city: str, timeout: int = DEFAULT_TIMEOUT) -> Tuple[Optional[float], Optional[float]]:
    """
    Geocode a city name to latitude and longitude coordinates.
    
    Uses intelligent caching to speed up repeated lookups and includes
    comprehensive error handling for various failure scenarios.
    
    """
    # Input validation
    if not city or not isinstance(city, str):
        logger.warning(f"Invalid city input: {city}")
        return None, None
    
    # Normalize city name for consistent caching
    city_key = _normalize_city_name(city)
    
    # Check cache first
    cached_result = _get_from_cache(city_key)
    if cached_result is not None:
        logger.info(f"Cache hit for city: {city}")
        return cached_result
    
    # Initialize geocoder
    geolocator = Nominatim(user_agent=USER_AGENT)
    
    # Attempt geocoding with retry logic
    for attempt in range(MAX_RETRIES):
        try:
            logger.info(f"Geocoding attempt {attempt + 1} for: {city}")
            
            # Perform geocoding with enhanced query
            location = geolocator.geocode(
                city, 
                timeout=timeout,
                exactly_one=True,  # Return only the best match
                addressdetails=True  # Get detailed address information
            )
            
            if location:
                coordinates = (location.latitude, location.longitude)
                
                # Cache the successful result
                _cache_result(city_key, coordinates, location.address)
                
                logger.info(f"Successfully geocoded {city} to {coordinates}")
                return coordinates
            else:
                logger.warning(f"No results found for city: {city}")
                break  # No point in retrying if no results found
                
        except GeocoderTimedOut:
            logger.warning(f"Geocoding timeout for {city} (attempt {attempt + 1})")
            if attempt == MAX_RETRIES - 1:
                logger.error(f"All geocoding attempts timed out for: {city}")
                
        except GeocoderServiceError as e:
            logger.error(f"Geocoding service error for {city}: {e}")
            if attempt == MAX_RETRIES - 1:
                break  # Don't retry on service errors
                
        except GeocoderUnavailable as e:
            logger.error(f"Geocoding service unavailable for {city}: {e}")
            break  # Don't retry if service is unavailable
            
        except Exception as e:
            logger.error(f"Unexpected error geocoding {city}: {e}")
            if attempt == MAX_RETRIES - 1:
                break
    
    # Cache the failed result to avoid repeated failed requests
    _cache_result(city_key, (None, None), None)
    return None, None


def get_city_info(city: str, timeout: int = DEFAULT_TIMEOUT) -> Dict[str, Any]:
    """
    Get comprehensive information about a city including coordinates and formatted address.
    
    """
    result = {
        'coordinates': (None, None),
        'formatted_address': None,
        'country': None,
        'state': None,
        'success': False
    }
    
    if not city or not isinstance(city, str):
        return result
    
    city_key = _normalize_city_name(city)
    
    # Check if we have cached detailed info
    if city_key in _geocode_cache and not _is_cache_expired(city_key):
        cache_entry = _geocode_cache[city_key]
        result['coordinates'] = cache_entry['coords']
        result['formatted_address'] = cache_entry.get('full_name')
        result['success'] = cache_entry['coords'] != (None, None)
        return result
    
    # Perform geocoding
    geolocator = Nominatim(user_agent=USER_AGENT)
    
    try:
        location = geolocator.geocode(
            city, 
            timeout=timeout,
            exactly_one=True,
            addressdetails=True
        )
        
        if location:
            result['coordinates'] = (location.latitude, location.longitude)
            result['formatted_address'] = location.address
            result['success'] = True
            
            # Extract additional details if available
            if hasattr(location, 'raw') and 'address' in location.raw:
                address_parts = location.raw['address']
                result['country'] = address_parts.get('country')
                result['state'] = address_parts.get('state') or address_parts.get('province')
            
            # Cache the result
            _cache_result(city_key, result['coordinates'], location.address)
            
    except Exception as e:
        logger.error(f"Error getting city info for {city}: {e}")
    
    return result


def validate_coordinates(lat: float, lon: float) -> bool:
    """
    Validate that latitude and longitude values are within valid ranges.
    
    """
    try:
        lat_valid = -90 <= float(lat) <= 90
        lon_valid = -180 <= float(lon) <= 180
        return lat_valid and lon_valid
    except (ValueError, TypeError):
        return False


def clear_cache() -> None:
    """
    Clear the geocoding cache.
    
    Useful for testing or when you want to force fresh geocoding requests.

    """
    global _geocode_cache
    _geocode_cache.clear()
    logger.info("Geocoding cache cleared")


def get_cache_stats() -> Dict[str, Any]:
    """
    Get statistics about the geocoding cache.
    
    """
    total_entries = len(_geocode_cache)
    successful_entries = sum(1 for entry in _geocode_cache.values() 
                           if entry['coords'] != (None, None))
    expired_entries = sum(1 for key in _geocode_cache.keys() 
                         if _is_cache_expired(key))
    
    return {
        'total_entries': total_entries,
        'successful_entries': successful_entries,
        'failed_entries': total_entries - successful_entries,
        'expired_entries': expired_entries,
        'cache_size_mb': _estimate_cache_size()
    }


def _normalize_city_name(city: str) -> str:
    """
    Normalize city name for consistent caching.
    
    """
    return city.lower().strip()


def _get_from_cache(city_key: str) -> Optional[Tuple[Optional[float], Optional[float]]]:
    """
    Retrieve coordinates from cache if available and not expired.
    
    """
    if city_key not in _geocode_cache:
        return None
    
    if _is_cache_expired(city_key):
        logger.info(f"Cache entry expired for: {city_key}")
        del _geocode_cache[city_key]
        return None
    
    return _geocode_cache[city_key]['coords']


def _cache_result(city_key: str, coordinates: Tuple[Optional[float], Optional[float]], 
                 full_name: Optional[str]) -> None:
    """
    Cache geocoding result with timestamp.
    
    """
    _geocode_cache[city_key] = {
        'coords': coordinates,
        'timestamp': time.time(),
        'full_name': full_name
    }


def _is_cache_expired(city_key: str) -> bool:
    """
    Check if a cache entry has expired.
    
    """
    if city_key not in _geocode_cache:
        return True
    
    entry_time = _geocode_cache[city_key]['timestamp']
    current_time = time.time()
    age_hours = (current_time - entry_time) / 3600
    
    return age_hours > CACHE_EXPIRY_HOURS


def _estimate_cache_size() -> float:
    """
    Estimate the memory usage of the cache in MB.
    
    """
    import sys
    total_size = sys.getsizeof(_geocode_cache)
    
    for key, value in _geocode_cache.items():
        total_size += sys.getsizeof(key)
        total_size += sys.getsizeof(value)
        for v in value.values():
            total_size += sys.getsizeof(v)
    
    return total_size / (1024 * 1024)  # Convert to MB


# Example usage and testing functions
if __name__ == "__main__":
    # Test the geocoding functions
    test_cities = ["New York", "London", "Tokyo", "InvalidCity123"]
    
    # Run tests silently for validation
    for city in test_cities:
        coords = get_lat_lon(city)
        
        if coords != (None, None):
            city_info = get_city_info(city)
            # Tests run silently - results available via logging
    
    # Cache statistics available via get_cache_stats() if needed
    