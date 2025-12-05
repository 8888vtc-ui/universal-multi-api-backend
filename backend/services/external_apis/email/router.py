"""
Email Router
"""
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


class EmailRouter:
    """Router for email with fallback"""
    
    def __init__(self):
        self.providers = []
        self._init_providers()
    
    def _init_providers(self):
        """Initialize email providers"""
        from .providers import SendGrid, Mailgun, Mailjet
        import os
        
        # SendGrid
        if os.getenv('SENDGRID_API_KEY'):
            try:
                self.providers.append({
                    'name': 'sendgrid',
                    'instance': SendGrid()
                })
                logger.info("✅ SendGrid email provider initialized")
            except Exception as e:
                logger.warning(f"⚠️ SendGrid failed: {e}")
        
        # Mailgun
        if os.getenv('MAILGUN_API_KEY') and os.getenv('MAILGUN_DOMAIN'):
            try:
                self.providers.append({
                    'name': 'mailgun',
                    'instance': Mailgun()
                })
                logger.info("✅ Mailgun email provider initialized")
            except Exception as e:
                logger.warning(f"⚠️ Mailgun failed: {e}")
        
        # Mailjet
        if os.getenv('MAILJET_API_KEY') and os.getenv('MAILJET_API_SECRET'):
            try:
                self.providers.append({
                    'name': 'mailjet',
                    'instance': Mailjet()
                })
                logger.info("✅ Mailjet email provider initialized")
            except Exception as e:
                logger.warning(f"⚠️ Mailjet failed: {e}")
    
    async def send_email(
        self,
        to_email: str,
        from_email: str,
        subject: str,
        content: str,
        content_type: str = 'text/plain'
    ) -> Dict[str, Any]:
        """Send email with fallback"""
        errors = []
        
        for provider in self.providers:
            name = provider['name']
            instance = provider['instance']
            
            try:
                logger.info(f"📧 Sending email with {name}...")
                result = await instance.send_email(
                    to_email, from_email, subject, content, content_type
                )
                
                logger.info(f"✅ Email sent with {name}")
                return {
                    **result,
                    "provider": name
                }
            
            except Exception as e:
                logger.warning(f"⚠️ {name} failed: {str(e)}")
                errors.append(f"{name}: {str(e)}")
                continue
        
        error_msg = f"All email providers failed. Errors: {'; '.join(errors)}"
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
