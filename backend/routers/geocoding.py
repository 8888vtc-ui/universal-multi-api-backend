"""
Geocoding API Router
Address to coordinates and reverse
"""
from fastapi import APIRouter, HTTPException, Query
from services.external_apis.geocoding import GeocodingRouter

router = APIRouter(prefix="/api/geocoding", tags=["geocoding"])

geocoding_router = GeocodingRouter()


@router.get("/forward")
@router.get("/search")  # Alias for compatibility
async def geocode_address(
    address: str = Query(None, description="Address to geocode"),
    q: str = Query(None, description="Query (alias for address)")
):
    """
    Convert address to coordinates (geocoding)
    
    Supports: Nominatim (OSM - free), OpenCage (2.5k/day), Positionstack (25k/month)
    """
    query = address or q
    if not query:
        raise HTTPException(status_code=400, detail="Address or q parameter required")
    
    try:
        result = await geocoding_router.search(query)
        return {"success": True, **result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/reverse")
async def reverse_geocode_coordinates(
    lat: float = Query(..., description="Latitude"),
    lon: float = Query(..., description="Longitude")
):
    """
    Convert coordinates to address (reverse geocoding)
    
    Supports: Nominatim, OpenCage, Positionstack
    """
    try:
        result = await geocoding_router.reverse_geocode(lat, lon)
        return {"success": True, **result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status")
async def get_geocoding_status():
    """Get geocoding router status"""
    try:
        status = geocoding_router.get_status()
        return {"success": True, **status}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
