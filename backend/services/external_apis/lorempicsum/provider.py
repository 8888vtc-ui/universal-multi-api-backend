"""Lorem Picsum Provider - Placeholder images"""
import httpx
from typing import Dict, Any, List, Optional

class LoremPicsumProvider:
    """Provider for Lorem Picsum API (free, unlimited)"""
    
    def __init__(self):
        self.base_url = "https://picsum.photos"
        self.available = True
        print("✅ Lorem Picsum provider initialized (free, unlimited)")
    
    async def get_image_url(self, width: int = 800, height: int = 600, seed: Optional[int] = None) -> Dict[str, Any]:
        """Get a random image URL"""
        url = f"{self.base_url}/{width}/{height}"
        if seed:
            url += f"?random={seed}"
        return {
            "url": url,
            "width": width,
            "height": height,
            "seed": seed
        }
    
    async def get_image_info(self, image_id: int) -> Dict[str, Any]:
        """Get image info by ID"""
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{self.base_url}/id/{image_id}/info")
            response.raise_for_status()
            return response.json()
    
    async def get_list(self, page: int = 1, limit: int = 30) -> List[Dict[str, Any]]:
        """Get list of images"""
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{self.base_url}/v2/list", params={"page": page, "limit": limit})
            response.raise_for_status()
            return response.json()

