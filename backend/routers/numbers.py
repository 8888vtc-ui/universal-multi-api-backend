"""Numbers Router - Facts about numbers"""
from fastapi import APIRouter, HTTPException, Query
from services.external_apis.numbers.provider import NumbersAPIProvider
from typing import Dict, Any

router = APIRouter(prefix="/api/numbers", tags=["numbers"])

numbers_provider = NumbersAPIProvider()


@router.get("/fact/{number}", response_model=Dict[str, Any])
async def get_number_fact(
    number: int,
    type: str = Query("trivia", description="Fact type: trivia, math, date, year")
):
    """Get a fact about a specific number"""
    try:
        return await numbers_provider.get_number_fact(number, type)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/random", response_model=Dict[str, Any])
async def get_random_fact(
    type: str = Query("trivia", description="Fact type: trivia, math, year")
):
    """Get a random number fact"""
    try:
        return await numbers_provider.get_random_fact(type)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/date/{month}/{day}", response_model=Dict[str, Any])
async def get_date_fact(month: int, day: int):
    """Get a fact about a specific date"""
    try:
        return await numbers_provider.get_date_fact(month, day)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))






