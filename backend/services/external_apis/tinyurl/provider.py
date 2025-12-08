"""TinyURL Provider - URL shortener"""
import httpx
from typing import Dict, Any

class TinyURLProvider:
    """Provider for TinyURL API (free, unlimited)"""
    
    def __init__(self):
        self.base_url = "https://tinyurl.com/api-create.php"
        self.available = True
        print("[OK] TinyURL provider initialized (free, unlimited)")
    
    async def shorten_url(self, url: str, alias: str = None) -> Dict[str, Any]:
        """Shorten a URL"""
        async with httpx.AsyncClient(timeout=10.0) as client:
            params = {"url": url}
            if alias:
                params["alias"] = alias
            response = await client.get(self.base_url, params=params)
            response.raise_for_status()
            short_url = response.text.strip()
            return {
                "original_url": url,
                "short_url": short_url,
                "alias": alias
            }






