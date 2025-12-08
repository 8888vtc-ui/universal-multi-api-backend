"""
Router pour la Recherche Intelligente IA + Data
Endpoints pour le moteur de recherche avec synthèse IA
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional, Dict, Any, List
from pydantic import BaseModel
import time

from services.ai_search_engine import ai_search_engine, SearchIntent


router = APIRouter(prefix="/api/ai-search", tags=["AI Search"])


class AISearchRequest(BaseModel):
    """Requête de recherche IA"""
    query: str
    use_cache: bool = True
    include_raw_data: bool = True


class AISearchResponse(BaseModel):
    """Réponse de recherche IA"""
    query: str
    intent: str
    sources_count: int
    ai_synthesis: str
    ai_recommendations: List[str]
    confidence_score: float
    execution_time_ms: float
    cached: bool
    data: Optional[Dict[str, Any]] = None


class QueryAnalysisResponse(BaseModel):
    """Réponse d'analyse de requête"""
    query: str
    intent: str
    entities: List[str]
    categories: List[str]
    freshness: str
    confidence: float
    ai_analyzed: bool


@router.post("/search", response_model=AISearchResponse)
async def ai_search(request: AISearchRequest):
    """
    🧠 RECHERCHE INTELLIGENTE IA + DATA
    
    Combine l'intelligence artificielle avec la recherche multi-sources:
    
    **Flux:**
    1. [INFO] L'IA analyse votre requête (intention, entités)
    2. 📡 Recherche parallèle dans les APIs pertinentes
    3. 🧠 L'IA synthétise et enrichit les résultats
    4. 💡 Recommandations personnalisées
    
    **Exemple:**
    ```json
    {
        "query": "Dois-je investir dans Bitcoin aujourd'hui?",
        "use_cache": true
    }
    ```
    
    **Réponse:**
    - Synthèse IA des données actuelles
    - Recommandations basées sur les tendances
    - Score de confiance
    """
    try:
        result = await ai_search_engine.search(
            query=request.query,
            use_cache=request.use_cache
        )
        
        response_data = {
            "query": result.query,
            "intent": result.intent,
            "sources_count": result.sources_count,
            "ai_synthesis": result.ai_synthesis,
            "ai_recommendations": result.ai_recommendations,
            "confidence_score": result.confidence_score,
            "execution_time_ms": round(result.execution_time_ms, 2),
            "cached": result.cached
        }
        
        if request.include_raw_data:
            response_data["data"] = result.data
        
        return AISearchResponse(**response_data)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/analyze", response_model=QueryAnalysisResponse)
