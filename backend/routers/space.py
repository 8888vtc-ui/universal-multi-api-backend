"""
Space/NASA API Router
Endpoints for space data
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from services.external_apis.space import SpaceRouter

router = APIRouter(prefix="/api/space", tags=["space"])

# Initialize space router
space_router = SpaceRouter()


@router.get("/apod")
async def get_astronomy_picture(
    date: Optional[str] = Query(None, description="Date (YYYY-MM-DD), defaults to today")
):
    """
    Get NASA Astronomy Picture of the Day
    
    Free unlimited access
    """
    try:
        result = await space_router.get_apod(date)
        return {"success": True, **result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/mars/{rover}/photos")
async def get_mars_rover_photos(
    rover: str,
    sol: int = Query(..., description="Martian sol (day)"),
    camera: Optional[str] = Query(None, description="Camera name (FHAZ, RHAZ, MAST, etc.)")
):
    """
    Get Mars Rover photos
    
    Rovers: curiosity, opportunity, spirit
    """
    try:
        result = await space_router.get_mars_photos(rover, sol, camera)
        return {"success": True, **result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/neo")
async def get_near_earth_objects(
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)")
):
    """Get Near Earth Objects (asteroids) feed"""
    try:
        result = await space_router.get_neo_feed(start_date, end_date)
        return {"success": True, **result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/epic")
async def get_epic_earth_images():
    """Get EPIC (Earth Polychromatic Imaging Camera) images"""
    try:
        result = await space_router.get_epic_images()
        return {"success": True, **result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status")
async def get_space_status():
    """Get space/NASA router status"""
    try:
        status = space_router.get_status()
        return {"success": True, **status}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
