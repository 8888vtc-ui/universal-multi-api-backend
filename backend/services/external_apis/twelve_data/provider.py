"""
Twelve Data Provider - Free stock and crypto data API
Free tier: 800 calls/day, 8 calls/minute
"""
import os
import logging
from typing import Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)


class TwelveDataProvider:
    """Twelve Data API - Stocks, Forex, Crypto (800/day, 8/min)"""
    
    def __init__(self):
        self.base_url = "https://api.twelvedata.com"
        self.api_key = os.getenv("TWELVE_DATA_API_KEY", "")
        self.available = bool(self.api_key and self.api_key != "your_twelve_data_api_key_here")
        
    async def get_stock_quote(self, symbol: str) -> Dict[str, Any]:
        """Get real-time stock quote"""
        if not self.available:
            raise Exception("Twelve Data API key not configured")
        
        from services.http_client import http_client
        
        try:
            response = await http_client.get(
                f"{self.base_url}/quote",
                params={
                    "symbol": symbol.upper(),
                    "apikey": self.api_key
                }
            )
            response.raise_for_status()
            data = response.json()
            
            return {
                "symbol": data.get("symbol"),
                "price": float(data.get("close", 0)),
                "change": float(data.get("change", 0)),
                "change_percent": float(data.get("percent_change", 0)),
                "high": float(data.get("high", 0)),
                "low": float(data.get("low", 0)),
                "open": float(data.get("open", 0)),
                "volume": int(data.get("volume", 0)),
                "timestamp": data.get("datetime")
            }
        except Exception as e:
            logger.error(f"Twelve Data API error: {e}")
            raise Exception(f"Twelve Data API error: {e}")
    
    async def get_crypto_price(self, symbol: str) -> Dict[str, Any]:
        """Get cryptocurrency price"""
        if not self.available:
            raise Exception("Twelve Data API key not configured")
        
        from services.http_client import http_client
        
        try:
            response = await http_client.get(
                f"{self.base_url}/price",
                params={
                    "symbol": symbol.upper(),
                    "apikey": self.api_key
                }
            )
            response.raise_for_status()
            data = response.json()
            
            return {
                "symbol": symbol.upper(),
                "price": float(data.get("price", 0))
            }
        except Exception as e:
            logger.error(f"Twelve Data crypto error: {e}")
            raise Exception(f"Twelve Data crypto error: {e}")
    
    async def get_time_series(self, symbol: str, interval: str = "1day", outputsize: int = 1) -> Dict[str, Any]:
        """Get time series data"""
        if not self.available:
            raise Exception("Twelve Data API key not configured")
        
        from services.http_client import http_client
        
        try:
            response = await http_client.get(
                f"{self.base_url}/time_series",
                params={
                    "symbol": symbol.upper(),
                    "interval": interval,
                    "outputsize": outputsize,
                    "apikey": self.api_key
                }
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Twelve Data time series error: {e}")
            raise Exception(f"Twelve Data time series error: {e}")


# Singleton instance
twelve_data = TwelveDataProvider()

