"""
Expert Chat Router
Provides specialized chat endpoints for each AI expert with data enrichment
"""
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from typing import Optional, List, Literal
import logging
import time
import asyncio

from services.expert_config import (
    get_expert, get_all_experts, Expert, ExpertId,
    get_all_categories, get_experts_grouped_by_category, get_experts_by_category, Category
)
from services.ai_router import ai_router
from services.cache import cache_service
from services.context_helpers import get_current_datetime_context, detect_language, get_language_instruction

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/expert", tags=["Expert AI"])


# ============================================
# SCHEMAS
# ============================================

class ExpertChatRequest(BaseModel):
    """Request to chat with an expert"""
    message: str = Field(..., min_length=1, max_length=2000)
    language: Optional[str] = None  # Auto-detect if not provided
    session_id: Optional[str] = None  # ID de session pour la mémoire conversationnelle


class ExpertChatResponse(BaseModel):
    """Response from expert chat"""
    expert_id: str
    expert_name: str
    response: str
    session_id: Optional[str] = None  # ID de session pour maintenir la conversation
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
    Fetch relevant data from expert's connected APIs (parallélisé pour performance)
    Uses intelligent query detection to skip APIs if not needed.
    Returns: (context_string, list_of_sources)
    """
    from services.intent_detector import IntentDetector, get_search_mode
    
    # 1. Detect Intent: Should we even call APIs?
    intent = IntentDetector.detect_intent(query, expert.id.value)
    
    if intent == "chat_only":
        logger.info(f"Skipping API calls for chat-only query: '{query}' ({expert.id.value})")
        return "Contexte: Conversation simple, pas de données externes nécessaires.", []
    
    # 2. For HEALTH expert: Check if DEEP search is needed
    if expert.id.value == "health":
        search_mode = get_search_mode(query, expert.id.value)
        logger.info(f"Health expert search mode: {search_mode}")
        
        if search_mode == "deep":
            # Use DEEP medical search - comprehensive search across ALL APIs
            try:
                from services.deep_medical_search import perform_deep_search
                logger.info(f"Starting DEEP medical search for: {query}")
                
                context, search_result = await perform_deep_search(query)
                
                # Build sources from the search
                sources = [f"[{api.upper()}]" for api in search_result.apis_with_data]
                
                logger.info(
                    f"DEEP search completed: {len(search_result.apis_searched)} APIs, "
                    f"{len(search_result.apis_with_data)} with data, "
                    f"{search_result.total_time_ms:.0f}ms"
                )
                
                return context, sources
                
            except Exception as e:
                logger.error(f"Deep search failed, falling back to standard: {e}")
                # Fall through to standard search
    
    # 3. For FINANCE expert, use intelligent detection
    if expert.id.value == "finance":
        from services.finance_query_detector import FinanceQueryDetector
        
        # Détecter le type de requête
        detection = FinanceQueryDetector.detect_query_type(query)
        query_type = detection["type"]
        symbol = detection.get("symbol")
        coin_id = detection.get("coin_id")
        
        # Obtenir les APIs recommandées selon le type
        recommended_apis = FinanceQueryDetector.get_recommended_apis(
            query_type, symbol, coin_id
        )
        
        # Utiliser les APIs recommandées si disponibles, sinon fallback sur expert.data_apis
        api_names = recommended_apis if recommended_apis else expert.data_apis[:3]
        
        # Préparer les paramètres pour les appels API
        query_params = {
            "query": query,
            "symbol": symbol,
            "coin_id": coin_id,
            "query_type": query_type
        }
    else:
        # Pour les autres experts, utiliser la méthode standard
        api_names = expert.data_apis[:3]
        query_params = {"query": query}
    
    if not api_names:
        return "Pas de données supplémentaires disponibles.", []
    
    # Appeler toutes les APIs en parallèle pour améliorer les performances
    try:
        tasks = [_fetch_from_api(api_name, query, query_params) for api_name in api_names]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        context_parts = []
        sources = []
        
        for api_name, result in zip(api_names, results):
            if isinstance(result, Exception):
                logger.debug(f"API {api_name} failed: {type(result).__name__}: {result}")
                continue
            
            if result:
                context_parts.append(f"[{api_name.upper()}]: {result[:500]}")  # Limit size
                sources.append(api_name)
                
    except Exception as e:
        logger.error(f"Error fetching context data: {e}")
        # En cas d'erreur de contexte, on continue sans contexte plutôt que de planter
        context_parts = []
        sources = []
    
    # Pour l'expert financier, ajouter des informations contextuelles même si les APIs échouent
    if expert.id.value == "finance" and not context_parts:
        # Ajouter des informations basées sur la détection
        detection_info = []
        if query_params.get("query_type") == "stock" and query_params.get("symbol"):
            symbol = query_params.get("symbol")
            detection_info.append(f"L'utilisateur demande des informations sur {symbol} (indice/ETF).")
        elif query_params.get("query_type") == "market":
            detection_info.append("L'utilisateur demande des informations sur les marchés financiers en général.")
        
        if detection_info:
            context_parts.append("[CONTEXTE]: " + " ".join(detection_info))
    
    context = "\n\n".join(context_parts) if context_parts else "Pas de données supplémentaires disponibles."
    return context, sources



async def _fetch_from_api(api_name: str, query: str, query_params: Optional[dict] = None) -> Optional[str]:
    """
    Fetch data from a specific API with retry and improved error handling
    """
    import httpx
    import os
    from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
    
    # Use environment variable or localhost + detected port for local dev
    port = os.getenv("PORT", "8000")
    default_url = f"http://localhost:{port}"
    base_url = os.getenv("APP_URL", default_url) + "/api"
    
    # Utiliser les paramètres de requête si disponibles (pour finance expert)
    symbol = query_params.get("symbol") if query_params else None
    coin_id = query_params.get("coin_id") if query_params else None
    query_type = query_params.get("query_type") if query_params else None
    
    # Construire les endpoints avec les bons paramètres
    api_endpoints = {
        "wikipedia": f"{base_url}/wikipedia/search?q={query}&limit=2",
        "weather": f"{base_url}/weather/current?location={query}",
        "countries": f"{base_url}/countries/search?q={query}",
        "finance": f"{base_url}/finance/crypto/{coin_id or query.lower()}",
        "coincap": f"{base_url}/coincap/assets?search={coin_id or query}",
        "sports": f"{base_url}/sports/news?q={query}",
        "news": f"{base_url}/news/search?q={query}&limit=3",
        "nutrition": f"{base_url}/nutrition/search?q={query}",
        "medical": f"{base_url}/medical/search?q={query}",
        "books": f"{base_url}/books/search?q={query}&limit=2",
        "trivia": f"{base_url}/trivia/random",
        "geocoding": f"{base_url}/geocoding/search?q={query}",
        "jokes": f"{base_url}/jokes/random",
        "quotes": f"{base_url}/quotes/random",
        "omdb": f"{base_url}/omdb/search?query={query}",
        "github": f"{base_url}/github/search/repos?q={query}",
        # New endpoints
        "exchange": f"{base_url}/exchange/rates",
        "numbers": f"{base_url}/numbers/random",
        "animals": f"{base_url}/animals/random",
        "history": f"{base_url}/history/today",
        "nameanalysis": f"{base_url}/nameanalysis/analyze?name={query}",
        # Finance endpoints (new) - utiliser symbol si disponible
        "finance_stock": f"{base_url}/finance/stock/quote/{symbol or query.upper()}",
        "finance_company": f"{base_url}/finance/stock/company/{symbol or query.upper()}",
        "finance_news": f"{base_url}/finance/stock/news/{symbol or query.upper()}?limit=5",
        "finance_market_news": f"{base_url}/finance/market/news?limit=5",
    }
    
    endpoint = api_endpoints.get(api_name)
    if not endpoint:
        logger.debug(f"API endpoint not found for {api_name}")
        return None
    
    # Retry avec backoff exponentiel pour les erreurs réseau
    @retry(
        stop=stop_after_attempt(2),  # 2 tentatives max (1 initiale + 1 retry)
        wait=wait_exponential(multiplier=0.5, min=0.5, max=2.0),
        retry=retry_if_exception_type((httpx.RequestError, httpx.HTTPStatusError)),
        reraise=True
    )
    async def _fetch_with_retry():
        """Fetch avec retry automatique"""
        timeout = httpx.Timeout(3.0, connect=2.0)  # Timeout plus court pour éviter les blocages
        async with httpx.AsyncClient(timeout=timeout) as client:
            try:
                response = await client.get(endpoint)
                response.raise_for_status()  # Lève une exception pour les codes d'erreur HTTP
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Handle error responses gracefully
                    if isinstance(data, dict):
                        if data.get("success") is False:
                            # API returned an error but with 200 status
                            logger.debug(f"API {api_name} returned error: {data.get('error', 'Unknown error')}")
                            return None
                    
                    # Special handling for finance APIs - extract data clearly
                    if api_name in ["finance", "coincap"]:
                        return _extract_crypto_summary(data, query)
                    elif api_name in ["finance_stock", "finance_company"]:
                        return _extract_stock_summary(data, api_name)
                    elif api_name in ["finance_news", "finance_market_news"]:
                        return _extract_news_summary(data)
                    # Extract relevant text from response
                    return _extract_summary(data)
                return None
            except httpx.TimeoutException as e:
                logger.warning(f"API {api_name} timeout after {timeout.read}s: {e}")
                raise  # Relancer pour le retry
            except httpx.HTTPStatusError as e:
                # Ne pas retry pour les erreurs 4xx (client errors)
                if 400 <= e.response.status_code < 500:
                    logger.debug(f"API {api_name} client error {e.response.status_code}: {e}")
                    return None
                # Retry pour les erreurs 5xx (server errors)
                logger.warning(f"API {api_name} server error {e.response.status_code}: {e}")
                raise
            except httpx.RequestError as e:
                logger.warning(f"API {api_name} request error (connection failed): {e}")
                raise  # Relancer pour le retry
            except Exception as e:
                # Autres erreurs (JSON decode, etc.) - ne pas retry
                logger.error(f"API {api_name} unexpected error: {type(e).__name__}: {e}")
                return None
    
    try:
        return await _fetch_with_retry()
    except (httpx.RequestError, httpx.HTTPStatusError) as e:
        # Échec après tous les retries
        logger.error(f"API {api_name} failed completely after retries: {type(e).__name__}: {e}")
        return None
    except Exception as e:
        # Erreur inattendue - logger avec stack trace pour debugging
        logger.error(
            f"API {api_name} critical error: {type(e).__name__}: {e}",
            exc_info=True  # Inclure la stack trace complète
        )
        return None


def _extract_crypto_summary(data: dict, query: str) -> str:
    """Extract crypto price data in a clear format"""
    try:
        if isinstance(data, list) and len(data) > 0:
            # CoinCap format
            coin = data[0]
            name = coin.get("name", query)
            symbol = coin.get("symbol", "")
            price = coin.get("priceUsd", "N/A")
            change24h = coin.get("changePercent24Hr", "N/A")
            
            # Format price nicely
            try:
                price_float = float(price)
                price_str = f"${price_float:,.2f}"
            except (ValueError, TypeError) as e:
                logger.debug(f"Could not format price '{price}': {e}")
                price_str = price
                
            try:
                change_float = float(change24h)
                change_str = f"{change_float:+.2f}%"
            except (ValueError, TypeError) as e:
                logger.debug(f"Could not format change '{change24h}': {e}")
                change_str = change24h
                
            return f"[PRIX CRYPTO TEMPS RÉEL] {name} ({symbol}): {price_str} | Variation 24h: {change_str}"
        
        # Try other formats
        if isinstance(data, dict):
            if "data" in data and isinstance(data["data"], list):
                return _extract_crypto_summary(data["data"], query)
            
            # CoinGecko format check
            for key in data:
                if isinstance(data[key], dict) and "usd" in data[key]:
                    price = data[key]["usd"]
                    return f"[PRIX CRYPTO TEMPS RÉEL] {key}: ${price:,.2f}"
        
        return str(data)[:500]
    except Exception as e:
        return str(data)[:500]


def _extract_stock_summary(data: dict, api_name: str) -> str:
    """Extract stock data in a clear format"""
    try:
        if not isinstance(data, dict):
            return str(data)[:500]
        
        # Handle different response formats
        if "data" in data:
            stock_data = data["data"]
        elif "success" in data and data.get("success"):
            stock_data = data.get("data", {})
        else:
            stock_data = data
        
        if not isinstance(stock_data, dict):
            return str(data)[:500]
        
        parts = []
        
        if api_name == "finance_stock":
            # Stock quote data
            symbol = stock_data.get("symbol", "N/A")
            price = stock_data.get("price") or stock_data.get("currentPrice") or stock_data.get("regularMarketPrice")
            change = stock_data.get("change") or stock_data.get("regularMarketChange")
            change_percent = stock_data.get("change_percent") or stock_data.get("changePercent") or stock_data.get("regularMarketChangePercent")
            volume = stock_data.get("volume")
            market_cap = stock_data.get("market_cap") or stock_data.get("marketCap")
            
            if price:
                price_str = f"${float(price):,.2f}" if isinstance(price, (int, float)) else str(price)
                parts.append(f"Prix: {price_str}")
            
            if change is not None:
                change_str = f"${float(change):,.2f}" if isinstance(change, (int, float)) else str(change)
                parts.append(f"Variation: {change_str}")
            
            if change_percent is not None:
                percent_str = f"{float(change_percent):+.2f}%" if isinstance(change_percent, (int, float)) else str(change_percent)
                parts.append(f"Variation %: {percent_str}")
            
            if volume:
                volume_str = f"{int(volume):,}" if isinstance(volume, (int, float)) else str(volume)
                parts.append(f"Volume: {volume_str}")
            
            if market_cap:
                cap_str = f"${int(market_cap):,}" if isinstance(market_cap, (int, float)) else str(market_cap)
                parts.append(f"Market Cap: {cap_str}")
            
            return f"[PRIX ACTION TEMPS RÉEL] {symbol}: {' | '.join(parts)}" if parts else str(data)[:500]
        
        elif api_name == "finance_company":
            # Company profile data
            company_name = stock_data.get("name") or stock_data.get("company_name") or stock_data.get("longName")
            industry = stock_data.get("industry")
            sector = stock_data.get("sector")
            description = stock_data.get("description") or stock_data.get("longBusinessSummary")
            
            if company_name:
                parts.append(f"Entreprise: {company_name}")
            if industry:
                parts.append(f"Industrie: {industry}")
            if sector:
                parts.append(f"Secteur: {sector}")
            if description:
                parts.append(f"Description: {description[:200]}")
            
            return f"[PROFIL ENTREPRISE] {' | '.join(parts)}" if parts else str(data)[:500]
        
        return str(data)[:500]
    except Exception as e:
        logger.debug(f"Error extracting stock summary: {e}")
        return str(data)[:500]


def _extract_news_summary(data: dict) -> str:
    """Extract news data in a clear format"""
    try:
        if not isinstance(data, dict):
            return str(data)[:500]
        
        # Handle different response formats
        if "news" in data:
            news_list = data["news"]
        elif "data" in data and isinstance(data["data"], list):
            news_list = data["data"]
        elif isinstance(data, list):
            news_list = data
        elif "success" in data and data.get("success"):
            news_list = data.get("data", {}).get("news", [])
        else:
            return str(data)[:500]
        
        if not isinstance(news_list, list) or len(news_list) == 0:
            return "Aucune actualité disponible."
        
        news_items = []
        for item in news_list[:5]:  # Limit to 5 news items
            if isinstance(item, dict):
                title = item.get("title") or item.get("headline")
                source = item.get("source") or item.get("source_name")
                summary = item.get("summary") or item.get("description")
                
                news_text = ""
                if title:
                    news_text = f"Titre: {title}"
                if source:
                    news_text += f" (Source: {source})"
                if summary:
                    news_text += f" - {summary[:150]}"
                
                if news_text:
                    news_items.append(news_text)
        
        return f"[ACTUALITÉS FINANCI├êRES]\n" + "\n".join(news_items) if news_items else "Aucune actualité disponible."
    except Exception as e:
        logger.debug(f"Error extracting news summary: {e}")
        return str(data)[:500]


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
    [LIST] Get list of all available AI experts
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


@router.get("/categories")
async def list_categories():
    """
    [CAT] Get all expert categories
    """
    categories = get_all_categories()
    return [
        {
            "id": c.id.value,
            "name": c.name,
            "name_en": c.name_en,
            "emoji": c.emoji,
            "description": c.description,
            "color": c.color,
        }
        for c in categories
    ]


@router.get("/grouped")
async def get_experts_by_categories():
    """
    [GROUP] Get all experts grouped by category
    Perfect for building an explore/discover page
    """
    return get_experts_grouped_by_category()


@router.get("/category/{category_id}")
async def get_category_experts(category_id: str):
    """
    [CAT] Get all experts in a specific category
    """
    experts = get_experts_by_category(category_id)
    if not experts:
        raise HTTPException(status_code=404, detail=f"No experts found for category '{category_id}'")
    
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
    [INFO] Get information about a specific expert
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
    [CHAT] Chat with a specialized AI expert
    
    The expert will:
    1. Fetch relevant data from its connected APIs
    2. Use its specialized personality and knowledge
    3. Provide contextual, domain-specific responses
    """
    start_time = time.time()
    
    # Générer session_id si non fourni
    import uuid
    session_id = body.session_id or f"session_{uuid.uuid4().hex[:12]}"
    
    # Get expert config
    expert = get_expert(expert_id)
    if not expert:
        raise HTTPException(status_code=404, detail=f"Expert '{expert_id}' not found")
    
    # Détecter les questions sensibles qui ne doivent pas être cachées
    sensitive_keywords = [
        "élection", "election", "président", "president", "biden", "trump",
        "aujourd'hui", "today", "maintenant", "now", "actuel", "current"
    ]
    is_sensitive = any(kw in body.message.lower() for kw in sensitive_keywords)
    use_cache = not is_sensitive  # Désactiver cache pour questions sensibles
    
    # Check cache first (avec session_id pour permettre variation)
    if use_cache:
        cache_key = f"expert:{expert_id}:{session_id}:{body.message}"
        cached = cache_service.get("expert_chat", cache_key)
        if cached:
            # Vérifier si la réponse est trop récente (moins de 2 minutes) - ignorer le cache pour éviter répétitions
            cached_timestamp = cached.get("timestamp", 0)
            cache_age = time.time() - cached_timestamp
            
            # Utiliser le cache seulement si la réponse a plus de 2 minutes (évite répétitions immédiates)
            if cache_age > 120:  # 2 minutes
                return ExpertChatResponse(
                    expert_id=expert_id,
                    expert_name=expert.name,
                    response=cached["response"],
                    session_id=session_id,
                    sources=cached.get("sources", []),
                    source="cache",
                    processing_time_ms=(time.time() - start_time) * 1000
                )
            # Sinon, ignorer le cache pour forcer une nouvelle réponse (évite répétitions immédiates)
    
    # ============================================
    # MÉMOIRE V2 - Système amélioré avec profilage
    # ============================================
    try:
        from services.enhanced_memory import enhanced_memory, get_smart_context
        
        # Stocker le message utilisateur avec tracking intelligent
        enhanced_memory.add_message(
            session_id=session_id,
            expert_id=expert_id,
            role="user",
            message=body.message
        )
        
        # Construire le contexte intelligent (profil + sujets + historique compact)
        memory_context = enhanced_memory.build_smart_context(
            session_id=session_id,
            expert_id=expert_id,
            include_profile=True,
            include_topics=True,
            max_messages=10
        )
        
        # Détection automatique du profil utilisateur (pour expert santé)
        if expert_id == "health":
            user_profile = enhanced_memory.get_or_create_profile(session_id)
            profile_type = user_profile.get("user_type")
            
            # Si profil détecté, adapter le format de réponse
            if profile_type:
                logger.info(f"Using profile '{profile_type}' for health expert")
        
    except ImportError:
        # Fallback sur l'ancien système si enhanced_memory n'existe pas
        from services.conversation_manager import conversation_manager
        
        history = conversation_manager.get_conversation_history(session_id, expert_id, limit=10)
        memory_context = conversation_manager.format_history_for_prompt(history)
        
        conversation_manager.add_message(
            session_id=session_id,
            expert_id=expert_id,
            role="user",
            message=body.message
        )
    
    # Fetch context data from expert's APIs
    context, sources = await fetch_context_data(expert, body.message)
    
    # Auto-detect language: prioriser la langue du message si détectable, sinon utiliser celle fournie
    # Si le message est clairement dans une langue différente de celle fournie, utiliser la langue du message
    detected_lang = detect_language(body.message)
    if body.language and detected_lang != body.language:
        # Si la langue détectée du message est différente de celle fournie, prioriser le message
        # Sauf si le message est trop court (< 10 caractères) ou ambigu
        if len(body.message.strip()) > 10:
            language = detected_lang
            logger.debug(f"Language mismatch: provided={body.language}, detected={detected_lang}, using detected")
        else:
            language = body.language
    else:
        language = body.language or detected_lang
    
    # Add current date/time to context (critical for date-aware experts)
    date_info = get_current_datetime_context(language)
    
    # Construire le contexte final (ordre optimisé pour les tokens)
    # Format: Date -> Mémoire (profil+historique) -> APIs
    context = f"{date_info}\n\n{memory_context}\n\n{context}" if memory_context else f"{date_info}\n\n{context}"
    
    # Build system prompt with context
    system_prompt = expert.system_prompt.replace("{context}", context)
    
    # Add language instruction
    lang_instruction = get_language_instruction(language)
    system_prompt += f"\n\n{lang_instruction}"
    
    # Add instruction to avoid repeating welcome message
    system_prompt += f"\n\nIMPORTANT: Ne répète JAMAIS le message d'introduction ou de bienvenue. Réponds directement à la question de l'utilisateur."
    
    # Améliorer le prompt avec le validateur
    from services.ai_response_validator import ai_response_validator
    system_prompt = ai_response_validator.enhance_system_prompt(
        system_prompt,
        body.message,
        expert_type=expert_id
    )
    
    # Route to AI avec retry automatique
    max_retries = 3
    retry_delay = 1.0
    result = None
    last_error = None
    
    for attempt in range(max_retries):
        try:
            result = await ai_router.route(
                prompt=body.message,
                system_prompt=system_prompt
            )
            break  # Succès, sortir de la boucle
            
        except Exception as e:
            last_error = e
            error_type = type(e).__name__
            error_msg = str(e)[:200]  # Limiter la longueur du message
            logger.warning(
                f"Expert chat attempt {attempt + 1}/{max_retries} failed for {expert_id}: "
                f"{error_type}: {error_msg}"
            )
            
            if attempt < max_retries - 1:
                # Attendre avant de réessayer (backoff exponentiel)
                wait_time = retry_delay * (2 ** attempt)
                logger.debug(f"Retrying in {wait_time:.1f}s...")
                await asyncio.sleep(wait_time)
            else:
                # Dernière tentative échouée
                logger.error(
                    f"Expert chat error after {max_retries} attempts for {expert_id}: "
                    f"{error_type}: {error_msg}",
                    exc_info=True  # Inclure la stack trace complète
                )
                raise HTTPException(
                    status_code=503, 
                    detail=f"AI service temporarily unavailable after {max_retries} attempts. Please try again later."
                )
    
    if not result:
        raise HTTPException(status_code=503, detail="AI service temporarily unavailable")
    
    # Valider la réponse
    is_valid, validation_details = ai_response_validator.validate_response(
        response=result["response"],
        query=body.message,
        context=context,
        expert_type=expert_id
    )
    
    # Re-génération automatique pour hallucinations critiques et réponses invalides
    confidence = validation_details.get("confidence_score", 1.0)
    has_critical_hallucination = any(
        "politique" in w.lower() and "électorale" in w.lower()
        for w in validation_details.get("warnings", [])
    )
    repetition_detected = any("répétition" in w.lower() for w in validation_details.get("warnings", []))
    
    # Re-générer si : hallucination critique OU confiance < 0.5 OU répétitions détectées
    should_regenerate = False
    regenerate_reason = ""
    
    if has_critical_hallucination:
        should_regenerate = True
        regenerate_reason = "hallucination critique"
    elif confidence < 0.5:
        should_regenerate = True
        regenerate_reason = "faible confiance"
    elif repetition_detected:
        should_regenerate = True
        regenerate_reason = "répétitions détectées"
    
    if should_regenerate:
        # Re-générer avec un prompt plus strict
        logger.warning(f"Re-génération nécessaire pour {expert_id}: {regenerate_reason} (confidence: {confidence:.2f})")
        
        # Construire un prompt de vérification stricte selon le type de problème
        strict_instructions = []
        if has_critical_hallucination:
            strict_instructions.append("[WARN] ATTENTION CRITIQUE: La réponse précédente contenait des informations potentiellement erronées. Vérifie TOUTES les informations factuelles avant de répondre. Si tu n'es pas sûr, dis-le clairement. Ne mentionne JAMAIS de résultats d'élections sans vérifier la date actuelle et les sources officielles.")
        if confidence < 0.5:
            strict_instructions.append("[WARN] IMPORTANT: La réponse précédente avait une faible confiance. Sois plus précis et factuel. Cite tes sources si possible.")
        if repetition_detected:
            strict_instructions.append("[WARN] IMPORTANT: La réponse précédente contenait des répétitions. Reformule différemment et évite de répéter les mêmes phrases.")
        
        strict_prompt = system_prompt + "\n\n" + "\n\n".join(strict_instructions)
        
        try:
            result = await ai_router.route(
                prompt=body.message,
                system_prompt=strict_prompt
            )
            
            # Re-valider
            is_valid, validation_details = ai_response_validator.validate_response(
                response=result["response"],
                query=body.message,
                context=context,
                expert_type=expert_id
            )
            
            confidence = validation_details.get("confidence_score", 1.0)
            logger.info(f"Re-génération terminée pour {expert_id}: nouvelle confiance = {confidence:.2f}")
        except Exception as e:
            logger.error(f"Error during regeneration: {e}")
    
    # Si la réponse n'est toujours pas valide après re-génération, rejeter complètement si confiance très faible
    if not is_valid or confidence < 0.3:
        logger.warning(f"Invalid expert response for {expert_id}: confidence={confidence:.2f}, validation={validation_details}")
        # Si confiance très faible, retourner quand même la réponse avec un avertissement plutôt que d'échouer
        # Cela évite les erreurs "Désolé, je n'ai pas pu répondre" pour des questions valides
        if confidence < 0.3:
            # Au lieu de rejeter, ajouter un avertissement mais retourner quand même la réponse
            logger.info(f"Low confidence response for {expert_id}, but returning it with warning (confidence: {confidence:.2f})")
            result["response"] = f"{result['response']}\n\n[WARN] Note: Cette réponse nécessite une vérification supplémentaire."
        else:
            # Sinon, ajouter un avertissement
            result["response"] = f"[WARN] {result['response']}\n\n(Note: Cette réponse nécessite une vérification supplémentaire)"
    
    # Stocker la réponse de l'IA dans la mémoire
    try:
        from services.enhanced_memory import enhanced_memory
        enhanced_memory.add_message(
            session_id=session_id,
            expert_id=expert_id,
            role="assistant",
            message=result["response"]
        )
    except ImportError:
        from services.conversation_manager import conversation_manager
        conversation_manager.add_message(
            session_id=session_id,
            expert_id=expert_id,
            role="assistant",
            message=result["response"]
        )
    
    # Cache the response
    if use_cache:
        cache_ttl = 600 if validation_details.get("confidence_score", 1.0) > 0.8 else 300
        cache_service.set(
            "expert_chat",
            cache_key,
            {
                "response": result["response"],
                "sources": sources,
                "timestamp": time.time()
            },
            ttl=cache_ttl
        )
    
    # Logging
    processing_time = (time.time() - start_time) * 1000
    logger.info(
        f"Expert chat completed: expert={expert_id}, "
        f"time={processing_time:.0f}ms, "
        f"valid={is_valid}, "
        f"sources={len(sources)}"
    )
    
    return ExpertChatResponse(
        expert_id=expert_id,
        expert_name=expert.name,
        response=result["response"],
        session_id=session_id,
        sources=sources,
        source=result["source"],
        processing_time_ms=processing_time
    )


