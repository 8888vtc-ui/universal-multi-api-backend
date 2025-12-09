"""
Request ID Middleware
Ajoute un ID unique à chaque requête pour le tracing
"""
import uuid
import logging
from typing import Callable
from contextvars import ContextVar
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

# Context variable pour stocker le request ID
request_id_ctx: ContextVar[str] = ContextVar("request_id", default="")

logger = logging.getLogger(__name__)


def get_request_id() -> str:
    """Obtenir le request ID courant (pour utilisation dans les logs)"""
    return request_id_ctx.get()


class RequestIDFilter(logging.Filter):
    """Filter pour ajouter le request ID aux logs"""
    
    def filter(self, record):
        record.request_id = get_request_id() or "-"
        return True


class RequestIDMiddleware(BaseHTTPMiddleware):
    """
    Middleware pour ajouter un ID unique à chaque requête
    
    Features:
    - Génère un UUID pour chaque requête
    - Utilise X-Request-ID du client si fourni
    - Ajoute l'ID dans les headers de réponse
    - Stocke dans ContextVar pour les logs
    """
    
    HEADER_NAME = "X-Request-ID"
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Utiliser l'ID fourni par le client ou en générer un nouveau
        request_id = request.headers.get(self.HEADER_NAME) or str(uuid.uuid4())
        
        # Stocker dans le context pour les logs
        token = request_id_ctx.set(request_id)
        
        try:
            # Ajouter à la request state pour accès dans les handlers
            request.state.request_id = request_id
            
            # Traiter la requête
            response = await call_next(request)
            
            # Ajouter l'ID dans la réponse
            response.headers[self.HEADER_NAME] = request_id
            
            return response
        finally:
            # Reset le context
            request_id_ctx.reset(token)


def setup_request_id_logging():
    """
    Configure le logging pour inclure le request ID
    
    Usage dans main.py:
        from middleware.request_id import setup_request_id_logging
        setup_request_id_logging()
    """
    # Format avec request_id
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(request_id)s | %(name)s:%(lineno)d | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    # Ajouter le filter au root logger
    root_logger = logging.getLogger()
    
    # Ajouter le filter à tous les handlers
    request_filter = RequestIDFilter()
    for handler in root_logger.handlers:
        handler.addFilter(request_filter)
        handler.setFormatter(formatter)
