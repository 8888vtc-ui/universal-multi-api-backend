"""JSONPlaceholder Provider - Free fake REST API for testing"""
import httpx
from typing import List, Dict, Any, Optional
from services.http_client import http_client

class JSONPlaceholderProvider:
    """Provider for JSONPlaceholder API (free, unlimited)"""
    
    def __init__(self):
        self.base_url = "https://jsonplaceholder.typicode.com"
        self.available = True
        print("[OK] JSONPlaceholder provider initialized (free, unlimited)")
    
    async def get_posts(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get all posts"""
        response = await http_client.get(f"{self.base_url}/posts")
        response.raise_for_status()
        posts = response.json()
        return posts[:limit] if limit else posts
    
    async def get_post(self, post_id: int) -> Dict[str, Any]:
        """Get a specific post by ID"""
        response = await http_client.get(f"{self.base_url}/posts/{post_id}")
        response.raise_for_status()
        return response.json()
    
    async def get_users(self) -> List[Dict[str, Any]]:
        """Get all users"""
        response = await http_client.get(f"{self.base_url}/users")
        response.raise_for_status()
        return response.json()
    
    async def get_user(self, user_id: int) -> Dict[str, Any]:
        """Get a specific user by ID"""
        response = await http_client.get(f"{self.base_url}/users/{user_id}")
        response.raise_for_status()
        return response.json()
    
    async def get_comments(self, post_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get comments, optionally filtered by post ID"""
        url = f"{self.base_url}/posts/{post_id}/comments" if post_id else f"{self.base_url}/comments"
        response = await http_client.get(url)
        response.raise_for_status()
        return response.json()
    
    async def get_albums(self) -> List[Dict[str, Any]]:
        """Get all albums"""
        response = await http_client.get(f"{self.base_url}/albums")
        response.raise_for_status()
        return response.json()
    
    async def get_photos(self, album_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get photos, optionally filtered by album ID"""
        url = f"{self.base_url}/albums/{album_id}/photos" if album_id else f"{self.base_url}/photos"
        response = await http_client.get(url)
        response.raise_for_status()
        return response.json()
    
    async def get_todos(self, user_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get todos, optionally filtered by user ID"""
        url = f"{self.base_url}/users/{user_id}/todos" if user_id else f"{self.base_url}/todos"
        response = await http_client.get(url)
        response.raise_for_status()
        return response.json()






