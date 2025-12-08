"""Bored Router - Activity suggestions"""
from fastapi import APIRouter, HTTPException, Query
from services.external_apis.bored.provider import BoredAPIProvider
from typing import Dict, Any, List, Optional

router = APIRouter(prefix="/api/bored", tags=["bored"])

bored_provider = BoredAPIProvider()


@router.get("/activity", response_model=Dict[str, Any])
async def get_random_activity(
    type: Optional[str] = Query(None, description="Activity type"),
    participants: Optional[int] = Query(None, ge=1, le=10),
    min_price: Optional[float] = Query(None, ge=0, le=1),
    max_price: Optional[float] = Query(None, ge=0, le=1)
):
    """Get a random activity suggestion when you're bored"""
    try:
        return await bored_provider.get_random_activity(type, participants, min_price, max_price)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/types", response_model=List[str])
async def get_activity_types():
    """Get available activity types"""
    return bored_provider.get_activity_types()






