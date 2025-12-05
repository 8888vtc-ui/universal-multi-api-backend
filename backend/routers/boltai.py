"""
BoltAI API Router
L'IA en un éclair ⚡
"""
from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
from typing import Optional
from services.boltai import BoltAIRouter

router = APIRouter(prefix="/api/boltai", tags=["boltai"])

boltai = BoltAIRouter()


class ChatRequest(BaseModel):
    message: str
    model: str = 'bolt-turbo'
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = 2000


@router.post("/chat")
async def boltai_chat(request: ChatRequest):
    """
    BoltAI Chat - L'IA en un éclair ⚡
    
    Modèles disponibles :
    - bolt-turbo : Ultra rapide (Groq)
    - bolt-pro : Puissant (Gemini)
    - bolt-french : Optimisé français (Mistral)
    - bolt-code : Spécialisé code (DeepSeek)
    - bolt-creative : Créatif (OpenRouter)
    
    Features :
    - Fallback automatique (99.99% uptime)
    - Réponses ultra-rapides
    - Support multi-langues
    - Spécialisations par domaine
    """
    try:
        result = await boltai.chat(
            message=request.message,
            model=request.model,
            temperature=request.temperature,
            max_tokens=request.max_tokens
        )
        return {"success": True, **result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/models")
async def get_boltai_models():
    """
    Liste des modèles BoltAI disponibles
    
    Retourne tous les modèles avec descriptions et cas d'usage
    """
    try:
        models = await boltai.get_models()
        return {"success": True, **models}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status")
async def get_boltai_status():
    """
    Status BoltAI
    
    Retourne l'état du service et les features
    """
    try:
        status = boltai.get_status()
        return {"success": True, **status}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/")
async def boltai_info():
    """
    Informations BoltAI
    """
    return {
        "service": "BoltAI",
        "tagline": "L'IA en un éclair ⚡",
        "version": "1.0.0",
        "description": "Agrégateur intelligent avec fallback automatique",
        "features": [
            "5 modèles spécialisés",
            "7 providers en fallback",
            "99.99% uptime garanti",
            "Réponses ultra-rapides",
            "Support français natif"
        ],
        "endpoints": {
            "chat": "/api/boltai/chat",
            "models": "/api/boltai/models",
            "status": "/api/boltai/status"
        },
        "pricing": {
            "free": "100 req/jour",
            "pro": "19€/mois - 10k req/mois",
            "business": "99€/mois - 100k req/mois"
        }
    }
