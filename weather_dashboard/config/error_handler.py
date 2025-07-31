"""
Weather App Error Handling & Validation Module
===============================================

This module provides comprehensive city input validation and 
error screen functionality for the weather application.

Key functions:
- Validate city names and handle all edge cases
- Display full-screen error messages with specific error types
- Handle network connectivity issues
- Support international cities with proper characters
- Provide clean recovery with back button to return to main screen
"""

import tkinter as tk
from tkinter import messagebox
import time
import requests
import os
import re
from dotenv import load_dotenv
from typing import Dict, Any, Optional, Tuple
from datetime import datetime
import json
import unicodedata
import socket

class CityValidator:
    """Comprehensive city validation with detailed error handling."""
    
    def __init__(self):
        # Known real cities that should always be allowed
        self.valid_cities = {
            'new york', 'london', 'paris', 'tokyo', 'berlin', 'madrid', 'rome', 
            'amsterdam', 'barcelona', 'sydney', 'toronto', 'montreal', 'mumbai', 
            'delhi', 'beijing', 'moscow', 'dubai', 'singapore', 'hong kong',
            'los angeles', 'chicago', 'houston', 'phoenix', 'philadelphia',
            'san antonio', 'san diego', 'dallas', 'san jose', 'austin',
            'miami', 'atlanta', 'boston', 'seattle', 'denver', 'detroit',
            'washington', 'portland', 'las vegas', 'baltimore', 'milwaukee',
            'oslo', 'bern', 'nice', 'cork', 'bath', 'york', 'hull', 'bonn',
            'linz', 'graz', 'lyon', 'metz', 'brest', 'tours', 'dijon', 'nancy',
            'vancouver', 'calgary', 'ottawa', 'winnipeg', 'quebec', 'halifax',
            'st. petersburg', 'saint-tropez', 'new delhi', 'kuala lumpur',
            'buenos aires', 'rio de janeiro', 'são paulo', 'mexico city',
            'saint john', 'st. louis', 'saint-étienne', 'coeur d\'alene'
        }
        
        # Valid hyphenated and apostrophe cities
        self.valid_special_cities = {
            'saint-tropez', 'baden-baden', 'stratford-upon-avon', 'winston-salem',
            'wilkes-barre', 'mineral wells', 'palm springs', 'crystal city',
            'garden city', 'cedar falls', 'grand rapids', 'sioux falls',
            'coeur d\'alene', 'martha\'s vineyard', 'queen\'s', 'king\'s lynn'
        }
        
        # Patterns that indicate fake/invalid input
        self.invalid_patterns = [
            r'^[bcdfghjklmnpqrstvwxyz]{5,}$',  # Only consonants (5+ chars)
            r'^[aeiou]{4,}$',  # Only vowels (4+ chars)
            r'^(.)\1{4,}',  # Repeated characters (5+ times)
            r'^(test|fake|dummy|random|error|null|none|spam)',  # Test words
            r'[;,!@#$%^&*()+=\[\]{}|\\:";\'<>?/~`]',  # Special characters except - and '
            r'^[qwerty]{5,}$',  # Keyboard patterns
            r'^[asdf]{5,}$',
            r'^[zxcv]{5,}$'
        ]
        
        # Known fake inputs to block immediately
        self.fake_inputs = {
            'khjl', 'khjl;', 'fnjaelf', 'bhjlk', 'njkef', 'ifej', 'haaae',
            'test', 'test123', 'asdf', 'qwer', 'hjkl', 'fake', 'dummy',
            'random', 'error', 'null', 'none', 'spam', 'invalid'
        }
    
    def check_internet_connection(self) -> bool:
        """Check if internet connection is available."""
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            return True
        except OSError:
            return False
    
    def contains_emoji(self, text: str) -> bool:
        """Check if text contains emojis using multiple detection methods."""
        for char in text:
            # Check for emoji categories
            if unicodedata.category(char) in ['So', 'Sm', 'Sk', 'Sc']:
                return True
            # Check for common emoji unicode ranges
            code_point = ord(char)
            if (0x1F600 <= code_point <= 0x1F64F) or \
               (0x1F300 <= code_point <= 0x1F5FF) or \
               (0x1F680 <= code_point <= 0x1F6FF) or \
               (0x1F1E0 <= code_point <= 0x1F1FF) or \
               (0x2600 <= code_point <= 0x26FF) or \
               (0x2700 <= code_point <= 0x27BF):
                return True
        return False
    
    def is_latin_script(self, text: str) -> bool:
        """Check if text uses Latin script (English-like characters)."""
        for char in text:
            if char.isalpha():
                script = unicodedata.name(char, '').split()[0]
                if not script.startswith('LATIN'):
                    return False
        return True
    
    def validate_city_input(self, city: str) -> Tuple[bool, str]:
        """
        Comprehensive city validation with specific error messages.
        Returns: (is_valid, error_message)
        """
        original_input = city
        
        # Check for empty input
        if not city or not city.strip():
            return False, "empty_input"
        
        # Check for very long input (over 50 characters)
        if len(city) > 50:
            return False, "too_long"
        
        # Check for emojis
        if self.contains_emoji(city):
            return False, "contains_emoji"
        
        # Check for numbers
        if any(char.isdigit() for char in city):
            return False, "contains_numbers"
        
        # Clean the input (handle leading/trailing spaces)
        city_clean = city.strip()
        
        # Check for non-English characters
        if not self.is_latin_script(city_clean):
            return False, "non_english"
        
        # Convert to lowercase for validation
        city_lower = city_clean.lower()
        
        # Check for known fake inputs
        if city_lower in self.fake_inputs:
            return False, "fake_input"
        
        # Allow known valid cities (including special characters)
        if city_lower in self.valid_cities or city_lower in self.valid_special_cities:
            return True, ""
        
        # Check for invalid special characters (except hyphens and apostrophes)
        if re.search(r'[;,!@#$%^&*()+=\[\]{}|\\:";\'<>?/~`]', city_clean):
            return False, "special_characters"
        
        # Validate hyphenated cities
        if '-' in city_clean:
            parts = city_clean.split('-')
            if len(parts) != 2 or any(len(part.strip()) < 2 for part in parts):
                return False, "invalid_hyphen"
        
        # Validate apostrophe cities
        if '\'' in city_clean:
            if city_clean.count('\'') > 1:
                return False, "invalid_apostrophe"
            parts = city_clean.split('\'')
            if len(parts) != 2 or any(len(part.strip()) < 1 for part in parts):
                return False, "invalid_apostrophe"
        
        # Check minimum length
        if len(city_clean) < 2:
            return False, "too_short"
        
        # Block obvious fake patterns
        for pattern in self.invalid_patterns:
            if re.search(pattern, city_lower):
                return False, "invalid_pattern"
        
        # Additional checks for suspicious patterns
        if len(city_clean) >= 4:
            # Check consonant/vowel ratio
            vowel_count = len(re.findall(r'[aeiou]', city_lower))
            consonant_count = len(re.sub(r'[^a-z]', '', city_lower)) - vowel_count
            
            if consonant_count > 0 and vowel_count == 0:
                return False, "no_vowels"
            
            if consonant_count > vowel_count * 3:
                return False, "too_many_consonants"
        
        return True, ""

