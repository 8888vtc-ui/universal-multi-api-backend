"""JSONPlaceholder Router - Free fake REST API"""
from fastapi import APIRouter, HTTPException, Query
from services.external_apis.jsonplaceholder.provider import JSONPlaceholderProvider
from typing import List, Dict, Any, Optional

router = APIRouter(prefix="/api/jsonplaceholder", tags=["jsonplaceholder"])

provider = JSONPlaceholderProvider()

@router.get("/posts", response_model=List[Dict[str, Any]])
async def get_posts(limit: Optional[int] = Query(None, ge=1, le=100)):
    """Get all posts"""
    try:
        return await provider.get_posts(limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/posts/{post_id}", response_model=Dict[str, Any])
async def get_post(post_id: int):
    """Get a specific post by ID"""
    try:
        return await provider.get_post(post_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/users", response_model=List[Dict[str, Any]])
async def get_users():
    """Get all users"""
    try:
        return await provider.get_users()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/users/{user_id}", response_model=Dict[str, Any])
async def get_user(user_id: int):
    """Get a specific user by ID"""
    try:
        return await provider.get_user(user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/comments", response_model=List[Dict[str, Any]])
async def get_comments(post_id: Optional[int] = Query(None)):
    """Get comments, optionally filtered by post ID"""
    try:
        return await provider.get_comments(post_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/albums", response_model=List[Dict[str, Any]])
async def get_albums():
    """Get all albums"""
    try:
        return await provider.get_albums()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/photos", response_model=List[Dict[str, Any]])
async def get_photos(album_id: Optional[int] = Query(None)):
    """Get photos, optionally filtered by album ID"""
    try:
        return await provider.get_photos(album_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/todos", response_model=List[Dict[str, Any]])
async def get_todos(user_id: Optional[int] = Query(None)):
    """Get todos, optionally filtered by user ID"""
    try:
        return await provider.get_todos(user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))






