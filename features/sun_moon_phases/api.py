"""
Sun and Moon Phases API Module
==============================

This module fetches astronomical data about the sun and moon for any city.
It's like having a personal astronomer that tells you when the sun rises,
when it sets, what phase the moon is in, and where celestial objects are in the sky!

Key features:
- Sunrise and sunset times for any city
- Current moon phase and illumination percentage
- Sun and moon positions in the sky (elevation and azimuth)
- Daytime/nighttime detection
- Golden hour calculations (best photography lighting)
- All calculations work worldwide with any city name

Data sources:
- Sunrise-Sunset API (free, no API key required)
- Mathematical calculations for moon phases
- Astronomical formulas for celestial positions

Think of this as your pocket planetarium that knows about the sky above any city!
"""

import requests  # For making HTTP requests to astronomy APIs
import math      # For astronomical calculations
import datetime  # For working with dates and times
from typing import Dict, Tuple, Optional  # For type hints to make code clearer


def get_coordinates_for_city(city: str) -> Tuple[Optional[float], Optional[float]]:
    """
    Get latitude and longitude coordinates for any city.
    
    This function acts like a GPS system to find where a city is located
    on Earth, which we need for astronomical calculations.
    
    Args:
        city (str): Name of the city (like "London", "Tokyo", "New York")
        
    Returns:
        tuple: (latitude, longitude) as numbers, or (None, None) if city not found
        
    Example:
        lat, lon = get_coordinates_for_city("Paris")
        # Returns: (48.8566, 2.3522) - Paris coordinates
    """
    # Validate input - make sure we have a valid city name
    if not isinstance(city, str) or not city.strip():
        return None, None
    
    try:
        # Use the free Open-Meteo geocoding API to find city coordinates
        url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json"
        response = requests.get(url, timeout=10)  # 10 second timeout
        
        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
            results = data.get("results", [])
            
            # Extract coordinates from the first (best) result
            if results:
                lat = results[0].get("latitude")
                lon = results[0].get("longitude")
                return lat, lon
        
        # If we get here, city wasn't found
        return None, None
        
    except Exception as e:
        # If anything goes wrong (network error, etc.), return None
        return None, None


def fetch_sun_moon_data(city: str) -> Dict:
    """
    Fetch comprehensive sun and moon data for a city.
    
    This is the main function that gets all astronomical information
    including sunrise/sunset times, moon phases, and celestial positions.
    
    Args:
        city (str): Name of the city to get data for
        
    Returns:
        dict: Complete astronomical data including:
            - sunrise/sunset times
            - sun position (elevation/azimuth)
            - moon phase and illumination
            - moon position
            - whether it's currently daytime
            - error information if something went wrong
            
    Example:
        data = fetch_sun_moon_data("London")
        print(f"Sunrise: {data['sunrise']}")
        print(f"Moon phase: {data['moon_phase_name']}")
        print(f"Currently daytime: {data['is_daytime']}")
    """
    # Step 1: Get city coordinates
    lat, lon = get_coordinates_for_city(city)
    
    # Step 2: If we couldn't find the city, return fallback data
    if not lat or not lon:
        return get_fallback_data()
    
    try:
        # Step 3: Get sunrise/sunset data from the free Sunrise-Sunset API
        url = f"https://api.sunrise-sunset.org/json?lat={lat}&lng={lon}&formatted=0"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            results = data.get("results", {})
            
            # Step 4: Calculate additional astronomical data
            sun_position = calculate_sun_position(lat, lon)
            moon_phase = calculate_moon_phase()
            moon_position = calculate_moon_position(lat, lon)
            is_day = is_currently_daytime(results.get("sunrise"), results.get("sunset"))
            
            # Step 5: Return comprehensive astronomical data
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
        
        # If API request failed, return fallback data
        return get_fallback_data(f"API returned status {response.status_code}")
        
    except Exception as e:
        # If anything goes wrong, return fallback data with error message
        return get_fallback_data(str(e))