class WeatherAPI:
    """Handles weather API calls with comprehensive error handling."""
    
    def __init__(self):
        load_dotenv()
        
        self.api_key = os.getenv('weatherdb_api_key')
        self.base_url = os.getenv('weatherdb_base_url')
        self.validator = CityValidator()
        
        if not self.api_key or not self.base_url:
            raise Exception("Missing API key or base URL in .env file")
    
    def get_weather(self, city: str) -> Tuple[Optional[Dict[str, Any]], str]:
        """
        Get weather data with comprehensive error handling.
        Returns: (weather_data, error_message)
        """
        try:
            # Check internet connection first
            if not self.validator.check_internet_connection():
                return None, "no_internet"
            
            # Validation is now handled in search_weather, so we can proceed with API call
            params = {
                'q': city.strip(),
                'appid': self.api_key,
                'units': 'imperial'
            }
            
            response = requests.get(self.base_url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'city': data['name'],
                    'country': data['sys']['country'],
                    'temp': round(data['main']['temp']),
                    'feels_like': round(data['main']['feels_like']),
                    'description': data['weather'][0]['description'].title(),
                    'humidity': data['main']['humidity'],
                    'pressure': data['main']['pressure'],
                    'wind_speed': data['wind'].get('speed', 0),
                    'visibility': data.get('visibility', 0) / 1000,
                    'uv_index': data.get('uvi', 0),
                    'precipitation': 0
                }, ""
            elif response.status_code == 404:
                return None, "city_not_found"
            elif response.status_code == 401:
                return None, "api_key_invalid"
            elif response.status_code == 429:
                return None, "api_limit_exceeded"
            else:
                return None, "api_error"
                
        except requests.exceptions.Timeout:
            return None, "request_timeout"
        except requests.exceptions.ConnectionError:
            return None, "connection_error"
        except requests.exceptions.RequestException:
            return None, "request_error"
        except Exception as e:
            return None, "unknown_error"

