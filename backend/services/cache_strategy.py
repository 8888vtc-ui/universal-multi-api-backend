"""
Advanced Cache Strategy
Cache multi-niveaux avec invalidation intelligente
"""
import time
import hashlib
import json
from typing import Any, Optional, Dict, Callable, TypeVar
from functools import wraps
from collections import OrderedDict
import asyncio
from services.cache import cache_service


T = TypeVar('T')


class L1Cache:
    """
    Cache L1 - Mémoire locale (très rapide)
    LRU Cache avec TTL
    """
    
    def __init__(self, max_size: int = 1000, default_ttl: int = 60):
        self.max_size = max_size
        self.default_ttl = default_ttl
        self._cache: OrderedDict = OrderedDict()
        self._timestamps: Dict[str, float] = {}
        self._lock = asyncio.Lock()
    
    async def get(self, key: str) -> Optional[Any]:
        """Obtenir une valeur du cache"""
        async with self._lock:
            if key not in self._cache:
                return None
            
            # Vérifier TTL
            if time.time() - self._timestamps[key] > self.default_ttl:
                del self._cache[key]
                del self._timestamps[key]
                return None
            
            # Mettre à jour l'ordre LRU
            self._cache.move_to_end(key)
            return self._cache[key]
    
    async def set(self, key: str, value: Any, ttl: Optional[int] = None):
        """Définir une valeur dans le cache"""
        async with self._lock:
            # Supprimer si existe
            if key in self._cache:
                del self._cache[key]
            
            # Éviction LRU si nécessaire
            while len(self._cache) >= self.max_size:
                oldest_key = next(iter(self._cache))
                del self._cache[oldest_key]
                del self._timestamps[oldest_key]
            
            self._cache[key] = value
            self._timestamps[key] = time.time()
    
    async def delete(self, key: str):
        """Supprimer une valeur du cache"""
        async with self._lock:
            if key in self._cache:
                del self._cache[key]
                del self._timestamps[key]
    
    async def clear(self):
        """Vider le cache"""
        async with self._lock:
            self._cache.clear()
            self._timestamps.clear()
    
    def stats(self) -> Dict[str, Any]:
        """Statistiques du cache"""
        return {
            "size": len(self._cache),
            "max_size": self.max_size,
            "default_ttl": self.default_ttl
        }


class MultiLevelCache:
    """
    Cache multi-niveaux
    L1: Mémoire locale (rapide, petite)
    L2: Redis (plus lent, plus grand, persistant)
    """
    
    def __init__(
        self,
        l1_max_size: int = 1000,
        l1_ttl: int = 60,
        l2_ttl: int = 3600
    ):
        self.l1 = L1Cache(max_size=l1_max_size, default_ttl=l1_ttl)
        self.l2 = cache_service
        self.l2_ttl = l2_ttl
        
        # Statistiques
        self.stats_l1_hits = 0
        self.stats_l2_hits = 0
        self.stats_misses = 0
    
    def _generate_key(self, prefix: str, data: Any) -> str:
        """Générer une clé de cache"""
        if isinstance(data, dict):
            data = json.dumps(data, sort_keys=True)
        elif not isinstance(data, str):
            data = str(data)
        
        hash_obj = hashlib.md5(data.encode())
        return f"{prefix}:{hash_obj.hexdigest()}"
    
    async def get(self, prefix: str, key: Any) -> Optional[Any]:
        """
        Obtenir une valeur du cache
        Essaie L1 d'abord, puis L2
        """
        cache_key = self._generate_key(prefix, key)
        
        # Essayer L1
        value = await self.l1.get(cache_key)
        if value is not None:
            self.stats_l1_hits += 1
            return value
        
        # Essayer L2 (Redis)
        value = self.l2.get(prefix, str(key))
        if value is not None:
            self.stats_l2_hits += 1
            # Mettre en cache L1
            await self.l1.set(cache_key, value)
            return value
        
        self.stats_misses += 1
        return None
    
    async def set(
        self,
        prefix: str,
        key: Any,
        value: Any,
        l1_ttl: Optional[int] = None,
        l2_ttl: Optional[int] = None
    ):
        """
        Définir une valeur dans le cache
        Écrit dans L1 et L2
        """
        cache_key = self._generate_key(prefix, key)
        
        # Écrire dans L1
        await self.l1.set(cache_key, value, l1_ttl)
        
        # Écrire dans L2 (Redis)
        self.l2.set(prefix, str(key), value, l2_ttl or self.l2_ttl)
    
    async def delete(self, prefix: str, key: Any):
        """Supprimer une valeur du cache"""
        cache_key = self._generate_key(prefix, key)
        
        await self.l1.delete(cache_key)
        self.l2.delete(prefix, str(key))
    
    async def invalidate_prefix(self, prefix: str):
        """Invalider toutes les clés avec un préfixe"""
        # L1: Vider tout (simplification)
        await self.l1.clear()
        
        # L2: Redis peut supprimer par pattern
        # Note: Nécessite SCAN pour éviter KEYS en production
    
    def get_stats(self) -> Dict[str, Any]:
        """Obtenir les statistiques du cache"""
        total_requests = self.stats_l1_hits + self.stats_l2_hits + self.stats_misses
        
        return {
            "l1": {
                **self.l1.stats(),
                "hits": self.stats_l1_hits,
                "hit_rate": self.stats_l1_hits / total_requests if total_requests > 0 else 0
            },
            "l2": {
                "available": self.l2.available,
                "hits": self.stats_l2_hits,
                "hit_rate": self.stats_l2_hits / total_requests if total_requests > 0 else 0
            },
            "total_requests": total_requests,
            "misses": self.stats_misses,
            "overall_hit_rate": (self.stats_l1_hits + self.stats_l2_hits) / total_requests if total_requests > 0 else 0
        }


# Singleton
multi_level_cache = MultiLevelCache()


def cached(
    prefix: str,
    ttl: int = 3600,
    key_builder: Optional[Callable[..., str]] = None
):
    """
    Décorateur pour cacher les résultats d'une fonction
    
    Args:
        prefix: Préfixe de la clé de cache
        ttl: TTL en secondes
        key_builder: Fonction pour construire la clé à partir des arguments
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> T:
            # Construire la clé
            if key_builder:
                cache_key = key_builder(*args, **kwargs)
            else:
                cache_key = f"{args}:{kwargs}"
            
            # Essayer de récupérer du cache
            cached_value = await multi_level_cache.get(prefix, cache_key)
            if cached_value is not None:
                return cached_value
            
            # Exécuter la fonction
            result = await func(*args, **kwargs)
            
            # Mettre en cache
            await multi_level_cache.set(prefix, cache_key, result, l2_ttl=ttl)
            
            return result
        
        return wrapper
    return decorator


