"""
Moteur de Recherche Intelligent IA + Data
Combine l'intelligence artificielle avec la recherche multi-sources
Approche RAG (Retrieval Augmented Generation)
"""
import asyncio
import time
import json
import hashlib
import logging
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import httpx

from services.ai_router import ai_router
from services.cache import cache_service
from services.ai_response_validator import ai_response_validator

logger = logging.getLogger(__name__)


class SearchIntent(Enum):
    """Types d'intentions de recherche détectées par l'IA"""
    INFORMATION = "information"      # Recherche d'info factuelle
    REALTIME = "realtime"            # Données temps réel
    COMPARISON = "comparison"        # Comparer des options
    RECOMMENDATION = "recommendation" # Obtenir des conseils
    ACTION = "action"                # Effectuer une action
    EXPLORATION = "exploration"      # Découvrir/explorer
    ANALYSIS = "analysis"            # Analyser des données


class DataFreshness(Enum):
    """Fraîcheur des données requises"""
    LIVE = "live"       # < 1 minute
    FRESH = "fresh"     # < 30 minutes
    RECENT = "recent"   # < 24 heures
    STABLE = "stable"   # Données stables


@dataclass
class SearchPlan:
    """Plan de recherche généré par l'IA"""
    query: str
    intent: SearchIntent
    entities: List[str]
    categories: List[str]
    apis_to_call: List[str]
    freshness: DataFreshness
    parallel_execution: bool
    expected_sources: int
    ai_synthesis_prompt: str


@dataclass
class SearchResult:
    """Résultat de recherche enrichi par l'IA"""
    query: str
    intent: str
    sources_count: int
    data: Dict[str, Any]
    ai_synthesis: str
    ai_recommendations: List[str]
    confidence_score: float
    execution_time_ms: float
    cached: bool = False


