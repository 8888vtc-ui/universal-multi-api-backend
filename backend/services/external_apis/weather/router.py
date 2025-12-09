"""
Weather Router with Dual-API Precision
Calls both Open-Meteo and WeatherAPI in parallel for maximum accuracy
"""
import logging
import asyncio
import math
from typing import Dict, Any, Optional, Tuple

logger = logging.getLogger(__name__)


class WeatherRouter:
    """Intelligent router for weather - uses BOTH APIs for precision"""
    
    def __init__(self):
        self.providers = []
        self._init_providers()
    
    def _init_providers(self):
        """Initialize available weather providers"""
        from .providers import OpenMeteo, WeatherAPI
        import os
        
        # Both providers
        potential_providers = [
            ('open_meteo', OpenMeteo, True),  # Always available
            ('weatherapi', WeatherAPI, os.getenv('WEATHERAPI_KEY'))
        ]
        
        for name, provider_class, condition in potential_providers:
            if condition:
                try:
                    provider = provider_class()
                    self.providers.append({
                        'name': name,
                        'instance': provider
                    })
                    logger.info(f"✅ {name.replace('_', '-').upper()} weather provider initialized")
                except Exception as e:
                    logger.warning(f"⚠️ Failed to initialize {name}: {e}")
        
        if not self.providers:
            logger.error("❌ No weather providers available!")
    
    async def get_current_weather(
        self,
        latitude: float,
        longitude: float
    ) -> Dict[str, Any]:
        """
        Get current weather from BOTH APIs in parallel for precision
        Aggregates data for maximum accuracy
        """
        # Appeler les 2 APIs en parallèle
        tasks = []
        provider_names = []
        
        for provider in self.providers:
            name = provider['name']
            instance = provider['instance']
            tasks.append(self._safe_fetch(instance, latitude, longitude))
            provider_names.append(name)
        
        # Exécuter en parallèle
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Collecter les données valides
        valid_data = {}
        for name, result in zip(provider_names, results):
            if result and not isinstance(result, Exception):
                valid_data[name] = result
                logger.info(f"✅ Weather data from {name}")
            else:
                logger.warning(f"⚠️ {name} failed: {result if isinstance(result, Exception) else 'No data'}")
        
        if not valid_data:
            raise Exception("All weather providers failed")
        
        # Si on a les 2 sources, agréger pour la précision
        if len(valid_data) >= 2:
            aggregated = self._aggregate_weather_data(valid_data)
            return aggregated
        
        # Sinon, retourner la seule source disponible
        provider_name = list(valid_data.keys())[0]
        data = valid_data[provider_name]
        data['provider'] = provider_name
        data['sources'] = [provider_name]
        data['precision_level'] = 'single_source'
        return data
    
    async def _safe_fetch(
        self,
        instance,
        latitude: float,
        longitude: float
    ) -> Optional[Dict]:
        """Fetch weather data safely (no exception thrown)"""
        try:
            return await instance.get_current_weather(latitude, longitude)
        except Exception as e:
            logger.debug(f"Provider fetch error: {e}")
            return None
    
    def _aggregate_weather_data(self, data_sources: Dict[str, Dict]) -> Dict[str, Any]:
        """
        Aggregate weather data from multiple sources for precision
        Calculates averages and precision metrics
        """
        open_meteo = data_sources.get('open_meteo', {})
        weatherapi = data_sources.get('weatherapi', {})
        
        # TEMPÉRATURE - Moyenne des 2 sources
        temp_om = open_meteo.get('temperature')
        temp_wa = weatherapi.get('temperature')
        
        if temp_om is not None and temp_wa is not None:
            temperature_avg = (temp_om + temp_wa) / 2
            temperature_precision = abs(temp_om - temp_wa)
        else:
            temperature_avg = temp_om if temp_om is not None else temp_wa
            temperature_precision = None
        
        # VENT - Vitesse moyenne
        wind_om = open_meteo.get('windspeed')
        wind_wa = weatherapi.get('windspeed')
        
        if wind_om is not None and wind_wa is not None:
            windspeed_avg = (wind_om + wind_wa) / 2
            windspeed_precision = abs(wind_om - wind_wa)
        else:
            windspeed_avg = wind_om if wind_om is not None else wind_wa
            windspeed_precision = None
        
        # DIRECTION VENT - Moyenne circulaire (gère 0/360)
        dir_om = open_meteo.get('winddirection')
        dir_wa = weatherapi.get('winddirection')
        
        if dir_om is not None and dir_wa is not None:
            winddirection_avg = self._circular_mean([dir_om, dir_wa])
        else:
            winddirection_avg = dir_om if dir_om is not None else dir_wa
        
        # Calculer le niveau de précision
        if temperature_precision is not None:
            if temperature_precision < 1.0:
                precision_level = 'high'
            elif temperature_precision < 2.0:
                precision_level = 'medium'
            else:
                precision_level = 'low'
        else:
            precision_level = 'single_source'
        
        return {
            # Température précise
            'temperature': round(temperature_avg, 1) if temperature_avg else None,
            'temperature_sources': {
                'open_meteo': temp_om,
                'weatherapi': temp_wa,
                'precision': round(temperature_precision, 1) if temperature_precision else None
            },
            
            # Vent précis
            'windspeed': round(windspeed_avg, 1) if windspeed_avg else None,
            'windspeed_sources': {
                'open_meteo': wind_om,
                'weatherapi': wind_wa,
                'precision': round(windspeed_precision, 1) if windspeed_precision else None
            },
            
            # Direction vent
            'winddirection': round(winddirection_avg) if winddirection_avg else None,
            'winddirection_sources': {
                'open_meteo': dir_om,
                'weatherapi': dir_wa
            },
            
            # Données complémentaires (WeatherAPI uniquement)
            'humidity': weatherapi.get('humidity'),
            'feels_like': weatherapi.get('feels_like'),
            'pressure': weatherapi.get('pressure'),
            'gust': weatherapi.get('gust'),
            'condition': weatherapi.get('condition') or open_meteo.get('condition'),
            'weathercode': open_meteo.get('weathercode'),
            
            # Métadonnées
            'sources': ['Open-Meteo', 'WeatherAPI'],
            'provider': 'aggregated',
            'precision_level': precision_level
        }
    
    def _circular_mean(self, angles: list) -> float:
        """Calculate circular mean of angles (handles 0/360 wrap)"""
        if not angles:
            return 0
        
        sin_sum = sum(math.sin(math.radians(a)) for a in angles)
        cos_sum = sum(math.cos(math.radians(a)) for a in angles)
        
        mean_angle = math.degrees(math.atan2(sin_sum, cos_sum))
        if mean_angle < 0:
            mean_angle += 360
        
        return mean_angle
    
    async def get_forecast(
        self,
        latitude: float,
        longitude: float,
        days: int = 7
    ) -> Dict[str, Any]:
        """Get weather forecast (uses first available provider)"""
        errors = []
        
        for provider in self.providers:
            name = provider['name']
            instance = provider['instance']
            
            try:
                logger.info(f"🔄 Getting forecast from {name}...")
                result = await instance.get_forecast(latitude, longitude, days)
                
                logger.info(f"✅ Forecast retrieved from {name}")
                return {
                    **result,
                    "provider": name,
                    "days": days
                }
            
            except Exception as e:
                logger.warning(f"⚠️ {name} failed: {str(e)}")
                errors.append(f"{name}: {str(e)}")
                continue
        
        error_msg = f"All weather providers failed. Errors: {'; '.join(errors)}"
        logger.error(f"❌ {error_msg}")
        raise Exception(error_msg)
    
    def get_status(self) -> Dict[str, Any]:
        """Get router status"""
        return {
            "providers": len(self.providers),
            "mode": "dual_api_precision",
            "details": [
                {"name": p['name'], "available": True}
                for p in self.providers
            ]
        }


