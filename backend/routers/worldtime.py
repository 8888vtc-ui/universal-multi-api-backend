"""World Time Router - Timezone and time data"""
from fastapi import APIRouter, HTTPException, Query
from services.external_apis.worldtime.provider import WorldTimeProvider
from typing import Dict, Any, List

router = APIRouter(prefix="/api/worldtime", tags=["worldtime"])

provider = WorldTimeProvider()

@router.get("/timezone/{timezone}", response_model=Dict[str, Any])
async def get_timezone(timezone: str):
    """Get time for a specific timezone (e.g., Europe/Paris, America/New_York)"""
    try:
        return await provider.get_timezone(timezone)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/ip", response_model=Dict[str, Any])
async def get_ip_time(ip: str = Query(None, description="IP address (optional, uses caller IP if not provided)")):
    """Get time based on IP address"""
    try:
        return await provider.get_ip_time(ip)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/timezones", response_model=List[str])
async def get_timezones():
    """Get list of all available timezones"""
    try:
        return await provider.get_timezones()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))






