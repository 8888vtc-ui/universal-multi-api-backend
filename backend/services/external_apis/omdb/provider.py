"""
OMDB API Provider
1,000 requests/day free
"""
import httpx
import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()


class OMDBProvider:
    """OMDB API - 1,000 req/day free"""
    
    BASE_URL = "http://www.omdbapi.com"
    
    def __init__(self):
        self.api_key = os.getenv("OMDB_API_KEY", "")
        self.available = bool(self.api_key)
    
    async def search(self, query: str, year: Optional[str] = None) -> Dict[str, Any]:
        """Search movies/TV shows"""
        if not self.available:
            raise Exception("OMDB_API_KEY not configured")
        async with httpx.AsyncClient(timeout=30.0) as client:
            params = {
                "apikey": self.api_key,
                "s": query
            }
            if year:
                params["y"] = year
            
            response = await client.get(f"{self.BASE_URL}/", params=params)
            if response.status_code == 200:
                return response.json()
            raise Exception(f"OMDB returned status {response.status_code}")
    
    async def get_by_title(self, title: str, year: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Get movie/TV show by title"""
        if not self.available:
            raise Exception("OMDB_API_KEY not configured")
        async with httpx.AsyncClient(timeout=30.0) as client:
            params = {
                "apikey": self.api_key,
                "t": title
            }
            if year:
                params["y"] = year
            
            response = await client.get(f"{self.BASE_URL}/", params=params)
            if response.status_code == 200:
                result = response.json()
                if result.get("Response") == "True":
                    return result
                return None
            raise Exception(f"OMDB returned status {response.status_code}")
    
    async def get_by_id(self, imdb_id: str) -> Optional[Dict[str, Any]]:
        """Get movie/TV show by IMDb ID"""
        if not self.available:
            raise Exception("OMDB_API_KEY not configured")
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                f"{self.BASE_URL}/",
                params={
                    "apikey": self.api_key,
                    "i": imdb_id
                }
            )
            if response.status_code == 200:
                result = response.json()
                if result.get("Response") == "True":
                    return result
                return None
            raise Exception(f"OMDB returned status {response.status_code}")

