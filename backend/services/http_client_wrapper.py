"""
HTTP Client Wrapper - Compatibilité globale
Remplace httpx.AsyncClient par http_client avec DNS personnalisé
"""
import httpx
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)


class AsyncClientWrapper:
    """
    Wrapper compatible avec httpx.AsyncClient mais utilise http_client en interne
    Permet de remplacer httpx.AsyncClient sans modifier le code existant
    """
    
    def __init__(self, timeout: Optional[float] = None, **kwargs):
        """
        Compatible avec httpx.AsyncClient(timeout=10.0)
        Les kwargs sont ignorés car http_client gère déjà la configuration
        """
        self.timeout = timeout
        self._kwargs = kwargs
        logger.debug(f"[HTTP_WRAPPER] AsyncClientWrapper créé (timeout={timeout})")
    
    async def __aenter__(self):
        """Context manager entry"""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - rien à fermer car http_client est un singleton"""
        pass
    
    async def get(self, url: str, **kwargs) -> httpx.Response:
        """GET request - utilise http_client avec DNS personnalisé"""
        from services.http_client import http_client as _http_client_pool
        try:
            # Utiliser http_client qui a le DNS resolver intégré
            response = await _http_client_pool.get(url, **kwargs)
            logger.debug(f"[HTTP_WRAPPER] GET {url} → {response.status_code}")
            return response
        except Exception as e:
            logger.error(f"[HTTP_WRAPPER] Erreur GET {url}: {e}")
            raise
    
    async def post(self, url: str, **kwargs) -> httpx.Response:
        """POST request - utilise http_client avec DNS personnalisé"""
        from services.http_client import http_client as _http_client_pool
        try:
            response = await _http_client_pool.post(url, **kwargs)
            logger.debug(f"[HTTP_WRAPPER] POST {url} → {response.status_code}")
            return response
        except Exception as e:
            logger.error(f"[HTTP_WRAPPER] Erreur POST {url}: {e}")
            raise
    
    async def put(self, url: str, **kwargs) -> httpx.Response:
        """PUT request"""
        from services.http_client import http_client as _http_client_pool
        try:
            response = await _http_client_pool.put(url, **kwargs)
            return response
        except Exception as e:
            logger.error(f"[HTTP_WRAPPER] Erreur PUT {url}: {e}")
            raise
    
    async def delete(self, url: str, **kwargs) -> httpx.Response:
        """DELETE request"""
        from services.http_client import http_client as _http_client_pool
        try:
            response = await _http_client_pool.delete(url, **kwargs)
            return response
        except Exception as e:
            logger.error(f"[HTTP_WRAPPER] Erreur DELETE {url}: {e}")
            raise


# Variable globale pour suivre l'état du patch
_is_patched = False
_original_async_client = None


def patch_httpx():
    """
    Remplace httpx.AsyncClient par AsyncClientWrapper globalement
    À appeler au démarrage de l'application
    """
    global _is_patched, _original_async_client
    
    if _is_patched:
        logger.debug("[HTTP_WRAPPER] httpx.AsyncClient déjà patché")
        return
    
    import httpx
    
    # Sauvegarder l'original (au cas où)
    _original_async_client = httpx.AsyncClient
    
    # Remplacer par notre wrapper
    httpx.AsyncClient = AsyncClientWrapper
    
    _is_patched = True
    logger.info("✅ [HTTP_WRAPPER] httpx.AsyncClient remplacé par AsyncClientWrapper (DNS personnalisé activé)")


def unpatch_httpx():
    """Restaurer httpx.AsyncClient original"""
    global _is_patched, _original_async_client
    
    if not _is_patched or _original_async_client is None:
        logger.debug("[HTTP_WRAPPER] Rien à restaurer")
        return
    
    import httpx
    httpx.AsyncClient = _original_async_client
    _is_patched = False
    logger.info("✅ [HTTP_WRAPPER] httpx.AsyncClient restauré")


def is_patched() -> bool:
    """Vérifier si httpx est patché"""
    return _is_patched
