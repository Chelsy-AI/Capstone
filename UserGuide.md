# User Guide: Weather Dashboard

## Overview

The Weather Dashboard is a comprehensive desktop application that provides real-time weather data, interactive visualizations, and advanced features to help you understand weather patterns and plan your activities. This guide explains how to use each feature effectively.

## Getting Started

### First Launch Setup

When you first open the Weather Dashboard, you'll be guided through initial setup:

1. **Language Selection**: Choose from English, Spanish, or Hindi
2. **Text Theme Preference**: Select light or dark text

Your preferences are automatically saved for future sessions.

## Core Features

### Weather Search and Display

The main dashboard provides comprehensive current weather information.

**How to search for weather:**
1. Enter any city name in the search box at the top
2. Press Enter
3. Current conditions appear instantly with detailed metrics

**Current weather includes:**
- Temperature
- Humidity and atmospheric pressure
- Wind speed and direction
- Visibility and UV index
- Precipitation data

### Temperature Unit Toggle

Switch between temperature units with a simple click.

**To change units:**
1. Click on any temperature display
2. Units toggle between Celsius (°C) and Fahrenheit (°F)
3. All temperature displays update instantly
4. Your preference is automatically saved

## Advanced Visualizations

### Interactive Weather Graphs

View weather data trends with dynamic, interactive charts.

**Features:**
- **Hover tooltips**: Get exact values by hovering over data points
- **Multiple metrics**: Temperature, humidity, pressure, and more

**How to use:**
1. Navigate to the Graphs section  
2. Select the desired graph type from the dropdown menu  
3. Hover over any data point to view detailed information  
4. Click on [i] for additional insights and explanations  

### Historical Weather Tracking

Access 7 days of historical weather data with intelligent caching.

**What you can track:**
- Daily high and low temperatures  
- Changes in weather conditions  
- Average temperature for each day  

**Navigation:**
1. Compare weather patterns across multiple days  
2. View cached data automatically when offline

## Interactive Features

### Weather Map Integration

Explore weather patterns with the interactive map feature.

**Map features:**
- Real-time city location markers
- Weather overlay information
- OpenStreetMap integration

**How to use the map:**
1. Click the map button
2. Navigate by clicking and dragging
3. Zoom with mouse wheel or +/- buttons
4. Click any location to get weather for that area

*Note: Enhanced map features require tkintermapview installation*

### City Comparison Tool

Compare weather conditions between multiple cities side-by-side.

**Setting up comparisons:**
1. Access the city comparison feature
2. Add cities using the search function
3. View side-by-side weather data
4. Compare metrics like temperature, humidity, and conditions

**Best uses:**
- Travel planning
- Climate research
- Relocating decisions
- Weather pattern analysis

### Weather Animations

Experience real-time particle-based animations that match current conditions.

**Animation types:**
- **Rain**: Animated raindrops for rainy conditions
- **Snow**: Falling snowflakes during snow
- **Storm**: Dynamic lightning effects
- **Clouds**: Drifting cloud particles
- **Clear**: Subtle atmospheric effects

**Performance options:**
- Animations run at smooth 30fps
- Automatically adjust based on system capabilities

## Astronomical Information

### Sun and Moon Phases

Get detailed astronomical data for any location.

**Available information:**
- Sunrise and sunset times
- Current moon phase with visual representation
- Moonrise and moonset times
- Solar noon and day length
- Astronomical twilight times

**How to access:**
1. Look for the sun/moon section in the main interface
2. Data updates automatically with location changes
3. Times are shown in local timezone

## Educational Features

### Weather Quiz System

Test and expand your weather knowledge with the built-in quiz.

**Quiz Features:**
- Based on meteorological data from five major global cities: Phoenix, Ahmedabad, Denver, Columbus, and Lebrija  
- Covers climate patterns, temperature variations, and weather phenomena  
- Designed to test and improve your weather knowledge  
- Displays results instantly after each quiz  

**How to take a quiz:**
1. Click on the Quiz section  
2. Answer the questions and receive your result instantly  
3. Click the "New Quiz" button to try again  


## Prediction and Forecasting

### Tomorrow's Weather Prediction

Get intelligent weather predictions with confidence scoring.

**Prediction features:**
- Tomorrow's temperature forecast
- Confidence score based on historical accuracy
- Prediction accuracy tracking
- Algorithm transparency

**Understanding predictions:**
- Higher confidence scores indicate more reliable forecasts
- Predictions improve with more historical data

## Customization and Themes

### Dynamic Text Theme Switching

Switch between light and dark texts to match your preference or time of day.

**Available text themes:**
- **Light Mode** – Black text on white for clear daytime viewing  
- **Dark Mode** – White text on dark for comfortable low-light use  

**To change themes:**
1. Locate the theme toggle button
2. Click to switch between light and dark modes
3. Theme preference is automatically saved
4. All interface elements update instantly

### Language Support

The application supports full internationalization with multiple languages.

**Supported languages:**
- English (default)
- Spanish (Español)
- Hindi (हिन्दी)

**To change language:**
1. Go to language button
2. Select your preferred language
3. Interface text updates immediately

## Data Export and Sharing

### Weather Icons and Visual Elements

The application uses a sophisticated multi-tier icon system.

**Icon features:**
- API-sourced weather icons for accuracy
- Custom canvas-drawn icons as backup
- Emoji fallbacks for maximum compatibility
- Consistent visual representation

## Performance and Optimization

### Memory and CPU Efficiency

The application is designed for optimal performance:

