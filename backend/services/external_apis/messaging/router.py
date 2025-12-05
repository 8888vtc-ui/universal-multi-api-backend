"""
Messaging Router
Supports: Telegram, LINE, Kakao
"""
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class MessagingRouter:
    """Router for messaging platforms"""
    
    def __init__(self):
        self.providers = {}
        self._init_providers()
    
    def _init_providers(self):
        """Initialize available messaging providers"""
        import os
        
        # Telegram
        if os.getenv('TELEGRAM_BOT_TOKEN'):
            try:
                from .telegram import TelegramBot
                self.providers['telegram'] = TelegramBot()
                logger.info("✅ Telegram Bot API initialized")
            except Exception as e:
                logger.warning(f"⚠️ Failed to initialize Telegram: {e}")
        
        # LINE (future)
        if os.getenv('LINE_CHANNEL_ACCESS_TOKEN'):
            logger.info("ℹ️ LINE token found but provider not yet implemented")
        
        # Kakao (future)
        if os.getenv('KAKAO_REST_API_KEY'):
            logger.info("ℹ️ Kakao key found but provider not yet implemented")
        
        if not self.providers:
            logger.warning("⚠️ No messaging providers available")
    
    async def send_message(
        self,
        platform: str,
        chat_id: str,
        text: str,
        **kwargs
    ) -> Dict[str, Any]:
        """Send message via specified platform"""
        if platform not in self.providers:
            raise ValueError(f"Platform '{platform}' not available. Available: {list(self.providers.keys())}")
        
        provider = self.providers[platform]
        
        try:
            logger.info(f"📤 Sending message via {platform}...")
            result = await provider.send_message(chat_id, text, **kwargs)
            logger.info(f"✅ Message sent via {platform}")
            return {
                **result,
                "platform": platform
            }
        except Exception as e:
            logger.error(f"❌ Failed to send message via {platform}: {e}")
            raise
    
    async def get_bot_info(self, platform: str) -> Dict[str, Any]:
        """Get bot information"""
        if platform not in self.providers:
            raise ValueError(f"Platform '{platform}' not available")
        
        provider = self.providers[platform]
        
        if hasattr(provider, 'get_me'):
            result = await provider.get_me()
            return {
                **result,
                "platform": platform
            }
        
        raise NotImplementedError(f"get_bot_info not implemented for {platform}")
    
    def get_status(self) -> Dict[str, Any]:
        """Get messaging router status"""
        return {
            "platforms": len(self.providers),
            "available": list(self.providers.keys()),
            "details": [
                {"platform": name, "available": True}
                for name in self.providers.keys()
            ]
        }