@router.post("/{expert_id}/chat/stream")
async def chat_with_expert_stream(expert_id: str, body: ExpertChatRequest):
    """
    [STREAM] Chat with a specialized AI expert (Streaming)
    """
    # Get expert config
    expert = get_expert(expert_id)
    if not expert:
        raise HTTPException(status_code=404, detail=f"Expert '{expert_id}' not found")

    # Generate session_id
    import uuid
    session_id = body.session_id or f"session_{uuid.uuid4().hex[:12]}"
    
    async def event_generator():
        try:
            # Update History
            from services.conversation_manager import conversation_manager
            conversation_manager.add_message(
                session_id=session_id,
                expert_id=expert_id,
                role="user",
                message=body.message
            )
            
            # Fetch Data
            context, sources = await fetch_context_data(expert, body.message)
            
            # Detect Language & Context
            detected_lang = detect_language(body.message)
            language = body.language or detected_lang
            
            history = conversation_manager.get_conversation_history(session_id, expert_id, limit=10)
            history_context = conversation_manager.format_history_for_prompt(history)
            
            date_info = get_current_datetime_context(language)
            full_context = f"{date_info}\n\n{context}"
            if history_context:
                full_context = f"{history_context}\n\n{full_context}"
                
            system_prompt = expert.system_prompt.replace("{context}", full_context)
            system_prompt += f"\n\n{get_language_instruction(language)}"
            system_prompt += "\n\nIMPORTANT: Réponds directement. Ne répète jamais le message de bienvenue."
            
            # Stream AI Response
            full_response_text = ""
            async for chunk in ai_router.route_stream(
                prompt=body.message, 
                system_prompt=system_prompt
            ):
                if chunk:
                    full_response_text += chunk
                    yield chunk
                    
            # Post-processing (Background)
            conversation_manager.add_message(
                session_id=session_id,
                expert_id=expert_id,
                role="assistant",
                message=full_response_text
            )
            
            if len(full_response_text) > 50:
                cache_key = f"expert:{expert_id}:{session_id}:{body.message}"
                cache_service.set(
                    "expert_chat",
                    cache_key,
                    {
                        "response": full_response_text,
                        "sources": sources,
                        "timestamp": time.time()
                    },
                    ttl=3600
                )
                
        except Exception as e:
            logger.error(f"Streaming error: {e}")
            yield f"\n[ERR] Error: {str(e)}"

    return StreamingResponse(event_generator(), media_type="text/plain")


