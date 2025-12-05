"""
Space Router
NASA APIs
"""
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


class SpaceRouter:
    """Router for space/NASA APIs"""
    
    def __init__(self):
        self.nasa = None
        self._init_providers()
    
    def _init_providers(self):
        """Initialize NASA provider"""
        try:
            from .nasa import NASAProvider
            self.nasa = NASAProvider()
            logger.info("✅ NASA APIs initialized")
        except Exception as e:
            logger.error(f"❌ Failed to initialize NASA: {e}")
    
    async def get_apod(self, date: str = None) -> Dict[str, Any]:
        """Get Astronomy Picture of the Day"""
        if not self.nasa:
            raise Exception("NASA provider not available")
        
        try:
            result = await self.nasa.get_apod(date)
            return {**result, "provider": "nasa"}
        except Exception as e:
            logger.error(f"❌ APOD failed: {e}")
            raise
    
    async def get_mars_photos(self, rover: str, sol: int, camera: str = None) -> Dict[str, Any]:
        """Get Mars Rover photos"""
        if not self.nasa:
            raise Exception("NASA provider not available")
        
        try:
            result = await self.nasa.get_mars_rover_photos(rover, sol, camera)
            return {**result, "provider": "nasa"}
        except Exception as e:
            logger.error(f"❌ Mars photos failed: {e}")
            raise
    
    async def get_neo_feed(self, start_date: str = None, end_date: str = None) -> Dict[str, Any]:
        """Get Near Earth Objects"""
        if not self.nasa:
            raise Exception("NASA provider not available")
        
        try:
            result = await self.nasa.get_neo_feed(start_date, end_date)
            return {**result, "provider": "nasa"}
        except Exception as e:
            logger.error(f"❌ NEO feed failed: {e}")
            raise
    
    async def get_epic_images(self) -> Dict[str, Any]:
        """Get EPIC Earth images"""
        if not self.nasa:
            raise Exception("NASA provider not available")
        
        try:
            result = await self.nasa.get_epic_images()
            return {**result, "provider": "nasa"}
        except Exception as e:
            logger.error(f"❌ EPIC images failed: {e}")
            raise
    
    def get_status(self) -> Dict[str, Any]:
        """Get router status"""
        return {
            "provider": "nasa",
            "available": self.nasa is not None,
            "apis": ["apod", "mars_rover", "neo", "epic"]
        }
