"""Lorem Ipsum Router - Generate placeholder text"""
from fastapi import APIRouter, HTTPException, Query
from services.external_apis.lorem.provider import LoremIpsumProvider
from typing import Dict, Any

router = APIRouter(prefix="/api/lorem", tags=["lorem"])

provider = LoremIpsumProvider()

@router.get("/text", response_model=str)
async def get_text(
    paragraphs: int = Query(1, ge=1, le=10, description="Number of paragraphs"),
    words: int = Query(None, ge=1, le=1000, description="Number of words (overrides paragraphs)")
):
    """Get Lorem Ipsum text"""
    try:
        return await provider.get_text(paragraphs, words)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/json", response_model=Dict[str, Any])
async def get_json(paragraphs: int = Query(1, ge=1, le=10)):
    """Get Lorem Ipsum as JSON"""
    try:
        return await provider.get_json(paragraphs)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))






