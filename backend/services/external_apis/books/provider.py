"""
Google Books API Provider
1,000 requests/day free
"""
import httpx
import os
from typing import Dict, Any, Optional, List
from dotenv import load_dotenv
from services.http_client import http_client

load_dotenv()


class GoogleBooksProvider:
    """Google Books API - 1,000 req/day free"""
    
    BASE_URL = "https://www.googleapis.com/books/v1"
    
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_BOOKS_API_KEY", "")
    
    async def search(self, query: str, max_results: int = 10) -> Dict[str, Any]:
        """Search books"""
        params = {
            "q": query,
            "maxResults": max_results
        }
        if self.api_key:
            params["key"] = self.api_key
        
        response = await http_client.get(
            f"{self.BASE_URL}/volumes",
            params=params
        )
        if response.status_code == 200:
            return response.json()
        raise Exception(f"Google Books returned status {response.status_code}")
    
    async def get_by_id(self, book_id: str) -> Optional[Dict[str, Any]]:
        """Get book by ID"""
        params = {}
        if self.api_key:
            params["key"] = self.api_key
        
        response = await http_client.get(
            f"{self.BASE_URL}/volumes/{book_id}",
            params=params
        )
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            return None
        raise Exception(f"Google Books returned status {response.status_code}")






