"""
HTTP Client avec Connection Pooling
Réutilise les connexions HTTP pour de meilleures performances
"""
import httpx
from typing import Optional, Dict, Any
import asyncio
import socket


class CustomDNSResolver:
    """Résolveur DNS personnalisé utilisant Google DNS"""
    
    @staticmethod
    def resolve_dns(hostname: str) -> str:
        """Résoudre le DNS en utilisant les serveurs Google"""
        try:
            # Utiliser les serveurs DNS Google
            import dns.resolver
            resolver = dns.resolver.Resolver()
            resolver.nameservers = ['8.8.8.8', '8.8.4.4', '1.1.1.1']
            resolver.lifetime = 5.0
            answers = resolver.resolve(hostname, 'A')
            return str(answers[0])
        except Exception:
            # Fallback sur la résolution système
            try:
                return socket.gethostbyname(hostname)
            except Exception:
                return hostname


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
                        connect=10.0,  # Augmenté pour DNS lent
                        read=30.0,
                        write=10.0,
                        pool=5.0
                    ),
                    limits=httpx.Limits(
                        max_connections=100,
                        max_keepalive_connections=20,
                        keepalive_expiry=30.0
                    ),
                    http2=True,  # Support HTTP/2 pour meilleures performances
                    follow_redirects=True,  # Suivre les redirections
                )
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
        return await client.get(url, **kwargs)
    
    async def post(self, url: str, **kwargs) -> httpx.Response:
        """POST request avec connection pooling"""
        client = await self.get_client()
        return await client.post(url, **kwargs)
    
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
