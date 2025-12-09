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

        
        if cached:
            return ChatResponse(
                response=cached["response"],
                source="cache",
                processing_time_ms=(time.time() - start_time) * 1000
            )
        
        # Build system prompt with date context
        date_context = get_current_datetime_context()
        system_prompt = SYSTEM_PROMPTS.get(body.language, SYSTEM_PROMPTS["he"])
        system_prompt = f"{date_context}\n\n{system_prompt}"
        
        if body.context:
            system_prompt += f"\n\nContext: {body.context}"
        
        # Améliorer le prompt système avec le validateur
        system_prompt = ai_response_validator.enhance_system_prompt(
            system_prompt, 
            body.message,
            expert_type=None
        )
        
        # Route to AI avec retry automatique
        max_retries = 3
        retry_delay = 1.0
        result = None
        
        for attempt in range(max_retries):
            try:
                result = await ai_router.route(
                    prompt=body.message,
                    system_prompt=system_prompt
                )
                break  # Succès, sortir de la boucle
                
            except Exception as e:
                error_type = type(e).__name__
                error_msg = str(e)[:200]  # Limiter la longueur du message
                logger.warning(
                    f"Chat attempt {attempt + 1}/{max_retries} failed: "
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
                        f"Chat error after {max_retries} attempts: "
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
            context=body.context
        )
        
        # Vérifier spécifiquement les informations politiques
        political_warnings = [w for w in validation_details.get("warnings", []) 
                            if "politique" in w.lower() or "électorale" in w.lower()]
        
        # Si la réponse n'est pas valide, logger et potentiellement améliorer
        if not is_valid:
            logger.warning(f"Invalid AI response detected: {validation_details}")
            # Optionnel: réessayer avec un prompt amélioré ou ajouter un avertissement
            confidence = validation_details.get("confidence_score", 1.0)
            if confidence < 0.3:
                # Retourner la réponse sans avertissement technique
                logger.info(f"Low confidence response, returning as-is (confidence: {confidence:.2f})")
                # Ne pas ajouter de [WARN] - laisser la réponse naturelle
        
        # Les informations politiques n'ont plus besoin d'avertissement spécial
        if political_warnings:
            logger.info(f"Political information detected in response: {political_warnings}")
        
        # Ajouter les métadonnées de validation
        result["validation"] = {
            "is_valid": is_valid,
            "confidence_score": validation_details.get("confidence_score", 1.0),
            "warnings": validation_details.get("warnings", [])
        }
        
        # Cache the response avec TTL adaptatif selon la qualité
        # TTL plus long pour les réponses validées avec haute confiance
        base_ttl = int(os.getenv("CACHE_TTL_CHAT", 3600))
        cache_ttl = base_ttl * 2 if validation_details.get("confidence_score", 1.0) > 0.8 else base_ttl
        cache_service.set(
            "chat",
            cache_key,
            {"response": result["response"]},
            ttl=cache_ttl
        )
        
        # Logging amélioré pour le diagnostic
        processing_time = (time.time() - start_time) * 1000
        logger.info(
            f"Chat completed: time={processing_time:.0f}ms, "
            f"valid={is_valid}, "
            f"confidence={validation_details.get('confidence_score', 1.0):.2f}, "
            f"warnings={len(validation_details.get('warnings', []))}, "
            f"cached_ttl={cache_ttl}s"
        )
        
        # 🧠 Memory Hook: Process conversation in background
        if user:
            user_id = user.get("sub", "anonymous")
            background_tasks.add_task(
                memory_manager.process_conversation, 
                user_id, 
                body.message, 
                "user"
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
