"""
Wikipedia API Router
Free unlimited access to Wikipedia articles
"""
from fastapi import APIRouter, HTTPException, Query
from services.external_apis.wikipedia.provider import WikipediaProvider
from typing import Optional

router = APIRouter(prefix="/api/wikipedia", tags=["wikipedia"])

provider = WikipediaProvider()


@router.get("/search")
async def search_wikipedia(
    query: str = Query(..., description="Search query"),
    limit: int = Query(10, description="Number of results")
):
    """Search Wikipedia articles"""
    try:
        results = await provider.search(query, limit)
        return {
            "success": True,
            "count": len(results),
            "results": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/page/{title}")
async def get_wikipedia_page(title: str):
    """Get Wikipedia page by title"""
    try:
        page = await provider.get_page(title)
        if page:
            return {"success": True, "page": page}
        else:
            raise HTTPException(status_code=404, detail="Page not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/summary/{title}")
async def get_wikipedia_summary(title: str):
    """Get Wikipedia page summary"""
    try:
        summary = await provider.get_summary(title)
        if summary:
            return {"success": True, "title": title, "summary": summary}
        else:
            raise HTTPException(status_code=404, detail="Page not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/random")
async def get_random_article():
    """Get random Wikipedia article"""
    try:
        article = await provider.get_random_article()
        if article:
            return {"success": True, "article": article}
        else:
            raise HTTPException(status_code=500, detail="Failed to get random article")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))






