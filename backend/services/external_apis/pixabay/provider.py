"""Pixabay Provider - Free images"""
import os
import httpx
from typing import List, Dict, Any, Optional
from services.http_client import http_client

class PixabayProvider:
    """Provider for Pixabay API (free, 5,000 req/day)"""
    
    def __init__(self):
        self.api_key = os.getenv("PIXABAY_API_KEY", "")
        if not self.api_key or self.api_key == "your_pixabay_api_key_here":
            self.available = False
            print("[WARN]  Pixabay API key not configured. Pixabay features will be unavailable.")
        else:
            self.base_url = "https://pixabay.com/api"
            self.available = True
            print("[OK] Pixabay provider initialized (free, 5,000 req/day)")
    
    async def search_images(self, query: str, limit: int = 20, image_type: str = "all") -> Dict[str, Any]:
        """Search for images"""
        if not self.available:
            raise Exception("Pixabay API not available: API key not configured.")
        response = await http_client.get(
            self.base_url,
            params={
                "key": self.api_key,
                "q": query,
                "image_type": image_type,
                "per_page": min(limit, 200)
            }
        )
        response.raise_for_status()
        return response.json()
    
    async def get_image(self, image_id: int) -> Dict[str, Any]:
        """Get image details by ID"""
        if not self.available:
            raise Exception("Pixabay API not available: API key not configured.")
        response = await http_client.get(
            self.base_url,
            params={"key": self.api_key, "id": image_id}
        )
        response.raise_for_status()
        return response.json()






