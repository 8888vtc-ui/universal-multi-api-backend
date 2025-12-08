"""RandomUser Provider - Generate random user data"""
import httpx
from typing import List, Dict, Any, Optional

class RandomUserProvider:
    """Provider for RandomUser API (free, unlimited)"""
    
    def __init__(self):
        self.base_url = "https://randomuser.me/api"
        self.available = True
        print("[OK] RandomUser provider initialized (free, unlimited)")
    
    async def get_users(self, count: int = 1, gender: Optional[str] = None, nationality: Optional[str] = None) -> Dict[str, Any]:
        """Get random users"""
        async with httpx.AsyncClient(timeout=10.0) as client:
            params = {"results": count}
            if gender:
                params["gender"] = gender
            if nationality:
                params["nat"] = nationality
            response = await client.get(self.base_url, params=params)
            response.raise_for_status()
            return response.json()






