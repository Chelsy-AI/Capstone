# Weather Dashboard

A comprehensive desktop weather application built with Python and CustomTkinter, featuring real-time weather data, interactive visualizations, and multilingual support.

## Features

### Core Weather Information

- **Real-time Weather Data**: Current conditions with detailed metrics including temperature, humidity, wind speed, pressure, visibility, UV index, and precipitation
- **7-Day Historical Tracking**: Complete historical weather data with intelligent caching and CSV persistence
- **Temperature Unit Toggle**: Switch between Celsius and Fahrenheit with a simple click
- **Weather Prediction**: Tomorrow's temperature prediction with confidence scoring and accuracy tracking

### User Interface & Experience

- **Dynamic Themes**: Light/dark mode toggle with persistent preferences
- **Multilingual Support**: Full internationalization with English, Spanish, and Hindi translations
- **Responsive Design**: Pagiated interface supporting content expansion across different screen sizes
- **Weather Animations**: Real-time particle-based animations matching current conditions (rain, snow, storms, clouds)

### Advanced Features

- **Interactive Weather Map**: Real-time city locations with weather overlays and OpenStreetMap integration
- **City Comparison**: Side-by-side weather comparison between multiple cities
- **Weather Graphs**: Interactive data visualizations with hover tooltips
- **Sun & Moon Phases**: Detailed astronomical information including sunrise, sunset, and lunar phases
- **Weather Quiz**: Educational quiz system with comprehensive question database
- **Custom Weather Icons**: Multi-tier icon system with API, canvas, and emoji fallbacks

## Installation

### Prerequisites

- Python 3.8 or higher
- Internet connection for real-time weather data

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/Chelsy-AI/Capstone.git
   cd weather-dashboard
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. (Optional) Install enhanced map features:
   ```bash
   pip install tkintermapview
   ```

## Usage

### Quick Start

```bash
python main.py
```

### Basic Operations

- **Search Weather**: Enter any city name in the search box
- **Toggle Units**: Click the temperature label to switch between °C and °F
- **Change Text Theme**: Use the text theme toggle button for light/dark mode
- **View History**: Scroll down to access 7-day historical data
- **Compare Cities**: Use the city comparison feature for side-by-side analysis
- **Interactive Map**: Explore the weather map with real-time location markers

### Language Selection

On first launch, select your preferred language from English, Spanish, or Hindi. The selection is saved and applied to all interface elements.

## Project Architecture

```
weather-dashboard/
├── config/                 # Core application configuration
│   ├── animations.py      # Weather animation system
│   ├── api.py             # Weather API integration
│   ├── error_handler.py   # Comprehensive error handling
│   ├── storage.py         # CSV data persistence
│   ├── themes.py          # Theme management
│   ├── utils.py           # Utility functions
│   └── weather_app.py     # Main application class
├── features/              # Modular feature implementations
│   ├── city_comparison/   # Multi-city weather comparison
│   ├── graphs/            # Interactive data visualizations
│   ├── history_tracker/   # Historical data management
│   ├── interactive_map/   # Map integration and controls
│   ├── sun_moon_phases/   # Astronomical data and calculations
│   ├── theme_switcher/    # Dynamic theme switching
│   ├── tomorrows_guess/   # Weather prediction algorithms
│   ├── weather_icons/     # Custom icon system
│   └── weather_quiz/      # Educational quiz system
├── gui/                   # User interface components
│   ├── animation_controller.py
│   ├── main_gui.py
│   └── weather_display.py
├── language/              # Internationalization system
│   ├── controller.py      # Language management
│   ├── translations.py    # Translation data
│   └── utils.py           # Language utilities
├── data/                  # Local data storage
├── docs/                  # Project documentation
└── tests/                 # Comprehensive test suite
```

## API Integration

The application integrates with multiple free APIs:

- **OpenWeatherMap API**: Current weather data and weather icons
- **Open-Meteo API**: Primary weather data source
- **Open-Meteo Geocoding**: City name to coordinates conversion
- **Open-Meteo Archive**: Historical weather data
- **OpenStreetMap Nominatim**: Backup geocoding for map features
- **Sunrise-Sunset API**: Astronomical data for sun and moon phases

## Technical Highlights

### Modular Design

- Feature-based architecture with clear separation of concerns
- Each feature is self-contained and independently testable
- Plugin-style architecture allows easy addition of new features

### Data Management

- CSV-based persistence for weather history and user preferences
- Intelligent caching system to minimize API calls
- Data validation and error recovery mechanisms

### Performance Optimizations

- Efficient particle system for smooth 30fps animations
- Lazy loading of non-essential components
- Memory-conscious data structures for historical data

### Error Handling

- Comprehensive error handling with user-friendly messages
- Graceful degradation when optional features are unavailable
- Network failure recovery and retry mechanisms

## Testing

Run the complete test suite:
```bash
pytest tests/
```

## Dependencies

### Core Dependencies

- `customtkinter>=5.2.0` - Modern GUI framework
- `requests>=2.31.0` - HTTP API communication
- `Pillow>=10.0.0` - Image processing for weather icons

### Optional Dependencies

- `tkintermapview>=1.29` - Interactive map functionality
- `pytest>=7.4.0` - Testing framework

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

### Development Guidelines

- Follow PEP 8 style guidelines
- Add tests for new features
- Update documentation for API changes
- Ensure cross-platform compatibility

## Troubleshooting

### Common Issues

**Map not displaying**: Install `tkintermapview` or the app will use a fallback interface.

**No weather data**: Check internet connection and verify city name spelling.

**Animation performance**: Disable animations in settings if experiencing performance issues.

**Language not switching**: Restart the application after changing language preferences.

## System Requirements

- **Operating System**: Windows 10+, macOS 10.14+, or Linux with GUI support
- **Python**: Version 3.8 or higher
- **RAM**: Minimum 4GB (8GB recommended for optimal performance)
- **Storage**: 100MB free space for application and data files
- **Network**: Internet connection required for real-time weather data

## Acknowledgments

- Weather data provided by [Open-Meteo](https://open-meteo.com/)
- Map services powered by [OpenStreetMap](https://www.openstreetmap.org/)
- Icons and animations inspired by modern weather applications
- Built with [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)

## Version History

- **v2.0.0** - Complete rewrite with modular architecture, multilingual support, and advanced features
- **v1.5.0** - Added interactive maps and weather animations
- **v1.0.0** - Initial release with basic weather functionality

---

For more information, bug reports, or feature requests, please visit our [GitHub repository](https://github.com/Chelsy-AI/Capstone.git) or contact the development team.