def calculate_sun_position(lat: float, lon: float) -> Dict:
    """
    Calculate the current position of the sun in the sky.
    
    This uses astronomical formulas to determine where the sun appears
    from a specific location on Earth right now.
    
    Args:
        lat (float): Latitude of the location
        lon (float): Longitude of the location
        
    Returns:
        dict: Sun position data including:
            - elevation: How high the sun is (0° = horizon, 90° = directly overhead)
            - azimuth: Direction of the sun (0° = North, 90° = East, 180° = South, 270° = West)
            - hour_angle: Technical angle used in calculations
            - declination: Sun's seasonal position
            
    Example:
        position = calculate_sun_position(40.7128, -74.0060)  # New York
        print(f"Sun elevation: {position['elevation']}°")
        print(f"Sun direction: {position['azimuth']}°")
    """
    try:
        # Get current UTC time for calculations
        now = datetime.datetime.utcnow()
        
        # Calculate day of year (1-365)
        day_of_year = now.timetuple().tm_yday
        
        # Calculate solar declination angle (how far north/south the sun appears)
        # This changes throughout the year due to Earth's axial tilt
        declination = 23.45 * math.sin(math.radians(360 * (284 + day_of_year) / 365))
        
        # Calculate time correction for longitude
        # Each degree of longitude = 4 minutes of time difference
        time_correction = lon / 15
        
        # Calculate solar hour angle (how far the sun has moved from noon)
        hour_angle = 15 * (now.hour + now.minute/60 + time_correction - 12)
        
        # Convert angles to radians for trigonometric calculations
        lat_rad = math.radians(lat)
        dec_rad = math.radians(declination)
        hour_rad = math.radians(hour_angle)
        
        # Calculate solar elevation angle (height above horizon)
        elevation = math.degrees(math.asin(
            math.sin(lat_rad) * math.sin(dec_rad) + 
            math.cos(lat_rad) * math.cos(dec_rad) * math.cos(hour_rad)
        ))
        
        # Calculate solar azimuth angle (compass direction)
        azimuth = math.degrees(math.atan2(
            math.sin(hour_rad),
            math.cos(hour_rad) * math.sin(lat_rad) - math.tan(dec_rad) * math.cos(lat_rad)
        ))
        
        # Normalize azimuth to 0-360 degrees
        if azimuth < 0:
            azimuth += 360
        
        return {
            "elevation": round(max(elevation, -90), 2),  # Clamp to realistic values
            "azimuth": round(azimuth, 2),
            "hour_angle": round(hour_angle, 2),
            "declination": round(declination, 2)
        }
        
    except Exception as e:
        # If calculation fails, return reasonable default values
        return {"elevation": 45, "azimuth": 180, "hour_angle": 0, "declination": 0}


def calculate_moon_phase() -> float:
    """
    Calculate the current phase of the moon.
    
    This determines where the moon is in its monthly cycle from new moon
    to full moon and back. The calculation is based on the known lunar cycle.
    
    Returns:
        float: Moon phase value from 0 to 1, where:
               0.0 = New Moon (completely dark)
               0.25 = First Quarter (half illuminated, waxing)
               0.5 = Full Moon (completely illuminated)
               0.75 = Last Quarter (half illuminated, waning)
               1.0 = Back to New Moon
               
    Example:
        phase = calculate_moon_phase()
        if phase < 0.1:
            print("It's a new moon!")
        elif 0.4 < phase < 0.6:
            print("It's nearly a full moon!")
    """
    try:
        # Use a known new moon date as reference point
        # January 6, 2000 at 18:14 UTC was a new moon
        known_new_moon = datetime.datetime(2000, 1, 6, 18, 14)
        now = datetime.datetime.utcnow()
        
        # The moon's cycle length (synodic period)
        cycle_length = 29.53058867  # Days from new moon to new moon
        
        # Calculate how many days have passed since our reference new moon
        days_since = (now - known_new_moon).total_seconds() / (24 * 3600)
        
        # Calculate current phase (0-1) within the current cycle
        phase = (days_since % cycle_length) / cycle_length
        
        return round(phase, 4)
        
    except Exception as e:
        # If calculation fails, return a reasonable default (waxing crescent)
        return 0.25


