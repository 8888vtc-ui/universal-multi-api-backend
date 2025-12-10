"""
Google Translate API Provider
Free tier: 500,000 characters/month
"""
import os
import httpx
from typing import Dict, Any
from services.http_client import http_client


class GoogleTranslate:
    """Google Cloud Translation API"""
    
    def __init__(self):
        self.api_key = os.getenv('GOOGLE_TRANSLATE_API_KEY')
        if not self.api_key:
            raise ValueError("GOOGLE_TRANSLATE_API_KEY not found in environment")
        
        self.base_url = "https://translation.googleapis.com/language/translate/v2"
        self.available = True
    
    async def translate(
        self,
        text: str,
        source_lang: str = 'auto',
        target_lang: str = 'en'
    ) -> Dict[str, Any]:
        """Translate text using Google Translate API"""
        params = {
            'key': self.api_key,
            'q': text,
            'target': target_lang
        }
        
        if source_lang != 'auto':
            params['source'] = source_lang
        
        response = await http_client.post(self.base_url, params=params)
        response.raise_for_status()
        
        data = response.json()
        translation = data['data']['translations'][0]
        
        return {
            'translation': translation['translatedText'],
            'source_lang': translation.get('detectedSourceLanguage', source_lang)
        }
    
    async def detect_language(self, text: str) -> Dict[str, Any]:
        """Detect language of text"""
        url = "https://translation.googleapis.com/language/translate/v2/detect"
        params = {
            'key': self.api_key,
            'q': text
        }
        
        response = await http_client.post(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        detection = data['data']['detections'][0][0]
        
        return {
            'language': detection['language'],
            'confidence': detection['confidence']
        }
