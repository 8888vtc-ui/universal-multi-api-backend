"""
Giphy API Router
Free unlimited GIFs
"""
from fastapi import APIRouter, HTTPException, Query
from services.external_apis.giphy.provider import GiphyProvider
from typing import Optional

router = APIRouter(prefix="/api/giphy", tags=["giphy"])

provider = GiphyProvider()


@router.get("/search")
async def search_gifs(
    query: str = Query(..., description="Search query"),
    limit: int = Query(25, description="Number of results"),
    rating: str = Query("g", description="Rating (g, pg, pg-13, r)")
):
    """Search GIFs"""
    try:
        result = await provider.search(query, limit, rating)
        return {
            "success": True,
            "count": len(result.get("data", [])),
            "gifs": result.get("data", [])
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/trending")
async def get_trending_gifs(
    limit: int = Query(25, description="Number of results")
):
    """Get trending GIFs"""
    try:
        result = await provider.get_trending(limit)
        return {
            "success": True,
            "count": len(result.get("data", [])),
            "gifs": result.get("data", [])
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/random")
async def get_random_gif(
    tag: Optional[str] = Query(None, description="Tag for random GIF")
):
    """Get random GIF"""
    try:
        result = await provider.get_random(tag)
        if result:
            return {"success": True, "gif": result.get("data", {})}
        else:
            raise HTTPException(status_code=500, detail="Failed to get random GIF")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{gif_id}")
async def get_gif_by_id(gif_id: str):
    """Get GIF by ID"""
    try:
        result = await provider.get_by_id(gif_id)
        if result:
            return {"success": True, "gif": result.get("data", {})}
        else:
            raise HTTPException(status_code=404, detail="GIF not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))






