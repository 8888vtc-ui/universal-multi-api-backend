"""Open Library Router - Free books"""
from fastapi import APIRouter, HTTPException, Query
from services.external_apis.openlibrary.provider import OpenLibraryProvider
from typing import Dict, Any, List

router = APIRouter(prefix="/api/openlibrary", tags=["openlibrary"])

openlibrary_provider = OpenLibraryProvider()


@router.get("/search", response_model=Dict[str, Any])
async def search_books(
    query: str = Query(..., description="Search query"),
    limit: int = Query(10, ge=1, le=100),
    page: int = Query(1, ge=1)
):
    """Search for books in Open Library"""
    try:
        return await openlibrary_provider.search_books(query, limit, page)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/book/{key:path}", response_model=Dict[str, Any])
async def get_book(key: str):
    """Get book details by key"""
    try:
        return await openlibrary_provider.get_book(f"/{key}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/authors/search", response_model=Dict[str, Any])
async def search_authors(
    query: str = Query(..., description="Author name"),
    limit: int = Query(10, ge=1, le=50)
):
    """Search for authors"""
    try:
        return await openlibrary_provider.search_authors(query, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/trending/{period}", response_model=Dict[str, Any])
async def get_trending_books(
    period: str = "daily"
):
    """Get trending books (daily, weekly, monthly, yearly)"""
    if period not in ["daily", "weekly", "monthly", "yearly"]:
        raise HTTPException(status_code=400, detail="Period must be: daily, weekly, monthly, yearly")
    try:
        return await openlibrary_provider.get_trending(period)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))






