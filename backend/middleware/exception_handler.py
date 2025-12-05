"""
Global Exception Handler
Gestion centralisée des erreurs avec logging
"""
import logging
import traceback
from typing import Callable
from fastapi import Request, Response, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from pydantic import ValidationError

logger = logging.getLogger(__name__)


class ExceptionHandlerMiddleware(BaseHTTPMiddleware):
    """
    Middleware pour gérer toutes les exceptions non capturées
    
    Features:
    - Log toutes les erreurs avec stack trace
    - Masque les détails en production
    - Format JSON cohérent
    - Inclut request_id si disponible
    """
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        try:
            return await call_next(request)
        
        except HTTPException:
            # Les HTTPException sont gérées par FastAPI
            raise
        
        except ValidationError as e:
            # Erreurs de validation Pydantic
            logger.warning(f"Validation error: {e}")
            return JSONResponse(
                status_code=422,
                content={
                    "error": "Validation Error",
                    "detail": e.errors(),
                    "request_id": getattr(request.state, 'request_id', None)
                }
            )
        
        except Exception as e:
            # Toute autre exception
            request_id = getattr(request.state, 'request_id', None)
            
            # Log l'erreur complète
            logger.error(
                f"Unhandled exception: {type(e).__name__}: {e}\n"
                f"Request: {request.method} {request.url}\n"
                f"Request ID: {request_id}\n"
                f"Traceback:\n{traceback.format_exc()}"
            )
            
            # Réponse sécurisée (pas de détails en production)
            import os
            is_dev = os.getenv("ENVIRONMENT", "development") == "development"
            
            error_detail = str(e) if is_dev else "An internal error occurred"
            
            return JSONResponse(
                status_code=500,
                content={
                    "error": "Internal Server Error",
                    "detail": error_detail,
                    "type": type(e).__name__ if is_dev else None,
                    "request_id": request_id
                }
            )


async def http_exception_handler(request: Request, exc: HTTPException):
    """Handler personnalisé pour HTTPException"""
    # Essayer d'obtenir le request_id de plusieurs façons
    request_id = None
    try:
        request_id = getattr(request.state, 'request_id', None)
    except:
        pass
    
    # Si toujours None, essayer depuis les headers
    if not request_id:
        request_id = request.headers.get("X-Request-ID")
    
    # Log les erreurs 5xx
    if exc.status_code >= 500:
        logger.error(f"HTTP {exc.status_code}: {exc.detail} [Request ID: {request_id}]")
    elif exc.status_code >= 400:
        logger.warning(f"HTTP {exc.status_code}: {exc.detail} [Request ID: {request_id}]")
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code,
            "request_id": request_id
        },
        headers=exc.headers
    )

