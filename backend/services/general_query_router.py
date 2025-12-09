"""
General Query Router - Intelligent API routing for universal expert
Détecte le type de requête et sélectionne les APIs pertinentes parmi 26 disponibles
"""
from typing import Dict, List, Tuple, Optional
import re
import logging

logger = logging.getLogger(__name__)


class GeneralQueryRouter:
    """
    Routeur intelligent pour l'expert Général (WikiAsk)
    Détecte automatiquement le type de requête et sélectionne les APIs pertinentes
    """
    
    # Toutes les APIs disponibles (26)
    ALL_APIS = [
        # Culture & Knowledge (5)
        "wikipedia", "news", "history", "trivia", "quotes",
        # Entertainment (4)
        "omdb", "books", "jokes", "animals",
        # Geography & Travel (4)
        "countries", "geocoding", "weather", "flights",
        # Tech (2)
        "github", "numbers",
        # Health & Food (2)
        "nutrition", "medical",
        # Finance (7)
        "finance", "coincap", "exchange", "finance_stock",
        "finance_company", "finance_news", "finance_market_news",
        # Sports (1)
        "sports",
        # Other (1)
        "nameanalysis"
    ]
    
    # APIs universelles (toujours disponibles en fallback)
    UNIVERSAL_APIS = ["wikipedia", "news"]
    
    # Patterns de détection par type de requête
    QUERY_PATTERNS = {
        "culture": {
            "keywords": [
                # Français
                "qui a inventé", "c'est quoi", "qu'est-ce que", "définition",
                "histoire de", "biographie", "qui est", "quand", "où",
                "explique", "comment fonctionne", "origine de", "signification",
                "pourquoi", "qu'est ce", "c est quoi", "que veut dire",
                # Anglais
                "who invented", "what is", "explain", "definition",
                "history of", "biography", "who is", "when", "where",
                "how does", "origin of", "meaning of", "why"
            ],
            "priority_apis": ["wikipedia", "news", "history"],
            "secondary_apis": ["trivia", "quotes"],
            "max_apis": 5
        },
        
        "cinema": {
            "keywords": [
                # Français
                "film", "movie", "série", "serie", "acteur", "actrice",
                "réalisateur", "director", "oscar", "césar", "imdb",
                "cinéma", "cinema", "netflix", "streaming", "acteurs",
                "meilleur film", "box office", "bande annonce",
                # Anglais
                "actor", "actress", "award", "movie",
                "series", "tv show", "best movie", "trailer"
            ],
            "priority_apis": ["omdb", "news", "wikipedia"],
            "secondary_apis": ["trivia"],
            "max_apis": 4
        },
        
        "sport": {
            "keywords": [
                # Français
                "football", "basketball", "tennis", "rugby", "sport",
                "match", "championnat", "ligue", "équipe", "joueur",
                "champion", "coupe", "tournoi", "jeux olympiques",
                "ligue 1", "champions league", "world cup", "euro",
                # Anglais
                "soccer", "basket", "championship", "league", "player",
                "team", "tournament", "cup", "olympics", "nba", "nfl"
            ],
            "priority_apis": ["sports", "news", "wikipedia"],
            "secondary_apis": ["trivia"],
            "max_apis": 4
        },
        
        "cuisine": {
            "keywords": [
                # Français
                "recette", "cuisine", "ingrédient", "aliment",
                "calorie", "nutrition", "régime", "manger",
                "repas", "plat", "cuisiner", "gastronomie",
                "comment faire", "comment cuisiner", "comment préparer",
                # Anglais
                "recipe", "food", "ingredient", "calories", "eat",
                "meal", "dish", "cooking", "cook", "how to make"
            ],
            "priority_apis": ["nutrition", "wikipedia"],
            "secondary_apis": ["books", "news"],
            "max_apis": 4
        },
        
        "tech": {
            "keywords": [
                # Français
                "code", "programmation", "python", "javascript", "github",
                "développement", "software", "application", "app", "api",
                "programme", "langage", "développer", "intelligence artificielle",
                "machine learning", "ia", "ai", "algorithme",
                # Anglais
                "programming", "developer", "coding", "repository",
                "software", "language", "develop", "artificial intelligence"
            ],
            "priority_apis": ["github", "news", "wikipedia"],
            "secondary_apis": ["numbers"],
            "max_apis": 5
        },
        
        "geography": {
            "keywords": [
                # Français
                "pays", "capitale", "ville", "géographie",
                "carte", "localisation", "où se trouve", "population",
                "continent", "frontière", "superficie", "drapeau",
                # Anglais
                "country", "capital", "city", "geography",
                "location", "where is", "population", "flag"
            ],
            "priority_apis": ["countries", "geocoding", "wikipedia"],
            "secondary_apis": ["weather", "news"],
            "max_apis": 5
        },
        
        "finance": {
            "keywords": [
                # Français
                "bourse", "stock", "action", "crypto", "bitcoin", "btc",
                "prix", "cours", "marché", "euro", "dollar",
                "investissement", "trading", "dividende", "portefeuille",
                # Anglais
                "market", "eur", "usd", "eth", "ethereum", "investment",
                "stock", "crypto", "price", "trading", "portfolio"
            ],
            "priority_apis": ["finance", "finance_news", "finance_market_news"],
            "secondary_apis": ["exchange", "coincap", "news"],
            "max_apis": 6
        },
        
        "voyage": {
            "keywords": [
                # Français
                "voyage", "vol", "destination", "hôtel", "hotel",
                "météo", "climat", "visiter", "tourisme",
                "vacances", "voyager", "aéroport", "billet",
                # Anglais
                "travel", "flight", "destination", "weather",
                "visit", "tourism", "vacation", "airport", "ticket"
            ],
            "priority_apis": ["flights", "geocoding", "weather", "countries"],
            "secondary_apis": ["news", "wikipedia"],
            "max_apis": 6
        },
        
        "sante": {
            "keywords": [
                # Français
                "santé", "maladie", "symptôme", "médicament",
                "traitement", "médecin", "docteur", "malade",
                "douleur", "fièvre", "grippe", "covid",
                # Anglais
                "health", "disease", "symptom", "medicine",
                "treatment", "doctor", "illness", "pain"
            ],
            "priority_apis": ["medical", "nutrition", "wikipedia"],
            "secondary_apis": ["news"],
            "max_apis": 4
        },
        
        "citation": {
            "keywords": [
                # Français
                "citation", "proverbe", "sagesse", "phrase célèbre",
                "dicton", "maxime", "parole de", "a dit",
                # Anglais
                "quote", "saying", "proverb", "wisdom", "famous quote"
            ],
            "priority_apis": ["quotes", "wikipedia"],
            "secondary_apis": [],
            "max_apis": 2
        },
        
        "humour": {
            "keywords": [
                # Français
                "blague", "rire", "drôle", "humour",
                "marrant", "amusant", "plaisanterie", "comique",
                # Anglais
                "joke", "funny", "humor", "laugh", "comic"
            ],
            "priority_apis": ["jokes", "trivia"],
            "secondary_apis": ["quotes"],
            "max_apis": 3
        },
        
        "litterature": {
            "keywords": [
                # Français
                "livre", "auteur", "écrivain", "roman", "poésie",
                "littérature", "lecture", "bestseller", "écrire",
                # Anglais
                "book", "author", "writer", "novel", "poetry",
                "literature", "reading", "bestseller"
            ],
            "priority_apis": ["books", "wikipedia"],
            "secondary_apis": ["quotes", "news"],
            "max_apis": 4
        },
        
        "prenom": {
            "keywords": [
                # Français
                "prénom", "signification prénom", "origine prénom",
                "signification du nom", "que signifie le prénom",
                # Anglais
                "name meaning", "name origin", "what does name mean"
            ],
            "priority_apis": ["nameanalysis", "wikipedia"],
            "secondary_apis": [],
            "max_apis": 2
        }
    }
    
    @classmethod
    def detect_query_type(cls, query: str) -> Tuple[str, float, List[str]]:
        """
        Détecte le type de requête avec score de confiance
        
        Args:
            query: Requête utilisateur
            
        Returns:
            (query_type, confidence, matched_keywords)
            - query_type: Type détecté ou "general"
            - confidence: Score 0.0-1.0
            - matched_keywords: Mots-clés trouvés
        """
        query_lower = query.lower()
        best_match = ("general", 0.0, [])
        
        for query_type, config in cls.QUERY_PATTERNS.items():
            matched = []
            for keyword in config["keywords"]:
                if keyword in query_lower:
                    matched.append(keyword)
            
            if matched:
                # Calcul de confiance basé sur le nombre de matches
                match_count = len(matched)
                confidence = min(0.9, 0.2 + match_count * 0.15)
                
                if confidence > best_match[1]:
                    best_match = (query_type, confidence, matched)
        
        return best_match
    
    @classmethod
    def get_relevant_apis(cls, query: str, max_apis: int = 8) -> List[str]:
        """
        Sélectionne les APIs pertinentes pour une requête
        
        Args:
            query: Requête utilisateur
            max_apis: Nombre maximum d'APIs à retourner
            
        Returns:
            Liste d'APIs ordonnées par pertinence
        """
        query_type, confidence, matched = cls.detect_query_type(query)
        
        logger.info(f"Query type detected: {query_type} (confidence: {confidence:.2f})")
        
        # Si type général ou confiance faible, utiliser APIs universelles + quelques autres
        if query_type == "general" or confidence < 0.3:
            # Mix d'APIs pour les requêtes générales
            return ["wikipedia", "news", "trivia"][:max_apis]
        
        # Récupérer la configuration du type
        config = cls.QUERY_PATTERNS.get(query_type, {})
        priority_apis = config.get("priority_apis", [])
        secondary_apis = config.get("secondary_apis", [])
        type_max = config.get("max_apis", max_apis)
        
        # Limiter le nombre d'APIs selon le type
        actual_max = min(max_apis, type_max)
        
        # Construire la liste
        selected = []
        
        # 1. Ajouter les APIs prioritaires
        for api in priority_apis:
            if len(selected) < actual_max:
                selected.append(api)
        
        # 2. Ajouter les APIs secondaires si espace disponible
        remaining = actual_max - len(selected)
        if remaining > 0:
            for api in secondary_apis:
                if len(selected) < actual_max and api not in selected:
                    selected.append(api)
        
        # 3. Toujours inclure wikipedia et news si pas déjà présents
        for universal_api in cls.UNIVERSAL_APIS:
            if universal_api not in selected and len(selected) < actual_max:
                selected.append(universal_api)
        
        return selected[:actual_max]
    
    @classmethod
    def get_all_available_apis(cls) -> List[str]:
        """Retourne toutes les APIs disponibles"""
        return cls.ALL_APIS.copy()
    
    @classmethod
    def get_fallback_message(cls, query_type: str) -> str:
        """Retourne un message de fallback approprié"""
        messages = {
            "culture": "Aucune donnée culturelle trouvée.",
            "cinema": "Aucune donnée cinéma trouvée.",
            "sport": "Aucune donnée sportive trouvée.",
            "cuisine": "Aucune donnée culinaire trouvée.",
            "tech": "Aucune donnée technique trouvée.",
            "geography": "Aucune donnée géographique trouvée.",
            "finance": "Aucune donnée financière trouvée.",
            "voyage": "Aucune donnée voyage trouvée.",
            "sante": "Aucune donnée santé trouvée.",
            "citation": "Aucune citation trouvée.",
            "humour": "Aucune blague trouvée.",
            "litterature": "Aucune donnée littéraire trouvée.",
            "prenom": "Aucune information sur ce prénom.",
            "general": "Aucune donnée trouvée."
        }
        return messages.get(query_type, messages["general"])


# Test function
def test_router():
    queries = [
        "Qui a inventé Internet ?",
        "Meilleur film 2024",
        "Recette carbonara",
        "Prix du Bitcoin",
        "Vol Paris Tokyo",
        "Résultats Ligue 1",
        "Blague du jour",
        "Citation inspirante"
    ]
    
    for query in queries:
        query_type, confidence, matched = GeneralQueryRouter.detect_query_type(query)
        apis = GeneralQueryRouter.get_relevant_apis(query)
        print(f"\nQuery: {query}")
        print(f"Type: {query_type} ({confidence:.0%})")
        print(f"APIs: {apis}")


if __name__ == "__main__":
    test_router()
