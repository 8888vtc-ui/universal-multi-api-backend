"""
IP Geolocation API Router
Free IP geolocation services
"""
from fastapi import APIRouter, HTTPException, Query
from services.external_apis.ip_geolocation.provider import IPGeolocationProvider
from typing import Optional

router = APIRouter(prefix="/api/ip", tags=["ip-geolocation"])

provider = IPGeolocationProvider()


@router.get("/location/{ip}")
async def get_ip_location(ip: str):
    """Get location by IP address"""
    try:
        result = await provider.get_location(ip)
        return {"success": True, **result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/my-ip")
async def get_my_ip():
    """Get current IP and location"""
    try:
        result = await provider.get_my_ip()
        return {"success": True, **result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))






