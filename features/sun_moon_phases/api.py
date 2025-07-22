"""
Sun and Moon Phases API Module
Fetches astronomical data using the Sunrise-Sunset API (free, no key required)
"""

import requests
import math
import datetime
from typing import Dict, Tuple, Optional


def get_coordinates_for_city(city: str) -> Tuple[Optional[float], Optional[float]]:
    """Get latitude and longitude for a city using Open-Meteo geocoding"""
    if not isinstance(city, str) or not city.strip():
        return None, None
    
    try:
        url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            results = data.get("results", [])
            
            if results:
                lat = results[0].get("latitude")
                lon = results[0].get("longitude")
                return lat, lon
        
        return None, None
        
    except Exception as e:
        return None, None


def fetch_sun_moon_data(city: str) -> Dict:
    """
    Fetch comprehensive sun and moon data for a city
    Uses Sunrise-Sunset API (free) + calculations for moon data
    """
    # Get coordinates
    lat, lon = get_coordinates_for_city(city)
    
    if not lat or not lon:
        return get_fallback_data()
    
    try:
        # Fetch sunrise/sunset from free API
        url = f"https://api.sunrise-sunset.org/json?lat={lat}&lng={lon}&formatted=0"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            results = data.get("results", {})
            
            # Calculate current sun position
            sun_position = calculate_sun_position(lat, lon)
            
            # Calculate moon phase and position
            moon_phase = calculate_moon_phase()
            moon_position = calculate_moon_position(lat, lon)
            
            # Check if currently daytime
            is_day = is_currently_daytime(results.get("sunrise"), results.get("sunset"))
            
            return {
                "city": city,
                "latitude": lat,
                "longitude": lon,
                "sunrise": results.get("sunrise"),
                "sunset": results.get("sunset"),
                "solar_noon": results.get("solar_noon"),
                "day_length": results.get("day_length"),
                "sun_position": sun_position,
                "moon_phase": moon_phase,
                "moon_phase_name": get_moon_phase_name(moon_phase),
                "moon_illumination": calculate_moon_illumination(moon_phase),
                "moon_position": moon_position,
                "is_daytime": is_day,
                "current_time": datetime.datetime.now().isoformat(),
                "error": None
            }
        
        return get_fallback_data(f"API returned status {response.status_code}")
        
    except Exception as e:
        return get_fallback_data(str(e))


def calculate_sun_position(lat: float, lon: float) -> Dict:
    """Calculate current sun position (elevation and azimuth)"""
    try:
        now = datetime.datetime.utcnow()
        
        # Day of year
        day_of_year = now.timetuple().tm_yday
        
        # Solar declination angle
        declination = 23.45 * math.sin(math.radians(360 * (284 + day_of_year) / 365))
        
        # Time correction for longitude
        time_correction = lon / 15
        
        # Solar hour angle
        hour_angle = 15 * (now.hour + now.minute/60 + time_correction - 12)
        
        # Convert to radians
        lat_rad = math.radians(lat)
        dec_rad = math.radians(declination)
        hour_rad = math.radians(hour_angle)
        
        # Solar elevation angle
        elevation = math.degrees(math.asin(
            math.sin(lat_rad) * math.sin(dec_rad) + 
            math.cos(lat_rad) * math.cos(dec_rad) * math.cos(hour_rad)
        ))
        
        # Solar azimuth angle
        azimuth = math.degrees(math.atan2(
            math.sin(hour_rad),
            math.cos(hour_rad) * math.sin(lat_rad) - math.tan(dec_rad) * math.cos(lat_rad)
        ))
        
        # Normalize azimuth to 0-360
        if azimuth < 0:
            azimuth += 360
        
        return {
            "elevation": round(max(elevation, -90), 2),  # Clamp to realistic values
            "azimuth": round(azimuth, 2),
            "hour_angle": round(hour_angle, 2),
            "declination": round(declination, 2)
        }
        
    except Exception as e:
        return {"elevation": 45, "azimuth": 180, "hour_angle": 0, "declination": 0}


