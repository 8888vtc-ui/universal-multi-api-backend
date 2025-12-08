"""
Analytics Router
Endpoints pour le dashboard analytics et monitoring
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from services.analytics.metrics_collector import metrics_collector

router = APIRouter(prefix="/api/analytics", tags=["analytics"])


@router.get("/metrics")
async def get_metrics(
    days: int = Query(7, ge=1, le=30, description="Nombre de jours"),
    endpoint: Optional[str] = Query(None, description="Filtrer par endpoint")
):
    """
    📊 Obtenir les métriques d'utilisation
    
    Retourne les statistiques d'utilisation de l'API :
    - Nombre total de requêtes
    - Temps de réponse moyen
    - Répartition par endpoint
    - Répartition par code de statut
    - Requêtes par jour
    """
    try:
        metrics = metrics_collector.get_metrics(days=days, endpoint=endpoint)
        
        return {
            "success": True,
            **metrics
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/errors")
async def get_errors(
    days: int = Query(7, ge=1, le=30, description="Nombre de jours")
):
    """
    ⚠️ Obtenir les erreurs
    
    Retourne les statistiques d'erreurs :
    - Nombre total d'erreurs
    - Types d'erreurs
    - Endpoints avec erreurs
    - Erreurs par jour
    """
    try:
        errors = metrics_collector.get_errors(days=days)
        
        return {
            "success": True,
            **errors
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/endpoints/top")
async def get_top_endpoints(
    days: int = Query(7, ge=1, le=30, description="Nombre de jours"),
    limit: int = Query(10, ge=1, le=50, description="Nombre d'endpoints")
):
    """
    🔝 Top Endpoints
    
    Retourne les endpoints les plus utilisés avec statistiques.
    """
    try:
        top_endpoints = metrics_collector.get_top_endpoints(days=days, limit=limit)
        
        return {
            "success": True,
            "endpoints": top_endpoints,
            "total": len(top_endpoints)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/performance")
async def get_performance_stats(
    days: int = Query(7, ge=1, le=30, description="Nombre de jours")
):
    """
    ⚡ Statistiques de Performance
    
    Retourne les statistiques de performance :
    - Temps de réponse moyen
    - Temps de réponse min/max
    - Total de requêtes
    """
    try:
        performance = metrics_collector.get_performance_stats(days=days)
        
        return {
            "success": True,
            **performance
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/dashboard")
async def get_dashboard_data(
    days: int = Query(7, ge=1, le=30, description="Nombre de jours")
):
    """
    📈 Données Complètes Dashboard
    
    Retourne toutes les données nécessaires pour le dashboard :
    - Métriques générales
    - Top endpoints
    - Erreurs
    - Performance
    """
    try:
        metrics = metrics_collector.get_metrics(days=days)
        errors = metrics_collector.get_errors(days=days)
        top_endpoints = metrics_collector.get_top_endpoints(days=days, limit=10)
        performance = metrics_collector.get_performance_stats(days=days)
        
        return {
            "success": True,
            "period_days": days,
            "metrics": metrics,
            "errors": errors,
            "top_endpoints": top_endpoints,
            "performance": performance,
            "summary": {
                "total_requests": metrics["total_requests"],
                "total_errors": errors["total_errors"],
                "error_rate": round(
                    (errors["total_errors"] / metrics["total_requests"]) * 100, 2
                ) if metrics["total_requests"] > 0 else 0,
                "avg_response_time_ms": performance["avg_response_time_ms"]
            }
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def analytics_health():
    """
    ❤️ Health Check Analytics
    
    Vérifie que le service analytics fonctionne correctement.
    """
    try:
        # Test simple : obtenir métriques du jour
        metrics = metrics_collector.get_metrics(days=1)
        
        return {
            "success": True,
            "status": "healthy",
            "database": "connected",
            "total_requests_today": metrics["total_requests"]
        }
    
    except Exception as e:
        return {
            "success": False,
            "status": "unhealthy",
            "error": str(e)
        }


@router.get("/")
async def analytics_info():
    """
    📚 Informations sur le service Analytics
    """
    return {
        "service": "Analytics & Monitoring",
        "version": "1.0.0",
        "description": "Service d'analyse et monitoring pour dashboard",
        "features": [
            "Collecte automatique de métriques",
            "Analyse de performance",
            "Tracking d'erreurs",
            "Top endpoints",
            "Dashboard complet"
        ],
        "endpoints": {
            "metrics": "/api/analytics/metrics",
            "errors": "/api/analytics/errors",
            "top_endpoints": "/api/analytics/endpoints/top",
            "performance": "/api/analytics/performance",
            "dashboard": "/api/analytics/dashboard"
        }
    }


<<<<<<< Updated upstream
=======





>>>>>>> Stashed changes
