"""CoinCap Router - Cryptocurrency data"""
from fastapi import APIRouter, HTTPException, Query
from services.external_apis.coincap.provider import CoinCapProvider
from typing import Dict, Any, Optional

router = APIRouter(prefix="/api/coincap", tags=["coincap"])

provider = CoinCapProvider()

@router.get("/assets", response_model=Dict[str, Any])
async def get_assets(
    limit: int = Query(100, ge=1, le=2000),
    search: Optional[str] = Query(None, description="Search query")
):
    """Get cryptocurrency assets"""
    try:
        return await provider.get_assets(limit, search)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/assets/{asset_id}", response_model=Dict[str, Any])
async def get_asset(asset_id: str):
    """Get specific asset by ID (e.g., bitcoin, ethereum)"""
    try:
        return await provider.get_asset(asset_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/assets/{asset_id}/history", response_model=Dict[str, Any])
async def get_asset_history(
    asset_id: str,
    interval: str = Query("d1", description="Interval (m1, m5, m15, m30, h1, h2, h6, h12, d1)")
):
    """Get asset price history"""
    try:
        return await provider.get_asset_history(asset_id, interval)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/markets", response_model=Dict[str, Any])
async def get_markets(limit: int = Query(100, ge=1, le=2000)):
    """Get markets data"""
    try:
        return await provider.get_markets(limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/exchanges", response_model=Dict[str, Any])
async def get_exchanges():
    """Get exchanges data"""
    try:
        return await provider.get_exchanges()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))