def calculate_moon_phase() -> float:
    """
    Calculate current moon phase (0-1, where 0/1 = new moon, 0.5 = full moon)
    """
    try:
        # Known new moon date (2000-01-06 18:14 UTC)
        known_new_moon = datetime.datetime(2000, 1, 6, 18, 14)
        now = datetime.datetime.utcnow()
        
        # Moon cycle length in days
        cycle_length = 29.53058867
        
        # Calculate days since known new moon
        days_since = (now - known_new_moon).total_seconds() / (24 * 3600)
        
        # Calculate phase (0-1)
        phase = (days_since % cycle_length) / cycle_length
        
        return round(phase, 4)
        
    except Exception as e:
        return 0.25  # Default to waxing crescent


def calculate_moon_position(lat: float, lon: float) -> Dict:
    """Calculate approximate moon position"""
    try:
        now = datetime.datetime.utcnow()
        
        # Simplified moon position calculation
        # Moon's orbit is complex, this is an approximation
        
        # Days since J2000.0 epoch
        j2000 = datetime.datetime(2000, 1, 1, 12, 0)
        days_since_j2000 = (now - j2000).total_seconds() / (24 * 3600)
        
        # Moon's mean longitude (degrees)
        moon_longitude = (218.316 + 13.176396 * days_since_j2000) % 360
        
        # Moon's mean anomaly (degrees) 
        moon_anomaly = (134.963 + 13.064993 * days_since_j2000) % 360
        
        # Simplified moon elevation (this is very approximate)
        # Real calculation would need more orbital elements
        moon_elevation = 30 * math.sin(math.radians(moon_longitude)) + lat/4
        
        # Moon azimuth (simplified)
        moon_azimuth = (moon_longitude + 180) % 360
        
        return {
            "elevation": round(max(min(moon_elevation, 90), -90), 2),
            "azimuth": round(moon_azimuth, 2),
            "longitude": round(moon_longitude, 2)
        }
        
    except Exception as e:
        return {"elevation": 30, "azimuth": 90, "longitude": 0}


def get_moon_phase_name(phase: float) -> str:
    """Convert moon phase value to descriptive name"""
    if phase < 0.0625 or phase >= 0.9375:
        return "New Moon"
    elif 0.0625 <= phase < 0.1875:
        return "Waxing Crescent"
    elif 0.1875 <= phase < 0.3125:
        return "First Quarter"
    elif 0.3125 <= phase < 0.4375:
        return "Waxing Gibbous"
    elif 0.4375 <= phase < 0.5625:
        return "Full Moon"
    elif 0.5625 <= phase < 0.6875:
        return "Waning Gibbous"
    elif 0.6875 <= phase < 0.8125:
        return "Last Quarter"
    else:
        return "Waning Crescent"


def get_moon_phase_emoji(phase: float) -> str:
    """Get emoji representation of moon phase"""
    if phase < 0.0625 or phase >= 0.9375:
        return "🌑"  # New Moon
    elif 0.0625 <= phase < 0.1875:
        return "🌒"  # Waxing Crescent
    elif 0.1875 <= phase < 0.3125:
        return "🌓"  # First Quarter
    elif 0.3125 <= phase < 0.4375:
        return "🌔"  # Waxing Gibbous
    elif 0.4375 <= phase < 0.5625:
        return "🌕"  # Full Moon
    elif 0.5625 <= phase < 0.6875:
        return "🌖"  # Waning Gibbous
    elif 0.6875 <= phase < 0.8125:
        return "🌗"  # Last Quarter
    else:
        return "🌘"  # Waning Crescent


