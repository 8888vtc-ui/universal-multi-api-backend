"""
📢 NOTIFICATION AGENT
Sends alerts via Telegram, Email, Slack, Discord.
Uses Groq for fast message formatting.
"""
import os
import httpx
from typing import Dict, Any, List
from .base_agent import BaseAgent
import logging

logger = logging.getLogger(__name__)


class NotificationAgent(BaseAgent):
    """Sends notifications across multiple channels"""
    
    def __init__(self):
        super().__init__(
            name="📢 Notification Agent",
            model="groq-llama3",
            role="Envoie des alertes et notifications via Telegram, Email, Slack"
        )
        self.telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID")
        self.slack_webhook = os.getenv("SLACK_WEBHOOK_URL")
        self.discord_webhook = os.getenv("DISCORD_WEBHOOK_URL")
    
    async def _do_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        action = task.get("action", "send_alert")
        
        actions = {
            "send_alert": self._send_alert,
            "send_telegram": self._send_telegram,
            "send_slack": self._send_slack,
            "send_discord": self._send_discord,
            "send_all": self._send_all,
            "format_message": self._format_message,
            "check_status": self._check_status,
        }
        
        handler = actions.get(action)
        if handler:
            return await handler(task)
        else:
            return {"success": False, "error": f"Unknown action: {action}"}
    
    async def _send_alert(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Send alert to best available channel"""
        message = task.get("message", "")
        level = task.get("level", "info")  # info, warning, error, critical
        title = task.get("title", "Alert")
        
        # Format message with AI
        formatted = await self._format_alert_message(title, message, level)
        
        # Try channels in priority order
        results = []
        
        if self.telegram_token and self.telegram_chat_id:
            result = await self._send_telegram({"message": formatted, "parse_mode": "HTML"})
            results.append({"channel": "telegram", **result})
        
        if self.slack_webhook:
            result = await self._send_slack({"message": formatted, "level": level})
            results.append({"channel": "slack", **result})
        
        if self.discord_webhook:
            result = await self._send_discord({"message": formatted, "level": level})
            results.append({"channel": "discord", **result})
        
        success = any(r.get("success") for r in results)
        return {
            "success": success,
            "channels_notified": [r["channel"] for r in results if r.get("success")],
            "results": results
        }
    
    async def _format_alert_message(self, title: str, message: str, level: str) -> str:
        """Format alert message with AI"""
        emoji = {
            "info": "ℹ️",
            "warning": "⚠️",
            "error": "❌",
            "critical": "🚨"
        }.get(level, "📢")
        
        prompt = f"""
        Formate ce message d'alerte de manière concise et professionnelle:
        
        Titre: {title}
        Niveau: {level}
        Message: {message}
        
        Format attendu:
        - Emoji approprié
        - Titre en gras
        - Message clair
        - Actions suggérées si applicable
        - Maximum 500 caractères
        
        Retourne uniquement le message formaté.
        """
        
        try:
            formatted = await self.think(prompt)
            return f"{emoji} {formatted}"
        except:
            return f"{emoji} <b>{title}</b>\n\n{message}"
    
    async def _send_telegram(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Send message via Telegram"""
        message = task.get("message", "")
        chat_id = task.get("chat_id", self.telegram_chat_id)
        parse_mode = task.get("parse_mode", "HTML")
        
        if not self.telegram_token:
            return {"success": False, "error": "Telegram bot token not configured"}
        
        if not chat_id:
            return {"success": False, "error": "Telegram chat ID not configured"}
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"https://api.telegram.org/bot{self.telegram_token}/sendMessage",
                    json={
                        "chat_id": chat_id,
                        "text": message[:4096],  # Telegram limit
                        "parse_mode": parse_mode,
                        "disable_web_page_preview": True
                    }
                )
                data = response.json()
                
                if data.get("ok"):
                    logger.info(f"✅ Telegram message sent to {chat_id}")
                    return {"success": True, "message_id": data.get("result", {}).get("message_id")}
                else:
                    return {"success": False, "error": data.get("description", "Unknown error")}
                    
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _send_slack(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Send message via Slack webhook"""
        message = task.get("message", "")
        level = task.get("level", "info")
        channel = task.get("channel")  # Optional override
        
        webhook_url = task.get("webhook_url", self.slack_webhook)
        
        if not webhook_url:
            return {"success": False, "error": "Slack webhook URL not configured"}
        
        # Color based on level
        color = {
            "info": "#36a64f",
            "warning": "#ffcc00",
            "error": "#ff0000",
            "critical": "#8b0000"
        }.get(level, "#36a64f")
        
        try:
            payload = {
                "attachments": [{
                    "color": color,
                    "text": message,
                    "mrkdwn_in": ["text"]
                }]
            }
            
            if channel:
                payload["channel"] = channel
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(webhook_url, json=payload)
                
                if response.status_code == 200:
                    logger.info("✅ Slack message sent")
                    return {"success": True}
                else:
                    return {"success": False, "error": f"HTTP {response.status_code}"}
                    
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _send_discord(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Send message via Discord webhook"""
        message = task.get("message", "")
        level = task.get("level", "info")
        
        webhook_url = task.get("webhook_url", self.discord_webhook)
        
        if not webhook_url:
            return {"success": False, "error": "Discord webhook URL not configured"}
        
        # Color based on level (Discord uses decimal colors)
        color = {
            "info": 3066993,     # Green
            "warning": 16776960, # Yellow
            "error": 15158332,   # Red
            "critical": 10038562 # Dark red
        }.get(level, 3066993)
        
        try:
            payload = {
                "embeds": [{
                    "description": message[:2048],  # Discord limit
                    "color": color
                }]
            }
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(webhook_url, json=payload)
                
                if response.status_code in [200, 204]:
                    logger.info("✅ Discord message sent")
                    return {"success": True}
                else:
                    return {"success": False, "error": f"HTTP {response.status_code}"}
                    
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _send_all(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Send to all configured channels"""
        message = task.get("message", "")
        level = task.get("level", "info")
        title = task.get("title", "Notification")
        
        formatted = await self._format_alert_message(title, message, level)
        
        results = {}
        
        # Telegram
        if self.telegram_token and self.telegram_chat_id:
            results["telegram"] = await self._send_telegram({"message": formatted})
        
        # Slack
        if self.slack_webhook:
            results["slack"] = await self._send_slack({"message": formatted, "level": level})
        
        # Discord
        if self.discord_webhook:
            results["discord"] = await self._send_discord({"message": formatted, "level": level})
        
        success_count = sum(1 for r in results.values() if r.get("success"))
        
        return {
            "success": success_count > 0,
            "channels_notified": success_count,
            "total_channels": len(results),
            "results": results
        }
    
    async def _format_message(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Format a message using AI"""
        raw_message = task.get("message", "")
        format_type = task.get("format", "alert")  # alert, report, summary
        
        prompt = f"""
        Formate ce message en style '{format_type}':
        
        {raw_message}
        
        Règles:
        - Concis et clair
        - Utilise des emojis appropriés
        - Maximum 1000 caractères
        - Format professionnel
        """
        
        formatted = await self.think(prompt)
        return {"success": True, "formatted_message": formatted}
    
    async def _check_status(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Check status of all notification channels"""
        status = {
            "telegram": {
                "configured": bool(self.telegram_token and self.telegram_chat_id),
                "bot_token": bool(self.telegram_token),
                "chat_id": bool(self.telegram_chat_id)
            },
            "slack": {
                "configured": bool(self.slack_webhook)
            },
            "discord": {
                "configured": bool(self.discord_webhook)
            }
        }
        
        # Test Telegram if configured
        if status["telegram"]["configured"]:
            try:
                async with httpx.AsyncClient(timeout=10.0) as client:
                    response = await client.get(
                        f"https://api.telegram.org/bot{self.telegram_token}/getMe"
                    )
                    data = response.json()
                    status["telegram"]["online"] = data.get("ok", False)
                    if data.get("ok"):
                        status["telegram"]["bot_name"] = data.get("result", {}).get("username")
            except:
                status["telegram"]["online"] = False
        
        return {
            "success": True,
            "channels": status,
            "active_channels": sum(1 for c in status.values() if c.get("configured"))
        }