class AISearchEngine:
    """
    Moteur de recherche intelligent combinant IA + Data
    
    Flux:
    1. IA analyse la requête (intention, entités)
    2. Planification intelligente (quelles APIs appeler)
    3. Exécution parallèle des recherches
    4. IA synthétise et enrichit les résultats
    """
    
    def __init__(self):
        self.intent_keywords = self._init_intent_keywords()
        self.category_apis = self._init_category_apis()
        self.api_endpoints = self._init_api_endpoints()
        print("[OK] AI Search Engine initialized")
    
    def _init_intent_keywords(self) -> Dict[SearchIntent, List[str]]:
        """Mots-clés pour détection d'intention"""
        return {
            SearchIntent.INFORMATION: [
                "qu'est-ce que", "what is", "définition", "explain", "c'est quoi",
                "qui est", "who is", "histoire de", "history of", "comment fonctionne"
            ],
            SearchIntent.REALTIME: [
                "prix", "price", "cours", "météo", "weather", "actualité", "news",
                "en ce moment", "maintenant", "today", "live", "temps réel"
            ],
            SearchIntent.COMPARISON: [
                "vs", "versus", "comparaison", "compare", "différence", "meilleur",
                "best", "better", "ou", "or", "lequel", "which"
            ],
            SearchIntent.RECOMMENDATION: [
                "dois-je", "should i", "conseille", "recommend", "suggère", "suggest",
                "que faire", "what to do", "avis", "opinion"
            ],
            SearchIntent.ACTION: [
                "traduire", "translate", "raccourcir", "shorten", "convertir", "convert",
                "générer", "generate", "créer", "create", "envoyer", "send"
            ],
            SearchIntent.EXPLORATION: [
                "découvrir", "discover", "explorer", "explore", "random", "aléatoire",
                "surprends-moi", "surprise me", "nouveauté", "new"
            ],
            SearchIntent.ANALYSIS: [
                "analyse", "analyze", "tendance", "trend", "évolution", "evolution",
                "statistique", "statistics", "performance", "rapport", "report"
            ]
        }
    
    def _init_category_apis(self) -> Dict[str, List[str]]:
        """Mapping catégories → APIs"""
        return {
            "finance_crypto": ["coincap", "coingecko"],
            "finance_stocks": ["yahoo_finance", "alphavantage"],
            "news": ["newsapi", "guardian"],
            "weather": ["openmeteo", "openweathermap"],
            "wikipedia": ["wikipedia"],
            "books": ["google_books"],
            "countries": ["rest_countries"],
            "translation": ["libretranslate", "deepl"],
            "images": ["unsplash", "pexels", "lorempicsum"],
            "quotes": ["quotable", "adviceslip"],
            "test_data": ["jsonplaceholder", "randomuser", "fakestore"],
            "github": ["github"],
            "geolocation": ["nominatim", "ip_geolocation"],
            "time": ["worldtime"],
            "url": ["tinyurl"],
            "medical": ["pubmed"],
            "nutrition": ["usda"],
            "space": ["nasa"],
            "entertainment": ["tmdb", "omdb"]
        }
    
    def _init_api_endpoints(self) -> Dict[str, str]:
        """Mapping API → Endpoint local"""
        return {
            "coincap": "/api/coincap/assets",
            "wikipedia": "/api/wikipedia/search",
            "weather": "/api/weather/current",
            "news": "/api/news/headlines",
            "countries": "/api/countries/name",
            "quotes": "/api/quotes/random",
            "github": "/api/github/search/repos",
            "books": "/api/books/search",
            "translation": "/api/translation/translate",
            "randomuser": "/api/randomuser/users",
            "fakestore": "/api/fakestore/products",
            "jsonplaceholder": "/api/jsonplaceholder/posts",
            "lorempicsum": "/api/lorempicsum/list",
            "worldtime": "/api/worldtime/timezones",
            "tinyurl": "/api/tinyurl/shorten",
            "ip_geolocation": "/api/ip/my-ip"
        }
    
    async def analyze_query(self, query: str) -> Dict[str, Any]:
        """
        Étape 1: L'IA analyse la requête
        Détecte l'intention, les entités et les catégories pertinentes
        """
        # Détection d'intention par mots-clés
        detected_intent = self._detect_intent(query)
        
        # Utiliser l'IA pour une analyse plus fine
        analysis_prompt = f"""Analyse cette requête de recherche et réponds en JSON strict:

Requête: "{query}"

Réponds UNIQUEMENT avec ce format JSON (sans markdown, sans explication):
{{
    "intent": "information|realtime|comparison|recommendation|action|exploration|analysis",
    "entities": ["liste", "des", "entités", "clés"],
    "categories": ["finance_crypto", "news", "weather", "wikipedia", "books", "countries", "quotes", "github", "entertainment", "medical", "nutrition", "space", "translation", "images", "test_data", "geolocation", "time", "url"],
    "freshness": "live|fresh|recent|stable",
    "confidence": 0.0 à 1.0
}}

Choisis les catégories parmi: finance_crypto, finance_stocks, news, weather, wikipedia, books, countries, quotes, github, entertainment, medical, nutrition, space, translation, images, test_data, geolocation, time, url"""

        try:
            ai_response = await ai_router.route(analysis_prompt)
            response_text = ai_response.get("response", "{}")
            
            # Nettoyer la réponse
            response_text = response_text.strip()
            if response_text.startswith("```"):
                response_text = response_text.split("```")[1]
                if response_text.startswith("json"):
                    response_text = response_text[4:]
            
            analysis = json.loads(response_text)
            
            # Valider et enrichir
            return {
                "intent": analysis.get("intent", detected_intent.value),
                "entities": analysis.get("entities", []),
                "categories": analysis.get("categories", [])[:5],  # Max 5 catégories
                "freshness": analysis.get("freshness", "fresh"),
                "confidence": analysis.get("confidence", 0.7),
                "ai_analyzed": True
            }
        except Exception as e:
            # Fallback sur détection par mots-clés
            categories = self._detect_categories(query)
            return {
                "intent": detected_intent.value,
                "entities": query.split()[:5],
                "categories": categories,
                "freshness": "fresh",
                "confidence": 0.5,
                "ai_analyzed": False,
                "error": str(e)
            }
    
    def _detect_intent(self, query: str) -> SearchIntent:
        """Détection d'intention par mots-clés"""
        query_lower = query.lower()
        
        for intent, keywords in self.intent_keywords.items():
            for keyword in keywords:
                if keyword in query_lower:
                    return intent
        
        return SearchIntent.INFORMATION  # Par défaut
    
    def _detect_categories(self, query: str) -> List[str]:
        """Détection de catégories par mots-clés"""
        query_lower = query.lower()
        categories = []
        
        category_keywords = {
            "finance_crypto": ["bitcoin", "crypto", "ethereum", "btc", "eth", "coin"],
            "finance_stocks": ["stock", "action", "bourse", "nasdaq", "trading"],
            "news": ["actualité", "news", "nouvelle", "journal"],
            "weather": ["météo", "weather", "température", "pluie"],
            "wikipedia": ["wiki", "définition", "qu'est-ce", "histoire"],
            "books": ["livre", "book", "auteur", "roman"],
            "countries": ["pays", "country", "capitale", "drapeau"],
            "quotes": ["citation", "quote", "proverbe", "conseil"],
            "github": ["github", "repo", "code", "projet"],
            "entertainment": ["film", "movie", "série", "acteur"]
        }
        
        for category, keywords in category_keywords.items():
            for keyword in keywords:
                if keyword in query_lower:
                    categories.append(category)
                    break
        
        return categories[:5] if categories else ["wikipedia", "news"]
    
    async def create_search_plan(self, query: str, analysis: Dict[str, Any]) -> SearchPlan:
        """
        Étape 2: Créer un plan de recherche optimisé
        """
        intent = SearchIntent(analysis["intent"]) if analysis["intent"] in [e.value for e in SearchIntent] else SearchIntent.INFORMATION
        freshness = DataFreshness(analysis["freshness"]) if analysis["freshness"] in [e.value for e in DataFreshness] else DataFreshness.FRESH
        
        # Déterminer les APIs à appeler
        apis_to_call = []
        for category in analysis["categories"]:
            if category in self.category_apis:
                apis_to_call.extend(self.category_apis[category][:2])  # Max 2 par catégorie
        
        # Limiter à 6 APIs maximum
        apis_to_call = list(dict.fromkeys(apis_to_call))[:6]
        
        # Créer le prompt de synthèse
        synthesis_prompt = self._create_synthesis_prompt(query, intent, analysis["entities"])
        
        return SearchPlan(
            query=query,
            intent=intent,
            entities=analysis["entities"],
            categories=analysis["categories"],
            apis_to_call=apis_to_call,
            freshness=freshness,
            parallel_execution=len(apis_to_call) > 1,
            expected_sources=len(apis_to_call),
            ai_synthesis_prompt=synthesis_prompt
        )
    
    def _create_synthesis_prompt(self, query: str, intent: SearchIntent, entities: List[str]) -> str:
        """Crée le prompt de synthèse adapté à l'intention"""
        prompts = {
            SearchIntent.INFORMATION: f"Synthétise les informations trouvées sur '{query}'. Donne une réponse claire et factuelle.",
            SearchIntent.REALTIME: f"Résume les données actuelles pour '{query}'. Mets en avant les chiffres clés et tendances.",
            SearchIntent.COMPARISON: f"Compare les différentes options trouvées pour '{query}'. Liste les avantages et inconvénients.",
            SearchIntent.RECOMMENDATION: f"Basé sur les données trouvées, donne des recommandations pour '{query}'. Sois pragmatique.",
            SearchIntent.ACTION: f"Explique comment réaliser l'action demandée: '{query}'. Donne des étapes claires.",
            SearchIntent.EXPLORATION: f"Présente les découvertes intéressantes liées à '{query}'. Sois créatif et engageant.",
            SearchIntent.ANALYSIS: f"Analyse les données trouvées pour '{query}'. Identifie les tendances et insights."
        }
        return prompts.get(intent, prompts[SearchIntent.INFORMATION])
    
    async def execute_search(self, plan: SearchPlan) -> Dict[str, Any]:
        """
        Étape 3: Exécuter les recherches en parallèle
        """
        results = {}
        base_url = "http://localhost:8000"
        
        async def fetch_api(api_name: str) -> Tuple[str, Any]:
            """Fetch une API individuelle"""
            try:
                endpoint = self.api_endpoints.get(api_name)
                if not endpoint:
                    return api_name, {"error": "Endpoint not configured"}
                
                async with httpx.AsyncClient(timeout=10.0) as client:
                    # Adapter les paramètres selon l'API
                    params = self._get_api_params(api_name, plan.query, plan.entities)
                    
                    if params.get("method") == "POST":
                        response = await client.post(
                            f"{base_url}{endpoint}",
                            json=params.get("body", {})
                        )
                    else:
                        response = await client.get(
                            f"{base_url}{endpoint}",
                            params=params.get("query", {})
                        )
                    
                    if response.status_code == 200:
                        return api_name, response.json()
                    else:
                        return api_name, {"error": f"Status {response.status_code}"}
            except Exception as e:
                return api_name, {"error": str(e)}
        
        # Exécuter en parallèle
        if plan.parallel_execution and plan.apis_to_call:
            tasks = [fetch_api(api) for api in plan.apis_to_call]
            api_results = await asyncio.gather(*tasks)
            
            for api_name, data in api_results:
                results[api_name] = data
        
        return results
    
    def _get_api_params(self, api_name: str, query: str, entities: List[str]) -> Dict[str, Any]:
        """Génère les paramètres pour chaque API"""
        search_term = entities[0] if entities else query.split()[0]
        
        params_map = {
            "coincap": {"method": "GET", "query": {"limit": 10, "search": search_term}},
            "wikipedia": {"method": "GET", "query": {"query": query, "limit": 3}},
            "quotes": {"method": "GET", "query": {}},
            "countries": {"method": "GET", "query": {}},
            "github": {"method": "GET", "query": {"query": search_term, "limit": 5}},
            "books": {"method": "GET", "query": {"query": query, "limit": 5}},
            "randomuser": {"method": "GET", "query": {"count": 3}},
            "fakestore": {"method": "GET", "query": {"limit": 5}},
            "jsonplaceholder": {"method": "GET", "query": {"limit": 5}},
            "lorempicsum": {"method": "GET", "query": {"limit": 5}},
            "worldtime": {"method": "GET", "query": {}},
        }
        
        return params_map.get(api_name, {"method": "GET", "query": {"query": query}})
    
    async def synthesize_results(
        self,
        query: str,
        plan: SearchPlan,
        raw_results: Dict[str, Any]
    ) -> SearchResult:
        """
        Étape 4: L'IA synthétise et enrichit les résultats
        """
        # Préparer le contexte pour l'IA
        context = self._prepare_context(raw_results)
        
        # Générer la synthèse
        base_synthesis_prompt = f"""{plan.ai_synthesis_prompt}

Données collectées:
{context}

Instructions:
1. Synthétise les informations de manière claire et concise
2. Mets en avant les points clés
3. Si des données manquent, indique-le
4. Termine par 2-3 recommandations ou suggestions
5. Sois précis et factuel, cite tes sources quand possible

Réponds en français, de manière naturelle et utile."""

        # Améliorer le prompt avec le validateur
        synthesis_prompt = ai_response_validator.enhance_system_prompt(
            base_synthesis_prompt,
            query,
            expert_type=None
        )

        try:
            ai_response = await ai_router.route(
                prompt=synthesis_prompt,
                system_prompt="Tu es un expert en synthèse d'informations. Fournis des réponses précises et factuelles."
            )
            synthesis = ai_response.get("response", "Synthèse non disponible")
            
            # Valider la synthèse
            is_valid, validation_details = ai_response_validator.validate_response(
                response=synthesis,
                query=query,
                context=context
            )
            
            # Si la synthèse n'est pas valide, logger et potentiellement améliorer
            if not is_valid:
                logger.warning(f"Invalid synthesis for query '{query}': {validation_details}")
                # Ajouter un avertissement si la confiance est très faible
                if validation_details.get("confidence_score", 1.0) < 0.3:
                    synthesis = f"[WARN] {synthesis}\n\n(Note: Cette synthèse nécessite une vérification supplémentaire)"
            
        except Exception as e:
            logger.error(f"Synthesis error: {e}")
            synthesis = f"Synthèse IA indisponible: {str(e)}"
        
        # Générer des recommandations
        recommendations = await self._generate_recommendations(query, plan.intent, raw_results)
        
        # Calculer le score de confiance
        confidence = self._calculate_confidence(raw_results, plan)
        
        return SearchResult(
            query=query,
            intent=plan.intent.value,
            sources_count=len([r for r in raw_results.values() if "error" not in r]),
            data=raw_results,
            ai_synthesis=synthesis,
            ai_recommendations=recommendations,
            confidence_score=confidence,
            execution_time_ms=0,  # Sera rempli par le caller
            cached=False
        )
    
    def _prepare_context(self, results: Dict[str, Any]) -> str:
        """Prépare le contexte pour l'IA"""
        context_parts = []
        
        for source, data in results.items():
            if "error" in data:
                continue
            
            # Limiter la taille des données
            data_str = json.dumps(data, ensure_ascii=False)[:500]
            context_parts.append(f"[{source}]: {data_str}")
        
        return "\n".join(context_parts) if context_parts else "Aucune donnée disponible"
    
    async def _generate_recommendations(
        self,
        query: str,
        intent: SearchIntent,
        results: Dict[str, Any]
    ) -> List[str]:
        """Génère des recommandations basées sur les résultats"""
        recommendations = []
        
        # Recommandations génériques selon l'intention
        intent_recs = {
            SearchIntent.INFORMATION: [
                "Consultez Wikipedia pour plus de détails",
                "Vérifiez les sources pour confirmer les informations"
            ],
            SearchIntent.REALTIME: [
                "Rafraîchissez régulièrement pour des données à jour",
                "Configurez des alertes pour suivre les changements"
            ],
            SearchIntent.COMPARISON: [
                "Comparez plusieurs sources avant de décider",
                "Considérez vos critères prioritaires"
            ],
            SearchIntent.RECOMMENDATION: [
                "Adaptez les conseils à votre situation",
                "Consultez un expert si nécessaire"
            ]
        }
        
        recommendations = intent_recs.get(intent, ["Explorez les résultats pour plus de détails"])
        
        # Ajouter des recommandations basées sur les sources disponibles
        if "coincap" in results or "coingecko" in results:
            recommendations.append("Suivez les tendances du marché crypto")
        if "wikipedia" in results:
            recommendations.append("Approfondissez sur Wikipedia")
        
        return recommendations[:3]
    
    def _calculate_confidence(self, results: Dict[str, Any], plan: SearchPlan) -> float:
        """Calcule un score de confiance"""
        successful_sources = len([r for r in results.values() if "error" not in r])
        expected_sources = plan.expected_sources
        
        if expected_sources == 0:
            return 0.0
        
        base_score = successful_sources / expected_sources
        
        # Bonus si plusieurs sources concordent
        if successful_sources >= 2:
            base_score += 0.1
        
        return min(base_score, 1.0)
    
    async def search(
        self,
        query: str,
        use_cache: bool = True
    ) -> SearchResult:
        """
        Méthode principale: Recherche intelligente IA + Data
        
        Args:
            query: Requête de recherche
            use_cache: Utiliser le cache
            
        Returns:
            SearchResult enrichi par l'IA
        """
        start_time = time.time()
        
        # Vérifier le cache
        cache_key = f"ai_search:{hashlib.md5(query.encode()).hexdigest()}"
        if use_cache:
            cached = cache_service.get("ai_search", cache_key)
            if cached:
                cached["cached"] = True
                cached["execution_time_ms"] = (time.time() - start_time) * 1000
                return SearchResult(**cached)
        
        # Étape 1: Analyser la requête
        analysis = await self.analyze_query(query)
        
        # Étape 2: Créer le plan de recherche
        plan = await self.create_search_plan(query, analysis)
        
        # Étape 3: Exécuter les recherches
        raw_results = await self.execute_search(plan)
        
        # Étape 4: Synthétiser avec l'IA
        result = await self.synthesize_results(query, plan, raw_results)
        
        # Mettre à jour le temps d'exécution
        result.execution_time_ms = (time.time() - start_time) * 1000
        
        # Mettre en cache
        if use_cache:
            cache_service.set("ai_search", cache_key, {
                "query": result.query,
                "intent": result.intent,
                "sources_count": result.sources_count,
                "data": result.data,
                "ai_synthesis": result.ai_synthesis,
                "ai_recommendations": result.ai_recommendations,
                "confidence_score": result.confidence_score,
                "execution_time_ms": result.execution_time_ms,
                "cached": False
            }, ttl=300)
        
        return result