def get_wind_direction_name(degrees: float) -> str:
    """Convert degrees to cardinal direction"""
    if degrees is None:
        return "N/A"
    directions = [
        "N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
        "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"
    ]
    index = int((degrees + 11.25) / 22.5) % 16
    return directions[index]


def format_weather_context(data: Dict, location: Dict = None) -> str:
    """Format weather data for AI context"""
    parts = []
    
    # Lieu
    if location:
        parts.append(f"[LIEU]: {location.get('name', 'Unknown')}, {location.get('country', '')}")
        parts.append(f"[COORDONNÉES]: {location.get('lat', '')}, {location.get('lon', '')}")
        parts.append("")
    
    # Température
    parts.append("🌡️ TEMPÉRATURE:")
    temp = data.get('temperature')
    parts.append(f"  • Actuelle: {temp}°C" if temp else "  • Non disponible")
    
    temp_sources = data.get('temperature_sources', {})
    if temp_sources.get('precision') is not None:
        parts.append(f"  • Précision: ±{temp_sources['precision']}°C")
        parts.append(f"  • Sources: Open-Meteo={temp_sources.get('open_meteo')}°C, WeatherAPI={temp_sources.get('weatherapi')}°C")
    
    if data.get('feels_like'):
        parts.append(f"  • Ressenti: {data['feels_like']}°C")
    
    parts.append("")
    
    # Vent
    parts.append("💨 VENT:")
    wind = data.get('windspeed')
    parts.append(f"  • Vitesse: {wind} km/h" if wind else "  • Non disponible")
    
    wind_sources = data.get('windspeed_sources', {})
    if wind_sources.get('precision') is not None:
        parts.append(f"  • Précision: ±{wind_sources['precision']} km/h")
    
    direction = data.get('winddirection')
    if direction is not None:
        direction_name = get_wind_direction_name(direction)
        parts.append(f"  • Direction: {direction}° ({direction_name})")
    
    if data.get('gust'):
        parts.append(f"  • Rafales: {data['gust']} km/h")
    
    parts.append("")
    
    # Conditions
    if data.get('condition'):
        parts.append(f"☁️ CONDITIONS: {data['condition']}")
    
    if data.get('humidity'):
        parts.append(f"💧 HUMIDITÉ: {data['humidity']}%")
    
    if data.get('pressure'):
        parts.append(f"📊 PRESSION: {data['pressure']} mb")
    
    parts.append("")
    
    # Sources
    sources = data.get('sources', [])
    precision = data.get('precision_level', 'unknown')
    if sources:
        parts.append(f"[SOURCES]: {' + '.join(sources)} (précision: {precision})")
    
    return "\n".join(parts)
