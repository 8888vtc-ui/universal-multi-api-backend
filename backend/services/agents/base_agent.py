"""
🤖 BASE AGENT CLASS - ULTRA OPTIMIZED VERSION
All agents inherit from this base class.

FEATURES:
- Redis cache for persistent caching
- ALL free-tier AI models as fallbacks
- Gemini, Mistral, Perplexity, Cohere support
- Smart model selection
- Performance metrics
"""
import os
import logging
import httpx
import hashlib
import asyncio
import json
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class RedisCache:
    """Redis-based cache for AI responses (with fallback to in-memory)"""
    
    def __init__(self, ttl_seconds: int = 600):
        self.ttl = ttl_seconds
        self.redis_client = None
        self.memory_cache: Dict[str, tuple] = {}  # Fallback
        self._init_redis()
    
    def _init_redis(self):
        """Initialize Redis connection"""
        try:
            import redis
            redis_url = os.getenv("REDIS_URL", os.getenv("UPSTASH_REDIS_REST_URL"))
            if redis_url:
                self.redis_client = redis.from_url(redis_url, decode_responses=True)
                self.redis_client.ping()
                logger.info("✅ Redis cache connected")
            else:
                logger.info("⚠️ Redis not configured, using in-memory cache")
        except Exception as e:
            logger.warning(f"Redis connection failed, using memory cache: {e}")
            self.redis_client = None
    
    def _hash_key(self, prompt: str, model: str) -> str:
        content = f"{model}:{prompt[:500]}"  # Limit prompt for key
        return f"agent_cache:{hashlib.md5(content.encode()).hexdigest()}"
    
    async def get(self, prompt: str, model: str) -> Optional[str]:
        key = self._hash_key(prompt, model)
        
        # Try Redis first
        if self.redis_client:
            try:
                data = self.redis_client.get(key)
                if data:
                    logger.debug(f"Redis cache HIT for {model}")
                    return data
            except Exception as e:
                logger.warning(f"Redis get error: {e}")
        
        # Fallback to memory
        if key in self.memory_cache:
            response, timestamp = self.memory_cache[key]
            if datetime.now() - timestamp < timedelta(seconds=self.ttl):
                logger.debug(f"Memory cache HIT for {model}")
                return response
            del self.memory_cache[key]
        
        return None
    
    async def set(self, prompt: str, model: str, response: str):
        key = self._hash_key(prompt, model)
        
        # Try Redis first
        if self.redis_client:
            try:
                self.redis_client.setex(key, self.ttl, response)
                return
            except Exception as e:
                logger.warning(f"Redis set error: {e}")
        
        # Fallback to memory
        self.memory_cache[key] = (response, datetime.now())
        if len(self.memory_cache) > 200:
            oldest = min(self.memory_cache, key=lambda k: self.memory_cache[k][1])
            del self.memory_cache[oldest]


class AgentMetrics:
    """Track agent performance metrics"""
    
    def __init__(self):
        self.total_requests = 0
        self.successful_requests = 0
        self.failed_requests = 0
        self.total_response_time = 0.0
        self.cache_hits = 0
        self.fallback_count = 0
        self.models_used: Dict[str, int] = {}
        self.errors_by_type: Dict[str, int] = {}
    
    def record_request(self, success: bool, response_time: float, model_used: str = None, cached: bool = False, error_type: str = None):
        self.total_requests += 1
        if success:
            self.successful_requests += 1
            if model_used:
                self.models_used[model_used] = self.models_used.get(model_used, 0) + 1
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
        return self.total_response_time / max(self.total_requests, 1)
    
    @property
    def success_rate(self) -> float:
        return self.successful_requests / max(self.total_requests, 1) * 100
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "total_requests": self.total_requests,
            "successful": self.successful_requests,
            "failed": self.failed_requests,
            "success_rate": f"{self.success_rate:.1f}%",
            "avg_response_time": f"{self.avg_response_time:.2f}s",
            "cache_hits": self.cache_hits,
            "fallbacks": self.fallback_count,
            "models_used": self.models_used,
            "errors_by_type": self.errors_by_type
        }


# Global Redis cache
_global_cache = RedisCache(ttl_seconds=600)


