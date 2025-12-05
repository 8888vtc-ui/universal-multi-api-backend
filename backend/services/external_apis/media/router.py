"""
Media Router
"""
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


class MediaRouter:
    """Router for media (photos, videos, GIFs)"""
    
    def __init__(self):
        self.providers = {}
        self._init_providers()
    
    def _init_providers(self):
        """Initialize media providers"""
        from .providers import Unsplash, Pexels, Giphy
        import os
        
        # Unsplash
        if os.getenv('UNSPLASH_ACCESS_KEY'):
            try:
                self.providers['unsplash'] = Unsplash()
                logger.info("✅ Unsplash initialized")
            except Exception as e:
                logger.warning(f"⚠️ Unsplash failed: {e}")
        
        # Pexels
        if os.getenv('PEXELS_API_KEY'):
            try:
                self.providers['pexels'] = Pexels()
                logger.info("✅ Pexels initialized")
            except Exception as e:
                logger.warning(f"⚠️ Pexels failed: {e}")
        
        # Giphy
        if os.getenv('GIPHY_API_KEY'):
            try:
                self.providers['giphy'] = Giphy()
                logger.info("✅ Giphy initialized")
            except Exception as e:
                logger.warning(f"⚠️ Giphy failed: {e}")
    
    async def search_photos(self, query: str, per_page: int = 10) -> Dict[str, Any]:
        """Search photos (Unsplash or Pexels)"""
        errors = []
        
        # Try Unsplash first
        if 'unsplash' in self.providers:
            try:
                result = await self.providers['unsplash'].search_photos(query, per_page)
                return {**result, "provider": "unsplash"}
            except Exception as e:
                errors.append(f"unsplash: {e}")
        
        # Fallback to Pexels
        if 'pexels' in self.providers:
            try:
                result = await self.providers['pexels'].search_photos(query, per_page)
                return {**result, "provider": "pexels"}
            except Exception as e:
                errors.append(f"pexels: {e}")
        
        raise Exception(f"Photo search failed: {'; '.join(errors)}")
    
    async def search_videos(self, query: str, per_page: int = 10) -> Dict[str, Any]:
        """Search videos (Pexels)"""
        if 'pexels' not in self.providers:
            raise Exception("Pexels not available")
        
        try:
            result = await self.providers['pexels'].search_videos(query, per_page)
            return {**result, "provider": "pexels"}
        except Exception as e:
            raise Exception(f"Video search failed: {e}")
    
    async def search_gifs(self, query: str, limit: int = 10) -> Dict[str, Any]:
        """Search GIFs (Giphy)"""
        if 'giphy' not in self.providers:
            raise Exception("Giphy not available")
        
        try:
            result = await self.providers['giphy'].search_gifs(query, limit)
            return {**result, "provider": "giphy"}
        except Exception as e:
            raise Exception(f"GIF search failed: {e}")
    
    def get_status(self) -> Dict[str, Any]:
        """Get router status"""
        return {
            "providers": list(self.providers.keys()),
            "count": len(self.providers)
        }
