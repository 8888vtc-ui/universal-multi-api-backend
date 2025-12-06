"""
YouTube Data API Provider
10,000 requests/day free
"""
import httpx
import os
from typing import Dict, Any, Optional, List
from dotenv import load_dotenv

load_dotenv()


class YouTubeProvider:
    """YouTube Data API - 10,000 req/day free"""
    
    BASE_URL = "https://www.googleapis.com/youtube/v3"
    
    def __init__(self):
        self.api_key = os.getenv("YOUTUBE_API_KEY", "")
        self.available = bool(self.api_key)
    
    async def search(
        self,
        query: str,
        max_results: int = 10,
        order: str = "relevance"
    ) -> Dict[str, Any]:
        """Search YouTube videos"""
        if not self.available:
            raise Exception("YOUTUBE_API_KEY not configured")
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                f"{self.BASE_URL}/search",
                params={
                    "key": self.api_key,
                    "q": query,
                    "part": "snippet",
                    "maxResults": max_results,
                    "order": order,
                    "type": "video"
                }
            )
            if response.status_code == 200:
                return response.json()
            raise Exception(f"YouTube returned status {response.status_code}")
    
    async def get_video(self, video_id: str) -> Optional[Dict[str, Any]]:
        """Get video details by ID"""
        if not self.available:
            raise Exception("YOUTUBE_API_KEY not configured")
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                f"{self.BASE_URL}/videos",
                params={
                    "key": self.api_key,
                    "id": video_id,
                    "part": "snippet,statistics,contentDetails"
                }
            )
            if response.status_code == 200:
                result = response.json()
                items = result.get("items", [])
                return items[0] if items else None
            raise Exception(f"YouTube returned status {response.status_code}")
    
    async def get_channel(self, channel_id: str) -> Optional[Dict[str, Any]]:
        """Get channel details by ID"""
        if not self.available:
            raise Exception("YOUTUBE_API_KEY not configured")
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                f"{self.BASE_URL}/channels",
                params={
                    "key": self.api_key,
                    "id": channel_id,
                    "part": "snippet,statistics"
                }
            )
            if response.status_code == 200:
                result = response.json()
                items = result.get("items", [])
                return items[0] if items else None
            raise Exception(f"YouTube returned status {response.status_code}")
    
    async def get_trending(self, region_code: str = "US", max_results: int = 25) -> Dict[str, Any]:
        """Get trending videos"""
        if not self.available:
            raise Exception("YOUTUBE_API_KEY not configured")
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                f"{self.BASE_URL}/videos",
                params={
                    "key": self.api_key,
                    "part": "snippet,statistics",
                    "chart": "mostPopular",
                    "regionCode": region_code,
                    "maxResults": max_results
                }
            )
            if response.status_code == 200:
                return response.json()
            raise Exception(f"YouTube returned status {response.status_code}")

