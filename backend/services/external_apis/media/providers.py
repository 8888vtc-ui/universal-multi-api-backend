"""
Media Providers
Unsplash, Pexels, Giphy
"""
import os
import httpx
from typing import Dict, Any, Optional, List
from services.http_client import http_client


class Unsplash:
    """Unsplash - 50 req/hour, HD photos free"""
    
    def __init__(self):
        self.access_key = os.getenv('UNSPLASH_ACCESS_KEY')
        if not self.access_key:
            raise ValueError("UNSPLASH_ACCESS_KEY not found")
        
        self.base_url = "https://api.unsplash.com"
        self.available = True
    
    async def search_photos(
        self,
        query: str,
        per_page: int = 10
    ) -> Dict[str, Any]:
        """Search photos"""
        url = f"{self.base_url}/search/photos"
        headers = {'Authorization': f'Client-ID {self.access_key}'}
        params = {
            'query': query,
            'per_page': min(per_page, 30)
        }
        
        response = await http_client.get(url, headers=headers, params=params)
        response.raise_for_status()
        
        data = response.json()
        return {
            'photos': data.get('results', []),
            'total': data.get('total', 0)
        }
    
    async def get_random_photo(self, query: Optional[str] = None) -> Dict[str, Any]:
        """Get random photo"""
        url = f"{self.base_url}/photos/random"
        headers = {'Authorization': f'Client-ID {self.access_key}'}
        params = {}
        if query:
            params['query'] = query
        
        response = await http_client.get(url, headers=headers, params=params)
        response.raise_for_status()
        
        return response.json()


class Pexels:
    """Pexels - 200 req/hour, photos and videos free"""
    
    def __init__(self):
        self.api_key = os.getenv('PEXELS_API_KEY')
        if not self.api_key:
            raise ValueError("PEXELS_API_KEY not found")
        
        self.base_url = "https://api.pexels.com/v1"
        self.available = True
    
    async def search_photos(
        self,
        query: str,
        per_page: int = 10
    ) -> Dict[str, Any]:
        """Search photos"""
        url = f"{self.base_url}/search"
        headers = {'Authorization': self.api_key}
        params = {
            'query': query,
            'per_page': min(per_page, 80)
        }
        
        response = await http_client.get(url, headers=headers, params=params)
        response.raise_for_status()
        
        data = response.json()
        return {
            'photos': data.get('photos', []),
            'total': data.get('total_results', 0)
        }
    
    async def search_videos(
        self,
        query: str,
        per_page: int = 10
    ) -> Dict[str, Any]:
        """Search videos"""
        url = "https://api.pexels.com/videos/search"
        headers = {'Authorization': self.api_key}
        params = {
            'query': query,
            'per_page': min(per_page, 80)
        }
        
        response = await http_client.get(url, headers=headers, params=params)
        response.raise_for_status()
        
        data = response.json()
        return {
            'videos': data.get('videos', []),
            'total': data.get('total_results', 0)
        }


class Giphy:
    """Giphy - 42 req/hour free, unlimited GIFs"""
    
    def __init__(self):
        self.api_key = os.getenv('GIPHY_API_KEY')
        if not self.api_key:
            raise ValueError("GIPHY_API_KEY not found")
        
        self.base_url = "https://api.giphy.com/v1/gifs"
        self.available = True
    
    async def search_gifs(
        self,
        query: str,
        limit: int = 10
    ) -> Dict[str, Any]:
        """Search GIFs"""
        url = f"{self.base_url}/search"
        params = {
            'api_key': self.api_key,
            'q': query,
            'limit': min(limit, 50)
        }
        
        response = await http_client.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        return {
            'gifs': data.get('data', []),
            'total': data.get('pagination', {}).get('total_count', 0)
        }
    
    async def get_trending(self, limit: int = 10) -> Dict[str, Any]:
        """Get trending GIFs"""
        url = f"{self.base_url}/trending"
        params = {
            'api_key': self.api_key,
            'limit': min(limit, 50)
        }
        
        response = await http_client.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        return {
            'gifs': data.get('data', []),
            'total': len(data.get('data', []))
        }
