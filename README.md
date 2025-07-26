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

# Weather App Language System

A modular, comprehensive language management system for the weather application, broken down into logical components for maintainability and extensibility.

## File Structure

### 1. `language_translations.py`
**Purpose**: Contains all translation data and language configuration.

**Contents**:
- `TRANSLATIONS`: Complete dictionary of all text translations for English, Spanish, and Hindi
- `SUPPORTED_LANGUAGES`: Mapping of language names to API codes
- All translatable text organized by categories (UI elements, weather terms, moon phases, etc.)

**Why separate**: Pure data file that can be easily maintained, exported, or replaced without affecting logic.

### 2. `language_ui.py`
**Purpose**: Handles all user interface components for language selection.

**Contents**:
- `LanguageUI` class managing the language selection page
- Widget creation and management for dropdowns, buttons, labels
- UI event handling and user interactions
- Page layout and styling for language selection

**Why separate**: Separates UI concerns from business logic, making it easier to modify the interface without affecting translation logic.

### 3. `language_controller.py`
**Purpose**: Main controller coordinating all language operations.

**Contents**:
- `LanguageController` class as the central language manager
- Core translation methods (`get_text`, `update_all_translatable_widgets`)
- Language switching logic and settings persistence
- Integration points with the main application
- Specialized translation methods for weather terms, moon phases, etc.

**Why separate**: Central coordination point that other parts of the app interact with, keeping the API simple and consistent.

### 4. `language_utils.py`
**Purpose**: Advanced utilities and analytics for translation management.

**Contents**:
- `LanguageUtils` class with advanced features
- Translation completeness analysis and reporting
- Import/export functionality for translations
- Validation and optimization tools
- Search and diff capabilities for translation management

**Why separate**: Advanced features that aren't needed for basic operation, keeping the core system lightweight while providing powerful tools for maintenance.

## Usage

### Basic Integration
```python
# In your main application
from language_controller import LanguageController

# Initialize
lang_ctrl = LanguageController(app, gui_controller)

# Get translated text
text = lang_ctrl.get_text("weather_app_title")

# Show language selection page
lang_ctrl.build_page(window_width, window_height)
```

### Advanced Features
```python
# For advanced translation management
from language_utils import LanguageUtils

utils = LanguageUtils(lang_ctrl)

# Get translation completeness report
stats = utils.get_translation_completeness()

# Export translations
utils.export_translations("backup.json")

# Validate translations
validation = utils.validate_translations()
```

## Key Benefits

### 1. **Modularity**
- Each file has a single, clear responsibility
- Components can be modified independently
- Easy to test individual components

### 2. **Maintainability**
- Translation data separated from logic
- UI components isolated from business logic
- Advanced features don't complicate basic usage

### 3. **Extensibility**
- Easy to add new languages by updating `language_translations.py`
- UI can be enhanced without affecting core functionality
- New advanced features can be added to utils without breaking existing code

### 4. **Scalability**
- Translation data can be moved to external files or databases
- UI components can be replaced with different frameworks
- Advanced features provide tools for managing large translation sets

## Import Structure

The system is designed to minimize dependencies:

```
language_controller.py
├── language_translations.py (data only)
└── language_ui.py
    └── language_translations.py (for supported languages list)

language_utils.py
├── language_translations.py (data only)
└── language_controller.py (for integration)
```

## Migration from Original File

To migrate from the original single file:

1. Replace the original import:
   ```python
   # Old
   from language_selection_controller import LanguageController
   
   # New
   from language_controller import LanguageController
   ```

2. All existing API calls remain the same - no code changes needed in the main application.

3. For advanced features, optionally add:
   ```python
   from language_utils import LanguageUtils
   utils = LanguageUtils(lang_ctrl)
   ```

## Adding New Languages

1. Add language to `SUPPORTED_LANGUAGES` in `language_translations.py`
2. Add complete translation dictionary to `TRANSLATIONS`
3. No code changes needed - the system automatically supports the new language

## Translation Management

The system provides comprehensive tools for managing translations:

- **Completeness tracking**: See which translations are missing
- **Validation**: Check for empty or invalid translations
- **Import/Export**: Backup and restore translation data
- **Search**: Find specific translations across languages
- **Optimization**: Clean up and optimize translation data

This modular approach ensures the language system can grow with the application while maintaining clean, maintainable code.