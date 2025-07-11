# Weather Dashboard Capstone Project

## Overview:
- Desktop weather app using Python and CustomTkinter
- Fetches real-time and 7-day historical weather data via Open-Meteo API (no API key needed)
- Supports light/dark themes toggle
- Temperature toggle between Celsius and Fahrenheit by clicking temperature label
- Shows detailed metrics: humidity, wind, pressure, visibility, UV index, pollen, precipitation, bugs
- Predicts tomorrow’s temperature with confidence and accuracy tracking
- Saves weather history and prediction accuracy locally as CSV files
- Custom canvas-based weather icons for different conditions
- User-friendly error handling and clear messages

## Installation:
- Clone repo: git clone https://github.com/Chelsy-AI/Capstone.git
- cd weather-dashboard
- Create and activate virtual environment
- Install dependencies: pip install -r requirements.txt

## Usage:
- Run app: python main.py
- Enter city name to get weather data
- Click temperature label to toggle between °C and °F
- Toggle light/dark theme with button
- View tomorrow’s prediction and confidence display
- Access 7-day historical weather data saved locally

## Testing:
- Run tests with: pytest tests/
- Includes tests for API, GUI, prediction logic, and utilities

## Dependencies:
- Python 3.8+
- CustomTkinter
- requests
- pytest


