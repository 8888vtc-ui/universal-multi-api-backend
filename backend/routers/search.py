"""
Universal Search Engine
Moteur de recherche unifié qui agrège TOUTES les APIs disponibles
Test et intégration multiple APIs en un seul endpoint
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional, Dict, Any, List
from pydantic import BaseModel
from services.ai_router import ai_router
from services.cache import cache_service
import asyncio
import re
import hashlib
import json

# Import all routers
from services.external_apis.weather import WeatherRouter
from services.external_apis.geocoding import GeocodingRouter
from services.external_apis.news import NewsRouter
from services.external_apis.translation import TranslationRouter
from services.external_apis.nutrition import NutritionRouter
from services.external_apis.media import MediaRouter
from services.external_apis.space import SpaceRouter
from services.external_apis.sports import SportsRouter
from services.external_apis import coingecko, yahoo_finance, alphavantage
from services.external_apis.entertainment import tmdb

router = APIRouter(prefix="/api/search", tags=["search"])

# Initialize all routers
weather_router = WeatherRouter()
geocoding_router = GeocodingRouter()
news_router = NewsRouter()
translation_router = TranslationRouter()
nutrition_router = NutritionRouter()
media_router = MediaRouter()
space_router = SpaceRouter()
sports_router = SportsRouter()


class SearchRequest(BaseModel):
    """Request for universal search"""
    query: str
    categories: Optional[List[str]] = None  # ["finance", "news", "weather", etc.]
    max_results_per_category: int = 5
    language: str = "fr"


class SearchResult(BaseModel):
    """Single search result"""
    category: str
    title: str
    content: Any
    source: str
    relevance_score: float
    url: Optional[str] = None


class SearchResponse(BaseModel):
    """Complete search response"""
    query: str
    total_results: int
    categories_searched: List[str]
    results: Dict[str, List[SearchResult]]
    ai_summary: Optional[str] = None
    suggested_queries: List[str] = []
    performance: Optional[Dict[str, Any]] = None  # Métriques de performance


def calculate_relevance_score(query: str, result_title: str, result_content: Any, category: str) -> float:
    """
    Calcule un score de pertinence amélioré pour un résultat
    Score basé sur :
    - Présence des mots-clés dans le titre (poids fort)
    - Présence dans le contenu (poids moyen)
    - Catégorie détectée (bonus)
    """
    query_words = set(query.lower().split())
    title_lower = result_title.lower()
    content_str = str(result_content).lower() if result_content else ""
    
    # Score de base
    score = 0.5
    
    # Bonus pour mots dans le titre (poids 0.3 par mot)
    title_matches = sum(1 for word in query_words if word in title_lower)
    score += min(title_matches * 0.3, 0.9)
    
    # Bonus pour mots dans le contenu (poids 0.1 par mot)
    content_matches = sum(1 for word in query_words if word in content_str)
    score += min(content_matches * 0.1, 0.3)
    
    # Bonus si catégorie correspond à l'intention détectée
    intents = detect_search_intent(query)
    if intents.get(category, False):
        score += 0.1
    
    # Normaliser entre 0 et 1
    return min(score, 1.0)


def detect_search_intent(query: str) -> Dict[str, bool]:
    """
    Détecte l'intention de recherche pour router vers les bonnes APIs
    """
    query_lower = query.lower()
    
    intents = {
        "finance": any(word in query_lower for word in [
            "bitcoin", "crypto", "btc", "eth", "prix", "cours", "bourse", 
            "action", "stock", "market", "trading", "investissement"
        ]),
        "news": any(word in query_lower for word in [
            "actualité", "news", "nouvelle", "événement", "évènement", 
            "breaking", "info", "information"
        ]),
        "weather": any(word in query_lower for word in [
            "météo", "weather", "température", "pluie", "soleil", "vent",
            "prévision", "forecast", "climat"
        ]),
        "location": any(word in query_lower for word in [
            "où", "adresse", "lieu", "ville", "pays", "localisation",
            "géolocalisation", "coordonnées", "map"
        ]),
        "medical": any(word in query_lower for word in [
            "médical", "santé", "maladie", "symptôme", "médicament", 
            "traitement", "recherche médicale", "pubmed"
        ]),
        "entertainment": any(word in query_lower for word in [
            "film", "movie", "série", "restaurant", "musique", "music",
            "spotify", "cinéma", "divertissement"
        ]),
        "nutrition": any(word in query_lower for word in [
            "recette", "cuisine", "aliment", "nutrition", "calorie",
            "repas", "ingrédient", "food"
        ]),
        "space": any(word in query_lower for word in [
            "nasa", "espace", "astronomie", "planète", "mars", "lune",
            "astéroïde", "galaxie", "telescope"
        ]),
        "sports": any(word in query_lower for word in [
            "football", "sport", "match", "équipe", "championnat",
            "ligue", "foot", "soccer"
        ]),
        "media": any(word in query_lower for word in [
            "photo", "image", "vidéo", "picture", "visual"
        ]),
        "translation": any(word in query_lower for word in [
            "traduire", "translation", "langue", "language", "traduction"
        ])
    }
    
    return intents


async def search_finance(query: str, max_results: int = 5) -> List[SearchResult]:
    """Recherche dans les APIs finance"""
    results = []
    try:
        # Détecter crypto ou stock
        if any(word in query.lower() for word in ["bitcoin", "btc", "crypto", "ethereum", "eth"]):
            # Recherche crypto
            coin_id = "bitcoin" if "bitcoin" in query.lower() or "btc" in query.lower() else "ethereum"
            try:
                price_data = await coingecko.get_crypto_price(coin_id, "usd")
                title = f"Prix {coin_id.upper()}"
                results.append(SearchResult(
                    category="finance",
                    title=title,
                    content=price_data,
                    source="CoinGecko",
                    relevance_score=calculate_relevance_score(query, title, price_data, "finance"),
                    url=f"https://www.coingecko.com/en/coins/{coin_id}"
                ))
            except:
                pass
            
            # Trending cryptos
            try:
                trending = await coingecko.get_trending()
                results.append(SearchResult(
                    category="finance",
                    title="Cryptos tendance",
                    content=trending,
                    source="CoinGecko",
                    relevance_score=0.7
                ))
            except:
                pass
        else:
            # Recherche stock
            # Extraire symbole si présent (ex: "AAPL", "TSLA")
            symbols = re.findall(r'\b[A-Z]{1,5}\b', query.upper())
            if symbols:
                for symbol in symbols[:max_results]:
                    try:
                        # Essayer Alpha Vantage d'abord
                        if alphavantage.available:
                            stock_data = await alphavantage.get_stock_quote(symbol)
                        else:
                            stock_data = await yahoo_finance.get_stock_info(symbol)
                        results.append(SearchResult(
                            category="finance",
                            title=f"Action {symbol}",
                            content=stock_data,
                            source="Yahoo Finance" if not alphavantage.available else "Alpha Vantage",
                            relevance_score=0.9
                        ))
                    except:
                        pass
    except Exception as e:
        pass
    
    return results[:max_results]


async def search_news(query: str, language: str, max_results: int = 5) -> List[SearchResult]:
    """Recherche dans les APIs news"""
    results = []
    try:
        news_data = await news_router.search(query, language, max_results)
        articles = news_data.get("articles", [])
        
        for article in articles:
            results.append(SearchResult(
                category="news",
                title=article.get("title", ""),
                content={
                    "description": article.get("description"),
                    "publishedAt": article.get("publishedAt"),
                    "source": article.get("source", {}).get("name") if isinstance(article.get("source"), dict) else article.get("source")
                },
                source=article.get("source", {}).get("name", "NewsAPI") if isinstance(article.get("source"), dict) else article.get("source", "NewsAPI"),
                relevance_score=0.8,
                url=article.get("url")
            ))
    except Exception as e:
        pass
    
    return results


async def search_weather(query: str, max_results: int = 5) -> List[SearchResult]:
    """Recherche météo"""
    results = []
    try:
        # D'abord géocoder pour obtenir coordonnées
        geocode_result = await geocoding_router.geocode(query)
        locations = geocode_result.get("results", [])
        
        if locations:
            location = locations[0]
            lat = location.get("latitude")
            lon = location.get("longitude")
            
            # Obtenir météo
            weather_data = await weather_router.get_current_weather(lat, lon)
            
            results.append(SearchResult(
                category="weather",
                title=f"Météo à {location.get('name', query)}",
                content=weather_data,
                source=weather_data.get("provider", "Open-Meteo"),
                relevance_score=0.9
            ))
    except Exception as e:
        pass
    
    return results


async def search_location(query: str, max_results: int = 5) -> List[SearchResult]:
    """Recherche de localisation"""
    results = []
    try:
        geocode_result = await geocoding_router.geocode(query)
        locations = geocode_result.get("results", [])
        
        for loc in locations[:max_results]:
            results.append(SearchResult(
                category="geocoding",
                title=loc.get("name", ""),
                content={
                    "latitude": loc.get("latitude"),
                    "longitude": loc.get("longitude"),
                    "country": loc.get("country"),
                    "admin1": loc.get("admin1")
                },
                source=geocode_result.get("provider", "Open-Meteo Geocoding"),
                relevance_score=0.85
            ))
    except Exception as e:
        pass
    
    return results


async def search_medical(query: str, max_results: int = 5) -> List[SearchResult]:
    """Recherche médicale"""
    results = []
    try:
        # Utiliser directement les services medical
        from services.external_apis import pubmed
        
        # Recherche PubMed
        pubmed_results = await pubmed.search_articles(query, max_results)
        articles = pubmed_results.get("articles", [])
        
        for article in articles[:max_results]:
            results.append(SearchResult(
                category="medical",
                title=article.get("title", ""),
                content={
                    "authors": article.get("authors"),
                    "journal": article.get("journal"),
                    "pub_date": article.get("pub_date"),
                    "abstract": article.get("abstract", "")[:200] if article.get("abstract") else ""
                },
                source="PubMed",
                relevance_score=0.8,
                url=article.get("url")
            ))
    except Exception as e:
        pass
    
    return results


async def search_entertainment(query: str, max_results: int = 5) -> List[SearchResult]:
    """Recherche entertainment"""
    results = []
    try:
        # Recherche films
        movies = await tmdb.search_movies(query)
        movie_results = movies.get("results", [])
        
        for movie in movie_results[:max_results]:
            results.append(SearchResult(
                category="entertainment",
                title=movie.get("title", ""),
                content={
                    "overview": movie.get("overview"),
                    "release_date": movie.get("release_date"),
                    "rating": movie.get("vote_average")
                },
                source="TMDB",
                relevance_score=0.8
            ))
    except Exception as e:
        pass
    
    return results


async def search_nutrition(query: str, max_results: int = 5) -> List[SearchResult]:
    """Recherche nutrition"""
    results = []
    try:
        # Recherche recettes
        recipes = await nutrition_router.search_recipes(query, max_results)
        recipe_list = recipes.get("results", [])
        
        for recipe in recipe_list[:max_results]:
            results.append(SearchResult(
                category="nutrition",
                title=recipe.get("title", ""),
                content={
                    "calories": recipe.get("nutrition", {}).get("calories") if isinstance(recipe.get("nutrition"), dict) else None,
                    "servings": recipe.get("servings"),
                    "ready_in_minutes": recipe.get("ready_in_minutes")
                },
                source=recipes.get("provider", "Spoonacular"),
                relevance_score=0.75,
                url=recipe.get("sourceUrl")
            ))
    except Exception as e:
        pass
    
    return results


async def search_space(query: str, max_results: int = 5) -> List[SearchResult]:
    """Recherche espace"""
    results = []
    try:
        # Image du jour NASA
        if "image" in query.lower() or "photo" in query.lower() or "picture" in query.lower():
            apod = await space_router.get_apod()
            results.append(SearchResult(
                category="space",
                title=apod.get("title", "NASA Image of the Day"),
                content={
                    "explanation": apod.get("explanation", "")[:200],
                    "date": apod.get("date"),
                    "media_type": apod.get("media_type")
                },
                source="NASA APOD",
                relevance_score=0.9,
                url=apod.get("url")
            ))
    except Exception as e:
        pass
    
    return results


async def search_sports(query: str, max_results: int = 5) -> List[SearchResult]:
    """Recherche sports"""
    results = []
    try:
        # Matchs en direct
        live_matches = await sports_router.get_live_matches()
        matches = live_matches.get("matches", []) or live_matches.get("response", [])
        
        for match in matches[:max_results]:
            # Gérer différents formats de réponse
            if isinstance(match, dict):
                home = match.get("home_team") or match.get("teams", {}).get("home", {}).get("name", "Home")
                away = match.get("away_team") or match.get("teams", {}).get("away", {}).get("name", "Away")
                
                results.append(SearchResult(
                    category="sports",
                    title=f"{home} vs {away}",
                    content={
                        "status": match.get("status") or match.get("fixture", {}).get("status", {}).get("long"),
                        "score": match.get("score") or match.get("goals"),
                        "league": match.get("league") or match.get("league", {}).get("name")
                    },
                    source="API-Football",
                    relevance_score=0.8
                ))
    except Exception as e:
        pass
    
    return results


async def search_media(query: str, max_results: int = 5) -> List[SearchResult]:
    """Recherche médias"""
    results = []
    try:
        # Recherche photos
        photos = await media_router.search_photos(query, max_results)
        photo_list = photos.get("results", [])
        
        for photo in photo_list[:max_results]:
            results.append(SearchResult(
                category="media",
                title=photo.get("description", query) or photo.get("alt_description", query),
                content={
                    "width": photo.get("width"),
                    "height": photo.get("height"),
                    "color": photo.get("color")
                },
                source=photos.get("provider", "Unsplash"),
                relevance_score=0.75,
                url=photo.get("urls", {}).get("regular") if isinstance(photo.get("urls"), dict) else photo.get("url")
            ))
    except Exception as e:
        pass
    
    return results


def _generate_cache_key(query: str, categories: Optional[List[str]], max_results: int, language: str) -> str:
    """Génère une clé de cache unique pour une requête"""
    cache_data = json.dumps({
        "query": query.lower().strip(),
        "categories": sorted(categories) if categories else None,
        "max_results": max_results,
        "language": language
    }, sort_keys=True)
    return hashlib.md5(cache_data.encode()).hexdigest()


@router.post("/universal", response_model=SearchResponse)
async def universal_search(request: SearchRequest):
    """
    🔍 MOTEUR DE RECHERCHE UNIVERSEL
    
    Recherche intelligente dans TOUTES les APIs disponibles :
    - Finance (crypto, stocks)
    - Actualités
    - Météo
    - Géolocalisation
    - Médical (PubMed)
    - Entertainment (films, restaurants)
    - Nutrition (recettes)
    - Espace (NASA)
    - Sports
    - Médias (photos)
    
    Les recherches sont exécutées en parallèle pour une réponse ultra-rapide !
    Cache Redis activé pour améliorer les performances (TTL: 5 minutes).
    """
    query = request.query
    categories = request.categories
    max_results = request.max_results_per_category
    language = request.language
    
    # Vérifier le cache Redis
    cache_key = _generate_cache_key(query, categories, max_results, language)
    cached_result = cache_service.get("search", cache_key)
    
    if cached_result:
        # Retourner résultat en cache avec flag cached=True
        cached_result["performance"] = cached_result.get("performance", {})
        cached_result["performance"]["cached"] = True
        cached_result["performance"]["total_time_ms"] = 0.1  # Très rapide depuis cache
        return SearchResponse(**cached_result)
    
    # Détecter les intentions si catégories non spécifiées
    if not categories:
        intents = detect_search_intent(query)
        categories = [cat for cat, should_search in intents.items() if should_search]
        
        # Si aucune intention détectée, chercher partout
        if not categories:
            categories = ["finance", "news", "weather", "location", "medical", 
                          "entertainment", "nutrition", "space", "sports", "media"]
    
    # Préparer toutes les recherches en parallèle
    search_tasks = []
    
    if "finance" in categories:
        search_tasks.append(("finance", search_finance(query, max_results)))
    
    if "news" in categories:
        search_tasks.append(("news", search_news(query, language, max_results)))
    
    if "weather" in categories:
        search_tasks.append(("weather", search_weather(query, max_results)))
    
    if "location" in categories or "geocoding" in categories:
        search_tasks.append(("geocoding", search_location(query, max_results)))
    
    if "medical" in categories:
        search_tasks.append(("medical", search_medical(query, max_results)))
    
    if "entertainment" in categories:
        search_tasks.append(("entertainment", search_entertainment(query, max_results)))
    
    if "nutrition" in categories:
        search_tasks.append(("nutrition", search_nutrition(query, max_results)))
    
    if "space" in categories:
        search_tasks.append(("space", search_space(query, max_results)))
    
    if "sports" in categories:
        search_tasks.append(("sports", search_sports(query, max_results)))
    
    if "media" in categories:
        search_tasks.append(("media", search_media(query, max_results)))
    
    # Exécuter toutes les recherches en parallèle avec timing
    import time
    start_time = time.time()
    
    results_dict = {}
    if search_tasks:
        tasks = [task for _, task in search_tasks]
        category_names = [cat for cat, _ in search_tasks]
        
        search_results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for category, results in zip(category_names, search_results):
            if isinstance(results, Exception):
                results_dict[category] = []
            else:
                # Trier par score de pertinence décroissant
                results.sort(key=lambda x: x.relevance_score, reverse=True)
                results_dict[category] = results
    
    total_time = time.time() - start_time
    
    # Compter le total
    total_results = sum(len(results) for results in results_dict.values())
    
    # Générer un résumé IA si on a des résultats
    ai_summary = None
    if total_results > 0:
        try:
            summary_prompt = f"""
            Résume les résultats de recherche suivants pour la requête : "{query}"
            
            Catégories trouvées : {', '.join(results_dict.keys())}
            Nombre total de résultats : {total_results}
            
            Donne un résumé concis en français de ce qui a été trouvé.
            """
            ai_response = await ai_router.chat(summary_prompt, max_tokens=200)
            ai_summary = ai_response.get("content", "")
        except:
            pass
    
    # Générer des suggestions de requêtes
    suggested_queries = []
    if total_results == 0:
        suggested_queries = [
            f"{query} actualités",
            f"{query} prix",
            f"{query} météo",
            f"informations sur {query}"
        ]
    
    # Créer la réponse avec métriques de performance
    response = SearchResponse(
        query=query,
        total_results=total_results,
        categories_searched=list(results_dict.keys()),
        results={cat: [r.dict() for r in results] for cat, results in results_dict.items()},
        ai_summary=ai_summary,
        suggested_queries=suggested_queries,
        performance={
            "total_time_ms": round(total_time * 1000, 2),
            "categories_count": len(results_dict),
            "cached": False
        }
    )
    
    # Mettre en cache (TTL: 5 minutes = 300 secondes)
    cache_service.set("search", cache_key, response.dict(), ttl=300)
    
    return response


@router.get("/quick")
async def quick_search(
    q: str = Query(..., description="Query de recherche"),
    categories: Optional[str] = Query(None, description="Catégories séparées par virgule (finance,news,weather)"),
    limit: int = Query(5, ge=1, le=20, description="Résultats par catégorie")
):
    """
    🔍 Recherche rapide (GET)
    Version simplifiée du moteur de recherche
    """
    cat_list = categories.split(",") if categories else None
    request = SearchRequest(
        query=q,
        categories=cat_list,
        max_results_per_category=limit
    )
    
    result = await universal_search(request)
    return result


@router.get("/categories")
async def get_search_categories():
    """
    Liste toutes les catégories de recherche disponibles
    """
    return {
        "categories": [
            {
                "id": "finance",
                "name": "Finance",
                "description": "Cryptomonnaies, actions, marchés financiers",
                "keywords": ["bitcoin", "crypto", "stock", "bourse", "prix"]
            },
            {
                "id": "news",
                "name": "Actualités",
                "description": "Articles de presse, breaking news",
                "keywords": ["actualité", "news", "nouvelle", "événement"]
            },
            {
                "id": "weather",
                "name": "Météo",
                "description": "Conditions météorologiques, prévisions",
                "keywords": ["météo", "weather", "température", "pluie"]
            },
            {
                "id": "geocoding",
                "name": "Géolocalisation",
                "description": "Recherche de lieux, adresses, coordonnées",
                "keywords": ["lieu", "adresse", "ville", "localisation"]
            },
            {
                "id": "medical",
                "name": "Médical",
                "description": "Recherche médicale, PubMed, médicaments",
                "keywords": ["santé", "médical", "médicament", "traitement"]
            },
            {
                "id": "entertainment",
                "name": "Divertissement",
                "description": "Films, séries, restaurants, musique",
                "keywords": ["film", "restaurant", "musique", "cinéma"]
            },
            {
                "id": "nutrition",
                "name": "Nutrition",
                "description": "Recettes, aliments, calories",
                "keywords": ["recette", "cuisine", "aliment", "nutrition"]
            },
            {
                "id": "space",
                "name": "Espace",
                "description": "NASA, astronomie, images spatiales",
                "keywords": ["nasa", "espace", "astronomie", "planète"]
            },
            {
                "id": "sports",
                "name": "Sports",
                "description": "Matchs en direct, classements",
                "keywords": ["football", "sport", "match", "équipe"]
            },
            {
                "id": "media",
                "name": "Médias",
                "description": "Photos, images, vidéos",
                "keywords": ["photo", "image", "vidéo", "visual"]
            }
        ],
        "total": 10
    }

