# Weather Dashboard

A comprehensive desktop weather application built with Python and CustomTkinter, featuring real-time weather data, interactive visualizations, multilingual support, and advanced weather prediction capabilities.

## ✨ Features

### 🌡️ Core Weather Information
- **Real-time Weather Data** - Current conditions including temperature, humidity, wind speed, pressure, visibility, UV index, and precipitation
- **7-Day Historical Tracking** - Complete weather history with intelligent caching and CSV persistence
- **Temperature Unit Toggle** - Seamless switching between Celsius and Fahrenheit
- **Weather Prediction** - AI-powered tomorrow's temperature prediction with confidence scoring

### 🎨 User Interface & Experience
- **Dynamic Themes** - Light/dark mode with persistent user preferences
- **Multilingual Support** - Complete localization in English, Spanish, and Hindi
- **Responsive Design** - Adaptive interface supporting various screen sizes
- **Weather Animations** - Real-time particle effects matching current conditions (rain, snow, storms, clouds)

### 🚀 Advanced Features
- **Interactive Weather Map** - Real-time city locations with weather overlays using OpenStreetMap
- **City Comparison Tool** - Side-by-side weather analysis between multiple locations
- **Interactive Graphs** - Dynamic data visualizations with hover tooltips and zoom functionality
- **Astronomical Data** - Detailed sun/moon phases, sunrise/sunset times, and lunar information
- **Educational Quiz System** - Interactive weather knowledge testing with scoring
- **Custom Icon System** - Multi-tier weather icons with API, canvas, and emoji fallbacks

## 🚀 Quick Start

### Prerequisites
- **Python 3.8+** (Python 3.9+ recommended)
- **Operating System**: Windows 10+, macOS 10.14+, or Linux with GUI support
- **Internet Connection** for real-time weather data
- **4GB RAM minimum** (8GB recommended for optimal performance)

### Installation

```bash
# Clone the repository
git clone https://github.com/Chelsy-AI/Capstone.git
cd Capstone

# Create virtual environment
python -m venv weather_env

# Activate virtual environment
# Windows:
weather_env\Scripts\activate
# macOS/Linux:
source weather_env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

### Optional Enhanced Features
```bash
# For interactive map functionality
pip install tkintermapview

# For enhanced graphs and visualizations
pip install matplotlib numpy pandas
```

### First Launch Setup
1. **Language Selection** - Choose from English, Spanish, or Hindi
2. **Text Theme Preference** - Select light or dark text
3. **Default Location** - Enter your preferred city for startup

## 📖 Usage Guide

### Basic Operations
- **Search Weather**: Enter city name in search box and press Enter
- **Toggle Units**: Click on temperature displays to switch °C/°F
- **Change Text Theme**: Use text toggle button for light/dark text
- **View History**: Scroll down to access 7-day historical data

### Advanced Features
- **Interactive Map**: Click map tab to explore weather globally
- **City Comparison**: Add multiple cities for side-by-side analysis
- **Weather Graphs**: Hover over charts for detailed data points
- **Quiz System**: Test weather knowledge in the quiz section
- **Predictions**: View tomorrow's forecast with confidence scores

## 🏗️ Project Architecture

```
weather-dashboard/
├── main.py                    # Application entry point
├── requirements.txt           # Python dependencies
├── language_settings.json    # Language preferences
├── data/                     # Local data storage
│   ├── weather_history.csv   # Historical weather data
│   ├── city.csv              # City database
│   └── combined.csv          # Aggregated data
├── weather_dashboard/        # Main application package
│   ├── config/              # Core configuration
│   │   ├── animations.py    # Weather animation system
│   │   ├── api.py          # API integration layer
│   │   ├── error_handler.py # Error handling & logging
│   │   ├── storage.py      # Data persistence
│   │   ├── themes.py       # Theme management
│   │   ├── utils.py        # Utility functions
│   │   └── weather_app.py  # Main application class
│   ├── features/           # Modular features
│   │   ├── city_comparison/     # Multi-city comparison
│   │   ├── graphs/             # Data visualizations
│   │   ├── history_tracker/    # Historical data
│   │   ├── interactive_map/    # Map integration
│   │   ├── sun_moon_phases/    # Astronomical data
│   │   ├── theme_switcher/     # Dynamic theming
│   │   ├── tomorrows_guess/    # Weather prediction
│   │   ├── weather_icons/      # Icon system
│   │   └── weather_quiz/       # Educational quiz
│   ├── gui/                # User interface
│   │   ├── animation_controller.py
│   │   ├── main_gui.py
│   │   └── weather_display.py
│   └── language/           # Internationalization
│       ├── controller.py   # Language management
│       ├── translations.py # Translation data
│       └── utils.py       # Language utilities
├── scripts/                # Build and deployment
│   └── build_config.py    # PyInstaller configuration
└── tests/                 # Test suite
    ├── __init__.py
    └── test_weather_app.py
