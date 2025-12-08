"""Jokes Router - Random jokes"""
from fastapi import APIRouter, HTTPException, Query
from services.external_apis.jokes.provider import JokeAPIProvider, ChuckNorrisProvider
from typing import Dict, Any, List, Optional

router = APIRouter(prefix="/api/jokes", tags=["jokes"])

joke_provider = JokeAPIProvider()
chuck_provider = ChuckNorrisProvider()


@router.get("/random", response_model=Dict[str, Any])
async def get_random_joke(
    category: str = Query("Any", description="Joke category"),
    language: str = Query("en", description="Language (en, de, cs, es, fr, pt)"),
    safe: bool = Query(True, description="Filter offensive jokes")
):
    """Get a random joke"""
    try:
        return await joke_provider.get_random_joke(category, language, safe)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/categories", response_model=List[str])
async def get_categories():
    """Get available joke categories"""
    return await joke_provider.get_categories()


@router.get("/chuck", response_model=Dict[str, Any])
async def get_chuck_norris_joke(
    category: Optional[str] = Query(None, description="Optional category")
):
    """Get a random Chuck Norris joke"""
    try:
        return await chuck_provider.get_random_joke(category)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/chuck/categories", response_model=List[str])
async def get_chuck_categories():
    """Get Chuck Norris joke categories"""
    try:
        return await chuck_provider.get_categories()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))






