import csv 
import os  
from datetime import datetime 

# ────────────────────────────────────────────────────────────────────────────── 
# WEATHER DATA STORAGE MODULE
# 
# This module handles saving weather data to CSV files for historical tracking.
# CSV (Comma Separated Values) is a simple format that can be opened in Excel.
# Each weather lookup gets saved as a new row with timestamp, city, temp, and description.
# ────────────────────────────────────────────────────────────────────────────── 

def save_weather(data, filepath="data/weather_history.csv"):
    """
    Save weather data to a CSV file for keeping history of all weather lookups.
    
    Args:
        data: Dictionary containing weather data from the API
        filepath: Path where to save the CSV file (default: data/weather_history.csv)
    
    The function will:
    1. Create the directory if it doesn't exist
    2. Create the CSV file with headers if it's new
    3. Add a new row with the current weather data
    """
    try:
        # --- CREATE DIRECTORY IF NEEDED ---
        # Extract the directory path from the full filepath
        # Example: "data/weather_history.csv" → "data"
        directory = os.path.dirname(filepath)
        
        # Create the directory if it doesn't exist
        # exist_ok=True means don't error if directory already exists
        if directory:  # Only create if directory path is not empty
            os.makedirs(directory, exist_ok=True)
        
        # --- CHECK IF FILE EXISTS ---
        # We need to know if the file exists to decide whether to write headers
        file_exists = os.path.isfile(filepath)
        
        # --- WRITE TO CSV FILE ---
        # Open file in append mode ("a") so we add to the end, not overwrite
        # newline="" prevents extra blank lines between rows on Windows
        with open(filepath, "a", newline="", encoding="utf-8") as csvfile:
            # Create a CSV writer object
            writer = csv.writer(csvfile)
            
            # --- WRITE HEADER ROW (only for new files) ---
            if not file_exists:
                # Write column headers as the first row
                writer.writerow(["timestamp", "city", "temperature", "description"])
            
            # --- EXTRACT DATA SAFELY ---
            # Use .get() method to safely extract data with fallbacks
            # This prevents crashes if the API response is missing expected fields
            
            # Get current timestamp in readable format
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Extract city name (fallback to 'Unknown' if missing)
            city = data.get('name', 'Unknown')
            
            # Extract temperature (nested inside 'main' dictionary)
            # Use nested .get() calls to safely navigate nested dictionaries
            temperature = data.get('main', {}).get('temp', 'N/A')
            
            # Extract weather description (nested inside 'weather' list)
            # weather is a list, so we get the first item [0], then get 'description'
            weather_list = data.get('weather', [{}])  # Get weather list or empty list
            if weather_list:  # Check if list is not empty
                description = weather_list[0].get('description', 'N/A')
            else:
                description = 'N/A'
            
            # --- WRITE DATA ROW ---
            writer.writerow([timestamp, city, temperature, description])
            
    except PermissionError:
        # Handle case where file is open in Excel or we don't have write permissions
        pass    
    
def load_weather_history(filepath="data/weather_history.csv"):
    """
    Load historical weather data from CSV file.
    
    """
    try:
        # Check if file exists before trying to open it
        if not os.path.isfile(filepath):
            return []
        
        weather_history = []
        
        # Open and read the CSV file
        with open(filepath, "r", newline="", encoding="utf-8") as csvfile:
            # Create a CSV reader that returns each row as a dictionary
            # This is easier to work with than plain lists
            reader = csv.DictReader(csvfile)
            
            # Read each row and add to our history list
            for row in reader:
                weather_history.append(row)
        
        return weather_history
        
    except Exception as e:
        return []
