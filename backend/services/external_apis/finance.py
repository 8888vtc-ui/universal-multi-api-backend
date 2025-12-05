"""
Finance API Providers
Crypto, Stocks, Forex data providers
"""
import os
import logging
from typing import Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)


class CoinGeckoProvider:
    """CoinGecko API - Crypto prices and data (10k/month, 30/min)"""
    
    def __init__(self):
        self.base_url = "https://api.coingecko.com/api/v3"
        self.api_key = os.getenv("COINGECKO_API_KEY", "")  # Optional for demo plan
        self.available = True
        
    async def get_crypto_price(self, coin_id: str, vs_currency: str = "usd") -> Dict[str, Any]:
        """Get current price of a cryptocurrency"""
        from services.http_client import http_client
        
        try:
            response = await http_client.get(
                f"{self.base_url}/simple/price",
                params={
                    "ids": coin_id,
                    "vs_currencies": vs_currency,
                    "include_24hr_change": "true",
                    "include_market_cap": "true"
                }
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"CoinGecko API error: {e}")
            raise Exception(f"CoinGecko API error: {e}")
    
    async def get_trending(self) -> Dict[str, Any]:
        """Get trending cryptocurrencies"""
        from services.http_client import http_client
        
        try:
            response = await http_client.get(f"{self.base_url}/search/trending")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"CoinGecko API error: {e}")
            raise Exception(f"CoinGecko API error: {e}")


class AlphaVantageProvider:
    """Alpha Vantage API - Stocks, Forex, Crypto (25/day, 5/min)"""
    
    def __init__(self):
        self.base_url = "https://www.alphavantage.co/query"
        self.api_key = os.getenv("ALPHAVANTAGE_API_KEY", "")
        self.available = bool(self.api_key and self.api_key != "your_alphavantage_api_key_here")
        
    async def get_stock_quote(self, symbol: str) -> Dict[str, Any]:
        """Get real-time stock quote"""
        if not self.available:
            raise Exception("Alpha Vantage API key not configured")
        
        from services.http_client import http_client
        
        try:
            response = await http_client.get(
                self.base_url,
                params={
                    "function": "GLOBAL_QUOTE",
                    "symbol": symbol,
                    "apikey": self.api_key
                }
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Alpha Vantage API error: {e}")
            raise Exception(f"Alpha Vantage API error: {e}")
    
    async def get_crypto_rating(self, symbol: str) -> Dict[str, Any]:
        """Get cryptocurrency rating"""
        if not self.available:
            raise Exception("Alpha Vantage API key not configured")
        
        from services.http_client import http_client
        
        try:
            response = await http_client.get(
                self.base_url,
                params={
                    "function": "CRYPTO_RATING",
                    "symbol": symbol,
                    "apikey": self.api_key
                }
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Alpha Vantage API error: {e}")
            raise Exception(f"Alpha Vantage API error: {e}")


class YahooFinanceProvider:
    """Yahoo Finance - Market data (unlimited via yfinance library)"""
    
    def __init__(self):
        self.available = True
        
    async def get_stock_info(self, symbol: str) -> Dict[str, Any]:
        """Get stock information"""
        try:
            # Using yfinance library (install: pip install yfinance)
            import yfinance as yf
            
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            return {
                "symbol": symbol,
                "price": info.get("currentPrice", info.get("regularMarketPrice")),
                "change": info.get("regularMarketChange"),
                "change_percent": info.get("regularMarketChangePercent"),
                "volume": info.get("volume"),
                "market_cap": info.get("marketCap"),
                "pe_ratio": info.get("trailingPE"),
                "company_name": info.get("longName")
            }
        except Exception as e:
            logger.error(f"Yahoo Finance error: {e}")
            raise Exception(f"Yahoo Finance error: {e}")
    
    async def get_market_summary(self) -> Dict[str, Any]:
        """Get market summary (major indices)"""
        try:
            import yfinance as yf
            
            indices = {
                "S&P 500": "^GSPC",
                "Dow Jones": "^DJI",
                "NASDAQ": "^IXIC"
            }
            
            summary = {}
            for name, symbol in indices.items():
                ticker = yf.Ticker(symbol)
                info = ticker.info
                summary[name] = {
                    "price": info.get("regularMarketPrice"),
                    "change": info.get("regularMarketChange"),
                    "change_percent": info.get("regularMarketChangePercent")
                }
            
            return summary
        except Exception as e:
            logger.error(f"Yahoo Finance error: {e}")
            raise Exception(f"Yahoo Finance error: {e}")


# Singleton instances
coingecko = CoinGeckoProvider()
alphavantage = AlphaVantageProvider()
yahoo_finance = YahooFinanceProvider()
