"""
Email Providers
SendGrid, Mailgun, Mailjet
"""
import os
import httpx
from typing import Dict, Any, Optional, List


class SendGrid:
    """SendGrid - 100 emails/day free"""
    
    def __init__(self):
        self.api_key = os.getenv('SENDGRID_API_KEY')
        if not self.api_key:
            raise ValueError("SENDGRID_API_KEY not found")
        
        self.base_url = "https://api.sendgrid.com/v3"
        self.available = True
    
    async def send_email(
        self,
        to_email: str,
        from_email: str,
        subject: str,
        content: str,
        content_type: str = 'text/plain'
    ) -> Dict[str, Any]:
        """Send email via SendGrid"""
        async with httpx.AsyncClient() as client:
            url = f"{self.base_url}/mail/send"
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            data = {
                'personalizations': [{
                    'to': [{'email': to_email}]
                }],
                'from': {'email': from_email},
                'subject': subject,
                'content': [{
                    'type': content_type,
                    'value': content
                }]
            }
            
            response = await client.post(url, json=data, headers=headers)
            response.raise_for_status()
            
            return {
                'sent': True,
                'to': to_email,
                'subject': subject
            }


class Mailgun:
    """Mailgun - 5,000 emails/month free"""
    
    def __init__(self):
        self.api_key = os.getenv('MAILGUN_API_KEY')
        self.domain = os.getenv('MAILGUN_DOMAIN')
        
        if not self.api_key or not self.domain:
            raise ValueError("MAILGUN_API_KEY and MAILGUN_DOMAIN required")
        
        self.base_url = f"https://api.mailgun.net/v3/{self.domain}"
        self.available = True
    
    async def send_email(
        self,
        to_email: str,
        from_email: str,
        subject: str,
        content: str,
        content_type: str = 'text/plain'
    ) -> Dict[str, Any]:
        """Send email via Mailgun"""
        async with httpx.AsyncClient() as client:
            url = f"{self.base_url}/messages"
            
            data = {
                'from': from_email,
                'to': to_email,
                'subject': subject
            }
            
            if content_type == 'text/html':
                data['html'] = content
            else:
                data['text'] = content
            
            response = await client.post(
                url,
                auth=('api', self.api_key),
                data=data
            )
            response.raise_for_status()
            
            result = response.json()
            return {
                'sent': True,
                'to': to_email,
                'subject': subject,
                'id': result.get('id')
            }


class Mailjet:
    """Mailjet - 6,000 emails/month or 200/day free"""
    
    def __init__(self):
        self.api_key = os.getenv('MAILJET_API_KEY')
        self.api_secret = os.getenv('MAILJET_API_SECRET')
        
        if not self.api_key or not self.api_secret:
            raise ValueError("MAILJET_API_KEY and MAILJET_API_SECRET required")
        
        self.base_url = "https://api.mailjet.com/v3.1"
        self.available = True
    
    async def send_email(
        self,
        to_email: str,
        from_email: str,
        subject: str,
        content: str,
        content_type: str = 'text/plain'
    ) -> Dict[str, Any]:
        """Send email via Mailjet"""
        async with httpx.AsyncClient() as client:
            url = f"{self.base_url}/send"
            
            message = {
                'From': {'Email': from_email},
                'To': [{'Email': to_email}],
                'Subject': subject
            }
            
            if content_type == 'text/html':
                message['HTMLPart'] = content
            else:
                message['TextPart'] = content
            
            data = {'Messages': [message]}
            
            response = await client.post(
                url,
                auth=(self.api_key, self.api_secret),
                json=data
            )
            response.raise_for_status()
            
            result = response.json()
            return {
                'sent': True,
                'to': to_email,
                'subject': subject,
                'message_id': result['Messages'][0]['To'][0]['MessageID']
            }
