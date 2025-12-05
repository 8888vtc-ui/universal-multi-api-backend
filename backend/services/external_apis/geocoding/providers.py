"""
Geocoding Providers
Nominatim (OSM), OpenCage, Positionstack
"""
import os
import logging
from typing import Dict, Any, Optional, List

logger = logging.getLogger(__name__)


class Nominatim:
    """Nominatim (OpenStreetMap) - Free geocoding (1 req/sec limit)"""
    
    def __init__(self):
        self.base_url = "https://nominatim.openstreetmap.org"
        self.available = True
        self.headers = {
            'User-Agent': 'UniversalBackendAPI/4.0'
        }
        logger.info("✅ Nominatim geocoding provider initialized")
    
    async def geocode(self, address: str) -> Dict[str, Any]:
        """Convert address to coordinates"""
        from services.http_client import http_client
        
        url = f"{self.base_url}/search"
        params = {
            'q': address,
            'format': 'json',
            'limit': 1
        }
        
        try:
            response = await http_client.get(url, params=params, headers=self.headers)
            response.raise_for_status()
            
            results = response.json()
            
            if not results:
                raise Exception(f"No results found for address: {address}")
            
            result = results[0]
            return {
                'lat': float(result['lat']),
                'lon': float(result['lon']),
                'display_name': result.get('display_name', ''),
                'address': result.get('address', {})
            }
        except Exception as e:
            logger.error(f"Nominatim geocode error: {e}")
            raise
    
    async def reverse_geocode(self, lat: float, lon: float) -> Dict[str, Any]:
        """Convert coordinates to address"""
        from services.http_client import http_client
        
        url = f"{self.base_url}/reverse"
        params = {
            'lat': lat,
            'lon': lon,
            'format': 'json'
        }
        
        try:
            response = await http_client.get(url, params=params, headers=self.headers)
            response.raise_for_status()
            
            result = response.json()
            
            return {
                'display_name': result.get('display_name', ''),
                'address': result.get('address', {})
            }
        except Exception as e:
            logger.error(f"Nominatim reverse geocode error: {e}")
            raise


class OpenCage:
    """OpenCage Geocoder - Free 2,500/day"""
    
    def __init__(self):
        self.api_key = os.getenv('OPENCAGE_API_KEY')
        if not self.api_key:
            raise ValueError("OPENCAGE_API_KEY not found")
        
        self.base_url = "https://api.opencagedata.com/geocode/v1/json"
        self.available = True
        logger.info("✅ OpenCage geocoding provider initialized")
    
    async def geocode(self, address: str) -> Dict[str, Any]:
        """Convert address to coordinates"""
        from services.http_client import http_client
        
        params = {
            'key': self.api_key,
            'q': address,
            'limit': 1
        }
        
        try:
            response = await http_client.get(self.base_url, params=params)
            response.raise_for_status()
            
            data = response.json()
            results = data.get('results', [])
            
            if not results:
                raise Exception(f"No results found for address: {address}")
            
            result = results[0]
            geometry = result['geometry']
            
            return {
                'lat': geometry['lat'],
                'lon': geometry['lng'],
                'display_name': result.get('formatted', ''),
                'address': result.get('components', {})
            }
        except Exception as e:
            logger.error(f"OpenCage geocode error: {e}")
            raise
    
    async def reverse_geocode(self, lat: float, lon: float) -> Dict[str, Any]:
        """Convert coordinates to address"""
        from services.http_client import http_client
        
        params = {
            'key': self.api_key,
            'q': f"{lat},{lon}",
            'limit': 1
        }
        
        try:
            response = await http_client.get(self.base_url, params=params)
            response.raise_for_status()
            
            data = response.json()
            results = data.get('results', [])
            
            if not results:
                raise Exception(f"No results found for coordinates: {lat},{lon}")
            
            result = results[0]
            
            return {
                'display_name': result.get('formatted', ''),
                'address': result.get('components', {})
            }
        except Exception as e:
            logger.error(f"OpenCage reverse geocode error: {e}")
            raise


class Positionstack:
    """Positionstack - Free 25,000/month"""
    
    def __init__(self):
        self.api_key = os.getenv('POSITIONSTACK_API_KEY')
        if not self.api_key:
            raise ValueError("POSITIONSTACK_API_KEY not found")
        
        self.base_url = "http://api.positionstack.com/v1"
        self.available = True
        logger.info("✅ Positionstack geocoding provider initialized")
    
    async def geocode(self, address: str) -> Dict[str, Any]:
        """Convert address to coordinates"""
        from services.http_client import http_client
        
        url = f"{self.base_url}/forward"
        params = {
            'access_key': self.api_key,
            'query': address,
            'limit': 1
        }
        
        try:
            response = await http_client.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            results = data.get('data', [])
            
            if not results:
                raise Exception(f"No results found for address: {address}")
            
            result = results[0]
            
            return {
                'lat': result['latitude'],
                'lon': result['longitude'],
                'display_name': result.get('label', ''),
                'address': {
                    'country': result.get('country', ''),
                    'region': result.get('region', ''),
                    'locality': result.get('locality', '')
                }
            }
        except Exception as e:
            logger.error(f"Positionstack geocode error: {e}")
            raise
    
    async def reverse_geocode(self, lat: float, lon: float) -> Dict[str, Any]:
        """Convert coordinates to address"""
        from services.http_client import http_client
        
        url = f"{self.base_url}/reverse"
        params = {
            'access_key': self.api_key,
            'query': f"{lat},{lon}",
            'limit': 1
        }
        
        try:
            response = await http_client.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            results = data.get('data', [])
            
            if not results:
                raise Exception(f"No results found for coordinates: {lat},{lon}")
            
            result = results[0]
            
            return {
                'display_name': result.get('label', ''),
                'address': {
                    'country': result.get('country', ''),
                    'region': result.get('region', ''),
                    'locality': result.get('locality', '')
                }
            }
        except Exception as e:
            logger.error(f"Positionstack reverse geocode error: {e}")
            raise
