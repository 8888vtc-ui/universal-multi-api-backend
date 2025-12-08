"""Pixabay Router - Free images"""
from fastapi import APIRouter, HTTPException, Query
from services.external_apis.pixabay.provider import PixabayProvider
from typing import Dict, Any

router = APIRouter(prefix="/api/pixabay", tags=["pixabay"])

provider = PixabayProvider()

@router.get("/search", response_model=Dict[str, Any])
async def search_images(
    query: str = Query(..., description="Search query for images"),
    limit: int = Query(20, ge=1, le=200, description="Number of images to return"),
    image_type: str = Query("all", description="Image type (all, photo, illustration, vector)")
):
    """Search for images"""
    if not provider.available:
        raise HTTPException(status_code=503, detail="Pixabay API not configured. Please set PIXABAY_API_KEY in .env")
    try:
        return await provider.search_images(query, limit, image_type)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/image/{image_id}", response_model=Dict[str, Any])
async def get_image(image_id: int):
    """Get image details by ID"""
    if not provider.available:
        raise HTTPException(status_code=503, detail="Pixabay API not configured. Please set PIXABAY_API_KEY in .env")
    try:
        return await provider.get_image(image_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))






