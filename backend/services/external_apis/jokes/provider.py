"""Jokes Provider - Random jokes from multiple sources"""
import httpx
from typing import Dict, Any, Optional, List
from services.http_client import http_client

class JokeAPIProvider:
    """Provider for JokeAPI (free, unlimited)"""
    
    def __init__(self):
        self.base_url = "https://v2.jokeapi.dev"
        self.available = True
        print("[OK] JokeAPI provider initialized (free, unlimited)")
    
    async def get_random_joke(
        self,
        category: str = "Any",
        language: str = "en",
        safe_mode: bool = True
    ) -> Dict[str, Any]:
        """Get a random joke"""
        flags = "nsfw,religious,political,racist,sexist" if safe_mode else ""
        params = {"lang": language}
        if safe_mode:
            params["blacklistFlags"] = flags
        
        response = await http_client.get(
            f"{self.base_url}/joke/{category}",
            params=params
        )
        response.raise_for_status()
        data = response.json()
        
        # Formater la réponse
        if data.get("type") == "single":
            return {
                "type": "single",
                "joke": data.get("joke"),
                "category": data.get("category"),
                "language": language
            }
        else:
            return {
                "type": "twopart",
                "setup": data.get("setup"),
                "delivery": data.get("delivery"),
                "category": data.get("category"),
                "language": language
            }
    
    async def get_categories(self) -> List[str]:
        """Get available joke categories"""
        return ["Any", "Programming", "Misc", "Dark", "Pun", "Spooky", "Christmas"]


class ChuckNorrisProvider:
    """Provider for Chuck Norris Jokes API (free, unlimited)"""
    
    def __init__(self):
        self.base_url = "https://api.chucknorris.io"
        self.available = True
        print("[OK] Chuck Norris API initialized (free, unlimited)")
    
    async def get_random_joke(self, category: Optional[str] = None) -> Dict[str, Any]:
        """Get a random Chuck Norris joke"""
        url = f"{self.base_url}/jokes/random"
        if category:
            url += f"?category={category}"
        
        response = await http_client.get(url)
        response.raise_for_status()
        data = response.json()
        
        return {
            "joke": data.get("value"),
            "id": data.get("id"),
            "icon_url": data.get("icon_url"),
            "categories": data.get("categories", [])
        }
    
    async def get_categories(self) -> List[str]:
        """Get available categories"""
        response = await http_client.get(f"{self.base_url}/jokes/categories")
        response.raise_for_status()
        return response.json()






