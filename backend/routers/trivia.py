"""Trivia Router - Quiz questions"""
from fastapi import APIRouter, HTTPException, Query
from services.external_apis.trivia.provider import OpenTriviaProvider
from typing import Dict, Any, List, Optional

router = APIRouter(prefix="/api/trivia", tags=["trivia"])

trivia_provider = OpenTriviaProvider()


@router.get("/questions", response_model=Dict[str, Any])
async def get_trivia_questions(
    amount: int = Query(10, ge=1, le=50, description="Number of questions"),
    category: Optional[int] = Query(None, description="Category ID (use /categories to see list)"),
    difficulty: Optional[str] = Query(None, description="Difficulty: easy, medium, hard"),
    type: Optional[str] = Query(None, description="Type: multiple, boolean")
):
    """Get trivia questions"""
    try:
        return await trivia_provider.get_questions(amount, category, difficulty, type)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/categories", response_model=List[Dict[str, Any]])
async def get_trivia_categories():
    """Get available trivia categories"""
    try:
        return await trivia_provider.get_categories()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))






