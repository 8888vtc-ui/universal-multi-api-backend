
"""
AI Providers Implementation
Separated from ai_router.py for better maintainability.
"""
import os
from typing import Optional
from groq import Groq
import httpx
from services.cache import cache_service
from services.circuit_breaker import circuit_breaker

try:
    from services.retry_handler import with_retry
except ImportError:
    # Fallback si retry_handler n'existe pas
    def with_retry(func):
        return func

class AIProvider:
    """Base AI provider class"""
    
    def __init__(self, name: str, priority: int, daily_quota: int = 0):
        self.name = name
        self.priority = priority
        self.daily_quota = daily_quota  # 0 = unlimited
        self.available = False
        self.last_error = None
    
    @property
    def requests_today(self) -> int:
        """Get current requests count from Redis"""
        return cache_service.get_quota_usage(self.name)
        
    def increment_usage(self):
        """Increment usage count in Redis"""
        cache_service.increment_quota_usage(self.name)
    
    def can_handle_request(self) -> bool:
        """Check if provider can handle another request"""
        return cache_service.check_quota_available(self.name, self.daily_quota)
    
    async def call(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Call AI provider - to be implemented by subclasses"""
        raise NotImplementedError

    async def stream(self, prompt: str, system_prompt: Optional[str] = None):
        """Stream AI response - to be implemented by subclasses
        Yields: str (chunks of response)
        """
        # Default fallback to non-streaming if not implemented
        response = await self.call(prompt, system_prompt)
        yield response


class GroqProvider(AIProvider):
    """Groq AI provider (Llama 3.1) - 30 req/min, ~14,400/day"""
    
    def __init__(self):
        super().__init__("groq", priority=1, daily_quota=14000)
        api_key = os.getenv("GROQ_API_KEY")
        
        if api_key and api_key != "your_groq_api_key_here":
            try:
                self.client = Groq(api_key=api_key)
                self.available = True
                print("[OK] Groq provider initialized (14k req/day)")
            except Exception as e:
                print(f"[WARN]  Groq initialization failed: {e}")
                self.available = False
        else:
            print("[WARN]  Groq API key not configured")
            self.available = False
    
    @circuit_breaker(name="groq")
    @with_retry()
    async def call(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Call Groq API"""
        try:
            messages = []
            
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            
            messages.append({"role": "user", "content": prompt})
            
            completion = self.client.chat.completions.create(
                messages=messages,
                model="llama-3.3-70b-versatile",
                temperature=0.7,
                max_tokens=1024,
            )
            
            self.increment_usage()
            return completion.choices[0].message.content
        
        except Exception as e:
            self.last_error = str(e)
            raise Exception(f"Groq API error: {e}")

    async def stream(self, prompt: str, system_prompt: Optional[str] = None):
        """Stream Groq API response"""
        try:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            
            messages.append({"role": "user", "content": prompt})
            
            stream = self.client.chat.completions.create(
                messages=messages,
                model="llama-3.3-70b-versatile",
                temperature=0.7,
                max_tokens=1024,
                stream=True
            )
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    yield chunk.choices[0].delta.content
            
            self.increment_usage()
        
        except Exception as e:
            self.last_error = str(e)
            raise Exception(f"Groq streaming error: {e}")


class MistralProvider(AIProvider):
    """Mistral AI provider - 1B tokens/month"""
    
    def __init__(self):
        super().__init__("mistral", priority=2, daily_quota=100000)
        api_key = os.getenv("MISTRAL_API_KEY")
        
        if api_key and api_key != "your_mistral_api_key_here":
            try:
                self.api_key = api_key
                self.available = True
                print("[OK] Mistral provider initialized (1B tokens/month)")
            except Exception as e:
                print(f"[WARN]  Mistral initialization failed: {e}")
                self.available = False
        else:
            print("[WARN]  Mistral API key not configured")
            self.available = False
    
    @circuit_breaker(name="mistral")
    @with_retry()
    async def call(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Call Mistral API"""
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                messages = []
                if system_prompt:
                    messages.append({"role": "system", "content": system_prompt})
                messages.append({"role": "user", "content": prompt})
                
                response = await client.post(
                    "https://api.mistral.ai/v1/chat/completions",
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    json={
                        "model": "mistral-small-latest",
                        "messages": messages,
                        "temperature": 0.7,
                        "max_tokens": 1024
                    }
                )
                
                if response.status_code == 200:
                    self.increment_usage()
                    return response.json()["choices"][0]["message"]["content"]
                else:
                    raise Exception(f"Mistral returned status {response.status_code}")
        
        except Exception as e:
            self.last_error = str(e)
            raise Exception(f"Mistral API error: {e}")


class GeminiProvider(AIProvider):
    """Google Gemini provider - 1,500 req/day"""
    
    def __init__(self):
        super().__init__("gemini", priority=6, daily_quota=1500)
        api_key = os.getenv("GEMINI_API_KEY")
        
        if api_key and api_key != "your_gemini_api_key_here":
            try:
                self.api_key = api_key
                self.available = True
                print("[OK] Gemini provider initialized (1,500 req/day)")
            except Exception as e:
                print(f"[WARN]  Gemini initialization failed: {e}")
                self.available = False
        else:
            print("[WARN]  Gemini API key not configured")
            self.available = False
    
    @circuit_breaker(name="gemini")
    @with_retry()
    async def call(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Call Gemini API"""
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
                
                response = await client.post(
                    f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.api_key}",
                    json={
                        "contents": [{"parts": [{"text": full_prompt}]}],
                        "generationConfig": {
                            "temperature": 0.7,
                            "maxOutputTokens": 1024
                        }
                    }
                )
                
                if response.status_code == 200:
                    self.increment_usage()
                    return response.json()["candidates"][0]["content"]["parts"][0]["text"]
                else:
                    raise Exception(f"Gemini returned status {response.status_code}")
        
        except Exception as e:
            self.last_error = str(e)
            raise Exception(f"Gemini API error: {e}")


class CohereChatProvider(AIProvider):
    """Cohere Chat provider - 100 req/day free"""
    
    def __init__(self):
        super().__init__("cohere_chat", priority=4, daily_quota=100)
        api_key = os.getenv("COHERE_API_KEY")
        
        if api_key and api_key != "your_cohere_api_key_here":
            self.api_key = api_key
            self.available = True
            print("[OK] Cohere Chat provider initialized (100 req/day)")
        else:
            self.available = False
            print("[WARN]  Cohere Chat API key not configured")
    
    @circuit_breaker(name="cohere_chat")
    @with_retry()
    async def call(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Call Cohere Chat API"""
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                if system_prompt:
                    full_prompt = f"{system_prompt}\n\n{prompt}"
                else:
                    full_prompt = prompt
                
                response = await client.post(
                    "https://api.cohere.ai/v1/chat",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "message": full_prompt,
                        "model": "command-r-plus",
                        "temperature": 0.7,
                        "max_tokens": 1024
                    }
                )
                
                if response.status_code == 200:
                    self.increment_usage()
                    return response.json()["text"]
                else:
                    raise Exception(f"Cohere returned status {response.status_code}: {response.text}")
        
        except Exception as e:
            self.last_error = str(e)
            raise Exception(f"Cohere Chat API error: {e}")


class AI21Provider(AIProvider):
    """AI21 Labs provider - 1,000 req/day free"""
    
    def __init__(self):
        super().__init__("ai21", priority=5, daily_quota=1000)
        api_key = os.getenv("AI21_API_KEY")
        
        if api_key and api_key != "your_ai21_api_key_here":
            self.api_key = api_key
            self.available = True
            print("[OK] AI21 Labs provider initialized (1,000 req/day)")
        else:
            self.available = False
            print("[WARN]  AI21 Labs API key not configured")
    
    @circuit_breaker(name="ai21")
    @with_retry()
    async def call(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Call AI21 Labs API"""
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                full_prompt = prompt
                if system_prompt:
                    full_prompt = f"{system_prompt}\n\n{prompt}"
                
                response = await client.post(
                    "https://api.ai21.com/studio/v1/j2-ultra/complete",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "prompt": full_prompt,
                        "temperature": 0.7,
                        "maxTokens": 1024,
                        "topP": 0.9
                    }
                )
                
                if response.status_code == 200:
                    self.increment_usage()
                    result = response.json()
                    return result["completions"][0]["data"]["text"]
                else:
                    raise Exception(f"AI21 returned status {response.status_code}: {response.text}")
        
        except Exception as e:
            self.last_error = str(e)
            raise Exception(f"AI21 Labs API error: {e}")


class OpenRouterProvider(AIProvider):
    """OpenRouter provider (DeepSeek + 67 models) - 50 req/day free"""
    
    def __init__(self):
        super().__init__("openrouter", priority=9, daily_quota=50)
        api_key = os.getenv("OPENROUTER_API_KEY")
        
        if api_key and api_key.startswith("sk-or-"):
            try:
                self.api_key = api_key
                self.available = True
                print("[OK] OpenRouter provider initialized (50 req/day, DeepSeek + 67 models)")
            except Exception as e:
                print(f"[WARN]  OpenRouter initialization failed: {e}")
                self.available = False
        else:
            print("[WARN]  OpenRouter API key not configured")
            self.available = False
    
    @circuit_breaker(name="openrouter")
    @with_retry()
    async def call(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Call OpenRouter API"""
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                messages = []
                if system_prompt:
                    messages.append({"role": "system", "content": system_prompt})
                messages.append({"role": "user", "content": prompt})
                
                response = await client.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "HTTP-Referer": "https://travelguide-ai.com",
                        "X-Title": "TravelGuide AI"
                    },
                    json={
                        "model": "deepseek/deepseek-chat",
                        "messages": messages,
                        "temperature": 0.7,
                        "max_tokens": 1024
                    }
                )
                
                if response.status_code == 200:
                    self.increment_usage()
                    return response.json()["choices"][0]["message"]["content"]
                else:
                    raise Exception(f"OpenRouter returned status {response.status_code}")
        
        except Exception as e:
            self.last_error = str(e)
            raise Exception(f"OpenRouter API error: {e}")


class AnthropicProvider(AIProvider):
    """Anthropic Claude provider - 5$ crédit gratuit"""
    
    def __init__(self):
        super().__init__("anthropic", priority=3, daily_quota=1000)
        api_key = os.getenv("ANTHROPIC_API_KEY")
        
        if api_key and api_key != "your_anthropic_api_key_here":
            self.api_key = api_key
            self.available = True
            print("[OK] Anthropic Claude provider initialized (5$ crédit gratuit)")
        else:
            self.available = False
            print("[WARN]  Anthropic API key not configured")
    
    @circuit_breaker(name="anthropic")
    @with_retry()
    async def call(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Call Anthropic Claude API"""
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                messages = []
                if system_prompt:
                    messages.append({"role": "system", "content": system_prompt})
                messages.append({"role": "user", "content": prompt})
                
                model = os.getenv("ANTHROPIC_MODEL", "claude-3-haiku-20240307")
                
                response = await client.post(
                    "https://api.anthropic.com/v1/messages",
                    headers={
                        "x-api-key": self.api_key,
                        "anthropic-version": "2023-06-01",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": model,
                        "max_tokens": 1024,
                        "messages": messages
                    }
                )
                
                if response.status_code == 200:
                    self.increment_usage()
                    return response.json()["content"][0]["text"]
                else:
                    raise Exception(f"Anthropic returned status {response.status_code}: {response.text}")
        
        except Exception as e:
            self.last_error = str(e)
            raise Exception(f"Anthropic API error: {e}")


class PerplexityProvider(AIProvider):
    """Perplexity AI provider - 5 req/day free (with web search)"""
    
    def __init__(self):
        super().__init__("perplexity", priority=7, daily_quota=5)
        api_key = os.getenv("PERPLEXITY_API_KEY")
        
        if api_key and api_key != "your_perplexity_api_key_here":
            self.api_key = api_key
            self.available = True
            print("[OK] Perplexity AI provider initialized (5 req/day, with web search)")
        else:
            self.available = False
            print("[WARN]  Perplexity API key not configured")
    
    @circuit_breaker(name="perplexity")
    @with_retry()
    async def call(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Call Perplexity AI API (with web search)"""
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                messages = []
                if system_prompt:
                    messages.append({"role": "system", "content": system_prompt})
                messages.append({"role": "user", "content": prompt})
                
                response = await client.post(
                    "https://api.perplexity.ai/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "sonar",
                        "messages": messages,
                        "temperature": 0.7,
                        "max_tokens": 1024
                    }
                )
                
                if response.status_code == 200:
                    self.increment_usage()
                    return response.json()["choices"][0]["message"]["content"]
                else:
                    raise Exception(f"Perplexity returned status {response.status_code}: {response.text}")
        
        except Exception as e:
            self.last_error = str(e)
            raise Exception(f"Perplexity API error: {e}")


class HuggingFaceProvider(AIProvider):
    """Hugging Face provider - Unlimited (rate limit ~30 req/min)"""
    
    def __init__(self):
        super().__init__("huggingface", priority=8, daily_quota=0)
        api_token = os.getenv("HUGGINGFACE_API_TOKEN")
        
        if api_token and api_token != "your_huggingface_token_here":
            self.api_token = api_token
            self.available = True
            self.default_model = os.getenv("HUGGINGFACE_MODEL", "meta-llama/Llama-3-8B-Instruct")
            print(f"[OK] Hugging Face provider initialized (unlimited, rate limit ~30 req/min, model: {self.default_model})")
        else:
            self.available = False
            print("[WARN]  Hugging Face API token not configured")
    
    @circuit_breaker(name="huggingface")
    @with_retry()
    async def call(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Call Hugging Face Inference API"""
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                if system_prompt:
                    full_prompt = f"{system_prompt}\n\n{prompt}"
                else:
                    full_prompt = prompt
                
                response = await client.post(
                    f"https://api-inference.huggingface.co/models/{self.default_model}",
                    headers={
                        "Authorization": f"Bearer {self.api_token}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "inputs": full_prompt,
                        "parameters": {
                            "temperature": 0.7,
                            "max_new_tokens": 1024,
                            "return_full_text": False
                        }
                    }
                )
                
                if response.status_code == 200:
                    self.increment_usage()
                    result = response.json()
                    if isinstance(result, list) and len(result) > 0:
                        return result[0].get("generated_text", "")
                    elif isinstance(result, dict):
                        return result.get("generated_text", "")
                    else:
                        return str(result)
                elif response.status_code == 503:
                    error_msg = response.json().get("error", "Model is loading")
                    raise Exception(f"Hugging Face model loading: {error_msg}")
                else:
                    raise Exception(f"Hugging Face returned status {response.status_code}: {response.text}")
        
        except Exception as e:
            self.last_error = str(e)
            raise Exception(f"Hugging Face API error: {e}")


class OllamaProvider(AIProvider):
    """Ollama local provider (unlimited fallback)"""
    
    def __init__(self):
        super().__init__("ollama", priority=10, daily_quota=0)
        self.base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        
        try:
            response = httpx.get(f"{self.base_url}/api/tags", timeout=2)
            if response.status_code == 200:
                self.available = True
                print("[OK] Ollama provider initialized (unlimited local)")
            else:
                self.available = False
                print("[WARN]  Ollama not responding")
        except Exception as e:
            self.available = False
            print(f"[WARN]  Ollama not available: {e}")
    
    @circuit_breaker(name="ollama")
    async def call(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Call Ollama API"""
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                payload = {
                    "model": "llama3.1",
                    "prompt": prompt,
                    "stream": False
                }
                
                if system_prompt:
                    payload["system"] = system_prompt
                
                response = await client.post(
                    f"{self.base_url}/api/generate",
                    json=payload
                )
                
                if response.status_code == 200:
                    self.increment_usage()
                    return response.json()["response"]
                else:
                    raise Exception(f"Ollama returned status {response.status_code}")
        
        except Exception as e:
            self.last_error = str(e)
            raise Exception(f"Ollama API error: {e}")

                print("[WARN]  Ollama not responding")
        except Exception as e:
            self.available = False
            print(f"[WARN]  Ollama not available: {e}")
    
    @circuit_breaker(name="ollama")
    async def call(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Call Ollama API"""
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                payload = {
                    "model": "llama3.1",
                    "prompt": prompt,
                    "stream": False
                }
                
                if system_prompt:
                    payload["system"] = system_prompt
                
                response = await client.post(
                    f"{self.base_url}/api/generate",
                    json=payload
                )
                
                if response.status_code == 200:
                    self.increment_usage()
                    return response.json()["response"]
                else:
                    raise Exception(f"Ollama returned status {response.status_code}")
        
        except Exception as e:
            self.last_error = str(e)
            raise Exception(f"Ollama API error: {e}")
