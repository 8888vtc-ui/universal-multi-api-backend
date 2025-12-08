"""Lorem Picsum Router - Placeholder images"""
from fastapi import APIRouter, HTTPException, Query
from services.external_apis.lorempicsum.provider import LoremPicsumProvider
from typing import Dict, Any, List, Optional

router = APIRouter(prefix="/api/lorempicsum", tags=["lorempicsum"])

provider = LoremPicsumProvider()

@router.get("/image", response_model=Dict[str, Any])
async def get_image_url(
    width: int = Query(800, ge=1, le=2000),
    height: int = Query(600, ge=1, le=2000),
    seed: Optional[int] = Query(None, description="Random seed for consistent image")
):
    """Get a random placeholder image URL"""
    try:
        return await provider.get_image_url(width, height, seed)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/image/{image_id}", response_model=Dict[str, Any])
async def get_image_info(image_id: int):
    """Get image info by ID"""
    try:
        return await provider.get_image_info(image_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/list", response_model=List[Dict[str, Any]])
async def get_list(
    page: int = Query(1, ge=1),
    limit: int = Query(30, ge=1, le=100)
):
    """Get list of images"""
    try:
        return await provider.get_list(page, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))