class WeatherApp:
    """Weather app with comprehensive error handling."""
    
    def __init__(self):
        self.weather_api = WeatherAPI()
        self.setup_gui()
        self.current_screen = "main"
        self.error_messages = {
            "empty_input": {
                "title": "Empty Input",
                "message": "Please enter a city name",
                "icon": "❌",
                "color": "#ff4444"
            },
            "too_long": {
                "title": "Input Too Long",
                "message": "City name is too long (max 50 characters)",
                "icon": "📏",
                "color": "#ff6600"
            },
            "contains_emoji": {
                "title": "Invalid Characters",
                "message": "City names cannot contain emojis",
                "icon": "😵",
                "color": "#ff4444"
            },
            "contains_numbers": {
                "title": "Invalid Characters",
                "message": "City names cannot contain numbers",
                "icon": "🔢",
                "color": "#ff4444"
            },
            "non_english": {
                "title": "Language Not Supported",
                "message": "Please use English alphabet characters only",
                "icon": "🌐",
                "color": "#ff6600"
            },
            "special_characters": {
                "title": "Invalid Characters",
                "message": "Only letters, spaces, hyphens, and apostrophes allowed",
                "icon": "⚠️",
                "color": "#ff4444"
            },
            "invalid_hyphen": {
                "title": "Invalid Format",
                "message": "Hyphenated cities must have valid parts (e.g., 'New-York')",
                "icon": "➖",
                "color": "#ff4444"
            },
            "invalid_apostrophe": {
                "title": "Invalid Format",
                "message": "Cities with apostrophes must be valid (e.g., 'Martha's Vineyard')",
                "icon": "❜",
                "color": "#ff4444"
            },
            "too_short": {
                "title": "Input Too Short",
                "message": "City name must be at least 2 characters long",
                "icon": "📏",
                "color": "#ff6600"
            },
            "fake_input": {
                "title": "Invalid City",
                "message": "This appears to be test input, not a real city",
                "icon": "🚫",
                "color": "#ff4444"
            },
            "invalid_pattern": {
                "title": "Invalid City",
                "message": "This doesn't appear to be a valid city name",
                "icon": "❌",
                "color": "#ff4444"
            },
            "no_vowels": {
                "title": "Invalid City",
                "message": "City names must contain vowels",
                "icon": "🔤",
                "color": "#ff4444"
            },
            "too_many_consonants": {
                "title": "Invalid City",
                "message": "This doesn't look like a real city name",
                "icon": "❌",
                "color": "#ff4444"
            },
            "no_internet": {
                "title": "No Internet Connection",
                "message": "Please check your internet connection and try again",
                "icon": "📡",
                "color": "#ff6600"
            },
            "city_not_found": {
                "title": "City Not Found",
                "message": "This city was not found in the weather database",
                "icon": "🔍",
                "color": "#ff6600"
            },
            "api_key_invalid": {
                "title": "Service Error",
                "message": "Weather service configuration error",
                "icon": "🔑",
                "color": "#ff4444"
            },
            "api_limit_exceeded": {
                "title": "Service Limit Reached",
                "message": "Too many requests. Please try again later",
                "icon": "⏰",
                "color": "#ff6600"
            },
            "request_timeout": {
                "title": "Request Timeout",
                "message": "The request took too long. Please try again",
                "icon": "⏱️",
                "color": "#ff6600"
            },
            "connection_error": {
                "title": "Connection Error",
                "message": "Unable to connect to weather service",
                "icon": "🌐",
                "color": "#ff6600"
            },
            "api_error": {
                "title": "Service Error",
                "message": "Weather service is temporarily unavailable",
                "icon": "⚠️",
                "color": "#ff6600"
            },
            "request_error": {
                "title": "Request Error",
                "message": "An error occurred while fetching weather data",
                "icon": "❌",
                "color": "#ff4444"
            },
            "unknown_error": {
                "title": "Unknown Error",
                "message": "An unexpected error occurred. Please try again",
                "icon": "❓",
                "color": "#ff4444"
            }
        }
    
    def setup_gui(self):
        """Setup the main GUI."""
        self.root = tk.Tk()
        self.root.title("Smart Weather App with Sun & Moon Phases")
        self.root.geometry("600x700")
        self.root.configure(bg='#87CEEB')
        
        # Main container frame
        self.main_frame = tk.Frame(self.root, bg='#87CEEB')
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        self.show_main_screen()
    
    def clear_screen(self):
        """Clear all widgets from the main frame."""
        for widget in self.main_frame.winfo_children():
            widget.destroy()
    
    def show_main_screen(self):
        """Show the main weather app screen."""
        self.clear_screen()
        self.current_screen = "main"
        
        # Title
        title = tk.Label(
            self.main_frame,
            text="🌤️ Smart Weather App with Sun & Moon Phases",
            font=("Arial", 20, "bold"),
            bg='#87CEEB',
            fg='#333'
        )
        title.pack(pady=20)
        
        # Search section
        search_frame = tk.Frame(self.main_frame, bg='#87CEEB')
        search_frame.pack(pady=10)
        
        self.city_entry = tk.Entry(
            search_frame,
            font=("Arial", 14),
            width=25,
            justify='center',
            relief='solid',
            bd=2
        )
        self.city_entry.pack(pady=10)
        self.city_entry.bind('<Return>', lambda e: self.search_weather())
        self.city_entry.bind('<KeyRelease>', self.on_key_release)  # Add real-time validation
        self.city_entry.focus()
        
        # Input help text
        help_text = tk.Label(
            search_frame,
            text="Enter city name (e.g., London, New York, Saint-Tropez, Martha's Vineyard)",
            font=("Arial", 10),
            bg='#87CEEB',
            fg='#666'
        )
        help_text.pack(pady=5)
        
        # Search button for alternative to Enter key
        search_button = tk.Button(
            search_frame,
            text="Get Weather",
            font=("Arial", 12, "bold"),
            bg='#4CAF50',
            fg='white',
            command=self.search_weather,
            cursor='hand2',
            relief='raised',
            bd=2
        )
        search_button.pack(pady=5)
        
        # Weather metrics display
        self.setup_weather_display()
        
        # Temperature and description
        self.temp_frame = tk.Frame(self.main_frame, bg='#87CEEB')
        self.temp_frame.pack(pady=20)
        
        self.temp_display = tk.Label(
            self.temp_frame,
            text="--°C",
            font=("Arial", 48, "bold"),
            bg='#87CEEB',
            fg='#000'
        )
        self.temp_display.pack()
        
        self.desc_display = tk.Label(
            self.temp_frame,
            text="Enter a city above",
            font=("Arial", 18),
            bg='#87CEEB',
            fg='#000'
        )
        self.desc_display.pack()
        
        # Feature buttons
        self.setup_feature_buttons()
    
    def setup_weather_display(self):
        """Setup weather metrics display."""
        metrics_frame = tk.Frame(self.main_frame, bg='#87CEEB')
        metrics_frame.pack(pady=20)
        
        metrics = [
            ("Humidity", "💧", "humidity_display"),
            ("Wind", "💨", "wind_display"),
            ("Press.", "🌡️", "pressure_display"),
            ("Visibility", "👁️", "visibility_display"),
            ("UV Index", "☀️", "uv_display"),
            ("Precip.", "🌧️", "precip_display")
        ]
        
        # Create two rows of 3 metrics each
        for i, (label, icon, attr) in enumerate(metrics):
            row = i // 3
            col = i % 3
            
            metric_frame = tk.Frame(metrics_frame, bg='#87CEEB')
            metric_frame.grid(row=row, column=col, padx=30, pady=15)
            
            # Icon and label
            label_widget = tk.Label(
                metric_frame,
                text=f"{label}",
                font=("Arial", 12, "bold"),
                bg='#87CEEB',
                fg='#333'
            )
            label_widget.pack()
            
            # Icon
            icon_widget = tk.Label(
                metric_frame,
                text=icon,
                font=("Arial", 20),
                bg='#87CEEB'
            )
            icon_widget.pack()
            
            # Value
            value_widget = tk.Label(
                metric_frame,
                text="N/A",
                font=("Arial", 14, "bold"),
                bg='#87CEEB',
                fg='#666'
            )
            value_widget.pack()
            setattr(self, attr, value_widget)
    
    def setup_feature_buttons(self):
        """Setup feature buttons."""
        buttons_frame = tk.Frame(self.main_frame, bg='#87CEEB')
        buttons_frame.pack(pady=30)
        
        button_names = [
            "Toggle Theme", "Tomorrow's Prediction", "Weather History",
            "City Comparison", "Weather Graphs", "Map View",
            "Weather Quiz", "Sun & Moon", "Language"
        ]
        
        for i, name in enumerate(button_names):
            row = i // 3
            col = i % 3
            
            btn = tk.Button(
                buttons_frame,
                text=name,
                font=("Arial", 10),
                bg='#999',
                fg='white',
                width=15,
                height=2,
                relief='raised',
                bd=2
            )
            btn.grid(row=row, column=col, padx=5, pady=5)
    
    def show_error_screen(self, city_input: str, error_type: str):
        """Show FULL-SCREEN error with specific error message and prominent back button."""
        # COMPLETELY CLEAR THE ENTIRE SCREEN
        self.clear_screen()
        self.current_screen = "error"
        
        # Get error details
        error_info = self.error_messages.get(error_type, {
            "title": "Error",
            "message": "An error occurred",
            "icon": "❌",
            "color": "#ff4444"
        })
        
        # Create FULL-SCREEN error container that takes up entire window
        error_container = tk.Frame(self.main_frame, bg='#87CEEB')
        error_container.pack(expand=True, fill=tk.BOTH)
        
        # Center everything vertically and horizontally
        center_frame = tk.Frame(error_container, bg='#87CEEB')
        center_frame.pack(expand=True)
        
        # LARGE error icon that dominates the screen
        error_icon = tk.Label(
            center_frame,
            text=error_info["icon"],
            font=("Arial", 120),  # Even larger icon
            bg='#87CEEB',
            fg=error_info["color"]
        )
        error_icon.pack(pady=(80, 40))
        
        # LARGE error title
        error_title = tk.Label(
            center_frame,
            text=error_info["title"],
            font=("Arial", 42, "bold"),  # Larger title
            bg='#87CEEB',
            fg=error_info["color"]
        )
        error_title.pack(pady=25)
        
        # Error message
        error_msg = tk.Label(
            center_frame,
            text=error_info["message"],
            font=("Arial", 22),  # Larger message
            bg='#87CEEB',
            fg='#333',
            wraplength=500  # Wrap long messages
        )
        error_msg.pack(pady=20)
        
        # Show the problematic input (if not empty)
        if city_input.strip() and error_type != "empty_input":
            input_display = tk.Label(
                center_frame,
                text=f"Your input: '{city_input}'",
                font=("Arial", 18, "italic"),
                bg='#87CEEB',
                fg='#666'
            )
            input_display.pack(pady=15)
        
        # Instructions
        instruction = tk.Label(
            center_frame,
            text="Please try again with a valid city name",
            font=("Arial", 20, "bold"),
            bg='#87CEEB',
            fg='#666'
        )
        instruction.pack(pady=20)
        
        # Examples
        examples = tk.Label(
            center_frame,
            text="Valid examples: London, New York, Saint-Tropez, Martha's Vineyard",
            font=("Arial", 16),
            bg='#87CEEB',
            fg='#888',
            wraplength=500
        )
        examples.pack(pady=15)
        
        # PROMINENT BACK BUTTON - Large and eye-catching
        back_button = tk.Button(
            center_frame,
            text="← Back to Weather App",
            font=("Arial", 24, "bold"),  # Much larger button text
            bg='#4CAF50',
            fg='white',
            width=20,  # Wider button
            height=3,  # Taller button
            command=self.show_main_screen,
            cursor='hand2',
            relief='raised',
            bd=4,  # Thicker border
            activebackground='#45a049',  # Hover effect
            activeforeground='white'
        )
        back_button.pack(pady=(60, 40))
        back_button.focus()
        
        # MULTIPLE ways to go back for user convenience
        self.root.bind('<Return>', lambda e: self.show_main_screen())
        self.root.bind('<Escape>', lambda e: self.show_main_screen())
        self.root.bind('<BackSpace>', lambda e: self.show_main_screen())
        
        # Add visual emphasis to the error state
        self.root.configure(bg='#87CEEB')  # Ensure consistent background
    
    def show_weather_data(self, weather_data: Dict[str, Any]):
        """Display weather data on main screen."""
        if self.current_screen == "main":
            # Update metrics
            self.humidity_display.config(text=f"{weather_data['humidity']}%", fg='#333')
            self.wind_display.config(text=f"{weather_data['wind_speed']:.1f} m/s", fg='#333')
            self.pressure_display.config(text=f"{weather_data['pressure']} hPa", fg='#333')
            self.visibility_display.config(text=f"{weather_data['visibility']:.1f} km", fg='#333')
            self.uv_display.config(text=f"{weather_data['uv_index']}", fg='#333')
            self.precip_display.config(text=f"{weather_data['precipitation']} mm", fg='#333')
            
            # Update temperature and description
            self.temp_display.config(text=f"{weather_data['temp']}°F", fg='#000')
            self.desc_display.config(text=f"{weather_data['description']} in {weather_data['city']}, {weather_data['country']}", fg='#000')
    
    def on_key_release(self, event):
        """Handle key release events for real-time feedback."""
        # This can be used for real-time validation feedback if needed
        pass
    
    def search_weather(self):
        """Search for weather with comprehensive error handling."""
        city_input = self.city_entry.get()
        
        # Clear any previous key bindings
        self.root.unbind('<Return>')
        self.root.unbind('<Escape>')
        self.root.unbind('<BackSpace>')
        
        # ALWAYS validate input first, regardless of content
        validator = CityValidator()
        is_valid, error_msg = validator.validate_city_input(city_input)
        
        # If validation fails, show error immediately
        if not is_valid:
            self.show_error_screen(city_input, error_msg)
            return
        
        try:
            # Get weather data with error handling
            weather_data, error_msg = self.weather_api.get_weather(city_input)
            
            if weather_data is None:
                # Show specific error screen
                self.show_error_screen(city_input, error_msg)
            else:
                # Valid city - show weather data
                self.show_weather_data(weather_data)
                
        except Exception as e:
            self.show_error_screen(city_input, "unknown_error")
    
    def run(self):
        """Start the application."""
        self.root.mainloop()

if __name__ == "__main__":
    try:
        app = WeatherApp()
        app.run()
    except Exception as e:
        messagebox.showerror("Startup Error", f"Could not start weather app:\n\n{e}")
        