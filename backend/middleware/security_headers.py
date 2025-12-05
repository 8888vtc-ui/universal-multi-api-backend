"""
Security Headers Middleware
Ajoute des headers de sécurité à toutes les réponses
"""
import os
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Middleware pour ajouter des headers de sécurité HTTP
    
    Headers ajoutés:
    - X-Content-Type-Options: Prevent MIME sniffing
    - X-Frame-Options: Clickjacking protection
    - X-XSS-Protection: XSS filter (legacy browsers)
    - Strict-Transport-Security: Force HTTPS
    - Content-Security-Policy: Control resources
    - Referrer-Policy: Control referrer info
    - Permissions-Policy: Disable unnecessary features
    """
    
    def __init__(self, app, enable_hsts: bool = None):
        super().__init__(app)
        # Enable HSTS only in production by default
        self.enable_hsts = enable_hsts if enable_hsts is not None else (
            os.getenv("ENVIRONMENT") == "production"
        )
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        response = await call_next(request)
        
        # Prevent MIME type sniffing
        response.headers["X-Content-Type-Options"] = "nosniff"
        
        # Clickjacking protection
        response.headers["X-Frame-Options"] = "DENY"
        
        # XSS protection for legacy browsers
        response.headers["X-XSS-Protection"] = "1; mode=block"
        
        # Referrer policy
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        
        # Permissions policy (disable unnecessary browser features)
        response.headers["Permissions-Policy"] = (
            "accelerometer=(), "
            "camera=(), "
            "geolocation=(), "
            "gyroscope=(), "
            "magnetometer=(), "
            "microphone=(), "
            "payment=(), "
            "usb=()"
        )
        
        # HSTS - Force HTTPS (only in production)
        if self.enable_hsts:
            response.headers["Strict-Transport-Security"] = (
                "max-age=31536000; includeSubDomains; preload"
            )
        
        # Content Security Policy
        # Permissive for API, stricter for web apps
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: https:; "
            "font-src 'self' data:; "
            "connect-src 'self' https:; "
            "frame-ancestors 'none'"
        )
        
        # API identifier
        response.headers["X-API-Version"] = "2.3.0"
        
        return response