# Instance globale
ai_search_engine = AISearchEngine()





Combine l'intelligence artificielle avec la recherche multi-sources
Approche RAG (Retrieval Augmented Generation)
"""
import asyncio
import time
import json
import hashlib
import logging
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import httpx

from services.ai_router import ai_router
from services.cache import cache_service
from services.ai_response_validator import ai_response_validator

logger = logging.getLogger(__name__)


class SearchIntent(Enum):
    """Types d'intentions de recherche détectées par l'IA"""
    INFORMATION = "information"      # Recherche d'info factuelle
    REALTIME = "realtime"            # Données temps réel
    COMPARISON = "comparison"        # Comparer des options
    RECOMMENDATION = "recommendation" # Obtenir des conseils
    ACTION = "action"                # Effectuer une action
    EXPLORATION = "exploration"      # Découvrir/explorer
    ANALYSIS = "analysis"            # Analyser des données


class DataFreshness(Enum):
    """Fraîcheur des données requises"""
    LIVE = "live"       # < 1 minute
    FRESH = "fresh"     # < 30 minutes
    RECENT = "recent"   # < 24 heures
    STABLE = "stable"   # Données stables


@dataclass
class SearchPlan:
    """Plan de recherche généré par l'IA"""
    query: str
    intent: SearchIntent
    entities: List[str]
    categories: List[str]
    apis_to_call: List[str]
    freshness: DataFreshness
    parallel_execution: bool
    expected_sources: int
    ai_synthesis_prompt: str


