"""
YouTube Data API Router
10,000 requests/day free
"""
from fastapi import APIRouter, HTTPException, Query
from services.external_apis.youtube.provider import YouTubeProvider
from typing import Optional

router = APIRouter(prefix="/api/youtube", tags=["youtube"])

try:
    provider = YouTubeProvider()
except Exception:
    provider = None


@router.get("/search")
async def search_videos(
    query: str = Query(..., description="Search query"),
    max_results: int = Query(10, description="Number of results"),
    order: str = Query("relevance", description="Order (relevance, date, rating, viewCount)")
):
    """Search YouTube videos"""
    if not provider or not provider.available:
        raise HTTPException(status_code=503, detail="YOUTUBE_API_KEY not configured")
    try:
        result = await provider.search(query, max_results, order)
        return {
            "success": True,
            "count": len(result.get("items", [])),
            "videos": result.get("items", [])
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/video/{video_id}")
async def get_video(video_id: str):
    """Get video details by ID"""
    if not provider or not provider.available:
        raise HTTPException(status_code=503, detail="YOUTUBE_API_KEY not configured")
    try:
        video = await provider.get_video(video_id)
        if video:
            return {"success": True, "video": video}
        else:
            raise HTTPException(status_code=404, detail="Video not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/channel/{channel_id}")
async def get_channel(channel_id: str):
    """Get channel details by ID"""
    if not provider or not provider.available:
        raise HTTPException(status_code=503, detail="YOUTUBE_API_KEY not configured")
    try:
        channel = await provider.get_channel(channel_id)
        if channel:
            return {"success": True, "channel": channel}
        else:
            raise HTTPException(status_code=404, detail="Channel not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/trending")
async def get_trending_videos(
    region_code: str = Query("US", description="Region code (e.g., US, FR)"),
    max_results: int = Query(25, description="Number of results")
):
    """Get trending videos"""
    if not provider or not provider.available:
        raise HTTPException(status_code=503, detail="YOUTUBE_API_KEY not configured")
    try:
        result = await provider.get_trending(region_code, max_results)
        return {
            "success": True,
            "count": len(result.get("items", [])),
            "videos": result.get("items", [])
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

