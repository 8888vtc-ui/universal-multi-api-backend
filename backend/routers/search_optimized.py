"""
Endpoint de recherche optimisée avec regroupement intelligent
Utilise la stratégie de regroupement pour optimiser les performances
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional, Dict, Any, List, Tuple
from pydantic import BaseModel
from services.search_optimizer import (
    search_optimizer,
    APICategory,
    SearchStrategy
)
from services.cache import cache_service
import asyncio
import time
import httpx

router = APIRouter(prefix="/api/search/optimized", tags=["search"])

# Base URL pour les appels internes
BASE_URL = "http://localhost:8000"


class OptimizedSearchRequest(BaseModel):
    """Requête pour recherche optimisée"""
    query: str
    categories: Optional[List[str]] = None
    max_results_per_category: int = 10
    use_cache: bool = True


class OptimizedSearchResponse(BaseModel):
    """Réponse de recherche optimisée"""
    query: str
    strategy: Dict[str, Any]
    results: Dict[str, Any]
    performance: Dict[str, Any]
    cached: bool = False


# Mapping catégorie → endpoint API
CATEGORY_ENDPOINTS = {
    "finance_crypto": [
        {"name": "coincap", "endpoint": "/api/coincap/assets", "params": {"limit": 10}},
    ],
    "finance_stocks": [
        {"name": "yahoo", "endpoint": "/api/finance/stock/quote/AAPL", "params": {}},
    ],
    "news": [
        {"name": "news", "endpoint": "/api/news/headlines", "params": {"country": "us", "limit": 5}},
    ],
    "weather": [
        {"name": "weather", "endpoint": "/api/weather/current", "params": {"city": "Paris"}},
    ],
    "wikipedia": [
        {"name": "wikipedia", "endpoint": "/api/wikipedia/search", "params": {"limit": 5}},
    ],
    "books": [
        {"name": "books", "endpoint": "/api/books/search", "params": {"limit": 5}},
    ],
    "countries": [
        {"name": "countries", "endpoint": "/api/countries/all", "params": {}},
    ],
    "quotes": [
        {"name": "quotes", "endpoint": "/api/quotes/random", "params": {}},
        {"name": "advice", "endpoint": "/api/quotes/advice/random", "params": {}},
    ],
    "github": [
        {"name": "github", "endpoint": "/api/github/search/repos", "params": {"limit": 5}},
    ],
    "images": [
        {"name": "lorempicsum", "endpoint": "/api/lorempicsum/list", "params": {"limit": 5}},
    ],
    "test_data": [
        {"name": "jsonplaceholder", "endpoint": "/api/jsonplaceholder/posts", "params": {"limit": 5}},
        {"name": "randomuser", "endpoint": "/api/randomuser/users", "params": {"count": 3}},
        {"name": "fakestore", "endpoint": "/api/fakestore/products", "params": {"limit": 5}},
    ],
    "utilities": [
        {"name": "worldtime", "endpoint": "/api/worldtime/timezones", "params": {}},
    ],
    "ip_geolocation": [
        {"name": "ip", "endpoint": "/api/ip/my-ip", "params": {}},
    ],
}


async def _fetch_api(
    client: httpx.AsyncClient,
    api_config: Dict[str, Any],
    query: str
) -> Tuple[str, Dict[str, Any]]:
    """Fetch une API individuelle"""
    try:
        endpoint = api_config["endpoint"]
        params = api_config.get("params", {}).copy()
        
        # Ajouter la query si l'endpoint le supporte
        if "search" in endpoint or "query" in str(params):
            params["query"] = query
        
        response = await client.get(
            f"{BASE_URL}{endpoint}",
            params=params,
            timeout=10.0
        )
        
        if response.status_code == 200:
            return api_config["name"], {
                "success": True,
                "data": response.json(),
                "status": response.status_code
            }
        else:
            return api_config["name"], {
                "success": False,
                "error": f"Status {response.status_code}",
                "status": response.status_code
            }
    except httpx.TimeoutException:
        return api_config["name"], {"success": False, "error": "Timeout"}
    except Exception as e:
        return api_config["name"], {"success": False, "error": str(e)[:100]}


async def _execute_group_search(
    group,
    query: str,
    max_results: int
) -> Dict[str, Any]:
    """
    Exécute les recherches pour un groupe d'APIs
    
    Args:
        group: APIGroup à exécuter
        query: Requête de recherche
        max_results: Nombre maximum de résultats
        
    Returns:
        Résultats du groupe avec données réelles
    """
    category_value = group.category.value
    api_configs = CATEGORY_ENDPOINTS.get(category_value, [])
    
    if not api_configs:
        return {
            "category": category_value,
            "apis_used": [],
            "results": [],
            "count": 0,
            "error": "No APIs configured for this category"
        }
    
    results = []
    apis_used = []
    
    async with httpx.AsyncClient() as client:
        # Exécuter en parallèle si le groupe le permet
        if group.parallel_execution and len(api_configs) > 1:
            tasks = [_fetch_api(client, config, query) for config in api_configs[:3]]
            api_results = await asyncio.gather(*tasks, return_exceptions=True)
            
            for result in api_results:
                if isinstance(result, tuple):
                    api_name, api_data = result
                    apis_used.append(api_name)
                    if api_data.get("success"):
                        results.append({
                            "source": api_name,
                            "data": api_data.get("data")
                        })
        else:
            # Exécution séquentielle avec fallback
            for config in api_configs[:2]:
                api_name, api_data = await _fetch_api(client, config, query)
                apis_used.append(api_name)
                if api_data.get("success"):
                    results.append({
                        "source": api_name,
                        "data": api_data.get("data")
                    })
                    if not group.fallback_enabled:
                        break  # Premier succès suffit
    
    return {
        "category": category_value,
        "apis_used": apis_used,
        "results": results,
        "count": len(results)
    }


@router.post("/search", response_model=OptimizedSearchResponse)
async def optimized_search(request: OptimizedSearchRequest):
    """
    🔍 RECHERCHE OPTIMISÉE AVEC REGROUPEMENT INTELLIGENT
    
    Recherche intelligente qui :
    - Détecte automatiquement les catégories pertinentes
    - Regroupe les APIs par catégorie pour optimisation
    - Utilise le cache intelligent par catégorie
    - Priorise les APIs les plus rapides
    - Exécute les recherches en parallèle quand possible
    
    **Avantages** :
    - ⚡ Plus rapide grâce au regroupement
    - 💾 Cache optimisé par catégorie
    - 🎯 Résultats plus pertinents
    - 📊 Métriques de performance détaillées
    """
    query = request.query
    categories = request.categories
    max_results = request.max_results_per_category
    use_cache = request.use_cache
    
    start_time = time.time()
    
    # Créer la stratégie de recherche
    strategy = search_optimizer.create_search_strategy(
        query=query,
        categories=categories,
        max_results=max_results
    )
    
    # Vérifier le cache si activé
    if use_cache:
        cached_result = search_optimizer.get_cached_result(strategy.cache_key)
        if cached_result:
            cached_result["performance"]["cached"] = True
            cached_result["performance"]["total_time_ms"] = (time.time() - start_time) * 1000
            return OptimizedSearchResponse(**cached_result)
    
    # Exécuter les recherches selon la stratégie
    results = {}
    execution_times = {}
    
    # Exécuter tous les groupes en parallèle
    async def execute_group_with_timing(group):
        category_start = time.time()
        try:
            group_results = await _execute_group_search(
                group=group,
                query=query,
                max_results=max_results
            )
            execution_time = (time.time() - category_start) * 1000
            return group.category.value, group_results, execution_time
        except Exception as e:
            execution_time = (time.time() - category_start) * 1000
            return group.category.value, {"error": str(e), "results": []}, execution_time
    
    # Exécuter tous les groupes en parallèle
    if strategy.api_groups:
        tasks = [execute_group_with_timing(group) for group in strategy.api_groups]
        group_results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for result in group_results:
            if isinstance(result, tuple):
                category_name, group_data, exec_time = result
                results[category_name] = group_data
                execution_times[category_name] = exec_time
    
    total_time = (time.time() - start_time) * 1000
    
    # Compter les résultats
    total_results = sum(
        r.get("count", 0) if isinstance(r, dict) else 0 
        for r in results.values()
    )
    
    # Préparer la réponse
    response_data = {
        "query": query,
        "strategy": {
            "detected_categories": [cat.value for cat in strategy.detected_categories],
            "api_groups_count": len(strategy.api_groups),
            "priority_apis": strategy.priority_apis,
            "estimated_time_ms": strategy.estimated_time_ms,
            "cache_key": strategy.cache_key
        },
        "results": results,
        "performance": {
            "total_time_ms": round(total_time, 2),
            "estimated_time_ms": strategy.estimated_time_ms,
            "categories_searched": len(results),
            "total_results": total_results,
            "execution_times": {k: round(v, 2) for k, v in execution_times.items()},
            "cached": False
        },
        "cached": False
    }
    
    # Mettre en cache avec TTL optimisé
    if use_cache and strategy.api_groups:
        min_ttl = min(group.cache_ttl for group in strategy.api_groups)
        search_optimizer.set_cached_result(
            strategy.cache_key,
            response_data,
            ttl=min_ttl
        )
    
    return OptimizedSearchResponse(**response_data)


@router.get("/categories", response_model=List[Dict[str, Any]])
async def get_categories():
    """
    📋 Liste toutes les catégories disponibles avec leurs informations
    
    Retourne la liste complète des catégories d'APIs avec :
    - APIs disponibles
    - Ordre de priorité
    - Configuration de cache
    - Stratégie d'exécution
    """
    categories_info = []
    for category in APICategory:
        info = search_optimizer.get_category_info(category)
        if info:
            # Ajouter les endpoints configurés
            info["endpoints_configured"] = len(CATEGORY_ENDPOINTS.get(category.value, []))
            categories_info.append(info)
    
    return categories_info


@router.get("/detect", response_model=Dict[str, Any])
async def detect_categories(
    query: str = Query(..., description="Requête pour détecter les catégories")
):
    """
    🎯 Détecte les catégories pertinentes pour une requête
    
    Analyse la requête et retourne :
    - Catégories détectées (triées par pertinence)
    - Score de pertinence pour chaque catégorie
    - APIs recommandées pour chaque catégorie
    """
    categories = search_optimizer.detect_categories(query)
    
    result = {
        "query": query,
        "detected_categories": [cat.value for cat in categories],
        "categories_info": []
    }
    
    for category in categories:
        info = search_optimizer.get_category_info(category)
        if info:
            info["endpoints_configured"] = len(CATEGORY_ENDPOINTS.get(category.value, []))
            result["categories_info"].append(info)
    
    return result


@router.get("/strategy", response_model=Dict[str, Any])
async def get_search_strategy(
    query: str = Query(..., description="Requête de recherche"),
    categories: Optional[str] = Query(None, description="Catégories séparées par virgule"),
    max_results: int = Query(10, ge=1, le=50)
):
    """
    🧠 Génère une stratégie de recherche optimisée
    
    Retourne la stratégie complète sans exécuter les recherches :
    - Catégories détectées
    - Groupes d'APIs
    - Temps estimé
    - Clé de cache
    - APIs prioritaires
    """
    category_list = categories.split(",") if categories else None
    
    strategy = search_optimizer.create_search_strategy(
        query=query,
        categories=category_list,
        max_results=max_results
    )
    
    return {
        "query": strategy.query,
        "detected_categories": [cat.value for cat in strategy.detected_categories],
        "api_groups": [
            {
                "category": group.category.value,
                "apis": group.apis,
                "priority_order": group.priority_order,
                "cache_ttl": group.cache_ttl,
                "parallel_execution": group.parallel_execution,
                "max_results": group.max_results,
                "endpoints_configured": len(CATEGORY_ENDPOINTS.get(group.category.value, []))
            }
            for group in strategy.api_groups
        ],
        "cache_key": strategy.cache_key,
        "estimated_time_ms": strategy.estimated_time_ms,
        "priority_apis": strategy.priority_apis
    }


@router.get("/test-category/{category}")
async def test_category(
    category: str,
    query: str = Query("test", description="Requête de test")
):
    """
    🧪 Teste une catégorie spécifique
    
    Exécute les APIs d'une catégorie et retourne les résultats bruts.
    Utile pour le debugging.
    """
    api_configs = CATEGORY_ENDPOINTS.get(category, [])
    
    if not api_configs:
        raise HTTPException(
            status_code=404,
            detail=f"Category '{category}' not found or has no endpoints configured"
        )
    
    results = []
    async with httpx.AsyncClient() as client:
        for config in api_configs:
            api_name, api_data = await _fetch_api(client, config, query)
            results.append({
                "api": api_name,
                "endpoint": config["endpoint"],
                "result": api_data
            })
    
    return {
        "category": category,
        "query": query,
        "apis_tested": len(api_configs),
        "results": results
    }
