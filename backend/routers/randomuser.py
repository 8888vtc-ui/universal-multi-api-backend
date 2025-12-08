"""RandomUser Router - Generate random user data"""
from fastapi import APIRouter, HTTPException, Query
from services.external_apis.randomuser.provider import RandomUserProvider
from typing import Dict, Any, Optional

router = APIRouter(prefix="/api/randomuser", tags=["randomuser"])

provider = RandomUserProvider()

@router.get("/users", response_model=Dict[str, Any])
async def get_users(
    count: int = Query(1, ge=1, le=5000, description="Number of users to generate"),
    gender: Optional[str] = Query(None, description="Filter by gender (male, female)"),
    nationality: Optional[str] = Query(None, description="Filter by nationality (e.g., us, fr, gb)")
):
    """Get random users"""
    try:
        return await provider.get_users(count, gender, nationality)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))






