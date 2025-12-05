"""
News Router with Intelligent Fallback
Supports: NewsAPI.org, NewsData.io
"""
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class NewsRouter:
    """Intelligent router for news with automatic fallback"""
    
    def __init__(self):
        self.providers = []
        self._init_providers()
    
    def _init_providers(self):
        """Initialize available news providers"""
        from .providers import NewsAPIOrg, NewsDataIO
        
        import os
        
        # Priority order
        potential_providers = [
            ('newsapi_org', NewsAPIOrg, os.getenv('NEWSAPI_ORG_KEY')),
            ('newsdata_io', NewsDataIO, os.getenv('NEWSDATA_IO_KEY'))
        ]
        
        for name, provider_class, api_key in potential_providers:
            if api_key:
                try:
                    provider = provider_class()
                    self.providers.append({
                        'name': name,
                        'instance': provider
                    })
                    logger.info(f"✅ {name.replace('_', '.').upper()} news provider initialized")
                except Exception as e:
                    logger.warning(f"⚠️ Failed to initialize {name}: {e}")
        
        if not self.providers:
            logger.error("❌ No news providers available!")
    
    async def search(
        self,
        query: str,
        language: str = 'en',
        page_size: int = 10
    ) -> Dict[str, Any]:
        """Search news with automatic fallback"""
        errors = []
        
        for provider in self.providers:
            name = provider['name']
            instance = provider['instance']
            
            try:
                logger.info(f"🔄 Searching news with {name}...")
                result = await instance.search(query, language, page_size)
                
                logger.info(f"✅ News search successful with {name}")
                return {
                    **result,
                    "provider": name
                }
            
            except Exception as e:
                logger.warning(f"⚠️ {name} failed: {str(e)}")
                errors.append(f"{name}: {str(e)}")
                continue
        
        error_msg = f"All news providers failed. Errors: {'; '.join(errors)}"
        logger.error(f"❌ {error_msg}")
        raise Exception(error_msg)
    
    async def get_top_headlines(
        self,
        country: str = 'us',
        category: Optional[str] = None,
        page_size: int = 10
    ) -> Dict[str, Any]:
        """Get top headlines with automatic fallback"""
        errors = []
        
        for provider in self.providers:
            name = provider['name']
            instance = provider['instance']
            
            try:
                logger.info(f"🔄 Getting headlines from {name}...")
                result = await instance.get_top_headlines(country, category, page_size)
                
                logger.info(f"✅ Headlines retrieved from {name}")
                return {
                    **result,
                    "provider": name
                }
            
            except Exception as e:
                logger.warning(f"⚠️ {name} failed: {str(e)}")
                errors.append(f"{name}: {str(e)}")
                continue
        
        error_msg = f"All news providers failed. Errors: {'; '.join(errors)}"
        logger.error(f"❌ {error_msg}")
        raise Exception(error_msg)
    
    def get_status(self) -> Dict[str, Any]:
        """Get router status"""
        return {
            "providers": len(self.providers),
            "details": [
                {"name": p['name'], "available": True}
                for p in self.providers
            ]
        }
