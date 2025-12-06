
from fastapi import APIRouter, HTTPException, Query
import json
import os
import glob
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

router = APIRouter(prefix="/api/blog", tags=["Blog"])

# Path to the data directory
# Assuming routers/blog.py -> backend/routers/blog.py
# Data dir -> backend/data/articles
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data", "articles")

class Article(BaseModel):
    slug: str
    expertId: str
    date: str
    readTime: int
    dataSources: List[str]
    keywords: List[str]
    fr: Dict[str, str]
    en: Dict[str, str]

@router.get("/list")
async def list_articles(
    limit: int = 20, 
    page: int = 1, 
    expert: Optional[str] = None,
    lang: str = "fr"
):
    """
    List articles with pagination.
    Note: In a real DB this would be efficient. With files, we scan directory.
    For 15k files, scanning dir every time is okay-ish (os.scandir is fast), 
    but caching the list would be better.
    """
    if not os.path.exists(DATA_DIR):
        return {"articles": [], "total": 0, "page": page}

    # Get all json files
    # Optimization: Use os.scandir instead of glob for speed on large dirs
    try:
        files = [f.name for f in os.scandir(DATA_DIR) if f.name.endswith('.json')]
    except FileNotFoundError:
        return {"articles": [], "total": 0}

    # This is a simple implementation. For 15k items, we'd want an index.json file.
    # But files works for now. 
    
    total = len(files)
    start = (page - 1) * limit
    end = start + limit
    
    paginated_files = files[start:end]
    results = []

    for filename in paginated_files:
        try:
            with open(os.path.join(DATA_DIR, filename), 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Return lightweight summary
                results.append({
                    "slug": data.get("slug", filename.replace(".json", "")),
                    "title": data.get(lang, {}).get("title", ""),
                    "excerpt": data.get(lang, {}).get("excerpt", ""),
                    "expertId": data.get("expertId"),
                    "date": data.get("date"),
                    "readTime": data.get("readTime")
                })
        except Exception:
            continue
            
    return {
        "articles": results,
        "total": total,
        "page": page,
        "limit": limit
    }

@router.get("/{slug}")
async def get_article(slug: str):
    """Get full article content by slug"""
    file_path = os.path.join(DATA_DIR, f"{slug}.json")
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Article not found")
        
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading article: {str(e)}")