def calculate_moon_position(lat: float, lon: float) -> Dict:
    """
    Calculate the approximate position of the moon in the sky.
    
    This provides a simplified calculation of where the moon appears
    from a specific location. Note: Real moon position calculations
    are extremely complex, so this is an approximation.
    
    Args:
        lat (float): Latitude of the location
        lon (float): Longitude of the location
        
    Returns:
        dict: Moon position data including:
            - elevation: How high the moon is above horizon
            - azimuth: Compass direction to the moon
            - longitude: Moon's celestial longitude
            
    Note:
        This is a simplified calculation. Professional astronomy software
        uses much more complex algorithms with thousands of terms.
    """
    try:
        now = datetime.datetime.utcnow()
        
        # Calculate days since J2000.0 epoch (January 1, 2000, 12:00 UTC)
        # This is a standard reference point used in astronomy
        j2000 = datetime.datetime(2000, 1, 1, 12, 0)
        days_since_j2000 = (now - j2000).total_seconds() / (24 * 3600)
        
        # Simplified lunar orbital calculations
        # Real calculations involve hundreds of periodic terms
        
        # Moon's mean longitude (degrees) - where moon would be in a circular orbit
        moon_longitude = (218.316 + 13.176396 * days_since_j2000) % 360
        
        # Moon's mean anomaly (degrees) - position in elliptical orbit
        moon_anomaly = (134.963 + 13.064993 * days_since_j2000) % 360
        
        # Very simplified moon elevation calculation
        # This is just an approximation for demonstration purposes
        moon_elevation = 30 * math.sin(math.radians(moon_longitude)) + lat/4
        
        # Simplified moon azimuth calculation
        moon_azimuth = (moon_longitude + 180) % 360
        
        return {
            "elevation": round(max(min(moon_elevation, 90), -90), 2),  # Clamp to valid range
            "azimuth": round(moon_azimuth, 2),
            "longitude": round(moon_longitude, 2)
        }
        
    except Exception as e:
        # If calculation fails, return reasonable default values
        return {"elevation": 30, "azimuth": 90, "longitude": 0}


def get_moon_phase_name(phase: float) -> str:
    """
    Convert a numerical moon phase to a descriptive name.
    
    This translates the 0-1 moon phase value into human-readable
    names that people are familiar with.
    
    Args:
        phase (float): Moon phase value from 0 to 1
        
    Returns:
        str: Descriptive moon phase name
        
    Example:
        name = get_moon_phase_name(0.5)
        # Returns: "Full Moon"
        
        name = get_moon_phase_name(0.25)
        # Returns: "First Quarter"
    """
    # Define phase ranges and their corresponding names
    if phase < 0.0625 or phase >= 0.9375:
        return "New Moon"          # Completely dark
    elif 0.0625 <= phase < 0.1875:
        return "Waxing Crescent"   # Thin crescent, growing
    elif 0.1875 <= phase < 0.3125:
        return "First Quarter"     # Half illuminated, right side
    elif 0.3125 <= phase < 0.4375:
        return "Waxing Gibbous"    # More than half, growing
    elif 0.4375 <= phase < 0.5625:
        return "Full Moon"         # Completely illuminated
    elif 0.5625 <= phase < 0.6875:
        return "Waning Gibbous"    # More than half, shrinking
    elif 0.6875 <= phase < 0.8125:
        return "Last Quarter"      # Half illuminated, left side
    else:
        return "Waning Crescent"   # Thin crescent, shrinking


