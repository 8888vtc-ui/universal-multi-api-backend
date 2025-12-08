"""
IP Geolocation Provider
Free IP geolocation services
"""
import httpx
import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()


class IPGeolocationProvider:
    """IP Geolocation - Multiple free providers"""
    
    async def get_location(self, ip: str) -> Dict[str, Any]:
        """Get location by IP address"""
        # Try ipapi.co first (free, no key needed)
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(f"https://ipapi.co/{ip}/json/")
                if response.status_code == 200:
                    data = response.json()
                    if "error" not in data:
                        return {
                            "ip": ip,
                            "country": data.get("country_name"),
                            "country_code": data.get("country_code"),
                            "city": data.get("city"),
                            "region": data.get("region"),
                            "latitude": data.get("latitude"),
                            "longitude": data.get("longitude"),
                            "timezone": data.get("timezone"),
                            "isp": data.get("org"),
                            "provider": "ipapi.co"
                        }
        except:
            pass
        
        # Fallback to ip-api.com (free, no key needed)
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(f"http://ip-api.com/json/{ip}")
                if response.status_code == 200:
                    data = response.json()
                    if data.get("status") == "success":
                        return {
                            "ip": ip,
                            "country": data.get("country"),
                            "country_code": data.get("countryCode"),
                            "city": data.get("city"),
                            "region": data.get("regionName"),
                            "latitude": data.get("lat"),
                            "longitude": data.get("lon"),
                            "timezone": data.get("timezone"),
                            "isp": data.get("isp"),
                            "provider": "ip-api.com"
                        }
        except:
            pass
        
        raise Exception("Failed to get IP geolocation from all providers")
    
    async def get_my_ip(self) -> Dict[str, Any]:
        """Get current IP and location"""
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                # Get IP first
                ip_response = await client.get("https://api.ipify.org?format=json")
                if ip_response.status_code == 200:
                    ip = ip_response.json().get("ip")
                    if ip:
                        return await self.get_location(ip)
        except:
            pass
        
        raise Exception("Failed to get current IP")






