"""
Weather API Providers
Open-Meteo (unlimited), WeatherAPI (1M/month)
"""
import os
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime

logger = logging.getLogger(__name__)


class OpenMeteo:
    """Open-Meteo - Free unlimited weather API"""
    
    def __init__(self):
        self.base_url = "https://api.open-meteo.com/v1"
        self.available = True
        logger.info("✅ OpenMeteo weather provider initialized")
    
    async def get_current_weather(
        self,
        latitude: float,
        longitude: float
    ) -> Dict[str, Any]:
        """Get current weather for coordinates"""
        from services.http_client import http_client
        
        url = f"{self.base_url}/forecast"
        params = {
            'latitude': latitude,
            'longitude': longitude,
            'current_weather': 'true'
        }
        
        try:
            response = await http_client.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            current = data['current_weather']
            
            return {
                'temperature': current['temperature'],
                'windspeed': current['windspeed'],
                'winddirection': current['winddirection'],
                'weathercode': current['weathercode'],
                'time': current['time']
            }
        except Exception as e:
            logger.error(f"OpenMeteo current weather error: {e}")
            raise
    
    async def get_forecast(
        self,
        latitude: float,
        longitude: float,
        days: int = 7
    ) -> Dict[str, Any]:
        """Get weather forecast"""
        from services.http_client import http_client
        
        url = f"{self.base_url}/forecast"
        params = {
            'latitude': latitude,
            'longitude': longitude,
            'daily': 'temperature_2m_max,temperature_2m_min,precipitation_sum,weathercode',
            'forecast_days': min(days, 16),
            'timezone': 'auto'
        }
        
        try:
            response = await http_client.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            daily = data['daily']
            
            forecast = []
            for i in range(len(daily['time'])):
                forecast.append({
                    'date': daily['time'][i],
                    'temp_max': daily['temperature_2m_max'][i],
                    'temp_min': daily['temperature_2m_min'][i],
                    'precipitation': daily['precipitation_sum'][i],
                    'weathercode': daily['weathercode'][i]
                })
            
            return {
                'forecast': forecast,
                'timezone': data['timezone']
            }
        except Exception as e:
            logger.error(f"OpenMeteo forecast error: {e}")
            raise


class WeatherAPI:
    """WeatherAPI.com - 1M calls/month free"""
    
    def __init__(self):
        self.api_key = os.getenv('WEATHERAPI_KEY')
        if not self.api_key:
            raise ValueError("WEATHERAPI_KEY not found")
        
        self.base_url = "https://api.weatherapi.com/v1"
        self.available = True
        logger.info("✅ WeatherAPI provider initialized")
    
    async def get_current_weather(
        self,
        latitude: float,
        longitude: float
    ) -> Dict[str, Any]:
        """Get current weather"""
        from services.http_client import http_client
        
        url = f"{self.base_url}/current.json"
        params = {
            'key': self.api_key,
            'q': f"{latitude},{longitude}"
        }
        
        try:
            response = await http_client.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            current = data['current']
            
            return {
                'temperature': current['temp_c'],
                'windspeed': current['wind_kph'],
                'winddirection': current['wind_degree'],
                'condition': current['condition']['text'],
                'humidity': current['humidity'],
                'feels_like': current['feelslike_c']
            }
        except Exception as e:
            logger.error(f"WeatherAPI current weather error: {e}")
            raise
    
    async def get_forecast(
        self,
        latitude: float,
        longitude: float,
        days: int = 7
    ) -> Dict[str, Any]:
        """Get weather forecast"""
        from services.http_client import http_client
        
        url = f"{self.base_url}/forecast.json"
        params = {
            'key': self.api_key,
            'q': f"{latitude},{longitude}",
            'days': min(days, 10)
        }
        
        try:
            response = await http_client.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            forecast_data = data['forecast']['forecastday']
            
            forecast = []
            for day in forecast_data:
                forecast.append({
                    'date': day['date'],
                    'temp_max': day['day']['maxtemp_c'],
                    'temp_min': day['day']['mintemp_c'],
                    'precipitation': day['day']['totalprecip_mm'],
                    'condition': day['day']['condition']['text']
                })
            
            return {
                'forecast': forecast,
                'location': data['location']['name']
            }
        except Exception as e:
            logger.error(f"WeatherAPI forecast error: {e}")
            raise
