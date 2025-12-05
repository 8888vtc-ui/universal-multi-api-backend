"""
Sports Router
"""
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


class SportsRouter:
    """Router for sports APIs"""
    
    def __init__(self):
        self.apisports = None
        self._init_providers()
    
    def _init_providers(self):
        """Initialize sports providers"""
        import os
        
        if os.getenv('APISPORTS_KEY'):
            try:
                from .apisports import APISports
                self.apisports = APISports()
                logger.info("✅ API-Sports initialized")
            except Exception as e:
                logger.warning(f"⚠️ Failed to initialize API-Sports: {e}")
    
    async def get_live_matches(self) -> Dict[str, Any]:
        """Get live matches"""
        if not self.apisports:
            raise Exception("Sports provider not available")
        
        try:
            result = await self.apisports.get_live_matches()
            return {**result, "provider": "apisports"}
        except Exception as e:
            logger.error(f"❌ Live matches failed: {e}")
            raise
    
    async def get_standings(self, league_id: int, season: int) -> Dict[str, Any]:
        """Get league standings"""
        if not self.apisports:
            raise Exception("Sports provider not available")
        
        try:
            result = await self.apisports.get_league_standings(league_id, season)
            return {**result, "provider": "apisports"}
        except Exception as e:
            logger.error(f"❌ Standings failed: {e}")
            raise
    
    async def get_team(self, team_id: int) -> Dict[str, Any]:
        """Get team info"""
        if not self.apisports:
            raise Exception("Sports provider not available")
        
        try:
            result = await self.apisports.get_team_info(team_id)
            return {**result, "provider": "apisports"}
        except Exception as e:
            logger.error(f"❌ Team info failed: {e}")
            raise
    
    def get_status(self) -> Dict[str, Any]:
        """Get router status"""
        return {
            "provider": "apisports",
            "available": self.apisports is not None
        }
