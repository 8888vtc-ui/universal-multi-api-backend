"""
News API Providers
NewsAPI.org, NewsData.io
"""
import os
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class NewsAPIOrg:
    """NewsAPI.org - 50k+ sources, 50 countries"""
    
    def __init__(self):
        self.api_key = os.getenv('NEWSAPI_ORG_KEY')
        if not self.api_key:
            raise ValueError("NEWSAPI_ORG_KEY not found")
        
        self.base_url = "https://newsapi.org/v2"
        self.available = True
    
    async def search(
        self,
        query: str,
        language: str = 'en',
        page_size: int = 10
    ) -> Dict[str, Any]:
        """Search news articles"""
        from services.http_client import http_client
        
        url = f"{self.base_url}/everything"
        params = {
            'apiKey': self.api_key,
            'q': query,
            'language': language,
            'pageSize': min(page_size, 100),
            'sortBy': 'publishedAt'
        }
        
        response = await http_client.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        return {
            'articles': data.get('articles', []),
            'total_results': data.get('totalResults', 0)
        }
    
    async def get_top_headlines(
        self,
        country: str = 'us',
        category: Optional[str] = None,
        page_size: int = 10
    ) -> Dict[str, Any]:
        """Get top headlines"""
        from services.http_client import http_client
        
        url = f"{self.base_url}/top-headlines"
        params = {
            'apiKey': self.api_key,
            'country': country,
            'pageSize': min(page_size, 100)
        }
        
        if category:
            params['category'] = category
        
        response = await http_client.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        return {
            'articles': data.get('articles', []),
            'total_results': data.get('totalResults', 0)
        }


class NewsDataIO:
    """NewsData.io - 79k+ sources, 206 countries"""
    
    def __init__(self):
        self.api_key = os.getenv('NEWSDATA_IO_KEY')
        if not self.api_key:
            raise ValueError("NEWSDATA_IO_KEY not found")
        
        self.base_url = "https://newsdata.io/api/1"
        self.available = True
    
    async def search(
        self,
        query: str,
        language: str = 'en',
        page_size: int = 10
    ) -> Dict[str, Any]:
        """Search news articles"""
        from services.http_client import http_client
        
        url = f"{self.base_url}/news"
        params = {
            'apikey': self.api_key,
            'q': query,
            'language': language,
            'size': min(page_size, 50)
        }
        
        response = await http_client.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        return {
            'articles': data.get('results', []),
            'total_results': data.get('totalResults', 0)
        }
    
    async def get_top_headlines(
        self,
        country: str = 'us',
        category: Optional[str] = None,
        page_size: int = 10
    ) -> Dict[str, Any]:
        """Get latest news (top headlines)"""
        from services.http_client import http_client
        
        url = f"{self.base_url}/news"
        params = {
            'apikey': self.api_key,
            'country': country,
            'size': min(page_size, 50)
        }
        
        if category:
            params['category'] = category
        
        response = await http_client.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        return {
            'articles': data.get('results', []),
            'total_results': data.get('totalResults', 0)
        }
