"""
Pydantic models for request/response validation
"""
from typing import Optional, List, Literal
from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    """Single chat message"""
    role: Literal["user", "assistant", "system"]
    content: str


class ChatRequest(BaseModel):
    """Chat API request"""
    message: str = Field(..., min_length=1, max_length=2000)
    conversation_history: Optional[List[ChatMessage]] = None
    language: Literal["he", "en"] = "he"
    context: Optional[str] = None


class ChatResponse(BaseModel):
    """Chat API response"""
    response: str
    source: str  # "groq", "ollama", "cache"
    tokens_used: Optional[int] = None
    processing_time_ms: float


class EmbeddingRequest(BaseModel):
    """Embedding creation request"""
    text: str = Field(..., min_length=1, max_length=5000)
    model: Literal["cohere", "openai"] = "cohere"


class EmbeddingResponse(BaseModel):
    """Embedding creation response"""
    embeddings: List[float]
    model: str
    dimensions: int


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    version: str
    ai_providers: dict
    cache_status: str
