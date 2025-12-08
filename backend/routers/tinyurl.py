"""TinyURL Router - URL shortener"""
from fastapi import APIRouter, HTTPException, Query
from services.external_apis.tinyurl.provider import TinyURLProvider
from typing import Dict, Any, Optional

router = APIRouter(prefix="/api/tinyurl", tags=["tinyurl"])

provider = TinyURLProvider()

@router.get("/shorten", response_model=Dict[str, Any])
async def shorten_url(
    url: str = Query(..., description="URL to shorten"),
    alias: Optional[str] = Query(None, description="Custom alias (optional)")
):
    """Shorten a URL"""
    try:
        return await provider.shorten_url(url, alias)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))






