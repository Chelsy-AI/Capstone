# Weather Dashboard Capstone Project

## Overview:

- Desktop weather app using Python and CustomTkinter
- Fetches real-time and 7-day historical weather data via Open-Meteo API 
- Supports light/dark themes toggle with persistent preferences
- Temperature toggle between Celsius and Fahrenheit by clicking temperature label
- Shows detailed metrics: humidity, wind, pressure, visibility, UV index, precipitation
- Predicts tomorrow's temperature with confidence and accuracy tracking
- Saves weather history and prediction accuracy locally as CSV files
- Interactive weather map with real-time city location updates and weather overlays
- Dynamic weather animations that match current conditions (rain, snow, storms, clouds)
- Custom canvas-based weather icons with API fallbacks
- Scrollable interface supporting content expansion
- Comprehensive error handling with user-friendly messages
- Modular architecture with organized feature separation

## Installation:

- Clone repo: `git clone https://github.com/yourusername/weather-dashboard.git`
- `cd weather-dashboard`
- Create and activate virtual environment:
  ```
  python -m venv venv
  # Windows: venv\Scripts\activate
  # Mac/Linux: source venv/bin/activate
  ```
- Install dependencies: `pip install -r requirements.txt`
- Optional: Install `tkintermapview` for enhanced map features

## Usage:

- Run app: `python main.py`
- Enter city name in search box to get weather data for any global location
- Click temperature label to toggle between °C and °F 
- Toggle light/dark theme with button 
- View tomorrow's prediction with confidence percentage and accuracy tracking
- Scroll down to access 7-day historical weather data with max/min/average temperatures
- Explore interactive map showing current city location with optional weather overlays
- Watch background animations automatically change based on current weather conditions

## Custom Features:

### 1. History Tracker 

- Comprehensive 7-day historical weather data tracking and display
- Fetches historical data from Open-Meteo Archive API with intelligent caching
- Responsive grid layout showing dates, max/min/average temperatures
- Automatic data processing and unit conversion (°C ↔ °F)
- CSV data persistence for long-term weather pattern analysis
- Smart error handling for missing or incomplete historical data

### 2. Theme Switcher

- Dynamic light/dark mode switching with smooth transitions
- Persistent theme preferences saved between sessions in JSON format
- Color scheme updates across all GUI components including animations
- Professional UI design with accessibility considerations
- Automatic background color adjustments for optimal contrast

### 3. Weather Icons System

- Multi-tier icon system with API, canvas, and emoji fallbacks
- Real-time weather icon fetching from OpenWeatherMap API
- Custom canvas-based weather icons with detailed graphics
- Intelligent caching system to improve performance
- Automatic fallback to emoji icons for maximum compatibility

### 4. Tomorrow's Weather Prediction

- Statistical analysis of 7-day historical weather patterns
- Tomorrow's temperature prediction with confidence metrics (0-100%)
- Accuracy tracking based on previous prediction performance
- Machine learning-inspired algorithms using moving averages
- Real-time confidence scoring based on data quality and consistency

### 5. Background Weather Animations

- Particle-based background animations with realistic physics
- Multiple weather types: rain drops with wind effects, snowflakes with drift patterns
- Storm animations with lightning effects and dark clouds
- Smooth 30fps performance with optimized particle management
- Automatic animation switching based on current weather descriptions

### 6. Interactive Weather Map

- Real-time map integration using tkintermapview library
- Automatic geocoding to show accurate city locations with markers
- Weather overlay layers including temperature, precipitation, and cloud coverage
- Graceful fallback interface for systems without map library installed
- Integration with OpenStreetMap for reliable global coverage

## Project Structure:

```
weather-dashboard/
├── main.py                 # Application entry point
├── config/                 # Core application modules
│   ├── weather_app.py     # Main application class
│   ├── api.py             # Weather API integration
│   ├── storage.py         # CSV data persistence
│   ├── gui/               # GUI components and layout
│   └── animations.py      # Weather animation system
├── features/              # Custom feature implementations
│   ├── interactive_map/   # Map integration and controls
│   ├── history_tracker/   # Historical data management
│   ├── tomorrows_guess/   # Prediction algorithms
│   └── theme_switcher/    # Theme management
├── data/                  # Local data storage
└── tests/                 # Comprehensive test suite
```

## API Integration:

- **Open-Meteo API**: Primary weather data source 

- **Open-Meteo Geocoding**: City name to coordinates conversion

- **Open-Meteo Archive**: Historical weather data for 7-day tracking

- **OpenStreetMap Nominatim**: Backup geocoding for map features

- All APIs are free with no API keys required

## Testing:

- Run tests with: `pytest tests/`
- Run animation tests: `python tests/test_animations.py`
- Includes tests for API integration, GUI components, prediction logic, and utility functions
- Coverage includes error handling, data validation, and feature functionality

## Dependencies:

- Python 3.8+
- CustomTkinter (modern GUI framework)
- requests (HTTP API calls)
- tkintermapview (interactive maps - optional)
- Pillow (image processing for weather icons)
- pytest (testing framework)

## Notes:

- Internet connection required for real-time weather data
- Application works with or without tkintermapview 
- All weather data automatically saved to CSV files in data/ directory
- Supports responsive layout for different screen sizes and resolutions