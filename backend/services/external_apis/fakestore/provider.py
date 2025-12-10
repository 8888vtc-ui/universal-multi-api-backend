"""FakeStore Provider - Free fake e-commerce API"""
import httpx
from typing import List, Dict, Any, Optional
from services.http_client import http_client

class FakeStoreProvider:
    """Provider for FakeStore API (free, unlimited)"""
    
    def __init__(self):
        self.base_url = "https://fakestoreapi.com"
        self.available = True
        print("[OK] FakeStore provider initialized (free, unlimited)")
    
    async def get_products(self, limit: Optional[int] = None, sort: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get all products"""
        url = f"{self.base_url}/products"
        params = {}
        if limit:
            params["limit"] = limit
        if sort:
            params["sort"] = sort
        response = await http_client.get(url, params=params)
        response.raise_for_status()
        return response.json()
    
    async def get_product(self, product_id: int) -> Dict[str, Any]:
        """Get a specific product by ID"""
        response = await http_client.get(f"{self.base_url}/products/{product_id}")
        response.raise_for_status()
        return response.json()
    
    async def get_categories(self) -> List[str]:
        """Get all product categories"""
        response = await http_client.get(f"{self.base_url}/products/categories")
        response.raise_for_status()
        return response.json()
    
    async def get_products_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Get products by category"""
        response = await http_client.get(f"{self.base_url}/products/category/{category}")
        response.raise_for_status()
        return response.json()
    
    async def get_users(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get all users"""
        url = f"{self.base_url}/users"
        params = {}
        if limit:
            params["limit"] = limit
        response = await http_client.get(url, params=params)
        response.raise_for_status()
        return response.json()
    
    async def get_carts(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get all carts"""
        url = f"{self.base_url}/carts"
        params = {}
        if limit:
            params["limit"] = limit
        response = await http_client.get(url, params=params)
        response.raise_for_status()
        return response.json()






