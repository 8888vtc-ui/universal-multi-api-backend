"""
Deep Health Check Router
Vérifie la santé de tous les services et dépendances
"""
import os
import asyncio
import logging
from datetime import datetime, timezone
from typing import Dict, Any, List
from fastapi import APIRouter, HTTPException

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/health", tags=["Health"])


async def check_redis() -> Dict[str, Any]:
    """Vérifier la connexion Redis"""
    try:
        from services.cache import cache_service
        if cache_service.available:
            # Test ping
            if cache_service.redis.ping():
                return {"status": "healthy", "type": "redis"}
        return {"status": "unavailable", "type": "redis"}
    except Exception as e:
        return {"status": "error", "type": "redis", "error": str(e)}


async def check_database() -> Dict[str, Any]:
    """Vérifier la base de données Auth"""
    try:
        from services.auth import auth_service
        # Test query
        conn = auth_service._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        conn.close()
        return {"status": "healthy", "type": "sqlite"}
    except Exception as e:
        return {"status": "error", "type": "sqlite", "error": str(e)}


async def check_ai_providers() -> Dict[str, Any]:
    """Vérifier les providers IA"""
    try:
        from services.ai_router import ai_router
        status = ai_router.get_status()
        available = [name for name, info in status.items() if info.get("available")]
        return {
            "status": "healthy" if available else "degraded",
            "available_count": len(available),
            "providers": available
        }
    except Exception as e:
        return {"status": "error", "error": str(e)}


async def check_external_api(name: str, url: str) -> Dict[str, Any]:
    """Vérifier une API externe"""
    try:
        from services.http_client import http_client
        response = await http_client.get(url, timeout=5.0)
        return {
            "status": "healthy" if response.status_code < 400 else "degraded",
            "response_time_ms": response.elapsed.total_seconds() * 1000,
            "status_code": response.status_code
        }
    except Exception as e:
        return {"status": "error", "error": str(e)}


@router.get("/deep")
async def deep_health_check():
    """
    🔍 Health check approfondi
    
    Vérifie:
    - Cache Redis
    - Base de données
    - Providers IA
    - APIs externes critiques
    - Système de fichiers
    
    Returns:
        status: healthy/degraded/unhealthy
        checks: détail de chaque vérification
        timestamp: heure du check
    """
    start_time = datetime.now(timezone.utc)
    
    # Exécuter tous les checks en parallèle
    checks = {}
    
    # Cache
    checks["cache"] = await check_redis()
    
    # Database
    checks["database"] = await check_database()
    
    # AI Providers
    checks["ai_providers"] = await check_ai_providers()
    
    # External APIs (sample)
    external_checks = await asyncio.gather(
        check_external_api("open_meteo", "https://api.open-meteo.com/v1/forecast?latitude=0&longitude=0&current_weather=true"),
        check_external_api("coingecko", "https://api.coingecko.com/api/v3/ping"),
        return_exceptions=True
    )
    
    checks["external_apis"] = {
        "open_meteo": external_checks[0] if not isinstance(external_checks[0], Exception) else {"status": "error"},
        "coingecko": external_checks[1] if not isinstance(external_checks[1], Exception) else {"status": "error"}
    }
    
    # File system
    try:
        data_dir = "./data"
        os.makedirs(data_dir, exist_ok=True)
        test_file = os.path.join(data_dir, ".health_check")
        with open(test_file, "w") as f:
            f.write("ok")
        os.remove(test_file)
        checks["filesystem"] = {"status": "healthy", "path": data_dir}
    except Exception as e:
        checks["filesystem"] = {"status": "error", "error": str(e)}
    
    # Déterminer le statut global
    statuses = []
    for check in checks.values():
        if isinstance(check, dict):
            if "status" in check:
                statuses.append(check["status"])
            else:
                for sub_check in check.values():
                    if isinstance(sub_check, dict) and "status" in sub_check:
                        statuses.append(sub_check["status"])
    
    if all(s == "healthy" for s in statuses):
        overall_status = "healthy"
    elif any(s == "error" for s in statuses):
        overall_status = "unhealthy"
    else:
        overall_status = "degraded"
    
    duration_ms = (datetime.now(timezone.utc) - start_time).total_seconds() * 1000
    
    response = {
        "status": overall_status,
        "timestamp": start_time.isoformat(),
        "duration_ms": round(duration_ms, 2),
        "version": "2.2.0",
        "environment": os.getenv("ENVIRONMENT", "development"),
        "checks": checks
    }
    
    # Log si unhealthy
    if overall_status == "unhealthy":
        logger.error(f"Deep health check failed: {response}")
    
    return response


@router.get("/ready")
async def readiness_check():
    """
    Readiness probe pour Kubernetes
    Vérifie si l'app est prête à recevoir du trafic
    """
    try:
        # Vérifier les dépendances critiques
        from services.ai_router import ai_router
        
        if not ai_router.available_providers:
            raise HTTPException(status_code=503, detail="No AI providers available")
        
        return {
            "status": "ready",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))


@router.get("/live")
async def liveness_check():
    """
    Liveness probe pour Kubernetes
    Vérifie si l'app est vivante
    """
    return {
        "status": "alive",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


<<<<<<< Updated upstream
=======





>>>>>>> Stashed changes
