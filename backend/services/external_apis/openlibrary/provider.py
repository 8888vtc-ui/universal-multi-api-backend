"""Open Library Provider - Free books database"""
import httpx
from typing import Dict, Any, List, Optional
from services.http_client import http_client

class OpenLibraryProvider:
    """Provider for Open Library API (free, unlimited)"""
    
    def __init__(self):
        self.base_url = "https://openlibrary.org"
        self.available = True
        print("[OK] Open Library API initialized (free, unlimited)")
    
    async def search_books(
        self,
        query: str,
        limit: int = 10,
        page: int = 1
    ) -> Dict[str, Any]:
        """Search for books"""
        response = await http_client.get(
            f"{self.base_url}/search.json",
            params={
                "q": query,
                "limit": limit,
                "page": page
            }
        )
        response.raise_for_status()
        data = response.json()
        
        books = []
        for doc in data.get("docs", [])[:limit]:
            books.append({
                "title": doc.get("title"),
                "author": doc.get("author_name", [None])[0],
                "authors": doc.get("author_name", []),
                "first_publish_year": doc.get("first_publish_year"),
                "isbn": doc.get("isbn", [None])[0] if doc.get("isbn") else None,
                "key": doc.get("key"),
                "cover_id": doc.get("cover_i"),
                "cover_url": f"https://covers.openlibrary.org/b/id/{doc.get('cover_i')}-M.jpg" if doc.get("cover_i") else None,
                "subject": doc.get("subject", [])[:5],
                "language": doc.get("language", [])
            })
        
        return {
            "query": query,
            "total": data.get("numFound", 0),
            "books": books,
            "count": len(books)
        }
    
    async def get_book(self, key: str) -> Dict[str, Any]:
        """Get book details by key"""
        response = await http_client.get(f"{self.base_url}{key}.json")
        response.raise_for_status()
        return response.json()
    
    async def search_authors(self, query: str, limit: int = 10) -> Dict[str, Any]:
        """Search for authors"""
        response = await http_client.get(
            f"{self.base_url}/search/authors.json",
            params={"q": query, "limit": limit}
        )
        response.raise_for_status()
        data = response.json()
        
        authors = []
        for doc in data.get("docs", [])[:limit]:
            authors.append({
                "key": doc.get("key"),
                "name": doc.get("name"),
                "birth_date": doc.get("birth_date"),
                "work_count": doc.get("work_count"),
                "top_work": doc.get("top_work")
            })
        
        return {
            "query": query,
            "total": data.get("numFound", 0),
            "authors": authors
        }
    
    async def get_trending(self, time_period: str = "daily") -> Dict[str, Any]:
        """Get trending books"""
        response = await http_client.get(
            f"{self.base_url}/trending/{time_period}.json"
        )
        response.raise_for_status()
        data = response.json()
        
        works = []
        for work in data.get("works", [])[:20]:
            works.append({
                "title": work.get("title"),
                "key": work.get("key"),
                "author": work.get("author_name", [None])[0],
                "cover_id": work.get("cover_i")
            })
        
        return {
            "period": time_period,
            "works": works,
            "count": len(works)
        }






