"""Quotes Router - Random quotes and advice"""
from fastapi import APIRouter, HTTPException, Query
from services.external_apis.quotes.provider import QuoteAPIProvider, AdviceSlipProvider
from typing import Dict, Any, Optional

router = APIRouter(prefix="/api/quotes", tags=["quotes"])

quote_provider = QuoteAPIProvider()
advice_provider = AdviceSlipProvider()

@router.get("/random", response_model=Dict[str, Any])
async def get_random_quote(
    tags: Optional[str] = Query(None, description="Filter by tags (comma-separated)"),
    max_length: Optional[int] = Query(None, description="Maximum quote length")
):
    """Get a random quote"""
    try:
        return await quote_provider.get_random_quote(tags, max_length)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/list", response_model=Dict[str, Any])
async def get_quotes(
    tags: Optional[str] = Query(None, description="Filter by tags"),
    limit: int = Query(20, ge=1, le=150)
):
    """Get multiple quotes"""
    try:
        return await quote_provider.get_quotes(tags, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{quote_id}", response_model=Dict[str, Any])
async def get_quote(quote_id: str):
    """Get a specific quote by ID"""
    try:
        return await quote_provider.get_quote(quote_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/tags/list", response_model=list)
async def get_tags():
    """Get all available tags"""
    try:
        return await quote_provider.get_tags()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/advice/random", response_model=Dict[str, Any])
async def get_random_advice():
    """Get random advice"""
    try:
        return await advice_provider.get_random_advice()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/advice/{advice_id}", response_model=Dict[str, Any])
async def get_advice(advice_id: int):
    """Get specific advice by ID"""
    try:
        return await advice_provider.get_advice(advice_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/advice/search/{query}", response_model=Dict[str, Any])
async def search_advice(query: str):
    """Search for advice"""
    try:
        return await advice_provider.search_advice(query)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))






