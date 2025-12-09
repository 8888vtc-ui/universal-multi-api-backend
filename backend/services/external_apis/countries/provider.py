"""RestCountries Provider - Free country information API"""
import httpx
from typing import Dict, Any, List, Optional


class RestCountriesProvider:
    """Provider for RestCountries API - Free, no API key required"""
    
    BASE_URL = "https://restcountries.com/v3.1"
    
    def __init__(self):
        self.timeout = 10.0
    
    async def get_all_countries(self) -> List[Dict[str, Any]]:
        """Get all countries"""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(f"{self.BASE_URL}/all")
                
                if response.status_code == 200:
                    countries = response.json()
                    return [self._format_country(c) for c in countries[:100]]  # Limit to 100
                return []
        except Exception as e:
            print(f"RestCountries error: {e}")
            return []
    
    async def search_countries(self, query: str) -> List[Dict[str, Any]]:
        """Search countries by name"""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(f"{self.BASE_URL}/name/{query}")
                
                if response.status_code == 200:
                    countries = response.json()
                    return [self._format_country(c) for c in countries[:10]]
                return []
        except Exception as e:
            print(f"RestCountries search error: {e}")
            return []
    
    async def get_country_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """Get country by exact name"""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(f"{self.BASE_URL}/name/{name}?fullText=true")
                
                if response.status_code == 200:
                    countries = response.json()
                    if countries:
                        return self._format_country(countries[0])
                return None
        except Exception as e:
            print(f"RestCountries get error: {e}")
            return None
    
    async def get_country_by_code(self, code: str) -> Optional[Dict[str, Any]]:
        """Get country by alpha code (2 or 3 letters)"""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(f"{self.BASE_URL}/alpha/{code}")
                
                if response.status_code == 200:
                    data = response.json()
                    countries = data if isinstance(data, list) else [data]
                    if countries:
                        return self._format_country(countries[0])
                return None
        except Exception as e:
            print(f"RestCountries code error: {e}")
            return None
    
    async def get_countries_by_region(self, region: str) -> List[Dict[str, Any]]:
        """Get countries by region"""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(f"{self.BASE_URL}/region/{region}")
                
                if response.status_code == 200:
                    countries = response.json()
                    return [self._format_country(c) for c in countries]
                return []
        except Exception as e:
            print(f"RestCountries region error: {e}")
            return []
    
    async def get_countries_by_currency(self, currency: str) -> List[Dict[str, Any]]:
        """Get countries by currency code"""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(f"{self.BASE_URL}/currency/{currency}")
                
                if response.status_code == 200:
                    countries = response.json()
                    return [self._format_country(c) for c in countries]
                return []
        except Exception as e:
            print(f"RestCountries currency error: {e}")
            return []
    
    def _format_country(self, country: Dict) -> Dict[str, Any]:
        """Format country data"""
        currencies = country.get("currencies", {})
        currency_list = list(currencies.keys()) if currencies else []
        
        languages = country.get("languages", {})
        language_list = list(languages.values()) if languages else []
        
        return {
            "name": country.get("name", {}).get("common", "Unknown"),
            "official_name": country.get("name", {}).get("official", "Unknown"),
            "capital": country.get("capital", [None])[0] if country.get("capital") else None,
            "region": country.get("region"),
            "subregion": country.get("subregion"),
            "population": country.get("population", 0),
            "area": country.get("area"),
            "currencies": currency_list,
            "languages": language_list,
            "flag_emoji": country.get("flag", ""),
            "flag_url": country.get("flags", {}).get("png"),
            "alpha2": country.get("cca2"),
            "alpha3": country.get("cca3"),
            "timezones": country.get("timezones", []),
        }
