#!/usr/bin/env python3
"""
Fixed Weather Data Storage Module
Ensures all weather data is properly saved to CSV files
"""

import csv 
import os  
from datetime import datetime 

def save_weather(data, filepath="data/weather_history.csv"):
    """
    Save weather data to CSV file with proper error handling and data extraction.
    
    Args:
        data: Dictionary containing weather data from the API
        filepath: Path where to save the CSV file
    """
    try:
        # Create directory if it doesn't exist
        directory = os.path.dirname(filepath)
        if directory:
            os.makedirs(directory, exist_ok=True)
        
        # Check if file exists
        file_exists = os.path.isfile(filepath)
        
        # Open file in append mode
        with open(filepath, "a", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            
            # Write header if new file
            if not file_exists:
                writer.writerow([
                    "timestamp", "city", "temperature", "description", 
                    "humidity", "wind_speed", "pressure", "visibility",
                    "uv_index", "precipitation"
                ])
            
            # Extract data safely
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Extract basic weather info
            city = data.get('name', 'Unknown')
            temperature = data.get('temperature', 'N/A')
            description = data.get('description', 'N/A')
            
            # Extract additional metrics
            humidity = data.get('humidity', 'N/A')
            wind_speed = data.get('wind_speed', 'N/A')
            pressure = data.get('pressure', 'N/A')
            visibility = data.get('visibility', 'N/A')
            uv_index = data.get('uv_index', 'N/A')
            precipitation = data.get('precipitation', 'N/A')
            
            # Write data row
            writer.writerow([
                timestamp, city, temperature, description,
                humidity, wind_speed, pressure, visibility,
                uv_index, precipitation
            ])
            
            print(f"✅ Weather data saved: {city} at {timestamp}")
            
    except PermissionError:
        print("⚠️ Permission denied - file might be open in Excel")
    except Exception as e:
        print(f"❌ Error saving weather data: {e}")


def load_weather_history(filepath="data/weather_history.csv"):
    """
    Load historical weather data from CSV file.
    
    Returns:
        List of dictionaries containing weather records
    """
    try:
        if not os.path.isfile(filepath):
            return []
        
        weather_history = []
        
        with open(filepath, "r", newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            
            for row in reader:
                weather_history.append(row)
        
        print(f"✅ Loaded {len(weather_history)} weather records")
        return weather_history
        
    except Exception as e:
        print(f"❌ Error loading weather history: {e}")
        return []


def get_recent_weather(city, limit=10, filepath="data/weather_history.csv"):
    """
    Get recent weather records for a specific city.
    
    Args:
        city: City name to filter by
        limit: Maximum number of records to return
        filepath: Path to CSV file
        
    Returns:
        List of recent weather records for the city
    """
    try:
        all_records = load_weather_history(filepath)
        
        # Filter by city (case insensitive)
        city_records = [
            record for record in all_records 
            if record.get('city', '').lower() == city.lower()
        ]
        
        # Sort by timestamp (most recent first)
        city_records.sort(
            key=lambda x: x.get('timestamp', ''), 
            reverse=True
        )
        
        # Return limited results
        return city_records[:limit]
        
    except Exception as e:
        print(f"❌ Error getting recent weather: {e}")
        return []


def clear_weather_history(filepath="data/weather_history.csv"):
    """
    Clear all weather history data.
    
    Args:
        filepath: Path to CSV file to clear
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        if os.path.isfile(filepath):
            os.remove(filepath)
            print(f"✅ Weather history cleared: {filepath}")
            return True
        else:
            print(f"⚠️ No history file found: {filepath}")
            return True
            
    except Exception as e:
        print(f"❌ Error clearing weather history: {e}")
        return False


def get_weather_stats(filepath="data/weather_history.csv"):
    """
    Get statistics about stored weather data.
    
    Returns:
        Dictionary with statistics
    """
    try:
        records = load_weather_history(filepath)
        
        if not records:
            return {"total_records": 0, "cities": [], "date_range": None}
        
        # Count unique cities
        cities = list(set(record.get('city', 'Unknown') for record in records))
        
        # Get date range
        timestamps = [record.get('timestamp', '') for record in records if record.get('timestamp')]
        timestamps.sort()
        
        date_range = None
        if timestamps:
            date_range = {
                "earliest": timestamps[0],
                "latest": timestamps[-1]
            }
        
        # Temperature statistics
        temps = []
        for record in records:
            try:
                temp = float(record.get('temperature', 0))
                temps.append(temp)
            except (ValueError, TypeError):
                pass
        
        temp_stats = {}
        if temps:
            temp_stats = {
                "min": min(temps),
                "max": max(temps),
                "avg": round(sum(temps) / len(temps), 1)
            }
        
        stats = {
            "total_records": len(records),
            "unique_cities": len(cities),
            "cities": cities,
            "date_range": date_range,
            "temperature_stats": temp_stats
        }
        
        return stats
        
    except Exception as e:
        print(f"❌ Error getting weather stats: {e}")
        return {"error": str(e)}


# Example usage and testing
if __name__ == "__main__":
    # Test the storage functions
    print("🧪 Testing weather storage functions...")
    
    # Test data
    test_weather_data = {
        "name": "Test City",
        "temperature": 22.5,
        "description": "Clear sky",
        "humidity": 60,
        "wind_speed": 5.2,
        "pressure": 1013,
        "visibility": 10000,
        "uv_index": 6,
        "precipitation": 0.0
    }
    
    # Test saving
    print("Testing save_weather...")
    save_weather(test_weather_data, "test_weather.csv")
    
    # Test loading
    print("Testing load_weather_history...")
    history = load_weather_history("test_weather.csv")
    print(f"Loaded {len(history)} records")
    
    # Test stats
    print("Testing get_weather_stats...")
    stats = get_weather_stats("test_weather.csv")
    print(f"Stats: {stats}")
    
    # Clean up test file
    try:
        os.remove("test_weather.csv")
        print("✅ Test file cleaned up")
    except:
        pass
    
    print("🧪 Storage tests completed")
    