def get_moon_phase_emoji(phase: float) -> str:
    """
    Get an emoji representation of the current moon phase.
    
    This provides a visual representation using moon emojis that
    can be displayed in the user interface.
    
    Args:
        phase (float): Moon phase value from 0 to 1
        
    Returns:
        str: Moon emoji corresponding to the phase
        
    Example:
        emoji = get_moon_phase_emoji(0.5)
        # Returns: "🌕" (full moon emoji)
    """
    # Map phase ranges to appropriate moon emojis
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
    """
    Calculate what percentage of the moon is illuminated.
    
    This converts the phase value into a percentage that tells
    you how much of the moon is visible (bright).
    
    Args:
        phase (float): Moon phase value from 0 to 1
        
    Returns:
        float: Illumination percentage from 0 to 100
        
    Example:
        illumination = calculate_moon_illumination(0.5)
        # Returns: 100.0 (full moon is 100% illuminated)
        
        illumination = calculate_moon_illumination(0.0)
        # Returns: 0.0 (new moon is 0% illuminated)
    """
    try:
        # Calculate illumination based on phase
        # The moon's illumination follows a specific pattern:
        # - From new moon (0) to full moon (0.5): illumination increases 0% to 100%
        # - From full moon (0.5) to new moon (1): illumination decreases 100% to 0%
        
        if phase <= 0.5:
            # Waxing phases: illumination increases
            illumination = phase * 2  # 0 to 1 (0% to 100%)
        else:
            # Waning phases: illumination decreases
            illumination = 2 - (phase * 2)  # 1 to 0 (100% to 0%)
        
        # Convert to percentage and round
        return round(illumination * 100, 1)
    except Exception:
        # If calculation fails, return reasonable default
        return 50.0


def is_currently_daytime(sunrise_str: Optional[str], sunset_str: Optional[str]) -> bool:
    """
    Determine if it's currently daytime based on sunrise/sunset times.
    
    This compares the current time with sunrise and sunset to determine
    whether the sun is above or below the horizon.
    
    Args:
        sunrise_str (str): Sunrise time in ISO format
        sunset_str (str): Sunset time in ISO format
        
    Returns:
        bool: True if it's currently daytime, False if nighttime
        
    Example:
        is_day = is_currently_daytime("2024-01-15T07:30:00Z", "2024-01-15T17:45:00Z")
        # Returns True if current time is between 7:30 AM and 5:45 PM
    """
    try:
        # If we don't have sunrise/sunset data, use simple time-based guess
        if not sunrise_str or not sunset_str:
            current_hour = datetime.datetime.now().hour
            return 6 <= current_hour < 18  # Assume daylight 6 AM to 6 PM
        
        # Parse the ISO time strings (handle timezone indicator)
        sunrise = datetime.datetime.fromisoformat(sunrise_str.replace('Z', '+00:00'))
        sunset = datetime.datetime.fromisoformat(sunset_str.replace('Z', '+00:00'))
        now = datetime.datetime.now(datetime.timezone.utc)
        
        # Check if current time is between sunrise and sunset
        return sunrise <= now <= sunset
        
    except Exception as e:
        # If time parsing fails, use simple hour-based fallback
        current_hour = datetime.datetime.now().hour
        return 6 <= current_hour < 18


def get_fallback_data(error_msg: str = "No data available") -> Dict:
    """
    Return reasonable fallback data when API calls fail.
    
    This ensures the app continues working even when we can't get
    real astronomical data from the internet.
    
    Args:
        error_msg (str): Description of what went wrong
        
    Returns:
        dict: Safe fallback astronomical data
    """
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
        "moon_phase": 0.25,                    # Default to waxing crescent
        "moon_phase_name": "Waxing Crescent",
        "moon_illumination": 50.0,
        "moon_position": {"elevation": 30, "azimuth": 90, "longitude": 0},
        "is_daytime": 6 <= now.hour < 18,      # Simple daytime guess
        "current_time": now.isoformat(),
        "error": error_msg
    }


