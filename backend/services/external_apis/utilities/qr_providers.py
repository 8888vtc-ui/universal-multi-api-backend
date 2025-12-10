"""
QR Code Providers
QuickChart, goQR, QRCoder
"""
import httpx
from typing import Dict, Any, Optional
import base64
from services.http_client import http_client


class QuickChart:
    """QuickChart - Free QR codes and charts (open-source)"""
    
    def __init__(self):
        self.base_url = "https://quickchart.io"
        self.available = True
    
    async def generate_qr(
        self,
        text: str,
        size: int = 300,
        format: str = 'png'
    ) -> Dict[str, Any]:
        """Generate QR code"""
        url = f"{self.base_url}/qr"
        params = {
            'text': text,
            'size': size,
            'format': format
        }
        
        response = await http_client.get(url, params=params)
        response.raise_for_status()
        
        # Return image URL
        image_url = f"{url}?text={text}&size={size}&format={format}"
        
        return {
            'image_url': image_url,
            'size': size,
            'format': format
        }


class GoQR:
    """goQR.me - Free QR code generator"""
    
    def __init__(self):
        self.base_url = "https://api.qrserver.com/v1"
        self.available = True
    
    async def generate_qr(
        self,
        text: str,
        size: int = 300,
        format: str = 'png'
    ) -> Dict[str, Any]:
        """Generate QR code"""
        # goQR doesn't need actual API call, just URL
        image_url = f"{self.base_url}/create-qr-code/?data={text}&size={size}x{size}&format={format}"
        
        return {
            'image_url': image_url,
            'size': size,
            'format': format
        }
