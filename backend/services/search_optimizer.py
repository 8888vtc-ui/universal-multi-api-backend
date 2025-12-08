"""
Service d'optimisation des recherches par regroupement intelligent
Stratégie de catégorisation et cache optimisé pour améliorer les performances
"""
from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
import hashlib
import json
from services.cache import cache_service


class APICategory(Enum):
    """Catégories d'APIs pour regroupement optimisé"""
    # IA & Chat
    AI_CHAT = "ai_chat"
    AI_EMBEDDINGS = "ai_embeddings"
    
    # Finance
    FINANCE_CRYPTO = "finance_crypto"
    FINANCE_STOCKS = "finance_stocks"
    FINANCE_EXCHANGE = "finance_exchange"
    
    # Actualités & Médias
    NEWS = "news"
    MEDIA_IMAGES = "media_images"
    MEDIA_VIDEO = "media_video"
    
    # Localisation & Environnement
    WEATHER = "weather"
    GEOCODING = "geocoding"
    IP_GEOLOCATION = "ip_geolocation"
    COUNTRIES = "countries"
    
    # Contenu & Éducation
    WIKIPEDIA = "wikipedia"
    BOOKS = "books"
    ENTERTAINMENT = "entertainment"
    
    # Utilitaires
    TRANSLATION = "translation"
    UTILITIES = "utilities"
    WEBHOOKS = "webhooks"
    
    # Santé & Nutrition
    MEDICAL = "medical"
    NUTRITION = "nutrition"
    SPORTS = "sports"
    
    # Espace & Science
    SPACE = "space"
    
    # Données de Test
    TEST_DATA = "test_data"
    
    # Communication
    MESSAGING = "messaging"
    EMAIL = "email"


@dataclass
class APIGroup:
    """Groupe d'APIs avec stratégie d'optimisation"""
    category: APICategory
    apis: List[str] = field(default_factory=list)
    priority_order: List[str] = field(default_factory=list)
    cache_ttl: int = 300  # 5 minutes par défaut
    parallel_execution: bool = True
    fallback_enabled: bool = True
    max_results: int = 10


@dataclass
class SearchStrategy:
    """Stratégie de recherche optimisée"""
    query: str
    detected_categories: List[APICategory]
    api_groups: List[APIGroup]
    cache_key: str
    estimated_time_ms: float
    priority_apis: List[str] = field(default_factory=list)


