"""CoinCap Provider - Cryptocurrency data"""
import httpx
from typing import List, Dict, Any, Optional

class CoinCapProvider:
    """Provider for CoinCap API (free, unlimited)"""
    
    # Fallback crypto data
    FALLBACK_ASSETS = [
        {"id": "bitcoin", "symbol": "BTC", "name": "Bitcoin", "priceUsd": "43000.00"},
        {"id": "ethereum", "symbol": "ETH", "name": "Ethereum", "priceUsd": "2300.00"},
        {"id": "tether", "symbol": "USDT", "name": "Tether", "priceUsd": "1.00"},
        {"id": "binance-coin", "symbol": "BNB", "name": "BNB", "priceUsd": "310.00"},
        {"id": "solana", "symbol": "SOL", "name": "Solana", "priceUsd": "100.00"},
    ]
    
    def __init__(self):
        self.base_url = "https://api.coincap.io/v2"
        self.available = True
        print("✅ CoinCap provider initialized (free, unlimited)")
    
    async def get_assets(self, limit: int = 100, search: Optional[str] = None) -> Dict[str, Any]:
        """Get cryptocurrency assets"""
        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                params = {"limit": limit}
                if search:
                    params["search"] = search
                response = await client.get(f"{self.base_url}/assets", params=params)
                if response.status_code == 200:
                    return response.json()
            except:
                pass
            
            # Fallback data
            return {
                "data": self.FALLBACK_ASSETS[:limit],
                "timestamp": None,
                "source": "fallback"
            }
    
    async def get_asset(self, asset_id: str) -> Dict[str, Any]:
        """Get specific asset by ID"""
        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                response = await client.get(f"{self.base_url}/assets/{asset_id}")
                if response.status_code == 200:
                    return response.json()
            except:
                pass
            
            # Fallback
            for asset in self.FALLBACK_ASSETS:
                if asset["id"] == asset_id or asset["symbol"].lower() == asset_id.lower():
                    return {"data": asset, "source": "fallback"}
            
            return {"data": None, "error": "Asset not found"}
    
    async def get_asset_history(self, asset_id: str, interval: str = "d1") -> Dict[str, Any]:
        """Get asset price history"""
        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                response = await client.get(
                    f"{self.base_url}/assets/{asset_id}/history",
                    params={"interval": interval}
                )
                if response.status_code == 200:
                    return response.json()
            except:
                pass
            
            return {"data": [], "source": "fallback", "message": "History not available"}
    
    async def get_markets(self, limit: int = 100) -> Dict[str, Any]:
        """Get markets data"""
        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                response = await client.get(f"{self.base_url}/markets", params={"limit": limit})
                if response.status_code == 200:
                    return response.json()
            except:
                pass
            
            return {"data": [], "source": "fallback", "message": "Markets not available"}
    
    async def get_exchanges(self) -> Dict[str, Any]:
        """Get exchanges data"""
        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                response = await client.get(f"{self.base_url}/exchanges")
                if response.status_code == 200:
                    return response.json()
            except:
                pass
            
            return {"data": [], "source": "fallback", "message": "Exchanges not available"}

