"""
Weather API Router
Endpoints for current weather and forecasts
"""
from fastapi import APIRouter, HTTPException, Query
from services.external_apis.weather import WeatherRouter

router = APIRouter(prefix="/api/weather", tags=["weather"])

# Initialize weather router
weather_router = WeatherRouter()


@router.get("/current")
async def get_current_weather(
    lat: float = Query(..., description="Latitude"),
    lon: float = Query(..., description="Longitude")
):
    """
    Get current weather for coordinates
    
    Supports: Open-Meteo (unlimited), WeatherAPI (1M/month)
    """
    # Vérifier que des providers sont disponibles
    if not weather_router.providers:
        raise HTTPException(
            status_code=503,
            detail="Weather service unavailable. No providers configured."
        )
    
    try:
        result = await weather_router.get_current_weather(lat, lon)
        return {"success": True, **result}
    except HTTPException:
        raise
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Weather fetch failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Weather service temporarily unavailable. Please try again later."
        )


@router.get("/forecast")
async def get_weather_forecast(
    lat: float = Query(..., description="Latitude"),
    lon: float = Query(..., description="Longitude"),
    days: int = Query(7, ge=1, le=16, description="Number of days (1-16)")
):
    """Get weather forecast for coordinates"""
    # Vérifier que des providers sont disponibles
    if not weather_router.providers:
        raise HTTPException(
            status_code=503,
            detail="Weather service unavailable. No providers configured."
        )
    
    try:
        result = await weather_router.get_forecast(lat, lon, days)
        return {"success": True, **result}
    except HTTPException:
        raise
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Weather forecast failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Weather service temporarily unavailable. Please try again later."
        )


@router.get("/status")
async def get_weather_status():
    """Get weather router status"""
    try:
        status = weather_router.get_status()
        return {"success": True, **status}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