def _extract_news_summary(data: dict) -> str:
    """Extract news data in a clear format"""
    try:
        if not isinstance(data, dict):
            return str(data)[:500]
        
        # Handle different response formats
        if "news" in data:
            news_list = data["news"]
        elif "data" in data and isinstance(data["data"], list):
            news_list = data["data"]
        elif isinstance(data, list):
            news_list = data
        elif "success" in data and data.get("success"):
            news_list = data.get("data", {}).get("news", [])
        else:
            return str(data)[:500]
        
        if not isinstance(news_list, list) or len(news_list) == 0:
            return "Aucune actualité disponible."
        
        news_items = []
        for item in news_list[:5]:  # Limit to 5 news items
            if isinstance(item, dict):
                title = item.get("title") or item.get("headline")
                source = item.get("source") or item.get("source_name")
                summary = item.get("summary") or item.get("description")
                
                news_text = ""
                if title:
                    news_text = f"Titre: {title}"
                if source:
                    news_text += f" (Source: {source})"
                if summary:
                    news_text += f" - {summary[:150]}"
                
                if news_text:
                    news_items.append(news_text)
        
        return f"[ACTUALITÉS FINANCI├êRES]\n" + "\n".join(news_items) if news_items else "Aucune actualité disponible."
    except Exception as e:
        logger.debug(f"Error extracting news summary: {e}")
        return str(data)[:500]


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
    [LIST] Get list of all available AI experts
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


