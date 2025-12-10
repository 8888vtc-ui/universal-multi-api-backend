"""Slack Webhook Provider"""
import httpx
from typing import Dict, Any, Optional
from services.http_client import http_client

class SlackWebhookProvider:
    """Provider for Slack Webhooks (free, unlimited)"""
    
    def __init__(self):
        self.available = True
        print("[OK] Slack Webhook provider initialized (free, unlimited)")
    
    async def send_message(self, webhook_url: str, text: str, channel: Optional[str] = None, username: Optional[str] = None) -> Dict[str, Any]:
        """Send a simple message to Slack"""
        payload = {"text": text}
        if channel:
            payload["channel"] = channel
        if username:
            payload["username"] = username
        
        response = await http_client.post(webhook_url, json=payload)
        response.raise_for_status()
        return {"success": True, "status_code": response.status_code}
    
    async def send_rich_message(self, webhook_url: str, blocks: list, channel: Optional[str] = None) -> Dict[str, Any]:
        """Send a rich message with blocks to Slack"""
        payload = {"blocks": blocks}
        if channel:
            payload["channel"] = channel
        
        response = await http_client.post(webhook_url, json=payload)
        response.raise_for_status()
        return {"success": True, "status_code": response.status_code}






