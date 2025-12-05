"""
LibreTranslate API Provider
Free tier: Unlimited (self-hosted or public instance)
"""
import httpx
from typing import Dict, Any


class LibreTranslate:
    """LibreTranslate - Open Source Translation API"""
    
    def __init__(self):
        # Use public instance or self-hosted
        self.base_url = "https://libretranslate.com"
        self.api_key = None  # Public instance doesn't require key
        self.available = True
    
    async def translate(
        self,
        text: str,
        source_lang: str = 'auto',
        target_lang: str = 'en'
    ) -> Dict[str, Any]:
        """Translate text using LibreTranslate API"""
        async with httpx.AsyncClient(timeout=30.0) as client:
            url = f"{self.base_url}/translate"
            
            data = {
                'q': text,
                'source': source_lang,
                'target': target_lang,
                'format': 'text'
            }
            
            if self.api_key:
                data['api_key'] = self.api_key
            
            response = await client.post(url, json=data)
            response.raise_for_status()
            
            result = response.json()
            
            return {
                'translation': result['translatedText'],
                'source_lang': result.get('detectedLanguage', {}).get('language', source_lang)
            }
    
    async def detect_language(self, text: str) -> Dict[str, Any]:
        """Detect language using LibreTranslate API"""
        async with httpx.AsyncClient(timeout=30.0) as client:
            url = f"{self.base_url}/detect"
            
            data = {'q': text}
            
            if self.api_key:
                data['api_key'] = self.api_key
            
            response = await client.post(url, json=data)
            response.raise_for_status()
            
            result = response.json()
            
            # LibreTranslate returns array of detections
            if result and len(result) > 0:
                detection = result[0]
                return {
                    'language': detection['language'],
                    'confidence': detection.get('confidence', 1.0)
                }
            
            return {'language': 'unknown', 'confidence': 0.0}
