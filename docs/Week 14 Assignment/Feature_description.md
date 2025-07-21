## What it is:

- Comprehensive 7-Day Weather History Tracker that automatically fetches and displays historical weather data for any searched city

## How it works:

- Integrates with Open-Meteo Archive API to retrieve detailed temperature data (maximum, minimum, and average) for the past seven days

- Intelligently caches data to improve performance and reduce API calls

- Processes and displays information in a responsive grid layout with automatic temperature unit conversion

- Saves all historical data to CSV files for long-term pattern analysis

## Known bugs/limitations:

- Graceful degradation when historical data is unavailable from API
- Limited to 7-day history period 

