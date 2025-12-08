"""
Finance tools for agents
"""
import os
import httpx
import logging
from typing import Dict, Any, Optional

from ..base_tool import BaseTool

logger = logging.getLogger(__name__)


class CryptoPriceTool(BaseTool):
    """Tool to fetch cryptocurrency prices"""
    
    def __init__(self):
        super().__init__(
            name="crypto_price",
            description="Fetch cryptocurrency price data from CoinGecko"
        )
        self.base_url = os.getenv("APP_URL", "http://localhost:8000") + "/api"
    
    async def execute(self, query: str, **kwargs) -> Dict[str, Any]:
        """Execute crypto price lookup"""
        coin_id = kwargs.get("coin_id") or query.lower().replace(" ", "-")
        
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    f"{self.base_url}/finance/crypto/price/{coin_id}",
                    params={"vs_currency": "usd"}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("success"):
                        return {
                            "success": True,
                            "data": str(data.get("data", {})),
                            "source": "coingecko"
                        }
                
                return {
                    "success": False,
                    "error": f"API returned status {response.status_code}",
                    "source": "coingecko"
                }
        except Exception as e:
            logger.error(f"CryptoPriceTool error: {e}", exc_info=True)
            return {
                "success": False,
                "error": str(e),
                "source": "coingecko"
            }


class StockQuoteTool(BaseTool):
    """Tool to fetch stock quotes"""
    
    def __init__(self):
        super().__init__(
            name="stock_quote",
            description="Fetch stock quote data from multiple providers"
        )
        self.base_url = os.getenv("APP_URL", "http://localhost:8000") + "/api"
    
    async def execute(self, query: str, **kwargs) -> Dict[str, Any]:
        """Execute stock quote lookup"""
        symbol = kwargs.get("symbol") or query.upper()
        
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    f"{self.base_url}/finance/stock/quote/{symbol}"
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("success"):
                        return {
                            "success": True,
                            "data": str(data.get("data", {})),
                            "source": data.get("source", "finance_api")
                        }
                
                return {
                    "success": False,
                    "error": f"API returned status {response.status_code}",
                    "source": "finance_api"
                }
        except Exception as e:
            logger.error(f"StockQuoteTool error: {e}", exc_info=True)
            return {
                "success": False,
                "error": str(e),
                "source": "finance_api"
            }


class MarketSummaryTool(BaseTool):
    """Tool to fetch market summary"""
    
    def __init__(self):
        super().__init__(
            name="market_summary",
            description="Fetch overall market summary and indices"
        )
        self.base_url = os.getenv("APP_URL", "http://localhost:8000") + "/api"
    
    async def execute(self, query: str, **kwargs) -> Dict[str, Any]:
        """Execute market summary lookup"""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    f"{self.base_url}/finance/market/summary"
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("success"):
                        return {
                            "success": True,
                            "data": str(data.get("data", {})),
                            "source": "finance_api"
                        }
                
                return {
                    "success": False,
                    "error": f"API returned status {response.status_code}",
                    "source": "finance_api"
                }
        except Exception as e:
            logger.error(f"MarketSummaryTool error: {e}", exc_info=True)
            return {
                "success": False,
                "error": str(e),
                "source": "finance_api"
            }


class CurrencyRateTool(BaseTool):
    """Tool to fetch currency exchange rates"""
    
    def __init__(self):
        super().__init__(
            name="currency_rate",
            description="Fetch currency exchange rates"
        )
        self.base_url = os.getenv("APP_URL", "http://localhost:8000") + "/api"
    
    async def execute(self, query: str, **kwargs) -> Dict[str, Any]:
        """Execute currency rate lookup"""
        from_currency = kwargs.get("from_currency", "USD")
        to_currency = kwargs.get("to_currency", "EUR")
        
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    f"{self.base_url}/exchange/rate",
                    params={"from": from_currency, "to": to_currency}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return {
                        "success": True,
                        "data": str(data),
                        "source": "exchange_api"
                    }
                
                return {
                    "success": False,
                    "error": f"API returned status {response.status_code}",
                    "source": "exchange_api"
                }
        except Exception as e:
            logger.error(f"CurrencyRateTool error: {e}", exc_info=True)
            return {
                "success": False,
                "error": str(e),
                "source": "exchange_api"
            }


class MarketNewsTool(BaseTool):
    """Tool to fetch market news"""
    
    def __init__(self):
        super().__init__(
            name="market_news",
            description="Fetch financial market news"
        )
        self.base_url = os.getenv("APP_URL", "http://localhost:8000") + "/api"
    
    async def execute(self, query: str, **kwargs) -> Dict[str, Any]:
        """Execute market news lookup"""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    f"{self.base_url}/finance/market/news",
                    params={"limit": 5}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("success"):
                        return {
                            "success": True,
                            "data": str(data.get("data", [])),
                            "source": "finance_api"
                        }
                
                return {
                    "success": False,
                    "error": f"API returned status {response.status_code}",
                    "source": "finance_api"
                }
        except Exception as e:
            logger.error(f"MarketNewsTool error: {e}", exc_info=True)
            return {
                "success": False,
                "error": str(e),
                "source": "finance_api"
            }


