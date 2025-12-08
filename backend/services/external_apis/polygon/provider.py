"""
Polygon.io Provider - Free stock market data API
Free tier: 5 calls/minute, unlimited calls/day
"""
import os
import logging
from typing import Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)


class PolygonProvider:
    """Polygon.io API - Stocks, Options, Forex (5/min, unlimited/day)"""
    
    def __init__(self):
        self.base_url = "https://api.polygon.io"
        self.api_key = os.getenv("POLYGON_API_KEY", "")
        self.available = bool(self.api_key and self.api_key != "your_polygon_api_key_here")
        
    async def get_stock_quote(self, symbol: str) -> Dict[str, Any]:
        """Get real-time stock quote"""
        if not self.available:
            raise Exception("Polygon API key not configured")
        
        from services.http_client import http_client
        
        try:
            response = await http_client.get(
                f"{self.base_url}/v2/aggs/ticker/{symbol.upper()}/prev",
                params={"apikey": self.api_key}
            )
            response.raise_for_status()
            data = response.json()
            
            if data.get("status") == "OK" and data.get("resultsCount", 0) > 0:
                result = data["results"][0]
                return {
                    "symbol": symbol.upper(),
                    "price": float(result.get("c", 0)),  # Close price
                    "change": float(result.get("c", 0) - result.get("o", 0)),  # Close - Open
                    "change_percent": float((result.get("c", 0) - result.get("o", 0)) / result.get("o", 1) * 100),
                    "high": float(result.get("h", 0)),
                    "low": float(result.get("l", 0)),
                    "open": float(result.get("o", 0)),
                    "volume": int(result.get("v", 0))
                }
            else:
                raise Exception("No data returned from Polygon")
        except Exception as e:
            logger.error(f"Polygon API error: {e}")
            raise Exception(f"Polygon API error: {e}")


# Singleton instance
polygon = PolygonProvider()


Polygon.io Provider - Free stock market data API
Free tier: 5 calls/minute, unlimited calls/day
"""
import os
import logging
from typing import Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)


class PolygonProvider:
    """Polygon.io API - Stocks, Options, Forex (5/min, unlimited/day)"""
    
    def __init__(self):
        self.base_url = "https://api.polygon.io"
        self.api_key = os.getenv("POLYGON_API_KEY", "")
        self.available = bool(self.api_key and self.api_key != "your_polygon_api_key_here")
        
    async def get_stock_quote(self, symbol: str) -> Dict[str, Any]:
        """Get real-time stock quote"""
        if not self.available:
            raise Exception("Polygon API key not configured")
        
        from services.http_client import http_client
        
        try:
            response = await http_client.get(
                f"{self.base_url}/v2/aggs/ticker/{symbol.upper()}/prev",
                params={"apikey": self.api_key}
            )
            response.raise_for_status()
            data = response.json()
            
            if data.get("status") == "OK" and data.get("resultsCount", 0) > 0:
                result = data["results"][0]
                return {
                    "symbol": symbol.upper(),
                    "price": float(result.get("c", 0)),  # Close price
                    "change": float(result.get("c", 0) - result.get("o", 0)),  # Close - Open
                    "change_percent": float((result.get("c", 0) - result.get("o", 0)) / result.get("o", 1) * 100),
                    "high": float(result.get("h", 0)),
                    "low": float(result.get("l", 0)),
                    "open": float(result.get("o", 0)),
                    "volume": int(result.get("v", 0))
                }
            else:
                raise Exception("No data returned from Polygon")
        except Exception as e:
            logger.error(f"Polygon API error: {e}")
            raise Exception(f"Polygon API error: {e}")


# Singleton instance
polygon = PolygonProvider()



