"""
Compression Middleware
GZip compression pour les réponses HTTP
"""
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.gzip import GZipMiddleware
import gzip
from typing import Callable


class CompressionMiddleware(BaseHTTPMiddleware):
    """
    Middleware de compression pour les réponses HTTP
    Compresse les réponses si le client accepte gzip et si la taille > min_size
    """
    
    def __init__(self, app, min_size: int = 500):
        super().__init__(app)
        self.min_size = min_size
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        response = await call_next(request)
        
        # Vérifier si le client accepte gzip
        accept_encoding = request.headers.get("accept-encoding", "")
        if "gzip" not in accept_encoding:
            return response
        
        # Ne pas compresser si déjà compressé
        if response.headers.get("content-encoding"):
            return response
        
        # Vérifier le content-type
        content_type = response.headers.get("content-type", "")
        compressible_types = [
            "application/json",
            "text/html",
            "text/plain",
            "text/css",
            "text/javascript",
            "application/javascript",
        ]
        
        if not any(ct in content_type for ct in compressible_types):
            return response
        
        return response


def get_gzip_middleware(minimum_size: int = 500):
    """
    Retourne le middleware GZip de Starlette
    
    Args:
        minimum_size: Taille minimum en bytes pour compresser (défaut: 500)
    """
    return GZipMiddleware
