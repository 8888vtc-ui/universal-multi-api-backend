"""
Entertainment API Router
Endpoints for movies, music, and restaurants
"""
from fastapi import APIRouter, HTTPException, Query
from services.external_apis import tmdb, yelp, spotify

router = APIRouter(prefix="/api/entertainment", tags=["entertainment"])


# Movies & TV
@router.get("/movies/search")
async def search_movies(query: str = Query(..., description="Movie title to search")):
    """Search for movies"""
    try:
        data = await tmdb.search_movies(query)
        return {"success": True, "data": data, "source": "tmdb"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/movies/trending")
async def get_trending_movies(
    media_type: str = Query("movie", description="movie or tv"),
    time_window: str = Query("week", description="day or week")
):
    """Get trending movies or TV shows"""
    try:
        data = await tmdb.get_trending(media_type, time_window)
        return {"success": True, "data": data, "source": "tmdb"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Restaurants
@router.get("/restaurants/search")
async def search_restaurants(
    term: str = Query(..., description="Search term (e.g., 'pizza', 'kosher')"),
    location: str = Query(..., description="Location (city, address)"),
    limit: int = Query(10, ge=1, le=50)
):
    """Search for restaurants and businesses"""
    try:
        data = await yelp.search_businesses(term, location, limit)
        return {"success": True, "data": data, "source": "yelp"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/restaurants/{business_id}")
async def get_restaurant_details(business_id: str):
    """Get detailed information about a restaurant"""
    try:
        data = await yelp.get_business_details(business_id)
        return {"success": True, "data": data, "source": "yelp"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Music
@router.get("/music/search")
async def search_music(
    query: str = Query(..., description="Song or artist name"),
    limit: int = Query(10, ge=1, le=50)
):
    """Search for music tracks"""
    try:
        data = await spotify.search_tracks(query, limit)
        return {"success": True, "data": data, "source": "spotify"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
