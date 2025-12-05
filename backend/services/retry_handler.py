"""
Retry Handler with Exponential Backoff
Gestion des retries avec backoff exponentiel pour appels API
"""
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
    RetryError
)
from typing import Callable, Any, Type
import functools


def with_retry(
    max_attempts: int = 3,
    initial_wait: float = 1.0,
    max_wait: float = 10.0,
    retry_exceptions: tuple = (Exception,)
):
    """
    Decorator pour retry avec backoff exponentiel
    
    Usage:
        @with_retry(max_attempts=3)
        async def my_api_call():
            ...
    """
    def decorator(func: Callable) -> Callable:
        @retry(
            stop=stop_after_attempt(max_attempts),
            wait=wait_exponential(multiplier=initial_wait, max=max_wait),
            retry=retry_if_exception_type(retry_exceptions),
            reraise=True
        )
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            return await func(*args, **kwargs)
        
        return wrapper
    return decorator


# Helper pour retry synchrone
def with_retry_sync(
    max_attempts: int = 3,
    initial_wait: float = 1.0,
    max_wait: float = 10.0,
    retry_exceptions: tuple = (Exception,)
):
    """Decorator pour retry synchrone"""
    def decorator(func: Callable) -> Callable:
        @retry(
            stop=stop_after_attempt(max_attempts),
            wait=wait_exponential(multiplier=initial_wait, max=max_wait),
            retry=retry_if_exception_type(retry_exceptions),
            reraise=True
        )
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        
        return wrapper
    return decorator
