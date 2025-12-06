"""
Discord Webhook Provider
Free unlimited webhooks for notifications
"""
import httpx
from typing import Optional, Dict, Any
import os


class DiscordWebhookProvider:
    """Discord Webhook - Unlimited free"""
    
    def __init__(self):
        self.available = True
        print("✅ Discord Webhook provider initialized (free, unlimited)")
    
    async def send_message(
        self,
        webhook_url: str,
        content: str,
        username: Optional[str] = None,
        avatar_url: Optional[str] = None,
        embeds: Optional[list] = None
    ) -> Dict[str, Any]:
        """Send message to Discord webhook"""
        async with httpx.AsyncClient(timeout=30.0) as client:
            payload = {"content": content}
            
            if username:
                payload["username"] = username
            if avatar_url:
                payload["avatar_url"] = avatar_url
            if embeds:
                payload["embeds"] = embeds
            
            response = await client.post(webhook_url, json=payload)
            
            if response.status_code in [200, 204]:
                return {"success": True, "message": "Sent to Discord"}
            else:
                raise Exception(f"Discord webhook returned status {response.status_code}: {response.text}")
    
    async def send_embed(
        self,
        webhook_url: str,
        title: str,
        description: str,
        color: Optional[int] = None,
        fields: Optional[list] = None,
        footer: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """Send embed message to Discord webhook"""
        embed = {
            "title": title,
            "description": description
        }
        
        if color:
            embed["color"] = color
        if fields:
            embed["fields"] = fields
        if footer:
            embed["footer"] = footer
        
        return await self.send_message(webhook_url, "", embeds=[embed])

