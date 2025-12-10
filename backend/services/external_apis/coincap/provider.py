"""CoinCap Provider - Cryptocurrency data from CoinCap API"""
import aiohttp
from typing import Dict, Any, Optional
from services.http_client import http_client


class CoinCapProvider:
    """Provider for CoinCap cryptocurrency API - Free, no API key required"""
    
    BASE_URL = "https://api.coincap.io/v2"
    
    def __init__(self):
        self.timeout = aiohttp.ClientTimeout(total=15)
    
    async def get_assets(self, limit: int = 100, search: Optional[str] = None) -> Dict[str, Any]:
        """Get cryptocurrency assets list"""
        try:
            async with aiohttp.ClientSession(timeout=self.timeout) as session:
                params = {"limit": limit}
                if search:
                    params["search"] = search
                
                async with session.get(f"{self.BASE_URL}/assets", params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        assets = data.get("data", [])
                        
                        # Format response
                        formatted = []
                        for asset in assets[:limit]:
                            formatted.append({
                                "id": asset.get("id"),
                                "name": asset.get("name"),
                                "symbol": asset.get("symbol"),
                                "price_usd": float(asset.get("priceUsd", 0)) if asset.get("priceUsd") else None,
                                "change_24h": float(asset.get("changePercent24Hr", 0)) if asset.get("changePercent24Hr") else None,
                                "market_cap": float(asset.get("marketCapUsd", 0)) if asset.get("marketCapUsd") else None,
                                "rank": int(asset.get("rank", 0)) if asset.get("rank") else None,
                            })
                        
                        return {
                            "count": len(formatted),
                            "assets": formatted,
                            "source": "CoinCap"
                        }
                    else:
                        return {"error": f"CoinCap returned status {response.status}", "assets": []}
                    
        except Exception as e:
            return {"error": str(e), "assets": []}
    
    async def get_asset(self, asset_id: str) -> Dict[str, Any]:
        """Get specific cryptocurrency by ID (e.g., bitcoin, ethereum)"""
        try:
            async with aiohttp.ClientSession(timeout=self.timeout) as session:
                async with session.get(f"{self.BASE_URL}/assets/{asset_id}") as response:
                    if response.status == 200:
                        data = (await response.json()).get("data", {})
                        
                        return {
                            "found": True,
                            "id": data.get("id"),
                            "name": data.get("name"),
                            "symbol": data.get("symbol"),
                            "price_usd": float(data.get("priceUsd", 0)) if data.get("priceUsd") else None,
                            "change_24h": float(data.get("changePercent24Hr", 0)) if data.get("changePercent24Hr") else None,
                            "market_cap": float(data.get("marketCapUsd", 0)) if data.get("marketCapUsd") else None,
                            "volume_24h": float(data.get("volumeUsd24Hr", 0)) if data.get("volumeUsd24Hr") else None,
                            "supply": float(data.get("supply", 0)) if data.get("supply") else None,
                            "max_supply": float(data.get("maxSupply", 0)) if data.get("maxSupply") else None,
                            "rank": int(data.get("rank", 0)) if data.get("rank") else None,
                            "source": "CoinCap"
                        }
                    else:
                        return {"found": False, "error": f"Asset not found: {asset_id}"}
                    
        except Exception as e:
            return {"found": False, "error": str(e)}
    
    async def get_asset_history(self, asset_id: str, interval: str = "d1") -> Dict[str, Any]:
        """Get asset price history"""
        try:
            response = await http_client.get(
                f"{self.BASE_URL}/assets/{asset_id}/history",
                params={"interval": interval}
            )
            
            if response.status_code == 200:
                data = response.json().get("data", [])
                
                # Return last 30 data points
                history = []
                for point in data[-30:]:
                    history.append({
                        "price_usd": float(point.get("priceUsd", 0)) if point.get("priceUsd") else None,
                        "time": point.get("time"),
                        "date": point.get("date")
                    })
                
                return {
                    "asset_id": asset_id,
                    "interval": interval,
                    "history": history,
                    "source": "CoinCap"
                }
            else:
                return {"error": f"History not found for {asset_id}", "history": []}
                
        except Exception as e:
            return {"error": str(e), "history": []}
    
    async def get_markets(self, limit: int = 100) -> Dict[str, Any]:
        """Get cryptocurrency markets"""
        try:
            response = await http_client.get(
                f"{self.BASE_URL}/markets",
                params={"limit": limit}
            )
            
            if response.status_code == 200:
                data = response.json().get("data", [])
                
                markets = []
                for market in data[:limit]:
                    markets.append({
                        "exchange_id": market.get("exchangeId"),
                        "base_symbol": market.get("baseSymbol"),
                        "quote_symbol": market.get("quoteSymbol"),
                        "price_usd": float(market.get("priceUsd", 0)) if market.get("priceUsd") else None,
                        "volume_24h": float(market.get("volumeUsd24Hr", 0)) if market.get("volumeUsd24Hr") else None,
                    })
                
                return {
                    "count": len(markets),
                    "markets": markets,
                    "source": "CoinCap"
                }
            else:
                return {"error": "Markets not available", "markets": []}
                
        except Exception as e:
            return {"error": str(e), "markets": []}
    
    async def get_exchanges(self) -> Dict[str, Any]:
        """Get cryptocurrency exchanges"""
        try:
            response = await http_client.get(f"{self.BASE_URL}/exchanges")
            
            if response.status_code == 200:
                data = response.json().get("data", [])
                
                exchanges = []
                for exchange in data[:50]:  # Top 50
                    exchanges.append({
                        "id": exchange.get("exchangeId"),
                        "name": exchange.get("name"),
                        "rank": int(exchange.get("rank", 0)) if exchange.get("rank") else None,
                        "volume_usd": float(exchange.get("volumeUsd", 0)) if exchange.get("volumeUsd") else None,
                        "trading_pairs": int(exchange.get("tradingPairs", 0)) if exchange.get("tradingPairs") else None,
                    })
                
                return {
                    "count": len(exchanges),
                    "exchanges": exchanges,
                    "source": "CoinCap"
                }
            else:
                return {"error": "Exchanges not available", "exchanges": []}
                
        except Exception as e:
            return {"error": str(e), "exchanges": []}
