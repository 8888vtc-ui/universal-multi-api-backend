"""Search History Router"""
from fastapi import APIRouter, HTTPException, Query
from services.search_history import search_history_service
from typing import Dict, Any, List, Optional
from pydantic import BaseModel

router = APIRouter(prefix="/api/history", tags=["history"])


class AddSearchRequest(BaseModel):
    query: str
    search_type: str = "general"
    results_count: int = 0
    metadata: Optional[Dict[str, Any]] = None


@router.post("/{user_id}/add", response_model=Dict[str, Any])
async def add_to_history(user_id: str, request: AddSearchRequest):
    """Add a search to user's history"""
    try:
        return search_history_service.add_search(
            user_id=user_id,
            query=request.query,
            search_type=request.search_type,
            results_count=request.results_count,
            metadata=request.metadata
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{user_id}", response_model=List[Dict[str, Any]])
async def get_user_history(
    user_id: str,
    limit: int = Query(20, ge=1, le=100),
    type: Optional[str] = Query(None, description="Filter by search type")
):
    """Get search history for a user"""
    return search_history_service.get_history(user_id, limit, type)


@router.delete("/{user_id}/{search_id}")
async def delete_search(user_id: str, search_id: str):
    """Delete a specific search from history"""
    success = search_history_service.delete_search(user_id, search_id)
    if not success:
        raise HTTPException(status_code=404, detail="Search not found")
    return {"deleted": True}


@router.delete("/{user_id}")
async def clear_user_history(user_id: str):
    """Clear all history for a user"""
    success = search_history_service.clear_history(user_id)
    return {"cleared": success}


@router.get("/{user_id}/stats", response_model=Dict[str, Any])
async def get_user_stats(user_id: str):
    """Get search statistics for a user"""
    return search_history_service.get_stats(user_id)


@router.get("/", response_model=Dict[str, Any])
async def get_global_stats():
    """Get global search statistics"""
    return search_history_service.get_stats()


@router.get("/popular/all", response_model=List[Dict[str, Any]])
async def get_popular_searches(
    limit: int = Query(10, ge=1, le=50),
    type: Optional[str] = Query(None, description="Filter by search type")
):
    """Get most popular searches"""
    return search_history_service.get_popular_searches(limit, type)


@router.get("/recent/all", response_model=List[Dict[str, Any]])
async def get_recent_searches(limit: int = Query(20, ge=1, le=100)):
    """Get most recent searches across all users"""
    return search_history_service.get_recent_searches(limit)






