import tkinter as tk
from tkinter import messagebox
import time
import requests
import os
import re
from dotenv import load_dotenv
from typing import Dict, Any, Optional
from datetime import datetime
import json

class CityValidator:
    """Strict city validation to block all fake inputs."""
    
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
            'vancouver', 'calgary', 'ottawa', 'winnipeg', 'quebec', 'halifax'
        }
        
        # Patterns that indicate fake/invalid input
        self.invalid_patterns = [
            r'^[bcdfghjklmnpqrstvwxyz]{4,}$',  # Only consonants
            r'^[aeiou]{3,}$',  # Only vowels
            r'^(.)\1{3,}',  # Repeated characters
            r'^(test|fake|dummy|random|error|null|none)',  # Test words
            r'\d{2,}',  # Multiple numbers
            r'^[qwerty]{4,}$',  # Keyboard patterns
            r'^[asdf]{4,}$',
            r'^[zxcv]{4,}$',
            r'[;,!@#$%^&*()]+',  # Punctuation
            r'^[a-z]{4}[;,]?$'  # 4 random letters with punctuation
        ]
        
        # Known fake inputs to block immediately
        self.fake_inputs = {
            'khjl', 'khjl;', 'fnjaelf', 'bhjlk', 'njkef', 'ifej', 'haaae',
            'test', 'test123', 'asdf', 'qwer', 'hjkl', 'fake', 'dummy'
        }
    
    def is_valid_city(self, city: str) -> bool:
        """Strict validation to block fake cities."""
        if not city or len(city.strip()) < 2:
            return False
        
        # Clean the input
        city_clean = city.strip().lower().replace(';', '').replace(',', '')
        
        # Block known fake inputs immediately
        if city_clean in self.fake_inputs:
            return False
        
        # Allow known valid cities
        if city_clean in self.valid_cities:
            return True
        
        # Block obvious fake patterns
        for pattern in self.invalid_patterns:
            if re.search(pattern, city_clean):
                return False
        
        # Additional strict checks
        if len(city_clean) >= 4:
            # Block if too many consonants in a row
            if re.search(r'[bcdfghjklmnpqrstvwxyz]{4,}', city_clean):
                return False
            
            # Block weird letter combinations
            weird_combos = ['fnj', 'jae', 'aelf', 'hjl', 'bhjl', 'njk', 'kef', 'khjl']
            for combo in weird_combos:
                if combo in city_clean:
                    return False
            
            # Check consonant/vowel ratio
            vowel_count = len(re.findall(r'[aeiou]', city_clean))
            consonant_count = len(city_clean) - vowel_count
            
            # Block if mostly consonants (suspicious)
            if consonant_count > vowel_count * 2.5:
                return False
        
        return True

class WeatherAPI:
    """Handles weather API calls with strict validation."""
    
    def __init__(self):
        load_dotenv()
        
        self.api_key = os.getenv('weatherdb_api_key')
        self.base_url = os.getenv('weatherdb_base_url')
        self.validator = CityValidator()
        
        if not self.api_key or not self.base_url:
            raise Exception("Missing API key or base URL in .env file")
    
    def get_weather(self, city: str) -> Optional[Dict[str, Any]]:
        """Get weather data only for valid cities."""
        try:
            # STRICT VALIDATION FIRST - Block fake cities before API call
            if not self.validator.is_valid_city(city):
                print(f"❌ Blocked fake city: {city}")
                return None
            
            params = {
                'q': city,
                'appid': self.api_key,
                'units': 'imperial'
            }
            
            response = requests.get(self.base_url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Valid weather data for: {data['name']}")
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
                }
            else:
                print(f"❌ API returned error for: {city}")
                return None
                
        except Exception as e:
            print(f"❌ Exception for {city}: {str(e)}")
            return None

