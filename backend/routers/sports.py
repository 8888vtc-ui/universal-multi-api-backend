"""
Sports API Router
"""
from fastapi import APIRouter, HTTPException, Query
from services.external_apis.sports import SportsRouter

router = APIRouter(prefix="/api/sports", tags=["sports"])

sports_router = SportsRouter()


@router.get("/live")
async def get_live_matches():
    """Get live football matches"""
    try:
        result = await sports_router.get_live_matches()
        return {"success": True, **result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/standings")
async def get_league_standings(
    league: int = Query(..., description="League ID"),
    season: int = Query(..., description="Season year")
):
    """Get league standings"""
    try:
        result = await sports_router.get_standings(league, season)
        return {"success": True, **result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/team/{team_id}")
async def get_team_info(team_id: int):
    """Get team information"""
    try:
        result = await sports_router.get_team(team_id)
        return {"success": True, **result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status")
async def get_sports_status():
    """Get sports router status"""
    try:
        status = sports_router.get_status()
        return {"success": True, **status}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