class BaseAgent(ABC):
    """Base class for all AI agents - ULTRA OPTIMIZED with all free-tier fallbacks"""
    
    # Complete fallback chain using FREE TIER models
    FALLBACK_MODELS = {
        "gpt-4o": ["gpt-4o-mini", "groq", "gemini", "mistral", "deepseek", "cohere", "perplexity"],
        "gpt-4o-mini": ["groq", "gemini", "mistral", "deepseek", "cohere"],
        "claude-3.5-sonnet": ["groq", "gemini", "mistral", "deepseek", "gpt-4o-mini", "cohere"],
        "deepseek-coder": ["groq", "gemini", "mistral", "gpt-4o-mini", "cohere"],
        "groq-llama3": ["gemini", "mistral", "deepseek", "gpt-4o-mini", "cohere"],
        "gemini": ["groq", "mistral", "deepseek", "gpt-4o-mini", "cohere"],
        "mistral": ["groq", "gemini", "deepseek", "gpt-4o-mini", "cohere"],
    }
    
    # Model info for smart selection (speed, cost)
    MODEL_INFO = {
        "groq": {"speed": "ultra-fast", "cost": "free", "quality": "high"},
        "gemini": {"speed": "fast", "cost": "free", "quality": "high"},
        "mistral": {"speed": "fast", "cost": "free", "quality": "high"},
        "deepseek": {"speed": "medium", "cost": "cheap", "quality": "high"},
        "cohere": {"speed": "medium", "cost": "free", "quality": "medium"},
        "perplexity": {"speed": "medium", "cost": "free", "quality": "high"},
        "gpt-4o-mini": {"speed": "fast", "cost": "cheap", "quality": "high"},
        "gpt-4o": {"speed": "medium", "cost": "expensive", "quality": "ultra"},
        "claude-3.5-sonnet": {"speed": "medium", "cost": "expensive", "quality": "ultra"},
    }
    
    MAX_RETRIES = 2
    RETRY_DELAY = 0.5
    
    def __init__(self, name: str, model: str, role: str):
        self.name = name
        self.model = model
        self.role = role
        self.status = "idle"
        self.last_action = None
        self.task_history: List[Dict] = []
        self.metrics = AgentMetrics()
        self.use_cache = True
        
    async def think(self, prompt: str, context: Optional[Dict] = None, use_cache: bool = True) -> str:
        """Use the AI model with smart fallback chain"""
        start_time = datetime.now()
        model_used = self.model
        
        # Check cache
        if use_cache and self.use_cache:
            cached = await _global_cache.get(prompt, self.model)
            if cached:
                self.metrics.record_request(True, 0.01, model_used, cached=True)
                return cached
        
        # Try primary model
        result = await self._call_with_retry(self.model, prompt, context)
        
        # If failed, try all fallbacks in order
        if result.startswith("ERROR:"):
            fallbacks = self.FALLBACK_MODELS.get(self.model, ["groq", "gemini", "mistral"])
            
            for fallback_model in fallbacks:
                self.metrics.record_fallback()
                logger.warning(f"[{self.name}] Trying fallback: {fallback_model}")
                result = await self._call_with_retry(fallback_model, prompt, context)
                if not result.startswith("ERROR:"):
                    model_used = fallback_model
                    break
        
        # Record metrics
        response_time = (datetime.now() - start_time).total_seconds()
        success = not result.startswith("ERROR:")
        self.metrics.record_request(success, response_time, model_used if success else None, 
                                   error_type=result[:50] if not success else None)
        
        # Cache successful responses
        if success and use_cache and self.use_cache:
            await _global_cache.set(prompt, self.model, result)
        
        return result
    
    async def _call_with_retry(self, model: str, prompt: str, context: Optional[Dict] = None) -> str:
        """Call AI model with retry"""
        last_error = None
        
        for attempt in range(self.MAX_RETRIES):
            try:
                result = await self._route_to_provider(model, prompt, context)
                if not result.startswith("ERROR:"):
                    return result
                last_error = result
            except Exception as e:
                last_error = f"ERROR: {str(e)}"
            
            if attempt < self.MAX_RETRIES - 1:
                await asyncio.sleep(self.RETRY_DELAY * (attempt + 1))
        
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
        elif "gemini" in model:
            return await self._call_gemini(prompt, context)
        elif "mistral" in model:
            return await self._call_mistral(prompt, context)
        elif "cohere" in model:
            return await self._call_cohere(prompt, context)
        elif "perplexity" in model:
            return await self._call_perplexity(prompt, context)
        else:
            return await self._call_groq(prompt, context)
    
    async def _call_openai(self, prompt: str, context: Optional[Dict] = None, model: str = "gpt-4o") -> str:
        """Call OpenAI API"""
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
        except Exception as e:
            return f"ERROR: OpenAI {str(e)}"
    
    async def _call_anthropic(self, prompt: str, context: Optional[Dict] = None) -> str:
        """Call Anthropic Claude API"""
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
        except Exception as e:
            return f"ERROR: Anthropic {str(e)}"
    
    async def _call_groq(self, prompt: str, context: Optional[Dict] = None) -> str:
        """Call Groq API (FASTEST - FREE)"""
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
        except Exception as e:
            return f"ERROR: Groq {str(e)}"
    
    async def _call_gemini(self, prompt: str, context: Optional[Dict] = None) -> str:
        """Call Google Gemini API (FREE)"""
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            return "ERROR: Missing Gemini API key"
        
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}",
                    json={
                        "contents": [{
                            "parts": [{"text": f"You are {self.name}. Role: {self.role}\n\n{prompt}"}]
                        }],
                        "generationConfig": {
                            "maxOutputTokens": 4000,
                            "temperature": 0.7
                        }
                    }
                )
                response.raise_for_status()
                data = response.json()
                return data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "No response")
        except Exception as e:
            return f"ERROR: Gemini {str(e)}"
    
    async def _call_mistral(self, prompt: str, context: Optional[Dict] = None) -> str:
        """Call Mistral API (FREE tier)"""
        api_key = os.getenv("MISTRAL_API_KEY")
        if not api_key:
            return "ERROR: Missing Mistral API key"
        
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    "https://api.mistral.ai/v1/chat/completions",
                    headers={"Authorization": f"Bearer {api_key}"},
                    json={
                        "model": "mistral-small-latest",
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
        except Exception as e:
            return f"ERROR: Mistral {str(e)}"
    
    async def _call_deepseek(self, prompt: str, context: Optional[Dict] = None) -> str:
        """Call DeepSeek API"""
        api_key = os.getenv("DEEPSEEK_API_KEY")
        if not api_key:
            return "ERROR: Missing DeepSeek API key"
        
        try:
            async with httpx.AsyncClient(timeout=90.0) as client:
                response = await client.post(
                    "https://api.deepseek.com/v1/chat/completions",
                    headers={"Authorization": f"Bearer {api_key}"},
                    json={
                        "model": "deepseek-chat",
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
        except Exception as e:
            return f"ERROR: DeepSeek {str(e)}"
    
    async def _call_cohere(self, prompt: str, context: Optional[Dict] = None) -> str:
        """Call Cohere API (FREE tier)"""
        api_key = os.getenv("COHERE_API_KEY")
        if not api_key:
            return "ERROR: Missing Cohere API key"
        
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    "https://api.cohere.ai/v1/chat",
                    headers={"Authorization": f"Bearer {api_key}"},
                    json={
                        "model": "command-r",
                        "message": prompt,
                        "preamble": f"You are {self.name}. Role: {self.role}"
                    }
                )
                response.raise_for_status()
                data = response.json()
                return data.get("text", "No response")
        except Exception as e:
            return f"ERROR: Cohere {str(e)}"
    
    async def _call_perplexity(self, prompt: str, context: Optional[Dict] = None) -> str:
        """Call Perplexity API (for web search)"""
        api_key = os.getenv("PERPLEXITY_API_KEY")
        if not api_key:
            return "ERROR: Missing Perplexity API key"
        
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    "https://api.perplexity.ai/chat/completions",
                    headers={"Authorization": f"Bearer {api_key}"},
                    json={
                        "model": "llama-3.1-sonar-small-128k-online",
                        "messages": [
                            {"role": "system", "content": f"You are {self.name}. Role: {self.role}"},
                            {"role": "user", "content": prompt}
                        ]
                    }
                )
                response.raise_for_status()
                data = response.json()
                return data.get("choices", [{}])[0].get("message", {}).get("content", "No response")
        except Exception as e:
            return f"ERROR: Perplexity {str(e)}"
    
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a task"""
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
            
            if len(self.task_history) > 20:
                self.task_history = self.task_history[-20:]
            
            self.status = "idle"
            result["execution_time"] = f"{execution_time:.2f}s"
            return result
            
        except Exception as e:
            self.status = "error"
            logger.error(f"[{self.name}] Task failed: {e}")
            return {"success": False, "error": str(e)}
    
    @abstractmethod
    async def _do_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        pass
    
    def get_status(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "model": self.model,
            "status": self.status,
            "last_action": self.last_action.isoformat() if self.last_action else None,
            "tasks_completed": len(self.task_history),
            "metrics": self.metrics.to_dict()
        }
    
    def reset_metrics(self):
        self.metrics = AgentMetrics()
