"""
Media API Router
Photos, videos, GIFs
"""
from fastapi import APIRouter, HTTPException, Query
from services.external_apis.media import MediaRouter

router = APIRouter(prefix="/api/media", tags=["media"])

media_router = MediaRouter()


@router.get("/photos/search")
async def search_photos(
    q: str = Query(..., description="Search query"),
    limit: int = Query(10, ge=1, le=100, description="Number of results")
):
    """
    Search photos
    
    Supports: Unsplash (50/hour), Pexels (200/hour)
    """
    try:
        result = await media_router.search_photos(q, limit)
        return {"success": True, **result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/videos/search")
async def search_videos(
    q: str = Query(..., description="Search query"),
    limit: int = Query(10, ge=1, le=100, description="Number of results")
):
    """
    Search videos
    
    Uses: Pexels (200/hour)
    """
    try:
        result = await media_router.search_videos(q, limit)
        return {"success": True, **result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/gifs/search")
async def search_gifs(
    q: str = Query(..., description="Search query"),
    limit: int = Query(10, ge=1, le=50, description="Number of results")
):
    """
    Search GIFs
    
    Uses: Giphy (42/hour)
    """
    try:
        result = await media_router.search_gifs(q, limit)
        return {"success": True, **result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status")
async def get_media_status():
    """Get media router status"""
    try:
        status = media_router.get_status()
        return {"success": True, **status}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