```

## 🔌 API Integration

The application integrates with multiple weather APIs for comprehensive data:

| API Service | Purpose | Fallback |
|-------------|---------|----------|
| **Open-Meteo** | Primary weather data | OpenWeatherMap |
| **Open-Meteo Geocoding** | City coordinates | Nominatim |
| **Open-Meteo Archive** | Historical data | Local cache |
| **Sunrise-Sunset API** | Astronomical data | Mathematical calculation |
| **OpenStreetMap** | Map tiles | Fallback map interface |

### API Rate Limiting
- Intelligent caching reduces API calls by 70%
- Automatic retry with exponential backoff
- Graceful degradation when APIs are unavailable

## 🚀 Building Executable

Create standalone executable for distribution:

```bash
# Install PyInstaller
pip install pyinstaller

# Build executable using provided script
python scripts/build_config.py

# Output locations:
# Windows: dist/WeatherDashboard.exe
# macOS: dist/WeatherDashboard.app
# Linux: dist/WeatherDashboard
```

### Build Features
- **Single File**: Complete application in one executable
- **Platform Icons**: Automatically includes appropriate icons
- **Version Info**: Embedded version information
- **Dependency Bundling**: All required libraries included

## 🧪 Testing

### Run Test Suite
```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=weather_dashboard

# Run specific test categories
pytest tests/ -k "test_api"      # API tests only
pytest tests/ -k "test_gui"      # GUI tests only
pytest tests/ -k "test_features" # Feature tests only
```

### Manual Testing Checklist
- [ ] Application starts without errors
- [ ] Weather data loads for multiple cities
- [ ] Text theme switching works correctly
- [ ] Language changes apply immediately
- [ ] Historical data displays properly
- [ ] Map functionality (if tkintermapview installed)
- [ ] Animations perform smoothly
- [ ] Error handling works gracefully

## 🛠️ Troubleshooting

### Common Issues

**Installation Problems:**
```bash
# Issue: Module import errors
# Solution: Ensure virtual environment is activated
source weather_env/bin/activate  # Linux/Mac
weather_env\Scripts\activate     # Windows

# Issue: Permission denied
# Solution: Run as administrator (Windows) or use sudo (Linux/Mac)
```

**Runtime Issues:**
- **No weather data**: Check internet connection, verify city name spelling
- **Map not displaying**: Install `tkintermapview` with `pip install tkintermapview`
- **Poor animation performance**: Disable animations in settings or reduce FPS
- **Language not switching**: Restart application after language change

**Performance Optimization:**
```bash
# Reduce memory usage
export MAX_CACHE_SIZE=500

# Improve animation performance  
export ANIMATION_FPS=15

# Disable optional features
export ENABLE_ANIMATIONS=false
export ENABLE_MAP=false
```

### Debug Mode
```bash
# Run with debug logging
python main.py --debug

# Enable verbose error messages
export WEATHER_DEBUG=true
python main.py
```

## 🤝 Contributing

### Development Setup
```bash
# Fork repository and clone
git clone https://github.com/Chelsy-AI/Capstone.git
cd Capstone

# Create development branch
git checkout -b feature/your-feature-name

# Install development dependencies
pip install -r requirements.txt
pip install pytest black flake8 mypy

# Run code quality checks
black weather_dashboard/          # Code formatting
flake8 weather_dashboard/         # Linting
mypy weather_dashboard/           # Type checking
pytest tests/                     # Run tests
```

### Contribution Guidelines
1. **Code Style**: Follow PEP 8, use Black for formatting
2. **Testing**: Add tests for new features, maintain >80% coverage
3. **Documentation**: Update relevant docs for API changes
4. **Commits**: Use conventional commit messages
5. **Pull Requests**: Include description, tests, and documentation updates

## 📊 Performance Metrics

### Typical Performance
- **Startup Time**: 2-5 seconds
- **Weather Data Fetch**: 500ms-2s
- **Animation Frame Rate**: 30 FPS
- **Memory Usage**: 50-150MB
- **Disk Space**: 100-200MB with cache

### Optimization Features
- **Lazy Loading**: Features load on-demand
- **Intelligent Caching**: Reduces API calls by 70%
- **Memory Management**: Automatic cleanup of unused data
- **Network Optimization**: Concurrent API requests

## 🙏 Acknowledgments

- **Weather Data**: [Open-Meteo](https://open-meteo.com/) - Free weather API
- **Map Services**: [OpenStreetMap](https://www.openstreetmap.org/) - Open source maps  
- **GUI Framework**: [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) - Modern Tkinter
- **Icons**: Weather icons adapted from various open source collections
- **Translations**: Community contributors for multilingual support

## 📈 Roadmap

### Upcoming Features
- [ ] **Extended Forecasts** - 14-day weather predictions
- [ ] **Weather Widgets** - Desktop widget support
- [ ] **Plugin System** - Third-party feature extensions
- [ ] **Mobile Companion** - Mobile app integration
- [ ] **Advanced Analytics** - Weather pattern analysis
- [ ] **Weather Impact on Health & Wellness** - Effects of weather on physical and mental health
- [ ] **AI-Powered Weather Chatbot** - Conversational assistant for forecasts and advice
- [ ] **Autofill Cities** - Smart location-based city suggestions

### Long-term Goals
- Web-based version for browser access
- Real-time weather station integration
- Machine learning enhanced predictions
- Social features for weather sharing
- Professional meteorologist tools

---

**Need Help?** 
- 📖 Read the [User Guide](UserGuide.md)
- 🐛 Report issues on [GitHub](https://github.com/Chelsy-AI/Capstone/issues)

**Version**: 2.0.0 | **Last Updated**: August 2025