def calculate_moon_illumination(phase: float) -> float:
    """Calculate percentage of moon that is illuminated"""
    try:
        # Illumination varies with phase
        # Full moon (0.5) = 100%, New moon (0 or 1) = 0%
        if phase <= 0.5:
            illumination = phase * 2  # 0 to 1 (0% to 100%)
        else:
            illumination = 2 - (phase * 2)  # 1 to 0 (100% to 0%)
        
        return round(illumination * 100, 1)
    except Exception:
        return 50.0


def is_currently_daytime(sunrise_str: Optional[str], sunset_str: Optional[str]) -> bool:
    """Check if it's currently daytime based on sunrise/sunset times"""
    try:
        if not sunrise_str or not sunset_str:
            # Fallback: assume daytime between 6 AM and 6 PM
            current_hour = datetime.datetime.now().hour
            return 6 <= current_hour < 18
        
        # Parse ISO time strings
        sunrise = datetime.datetime.fromisoformat(sunrise_str.replace('Z', '+00:00'))
        sunset = datetime.datetime.fromisoformat(sunset_str.replace('Z', '+00:00'))
        now = datetime.datetime.now(datetime.timezone.utc)
        
        return sunrise <= now <= sunset
        
    except Exception as e:
        current_hour = datetime.datetime.now().hour
        return 6 <= current_hour < 18


def get_fallback_data(error_msg: str = "No data available") -> Dict:
    """Return fallback data when API fails"""
    now = datetime.datetime.now()
    
    return {
        "city": "Unknown",
        "latitude": None,
        "longitude": None,
        "sunrise": None,
        "sunset": None,
        "solar_noon": None,
        "day_length": None,
        "sun_position": {"elevation": 45, "azimuth": 180, "hour_angle": 0, "declination": 0},
        "moon_phase": 0.25,
        "moon_phase_name": "Waxing Crescent",
        "moon_illumination": 50.0,
        "moon_position": {"elevation": 30, "azimuth": 90, "longitude": 0},
        "is_daytime": 6 <= now.hour < 18,
        "current_time": now.isoformat(),
        "error": error_msg
    }


def format_time_for_display(time_str: Optional[str]) -> str:
    """Format ISO time string for user-friendly display"""
    try:
        if not time_str:
            return "N/A"
        
        # Parse ISO time
        dt = datetime.datetime.fromisoformat(time_str.replace('Z', '+00:00'))
        
        # Convert to local time and format for display
        local_dt = dt.replace(tzinfo=datetime.timezone.utc).astimezone()
        return local_dt.strftime("%I:%M %p")
        
    except Exception as e:
        return "N/A"


def calculate_golden_hour(sunrise_str: Optional[str], sunset_str: Optional[str]) -> Dict:
    """Calculate golden hour times (photographer's best lighting)"""
    try:
        if not sunrise_str or not sunset_str:
            return {"morning_start": "N/A", "morning_end": "N/A", 
                   "evening_start": "N/A", "evening_end": "N/A"}
        
        sunrise = datetime.datetime.fromisoformat(sunrise_str.replace('Z', '+00:00'))
        sunset = datetime.datetime.fromisoformat(sunset_str.replace('Z', '+00:00'))
        
        # Golden hour is approximately 1 hour after sunrise and 1 hour before sunset
        morning_end = sunrise + datetime.timedelta(hours=1)
        evening_start = sunset - datetime.timedelta(hours=1)
        
        return {
            "morning_start": format_time_for_display(sunrise.isoformat()),
            "morning_end": format_time_for_display(morning_end.isoformat()),
            "evening_start": format_time_for_display(evening_start.isoformat()),
            "evening_end": format_time_for_display(sunset.isoformat())
        }
        
    except Exception as e:
        return {"morning_start": "N/A", "morning_end": "N/A", 
               "evening_start": "N/A", "evening_end": "N/A"}


# Test function
if __name__ == "__main__":
    
    test_cities = ["New York", "London", "Tokyo"]
    
    for city in test_cities:
        data = fetch_sun_moon_data(city)
                    