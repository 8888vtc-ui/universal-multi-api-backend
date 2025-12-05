"""
Circuit Breaker Pattern Implementation
Protection contre les appels API qui échouent répétitivement
"""
try:
    from circuitbreaker import circuit
    CIRCUIT_BREAKER_AVAILABLE = True
except ImportError:
    CIRCUIT_BREAKER_AVAILABLE = False
    print("WARNING: circuitbreaker not installed. Circuit breaker disabled.")


def circuit_breaker(name=None, failure_threshold=5, recovery_timeout=60):
    """
    Decorator pour circuit breaker
    
    Usage:
        @circuit_breaker(name="groq")
        async def my_api_call():
            ...
    """
    if CIRCUIT_BREAKER_AVAILABLE:
        return circuit(
            name=name,
            failure_threshold=failure_threshold,
            recovery_timeout=recovery_timeout,
            expected_exception=Exception
        )
    else:
        # Dummy decorator si circuitbreaker n'est pas disponible
        def dummy_decorator(func):
            return func
        return dummy_decorator