@router.get("/categories")
async def list_categories():
    """
    [CAT] Get all expert categories
    """
    categories = get_all_categories()
    return [
        {
            "id": c.id.value,
            "name": c.name,
            "name_en": c.name_en,
            "emoji": c.emoji,
            "description": c.description,
            "color": c.color,
        }
        for c in categories
    ]


@router.get("/grouped")
async def get_experts_by_categories():
    """
    [GROUP] Get all experts grouped by category
    Perfect for building an explore/discover page
    """
    return get_experts_grouped_by_category()


@router.get("/category/{category_id}")
async def get_category_experts(category_id: str):
    """
    [CAT] Get all experts in a specific category
    """
    experts = get_experts_by_category(category_id)
    if not experts:
        raise HTTPException(status_code=404, detail=f"No experts found for category '{category_id}'")
    
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
    [INFO] Get information about a specific expert
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
    [CHAT] Chat with a specialized AI expert
    
    The expert will:
    1. Fetch relevant data from its connected APIs
    2. Use its specialized personality and knowledge
    3. Provide contextual, domain-specific responses
    """
    start_time = time.time()
    
    # Générer session_id si non fourni
    import uuid
    session_id = body.session_id or f"session_{uuid.uuid4().hex[:12]}"
    
    # Get expert config
    expert = get_expert(expert_id)
    if not expert:
        raise HTTPException(status_code=404, detail=f"Expert '{expert_id}' not found")
    
    # Détecter les questions sensibles qui ne doivent pas être cachées
    sensitive_keywords = [
        "élection", "election", "président", "president", "biden", "trump",
        "aujourd'hui", "today", "maintenant", "now", "actuel", "current"
    ]
    is_sensitive = any(kw in body.message.lower() for kw in sensitive_keywords)
    use_cache = not is_sensitive  # Désactiver cache pour questions sensibles
    
    # Check cache first (avec session_id pour permettre variation)
    if use_cache:
        cache_key = f"expert:{expert_id}:{session_id}:{body.message}"
        cached = cache_service.get("expert_chat", cache_key)
        if cached:
            # Vérifier si la réponse est trop récente (moins de 2 minutes) - ignorer le cache pour éviter répétitions
            cached_timestamp = cached.get("timestamp", 0)
            cache_age = time.time() - cached_timestamp
            
            # Utiliser le cache seulement si la réponse a plus de 2 minutes (évite répétitions immédiates)
            if cache_age > 120:  # 2 minutes
                return ExpertChatResponse(
                    expert_id=expert_id,
                    expert_name=expert.name,
                    response=cached["response"],
                    session_id=session_id,
                    sources=cached.get("sources", []),
                    source="cache",
                    processing_time_ms=(time.time() - start_time) * 1000
                )
            # Sinon, ignorer le cache pour forcer une nouvelle réponse (évite répétitions immédiates)
    
    # Récupérer l'historique de conversation
    from services.conversation_manager import conversation_manager
    history = conversation_manager.get_conversation_history(session_id, expert_id, limit=10)
    history_context = conversation_manager.format_history_for_prompt(history)
    
    # Stocker le message utilisateur
    conversation_manager.add_message(
        session_id=session_id,
        expert_id=expert_id,
        role="user",
        message=body.message
    )
    
    # Fetch context data from expert's APIs
    context, sources = await fetch_context_data(expert, body.message)
    
    # Auto-detect language: prioriser la langue du message si détectable, sinon utiliser celle fournie
    # Si le message est clairement dans une langue différente de celle fournie, utiliser la langue du message
    detected_lang = detect_language(body.message)
    if body.language and detected_lang != body.language:
        # Si la langue détectée du message est différente de celle fournie, prioriser le message
        # Sauf si le message est trop court (< 10 caractères) ou ambigu
        if len(body.message.strip()) > 10:
            language = detected_lang
            logger.debug(f"Language mismatch: provided={body.language}, detected={detected_lang}, using detected")
        else:
            language = body.language
    else:
        language = body.language or detected_lang
    
    # Add current date/time to context (critical for date-aware experts)
    date_info = get_current_datetime_context(language)
    context = date_info + "\n\n" + context
    
    # Injecter l'historique dans le contexte
    if history_context:
        context = history_context + "\n\n" + context
    
    # Build system prompt with context
    system_prompt = expert.system_prompt.replace("{context}", context)
    
    # Add language instruction
    lang_instruction = get_language_instruction(language)
    system_prompt += f"\n\n{lang_instruction}"
    
    # Add instruction to avoid repeating welcome message
    system_prompt += f"\n\nIMPORTANT: Ne répète JAMAIS le message d'introduction ou de bienvenue. Réponds directement à la question de l'utilisateur."
    
    # Améliorer le prompt avec le validateur
    from services.ai_response_validator import ai_response_validator
    system_prompt = ai_response_validator.enhance_system_prompt(
        system_prompt,
        body.message,
        expert_type=expert_id
    )
    
    # Route to AI avec retry automatique
    max_retries = 3
    retry_delay = 1.0
    result = None
    last_error = None
    
    for attempt in range(max_retries):
        try:
            result = await ai_router.route(
                prompt=body.message,
                system_prompt=system_prompt
            )
            break  # Succès, sortir de la boucle
            
        except Exception as e:
            last_error = e
            error_type = type(e).__name__
            error_msg = str(e)[:200]  # Limiter la longueur du message
            logger.warning(
                f"Expert chat attempt {attempt + 1}/{max_retries} failed for {expert_id}: "
                f"{error_type}: {error_msg}"
            )
            
            if attempt < max_retries - 1:
                # Attendre avant de réessayer (backoff exponentiel)
                wait_time = retry_delay * (2 ** attempt)
                logger.debug(f"Retrying in {wait_time:.1f}s...")
                await asyncio.sleep(wait_time)
            else:
                # Dernière tentative échouée
                logger.error(
                    f"Expert chat error after {max_retries} attempts for {expert_id}: "
                    f"{error_type}: {error_msg}",
                    exc_info=True  # Inclure la stack trace complète
                )
                raise HTTPException(
                    status_code=503, 
                    detail=f"AI service temporarily unavailable after {max_retries} attempts. Please try again later."
                )
    
    if not result:
        raise HTTPException(status_code=503, detail="AI service temporarily unavailable")
    
    # Valider la réponse
    is_valid, validation_details = ai_response_validator.validate_response(
        response=result["response"],
        query=body.message,
        context=context,
        expert_type=expert_id
    )
    
    # Re-génération automatique pour hallucinations critiques et réponses invalides
    confidence = validation_details.get("confidence_score", 1.0)
    has_critical_hallucination = any(
        "politique" in w.lower() and "électorale" in w.lower()
        for w in validation_details.get("warnings", [])
    )
    repetition_detected = any("répétition" in w.lower() for w in validation_details.get("warnings", []))
    
    # Re-générer si : hallucination critique OU confiance < 0.5 OU répétitions détectées
    should_regenerate = False
    regenerate_reason = ""
    
    if has_critical_hallucination:
        should_regenerate = True
        regenerate_reason = "hallucination critique"
    elif confidence < 0.5:
        should_regenerate = True
        regenerate_reason = "faible confiance"
    elif repetition_detected:
        should_regenerate = True
        regenerate_reason = "répétitions détectées"
    
    if should_regenerate:
        # Re-générer avec un prompt plus strict
        logger.warning(f"Re-génération nécessaire pour {expert_id}: {regenerate_reason} (confidence: {confidence:.2f})")
        
        # Construire un prompt de vérification stricte selon le type de problème
        strict_instructions = []
        if has_critical_hallucination:
            strict_instructions.append("[WARN] ATTENTION CRITIQUE: La réponse précédente contenait des informations potentiellement erronées. Vérifie TOUTES les informations factuelles avant de répondre. Si tu n'es pas sûr, dis-le clairement. Ne mentionne JAMAIS de résultats d'élections sans vérifier la date actuelle et les sources officielles.")
        if confidence < 0.5:
            strict_instructions.append("[WARN] IMPORTANT: La réponse précédente avait une faible confiance. Sois plus précis et factuel. Cite tes sources si possible.")
        if repetition_detected:
            strict_instructions.append("[WARN] IMPORTANT: La réponse précédente contenait des répétitions. Reformule différemment et évite de répéter les mêmes phrases.")
        
        strict_prompt = system_prompt + "\n\n" + "\n\n".join(strict_instructions)
        
        try:
            result = await ai_router.route(
                prompt=body.message,
                system_prompt=strict_prompt
            )
            
            # Re-valider
            is_valid, validation_details = ai_response_validator.validate_response(
                response=result["response"],
                query=body.message,
                context=context,
                expert_type=expert_id
            )
            
            confidence = validation_details.get("confidence_score", 1.0)
            logger.info(f"Re-génération terminée pour {expert_id}: nouvelle confiance = {confidence:.2f}")
        except Exception as e:
            logger.error(f"Error during regeneration: {e}")
    
    # Si la réponse n'est toujours pas valide après re-génération, rejeter complètement si confiance très faible
    if not is_valid or confidence < 0.3:
        logger.warning(f"Invalid expert response for {expert_id}: confidence={confidence:.2f}, validation={validation_details}")
        # Si confiance très faible, retourner quand même la réponse avec un avertissement plutôt que d'échouer
        # Cela évite les erreurs "Désolé, je n'ai pas pu répondre" pour des questions valides
        if confidence < 0.3:
            # Au lieu de rejeter, ajouter un avertissement mais retourner quand même la réponse
            logger.info(f"Low confidence response for {expert_id}, but returning it with warning (confidence: {confidence:.2f})")
            result["response"] = f"{result['response']}\n\n[WARN] Note: Cette réponse nécessite une vérification supplémentaire."
        else:
            # Sinon, ajouter un avertissement
            result["response"] = f"[WARN] {result['response']}\n\n(Note: Cette réponse nécessite une vérification supplémentaire)"
    
    # Stocker la réponse de l'IA dans la conversation
    conversation_manager.add_message(
        session_id=session_id,
        expert_id=expert_id,
        message=result["response"]
    )
    
    # Cache the response
    if use_cache:
        cache_ttl = 600 if validation_details.get("confidence_score", 1.0) > 0.8 else 300
        cache_service.set(
            "expert_chat",
            cache_key,
            {
                "response": result["response"],
                "sources": sources,
                "timestamp": time.time()
            },
            ttl=cache_ttl
        )
    
    # Logging
    processing_time = (time.time() - start_time) * 1000
    logger.info(
        f"Expert chat completed: expert={expert_id}, "
        f"time={processing_time:.0f}ms, "
        f"valid={is_valid}, "
        f"sources={len(sources)}"
    )
    
    return ExpertChatResponse(
        expert_id=expert_id,
        expert_name=expert.name,
        response=result["response"],
        session_id=session_id,
        sources=sources,
        source=result["source"],
        processing_time_ms=processing_time
    )


@router.post("/{expert_id}/chat/stream")
async def chat_with_expert_stream(expert_id: str, body: ExpertChatRequest):
    """
    [STREAM] Chat with a specialized AI expert (Streaming)
    """
    # Get expert config
    expert = get_expert(expert_id)
    if not expert:
        raise HTTPException(status_code=404, detail=f"Expert '{expert_id}' not found")

    # Generate session_id
    import uuid
    session_id = body.session_id or f"session_{uuid.uuid4().hex[:12]}"
    
    async def event_generator():
        try:
            # Update History
            from services.conversation_manager import conversation_manager
            conversation_manager.add_message(
                session_id=session_id,
                expert_id=expert_id,
                role="user",
                message=body.message
            )
            
            # Fetch Data
            context, sources = await fetch_context_data(expert, body.message)
            
            # Detect Language & Context
            detected_lang = detect_language(body.message)
            language = body.language or detected_lang
            
            history = conversation_manager.get_conversation_history(session_id, expert_id, limit=10)
            history_context = conversation_manager.format_history_for_prompt(history)
            
            date_info = get_current_datetime_context(language)
            full_context = f"{date_info}\n\n{context}"
            if history_context:
                full_context = f"{history_context}\n\n{full_context}"
                
            system_prompt = expert.system_prompt.replace("{context}", full_context)
            system_prompt += f"\n\n{get_language_instruction(language)}"
            system_prompt += "\n\nIMPORTANT: Réponds directement. Ne répète jamais le message de bienvenue."
            
            # Stream AI Response
            full_response_text = ""
            async for chunk in ai_router.route_stream(
                prompt=body.message, 
                system_prompt=system_prompt
            ):
                if chunk:
                    full_response_text += chunk
                    yield chunk
                    
            # Post-processing (Background)
            conversation_manager.add_message(
                session_id=session_id,
                expert_id=expert_id,
                role="assistant",
                message=full_response_text
            )
            
            if len(full_response_text) > 50:
                cache_key = f"expert:{expert_id}:{session_id}:{body.message}"
                cache_service.set(
                    "expert_chat",
                    cache_key,
                    {
                        "response": full_response_text,
                        "sources": sources,
                        "timestamp": time.time()
                    },
                    ttl=3600
                )
                
        except Exception as e:
            logger.error(f"Streaming error: {e}")
            yield f"\n[ERR] Error: {str(e)}"

    return StreamingResponse(event_generator(), media_type="text/plain")
