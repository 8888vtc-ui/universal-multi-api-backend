"""Dog and Cat API Providers"""
import httpx
from typing import Dict, Any, List

class DogAPIProvider:
    """Provider for Dog API (free, unlimited)"""
    
    def __init__(self):
        self.base_url = "https://dog.ceo/api"
        self.available = True
        print("[OK] Dog API initialized (free, unlimited)")
    
    async def get_random_image(self) -> Dict[str, Any]:
        """Get a random dog image"""
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{self.base_url}/breeds/image/random")
            response.raise_for_status()
            data = response.json()
            return {
                "image_url": data.get("message"),
                "status": data.get("status")
            }
    
    async def get_random_images(self, count: int = 5) -> Dict[str, Any]:
        """Get multiple random dog images"""
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{self.base_url}/breeds/image/random/{count}")
            response.raise_for_status()
            data = response.json()
            return {
                "images": data.get("message", []),
                "count": len(data.get("message", [])),
                "status": data.get("status")
            }
    
    async def get_breeds(self) -> List[str]:
        """Get all dog breeds"""
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{self.base_url}/breeds/list/all")
            response.raise_for_status()
            data = response.json()
            return list(data.get("message", {}).keys())
    
    async def get_breed_images(self, breed: str, count: int = 5) -> Dict[str, Any]:
        """Get images of a specific breed"""
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{self.base_url}/breed/{breed}/images/random/{count}")
            response.raise_for_status()
            data = response.json()
            return {
                "breed": breed,
                "images": data.get("message", []),
                "count": len(data.get("message", [])),
                "status": data.get("status")
            }


class CatAPIProvider:
    """Provider for Cat API (free, unlimited)"""
    
    def __init__(self):
        self.base_url = "https://api.thecatapi.com/v1"
        self.available = True
        print("[OK] Cat API initialized (free, unlimited)")
    
    async def get_random_image(self) -> Dict[str, Any]:
        """Get a random cat image"""
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{self.base_url}/images/search")
            response.raise_for_status()
            data = response.json()
            if data:
                return {
                    "image_url": data[0].get("url"),
                    "width": data[0].get("width"),
                    "height": data[0].get("height"),
                    "id": data[0].get("id")
                }
            return {"error": "No image found"}
    
    async def get_random_images(self, count: int = 5) -> Dict[str, Any]:
        """Get multiple random cat images"""
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                f"{self.base_url}/images/search",
                params={"limit": count}
            )
            response.raise_for_status()
            data = response.json()
            return {
                "images": [img.get("url") for img in data],
                "count": len(data)
            }






