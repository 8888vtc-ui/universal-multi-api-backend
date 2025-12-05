"""
Webhook System
Notifications pour événements importants
"""
import os
import hashlib
import hmac
import time
import json
import asyncio
import logging
from typing import Dict, Any, List, Optional, Callable
from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum
import httpx

logger = logging.getLogger(__name__)


class WebhookEvent(str, Enum):
    """Types d'événements webhook"""
    QUOTA_LOW = "quota.low"
    QUOTA_EXHAUSTED = "quota.exhausted"
    API_ERROR = "api.error"
    API_RECOVERED = "api.recovered"
    RATE_LIMIT_EXCEEDED = "rate_limit.exceeded"
    NEW_USER = "user.created"
    REQUEST_COMPLETED = "request.completed"
    HEALTH_CHECK_FAILED = "health.failed"


@dataclass
class WebhookConfig:
    """Configuration d'un webhook"""
    id: str
    url: str
    secret: str
    events: List[WebhookEvent]
    active: bool = True
    retry_count: int = 3
    timeout: float = 10.0
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class WebhookPayload:
    """Payload d'un webhook"""
    event: WebhookEvent
    data: Dict[str, Any]
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    webhook_id: str = ""


class WebhookManager:
    """Gestionnaire de webhooks"""
    
    def __init__(self):
        self.webhooks: Dict[str, WebhookConfig] = {}
        self.delivery_history: List[Dict[str, Any]] = []
        self._load_webhooks_from_env()
    
    def _load_webhooks_from_env(self):
        """Charger les webhooks depuis les variables d'environnement"""
        # Format: WEBHOOK_1_URL, WEBHOOK_1_SECRET, WEBHOOK_1_EVENTS
        i = 1
        while True:
            url = os.getenv(f"WEBHOOK_{i}_URL")
            if not url:
                break
            
            secret = os.getenv(f"WEBHOOK_{i}_SECRET", "")
            events_str = os.getenv(f"WEBHOOK_{i}_EVENTS", "")
            
            events = []
            if events_str:
                for event_name in events_str.split(","):
                    try:
                        events.append(WebhookEvent(event_name.strip()))
                    except ValueError:
                        logger.warning(f"Unknown webhook event: {event_name}")
            
            if events:
                webhook = WebhookConfig(
                    id=f"webhook_{i}",
                    url=url,
                    secret=secret,
                    events=events
                )
                self.webhooks[webhook.id] = webhook
                logger.info(f"Loaded webhook: {webhook.id} -> {url}")
            
            i += 1
    
    def register_webhook(self, config: WebhookConfig) -> str:
        """Enregistrer un nouveau webhook"""
        self.webhooks[config.id] = config
        logger.info(f"Registered webhook: {config.id}")
        return config.id
    
    def unregister_webhook(self, webhook_id: str) -> bool:
        """Supprimer un webhook"""
        if webhook_id in self.webhooks:
            del self.webhooks[webhook_id]
            logger.info(f"Unregistered webhook: {webhook_id}")
            return True
        return False
    
    def _generate_signature(self, payload: str, secret: str) -> str:
        """Générer la signature HMAC-SHA256"""
        return hmac.new(
            secret.encode('utf-8'),
            payload.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
    
    async def _send_webhook(
        self,
        webhook: WebhookConfig,
        payload: WebhookPayload
    ) -> bool:
        """Envoyer un webhook avec retry"""
        payload_dict = {
            "event": payload.event.value,
            "data": payload.data,
            "timestamp": payload.timestamp,
            "webhook_id": webhook.id
        }
        payload_json = json.dumps(payload_dict)
        
        headers = {
            "Content-Type": "application/json",
            "X-Webhook-Event": payload.event.value,
            "X-Webhook-Timestamp": str(int(time.time())),
        }
        
        # Ajouter la signature si secret configuré
        if webhook.secret:
            signature = self._generate_signature(payload_json, webhook.secret)
            headers["X-Webhook-Signature"] = f"sha256={signature}"
        
        # Retry logic
        for attempt in range(webhook.retry_count):
            try:
                async with httpx.AsyncClient(timeout=webhook.timeout) as client:
                    response = await client.post(
                        webhook.url,
                        content=payload_json,
                        headers=headers
                    )
                    
                    if response.status_code in [200, 201, 202, 204]:
                        self._record_delivery(webhook.id, payload.event, True)
                        logger.info(f"Webhook sent: {webhook.id} -> {payload.event.value}")
                        return True
                    else:
                        logger.warning(
                            f"Webhook failed: {webhook.id} -> {response.status_code}"
                        )
            
            except Exception as e:
                logger.error(f"Webhook error: {webhook.id} -> {e}")
            
            # Attendre avant retry (backoff exponentiel)
            if attempt < webhook.retry_count - 1:
                await asyncio.sleep(2 ** attempt)
        
        self._record_delivery(webhook.id, payload.event, False)
        return False
    
    def _record_delivery(self, webhook_id: str, event: WebhookEvent, success: bool):
        """Enregistrer l'historique de livraison"""
        self.delivery_history.append({
            "webhook_id": webhook_id,
            "event": event.value,
            "success": success,
            "timestamp": datetime.now().isoformat()
        })
        
        # Garder seulement les 1000 derniers
        if len(self.delivery_history) > 1000:
            self.delivery_history = self.delivery_history[-1000:]
    
    async def trigger(self, event: WebhookEvent, data: Dict[str, Any]):
        """Déclencher un événement webhook"""
        payload = WebhookPayload(event=event, data=data)
        
        # Trouver tous les webhooks qui écoutent cet événement
        tasks = []
        for webhook in self.webhooks.values():
            if webhook.active and event in webhook.events:
                tasks.append(self._send_webhook(webhook, payload))
        
        # Envoyer en parallèle
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
    
    def get_delivery_history(self, webhook_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Obtenir l'historique de livraison"""
        if webhook_id:
            return [h for h in self.delivery_history if h["webhook_id"] == webhook_id]
        return self.delivery_history
    
    def get_status(self) -> Dict[str, Any]:
        """Obtenir le statut des webhooks"""
        return {
            "total_webhooks": len(self.webhooks),
            "active_webhooks": sum(1 for w in self.webhooks.values() if w.active),
            "recent_deliveries": len(self.delivery_history),
            "webhooks": [
                {
                    "id": w.id,
                    "url": w.url[:50] + "..." if len(w.url) > 50 else w.url,
                    "events": [e.value for e in w.events],
                    "active": w.active
                }
                for w in self.webhooks.values()
            ]
        }


# Singleton
webhook_manager = WebhookManager()


# Helper functions
async def trigger_webhook(event: WebhookEvent, data: Dict[str, Any]):
    """Helper pour déclencher un webhook"""
    await webhook_manager.trigger(event, data)


# Decorateur pour déclencher webhooks automatiquement
def webhook_on_error(event: WebhookEvent = WebhookEvent.API_ERROR):
    """Decorateur pour déclencher webhook sur erreur"""
    def decorator(func: Callable):
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                await trigger_webhook(event, {
                    "function": func.__name__,
                    "error": str(e),
                    "args": str(args)[:200],
                })
                raise
        return wrapper
    return decorator


