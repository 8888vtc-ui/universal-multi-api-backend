"""
News API Router
Endpoints for news search and headlines
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from services.external_apis.news import NewsRouter

router = APIRouter(prefix="/api/news", tags=["news"])

# Initialize news router
news_router = NewsRouter()


@router.get("/search")
async def search_news(
    q: str = Query(..., description="Search query"),
    language: str = Query('en', description="Language code (en, fr, es, etc.)"),
    page_size: int = Query(10, ge=1, le=100, description="Number of results")
):
    """
    Search news articles with automatic provider fallback
    
    Supports: NewsAPI.org, NewsData.io
    """
    # Vérifier que des providers sont disponibles
    if not news_router.providers:
        raise HTTPException(
            status_code=503,
            detail="News service unavailable. No providers configured. Please set NEWSAPI_ORG_KEY or NEWSDATA_IO_KEY in environment variables."
        )
    
    try:
        result = await news_router.search(q, language, page_size)
        return {"success": True, **result}
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"News search failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="News service temporarily unavailable. Please try again later."
        )


@router.get("/headlines")
async def get_top_headlines(
    country: str = Query('us', description="Country code (us, fr, gb, etc.)"),
    category: Optional[str] = Query(None, description="Category (business, technology, sports, etc.)"),
    page_size: int = Query(10, ge=1, le=100, description="Number of results")
):
    """Get top headlines by country and category"""
    # Vérifier que des providers sont disponibles
    if not news_router.providers:
        raise HTTPException(
            status_code=503,
            detail="News service unavailable. No providers configured. Please set NEWSAPI_ORG_KEY or NEWSDATA_IO_KEY in environment variables."
        )
    
    try:
        result = await news_router.get_top_headlines(country, category, page_size)
        return {"success": True, **result}
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"News headlines failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="News service temporarily unavailable. Please try again later."
        )


@router.get("/status")
async def get_news_status():
    """Get news router status"""
    try:
        status = news_router.get_status()
        return {"success": True, **status}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