Finance tools for agents
"""
import os
import httpx
import logging
from typing import Dict, Any, Optional

from ..base_tool import BaseTool

logger = logging.getLogger(__name__)


class CryptoPriceTool(BaseTool):
    """Tool to fetch cryptocurrency prices"""
    
    def __init__(self):
        super().__init__(
            name="crypto_price",
            description="Fetch cryptocurrency price data from CoinGecko"
        )
        self.base_url = os.getenv("APP_URL", "http://localhost:8000") + "/api"
    
    async def execute(self, query: str, **kwargs) -> Dict[str, Any]:
        """Execute crypto price lookup"""
        coin_id = kwargs.get("coin_id") or query.lower().replace(" ", "-")
        
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    f"{self.base_url}/finance/crypto/price/{coin_id}",
                    params={"vs_currency": "usd"}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("success"):
                        return {
                            "success": True,
                            "data": str(data.get("data", {})),
                            "source": "coingecko"
                        }
                
                return {
                    "success": False,
                    "error": f"API returned status {response.status_code}",
                    "source": "coingecko"
                }
        except Exception as e:
            logger.error(f"CryptoPriceTool error: {e}", exc_info=True)
            return {
                "success": False,
                "error": str(e),
                "source": "coingecko"
            }


class StockQuoteTool(BaseTool):
    """Tool to fetch stock quotes"""
    
    def __init__(self):
        super().__init__(
            name="stock_quote",
            description="Fetch stock quote data from multiple providers"
        )
        self.base_url = os.getenv("APP_URL", "http://localhost:8000") + "/api"
    
    async def execute(self, query: str, **kwargs) -> Dict[str, Any]:
        """Execute stock quote lookup"""
        symbol = kwargs.get("symbol") or query.upper()
        
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    f"{self.base_url}/finance/stock/quote/{symbol}"
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("success"):
                        return {
                            "success": True,
                            "data": str(data.get("data", {})),
                            "source": data.get("source", "finance_api")
                        }
                
                return {
                    "success": False,
                    "error": f"API returned status {response.status_code}",
                    "source": "finance_api"
                }
        except Exception as e:
            logger.error(f"StockQuoteTool error: {e}", exc_info=True)
            return {
                "success": False,
                "error": str(e),
                "source": "finance_api"
            }


class MarketSummaryTool(BaseTool):
    """Tool to fetch market summary"""
    
    def __init__(self):
        super().__init__(
            name="market_summary",
            description="Fetch overall market summary and indices"
        )
        self.base_url = os.getenv("APP_URL", "http://localhost:8000") + "/api"
    
    async def execute(self, query: str, **kwargs) -> Dict[str, Any]:
        """Execute market summary lookup"""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    f"{self.base_url}/finance/market/summary"
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("success"):
                        return {
                            "success": True,
                            "data": str(data.get("data", {})),
                            "source": "finance_api"
                        }
                
                return {
                    "success": False,
                    "error": f"API returned status {response.status_code}",
                    "source": "finance_api"
                }
        except Exception as e:
            logger.error(f"MarketSummaryTool error: {e}", exc_info=True)
            return {
                "success": False,
                "error": str(e),
                "source": "finance_api"
            }


class CurrencyRateTool(BaseTool):
    """Tool to fetch currency exchange rates"""
    
    def __init__(self):
        super().__init__(
            name="currency_rate",
            description="Fetch currency exchange rates"
        )
        self.base_url = os.getenv("APP_URL", "http://localhost:8000") + "/api"
    
    async def execute(self, query: str, **kwargs) -> Dict[str, Any]:
        """Execute currency rate lookup"""
        from_currency = kwargs.get("from_currency", "USD")
        to_currency = kwargs.get("to_currency", "EUR")
        
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    f"{self.base_url}/exchange/rate",
                    params={"from": from_currency, "to": to_currency}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return {
                        "success": True,
                        "data": str(data),
                        "source": "exchange_api"
                    }
                
                return {
                    "success": False,
                    "error": f"API returned status {response.status_code}",
                    "source": "exchange_api"
                }
        except Exception as e:
            logger.error(f"CurrencyRateTool error: {e}", exc_info=True)
            return {
                "success": False,
                "error": str(e),
                "source": "exchange_api"
            }


class MarketNewsTool(BaseTool):
    """Tool to fetch market news"""
    
    def __init__(self):
        super().__init__(
            name="market_news",
            description="Fetch financial market news"
        )
        self.base_url = os.getenv("APP_URL", "http://localhost:8000") + "/api"
    
    async def execute(self, query: str, **kwargs) -> Dict[str, Any]:
        """Execute market news lookup"""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    f"{self.base_url}/finance/market/news",
                    params={"limit": 5}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("success"):
                        return {
                            "success": True,
                            "data": str(data.get("data", [])),
                            "source": "finance_api"
                        }
                
                return {
                    "success": False,
                    "error": f"API returned status {response.status_code}",
                    "source": "finance_api"
                }
        except Exception as e:
            logger.error(f"MarketNewsTool error: {e}", exc_info=True)
            return {
                "success": False,
                "error": str(e),
                "source": "finance_api"
            }



