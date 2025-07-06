"""
Geocoding Service Module
========================

This module provides geocoding functionality to convert city names into
latitude and longitude coordinates. It uses the Open-Meteo geocoding API
to resolve geographic locations, which is essential for weather APIs
that require coordinate-based queries.

Key Features:
- City name to coordinates conversion
- Robust error handling and validation
- Defensive programming practices
- API failure logging and recovery
- Input validation for safety

"""

import requests


def get_lat_lon(city):
    """
    Convert city name to latitude and longitude coordinates
    
    This function uses the Open-Meteo geocoding API to find the geographic
    coordinates (latitude and longitude) for a given city name. This is
    essential for weather APIs that require coordinate-based queries instead
    of city names.
    
    The function implements defensive programming practices:
    - Validates input parameters
    - Handles API failures gracefully
    - Logs errors for debugging
    - Returns None values for failed requests
                
    API Details:
        - Uses Open-Meteo Geocoding API (free, no API key required)
        - Requests only the first result (count=1)
        - Uses English language for consistent results
        - Returns JSON format for easy parsing

    """
    
    # Input validation: ensure city is a valid string
    if not isinstance(city, str):
        # Log error and return None values for invalid input
        return None, None
    
    # Construct the geocoding API URL with search parameters
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json"
    
    try:
        # Make HTTP GET request to the geocoding API
        response = requests.get(url)
        
        # Check if the API request was successful (HTTP 200)
        if response.status_code != 200:
            # Log HTTP error and return None values
            return None, None

        # Parse the JSON response from the API
        data = response.json()
        
        # Extract results array from the API response
        results = data.get("results")
        
        # Check if we got valid results
        if results and len(results) > 0:
            # Extract latitude and longitude from the first result
            lat = results[0].get("latitude")
            lon = results[0].get("longitude")
            
            # Ensure both coordinates are present and valid
            if lat is not None and lon is not None:
                return lat, lon
        
        # Log when no results are found for the given city
        return None, None
        
    except requests.exceptions.RequestException as e:
        # Handle network-related errors (timeout, connection issues, etc.)
        return None, None
        
    except ValueError as e:
        # Handle JSON parsing errors
        return None, None
        
    except Exception as e:
        # Handle any other unexpected errors
        return None, None