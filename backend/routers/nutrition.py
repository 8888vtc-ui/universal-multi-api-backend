"""
Nutrition API Router
Recipes and food nutrition data
"""
from fastapi import APIRouter, HTTPException, Query
from services.external_apis.nutrition import NutritionRouter

router = APIRouter(prefix="/api/nutrition", tags=["nutrition"])

nutrition_router = NutritionRouter()


@router.get("/recipes/search")
async def search_recipes(
    q: str = Query(..., description="Search query"),
    limit: int = Query(10, ge=1, le=100, description="Number of results")
):
    """
    Search recipes
    
    Supports: Spoonacular (365k recipes), Edamam (2.3M recipes)
    """
    try:
        result = await nutrition_router.search_recipes(q, limit)
        return {"success": True, **result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/foods/search")
async def search_foods(
    q: str = Query(..., description="Food name"),
    limit: int = Query(10, ge=1, le=100, description="Number of results")
):
    """
    Search food nutrition database
    
    Uses: USDA FoodData Central (300k+ foods)
    """
    try:
        result = await nutrition_router.search_foods(q, limit)
        return {"success": True, **result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status")
async def get_nutrition_status():
    """Get nutrition router status"""
    try:
        status = nutrition_router.get_status()
        return {"success": True, **status}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
