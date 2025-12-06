"""
Wikipedia API Provider
Free unlimited access to Wikipedia articles
"""
import httpx
from typing import Dict, Any, Optional, List


class WikipediaProvider:
    """Wikipedia API - Unlimited free"""
    
    # Using Wikipedia's Action API which is more reliable
    BASE_URL = "https://en.wikipedia.org/w/api.php"
    HEADERS = {
        "User-Agent": "UniversalAPIBackend/2.4.0 (https://github.com/universal-api; contact@example.com)"
    }
    
    async def search(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search Wikipedia articles"""
        async with httpx.AsyncClient(timeout=30.0, headers=self.HEADERS) as client:
            # Use Wikipedia's Action API for search
            response = await client.get(
                self.BASE_URL,
                params={
                    "action": "query",
                    "list": "search",
                    "srsearch": query,
                    "srlimit": limit,
                    "format": "json",
                    "utf8": 1
                }
            )
            if response.status_code == 200:
                data = response.json()
                results = data.get("query", {}).get("search", [])
                return [
                    {
                        "title": r.get("title"),
                        "snippet": r.get("snippet", "").replace("<span class=\"searchmatch\">", "").replace("</span>", ""),
                        "pageid": r.get("pageid"),
                        "wordcount": r.get("wordcount"),
                        "url": f"https://en.wikipedia.org/wiki/{r.get('title', '').replace(' ', '_')}"
                    }
                    for r in results
                ]
            raise Exception(f"Wikipedia returned status {response.status_code}")
    
    async def get_page(self, title: str) -> Optional[Dict[str, Any]]:
        """Get Wikipedia page by title"""
        async with httpx.AsyncClient(timeout=30.0, headers=self.HEADERS) as client:
            # Use Action API for page content
            response = await client.get(
                self.BASE_URL,
                params={
                    "action": "query",
                    "titles": title,
                    "prop": "extracts|info|pageimages",
                    "exintro": True,
                    "explaintext": True,
                    "inprop": "url",
                    "pithumbsize": 500,
                    "format": "json",
                    "utf8": 1
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                pages = data.get("query", {}).get("pages", {})
                for page_id, page_data in pages.items():
                    if page_id != "-1":  # Page exists
                        return {
                            "title": page_data.get("title"),
                            "pageid": page_data.get("pageid"),
                            "extract": page_data.get("extract", ""),
                            "url": page_data.get("fullurl"),
                            "thumbnail": page_data.get("thumbnail", {}).get("source")
                        }
            
            return None
    
    async def get_summary(self, title: str) -> Optional[str]:
        """Get Wikipedia page summary"""
        page = await self.get_page(title)
        if page:
            return page.get("extract", "")
        return None
    
    async def get_random_article(self) -> Optional[Dict[str, Any]]:
        """Get random Wikipedia article"""
        async with httpx.AsyncClient(timeout=30.0, headers=self.HEADERS) as client:
            # Get random page title
            response = await client.get(
                self.BASE_URL,
                params={
                    "action": "query",
                    "list": "random",
                    "rnlimit": 1,
                    "rnnamespace": 0,  # Main namespace only
                    "format": "json"
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                random_pages = data.get("query", {}).get("random", [])
                if random_pages:
                    title = random_pages[0].get("title")
                    # Get full page info
                    return await self.get_page(title)
            
            return None

