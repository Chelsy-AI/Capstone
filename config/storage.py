"""
Weather Data Storage Module
===========================

This module handles saving and loading weather data to/from CSV files.
It stores every weather search so you can look back at historical data.

Key features:
- Save weather data automatically when you search for a city
- Load historical weather data for charts and analysis
- Track which cities you've searched for
- Get statistics about your weather data collection
- Clean and manage old data
"""

import csv
import os
from datetime import datetime


def save_weather(data, city_name=None, filepath="data/weather_history.csv"):
    """
    Save weather data to a CSV file.
    
    Every time you search for weather, this function saves that information
    to a CSV file so you can see historical patterns and trends.
    
    Args:
        data (dict): Weather information from the API
        city_name (str): Name of the city (optional, can extract from data)
        filepath (str): Where to save the CSV file
    """
    try:
        # Step 1: Make sure the folder exists to save the file
        directory = os.path.dirname(filepath)
        if directory:
            # Create the directory if it doesn't exist (like creating a new folder)
            os.makedirs(directory, exist_ok=True)
        
        # Step 2: Check if the CSV file already exists
        file_exists = os.path.isfile(filepath)
        
        # Step 3: Open the CSV file for writing (append mode adds to the end)
        with open(filepath, "a", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            
            # Step 4: If this is a new file, write the column headers first
            if not file_exists:
                writer.writerow([
                    "timestamp", "city", "temperature", "description", 
                    "humidity", "wind_speed", "pressure", "visibility",
                    "uv_index", "precipitation"
                ])
            
            # Step 5: Extract and prepare the data to save
            
            # Create a timestamp for when this data was saved
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Get the city name - try multiple sources
            city = city_name or data.get('name') or data.get('city') or 'Unknown'
            
            # Extract weather measurements, using safe defaults if data is missing
            temperature = data.get('temperature', 'N/A')
            description = data.get('description', 'N/A')
            humidity = data.get('humidity', 'N/A')
            wind_speed = data.get('wind_speed', 'N/A')
            pressure = data.get('pressure', 'N/A')
            visibility = data.get('visibility', 'N/A')
            uv_index = data.get('uv_index', 'N/A')
            precipitation = data.get('precipitation', 'N/A')
            
            # Step 6: Write the data row to the CSV file
            writer.writerow([
                timestamp, city, temperature, description,
                humidity, wind_speed, pressure, visibility,
                uv_index, precipitation
            ])
                        
    except Exception as e:
        # If something goes wrong, just continue - saving weather data
        pass


def load_weather_history(filepath="data/weather_history.csv"):
    """
    Load historical weather data from the CSV file.
    
    This reads all the weather searches you've done in the past
    and returns them as a list of dictionaries.
    
    Args:
        filepath (str): Path to the CSV file to read
        
    Returns:
        list: List of weather records, each as a dictionary
    """
    try:
        # Check if the file exists
        if not os.path.isfile(filepath):
            return []  # Return empty list if no history file exists yet
        
        weather_history = []
        
        # Open and read the CSV file
        with open(filepath, "r", newline="", encoding="utf-8") as csvfile:
            # Create a CSV reader that converts each row to a dictionary
            reader = csv.DictReader(csvfile)
            
            # Read each row and add it to our history list
            for row in reader:
                weather_history.append(row)
        
        return weather_history
        
    except Exception as e:
        # If reading fails, return empty list so the app can continue
        return []


def get_recent_weather(city, limit=10, filepath="data/weather_history.csv"):
    """
    Get recent weather records for a specific city.
    
    This is useful for showing a city's weather history.
    
    Args:
        city (str): Name of the city to get history for
        limit (int): Maximum number of records to return
        filepath (str): Path to the CSV file
        
    Returns:
        list: Most recent weather records for the city
    """
    try:
        # Load all weather records
        all_records = load_weather_history(filepath)
        
        # Filter records to only include the specified city
        # Use case-insensitive comparison so "london" matches "London"
        city_records = [
            record for record in all_records 
            if record.get('city', '').lower() == city.lower()
        ]
        
        # Sort by timestamp with most recent first
        city_records.sort(
            key=lambda x: x.get('timestamp', ''), 
            reverse=True  # reverse=True puts newest first
        )
        
        # Return only the requested number of records
        return city_records[:limit]
        
    except Exception as e:
        # If something goes wrong, return empty list
        return []


def get_searched_cities(filepath="data/weather_history.csv"):
    """
    Get a list of all unique cities that have been searched.
    
    This is useful for showing the user which cities they've looked up before.
    
    Returns:
        list: Sorted list of unique city names
    """
    try:
        # Load all weather records
        all_records = load_weather_history(filepath)
        
        # Extract unique city names
        cities = set()
        for record in all_records:
            city = record.get('city', '').strip()
            # Only add non-empty cities that aren't "Unknown"
            if city and city != 'Unknown':
                cities.add(city)
        
        # Convert to sorted list for consistent ordering
        return sorted(list(cities))
        
    except Exception as e:
        # If something goes wrong, return empty list
        return []


def clear_weather_history(filepath="data/weather_history.csv"):
    """
    Clear all weather history data.
    
    This deletes the entire weather history file.
    
    Args:
        filepath (str): Path to the CSV file to clear
        
    Returns:
        bool: True if successful, False if there was an error
    """
    try:
        # Check if the file exists before trying to delete it
        if os.path.isfile(filepath):
            os.remove(filepath)  # Delete the file
            return True
        else:
            # If file doesn't exist, consider it "successfully cleared"
            return True
            
    except Exception as e:
        # If deletion fails, return False
        return False


def get_weather_stats(filepath="data/weather_history.csv"):
    """
    Get statistics about stored weather data.
    
    This analyzes your weather history and returns statistics
    
    Returns:
        dict: Dictionary containing various statistics
    """
    try:
        # Load all weather records
        records = load_weather_history(filepath)
        
        # If no records exist, return basic info
        if not records:
            return {"total_records": 0, "cities": [], "date_range": None}
        
        # Count unique cities
        cities = list(set(record.get('city', 'Unknown') for record in records))
        
        # Calculate date range (earliest to latest record)
        timestamps = [record.get('timestamp', '') for record in records if record.get('timestamp')]
        timestamps.sort()
        
        date_range = None
        if timestamps:
            date_range = {
                "earliest": timestamps[0],
                "latest": timestamps[-1]
            }
        
        # Calculate temperature statistics
        temps = []
        for record in records:
            try:
                # Try to convert temperature to a number
                temp = float(record.get('temperature', 0))
                temps.append(temp)
            except (ValueError, TypeError):
                # Skip invalid temperature values
                pass
        
        # Calculate temperature stats if we have valid temperatures
        temp_stats = {}
        if temps:
            temp_stats = {
                "min": min(temps),           # Coldest temperature recorded
                "max": max(temps),           # Hottest temperature recorded
                "avg": round(sum(temps) / len(temps), 1)  # Average temperature
            }
        
        # Compile all statistics
        stats = {
            "total_records": len(records),
            "unique_cities": len(cities),
            "cities": cities,
            "date_range": date_range,
            "temperature_stats": temp_stats
        }
        
        return stats
        
    except Exception as e:
        # If analysis fails, return error information
        return {"error": str(e)}
