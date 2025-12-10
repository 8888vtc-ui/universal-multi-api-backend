"""
HTTP Client avec Connection Pooling
Client HTTP simplifié qui utilise le DNS système (fonctionne sur Fly.io)
"""
import httpx
from typing import Optional
import asyncio
import logging

logger = logging.getLogger(__name__)


class HTTPClientPool:
    """
    Pool de connexions HTTP asynchrones
    Réutilise les connexions pour éviter l'overhead de création
    """
    
    _instance: Optional['HTTPClientPool'] = None
    _client: Optional[httpx.AsyncClient] = None
    _lock = asyncio.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    async def get_client(self) -> httpx.AsyncClient:
        """Obtenir le client HTTP avec connection pooling"""
        async with self._lock:
            if self._client is None or self._client.is_closed:
                self._client = httpx.AsyncClient(
                    timeout=httpx.Timeout(
                        connect=10.0,
                        read=30.0,
                        write=10.0,
                        pool=5.0
                    ),
                    limits=httpx.Limits(
                        max_connections=100,
                        max_keepalive_connections=20,
                        keepalive_expiry=30.0
                    ),
                    http2=True,
                    follow_redirects=True,
                )
                logger.info("✅ HTTPClientPool initialized")
        return self._client
    
    async def close(self):
        """Fermer le client"""
        async with self._lock:
            if self._client and not self._client.is_closed:
                await self._client.aclose()
                self._client = None
    
    async def get(self, url: str, **kwargs) -> httpx.Response:
        """GET request avec connection pooling"""
        client = await self.get_client()
        try:
            response = await client.get(url, **kwargs)
            logger.debug(f"[HTTP] GET {url} → {response.status_code}")
            return response
        except Exception as e:
            logger.error(f"[HTTP] Erreur GET {url}: {e}")
            raise
    
    async def post(self, url: str, **kwargs) -> httpx.Response:
        """POST request avec connection pooling"""
        client = await self.get_client()
        try:
            response = await client.post(url, **kwargs)
            logger.debug(f"[HTTP] POST {url} → {response.status_code}")
            return response
        except Exception as e:
            logger.error(f"[HTTP] Erreur POST {url}: {e}")
            raise
    
    async def put(self, url: str, **kwargs) -> httpx.Response:
        """PUT request avec connection pooling"""
        client = await self.get_client()
        return await client.put(url, **kwargs)
    
    async def delete(self, url: str, **kwargs) -> httpx.Response:
        """DELETE request avec connection pooling"""
        client = await self.get_client()
        return await client.delete(url, **kwargs)


# Singleton instance
http_client = HTTPClientPool()


async def get_http_client() -> httpx.AsyncClient:
    """Helper pour obtenir le client HTTP"""
    return await http_client.get_client()


# Cleanup on shutdown
async def cleanup_http_client():
    """Fermer le client HTTP lors de l'arrêt"""
    await http_client.close()
