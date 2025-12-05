"""
DeepL Translation API Provider
Free tier: 500,000 characters/month
"""
import os
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


class DeepLTranslate:
    """DeepL Translation API"""
    
    def __init__(self):
        self.api_key = os.getenv('DEEPL_API_KEY')
        if not self.api_key:
            raise ValueError("DEEPL_API_KEY not found in environment")
        
        # Free API uses api-free.deepl.com, paid uses api.deepl.com
        self.base_url = "https://api-free.deepl.com/v2"
        self.available = True
        logger.info("✅ DeepL translation provider initialized")
    
    async def translate(
        self,
        text: str,
        source_lang: str = 'auto',
        target_lang: str = 'EN'
    ) -> Dict[str, Any]:
        """Translate text using DeepL API"""
        from services.http_client import http_client
        
        url = f"{self.base_url}/translate"
        
        data = {
            'auth_key': self.api_key,
            'text': text,
            'target_lang': target_lang.upper()
        }
        
        if source_lang != 'auto':
            data['source_lang'] = source_lang.upper()
        
        try:
            response = await http_client.post(url, data=data)
            response.raise_for_status()
            
            result = response.json()
            translation = result['translations'][0]
            
            return {
                'translation': translation['text'],
                'source_lang': translation.get('detected_source_language', source_lang).lower()
            }
        except Exception as e:
            logger.error(f"DeepL translation error: {e}")
            raise
    
    async def detect_language(self, text: str) -> Dict[str, Any]:
        """Detect language (DeepL doesn't have dedicated endpoint, use translate with auto)"""
        result = await self.translate(text, 'auto', 'EN')
        return {
            'language': result['source_lang'],
            'confidence': 1.0  # DeepL doesn't provide confidence
        }
