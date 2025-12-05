"""
Translation Router with Intelligent Fallback
Supports: Google Translate, DeepL, Yandex, LibreTranslate
"""
import os
import logging
from typing import Optional, Dict, Any
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class TranslationRouter:
    """Intelligent router for translation with automatic fallback"""
    
    def __init__(self):
        self.providers = []
        self.quota_usage = {}
        self.last_reset = {}
        
        # Initialize providers based on available API keys
        self._init_providers()
    
    def _init_providers(self):
        """Initialize available translation providers"""
        from .google import GoogleTranslate
        from .deepl import DeepLTranslate
        from .yandex import YandexTranslate
        from .libre import LibreTranslate
        
        # Priority order with quotas (chars/month)
        potential_providers = [
            ('google', GoogleTranslate, 500000, os.getenv('GOOGLE_TRANSLATE_API_KEY')),
            ('deepl', DeepLTranslate, 500000, os.getenv('DEEPL_API_KEY')),
            ('yandex', YandexTranslate, 100000, os.getenv('YANDEX_TRANSLATE_API_KEY')),
            ('libre', LibreTranslate, float('inf'), True)  # Always available (self-hosted option)
        ]
        
        for name, provider_class, quota, api_key in potential_providers:
            if api_key:
                try:
                    provider = provider_class()
                    self.providers.append({
                        'name': name,
                        'instance': provider,
                        'quota': quota,
                        'available': True
                    })
                    self.quota_usage[name] = 0
                    self.last_reset[name] = datetime.now()
                    logger.info(f"✅ {name.capitalize()} translation provider initialized (quota: {quota:,} chars/month)")
                except Exception as e:
                    logger.warning(f"⚠️ Failed to initialize {name}: {e}")
        
        if not self.providers:
            logger.error("❌ No translation providers available!")
    
    def _check_quota(self, provider_name: str, text_length: int) -> bool:
        """Check if provider has enough quota"""
        if provider_name not in self.quota_usage:
            return False
        
        provider = next((p for p in self.providers if p['name'] == provider_name), None)
        if not provider:
            return False
        
        # Reset quota if month has passed
        if datetime.now() - self.last_reset[provider_name] > timedelta(days=30):
            self.quota_usage[provider_name] = 0
            self.last_reset[provider_name] = datetime.now()
        
        # Check if quota available
        if provider['quota'] == float('inf'):
            return True
        
        return self.quota_usage[provider_name] + text_length <= provider['quota']
    
    def _log_usage(self, provider_name: str, text_length: int):
        """Log API usage"""
        if provider_name in self.quota_usage:
            self.quota_usage[provider_name] += text_length
    
    async def translate(
        self,
        text: str,
        source_lang: str = 'auto',
        target_lang: str = 'en'
    ) -> Dict[str, Any]:
        """
        Translate text with automatic fallback
        
        Args:
            text: Text to translate
            source_lang: Source language code (auto-detect if 'auto')
            target_lang: Target language code
        
        Returns:
            {
                "translation": "translated text",
                "source_lang": "detected/provided source",
                "target_lang": "target language",
                "provider": "provider used",
                "chars_used": 123
            }
        """
        text_length = len(text)
        errors = []
        
        for provider in self.providers:
            name = provider['name']
            instance = provider['instance']
            
            # Check quota
            if not self._check_quota(name, text_length):
                logger.warning(f"⚠️ {name.capitalize()} quota exceeded, trying next provider...")
                errors.append(f"{name}: quota exceeded")
                continue
            
            # Try translation
            try:
                logger.info(f"🔄 Attempting translation with {name.capitalize()}...")
                result = await instance.translate(text, source_lang, target_lang)
                
                # Log usage
                self._log_usage(name, text_length)
                
                logger.info(f"✅ Translation successful with {name.capitalize()}")
                return {
                    "translation": result['translation'],
                    "source_lang": result.get('source_lang', source_lang),
                    "target_lang": target_lang,
                    "provider": name,
                    "chars_used": text_length
                }
            
            except Exception as e:
                logger.warning(f"⚠️ {name.capitalize()} failed: {str(e)}")
                errors.append(f"{name}: {str(e)}")
                continue
        
        # All providers failed
        error_msg = f"All translation providers failed. Errors: {'; '.join(errors)}"
        logger.error(f"❌ {error_msg}")
        raise Exception(error_msg)
    
    async def detect_language(self, text: str) -> Dict[str, Any]:
        """Detect language of text"""
        for provider in self.providers:
            try:
                result = await provider['instance'].detect_language(text)
                return {
                    "language": result['language'],
                    "confidence": result.get('confidence', 1.0),
                    "provider": provider['name']
                }
            except:
                continue
        
        raise Exception("Language detection failed with all providers")
    
    def get_status(self) -> Dict[str, Any]:
        """Get router status and quota usage"""
        status = {
            "providers": len(self.providers),
            "details": []
        }
        
        for provider in self.providers:
            name = provider['name']
            quota = provider['quota']
            used = self.quota_usage.get(name, 0)
            
            status["details"].append({
                "name": name,
                "available": provider['available'],
                "quota": quota if quota != float('inf') else "unlimited",
                "used": used,
                "remaining": quota - used if quota != float('inf') else "unlimited"
            })
        
        return status
