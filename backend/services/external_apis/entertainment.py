"""
Entertainment API Providers
Movies, Music, Restaurants
"""
import os
import httpx
from typing import Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()


class TMDBProvider:
    """The Movie Database API - Movies and TV shows (1000/day)"""
    
    def __init__(self):
        self.base_url = "https://api.themoviedb.org/3"
        self.api_key = os.getenv("TMDB_API_KEY", "")
        self.available = bool(self.api_key and self.api_key != "your_tmdb_api_key_here")
        
    async def search_movies(self, query: str) -> Dict[str, Any]:
        """Search for movies"""
        if not self.available:
            raise Exception("TMDB API key not configured")
        
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    f"{self.base_url}/search/movie",
                    params={
                        "api_key": self.api_key,
                        "query": query
                    }
                )
                
                if response.status_code == 200:
                    return response.json()
                else:
                    raise Exception(f"TMDB returned status {response.status_code}")
        
        except Exception as e:
            raise Exception(f"TMDB API error: {e}")
    
    async def get_trending(self, media_type: str = "movie", time_window: str = "week") -> Dict[str, Any]:
        """Get trending movies or TV shows"""
        if not self.available:
            raise Exception("TMDB API key not configured")
        
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    f"{self.base_url}/trending/{media_type}/{time_window}",
                    params={"api_key": self.api_key}
                )
                
                if response.status_code == 200:
                    return response.json()
                else:
                    raise Exception(f"TMDB returned status {response.status_code}")
        
        except Exception as e:
            raise Exception(f"TMDB API error: {e}")


class YelpProvider:
    """Yelp API - Restaurants and businesses (5000/day)"""
    
    def __init__(self):
        self.base_url = "https://api.yelp.com/v3"
        self.api_key = os.getenv("YELP_API_KEY", "")
        self.available = bool(self.api_key and self.api_key != "your_yelp_api_key_here")
        
    async def search_businesses(self, term: str, location: str, limit: int = 10) -> Dict[str, Any]:
        """Search for businesses (restaurants, etc.)"""
        if not self.available:
            raise Exception("Yelp API key not configured")
        
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    f"{self.base_url}/businesses/search",
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    params={
                        "term": term,
                        "location": location,
                        "limit": limit
                    }
                )
                
                if response.status_code == 200:
                    return response.json()
                else:
                    raise Exception(f"Yelp returned status {response.status_code}")
        
        except Exception as e:
            raise Exception(f"Yelp API error: {e}")
    
    async def get_business_details(self, business_id: str) -> Dict[str, Any]:
        """Get detailed information about a business"""
        if not self.available:
            raise Exception("Yelp API key not configured")
        
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    f"{self.base_url}/businesses/{business_id}",
                    headers={"Authorization": f"Bearer {self.api_key}"}
                )
                
                if response.status_code == 200:
                    return response.json()
                else:
                    raise Exception(f"Yelp returned status {response.status_code}")
        
        except Exception as e:
            raise Exception(f"Yelp API error: {e}")


class SpotifyProvider:
    """Spotify API - Music data (requires OAuth, free tier available)"""
    
    def __init__(self):
        self.base_url = "https://api.spotify.com/v1"
        self.client_id = os.getenv("SPOTIFY_CLIENT_ID", "")
        self.client_secret = os.getenv("SPOTIFY_CLIENT_SECRET", "")
        self.available = bool(self.client_id and self.client_secret)
        self.access_token = None
        
    async def _get_access_token(self) -> str:
        """Get Spotify access token"""
        if self.access_token:
            return self.access_token
        
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(
                    "https://accounts.spotify.com/api/token",
                    data={"grant_type": "client_credentials"},
                    auth=(self.client_id, self.client_secret)
                )
                
                if response.status_code == 200:
                    data = response.json()
                    self.access_token = data["access_token"]
                    return self.access_token
                else:
                    raise Exception(f"Spotify auth failed: {response.status_code}")
        
        except Exception as e:
            raise Exception(f"Spotify auth error: {e}")
    
    async def search_tracks(self, query: str, limit: int = 10) -> Dict[str, Any]:
        """Search for music tracks"""
        if not self.available:
            raise Exception("Spotify API credentials not configured")
        
        try:
            token = await self._get_access_token()
            
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    f"{self.base_url}/search",
                    headers={"Authorization": f"Bearer {token}"},
                    params={
                        "q": query,
                        "type": "track",
                        "limit": limit
                    }
                )
                
                if response.status_code == 200:
                    return response.json()
                else:
                    raise Exception(f"Spotify returned status {response.status_code}")
        
        except Exception as e:
            raise Exception(f"Spotify API error: {e}")


# Singleton instances
tmdb = TMDBProvider()
yelp = YelpProvider()
spotify = SpotifyProvider()
