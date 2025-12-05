"""
Yandex Translate API Provider
Free tier: ~100,000 characters/month
"""
import os
import httpx
from typing import Dict, Any


class YandexTranslate:
    """Yandex Cloud Translation API"""
    
    def __init__(self):
        self.api_key = os.getenv('YANDEX_TRANSLATE_API_KEY')
        if not self.api_key:
            raise ValueError("YANDEX_TRANSLATE_API_KEY not found in environment")
        
        self.base_url = "https://translate.api.cloud.yandex.net/translate/v2"
        self.available = True
    
    async def translate(
        self,
        text: str,
        source_lang: str = 'auto',
        target_lang: str = 'en'
    ) -> Dict[str, Any]:
        """Translate text using Yandex Translate API"""
        async with httpx.AsyncClient() as client:
            url = f"{self.base_url}/translate"
            
            headers = {
                'Authorization': f'Api-Key {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            data = {
                'texts': [text],
                'targetLanguageCode': target_lang
            }
            
            if source_lang != 'auto':
                data['sourceLanguageCode'] = source_lang
            
            response = await client.post(url, json=data, headers=headers)
            response.raise_for_status()
            
            result = response.json()
            translation = result['translations'][0]
            
            return {
                'translation': translation['text'],
                'source_lang': translation.get('detectedLanguageCode', source_lang)
            }
    
    async def detect_language(self, text: str) -> Dict[str, Any]:
        """Detect language using Yandex API"""
        async with httpx.AsyncClient() as client:
            url = f"{self.base_url}/detect"
            
            headers = {
                'Authorization': f'Api-Key {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            data = {'text': text}
            
            response = await client.post(url, json=data, headers=headers)
            response.raise_for_status()
            
            result = response.json()
            
            return {
                'language': result['languageCode'],
                'confidence': 1.0  # Yandex doesn't provide confidence
            }
