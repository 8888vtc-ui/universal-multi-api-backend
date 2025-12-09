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
        except ImportError:
            logger.error("yfinance library not installed")
            raise Exception("Yahoo Finance library not available")
        except Exception as e:
            logger.error(f"Yahoo Finance error for {symbol}: {e}", exc_info=True)
            raise Exception(f"Yahoo Finance error: {e}")
    
    async def get_market_summary(self) -> Dict[str, Any]:
        """Get market summary (major indices)"""
        try:
            import yfinance as yf
            import pandas as pd
            
            indices = {
                "S&P 500": "^GSPC",
                "Dow Jones": "^DJI",
                "NASDAQ": "^IXIC"
            }
            
            summary = {}
            for name, symbol in indices.items():
                try:
                    ticker = yf.Ticker(symbol)
                    data_found = False
                    
                    # Method 1: Try history (more reliable)
                    try:
                        hist = ticker.history(period="5d", interval="1d")
                        if not hist.empty and len(hist) > 0:
                            last_price = float(hist['Close'].iloc[-1])
                            prev_close = float(hist['Close'].iloc[0]) if len(hist) > 1 else last_price
                            change = last_price - prev_close
                            change_percent = (change / prev_close * 100) if prev_close > 0 else 0
                            summary[name] = {
                                "price": last_price,
                                "change": change,
                                "change_percent": change_percent
                            }
                            data_found = True
                    except Exception as e:
                        logger.debug(f"History failed for {name} ({symbol}): {e}")
                    
                    # Method 2: Try fast_info
                    if not data_found:
                        try:
                            fast_info = ticker.fast_info
                            if fast_info and hasattr(fast_info, 'last_price') and fast_info.last_price:
                                last_price = float(fast_info.last_price)
                                prev_close = float(fast_info.previous_close) if hasattr(fast_info, 'previous_close') and fast_info.previous_close else last_price
                                change = last_price - prev_close
                                change_percent = (change / prev_close * 100) if prev_close > 0 else 0
                                summary[name] = {
                                    "price": last_price,
                                    "change": change,
                                    "change_percent": change_percent
                                }
                                data_found = True
                        except Exception as e:
                            logger.debug(f"Fast info failed for {name} ({symbol}): {e}")
                    
                    # Method 3: Fallback to info
                    if not data_found:
                        try:
                            info = ticker.info
                            if info and len(info) > 0:
                                summary[name] = {
                                    "price": info.get("regularMarketPrice"),
                                    "change": info.get("regularMarketChange"),
                                    "change_percent": info.get("regularMarketChangePercent")
                                }
                                data_found = True
                        except Exception as e:
                            logger.debug(f"Info failed for {name} ({symbol}): {e}")
                    
                    if not data_found:
                        logger.warning(f"No data found for {name} ({symbol})")
                        
                except Exception as e:
                    logger.warning(f"Failed to get data for {name} ({symbol}): {e}")
                    # Continue with other indices even if one fails
                    continue
            
            if not summary:
                raise Exception("No market data available from any index")
            
            return summary
        except ImportError:
            logger.error("yfinance library not installed")
            raise Exception("Yahoo Finance library not available")
        except Exception as e:
            logger.error(f"Yahoo Finance market summary error: {e}", exc_info=True)
            raise Exception(f"Yahoo Finance error: {e}")


# Singleton instances
coingecko = CoinGeckoProvider()
alphavantage = AlphaVantageProvider()
yahoo_finance = YahooFinanceProvider()
