"""Quote Providers - Random quotes and advice"""
import httpx
from typing import Dict, Any, Optional

class QuoteAPIProvider:
    """Provider for Quote API (free, unlimited)"""
    
    def __init__(self):
        # Using ZenQuotes as primary (more reliable)
        self.base_url = "https://zenquotes.io/api"
        self.fallback_url = "https://api.quotable.io"
        self.available = True
        print("✅ Quote API provider initialized (free, unlimited)")
    
    async def get_random_quote(self, tags: Optional[str] = None, max_length: Optional[int] = None) -> Dict[str, Any]:
        """Get a random quote"""
        async with httpx.AsyncClient(timeout=10.0, verify=False) as client:
            try:
                # Try ZenQuotes first (more reliable)
                response = await client.get(f"{self.base_url}/random")
                if response.status_code == 200:
                    data = response.json()
                    if data and len(data) > 0:
                        quote = data[0]
                        return {
                            "content": quote.get("q", ""),
                            "author": quote.get("a", "Unknown"),
                            "source": "zenquotes"
                        }
            except:
                pass
            
            # Fallback to quotable.io
            params = {}
            if tags:
                params["tags"] = tags
            if max_length:
                params["maxLength"] = max_length
            response = await client.get(f"{self.fallback_url}/random", params=params)
            response.raise_for_status()
            return response.json()
    
    async def get_quotes(self, tags: Optional[str] = None, limit: int = 20) -> Dict[str, Any]:
        """Get multiple quotes"""
        async with httpx.AsyncClient(timeout=10.0) as client:
            params = {"limit": limit}
            if tags:
                params["tags"] = tags
            response = await client.get(f"{self.base_url}/quotes", params=params)
            response.raise_for_status()
            return response.json()
    
    async def get_quote(self, quote_id: str) -> Dict[str, Any]:
        """Get a specific quote by ID"""
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{self.base_url}/quotes/{quote_id}")
            response.raise_for_status()
            return response.json()
    
    async def get_tags(self) -> list:
        """Get all available tags"""
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{self.base_url}/tags")
            response.raise_for_status()
            return response.json()


class AdviceSlipProvider:
    """Provider for Advice Slip API (free, unlimited)"""
    
    def __init__(self):
        self.base_url = "https://api.adviceslip.com"
        self.available = True
        print("✅ Advice Slip provider initialized (free, unlimited)")
    
    async def get_random_advice(self) -> Dict[str, Any]:
        """Get random advice"""
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{self.base_url}/advice")
            response.raise_for_status()
            return response.json()
    
    async def get_advice(self, advice_id: int) -> Dict[str, Any]:
        """Get specific advice by ID"""
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{self.base_url}/advice/{advice_id}")
            response.raise_for_status()
            return response.json()
    
    async def search_advice(self, query: str) -> Dict[str, Any]:
        """Search for advice"""
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{self.base_url}/advice/search/{query}")
            response.raise_for_status()
            return response.json()

