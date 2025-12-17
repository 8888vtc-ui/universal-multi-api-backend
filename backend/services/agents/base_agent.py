"""
🤖 BASE AGENT CLASS - OPTIMIZED VERSION
All agents inherit from this base class.

OPTIMIZATIONS:
- Retry logic with exponential backoff
- Fallback between AI models
- Response caching
- Performance metrics
- Better error handling
"""
import os
import logging
import httpx
import hashlib
import asyncio
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from functools import lru_cache

logger = logging.getLogger(__name__)


class ResponseCache:
    """Simple in-memory cache for AI responses"""
    
    def __init__(self, ttl_seconds: int = 300):
        self.cache: Dict[str, tuple] = {}  # key -> (response, timestamp)
        self.ttl = timedelta(seconds=ttl_seconds)
    
    def _hash_key(self, prompt: str, model: str) -> str:
        """Create a hash key from prompt and model"""
        content = f"{model}:{prompt}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def get(self, prompt: str, model: str) -> Optional[str]:
        """Get cached response if valid"""
        key = self._hash_key(prompt, model)
        if key in self.cache:
            response, timestamp = self.cache[key]
            if datetime.now() - timestamp < self.ttl:
                logger.debug(f"Cache HIT for {model}")
                return response
            else:
                del self.cache[key]  # Expired
        return None
    
    def set(self, prompt: str, model: str, response: str):
        """Cache a response"""
        key = self._hash_key(prompt, model)
        self.cache[key] = (response, datetime.now())
        # Clean old entries (max 100)
        if len(self.cache) > 100:
            oldest_key = min(self.cache, key=lambda k: self.cache[k][1])
            del self.cache[oldest_key]


class AgentMetrics:
    """Track agent performance metrics"""
    
    def __init__(self):
        self.total_requests = 0
        self.successful_requests = 0
        self.failed_requests = 0
        self.total_response_time = 0.0
        self.cache_hits = 0
        self.fallback_count = 0
        self.errors_by_type: Dict[str, int] = {}
    
    def record_request(self, success: bool, response_time: float, cached: bool = False, error_type: str = None):
        self.total_requests += 1
        if success:
            self.successful_requests += 1
        else:
            self.failed_requests += 1
            if error_type:
                self.errors_by_type[error_type] = self.errors_by_type.get(error_type, 0) + 1
        self.total_response_time += response_time
        if cached:
            self.cache_hits += 1
    
    def record_fallback(self):
        self.fallback_count += 1
    
    @property
    def avg_response_time(self) -> float:
        if self.total_requests == 0:
            return 0
        return self.total_response_time / self.total_requests
    
    @property
    def success_rate(self) -> float:
        if self.total_requests == 0:
            return 0
        return self.successful_requests / self.total_requests * 100
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "total_requests": self.total_requests,
            "successful": self.successful_requests,
            "failed": self.failed_requests,
            "success_rate": f"{self.success_rate:.1f}%",
            "avg_response_time": f"{self.avg_response_time:.2f}s",
            "cache_hits": self.cache_hits,
            "fallbacks": self.fallback_count,
            "errors_by_type": self.errors_by_type
        }


# Global cache shared by all agents
_global_cache = ResponseCache(ttl_seconds=300)


