"""
Giphy API Provider
Free unlimited GIFs (with API key)
"""
import httpx
import os
from typing import Dict, Any, Optional, List
from dotenv import load_dotenv
from services.http_client import http_client

load_dotenv()


class GiphyProvider:
    """Giphy API - Unlimited free with API key"""
    
    BASE_URL = "https://api.giphy.com/v1"
    
    def __init__(self):
        self.api_key = os.getenv("GIPHY_API_KEY", "")
        if not self.api_key:
            # Giphy has a public beta key that works for limited use
            self.api_key = "dc6zaTOxFJmzC"  # Public beta key
    
    async def search(self, query: str, limit: int = 25, rating: str = "g") -> Dict[str, Any]:
        """Search GIFs"""
        response = await http_client.get(
            f"{self.BASE_URL}/gifs/search",
            params={
                "api_key": self.api_key,
                "q": query,
                "limit": limit,
                "rating": rating
            }
        )
        if response.status_code == 200:
            return response.json()
        raise Exception(f"Giphy returned status {response.status_code}")
    
    async def get_trending(self, limit: int = 25) -> Dict[str, Any]:
        """Get trending GIFs"""
        response = await http_client.get(
            f"{self.BASE_URL}/gifs/trending",
            params={
                "api_key": self.api_key,
                "limit": limit
            }
        )
        if response.status_code == 200:
            return response.json()
        raise Exception(f"Giphy returned status {response.status_code}")
    
    async def get_by_id(self, gif_id: str) -> Optional[Dict[str, Any]]:
        """Get GIF by ID"""
        response = await http_client.get(
            f"{self.BASE_URL}/gifs/{gif_id}",
            params={"api_key": self.api_key}
        )
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            return None
        raise Exception(f"Giphy returned status {response.status_code}")
    
    async def get_random(self, tag: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Get random GIF"""
        params = {"api_key": self.api_key}
        if tag:
            params["tag"] = tag
        
        response = await http_client.get(
            f"{self.BASE_URL}/gifs/random",
            params=params
        )
        if response.status_code == 200:
            return response.json()
        return None






