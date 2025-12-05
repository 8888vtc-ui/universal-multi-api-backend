"""
Redis cache service for AI responses
"""
import json
import hashlib
from typing import Optional, Any
from redis import Redis
from redis.exceptions import RedisError
import os
from dotenv import load_dotenv

load_dotenv()


class CacheService:
    """Redis cache service with fallback"""
    
    def __init__(self):
        try:
            from redis.connection import ConnectionPool
            
            pool = ConnectionPool(
                host=os.getenv("REDIS_HOST", "localhost"),
                port=int(os.getenv("REDIS_PORT", 6379)),
                db=int(os.getenv("REDIS_DB", 0)),
                password=os.getenv("REDIS_PASSWORD") or None,
                max_connections=50,
                decode_responses=True,
                socket_connect_timeout=2
            )
            
            self.redis = Redis(connection_pool=pool)
            # Test connection
            self.redis.ping()
            self.available = True
            print("✅ Redis cache connected")
        except (RedisError, Exception) as e:
            print(f"⚠️  Redis unavailable: {e}. Running without cache.")
            self.available = False
    
    def _generate_key(self, prefix: str, data: str) -> str:
        """Generate cache key from data"""
        hash_obj = hashlib.md5(data.encode())
        return f"{prefix}:{hash_obj.hexdigest()}"
    
    def get(self, prefix: str, data: str) -> Optional[Any]:
        """Get cached value"""
        if not self.available:
            return None
        
        try:
            key = self._generate_key(prefix, data)
            cached = self.redis.get(key)
            if cached:
                return json.loads(cached)
            return None
        except Exception as e:
            print(f"Cache get error: {e}")
            return None
    
    def set(self, prefix: str, data: str, value: Any, ttl: int = 3600):
        """Set cached value with TTL"""
        if not self.available:
            return
        
        try:
            key = self._generate_key(prefix, data)
            self.redis.setex(
                key,
                ttl,
                json.dumps(value)
            )
        except Exception as e:
            print(f"Cache set error: {e}")
    
    def delete(self, prefix: str, data: str):
        """Delete cached value"""
        if not self.available:
            return
        
        try:
            key = self._generate_key(prefix, data)
            self.redis.delete(key)
        except Exception as e:
            print(f"Cache delete error: {e}")
    
    def health_check(self) -> bool:
        """Check if cache is healthy"""
        if not self.available:
            return False
        
        try:
            return self.redis.ping()
        except:
            return False

    # Quota Management Methods
    
    def _get_quota_key(self, provider: str) -> str:
        """Generate quota key for today"""
        from datetime import datetime
        today = datetime.now().strftime("%Y-%m-%d")
        return f"quota:{provider}:{today}"

    def increment_quota_usage(self, provider: str, amount: int = 1) -> int:
        """Increment quota usage for a provider"""
        if not self.available:
            return 0
        
        try:
            key = self._get_quota_key(provider)
            # Increment and set expiry to 24h + buffer if new key
            pipe = self.redis.pipeline()
            pipe.incrby(key, amount)
            pipe.expire(key, 86400 * 2)  # Keep for 2 days just in case
            result = pipe.execute()
            return result[0]
        except Exception as e:
            print(f"Quota increment error: {e}")
            return 0

    def get_quota_usage(self, provider: str) -> int:
        """Get current quota usage for a provider"""
        if not self.available:
            return 0
        
        try:
            key = self._get_quota_key(provider)
            val = self.redis.get(key)
            return int(val) if val else 0
        except Exception as e:
            print(f"Quota get error: {e}")
            return 0

    def check_quota_available(self, provider: str, daily_quota: int) -> bool:
        """Check if quota is available"""
        if daily_quota == 0:  # Unlimited
            return True
            
        if not self.available:
            # Fallback to memory if Redis unavailable (handled in provider)
            return True
            
        current = self.get_quota_usage(provider)
        return current < daily_quota


# Singleton instance
cache_service = CacheService()
