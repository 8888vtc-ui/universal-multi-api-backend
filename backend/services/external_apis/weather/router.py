"""
Weather Router with Intelligent Fallback
Supports: Open-Meteo, WeatherAPI
"""
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


class WeatherRouter:
    """Intelligent router for weather with automatic fallback"""
    
    def __init__(self):
        self.providers = []
        self._init_providers()
    
    def _init_providers(self):
        """Initialize available weather providers"""
        from .providers import OpenMeteo, WeatherAPI
        import os
        
        # Priority order (Open-Meteo first - unlimited)
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
        """Get current weather with automatic fallback"""
        errors = []
        
        for provider in self.providers:
            name = provider['name']
            instance = provider['instance']
            
            try:
                logger.info(f"🔄 Getting current weather from {name}...")
                result = await instance.get_current_weather(latitude, longitude)
                
                logger.info(f"✅ Weather data retrieved from {name}")
                return {
                    **result,
                    "provider": name
                }
            
            except Exception as e:
                logger.warning(f"⚠️ {name} failed: {str(e)}")
                errors.append(f"{name}: {str(e)}")
                continue
        
        error_msg = f"All weather providers failed. Errors: {'; '.join(errors)}"
        logger.error(f"❌ {error_msg}")
        raise Exception(error_msg)
    
    async def get_forecast(
        self,
        latitude: float,
        longitude: float,
        days: int = 7
    ) -> Dict[str, Any]:
        """Get weather forecast with automatic fallback"""
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
            "details": [
                {"name": p['name'], "available": True}
                for p in self.providers
            ]
        }
