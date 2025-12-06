"""
REST Countries API Provider
Free unlimited API for country information
"""
import httpx
from typing import Dict, Any, Optional, List


class RestCountriesProvider:
    """REST Countries API - Unlimited free"""
    
    BASE_URL = "https://restcountries.com/v3.1"
    
    async def get_all_countries(self) -> List[Dict[str, Any]]:
        """Get all countries"""
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Use fields to reduce payload size
            response = await client.get(
                f"{self.BASE_URL}/all",
                params={"fields": "name,capital,population,region,flags,cca2,cca3"}
            )
            if response.status_code == 200:
                return response.json()
            raise Exception(f"REST Countries returned status {response.status_code}")
    
    async def get_country_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """Get country by name"""
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(f"{self.BASE_URL}/name/{name}")
            if response.status_code == 200:
                countries = response.json()
                return countries[0] if countries else None
            elif response.status_code == 404:
                return None
            raise Exception(f"REST Countries returned status {response.status_code}")
    
    async def get_country_by_code(self, code: str) -> Optional[Dict[str, Any]]:
        """Get country by alpha code (2 or 3 letters)"""
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(f"{self.BASE_URL}/alpha/{code}")
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                return None
            raise Exception(f"REST Countries returned status {response.status_code}")
    
    async def search_countries(self, query: str) -> List[Dict[str, Any]]:
        """Search countries by name"""
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(f"{self.BASE_URL}/name/{query}")
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                return []
            raise Exception(f"REST Countries returned status {response.status_code}")
    
    async def get_countries_by_region(self, region: str) -> List[Dict[str, Any]]:
        """Get countries by region"""
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(f"{self.BASE_URL}/region/{region}")
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                return []
            raise Exception(f"REST Countries returned status {response.status_code}")
    
    async def get_countries_by_currency(self, currency: str) -> List[Dict[str, Any]]:
        """Get countries by currency code"""
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(f"{self.BASE_URL}/currency/{currency}")
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                return []
            raise Exception(f"REST Countries returned status {response.status_code}")