def format_time_for_display(time_str: Optional[str]) -> str:
    """
    Format ISO time string for user-friendly display.
    
    This converts technical time formats into times that
    are easy for users to read and understand.
    
    Args:
        time_str (str): ISO time string from API
        
    Returns:
        str: User-friendly time string
        
    Example:
        formatted = format_time_for_display("2024-01-15T07:30:00Z")
        # Returns: "7:30 AM"
    """
    try:
        if not time_str:
            return "N/A"
        
        # Parse the ISO time string
        dt = datetime.datetime.fromisoformat(time_str.replace('Z', '+00:00'))
        
        # Convert to local time and format for display
        local_dt = dt.replace(tzinfo=datetime.timezone.utc).astimezone()
        return local_dt.strftime("%I:%M %p")  # Format: "7:30 AM"
        
    except Exception as e:
        return "N/A"


def calculate_golden_hour(sunrise_str: Optional[str], sunset_str: Optional[str]) -> Dict:
    """
    Calculate golden hour times for photography.
    
    Golden hour is the period shortly after sunrise and before sunset
    when the sun is low and provides beautiful, warm lighting for photography.
    
    Args:
        sunrise_str (str): Sunrise time in ISO format
        sunset_str (str): Sunset time in ISO format
        
    Returns:
        dict: Golden hour timing information
        
    Example:
        golden = calculate_golden_hour(sunrise, sunset)
        print(f"Morning golden hour: {golden['morning_start']} - {golden['morning_end']}")
        print(f"Evening golden hour: {golden['evening_start']} - {golden['evening_end']}")
    """
    try:
        if not sunrise_str or not sunset_str:
            return {"morning_start": "N/A", "morning_end": "N/A", 
                   "evening_start": "N/A", "evening_end": "N/A"}
        
        # Parse sunrise and sunset times
        sunrise = datetime.datetime.fromisoformat(sunrise_str.replace('Z', '+00:00'))
        sunset = datetime.datetime.fromisoformat(sunset_str.replace('Z', '+00:00'))
        
        # Calculate golden hour periods
        # Morning golden hour: from sunrise to 1 hour after sunrise
        morning_end = sunrise + datetime.timedelta(hours=1)
        
        # Evening golden hour: from 1 hour before sunset to sunset
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


def get_astronomical_season(date: datetime.date = None) -> str:
    """
    Determine the current astronomical season.
    
    This calculates which season it is based on the sun's position,
    which is more accurate than calendar seasons.
    
    Args:
        date (datetime.date): Date to check (default: today)
        
    Returns:
        str: Season name ("Spring", "Summer", "Fall", "Winter")
        
    Example:
        season = get_astronomical_season()
        print(f"Current season: {season}")
    """
    if date is None:
        date = datetime.date.today()
    
    # Get day of year (1-365)
    day_of_year = date.timetuple().tm_yday
    
    # Approximate astronomical season boundaries
    # These vary slightly each year, but these are close averages
    if 80 <= day_of_year < 172:    # Around March 21 to June 21
        return "Spring"
    elif 172 <= day_of_year < 266:  # Around June 21 to September 23
        return "Summer"
    elif 266 <= day_of_year < 355:  # Around September 23 to December 21
        return "Fall"
    else:                           # Around December 21 to March 21
        return "Winter"


