"""
OMDB API Router
1,000 requests/day free - Movies and TV shows data
"""
from fastapi import APIRouter, HTTPException, Query
from services.external_apis.omdb.provider import OMDBProvider
from typing import Optional

router = APIRouter(prefix="/api/omdb", tags=["omdb"])

try:
    provider = OMDBProvider()
except Exception:
    provider = None


@router.get("/search")
async def search_movies(
    query: str = Query(..., description="Search query"),
    year: Optional[str] = Query(None, description="Year filter")
):
    """Search movies/TV shows"""
    if not provider or not provider.available:
        raise HTTPException(status_code=503, detail="OMDB API key not configured")
    try:
        result = await provider.search(query, year)
        if result.get("Response") == "True":
            return {
                "success": True,
                "count": len(result.get("Search", [])),
                "results": result.get("Search", [])
            }
        else:
            return {
                "success": False,
                "error": result.get("Error", "No results found"),
                "count": 0,
                "results": []
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/title/{title}")
async def get_movie_by_title(
    title: str,
    year: Optional[str] = Query(None, description="Year filter")
):
    """Get movie/TV show by title"""
    if not provider or not provider.available:
        raise HTTPException(status_code=503, detail="OMDB API key not configured")
    try:
        result = await provider.get_by_title(title, year)
        if result:
            return {"success": True, "movie": result}
        else:
            raise HTTPException(status_code=404, detail="Movie/TV show not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/id/{imdb_id}")
async def get_movie_by_id(imdb_id: str):
    """Get movie/TV show by IMDb ID"""
    if not provider or not provider.available:
        raise HTTPException(status_code=503, detail="OMDB API key not configured")
    try:
        result = await provider.get_by_id(imdb_id)
        if result:
            return {"success": True, "movie": result}
        else:
            raise HTTPException(status_code=404, detail="Movie/TV show not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

