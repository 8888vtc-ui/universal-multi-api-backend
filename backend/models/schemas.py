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


class WidgetData(BaseModel):
    """Data structure for UI widgets"""
    type: Literal["chart", "news_list", "weather_card", "crypto_card", "stats_card"]
    title: Optional[str] = None
    data: dict  # Flexible data payload for the specific widget


class ChatResponse(BaseModel):
    """Chat API response"""
    response: str
    source: str  # "groq", "ollama", "cache"
    tokens_used: Optional[int] = None
    processing_time_ms: float
    widgets: Optional[List[WidgetData]] = None  # UI Widgets support


class ExpertChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    language: Optional[str] = None


class ExpertChatResponse(BaseModel):
    expert_id: str
    expert_name: str
    response: str
    session_id: str
    sources: List[str]
    source: str
    processing_time_ms: float
    widgets: Optional[List[WidgetData]] = None  # UI Widgets support


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
