"""
Chat endpoint with AI integration and caching
"""
from fastapi import APIRouter, HTTPException, Request
from models.schemas import ChatRequest, ChatResponse
from services.ai_router import ai_router
from services.cache import cache_service
from services.rate_limiter import get_limiter
from services.sanitizer import sanitize
import logging
import os
import time

limiter = get_limiter()
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["chat"])


# System prompts by language
SYSTEM_PROMPTS = {
    "he": """אתה מדריך תיירות מומחה לתיירים ישראלים. 
אתה מספק עצות בטיחות, המלצות כשרות, ומידע מותאם לצרכים של תיירים ישראלים.
תמיד תשיב בעברית אלא אם כן התבקשת אחרת.
היה ידידותי, מועיל ומדויק.""",
    
    "en": """You are an expert travel guide for Israeli tourists.
You provide safety advice, kosher recommendations, and information tailored to Israeli travelers' needs.
Always respond in English unless asked otherwise.
Be friendly, helpful, and accurate."""
}


@router.post("/chat", response_model=ChatResponse)
async def chat(request: Request, body: ChatRequest):
    """
    Chat with AI assistant
    
    - **message**: User message (required)
    - **language**: Response language (he/en)
    - **context**: Optional context for the conversation
    """
    try:
        start_time = time.time()
        
        # Sanitize input
        body.message = sanitize(body.message, max_length=5000)
        if body.context:
            body.context = sanitize(body.context, max_length=2000)
        
        # Vérifier que des providers IA sont disponibles
        if not ai_router.available_providers:
            raise HTTPException(
                status_code=503,
                detail="AI service unavailable. No AI providers configured. Please set at least one API key (GROQ_API_KEY, MISTRAL_API_KEY, etc.) or install Ollama locally."
            )
        
        # Check cache first
        cache_key = f"{body.message}:{body.language}"
        cached = cache_service.get("chat", cache_key)
        
        if cached:
            return ChatResponse(
                response=cached["response"],
                source="cache",
                processing_time_ms=(time.time() - start_time) * 1000
            )
        
        # Build system prompt
        system_prompt = SYSTEM_PROMPTS.get(body.language, SYSTEM_PROMPTS["he"])
        
        if body.context:
            system_prompt += f"\n\nContext: {body.context}"
        
        # Route to AI
        result = await ai_router.route(
            prompt=body.message,
            system_prompt=system_prompt
        )
        
        # Cache the response
        cache_ttl = int(os.getenv("CACHE_TTL_CHAT", 3600))
        cache_service.set(
            "chat",
            cache_key,
            {"response": result["response"]},
            ttl=cache_ttl
        )
        
        return ChatResponse(
            response=result["response"],
            source=result["source"],
            processing_time_ms=result["processing_time_ms"]
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Chat error: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Chat service temporarily unavailable. Please try again later."
        )