class SearchOptimizer:
    """
    Optimiseur de recherches par regroupement intelligent
    
    Fonctionnalités :
    - Regroupement automatique des APIs par catégorie
    - Cache intelligent par catégorie
    - Priorisation des APIs les plus rapides
    - Exécution parallèle optimisée
    - Détection d'intention améliorée
    """
    
    def __init__(self):
        self.api_groups = self._initialize_api_groups()
        self.category_keywords = self._initialize_category_keywords()
        self.api_performance = {}  # Cache des performances par API
        
    def _initialize_api_groups(self) -> Dict[APICategory, APIGroup]:
        """Initialise les groupes d'APIs avec stratégie d'optimisation"""
        return {
            # IA & Chat
            APICategory.AI_CHAT: APIGroup(
                category=APICategory.AI_CHAT,
                apis=["groq", "mistral", "anthropic", "gemini", "ollama"],
                priority_order=["groq", "ollama", "mistral", "anthropic", "gemini"],
                cache_ttl=600,  # 10 minutes pour les réponses IA
                parallel_execution=False,  # Séquentiel avec fallback
                max_results=1
            ),
            
            # Finance Crypto
            APICategory.FINANCE_CRYPTO: APIGroup(
                category=APICategory.FINANCE_CRYPTO,
                apis=["coingecko", "coincap", "yahoo_finance"],
                priority_order=["coingecko", "coincap", "yahoo_finance"],
                cache_ttl=60,  # 1 minute (données financières changeantes)
                parallel_execution=True,
                max_results=10
            ),
            
            # Finance Stocks
            APICategory.FINANCE_STOCKS: APIGroup(
                category=APICategory.FINANCE_STOCKS,
                apis=["alphavantage", "yahoo_finance"],
                priority_order=["yahoo_finance", "alphavantage"],
                cache_ttl=60,
                parallel_execution=True,
                max_results=10
            ),
            
            # Actualités
            APICategory.NEWS: APIGroup(
                category=APICategory.NEWS,
                apis=["newsapi", "the_guardian"],
                priority_order=["newsapi", "the_guardian"],
                cache_ttl=300,  # 5 minutes
                parallel_execution=True,
                max_results=10
            ),
            
            # Météo
            APICategory.WEATHER: APIGroup(
                category=APICategory.WEATHER,
                apis=["openweathermap", "openmeteo", "weatherapi"],
                priority_order=["openmeteo", "openweathermap", "weatherapi"],
                cache_ttl=1800,  # 30 minutes (météo change lentement)
                parallel_execution=False,  # Un seul provider suffit
                max_results=1
            ),
            
            # Géocodage
            APICategory.GEOCODING: APIGroup(
                category=APICategory.GEOCODING,
                apis=["nominatim", "opencage", "mapbox"],
                priority_order=["nominatim", "opencage", "mapbox"],
                cache_ttl=86400,  # 24 heures (adresses ne changent pas)
                parallel_execution=False,
                max_results=5
            ),
            
            # Images
            APICategory.MEDIA_IMAGES: APIGroup(
                category=APICategory.MEDIA_IMAGES,
                apis=["unsplash", "pexels", "pixabay", "lorempicsum"],
                priority_order=["unsplash", "pexels", "pixabay", "lorempicsum"],
                cache_ttl=3600,  # 1 heure
                parallel_execution=True,
                max_results=20
            ),
            
            # Wikipedia & Contenu
            APICategory.WIKIPEDIA: APIGroup(
                category=APICategory.WIKIPEDIA,
                apis=["wikipedia"],
                priority_order=["wikipedia"],
                cache_ttl=3600,
                parallel_execution=False,
                max_results=5
            ),
            
            # Livres
            APICategory.BOOKS: APIGroup(
                category=APICategory.BOOKS,
                apis=["google_books"],
                priority_order=["google_books"],
                cache_ttl=3600,
                parallel_execution=False,
                max_results=10
            ),
            
            # Traduction
            APICategory.TRANSLATION: APIGroup(
                category=APICategory.TRANSLATION,
                apis=["google_translate", "deepl", "libretranslate", "yandex"],
                priority_order=["deepl", "google_translate", "libretranslate", "yandex"],
                cache_ttl=86400,  # 24 heures (traductions stables)
                parallel_execution=False,
                max_results=1
            ),
            
            # Test Data
            APICategory.TEST_DATA: APIGroup(
                category=APICategory.TEST_DATA,
                apis=["jsonplaceholder", "randomuser", "fakestore"],
                priority_order=["jsonplaceholder", "randomuser", "fakestore"],
                cache_ttl=300,
                parallel_execution=True,
                max_results=20
            ),
            
            # Countries
            APICategory.COUNTRIES: APIGroup(
                category=APICategory.COUNTRIES,
                apis=["rest_countries"],
                priority_order=["rest_countries"],
                cache_ttl=86400,
                parallel_execution=False,
                max_results=50
            ),
            
            # IP Geolocation
            APICategory.IP_GEOLOCATION: APIGroup(
                category=APICategory.IP_GEOLOCATION,
                apis=["ip_geolocation"],
                priority_order=["ip_geolocation"],
                cache_ttl=86400,
                parallel_execution=False,
                max_results=1
            ),
            
            # GitHub
            APICategory.UTILITIES: APIGroup(
                category=APICategory.UTILITIES,
                apis=["github", "tinyurl"],
                priority_order=["github", "tinyurl"],
                cache_ttl=300,
                parallel_execution=True,
                max_results=10
            ),
        }
    
    def _initialize_category_keywords(self) -> Dict[APICategory, Set[str]]:
        """Initialise les mots-clés pour détection de catégorie"""
        return {
            APICategory.AI_CHAT: {"chat", "ia", "ai", "assistant", "gpt", "claude", "répondre", "question"},
            APICategory.FINANCE_CRYPTO: {"bitcoin", "crypto", "ethereum", "btc", "eth", "coin", "blockchain"},
            APICategory.FINANCE_STOCKS: {"stock", "action", "bourse", "nasdaq", "s&p", "dow", "ticker"},
            APICategory.NEWS: {"actualité", "news", "nouvelle", "article", "journal", "presse"},
            APICategory.WEATHER: {"météo", "weather", "température", "pluie", "soleil", "nuage"},
            APICategory.GEOCODING: {"adresse", "lieu", "ville", "pays", "coordonnées", "localisation"},
            APICategory.MEDIA_IMAGES: {"image", "photo", "picture", "gif", "meme"},
            APICategory.WIKIPEDIA: {"wikipedia", "encyclopédie", "définition", "qu'est-ce que"},
            APICategory.BOOKS: {"livre", "book", "auteur", "bibliothèque", "roman"},
            APICategory.TRANSLATION: {"traduire", "translate", "langue", "anglais", "français"},
            APICategory.TEST_DATA: {"test", "fake", "dummy", "exemple", "sample"},
            APICategory.COUNTRIES: {"pays", "country", "nation", "drapeau", "capitale"},
            APICategory.IP_GEOLOCATION: {"ip", "adresse ip", "géolocalisation ip"},
        }
    
    def detect_categories(self, query: str) -> List[APICategory]:
        """
        Détecte les catégories pertinentes pour une requête
        Retourne les catégories triées par pertinence
        """
        query_lower = query.lower()
        query_words = set(query_lower.split())
        
        category_scores = {}
        
        for category, keywords in self.category_keywords.items():
            score = 0
            # Score basé sur les mots-clés
            for keyword in keywords:
                if keyword in query_lower:
                    score += 1
            # Bonus si plusieurs mots correspondent
            matching_words = query_words.intersection(keywords)
            if matching_words:
                score += len(matching_words) * 0.5
            
            if score > 0:
                category_scores[category] = score
        
        # Trier par score décroissant
        sorted_categories = sorted(
            category_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        return [cat for cat, _ in sorted_categories[:5]]  # Top 5 catégories
    
    def create_search_strategy(
        self,
        query: str,
        categories: Optional[List[str]] = None,
        max_results: int = 10
    ) -> SearchStrategy:
        """
        Crée une stratégie de recherche optimisée
        
        Args:
            query: Requête de recherche
            categories: Catégories spécifiées (optionnel)
            max_results: Nombre maximum de résultats par catégorie
            
        Returns:
            SearchStrategy avec regroupement optimisé
        """
        # Détecter les catégories si non spécifiées
        if categories:
            # Convertir les noms de catégories en enum
            detected = []
            for cat_name in categories:
                try:
                    detected.append(APICategory(cat_name))
                except ValueError:
                    # Essayer de trouver par nom partiel
                    for cat in APICategory:
                        if cat_name.lower() in cat.value.lower():
                            detected.append(cat)
                            break
        else:
            detected = self.detect_categories(query)
        
        # Créer les groupes d'APIs pour les catégories détectées
        api_groups = []
        for category in detected:
            if category in self.api_groups:
                group = self.api_groups[category]
                # Ajuster max_results si nécessaire
                group.max_results = min(max_results, group.max_results)
                api_groups.append(group)
        
        # Générer la clé de cache
        cache_key = self._generate_cache_key(query, detected, max_results)
        
        # Estimer le temps d'exécution
        estimated_time = self._estimate_execution_time(api_groups)
        
        # Déterminer les APIs prioritaires
        priority_apis = self._get_priority_apis(api_groups)
        
        return SearchStrategy(
            query=query,
            detected_categories=detected,
            api_groups=api_groups,
            cache_key=cache_key,
            estimated_time_ms=estimated_time,
            priority_apis=priority_apis
        )
    
    def _generate_cache_key(
        self,
        query: str,
        categories: List[APICategory],
        max_results: int
    ) -> str:
        """Génère une clé de cache optimisée"""
        cache_data = {
            "query": query.lower().strip(),
            "categories": [cat.value for cat in categories],
            "max_results": max_results
        }
        cache_str = json.dumps(cache_data, sort_keys=True)
        return f"search_opt:{hashlib.md5(cache_str.encode()).hexdigest()}"
    
    def _estimate_execution_time(self, api_groups: List[APIGroup]) -> float:
        """Estime le temps d'exécution en millisecondes"""
        if not api_groups:
            return 0.0
        
        # Temps de base par groupe
        base_time_per_group = 200  # 200ms par groupe
        
        # Si exécution parallèle, prendre le maximum
        if all(group.parallel_execution for group in api_groups):
            return base_time_per_group * len(api_groups)
        
        # Sinon, additionner les temps
        total_time = 0
        for group in api_groups:
            if group.parallel_execution:
                total_time += base_time_per_group
            else:
                total_time += base_time_per_group * len(group.priority_order)
        
        return total_time
    
    def _get_priority_apis(self, api_groups: List[APIGroup]) -> List[str]:
        """Récupère les APIs prioritaires de tous les groupes"""
        priority_apis = []
        for group in api_groups:
            if group.priority_order:
                priority_apis.extend(group.priority_order[:2])  # Top 2 par groupe
        return list(dict.fromkeys(priority_apis))  # Supprimer les doublons
    
    def get_cached_result(self, cache_key: str) -> Optional[Dict[str, Any]]:
        """Récupère un résultat depuis le cache"""
        return cache_service.get("search_optimized", cache_key)
    
    def set_cached_result(
        self,
        cache_key: str,
        result: Dict[str, Any],
        ttl: Optional[int] = None
    ):
        """Met en cache un résultat avec TTL optimisé"""
        if ttl is None:
            # Utiliser le TTL le plus court des groupes utilisés
            ttl = 300  # Par défaut 5 minutes
        
        cache_service.set("search_optimized", cache_key, result, ttl=ttl)
    
    def get_group_for_category(self, category: APICategory) -> Optional[APIGroup]:
        """Récupère le groupe d'APIs pour une catégorie"""
        return self.api_groups.get(category)
    
    def get_all_categories(self) -> List[str]:
        """Retourne toutes les catégories disponibles"""
        return [cat.value for cat in APICategory]
    
    def get_category_info(self, category: APICategory) -> Dict[str, Any]:
        """Retourne les informations sur une catégorie"""
        group = self.api_groups.get(category)
        if not group:
            return {}
        
        return {
            "category": category.value,
            "apis": group.apis,
            "priority_order": group.priority_order,
            "cache_ttl": group.cache_ttl,
            "parallel_execution": group.parallel_execution,
            "max_results": group.max_results
        }


# Instance globale
search_optimizer = SearchOptimizer()






