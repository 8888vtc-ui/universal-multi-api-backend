"""GitHub Router - Repository and user data"""
from fastapi import APIRouter, HTTPException, Query
from services.external_apis.github.provider import GitHubProvider
from typing import List, Dict, Any

router = APIRouter(prefix="/api/github", tags=["github"])

provider = GitHubProvider()

@router.get("/users/{username}", response_model=Dict[str, Any])
async def get_user(username: str):
    """Get user information"""
    try:
        return await provider.get_user(username)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/users/{username}/repos", response_model=List[Dict[str, Any]])
async def get_user_repos(
    username: str,
    limit: int = Query(30, ge=1, le=100)
):
    """Get user repositories"""
    try:
        return await provider.get_user_repos(username, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/repos/{owner}/{repo}", response_model=Dict[str, Any])
async def get_repo(owner: str, repo: str):
    """Get repository information"""
    try:
        return await provider.get_repo(owner, repo)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/search/repos", response_model=Dict[str, Any])
async def search_repos(
    query: str = Query(..., description="Search query"),
    limit: int = Query(30, ge=1, le=100)
):
    """Search repositories"""
    try:
        return await provider.search_repos(query, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/repos/{owner}/{repo}/readme", response_model=str)
async def get_repo_readme(owner: str, repo: str):
    """Get repository README content"""
    try:
        return await provider.get_repo_readme(owner, repo)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))