def get_daylight_info(sunrise_str: Optional[str], sunset_str: Optional[str]) -> Dict:
    """
    Calculate detailed daylight information.
    
    This provides comprehensive information about daylight duration,
    solar timing, and day/night characteristics.
    
    Args:
        sunrise_str (str): Sunrise time in ISO format
        sunset_str (str): Sunset time in ISO format
        
    Returns:
        dict: Detailed daylight information
    """
    try:
        if not sunrise_str or not sunset_str:
            return {"error": "Missing sunrise/sunset data"}
        
        # Parse times
        sunrise = datetime.datetime.fromisoformat(sunrise_str.replace('Z', '+00:00'))
        sunset = datetime.datetime.fromisoformat(sunset_str.replace('Z', '+00:00'))
        
        # Calculate daylight duration
        daylight_duration = sunset - sunrise
        daylight_hours = daylight_duration.total_seconds() / 3600
        
        # Calculate solar noon (midpoint between sunrise and sunset)
        solar_noon = sunrise + (daylight_duration / 2)
        
        # Current time info
        now = datetime.datetime.now(datetime.timezone.utc)
        is_day = sunrise <= now <= sunset
        
        # Time until next sunrise/sunset
        if is_day:
            time_until_sunset = sunset - now
            next_event = "sunset"
            time_until_event = time_until_sunset.total_seconds() / 3600
        else:
            # Calculate next sunrise (might be tomorrow)
            if now < sunrise:
                time_until_sunrise = sunrise - now
            else:
                # Tomorrow's sunrise (approximate)
                tomorrow_sunrise = sunrise + datetime.timedelta(days=1)
                time_until_sunrise = tomorrow_sunrise - now
            
            next_event = "sunrise"
            time_until_event = time_until_sunrise.total_seconds() / 3600
        
        return {
            "daylight_hours": round(daylight_hours, 2),
            "solar_noon": format_time_for_display(solar_noon.isoformat()),
            "is_daytime": is_day,
            "next_event": next_event,
            "hours_until_next_event": round(time_until_event, 1),
            "season": get_astronomical_season(),
            "error": None
        }
        
    except Exception as e:
        return {"error": str(e)}


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TESTING AND EXAMPLE USAGE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

if __name__ == "__main__":
    """
    This section runs when you execute this file directly.
    It's useful for testing the sun and moon calculation functions.
    """
    
    print("Testing Sun and Moon Phases API")
    print("=" * 35)
    
    # Test cities from different time zones
    test_cities = ["London", "New York", "Tokyo", "Sydney", "Cairo"]
    
    print("\n🌍 Testing astronomical data for multiple cities:")
    
    for city in test_cities:
        print(f"\n📍 Testing {city}:")
        
        # Test main sun/moon data function
        data = fetch_sun_moon_data(city)
        
        if not data.get("error"):
            print(f"  🌅 Sunrise: {format_time_for_display(data.get('sunrise'))}")
            print(f"  🌇 Sunset: {format_time_for_display(data.get('sunset'))}")
            print(f"  🌙 Moon phase: {data.get('moon_phase_name')} ({data.get('moon_illumination')}% lit)")
            print(f"  ☀️ Sun elevation: {data.get('sun_position', {}).get('elevation', 'N/A')}°")
            print(f"  🌞 Currently: {'Daytime' if data.get('is_daytime') else 'Nighttime'}")
            
            # Test golden hour calculation
            golden = calculate_golden_hour(data.get('sunrise'), data.get('sunset'))
            if golden.get('morning_start') != 'N/A':
                print(f"  📸 Golden hours: {golden['morning_start']}-{golden['morning_end']}, {golden['evening_start']}-{golden['evening_end']}")
            
        else:
            print(f"  ❌ Error: {data.get('error')}")
    
    # Test individual calculation functions
    print(f"\n🔬 Testing individual calculations:")
    
    # Test moon phase calculation
    moon_phase = calculate_moon_phase()
    moon_name = get_moon_phase_name(moon_phase)
    moon_emoji = get_moon_phase_emoji(moon_phase)
    moon_illumination = calculate_moon_illumination(moon_phase)
    
    print(f"  🌙 Current moon phase: {moon_name} {moon_emoji}")
    print(f"  💡 Moon illumination: {moon_illumination}%")
    print(f"  📊 Phase value: {moon_phase}")
    
    # Test season calculation
    season = get_astronomical_season()
    print(f"  🍂 Current season: {season}")
    
    # Test coordinate lookup
    lat, lon = get_coordinates_for_city("Paris")
    if lat and lon:
        print(f"  📍 Paris coordinates: {lat:.4f}, {lon:.4f}")
    
    print(f"\n✅ Sun and moon API testing completed!")
    print(f"\nNote: This API provides real astronomical data")
    print(f"including sunrise/sunset times and moon phases for any city worldwide.")
    