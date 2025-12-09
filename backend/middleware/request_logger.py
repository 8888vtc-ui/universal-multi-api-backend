"""
Request Logger Middleware
Logs toutes les requêtes avec timing et métriques
"""
import time
import logging
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)


class RequestLoggerMiddleware(BaseHTTPMiddleware):
    """
    Middleware pour logger toutes les requêtes HTTP
    
    Logs:
    - Méthode HTTP
    - URL
    - Temps de réponse
    - Status code
    - Client IP
    """
    
    # Endpoints à exclure du logging (health checks, etc.)
    EXCLUDED_PATHS = [
        "/api/health",
        "/health",
        "/docs",
        "/redoc",
        "/openapi.json",
        "/favicon.ico",
    ]
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Skip logging for excluded paths
        if any(request.url.path.startswith(path) for path in self.EXCLUDED_PATHS):
            return await call_next(request)
        
        # Capture start time
        start_time = time.time()
        
        # Get client IP
        client_ip = request.client.host if request.client else "unknown"
        forwarded_for = request.headers.get("x-forwarded-for")
        if forwarded_for:
            client_ip = forwarded_for.split(",")[0].strip()
        
        # Process request
        try:
            response = await call_next(request)
            
            # Calculate duration
            duration_ms = (time.time() - start_time) * 1000
            
            # Log based on status code
            log_message = (
                f"{request.method} {request.url.path} "
                f"-> {response.status_code} "
                f"({duration_ms:.1f}ms) "
                f"[{client_ip}]"
            )
            
            if response.status_code >= 500:
                logger.error(log_message)
            elif response.status_code >= 400:
                logger.warning(log_message)
            elif duration_ms > 5000:  # Slow request warning
                logger.warning(f"🐢 SLOW: {log_message}")
            else:
                logger.info(log_message)
            
            # Add timing header
            response.headers["X-Response-Time"] = f"{duration_ms:.1f}ms"
            
            return response
            
        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000
            logger.error(
                f"{request.method} {request.url.path} "
                f"-> ERROR ({duration_ms:.1f}ms) [{client_ip}]: {e}"
            )
            raise
