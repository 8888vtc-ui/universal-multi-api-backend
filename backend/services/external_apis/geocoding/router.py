"""
Geocoding Router with Intelligent Fallback
"""
import logging
from typing import Dict, Any
import asyncio

logger = logging.getLogger(__name__)


class GeocodingRouter:
    """Router for geocoding with fallback"""
    
    def __init__(self):
        self.providers = []
        self._init_providers()
    
    def _init_providers(self):
        """Initialize geocoding providers"""
        from .providers import Nominatim, OpenCage, Positionstack
        import os
        
        # Nominatim (always available, but 1 req/sec limit)
        try:
            self.providers.append({
                'name': 'nominatim',
                'instance': Nominatim()
            })
            logger.info("✅ Nominatim (OSM) geocoding initialized")
        except Exception as e:
            logger.warning(f"⚠️ Nominatim failed: {e}")
        
        # OpenCage
        if os.getenv('OPENCAGE_API_KEY'):
            try:
                self.providers.append({
                    'name': 'opencage',
                    'instance': OpenCage()
                })
                logger.info("✅ OpenCage geocoding initialized")
            except Exception as e:
                logger.warning(f"⚠️ OpenCage failed: {e}")
        
        # Positionstack
        if os.getenv('POSITIONSTACK_API_KEY'):
            try:
                self.providers.append({
                    'name': 'positionstack',
                    'instance': Positionstack()
                })
                logger.info("✅ Positionstack geocoding initialized")
            except Exception as e:
                logger.warning(f"⚠️ Positionstack failed: {e}")
    
    async def geocode(self, address: str) -> Dict[str, Any]:
        """Geocode address with fallback"""
        errors = []
        
        for provider in self.providers:
            name = provider['name']
            instance = provider['instance']
            
            try:
                logger.info(f"🔄 Geocoding with {name}...")
                
                # Respect Nominatim rate limit (1 req/sec)
                if name == 'nominatim':
                    await asyncio.sleep(1)
                
                result = await instance.geocode(address)
                
                logger.info(f"✅ Geocoded with {name}")
                return {
                    **result,
                    "provider": name
                }
            
            except Exception as e:
                logger.warning(f"⚠️ {name} failed: {str(e)}")
                errors.append(f"{name}: {str(e)}")
                continue
        
        error_msg = f"All geocoding providers failed. Errors: {'; '.join(errors)}"
        logger.error(f"❌ {error_msg}")
        raise Exception(error_msg)
    
    async def reverse_geocode(self, lat: float, lon: float) -> Dict[str, Any]:
        """Reverse geocode with fallback"""
        errors = []
        
        for provider in self.providers:
            name = provider['name']
            instance = provider['instance']
            
            try:
                logger.info(f"🔄 Reverse geocoding with {name}...")
                
                # Respect Nominatim rate limit
                if name == 'nominatim':
                    await asyncio.sleep(1)
                
                result = await instance.reverse_geocode(lat, lon)
                
                logger.info(f"✅ Reverse geocoded with {name}")
                return {
                    **result,
                    "provider": name,
                    "lat": lat,
                    "lon": lon
                }
            
            except Exception as e:
                logger.warning(f"⚠️ {name} failed: {str(e)}")
                errors.append(f"{name}: {str(e)}")
                continue
        
        error_msg = f"All geocoding providers failed. Errors: {'; '.join(errors)}"
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
