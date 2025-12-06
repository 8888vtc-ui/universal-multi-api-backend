"""
Expert Chat Router
Provides specialized chat endpoints for each AI expert with data enrichment
"""
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field
from typing import Optional, List, Literal
import logging
import time

from services.expert_config import get_expert, get_all_experts, Expert, ExpertId
from services.ai_router import ai_router
from services.cache import cache_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/expert", tags=["Expert AI"])


# ============================================
# SCHEMAS
# ============================================

class ExpertChatRequest(BaseModel):
    """Request to chat with an expert"""
    message: str = Field(..., min_length=1, max_length=2000)
    language: Literal["fr", "en", "es", "de"] = "fr"


class ExpertChatResponse(BaseModel):
    """Response from expert chat"""
    expert_id: str
    expert_name: str
    response: str
    # Sources hidden from public response for cleaner UX


class ExpertInfo(BaseModel):
    """Public expert information"""
    id: str
    name: str
    emoji: str
    tagline: str
    description: str
    color: str
    welcome_message: str
    example_questions: List[str]


# ============================================
# DATA ENRICHMENT
# ============================================

async def fetch_context_data(expert: Expert, query: str) -> tuple[str, List[str]]:
    """
    Fetch relevant data from expert's connected APIs
    Returns: (context_string, list_of_sources)
    """
    context_parts = []
    sources = []
    
    # Import API functions dynamically based on expert's data_apis
    for api_name in expert.data_apis[:3]:  # Limit to 3 APIs for speed
        try:
            data = await _fetch_from_api(api_name, query)
            if data:
                context_parts.append(f"[{api_name.upper()}]: {data[:500]}")  # Limit size
                sources.append(api_name)
        except Exception as e:
            logger.warning(f"Failed to fetch from {api_name}: {e}")
    
    context = "\n\n".join(context_parts) if context_parts else "Pas de données supplémentaires disponibles."
    return context, sources


async def _fetch_from_api(api_name: str, query: str) -> Optional[str]:
    """Fetch data from a specific API"""
    import httpx
    
    base_url = "http://localhost:8000/api"  # Internal API call
    
    api_endpoints = {
        "wikipedia": f"{base_url}/wikipedia/search?q={query}&limit=2",
        "weather": f"{base_url}/weather/current?location={query}",
        "countries": f"{base_url}/countries/search?q={query}",
        "finance": f"{base_url}/finance/crypto/{query.lower()}",
        "coincap": f"{base_url}/coincap/assets?search={query}",
        \"sports\": f\"{base_url}/sports/news?q={query}\",
        \"news\": f\"{base_url}/news/search?q={query}&limit=3\",
        \"nutrition\": f\"{base_url}/nutrition/search?q={query}\",
        \"medical\": f\"{base_url}/medical/search?q={query}\",
        \"books\": f\"{base_url}/books/search?q={query}&limit=2\",
        \"trivia\": f\"{base_url}/trivia/random\",
        \"geocoding\": f\"{base_url}/geocoding/search?q={query}\",
        \"jokes\": f\"{base_url}/jokes/random\",
        \"quotes\": f\"{base_url}/quotes/random\",
        \"omdb\": f\"{base_url}/omdb/search?query={query}\",
        \"github\": f\"{base_url}/github/search/repos?q={query}\",
        # New endpoints
        \"exchange\": f\"{base_url}/exchange/rates\",
        \"numbers\": f\"{base_url}/numbers/random\",
        \"animals\": f\"{base_url}/animals/random\",
        \"countries\": f\"{base_url}/countries/search?q={query}\",
        \"history\": f\"{base_url}/history/today\",
        \"nameanalysis\": f\"{base_url}/nameanalysis/analyze?name={query}\",
    }
    
    endpoint = api_endpoints.get(api_name)
    if not endpoint:
        return None
    
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(endpoint)
            if response.status_code == 200:
                data = response.json()
                # Extract relevant text from response
                return _extract_summary(data)
    except Exception as e:
        logger.debug(f"API {api_name} fetch failed: {e}")
    
    return None


