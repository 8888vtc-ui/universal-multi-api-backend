"""Name Analysis Router - Age, Gender, Nationality prediction"""
from fastapi import APIRouter, HTTPException, Query
from services.external_apis.agify.provider import NameAnalysisProvider
from typing import Dict, Any, Optional

router = APIRouter(prefix="/api/name", tags=["name-analysis"])

name_provider = NameAnalysisProvider()


@router.get("/analyze", response_model=Dict[str, Any])
async def analyze_name(
    name: str = Query(..., description="Name to analyze"),
    country: Optional[str] = Query(None, description="ISO 3166-1 alpha-2 country code")
):
    """Full name analysis: predict age, gender, and nationality"""
    try:
        return await name_provider.analyze_name(name, country)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/age", response_model=Dict[str, Any])
async def predict_age(
    name: str = Query(..., description="Name to analyze"),
    country: Optional[str] = Query(None, description="ISO 3166-1 alpha-2 country code")
):
    """Predict age from name"""
    try:
        return await name_provider.predict_age(name, country)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/gender", response_model=Dict[str, Any])
async def predict_gender(
    name: str = Query(..., description="Name to analyze"),
    country: Optional[str] = Query(None, description="ISO 3166-1 alpha-2 country code")
):
    """Predict gender from name"""
    try:
        return await name_provider.predict_gender(name, country)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/nationality", response_model=Dict[str, Any])
async def predict_nationality(
    name: str = Query(..., description="Name to analyze")
):
    """Predict nationality from name"""
    try:
        return await name_provider.predict_nationality(name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))






