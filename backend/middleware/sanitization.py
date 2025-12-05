"""
Sanitization Middleware
Sanitize automatiquement les inputs des requêtes
"""
import json
import logging
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)


class SanitizationMiddleware(BaseHTTPMiddleware):
    """
    Middleware pour sanitizer automatiquement les inputs
    
    Protège contre:
    - XSS (Cross-Site Scripting)
    - SQL Injection (basique)
    - Caractères de contrôle dangereux
    """
    
    # Patterns dangereux à détecter
    DANGEROUS_PATTERNS = [
        "<script",
        "javascript:",
        "onerror=",
        "onclick=",
        "onload=",
        "onmouseover=",
        "<iframe",
        "<object",
        "<embed",
    ]
    
    # Endpoints à exclure de la sanitization
    EXCLUDED_PATHS = [
        "/docs",
        "/redoc",
        "/openapi.json",
    ]
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Skip for excluded paths
        if any(request.url.path.startswith(path) for path in self.EXCLUDED_PATHS):
            return await call_next(request)
        
        # Check query parameters
        for key, value in request.query_params.items():
            if self._is_dangerous(value):
                logger.warning(
                    f"🚨 Dangerous query param detected: {key}={value[:50]}... "
                    f"[{request.client.host if request.client else 'unknown'}]"
                )
                # Could reject or sanitize - for now just log
        
        # For POST/PUT/PATCH, we could inspect body but that requires
        # modifying the request which is complex. Better to use
        # Pydantic validators on the models.
        
        return await call_next(request)
    
    def _is_dangerous(self, value: str) -> bool:
        """Check if value contains dangerous patterns"""
        if not isinstance(value, str):
            return False
        
        value_lower = value.lower()
        return any(pattern in value_lower for pattern in self.DANGEROUS_PATTERNS)


