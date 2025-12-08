"""
Finnhub Provider - Free stock market data API
Free tier: 60 calls/minute, unlimited calls/day
"""
import os
import logging
from typing import Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)


class FinnhubProvider:
    """Finnhub API - Stock quotes, company info, news (60/min, unlimited/day)"""
    
    def __init__(self):
        self.base_url = "https://finnhub.io/api/v1"
        self.api_key = os.getenv("FINNHUB_API_KEY", "")
        # Finnhub allows free tier without key for some endpoints, but better with key
        self.available = True  # Always available, but some endpoints need key
        
    async def get_stock_quote(self, symbol: str) -> Dict[str, Any]:
        """Get real-time stock quote"""
        from services.http_client import http_client
        
        try:
            params = {"symbol": symbol.upper()}
            if self.api_key:
                params["token"] = self.api_key
            
            response = await http_client.get(
                f"{self.base_url}/quote",
                params=params
            )
            response.raise_for_status()
            data = response.json()
            
            return {
                "symbol": symbol.upper(),
                "price": data.get("c"),  # Current price
                "change": data.get("d"),  # Change
                "change_percent": data.get("dp"),  # Change percent
                "high": data.get("h"),  # High
                "low": data.get("l"),  # Low
                "open": data.get("o"),  # Open
                "previous_close": data.get("pc"),  # Previous close
                "timestamp": data.get("t")  # Timestamp
            }
        except Exception as e:
            logger.error(f"Finnhub API error: {e}")
            raise Exception(f"Finnhub API error: {e}")
    
    async def get_company_profile(self, symbol: str) -> Dict[str, Any]:
        """Get company profile information"""
        from services.http_client import http_client
        
        try:
            params = {"symbol": symbol.upper()}
            if self.api_key:
                params["token"] = self.api_key
            
            response = await http_client.get(
                f"{self.base_url}/stock/profile2",
                params=params
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Finnhub company profile error: {e}")
            raise Exception(f"Finnhub company profile error: {e}")
    
    async def get_company_news(self, symbol: str, limit: int = 10) -> Dict[str, Any]:
        """Get company news"""
        from services.http_client import http_client
        from datetime import datetime, timedelta
        
        try:
            # Get news from last 7 days
            to_date = datetime.now()
            from_date = to_date - timedelta(days=7)
            
            params = {
                "symbol": symbol.upper(),
                "from": from_date.strftime("%Y-%m-%d"),
                "to": to_date.strftime("%Y-%m-%d")
            }
            if self.api_key:
                params["token"] = self.api_key
            
            response = await http_client.get(
                f"{self.base_url}/company-news",
                params=params
            )
            response.raise_for_status()
            news = response.json()
            
            # Limit results
            if isinstance(news, list):
                news = news[:limit]
            
            return {"news": news, "count": len(news) if isinstance(news, list) else 0}
        except Exception as e:
            logger.error(f"Finnhub news error: {e}")
            raise Exception(f"Finnhub news error: {e}")
    
    async def get_market_news(self, category: str = "general", limit: int = 10) -> Dict[str, Any]:
        """Get general market news"""
        from services.http_client import http_client
        
        try:
            params = {"category": category}
            if self.api_key:
                params["token"] = self.api_key
            
            response = await http_client.get(
                f"{self.base_url}/news",
                params=params
            )
            response.raise_for_status()
            news = response.json()
            
            # Limit results
            if isinstance(news, list):
                news = news[:limit]
            
            return {"news": news, "count": len(news) if isinstance(news, list) else 0}
        except Exception as e:
            logger.error(f"Finnhub market news error: {e}")
            raise Exception(f"Finnhub market news error: {e}")


# Singleton instance
finnhub = FinnhubProvider()


Finnhub Provider - Free stock market data API
Free tier: 60 calls/minute, unlimited calls/day
"""
import os
import logging
from typing import Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)


class FinnhubProvider:
    """Finnhub API - Stock quotes, company info, news (60/min, unlimited/day)"""
    
    def __init__(self):
        self.base_url = "https://finnhub.io/api/v1"
        self.api_key = os.getenv("FINNHUB_API_KEY", "")
        # Finnhub allows free tier without key for some endpoints, but better with key
        self.available = True  # Always available, but some endpoints need key
        
    async def get_stock_quote(self, symbol: str) -> Dict[str, Any]:
        """Get real-time stock quote"""
        from services.http_client import http_client
        
        try:
            params = {"symbol": symbol.upper()}
            if self.api_key:
                params["token"] = self.api_key
            
            response = await http_client.get(
                f"{self.base_url}/quote",
                params=params
            )
            response.raise_for_status()
            data = response.json()
            
            return {
                "symbol": symbol.upper(),
                "price": data.get("c"),  # Current price
                "change": data.get("d"),  # Change
                "change_percent": data.get("dp"),  # Change percent
                "high": data.get("h"),  # High
                "low": data.get("l"),  # Low
                "open": data.get("o"),  # Open
                "previous_close": data.get("pc"),  # Previous close
                "timestamp": data.get("t")  # Timestamp
            }
        except Exception as e:
            logger.error(f"Finnhub API error: {e}")
            raise Exception(f"Finnhub API error: {e}")
    
    async def get_company_profile(self, symbol: str) -> Dict[str, Any]:
        """Get company profile information"""
        from services.http_client import http_client
        
        try:
            params = {"symbol": symbol.upper()}
            if self.api_key:
                params["token"] = self.api_key
            
            response = await http_client.get(
                f"{self.base_url}/stock/profile2",
                params=params
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Finnhub company profile error: {e}")
            raise Exception(f"Finnhub company profile error: {e}")
    
    async def get_company_news(self, symbol: str, limit: int = 10) -> Dict[str, Any]:
        """Get company news"""
        from services.http_client import http_client
        from datetime import datetime, timedelta
        
        try:
            # Get news from last 7 days
            to_date = datetime.now()
            from_date = to_date - timedelta(days=7)
            
            params = {
                "symbol": symbol.upper(),
                "from": from_date.strftime("%Y-%m-%d"),
                "to": to_date.strftime("%Y-%m-%d")
            }
            if self.api_key:
                params["token"] = self.api_key
            
            response = await http_client.get(
                f"{self.base_url}/company-news",
                params=params
            )
            response.raise_for_status()
            news = response.json()
            
            # Limit results
            if isinstance(news, list):
                news = news[:limit]
            
            return {"news": news, "count": len(news) if isinstance(news, list) else 0}
        except Exception as e:
            logger.error(f"Finnhub news error: {e}")
            raise Exception(f"Finnhub news error: {e}")
    
    async def get_market_news(self, category: str = "general", limit: int = 10) -> Dict[str, Any]:
        """Get general market news"""
        from services.http_client import http_client
        
        try:
            params = {"category": category}
            if self.api_key:
                params["token"] = self.api_key
            
            response = await http_client.get(
                f"{self.base_url}/news",
                params=params
            )
            response.raise_for_status()
            news = response.json()
            
            # Limit results
            if isinstance(news, list):
                news = news[:limit]
            
            return {"news": news, "count": len(news) if isinstance(news, list) else 0}
        except Exception as e:
            logger.error(f"Finnhub market news error: {e}")
            raise Exception(f"Finnhub market news error: {e}")


# Singleton instance
finnhub = FinnhubProvider()