def _extract_summary(data: dict) -> str:
    """Extract a readable summary from API response"""
    if isinstance(data, str):
        return data[:500]
    
    if isinstance(data, list):
        items = []
        for item in data[:3]:
            if isinstance(item, dict):
                # Try common keys
                for key in ['title', 'name', 'summary', 'description', 'content', 'text']:
                    if key in item:
                        items.append(str(item[key])[:200])
                        break
        return " | ".join(items)
    
    if isinstance(data, dict):
        # Try to extract useful info
        summary_parts = []
        for key in ['summary', 'description', 'content', 'title', 'name', 'data', 'result']:
            if key in data:
                val = data[key]
                if isinstance(val, str):
                    summary_parts.append(val[:300])
                elif isinstance(val, dict):
                    summary_parts.append(str(val)[:300])
        return " | ".join(summary_parts[:3]) if summary_parts else str(data)[:500]
    
    return str(data)[:500]


# ============================================
# ENDPOINTS
# ============================================

@router.get("/list", response_model=List[ExpertInfo])
async def list_experts():
    """
    📋 Get list of all available AI experts
    """
    experts = get_all_experts()
    return [
        ExpertInfo(
            id=e.id.value,
            name=e.name,
            emoji=e.emoji,
            tagline=e.tagline,
            description=e.description,
            color=e.color,
            welcome_message=e.welcome_message,
            example_questions=e.example_questions
        )
        for e in experts
    ]


@router.get("/{expert_id}", response_model=ExpertInfo)
async def get_expert_info(expert_id: str):
    """
    ℹ️ Get information about a specific expert
    """
    expert = get_expert(expert_id)
    if not expert:
        raise HTTPException(status_code=404, detail=f"Expert '{expert_id}' not found")
    
    return ExpertInfo(
        id=expert.id.value,
        name=expert.name,
        emoji=expert.emoji,
        tagline=expert.tagline,
        description=expert.description,
        color=expert.color,
        welcome_message=expert.welcome_message,
        example_questions=expert.example_questions
    )


@router.post("/{expert_id}/chat", response_model=ExpertChatResponse)
async def chat_with_expert(expert_id: str, body: ExpertChatRequest):
    """
    💬 Chat with a specialized AI expert
    
    The expert will:
    1. Fetch relevant data from its connected APIs
    2. Use its specialized personality and knowledge
    3. Provide contextual, domain-specific responses
    """
    start_time = time.time()
    
    # Get expert config
    expert = get_expert(expert_id)
    if not expert:
        raise HTTPException(status_code=404, detail=f"Expert '{expert_id}' not found")
    
    # Check cache first
    cache_key = f"expert:{expert_id}:{body.message}"
    cached = cache_service.get("expert_chat", cache_key)
    if cached:
        return ExpertChatResponse(
            expert_id=expert_id,
            expert_name=expert.name,
            response=cached["response"],
            sources=cached.get("sources", []),
            source="cache",
            processing_time_ms=(time.time() - start_time) * 1000
        )
    
    # Fetch context data from expert's APIs
    context, sources = await fetch_context_data(expert, body.message)
    
    # Build system prompt with context
    system_prompt = expert.system_prompt.replace("{context}", context)
    
    # Add language instruction if not French
    if body.language != "fr":
        language_names = {"en": "English", "es": "Spanish", "de": "German"}
        system_prompt += f"\n\nIMPORTANT: Respond in {language_names.get(body.language, 'English')}."
    
    # Route to AI
    try:
        result = await ai_router.route(
            prompt=body.message,
            system_prompt=system_prompt
        )
    except Exception as e:
        logger.error(f"Expert chat error: {e}")
        raise HTTPException(status_code=503, detail="AI service temporarily unavailable")
    
    # Cache the response
    cache_service.set(
        "expert_chat",
        cache_key,
        {"response": result["response"], "sources": sources},
        ttl=1800  # 30 minutes
    )
    
    return ExpertChatResponse(
        expert_id=expert_id,
        expert_name=expert.name,
        response=result["response"]
    )
