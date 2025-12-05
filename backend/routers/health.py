"""
Health check endpoint
"""
from fastapi import APIRouter
from models.schemas import HealthResponse
from services.ai_router import ai_router
from services.cache import cache_service

router = APIRouter(prefix="/api", tags=["health"])


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint
    Returns status of all services
    """
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        ai_providers=ai_router.get_status(),
        cache_status="available" if cache_service.health_check() else "unavailable"
    )
