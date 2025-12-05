"""
Router pour vérification de santé des APIs
"""
from fastapi import APIRouter, HTTPException
from services.api_health_checker import api_health_checker

router = APIRouter(prefix="/api/health-check", tags=["Health Check"])


@router.get("/apis")
async def check_all_apis():
    """
    Vérifier la santé de toutes les APIs
    
    Retourne :
    - Statut de chaque API
    - Clés manquantes
    - Recommandations
    """
    health = api_health_checker.check_all_apis()
    missing = api_health_checker.get_missing_keys()
    recommendations = api_health_checker.get_recommendations()
    
    return {
        "health": health,
        "missing_keys": missing,
        "recommendations": recommendations
    }


@router.get("/apis/{api_name}")
async def check_api(api_name: str):
    """Vérifier la santé d'une API spécifique"""
    health = api_health_checker.check_api_health(api_name)
    return health


@router.get("/missing-keys")
async def get_missing_keys():
    """Obtenir la liste des clés API manquantes"""
    return {
        "missing_keys": api_health_checker.get_missing_keys(),
        "recommendations": api_health_checker.get_recommendations()
    }


