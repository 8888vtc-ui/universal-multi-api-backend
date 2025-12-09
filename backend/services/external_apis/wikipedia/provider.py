"""Wikipedia Provider - Free Wikipedia API access"""
import httpx
from typing import Dict, Any, List, Optional


class WikipediaProvider:
    """Provider for Wikipedia API - Free, no API key required"""
    
    BASE_URL = "https://en.wikipedia.org/api/rest_v1"
    SEARCH_URL = "https://en.wikipedia.org/w/api.php"
    
    def __init__(self):
        self.timeout = 10.0
    
    async def search(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search Wikipedia articles"""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                params = {
                    "action": "query",
                    "list": "search",
                    "srsearch": query,
                    "srlimit": limit,
                    "format": "json"
                }
                
                response = await client.get(self.SEARCH_URL, params=params)
                
                if response.status_code == 200:
                    data = response.json()
                    search_results = data.get("query", {}).get("search", [])
                    
                    results = []
                    for item in search_results:
                        results.append({
                            "title": item.get("title"),
                            "snippet": item.get("snippet", "").replace("<span class=\"searchmatch\">", "").replace("</span>", ""),
                            "page_id": item.get("pageid"),
                            "word_count": item.get("wordcount")
                        })
                    return results
                return []
        except Exception as e:
            print(f"Wikipedia search error: {e}")
            return []
    
    async def get_page(self, title: str) -> Optional[Dict[str, Any]]:
        """Get Wikipedia page by title"""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                # URL encode the title
                encoded_title = title.replace(" ", "_")
                response = await client.get(f"{self.BASE_URL}/page/summary/{encoded_title}")
                
                if response.status_code == 200:
                    data = response.json()
                    return {
                        "title": data.get("title"),
                        "extract": data.get("extract"),
                        "description": data.get("description"),
                        "thumbnail": data.get("thumbnail", {}).get("source") if data.get("thumbnail") else None,
                        "content_url": data.get("content_urls", {}).get("desktop", {}).get("page"),
                        "type": data.get("type")
                    }
                return None
        except Exception as e:
            print(f"Wikipedia page error: {e}")
            return None
    
    async def get_summary(self, title: str) -> Optional[str]:
        """Get Wikipedia page summary"""
        try:
            page = await self.get_page(title)
            if page:
                return page.get("extract")
            return None
        except Exception as e:
            print(f"Wikipedia summary error: {e}")
            return None
    
    async def get_random_article(self) -> Optional[Dict[str, Any]]:
        """Get random Wikipedia article"""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(f"{self.BASE_URL}/page/random/summary")
                
                if response.status_code == 200:
                    data = response.json()
                    return {
                        "title": data.get("title"),
                        "extract": data.get("extract"),
                        "description": data.get("description"),
                        "thumbnail": data.get("thumbnail", {}).get("source") if data.get("thumbnail") else None,
                        "content_url": data.get("content_urls", {}).get("desktop", {}).get("page")
                    }
                return None
        except Exception as e:
            print(f"Wikipedia random error: {e}")
            return None