@dataclass
class SearchResult:
    """Résultat de recherche enrichi par l'IA"""
    query: str
    intent: str
    sources_count: int
    data: Dict[str, Any]
    ai_synthesis: str
    ai_recommendations: List[str]
    confidence_score: float
    execution_time_ms: float
    cached: bool = False


class AISearchEngine:
    """
    Moteur de recherche intelligent combinant IA + Data
    
    Flux:
    1. IA analyse la requête (intention, entités)
    2. Planification intelligente (quelles APIs appeler)
    3. Exécution parallèle des recherches
    4. IA synthétise et enrichit les résultats
    """
    
    def __init__(self):
        self.intent_keywords = self._init_intent_keywords()
        self.category_apis = self._init_category_apis()
        self.api_endpoints = self._init_api_endpoints()
        print("[OK] AI Search Engine initialized")
    
    def _init_intent_keywords(self) -> Dict[SearchIntent, List[str]]:
        """Mots-clés pour détection d'intention"""
        return {
            SearchIntent.INFORMATION: [
                "qu'est-ce que", "what is", "définition", "explain", "c'est quoi",
                "qui est", "who is", "histoire de", "history of", "comment fonctionne"
            ],
            SearchIntent.REALTIME: [
                "prix", "price", "cours", "météo", "weather", "actualité", "news",
                "en ce moment", "maintenant", "today", "live", "temps réel"
            ],
            SearchIntent.COMPARISON: [
                "vs", "versus", "comparaison", "compare", "différence", "meilleur",
                "best", "better", "ou", "or", "lequel", "which"
            ],
            SearchIntent.RECOMMENDATION: [
                "dois-je", "should i", "conseille", "recommend", "suggère", "suggest",
                "que faire", "what to do", "avis", "opinion"
            ],
            SearchIntent.ACTION: [
                "traduire", "translate", "raccourcir", "shorten", "convertir", "convert",
                "générer", "generate", "créer", "create", "envoyer", "send"
            ],
            SearchIntent.EXPLORATION: [
                "découvrir", "discover", "explorer", "explore", "random", "aléatoire",
                "surprends-moi", "surprise me", "nouveauté", "new"
            ],
            SearchIntent.ANALYSIS: [
                "analyse", "analyze", "tendance", "trend", "évolution", "evolution",
                "statistique", "statistics", "performance", "rapport", "report"
            ]
        }
    
    def _init_category_apis(self) -> Dict[str, List[str]]:
        """Mapping catégories → APIs"""
        return {
            "finance_crypto": ["coincap", "coingecko"],
            "finance_stocks": ["yahoo_finance", "alphavantage"],
            "news": ["newsapi", "guardian"],
            "weather": ["openmeteo", "openweathermap"],
            "wikipedia": ["wikipedia"],
            "books": ["google_books"],
            "countries": ["rest_countries"],
            "translation": ["libretranslate", "deepl"],
            "images": ["unsplash", "pexels", "lorempicsum"],
            "quotes": ["quotable", "adviceslip"],
            "test_data": ["jsonplaceholder", "randomuser", "fakestore"],
            "github": ["github"],
            "geolocation": ["nominatim", "ip_geolocation"],
            "time": ["worldtime"],
            "url": ["tinyurl"],
            "medical": ["pubmed"],
            "nutrition": ["usda"],
            "space": ["nasa"],
            "entertainment": ["tmdb", "omdb"]
        }
    
    def _init_api_endpoints(self) -> Dict[str, str]:
        """Mapping API → Endpoint local"""
        return {
            "coincap": "/api/coincap/assets",
            "wikipedia": "/api/wikipedia/search",
            "weather": "/api/weather/current",
            "news": "/api/news/headlines",
            "countries": "/api/countries/name",
            "quotes": "/api/quotes/random",
            "github": "/api/github/search/repos",
            "books": "/api/books/search",
            "translation": "/api/translation/translate",
            "randomuser": "/api/randomuser/users",
            "fakestore": "/api/fakestore/products",
            "jsonplaceholder": "/api/jsonplaceholder/posts",
            "lorempicsum": "/api/lorempicsum/list",
            "worldtime": "/api/worldtime/timezones",
            "tinyurl": "/api/tinyurl/shorten",
            "ip_geolocation": "/api/ip/my-ip"
        }
    
    async def analyze_query(self, query: str) -> Dict[str, Any]:
        """
        Étape 1: L'IA analyse la requête
        Détecte l'intention, les entités et les catégories pertinentes
        """
        # Détection d'intention par mots-clés
        detected_intent = self._detect_intent(query)
        
        # Utiliser l'IA pour une analyse plus fine
        analysis_prompt = f"""Analyse cette requête de recherche et réponds en JSON strict:

Requête: "{query}"

Réponds UNIQUEMENT avec ce format JSON (sans markdown, sans explication):
{{
    "intent": "information|realtime|comparison|recommendation|action|exploration|analysis",
    "entities": ["liste", "des", "entités", "clés"],
    "categories": ["finance_crypto", "news", "weather", "wikipedia", "books", "countries", "quotes", "github", "entertainment", "medical", "nutrition", "space", "translation", "images", "test_data", "geolocation", "time", "url"],
    "freshness": "live|fresh|recent|stable",
    "confidence": 0.0 à 1.0
}}

Choisis les catégories parmi: finance_crypto, finance_stocks, news, weather, wikipedia, books, countries, quotes, github, entertainment, medical, nutrition, space, translation, images, test_data, geolocation, time, url"""

        try:
            ai_response = await ai_router.route(analysis_prompt)
            response_text = ai_response.get("response", "{}")
            
            # Nettoyer la réponse
            response_text = response_text.strip()
            if response_text.startswith("```"):
                response_text = response_text.split("```")[1]
                if response_text.startswith("json"):
                    response_text = response_text[4:]
            
            analysis = json.loads(response_text)
            
            # Valider et enrichir
            return {
                "intent": analysis.get("intent", detected_intent.value),
                "entities": analysis.get("entities", []),
                "categories": analysis.get("categories", [])[:5],  # Max 5 catégories
                "freshness": analysis.get("freshness", "fresh"),
                "confidence": analysis.get("confidence", 0.7),
                "ai_analyzed": True
            }
        except Exception as e:
            # Fallback sur détection par mots-clés
            categories = self._detect_categories(query)
            return {
                "intent": detected_intent.value,
                "entities": query.split()[:5],
                "categories": categories,
                "freshness": "fresh",
                "confidence": 0.5,
                "ai_analyzed": False,
                "error": str(e)
            }
    
    def _detect_intent(self, query: str) -> SearchIntent:
        """Détection d'intention par mots-clés"""
        query_lower = query.lower()
        
        for intent, keywords in self.intent_keywords.items():
            for keyword in keywords:
                if keyword in query_lower:
                    return intent
        
        return SearchIntent.INFORMATION  # Par défaut
    
    def _detect_categories(self, query: str) -> List[str]:
        """Détection de catégories par mots-clés"""
        query_lower = query.lower()
        categories = []
        
        category_keywords = {
            "finance_crypto": ["bitcoin", "crypto", "ethereum", "btc", "eth", "coin"],
            "finance_stocks": ["stock", "action", "bourse", "nasdaq", "trading"],
            "news": ["actualité", "news", "nouvelle", "journal"],
            "weather": ["météo", "weather", "température", "pluie"],
            "wikipedia": ["wiki", "définition", "qu'est-ce", "histoire"],
            "books": ["livre", "book", "auteur", "roman"],
            "countries": ["pays", "country", "capitale", "drapeau"],
            "quotes": ["citation", "quote", "proverbe", "conseil"],
            "github": ["github", "repo", "code", "projet"],
            "entertainment": ["film", "movie", "série", "acteur"]
        }
        
        for category, keywords in category_keywords.items():
            for keyword in keywords:
                if keyword in query_lower:
                    categories.append(category)
                    break
        
        return categories[:5] if categories else ["wikipedia", "news"]
    
    async def create_search_plan(self, query: str, analysis: Dict[str, Any]) -> SearchPlan:
        """
        Étape 2: Créer un plan de recherche optimisé
        """
        intent = SearchIntent(analysis["intent"]) if analysis["intent"] in [e.value for e in SearchIntent] else SearchIntent.INFORMATION
        freshness = DataFreshness(analysis["freshness"]) if analysis["freshness"] in [e.value for e in DataFreshness] else DataFreshness.FRESH
        
        # Déterminer les APIs à appeler
        apis_to_call = []
        for category in analysis["categories"]:
            if category in self.category_apis:
                apis_to_call.extend(self.category_apis[category][:2])  # Max 2 par catégorie
        
        # Limiter à 6 APIs maximum
        apis_to_call = list(dict.fromkeys(apis_to_call))[:6]
        
        # Créer le prompt de synthèse
        synthesis_prompt = self._create_synthesis_prompt(query, intent, analysis["entities"])
        
        return SearchPlan(
            query=query,
            intent=intent,
            entities=analysis["entities"],
            categories=analysis["categories"],
            apis_to_call=apis_to_call,
            freshness=freshness,
            parallel_execution=len(apis_to_call) > 1,
            expected_sources=len(apis_to_call),
            ai_synthesis_prompt=synthesis_prompt
        )
    
    def _create_synthesis_prompt(self, query: str, intent: SearchIntent, entities: List[str]) -> str:
        """Crée le prompt de synthèse adapté à l'intention"""
        prompts = {
            SearchIntent.INFORMATION: f"Synthétise les informations trouvées sur '{query}'. Donne une réponse claire et factuelle.",
            SearchIntent.REALTIME: f"Résume les données actuelles pour '{query}'. Mets en avant les chiffres clés et tendances.",
            SearchIntent.COMPARISON: f"Compare les différentes options trouvées pour '{query}'. Liste les avantages et inconvénients.",
            SearchIntent.RECOMMENDATION: f"Basé sur les données trouvées, donne des recommandations pour '{query}'. Sois pragmatique.",
            SearchIntent.ACTION: f"Explique comment réaliser l'action demandée: '{query}'. Donne des étapes claires.",
            SearchIntent.EXPLORATION: f"Présente les découvertes intéressantes liées à '{query}'. Sois créatif et engageant.",
            SearchIntent.ANALYSIS: f"Analyse les données trouvées pour '{query}'. Identifie les tendances et insights."
        }
        return prompts.get(intent, prompts[SearchIntent.INFORMATION])
    
    async def execute_search(self, plan: SearchPlan) -> Dict[str, Any]:
        """
        Étape 3: Exécuter les recherches en parallèle
        """
        results = {}
        base_url = "http://localhost:8000"
        
        async def fetch_api(api_name: str) -> Tuple[str, Any]:
            """Fetch une API individuelle"""
            try:
                endpoint = self.api_endpoints.get(api_name)
                if not endpoint:
                    return api_name, {"error": "Endpoint not configured"}
                
                async with httpx.AsyncClient(timeout=10.0) as client:
                    # Adapter les paramètres selon l'API
                    params = self._get_api_params(api_name, plan.query, plan.entities)
                    
                    if params.get("method") == "POST":
                        response = await client.post(
                            f"{base_url}{endpoint}",
                            json=params.get("body", {})
                        )
                    else:
                        response = await client.get(
                            f"{base_url}{endpoint}",
                            params=params.get("query", {})
                        )
                    
                    if response.status_code == 200:
                        return api_name, response.json()
                    else:
                        return api_name, {"error": f"Status {response.status_code}"}
            except Exception as e:
                return api_name, {"error": str(e)}
        
        # Exécuter en parallèle
        if plan.parallel_execution and plan.apis_to_call:
            tasks = [fetch_api(api) for api in plan.apis_to_call]
            api_results = await asyncio.gather(*tasks)
            
            for api_name, data in api_results:
                results[api_name] = data
        
        return results
    
    def _get_api_params(self, api_name: str, query: str, entities: List[str]) -> Dict[str, Any]:
        """Génère les paramètres pour chaque API"""
        search_term = entities[0] if entities else query.split()[0]
        
        params_map = {
            "coincap": {"method": "GET", "query": {"limit": 10, "search": search_term}},
            "wikipedia": {"method": "GET", "query": {"query": query, "limit": 3}},
            "quotes": {"method": "GET", "query": {}},
            "countries": {"method": "GET", "query": {}},
            "github": {"method": "GET", "query": {"query": search_term, "limit": 5}},
            "books": {"method": "GET", "query": {"query": query, "limit": 5}},
            "randomuser": {"method": "GET", "query": {"count": 3}},
            "fakestore": {"method": "GET", "query": {"limit": 5}},
            "jsonplaceholder": {"method": "GET", "query": {"limit": 5}},
            "lorempicsum": {"method": "GET", "query": {"limit": 5}},
            "worldtime": {"method": "GET", "query": {}},
        }
        
        return params_map.get(api_name, {"method": "GET", "query": {"query": query}})
    
    async def synthesize_results(
        self,
        query: str,
        plan: SearchPlan,
        raw_results: Dict[str, Any]
    ) -> SearchResult:
        """
        Étape 4: L'IA synthétise et enrichit les résultats
        """
        # Préparer le contexte pour l'IA
        context = self._prepare_context(raw_results)
        
        # Générer la synthèse
        base_synthesis_prompt = f"""{plan.ai_synthesis_prompt}

Données collectées:
{context}

Instructions:
1. Synthétise les informations de manière claire et concise
2. Mets en avant les points clés
3. Si des données manquent, indique-le
4. Termine par 2-3 recommandations ou suggestions
5. Sois précis et factuel, cite tes sources quand possible

Réponds en français, de manière naturelle et utile."""

        # Améliorer le prompt avec le validateur
        synthesis_prompt = ai_response_validator.enhance_system_prompt(
            base_synthesis_prompt,
            query,
            expert_type=None
        )

        try:
            ai_response = await ai_router.route(
                prompt=synthesis_prompt,
                system_prompt="Tu es un expert en synthèse d'informations. Fournis des réponses précises et factuelles."
            )
            synthesis = ai_response.get("response", "Synthèse non disponible")
            
            # Valider la synthèse
            is_valid, validation_details = ai_response_validator.validate_response(
                response=synthesis,
                query=query,
                context=context
            )
            
            # Si la synthèse n'est pas valide, logger et potentiellement améliorer
            if not is_valid:
                logger.warning(f"Invalid synthesis for query '{query}': {validation_details}")
                # Ajouter un avertissement si la confiance est très faible
                if validation_details.get("confidence_score", 1.0) < 0.3:
                    synthesis = f"[WARN] {synthesis}\n\n(Note: Cette synthèse nécessite une vérification supplémentaire)"
            
        except Exception as e:
            logger.error(f"Synthesis error: {e}")
            synthesis = f"Synthèse IA indisponible: {str(e)}"
        
        # Générer des recommandations
        recommendations = await self._generate_recommendations(query, plan.intent, raw_results)
        
        # Calculer le score de confiance
        confidence = self._calculate_confidence(raw_results, plan)
        
        return SearchResult(
            query=query,
            intent=plan.intent.value,
            sources_count=len([r for r in raw_results.values() if "error" not in r]),
            data=raw_results,
            ai_synthesis=synthesis,
            ai_recommendations=recommendations,
            confidence_score=confidence,
            execution_time_ms=0,  # Sera rempli par le caller
            cached=False
        )
    
    def _prepare_context(self, results: Dict[str, Any]) -> str:
        """Prépare le contexte pour l'IA"""
        context_parts = []
        
        for source, data in results.items():
            if "error" in data:
                continue
            
            # Limiter la taille des données
            data_str = json.dumps(data, ensure_ascii=False)[:500]
            context_parts.append(f"[{source}]: {data_str}")
        
        return "\n".join(context_parts) if context_parts else "Aucune donnée disponible"
    
    async def _generate_recommendations(
        self,
        query: str,
        intent: SearchIntent,
        results: Dict[str, Any]
    ) -> List[str]:
        """Génère des recommandations basées sur les résultats"""
        recommendations = []
        
        # Recommandations génériques selon l'intention
        intent_recs = {
            SearchIntent.INFORMATION: [
                "Consultez Wikipedia pour plus de détails",
                "Vérifiez les sources pour confirmer les informations"
            ],
            SearchIntent.REALTIME: [
                "Rafraîchissez régulièrement pour des données à jour",
                "Configurez des alertes pour suivre les changements"
            ],
            SearchIntent.COMPARISON: [
                "Comparez plusieurs sources avant de décider",
                "Considérez vos critères prioritaires"
            ],
            SearchIntent.RECOMMENDATION: [
                "Adaptez les conseils à votre situation",
                "Consultez un expert si nécessaire"
            ]
        }
        
        recommendations = intent_recs.get(intent, ["Explorez les résultats pour plus de détails"])
        
        # Ajouter des recommandations basées sur les sources disponibles
        if "coincap" in results or "coingecko" in results:
            recommendations.append("Suivez les tendances du marché crypto")
        if "wikipedia" in results:
            recommendations.append("Approfondissez sur Wikipedia")
        
        return recommendations[:3]
    
    def _calculate_confidence(self, results: Dict[str, Any], plan: SearchPlan) -> float:
        """Calcule un score de confiance"""
        successful_sources = len([r for r in results.values() if "error" not in r])
        expected_sources = plan.expected_sources
        
        if expected_sources == 0:
            return 0.0
        
        base_score = successful_sources / expected_sources
        
        # Bonus si plusieurs sources concordent
        if successful_sources >= 2:
            base_score += 0.1
        
        return min(base_score, 1.0)
    
    async def search(
        self,
        query: str,
        use_cache: bool = True
    ) -> SearchResult:
        """
        Méthode principale: Recherche intelligente IA + Data
        
        Args:
            query: Requête de recherche
            use_cache: Utiliser le cache
            
        Returns:
            SearchResult enrichi par l'IA
        """
        start_time = time.time()
        
        # Vérifier le cache
        cache_key = f"ai_search:{hashlib.md5(query.encode()).hexdigest()}"
        if use_cache:
            cached = cache_service.get("ai_search", cache_key)
            if cached:
                cached["cached"] = True
                cached["execution_time_ms"] = (time.time() - start_time) * 1000
                return SearchResult(**cached)
        
        # Étape 1: Analyser la requête
        analysis = await self.analyze_query(query)
        
        # Étape 2: Créer le plan de recherche
        plan = await self.create_search_plan(query, analysis)
        
        # Étape 3: Exécuter les recherches
        raw_results = await self.execute_search(plan)
        
        # Étape 4: Synthétiser avec l'IA
        result = await self.synthesize_results(query, plan, raw_results)
        
        # Mettre à jour le temps d'exécution
        result.execution_time_ms = (time.time() - start_time) * 1000
        
        # Mettre en cache
        if use_cache:
            cache_service.set("ai_search", cache_key, {
                "query": result.query,
                "intent": result.intent,
                "sources_count": result.sources_count,
                "data": result.data,
                "ai_synthesis": result.ai_synthesis,
                "ai_recommendations": result.ai_recommendations,
                "confidence_score": result.confidence_score,
                "execution_time_ms": result.execution_time_ms,
                "cached": False
            }, ttl=300)
        
        return result


# Instance globale
ai_search_engine = AISearchEngine()