**Optimization features:**
- Intelligent caching reduces API calls
- Lazy loading of non-essential components
- Memory-conscious data structures
- Efficient 30fps animation system

**Performance tips:**
- Close unused features when not needed
- Disable animations on older hardware
- Clear cache periodically through settings
- Ensure stable internet connection for best experience

## Troubleshooting

### Common Issues and Solutions

**Application won't start:**
- Verify Python 3.8+ is installed
- Check all dependencies are installed: `pip install -r requirements.txt`
- Ensure no firewall is blocking the application

**No weather data displaying:**
- Check internet connection
- Verify city name spelling
- Try searching for a different location
- Check application logs for error messages

**Map not displaying:**
- Install optional map features: `pip install tkintermapview`
- Application will use fallback interface without this package
- Restart application after installation

**Animation performance issues:**
- Close other resource-intensive applications
- Update graphics drivers
- Reduce visual effects in system settings

**Language not switching:**
- Verify language files are properly installed
- Check for system locale compatibility

### Error Recovery

The application includes comprehensive error handling:

- **Network failures**: Automatic retry mechanisms
- **API unavailability**: Graceful degradation to cached data
- **Data corruption**: Automatic data validation and recovery
- **Missing features**: Fallback options for optional components

## Tips and Best Practices

### Maximizing Accuracy

**For best weather data:**
- Use specific city names rather than general areas
- Verify location accuracy when searching
- Check multiple data sources when planning important activities
- Understand that forecasts become less accurate over longer periods

### Efficient Usage

**Performance optimization:**
- Limit historical data requests to needed timeframes
- Close unused features to conserve system resources
- Use cached data when available to reduce API calls
- Regular application updates ensure optimal performance

### Data Interpretation

**Understanding weather patterns:**
- Look for trends rather than focusing on individual readings
- Compare current conditions with historical averages
- Consider multiple metrics together for comprehensive understanding
- Use comparison tools to understand regional differences

## Advanced Features

### Custom Configurations

Power users can customize various aspects:

**Available customizations:**
- Animation settings and performance
- Data refresh intervals
- Display preferences
- Cache management options

### API Integration Understanding

The application uses multiple weather APIs for comprehensive data:

- **Primary data**: Open-Meteo API for current conditions
- **Historical data**: Open-Meteo Archive
- **Geocoding**: Multiple services for accurate location finding
- **Astronomical data**: Specialized APIs for sun/moon information

### Data Persistence

**How your data is stored:**
- Weather history in CSV format for portability
- User preferences in configuration files
- Cache data for offline functionality
- No personal data is transmitted or stored remotely

## Keyboard Shortcuts

### Navigation Shortcuts

| Shortcut | Action |
|----------|--------|
| `Enter` | Search for weather (when in search box) |
| `Ctrl+R` | Refresh current weather data |
| `Ctrl+L` | Focus on location search box |
| `Tab` | Navigate between interface elements |
| `Esc` | Close dialogs or return to main view |

### Feature Shortcuts

| Shortcut | Action |
|----------|--------|
| `F11` | Toggle fullscreen mode |
| `Ctrl+T` | Toggle between light/dark themes |
| `Ctrl+M` | Open/close interactive map |
| `Ctrl+H` | View historical data |
| `Ctrl+Q` | Quit application |

## Getting Help

### Additional Resources

- **GitHub Repository**: [Weather Dashboard](https://github.com/Chelsy-AI/Capstone.git)
- **Issue Tracking**: Report bugs or request features
- **Documentation**: Additional technical documentation in `/docs`

### Support Information

When seeking help, please provide:
- Operating system and version
- Python version
- Error messages or logs
- Steps to reproduce the issue
- Screenshots when relevant

### Installation Help

**If you encounter installation issues:**

```bash
# Check Python version
python --version

# Reinstall dependencies
pip uninstall -r requirements.txt -y
pip install -r requirements.txt

# Clear cache and restart
rm -rf __pycache__
python main.py
```

**For Windows users:**
```cmd
# If you see SSL errors
pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org -r requirements.txt
```

**For macOS users:**
```bash
# If you see permission errors
pip install --user -r requirements.txt
```

**For Linux users:**
```bash
# Install system dependencies
sudo apt-get update
sudo apt-get install python3-tk python3-dev

# Then install Python requirements
pip install -r requirements.txt
```

### Performance Troubleshooting

**If the application runs slowly:**

1. **Check system requirements:**
   - 4GB RAM minimum (8GB recommended)
   - Python 3.8+ installed
   - Stable internet connection

2. **Optimize performance:**
   ```bash
   # Disable animations
   export ENABLE_ANIMATIONS=false
   
   # Reduce cache size
   export MAX_CACHE_SIZE=100
   
   # Lower animation framerate
   export ANIMATION_FPS=15
   ```

3. **Close other applications:**
   - Close unnecessary programs
   - Check for background processes using CPU
   - Ensure adequate free disk space

### Data and Privacy

**What data is stored:**
- Weather history (locally in CSV files)
- User preferences (language, theme, default city)
- Temporary cache files for performance

**What data is NOT stored:**
- Personal information
- Location tracking
- Usage analytics
- Any data sent to third parties

**Clearing data:**
```bash
# Remove all cached data
rm -rf data/cache/

# Reset user preferences
rm language_settings.json

# Clear weather history
rm data/weather_history.csv
```

---

*This guide covers the main features of Weather Dashboard. For technical documentation, see the [README](README.md) or visit our [GitHub repository](https://github.com/Chelsy-AI/Capstone.git).*