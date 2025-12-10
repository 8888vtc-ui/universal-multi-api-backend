"""
OCR Providers
OCR.space, Optiic
"""
import os
import httpx
from typing import Dict, Any, Optional
import base64
from services.http_client import http_client


class OCRSpace:
    """OCR.space - Free OCR API (500/day)"""
    
    def __init__(self):
        self.api_key = os.getenv('OCRSPACE_API_KEY', 'helloworld')  # Free key
        self.base_url = "https://api.ocr.space/parse/image"
        self.available = True
    
    async def extract_text(
        self,
        image_url: str = None,
        image_base64: str = None,
        language: str = 'eng'
    ) -> Dict[str, Any]:
        """Extract text from image"""
        data = {
            'apikey': self.api_key,
            'language': language,
            'isOverlayRequired': False
        }
        
        if image_url:
            data['url'] = image_url
        elif image_base64:
            data['base64Image'] = f"data:image/png;base64,{image_base64}"
        else:
            raise ValueError("Either image_url or image_base64 required")
        
        response = await http_client.post(self.base_url, data=data)
        response.raise_for_status()
        
        result = response.json()
        
        if result.get('IsErroredOnProcessing'):
            raise Exception(result.get('ErrorMessage', ['Unknown error'])[0])
        
        # Extract all text
        text_results = []
        for parsed_result in result.get('ParsedResults', []):
            text_results.append(parsed_result.get('ParsedText', ''))
        
        return {
            'text': '\n'.join(text_results),
            'language': language,
            'processing_time': result.get('ProcessingTimeInMilliseconds', 0)
        }


class Optiic:
    """Optiic - Free OCR API"""
    
    def __init__(self):
        self.base_url = "https://api.optiic.dev/process"
        self.available = True
    
    async def extract_text(
        self,
        image_url: str = None,
        image_base64: str = None,
        language: str = 'eng'
    ) -> Dict[str, Any]:
        """Extract text from image"""
        if image_url:
            data = {'url': image_url}
        elif image_base64:
            data = {'image': image_base64}
        else:
            raise ValueError("Either image_url or image_base64 required")
        
        response = await http_client.post(self.base_url, json=data)
        response.raise_for_status()
        
        result = response.json()
        
        return {
            'text': result.get('text', ''),
            'language': language
        }
