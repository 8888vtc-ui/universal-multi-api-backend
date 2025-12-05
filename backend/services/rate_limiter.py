"""
Rate Limiter Service
Gestion du rate limiting avec slowapi
"""
try:
    from slowapi import Limiter, _rate_limit_exceeded_handler
    from slowapi.util import get_remote_address
    from slowapi.errors import RateLimitExceeded
    SLOWAPI_AVAILABLE = True
except ImportError:
    SLOWAPI_AVAILABLE = False
    print("⚠️  slowapi not installed. Rate limiting disabled. Install with: pip install slowapi")


# Créer le limiter
if SLOWAPI_AVAILABLE:
    limiter = Limiter(
        key_func=get_remote_address,
        default_limits=["1000/hour", "100/minute"],  # Limites par défaut
        storage_uri="memory://"  # Stockage en mémoire (peut être changé pour Redis)
    )
else:
    # Dummy limiter si slowapi n'est pas disponible
    limiter = None


# Limites spécifiques par endpoint
ENDPOINT_LIMITS = {
    # AI endpoints - plus restrictifs
    "/api/chat": ["50/hour", "10/minute"],
    "/api/embeddings": ["100/hour", "20/minute"],
    
    # Search - modéré
    "/api/search/universal": ["200/hour", "30/minute"],
    "/api/search/quick": ["500/hour", "50/minute"],
    
    # Video - très restrictif (coûteux)
    "/api/video/avatar/create": ["20/hour", "5/minute"],
    "/api/video/course/generate": ["10/hour", "2/minute"],
    
    # Assistant - modéré
    "/api/assistant/learn": ["500/hour", "100/minute"],
    "/api/assistant/recommendations": ["200/hour", "30/minute"],
    
    # Aggregated - modéré
    "/api/aggregated": ["100/hour", "20/minute"],
    
    # Health - très permissif
    "/api/health": ["10000/hour"],
}


def get_limit_for_endpoint(endpoint: str) -> list:
    """Obtenir la limite pour un endpoint spécifique"""
    # Chercher correspondance exacte
    if endpoint in ENDPOINT_LIMITS:
        return ENDPOINT_LIMITS[endpoint]
    
    # Chercher correspondance partielle
    for pattern, limits in ENDPOINT_LIMITS.items():
        if endpoint.startswith(pattern):
            return limits
    
    # Limite par défaut
    return ["1000/hour", "100/minute"]


# Fonction helper pour appliquer rate limit
def apply_rate_limit(endpoint: str = None):
    """
    Appliquer rate limit à un endpoint
    
    Usage:
        @router.get("/endpoint")
        @apply_rate_limit("/api/endpoint")
        async def my_endpoint():
            ...
    """
    if not SLOWAPI_AVAILABLE or not limiter:
        # Dummy decorator si slowapi n'est pas disponible
        def dummy_decorator(func):
            return func
        return dummy_decorator
    
    if endpoint:
        limits = get_limit_for_endpoint(endpoint)
        return limiter.limit(limits[0])
    return limiter.limit("1000/hour")


# Helper pour utiliser limiter dans les routers
def get_limiter():
    """Obtenir le limiter (ou None si non disponible)"""
    return limiter if SLOWAPI_AVAILABLE else None
