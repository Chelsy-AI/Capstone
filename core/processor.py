import requests
from PIL import Image, ImageTk
import io
from datetime import datetime

def display_weather(data, temp_label, desc_label, update_label, icon_label, app):
    """
    Update the GUI weather display widgets with the latest weather data.
    
    Args:
        data: Dictionary containing weather data from OpenWeatherMap API
        temp_label: GUI label widget to show temperature
        desc_label: GUI label widget to show weather description
        update_label: GUI label widget to show last update time
        icon_label: GUI label widget to show weather icon
        app: Main application object that stores settings and images
    """
    try:
        # --- TEMPERATURE PROCESSING ---
        # Get temperature in Celsius from the API data
        temp_c = data["main"]["temp"]
        
        # Convert Celsius to Fahrenheit using the formula: (C × 9/5) + 32
        temp_f = temp_c * 9 / 5 + 32
        
        # Format temperature string based on user's preferred unit
        # Check what unit the user wants (stored in app.unit)
        if app.unit == "C":
            temp = f"{round(temp_c)} °C"  # Round to nearest whole number
        else:
            temp = f"{round(temp_f)} °F"
        
        # Update the temperature label on the GUI
        temp_label.configure(text=temp)
        
        # --- WEATHER DESCRIPTION ---
        # Get the first weather condition from the list
        weather = data["weather"][0]  # weather is a list, we want the first item
        
        # Get description and capitalize first letter (e.g., "partly cloudy" → "Partly cloudy")
        description = weather["description"].capitalize()
        
        # Update the description label on the GUI
        desc_label.configure(text=description)
        
        # --- UPDATE TIME ---
        # Convert Unix timestamp to readable date/time format
        # dt is the timestamp when this weather data was last updated
        update_time = datetime.utcfromtimestamp(data["dt"]).strftime("%Y-%m-%d %H:%M UTC")
        
        # Update the time label on the GUI
        update_label.configure(text=f"Updated at: {update_time}")
        
        # --- WEATHER ICON ---
        # Get the icon code (like "01d" for clear day, "02n" for few clouds night)
        icon_code = weather["icon"]
        
        # Build the URL to download the weather icon from OpenWeatherMap
        # @2x means we get a higher resolution version
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
        
        # Download the icon image from the internet
        # IMPROVEMENT: Add timeout to prevent hanging if internet is slow
        response = requests.get(icon_url, timeout=10)
        
        # Check if the download was successful
        if response.status_code == 200:
            # Convert the downloaded bytes into a PIL Image
            # io.BytesIO treats the bytes like a file
            image = Image.open(io.BytesIO(response.content)).convert("RGBA")
            
            # Store the original image in the app (useful for resizing later)
            app.original_icon = image
            
            # Convert PIL Image to Tkinter PhotoImage so it can be displayed
            app.icon_image = ImageTk.PhotoImage(image)
            
            # Update the icon label with the new image
            icon_label.configure(image=app.icon_image)
            # Keep a reference to prevent garbage collection (important for Tkinter!)
            icon_label.image = app.icon_image
        else:
            pass
            
    except KeyError as e:
        # Handle missing data in the API response
        _set_error_display(temp_label, desc_label, update_label)
        
    except requests.RequestException as e:
        # Handle network errors (no internet, timeout, etc.)
        _set_error_display(temp_label, desc_label, update_label)
        
    except Exception as e:
        # Handle any other unexpected errors
        _set_error_display(temp_label, desc_label, update_label)

def _set_error_display(temp_label, desc_label, update_label):
    """
    Helper function to set error messages when something goes wrong.
    The underscore at the start means this is a "private" function - 
    only meant to be used within this file.

    """
    temp_label.configure(text="N/A")
    desc_label.configure(text="No description")
    update_label.configure(text="Updated at: Unknown")

def extract_weather_details(data):
    """
    Extracts detailed weather information from weather data dictionary.
    
    This function seems to expect data from a Open-Mete weather API.
            
    """
    # Get current weather conditions (or empty dict if not found)
    current = data.get("current", {})
    
    # Get daily weather forecast (or empty dict if not found)
    daily = data.get("daily", {})
    
    # Extract specific weather metrics, with fallback to "N/A" if not found
    weather_details = {
        "humidity": current.get("relative_humidity_2m", "N/A"),  # Humidity percentage
        "wind": current.get("wind_speed_10m", "N/A"),           # Wind speed
        "pressure": current.get("surface_pressure", "N/A"),     # Atmospheric pressure
        "visibility": current.get("visibility", "N/A"),         # How far you can see
        "uv": daily.get("uv_index_max", ["N/A"])[0],           # UV index (sun strength)
        "precipitation": daily.get("precipitation_sum", ["N/A"])[0],  # Rain/snow amount
    }
    
    return weather_details
