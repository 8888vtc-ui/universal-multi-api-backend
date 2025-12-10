"""
Telegram Bot API Provider
Free tier: Unlimited (rate limits only)
900M+ users worldwide
"""
import os
import httpx
from typing import Dict, Any, Optional, List
from services.http_client import http_client


class TelegramBot:
    """Telegram Bot API - Most popular bot platform"""
    
    def __init__(self):
        self.bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        if not self.bot_token:
            raise ValueError("TELEGRAM_BOT_TOKEN not found in environment")
        
        self.base_url = f"https://api.telegram.org/bot{self.bot_token}"
        self.available = True
    
    async def send_message(
        self,
        chat_id: str,
        text: str,
        parse_mode: Optional[str] = None,
        reply_markup: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Send text message to a chat"""
        url = f"{self.base_url}/sendMessage"
        
        data = {
            'chat_id': chat_id,
            'text': text
        }
        
        if parse_mode:
            data['parse_mode'] = parse_mode
        
        if reply_markup:
            data['reply_markup'] = reply_markup
        
        response = await http_client.post(url, json=data)
        response.raise_for_status()
        
        result = response.json()
        return {
            'message_id': result['result']['message_id'],
            'chat_id': result['result']['chat']['id'],
            'sent': True
        }
    
    async def send_photo(
        self,
        chat_id: str,
        photo_url: str,
        caption: Optional[str] = None
    ) -> Dict[str, Any]:
        """Send photo to a chat"""
        url = f"{self.base_url}/sendPhoto"
        
        data = {
            'chat_id': chat_id,
            'photo': photo_url
        }
        
        if caption:
            data['caption'] = caption
        
        response = await http_client.post(url, json=data)
        response.raise_for_status()
        
        result = response.json()
        return {
            'message_id': result['result']['message_id'],
            'sent': True
        }
    
    async def get_updates(
        self,
        offset: Optional[int] = None,
        limit: int = 100
    ) -> Dict[str, Any]:
        """Get incoming updates (messages, commands, etc.)"""
        url = f"{self.base_url}/getUpdates"
        
        params = {'limit': limit}
        if offset:
            params['offset'] = offset
        
        response = await http_client.get(url, params=params)
        response.raise_for_status()
        
        result = response.json()
        return {
            'updates': result['result'],
            'count': len(result['result'])
        }
    
    async def set_webhook(
        self,
        webhook_url: str,
        secret_token: Optional[str] = None
    ) -> Dict[str, Any]:
        """Set webhook for receiving updates"""
        url = f"{self.base_url}/setWebhook"
        
        data = {'url': webhook_url}
        
        if secret_token:
            data['secret_token'] = secret_token
        
        response = await http_client.post(url, json=data)
        response.raise_for_status()
        
        result = response.json()
        return {
            'webhook_set': result['result'],
            'url': webhook_url
        }
    
    async def get_me(self) -> Dict[str, Any]:
        """Get bot information"""
        url = f"{self.base_url}/getMe"
        
        response = await http_client.get(url)
        response.raise_for_status()
        
        result = response.json()
        bot_info = result['result']
        
        return {
            'id': bot_info['id'],
            'username': bot_info['username'],
            'first_name': bot_info['first_name'],
            'can_join_groups': bot_info.get('can_join_groups', False),
            'can_read_all_group_messages': bot_info.get('can_read_all_group_messages', False)
        }
    
    async def send_document(
        self,
        chat_id: str,
        document_url: str,
        caption: Optional[str] = None
    ) -> Dict[str, Any]:
        """Send document to a chat"""
        url = f"{self.base_url}/sendDocument"
        
        data = {
            'chat_id': chat_id,
            'document': document_url
        }
        
        if caption:
            data['caption'] = caption
        
        response = await http_client.post(url, json=data)
        response.raise_for_status()
        
        result = response.json()
        return {
            'message_id': result['result']['message_id'],
            'sent': True
        }
