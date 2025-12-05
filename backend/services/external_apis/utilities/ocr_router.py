"""
OCR Router
"""
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class OCRRouter:
    """Router for OCR with fallback"""
    
    def __init__(self):
        self.providers = []
        self._init_providers()
    
    def _init_providers(self):
        """Initialize OCR providers"""
        from .ocr_providers import OCRSpace, Optiic
        
        # OCR.space (free key always works)
        try:
            self.providers.append({
                'name': 'ocrspace',
                'instance': OCRSpace()
            })
            logger.info("✅ OCR.space provider initialized")
        except Exception as e:
            logger.warning(f"⚠️ OCR.space failed: {e}")
        
        # Optiic
        try:
            self.providers.append({
                'name': 'optiic',
                'instance': Optiic()
            })
            logger.info("✅ Optiic provider initialized")
        except Exception as e:
            logger.warning(f"⚠️ Optiic failed: {e}")
    
    async def extract_text(
        self,
        image_url: str = None,
        image_base64: str = None,
        language: str = 'eng'
    ) -> Dict[str, Any]:
        """Extract text from image with fallback"""
        errors = []
        
        for provider in self.providers:
            name = provider['name']
            instance = provider['instance']
            
            try:
                logger.info(f"🔄 Extracting text with {name}...")
                result = await instance.extract_text(image_url, image_base64, language)
                
                logger.info(f"✅ Text extracted with {name}")
                return {
                    **result,
                    "provider": name
                }
            
            except Exception as e:
                logger.warning(f"⚠️ {name} failed: {str(e)}")
                errors.append(f"{name}: {str(e)}")
                continue
        
        error_msg = f"All OCR providers failed. Errors: {'; '.join(errors)}"
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
