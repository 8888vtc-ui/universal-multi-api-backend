"""Bored API Provider - Activity suggestions"""
import httpx
from typing import Dict, Any, Optional

class BoredAPIProvider:
    """Provider for Bored API (free, unlimited)"""
    
    # Predefined activities as fallback
    FALLBACK_ACTIVITIES = [
        {"activity": "Learn a new programming language", "type": "education", "participants": 1, "price": 0, "accessibility": 0.1},
        {"activity": "Go for a walk in nature", "type": "recreational", "participants": 1, "price": 0, "accessibility": 0.1},
        {"activity": "Cook a new recipe", "type": "cooking", "participants": 1, "price": 0.2, "accessibility": 0.2},
        {"activity": "Read a book", "type": "relaxation", "participants": 1, "price": 0, "accessibility": 0.1},
        {"activity": "Start a journal", "type": "relaxation", "participants": 1, "price": 0, "accessibility": 0},
        {"activity": "Learn to play a new instrument", "type": "music", "participants": 1, "price": 0.3, "accessibility": 0.3},
        {"activity": "Volunteer at a local charity", "type": "charity", "participants": 1, "price": 0, "accessibility": 0.2},
        {"activity": "Have a movie marathon", "type": "recreational", "participants": 1, "price": 0.1, "accessibility": 0.1},
        {"activity": "Learn a new language", "type": "education", "participants": 1, "price": 0, "accessibility": 0.1},
        {"activity": "Do a puzzle", "type": "recreational", "participants": 1, "price": 0.1, "accessibility": 0.1},
    ]
    
    def __init__(self):
        self.base_url = "https://bored-api.appbrewery.com/random"
        self.fallback_url = "https://www.boredapi.com/api"
        self.available = True
        print("✅ Bored API initialized (free, unlimited)")
    
    async def get_random_activity(
        self,
        activity_type: Optional[str] = None,
        participants: Optional[int] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None
    ) -> Dict[str, Any]:
        """Get a random activity suggestion"""
        import random
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            # Try primary API
            try:
                response = await client.get(self.base_url)
                if response.status_code == 200:
                    data = response.json()
                    return {
                        "activity": data.get("activity"),
                        "type": data.get("type"),
                        "participants": data.get("participants"),
                        "price": data.get("price"),
                        "link": data.get("link") or None,
                        "accessibility": data.get("accessibility"),
                        "key": data.get("key"),
                        "source": "bored-api"
                    }
            except:
                pass
            
            # Try fallback API
            try:
                params = {}
                if activity_type:
                    params["type"] = activity_type
                if participants:
                    params["participants"] = participants
                
                response = await client.get(f"{self.fallback_url}/activity", params=params)
                if response.status_code == 200:
                    data = response.json()
                    return {
                        "activity": data.get("activity"),
                        "type": data.get("type"),
                        "participants": data.get("participants"),
                        "price": data.get("price"),
                        "link": data.get("link") or None,
                        "accessibility": data.get("accessibility"),
                        "key": data.get("key"),
                        "source": "boredapi"
                    }
            except:
                pass
            
            # Use fallback predefined activities
            activity = random.choice(self.FALLBACK_ACTIVITIES)
            return {
                **activity,
                "link": None,
                "key": str(random.randint(1000000, 9999999)),
                "source": "fallback"
            }
    
    def get_activity_types(self) -> list:
        """Get available activity types"""
        return [
            "education", "recreational", "social", "diy",
            "charity", "cooking", "relaxation", "music", "busywork"
        ]

