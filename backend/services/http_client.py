"""
HTTP Client avec Connection Pooling et DNS personnalisé
Réutilise les connexions HTTP pour éviter l'overhead de création
"""
import httpx
from typing import Optional, Dict, Any, Tuple
import asyncio
import socket
import logging
from urllib.parse import urlparse

logger = logging.getLogger(__name__)


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
            
            # ✅ LOG: Tentative de résolution
            logger.debug(f"[DNS] Résolution de {hostname} avec Google DNS...")
            
            answers = resolver.resolve(hostname, 'A')
            ip = str(answers[0])
            
            # ✅ LOG: Résolution réussie
            logger.info(f"[DNS] ✅ {hostname} → {ip}")
            
            return ip
        except Exception as e:
            # ✅ LOG: Erreur DNS
            logger.warning(f"[DNS] ⚠️ Résolution Google DNS échouée pour {hostname}: {e}")
            
            # Fallback sur la résolution système
            try:
                ip = socket.gethostbyname(hostname)
                logger.info(f"[DNS] ✅ Fallback système: {hostname} → {ip}")
                return ip
            except Exception as e2:
                logger.error(f"[DNS] ❌ Résolution système échouée pour {hostname}: {e2}")
                return hostname
    
    @staticmethod
    def resolve_url(url: str) -> Tuple[str, Optional[str]]:
        """
        Résoudre le DNS d'une URL et retourner (url_avec_ip, hostname_original)
        Si le DNS échoue, retourne l'URL originale
        """
        try:
            parsed = urlparse(url)
            hostname = parsed.hostname
            
            if not hostname:
                return url, None
            
            # Ne pas résoudre localhost ou IPs
            if hostname in ['localhost', '127.0.0.1'] or hostname.replace('.', '').isdigit():
                return url, None
            
            # Résoudre le DNS
            ip_address = CustomDNSResolver.resolve_dns(hostname)
            
            # Si résolution réussie et différente du hostname
            if ip_address != hostname:
                # Reconstruire l'URL avec l'IP
                new_url = url.replace(hostname, ip_address)
                logger.info(f"[DNS] 🔄 URL résolue: {url} → {new_url} (Host: {hostname})")
                return new_url, hostname
            
            return url, None
        except Exception as e:
            logger.warning(f"[DNS] Erreur lors de la résolution de {url}: {e}")
            return url, None


class HTTPClientPool:
    """
    Pool de connexions HTTP asynchrones avec DNS personnalisé
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
        """GET request avec DNS personnalisé et connection pooling"""
        # ✅ TEMPORAIRE: Désactiver la résolution DNS pour test
        # resolved_url, original_host = CustomDNSResolver.resolve_url(url)
        resolved_url = url
        original_host = None
        
        client = await self.get_client()
        
        # ✅ Ajouter le header Host si on utilise l'IP
        headers = kwargs.get('headers', {})
        if original_host:
            headers['Host'] = original_host
            kwargs['headers'] = headers
            logger.debug(f"[DNS] Utilisation de l'IP avec header Host: {original_host}")
        
        try:
            logger.info(f"[HTTP] GET {resolved_url}")
            response = await client.get(resolved_url, **kwargs)
            logger.info(f"[HTTP] Response: {response.status_code}")
            return response
        except Exception as e:
            logger.error(f"[HTTP] Erreur GET {url}: {e}")
            raise
    
    async def post(self, url: str, **kwargs) -> httpx.Response:
        """POST request avec DNS personnalisé et connection pooling"""
        # ✅ RÉSOLUTION DNS AVANT L'APPEL
        resolved_url, original_host = CustomDNSResolver.resolve_url(url)
        
        client = await self.get_client()
        
        # ✅ Ajouter le header Host si on utilise l'IP
        headers = kwargs.get('headers', {})
        if original_host:
            headers['Host'] = original_host
            kwargs['headers'] = headers
            logger.debug(f"[DNS] Utilisation de l'IP avec header Host: {original_host}")
        
        try:
            response = await client.post(resolved_url, **kwargs)
            return response
        except Exception as e:
            logger.error(f"[HTTP] Erreur POST {url}: {e}")
            raise
    
    async def put(self, url: str, **kwargs) -> httpx.Response:
        """PUT request avec DNS personnalisé et connection pooling"""
        resolved_url, original_host = CustomDNSResolver.resolve_url(url)
        client = await self.get_client()
        headers = kwargs.get('headers', {})
        if original_host:
            headers['Host'] = original_host
            kwargs['headers'] = headers
        return await client.put(resolved_url, **kwargs)
    
    async def delete(self, url: str, **kwargs) -> httpx.Response:
        """DELETE request avec DNS personnalisé et connection pooling"""
        resolved_url, original_host = CustomDNSResolver.resolve_url(url)
        client = await self.get_client()
        headers = kwargs.get('headers', {})
        if original_host:
            headers['Host'] = original_host
            kwargs['headers'] = headers
        return await client.delete(resolved_url, **kwargs)


# Singleton instance
http_client = HTTPClientPool()


async def get_http_client() -> httpx.AsyncClient:
    """Helper pour obtenir le client HTTP"""
    return await http_client.get_client()


# Cleanup on shutdown
async def cleanup_http_client():
    """Fermer le client HTTP lors de l'arrêt"""
    await http_client.close()
