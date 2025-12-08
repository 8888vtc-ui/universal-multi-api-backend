"""
Analytics Middleware
Middleware pour collecter automatiquement les métriques
"""
import time
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from services.analytics.metrics_collector import metrics_collector


class AnalyticsMiddleware(BaseHTTPMiddleware):
    """Middleware pour collecter les métriques automatiquement"""
    
    async def dispatch(self, request: Request, call_next):
        # Temps de début
        start_time = time.time()
        
        # Obtenir user_id depuis headers ou query
        user_id = request.headers.get("X-User-ID") or request.query_params.get("user_id")
        ip_address = request.client.host if request.client else None
        
        # Exécuter la requête
        try:
            response = await call_next(request)
            
            # Calculer temps de réponse
            response_time_ms = (time.time() - start_time) * 1000
            
            # Enregistrer métrique (uniquement pour /api/*)
            if request.url.path.startswith("/api/"):
                metrics_collector.record_request(
                    endpoint=request.url.path,
                    method=request.method,
                    status_code=response.status_code,
                    response_time_ms=response_time_ms,
                    user_id=user_id,
                    ip_address=ip_address
                )
            
            return response
        
        except Exception as e:
            # Enregistrer erreur
            if request.url.path.startswith("/api/"):
                metrics_collector.record_error(
                    endpoint=request.url.path,
                    error_type=type(e).__name__,
                    error_message=str(e),
                    user_id=user_id
                )
            raise


<<<<<<< Updated upstream
=======





>>>>>>> Stashed changes
