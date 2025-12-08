"""
Google Books API Router
1,000 requests/day free
"""
from fastapi import APIRouter, HTTPException, Query
from services.external_apis.books.provider import GoogleBooksProvider
from typing import Optional

router = APIRouter(prefix="/api/books", tags=["books"])

provider = GoogleBooksProvider()


@router.get("/search")
async def search_books(
    query: str = Query(..., description="Search query"),
    max_results: int = Query(10, description="Number of results")
):
    """Search books"""
    try:
        result = await provider.search(query, max_results)
        return {
            "success": True,
            "count": result.get("totalItems", 0),
            "books": result.get("items", [])
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{book_id}")
async def get_book_by_id(book_id: str):
    """Get book by ID"""
    try:
        book = await provider.get_by_id(book_id)
        if book:
            return {"success": True, "book": book}
        else:
            raise HTTPException(status_code=404, detail="Book not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))






