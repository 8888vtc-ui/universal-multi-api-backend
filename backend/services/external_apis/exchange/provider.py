"""Exchange Rate Provider"""
import httpx
from typing import Dict, Any, List, Optional

class ExchangeRateProvider:
    """Provider for ExchangeRate-API (free, 1,500/month)"""
    
    def __init__(self):
        self.base_url = "https://open.er-api.com/v6"
        self.available = True
        print("[OK] Exchange Rate API initialized (free, 1,500/month)")
    
    async def get_rates(self, base_currency: str = "USD") -> Dict[str, Any]:
        """Get exchange rates for a base currency"""
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{self.base_url}/latest/{base_currency}")
            response.raise_for_status()
            data = response.json()
            
            return {
                "base": data.get("base_code"),
                "rates": data.get("rates", {}),
                "time_last_updated": data.get("time_last_update_utc"),
                "time_next_update": data.get("time_next_update_utc")
            }
    
    async def convert(
        self,
        amount: float,
        from_currency: str,
        to_currency: str
    ) -> Dict[str, Any]:
        """Convert amount from one currency to another"""
        rates_data = await self.get_rates(from_currency)
        rates = rates_data.get("rates", {})
        
        if to_currency not in rates:
            raise ValueError(f"Currency {to_currency} not found")
        
        rate = rates[to_currency]
        converted = amount * rate
        
        return {
            "amount": amount,
            "from": from_currency,
            "to": to_currency,
            "rate": rate,
            "converted": round(converted, 2)
        }
    
    async def get_supported_currencies(self) -> List[str]:
        """Get list of supported currencies"""
        data = await self.get_rates("USD")
        return list(data.get("rates", {}).keys())