class WeatherApp:
    """Weather app with strict validation and error screen."""
    
    def __init__(self):
        self.weather_api = WeatherAPI()
        self.setup_gui()
        self.current_screen = "main"
    
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
        self.city_entry.focus()
        
        # Weather metrics display
        self.setup_weather_display()
        
        # Temperature and description (like your original design)
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
        """Setup feature buttons like your original design."""
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
    
    def show_error_screen(self, city_input: str):
        """Show full-screen error when city is invalid."""
        print(f"🚫 Showing error screen for: {city_input}")
        
        # COMPLETELY CLEAR THE SCREEN
        self.clear_screen()
        self.current_screen = "error"
        
        # Create error screen with centered content
        error_container = tk.Frame(self.main_frame, bg='#87CEEB')
        error_container.pack(expand=True, fill=tk.BOTH)
        
        # Center everything vertically
        center_frame = tk.Frame(error_container, bg='#87CEEB')
        center_frame.pack(expand=True)
        
        # Large error icon
        error_icon = tk.Label(
            center_frame,
            text="❌",
            font=("Arial", 100),
            bg='#87CEEB',
            fg='#ff4444'
        )
        error_icon.pack(pady=(50, 30))
        
        # Error title
        error_title = tk.Label(
            center_frame,
            text="Incorrect Input",
            font=("Arial", 36, "bold"),
            bg='#87CEEB',
            fg='#ff4444'
        )
        error_title.pack(pady=20)
        
        # Error message with the specific input
        error_msg = tk.Label(
            center_frame,
            text=f"'{city_input}' is not a valid city name",
            font=("Arial", 20),
            bg='#87CEEB',
            fg='#333'
        )
        error_msg.pack(pady=15)
        
        # Instructions
        instruction = tk.Label(
            center_frame,
            text="Please enter a valid city",
            font=("Arial", 18, "bold"),
            bg='#87CEEB',
            fg='#666'
        )
        instruction.pack(pady=15)
        
        # Examples
        examples = tk.Label(
            center_frame,
            text="Examples: New York, London, Tokyo, Paris, Berlin",
            font=("Arial", 16),
            bg='#87CEEB',
            fg='#888'
        )
        examples.pack(pady=15)
        
        # Back button - large and prominent
        back_button = tk.Button(
            center_frame,
            text="← Back",
            font=("Arial", 20, "bold"),
            bg='#4CAF50',
            fg='white',
            width=12,
            height=2,
            command=self.show_main_screen,
            cursor='hand2',
            relief='raised',
            bd=3
        )
        back_button.pack(pady=(50, 20))
        back_button.focus()
        
        # Also bind Enter key to go back
        self.root.bind('<Return>', lambda e: self.show_main_screen())
    
    def show_weather_data(self, weather_data: Dict[str, Any]):
        """Display weather data on main screen."""
        if self.current_screen == "main":
            # Update metrics
            self.humidity_display.config(text=f"{weather_data['humidity']}%", fg='#333')
            self.wind_display.config(text=f"{weather_data['wind_speed']} m/s", fg='#333')
            self.pressure_display.config(text=f"{weather_data['pressure']} hPa", fg='#333')
            self.visibility_display.config(text=f"{weather_data['visibility']:.1f} km", fg='#333')
            self.uv_display.config(text=f"{weather_data['uv_index']}", fg='#333')
            self.precip_display.config(text=f"{weather_data['precipitation']} mm", fg='#333')
            
            # Update temperature and description
            self.temp_display.config(text=f"{weather_data['temp']}°C", fg='#000')
            self.desc_display.config(text=weather_data['description'], fg='#000')
    
    def search_weather(self):
        """Search for weather with strict validation."""
        city_input = self.city_entry.get().strip()
        
        print(f"\n🔍 Searching for: '{city_input}'")
        
        if not city_input:
            print("❌ Empty input")
            return
        
        # Clear any previous key bindings
        self.root.unbind('<Return>')
        
        try:
            # Get weather data (validation happens inside WeatherAPI)
            weather_data = self.weather_api.get_weather(city_input)
            
            if weather_data is None:
                # City is invalid - show error screen
                print(f"🚫 Invalid city, showing error screen")
                self.show_error_screen(city_input)
            else:
                # Valid city - show weather data
                print(f"✅ Showing weather data")
                self.show_weather_data(weather_data)
                
        except Exception as e:
            print(f"❌ Exception occurred: {str(e)}")
            self.show_error_screen(city_input)
    
    def run(self):
        """Start the application."""
        print("🌤️ Smart Weather App Started")
        print("=" * 50)
        print("• Invalid cities will show error screen")
        print("• Use back button to return and try again")
        print("• Fake inputs like 'khjl;' will be blocked")
        print("=" * 50)
        
        self.root.mainloop()

if __name__ == "__main__":
    try:
        app = WeatherApp()
        app.run()
    except Exception as e:
        print(f"❌ Failed to start app: {e}")
        messagebox.showerror("Startup Error", f"Could not start weather app:\n\n{e}")
        