async def analyze_query(
    query: str = Query(..., description="Requête à analyser")
):
    """
    [INFO] ANALYSE DE REQUÊTE PAR L'IA
    
    L'IA analyse votre requête et détecte:
    - **Intention**: information, realtime, comparison, recommendation, etc.
    - **Entités**: éléments clés de la requête
    - **Catégories**: APIs pertinentes à interroger
    - **Fraîcheur**: niveau de fraîcheur des données requis
    
    **Exemple:**
    ```
    GET /api/ai-search/analyze?query=prix bitcoin
    ```
    """
    try:
        analysis = await ai_search_engine.analyze_query(query)
        
        return QueryAnalysisResponse(
            query=query,
            intent=analysis.get("intent", "information"),
            entities=analysis.get("entities", []),
            categories=analysis.get("categories", []),
            freshness=analysis.get("freshness", "fresh"),
            confidence=analysis.get("confidence", 0.5),
            ai_analyzed=analysis.get("ai_analyzed", False)
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/intents", response_model=List[Dict[str, str]])
async def list_intents():
    """
    📋 LISTE DES INTENTIONS DE RECHERCHE
    
    Retourne les types d'intentions que l'IA peut détecter:
    - **information**: Recherche d'informations factuelles
    - **realtime**: Données en temps réel
    - **comparison**: Comparer des options
    - **recommendation**: Obtenir des conseils
    - **action**: Effectuer une action
    - **exploration**: Découvrir/explorer
    - **analysis**: Analyser des données
    """
    return [
        {"intent": "information", "description": "Recherche d'informations factuelles (wiki, livres, définitions)"},
        {"intent": "realtime", "description": "Données en temps réel (prix, météo, actualités)"},
        {"intent": "comparison", "description": "Comparer des options (vs, meilleur, différence)"},
        {"intent": "recommendation", "description": "Obtenir des conseils (dois-je, suggère, avis)"},
        {"intent": "action", "description": "Effectuer une action (traduire, raccourcir, créer)"},
        {"intent": "exploration", "description": "Découvrir/explorer (random, surprends-moi)"},
        {"intent": "analysis", "description": "Analyser des données (tendance, évolution, statistiques)"}
    ]


@router.get("/categories", response_model=Dict[str, List[str]])
async def list_categories():
    """
    📂 LISTE DES CATÉGORIES ET APIS
    
    Retourne le mapping catégories → APIs disponibles:
    - **finance_crypto**: CoinCap, CoinGecko
    - **news**: NewsAPI, The Guardian
    - **weather**: OpenMeteo, OpenWeatherMap
    - etc.
    """
    return ai_search_engine.category_apis


@router.post("/quick")
async def quick_search(
    query: str = Query(..., description="Requête de recherche"),
    max_sources: int = Query(3, ge=1, le=10, description="Nombre max de sources")
):
    """
    ⚡ RECHERCHE RAPIDE
    
    Version simplifiée pour des réponses rapides.
    Moins de sources mais plus rapide.
    
    **Exemple:**
    ```
    POST /api/ai-search/quick?query=météo Paris&max_sources=2
    ```
    """
    try:
        start_time = time.time()
        
        # Analyse rapide
        analysis = await ai_search_engine.analyze_query(query)
        
        # Limiter les catégories
        analysis["categories"] = analysis["categories"][:max_sources]
        
        # Créer et exécuter le plan
        plan = await ai_search_engine.create_search_plan(query, analysis)
        plan.apis_to_call = plan.apis_to_call[:max_sources]
        
        raw_results = await ai_search_engine.execute_search(plan)
        result = await ai_search_engine.synthesize_results(query, plan, raw_results)
        
        execution_time = (time.time() - start_time) * 1000
        
        return {
            "query": query,
            "intent": result.intent,
            "synthesis": result.ai_synthesis,
            "recommendations": result.ai_recommendations[:2],
            "sources": result.sources_count,
            "execution_time_ms": round(execution_time, 2)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/examples")
async def get_examples():
    """
    [NOTE] EXEMPLES DE REQUÊTES
    
    Exemples de requêtes pour tester le moteur de recherche IA:
    """
    return {
        "information": [
            "Qu'est-ce que Bitcoin?",
            "Histoire de la France",
            "Comment fonctionne l'intelligence artificielle?"
        ],
        "realtime": [
            "Prix du Bitcoin aujourd'hui",
            "Météo à Paris maintenant",
            "Dernières actualités tech"
        ],
        "comparison": [
            "Bitcoin vs Ethereum",
            "Python ou JavaScript pour le web?",
            "Meilleur framework frontend 2024"
        ],
        "recommendation": [
            "Dois-je investir dans les crypto?",
            "Quel livre lire sur l'IA?",
            "Conseils pour apprendre Python"
        ],
        "action": [
            "Traduire 'Hello World' en français",
            "Raccourcir cette URL: https://example.com/very-long-url",
            "Générer des données de test"
        ],
        "exploration": [
            "Une citation inspirante",
            "Découvrir un pays au hasard",
            "Image aléatoire"
        ],
        "analysis": [
            "Tendance du Bitcoin cette semaine",
            "Évolution des cryptomonnaies",
            "Analyse du marché tech"
        ]
    }