class BaseAgent(ABC):
    """Base class for all AI agents - OPTIMIZED"""
    
    # Fallback chain for each primary model
    FALLBACK_MODELS = {
        "gpt-4o": ["gpt-4o-mini", "groq", "deepseek"],
        "claude-3.5-sonnet": ["groq", "gpt-4o-mini", "deepseek"],
        "deepseek-coder": ["groq", "gpt-4o-mini", "claude-3.5-sonnet"],
        "groq-llama3": ["deepseek", "gpt-4o-mini", "claude-3.5-sonnet"],
    }
    
    MAX_RETRIES = 3
    RETRY_DELAY = 1.0  # Initial delay in seconds
    
    def __init__(self, name: str, model: str, role: str):
        self.name = name
        self.model = model
        self.role = role
        self.status = "idle"
        self.last_action = None
        self.task_history: List[Dict] = []
        self.metrics = AgentMetrics()
        self.use_cache = True  # Enable caching by default
        
    async def think(self, prompt: str, context: Optional[Dict] = None, use_cache: bool = True) -> str:
        """Use the AI model to think/reason about a task - WITH RETRY AND FALLBACK"""
        start_time = datetime.now()
        
        # Check cache first
        if use_cache and self.use_cache:
            cached = _global_cache.get(prompt, self.model)
            if cached:
                self.metrics.record_request(True, 0.01, cached=True)
                return cached
        
        # Try primary model with retries
        result = await self._call_with_retry(self.model, prompt, context)
        
        # If failed, try fallback models
        if result.startswith("ERROR:"):
            self.metrics.record_fallback()
            fallbacks = self.FALLBACK_MODELS.get(self.model, ["groq"])
            
            for fallback_model in fallbacks:
                logger.warning(f"[{self.name}] Falling back to {fallback_model}")
                result = await self._call_with_retry(fallback_model, prompt, context)
                if not result.startswith("ERROR:"):
                    break
        
        # Record metrics
        response_time = (datetime.now() - start_time).total_seconds()
        success = not result.startswith("ERROR:")
        self.metrics.record_request(success, response_time, error_type=result[:50] if not success else None)
        
        # Cache successful responses
        if success and use_cache and self.use_cache:
            _global_cache.set(prompt, self.model, result)
        
        return result
    
    async def _call_with_retry(self, model: str, prompt: str, context: Optional[Dict] = None) -> str:
        """Call AI model with retry logic"""
        last_error = None
        
        for attempt in range(self.MAX_RETRIES):
            try:
                result = await self._route_to_provider(model, prompt, context)
                if not result.startswith("ERROR:"):
                    return result
                last_error = result
            except Exception as e:
                last_error = f"ERROR: {str(e)}"
                logger.warning(f"[{self.name}] Attempt {attempt + 1} failed: {e}")
            
            # Exponential backoff
            if attempt < self.MAX_RETRIES - 1:
                delay = self.RETRY_DELAY * (2 ** attempt)
                await asyncio.sleep(delay)
        
        return last_error or "ERROR: All retries failed"
    
    async def _route_to_provider(self, model: str, prompt: str, context: Optional[Dict] = None) -> str:
        """Route to the appropriate AI provider"""
        if "gpt" in model or "openai" in model:
            return await self._call_openai(prompt, context, model)
        elif "claude" in model or "anthropic" in model:
            return await self._call_anthropic(prompt, context)
        elif "deepseek" in model:
            return await self._call_deepseek(prompt, context)
        elif "groq" in model or "llama" in model:
            return await self._call_groq(prompt, context)
        else:
            return await self._call_groq(prompt, context)
    
    async def _call_openai(self, prompt: str, context: Optional[Dict] = None, model: str = "gpt-4o") -> str:
        """Call OpenAI GPT with configurable model"""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return "ERROR: Missing OpenAI API key"
        
        actual_model = "gpt-4o-mini" if "mini" in model else "gpt-4o"
        
        try:
            async with httpx.AsyncClient(timeout=90.0) as client:
                response = await client.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers={"Authorization": f"Bearer {api_key}"},
                    json={
                        "model": actual_model,
                        "messages": [
                            {"role": "system", "content": f"You are {self.name}. Role: {self.role}"},
                            {"role": "user", "content": prompt}
                        ],
                        "max_tokens": 4000,
                        "temperature": 0.7
                    }
                )
                response.raise_for_status()
                data = response.json()
                return data.get("choices", [{}])[0].get("message", {}).get("content", "No response")
        except httpx.TimeoutException:
            return "ERROR: OpenAI timeout"
        except httpx.HTTPStatusError as e:
            return f"ERROR: OpenAI HTTP {e.response.status_code}"
        except Exception as e:
            return f"ERROR: OpenAI {str(e)}"
    
    async def _call_anthropic(self, prompt: str, context: Optional[Dict] = None) -> str:
        """Call Anthropic Claude"""
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            return "ERROR: Missing Anthropic API key"
        
        try:
            async with httpx.AsyncClient(timeout=90.0) as client:
                response = await client.post(
                    "https://api.anthropic.com/v1/messages",
                    headers={
                        "x-api-key": api_key,
                        "anthropic-version": "2023-06-01",
                        "content-type": "application/json"
                    },
                    json={
                        "model": "claude-3-5-sonnet-20241022",
                        "max_tokens": 4000,
                        "system": f"You are {self.name}. Role: {self.role}",
                        "messages": [{"role": "user", "content": prompt}]
                    }
                )
                response.raise_for_status()
                data = response.json()
                return data.get("content", [{}])[0].get("text", "No response")
        except httpx.TimeoutException:
            return "ERROR: Anthropic timeout"
        except httpx.HTTPStatusError as e:
            return f"ERROR: Anthropic HTTP {e.response.status_code}"
        except Exception as e:
            return f"ERROR: Anthropic {str(e)}"
    
    async def _call_deepseek(self, prompt: str, context: Optional[Dict] = None) -> str:
        """Call DeepSeek"""
        api_key = os.getenv("DEEPSEEK_API_KEY")
        if not api_key:
            return "ERROR: Missing DeepSeek API key"
        
        try:
            async with httpx.AsyncClient(timeout=90.0) as client:
                response = await client.post(
                    "https://api.deepseek.com/v1/chat/completions",
                    headers={"Authorization": f"Bearer {api_key}"},
                    json={
                        "model": "deepseek-coder",
                        "messages": [
                            {"role": "system", "content": f"You are {self.name}. Role: {self.role}"},
                            {"role": "user", "content": prompt}
                        ],
                        "max_tokens": 4000
                    }
                )
                response.raise_for_status()
                data = response.json()
                return data.get("choices", [{}])[0].get("message", {}).get("content", "No response")
        except httpx.TimeoutException:
            return "ERROR: DeepSeek timeout"
        except httpx.HTTPStatusError as e:
            return f"ERROR: DeepSeek HTTP {e.response.status_code}"
        except Exception as e:
            return f"ERROR: DeepSeek {str(e)}"
    
    async def _call_groq(self, prompt: str, context: Optional[Dict] = None) -> str:
        """Call Groq (Llama 3) - FASTEST"""
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            return "ERROR: Missing Groq API key"
        
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={"Authorization": f"Bearer {api_key}"},
                    json={
                        "model": "llama-3.3-70b-versatile",
                        "messages": [
                            {"role": "system", "content": f"You are {self.name}. Role: {self.role}"},
                            {"role": "user", "content": prompt}
                        ],
                        "max_tokens": 4000
                    }
                )
                response.raise_for_status()
                data = response.json()
                return data.get("choices", [{}])[0].get("message", {}).get("content", "No response")
        except httpx.TimeoutException:
            return "ERROR: Groq timeout"
        except httpx.HTTPStatusError as e:
            return f"ERROR: Groq HTTP {e.response.status_code}"
        except Exception as e:
            return f"ERROR: Groq {str(e)}"
    
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a task with enhanced error handling"""
        self.status = "working"
        self.last_action = datetime.now()
        start_time = datetime.now()
        
        try:
            result = await self._do_task(task)
            
            execution_time = (datetime.now() - start_time).total_seconds()
            
            self.task_history.append({
                "task": task,
                "result": result,
                "timestamp": datetime.now().isoformat(),
                "execution_time": execution_time
            })
            
            # Keep only last 20 tasks in history
            if len(self.task_history) > 20:
                self.task_history = self.task_history[-20:]
            
            self.status = "idle"
            result["execution_time"] = f"{execution_time:.2f}s"
            return result
            
        except Exception as e:
            self.status = "error"
            logger.error(f"[{self.name}] Task failed: {e}")
            return {
                "success": False, 
                "error": str(e),
                "agent": self.name,
                "timestamp": datetime.now().isoformat()
            }
    
    @abstractmethod
    async def _do_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Actual task implementation - override in subclasses"""
        pass
    
    def get_status(self) -> Dict[str, Any]:
        """Get agent status with metrics"""
        return {
            "name": self.name,
            "model": self.model,
            "status": self.status,
            "last_action": self.last_action.isoformat() if self.last_action else None,
            "tasks_completed": len(self.task_history),
            "metrics": self.metrics.to_dict()
        }
    
    def reset_metrics(self):
        """Reset performance metrics"""
        self.metrics = AgentMetrics()
