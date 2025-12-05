"""
QR Code Router
"""
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


class QRRouter:
    """Router for QR code generation"""
    
    def __init__(self):
        self.providers = []
        self._init_providers()
    
    def _init_providers(self):
        """Initialize QR code providers"""
        from .qr_providers import QuickChart, GoQR
        
        # Both are always available (no API key needed)
        try:
            self.providers.append({
                'name': 'quickchart',
                'instance': QuickChart()
            })
            logger.info("✅ QuickChart QR provider initialized")
        except Exception as e:
            logger.warning(f"⚠️ QuickChart failed: {e}")
        
        try:
            self.providers.append({
                'name': 'goqr',
                'instance': GoQR()
            })
            logger.info("✅ goQR provider initialized")
        except Exception as e:
            logger.warning(f"⚠️ goQR failed: {e}")
    
    async def generate_qr(
        self,
        text: str,
        size: int = 300,
        format: str = 'png'
    ) -> Dict[str, Any]:
        """Generate QR code with fallback"""
        errors = []
        
        for provider in self.providers:
            name = provider['name']
            instance = provider['instance']
            
            try:
                logger.info(f"🔄 Generating QR with {name}...")
                result = await instance.generate_qr(text, size, format)
                
                logger.info(f"✅ QR generated with {name}")
                return {
                    **result,
                    "provider": name,
                    "text": text
                }
            
            except Exception as e:
                logger.warning(f"⚠️ {name} failed: {str(e)}")
                errors.append(f"{name}: {str(e)}")
                continue
        
        error_msg = f"All QR providers failed. Errors: {'; '.join(errors)}"
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
