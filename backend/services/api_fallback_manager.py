"""
Gestionnaire de fallback pour les APIs
Assure qu'il y a toujours un fallback disponible
"""
import os
import logging
from typing import Dict, List, Optional, Any
from services.api_health_checker import api_health_checker

logger = logging.getLogger(__name__)


class APIFallbackManager:
    """Gérer les fallbacks entre APIs"""
    
    def __init__(self):
        self.fallback_chains = self._build_fallback_chains()
    
    def _build_fallback_chains(self) -> Dict[str, List[str]]:
        """Construire les chaînes de fallback"""
        return {
            "ai": ["groq", "mistral", "gemini", "openrouter", "ollama"],
            "news": ["news_api", "guardian"],
            "weather": ["openweather", "weather_api"],
            "finance": ["coingecko", "alpha_vantage", "yfinance"],
            "translation": ["google", "deepl", "yandex", "libre"],
            "geocoding": ["google", "mapbox"],
            "media": ["unsplash", "pexels", "pixabay"],
        }
    
    def get_available_providers(self, category: str) -> List[str]:
        """Obtenir les providers disponibles pour une catégorie"""
        chain = self.fallback_chains.get(category, [])
        available = []
        
        for provider in chain:
            health = api_health_checker.check_api_health(provider)
            if health["available"]:
                available.append(provider)
        
        return available
    
    def get_fallback_chain(self, category: str) -> List[str]:
        """Obtenir la chaîne de fallback pour une catégorie"""
        chain = self.fallback_chains.get(category, [])
        return self.get_available_providers(category)
    
    def ensure_fallback(self, category: str) -> bool:
        """S'assurer qu'il y a au moins un fallback disponible"""
        available = self.get_available_providers(category)
        
        if not available:
            logger.warning(f"⚠️ Aucun provider disponible pour {category}")
            
            # Pour AI, toujours avoir Ollama comme dernier recours
            if category == "ai":
                logger.info("💡 Ollama devrait être disponible (local, gratuit)")
                return True
            
            return False
        
        if len(available) == 1:
            logger.warning(f"⚠️ Seul 1 provider disponible pour {category}: {available[0]}")
        
        return True
    
    def get_next_fallback(self, category: str, current_provider: str) -> Optional[str]:
        """Obtenir le prochain provider en fallback"""
        chain = self.get_fallback_chain(category)
        
        try:
            current_index = chain.index(current_provider)
            if current_index + 1 < len(chain):
                return chain[current_index + 1]
        except ValueError:
            pass
        
        return None
    
    def check_all_categories(self) -> Dict[str, Any]:
        """Vérifier toutes les catégories"""
        results = {}
        
        for category in self.fallback_chains.keys():
            available = self.get_available_providers(category)
            has_fallback = len(available) > 1
            
            results[category] = {
                "available_providers": available,
                "count": len(available),
                "has_fallback": has_fallback,
                "status": "OK" if available else "CRITICAL",
                "recommendation": self._get_recommendation(category, available)
            }
        
        return results
    
    def _get_recommendation(self, category: str, available: List[str]) -> str:
        """Obtenir une recommandation pour une catégorie"""
        if not available:
            return f"⚠️ Configurez au moins un provider pour {category}"
        elif len(available) == 1:
            return f"💡 Ajoutez un provider de fallback pour {category}"
        else:
            return f"✅ {len(available)} providers disponibles pour {category}"


# Singleton
api_fallback_manager = APIFallbackManager()


