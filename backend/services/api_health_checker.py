"""
Service de vérification de santé des APIs
Vérifie que les variables d'environnement sont configurées et que les APIs sont disponibles
"""
import os
from typing import Dict, List, Any, Optional
from dotenv import load_dotenv

load_dotenv()


class APIHealthChecker:
    """Vérifier la santé et disponibilité des APIs"""
    
    def __init__(self):
        self.api_configs = self._load_api_configs()
    
    def _load_api_configs(self) -> Dict[str, Dict[str, Any]]:
        """Charger toutes les configurations d'APIs"""
        return {
            # AI Providers
            "groq": {
                "env_var": "GROQ_API_KEY",
                "required": False,
                "fallback": "ollama",
                "category": "ai"
            },
            "mistral": {
                "env_var": "MISTRAL_API_KEY",
                "required": False,
                "fallback": "groq",
                "category": "ai"
            },
            "gemini": {
                "env_var": "GEMINI_API_KEY",
                "required": False,
                "fallback": "mistral",
                "category": "ai"
            },
            "openrouter": {
                "env_var": "OPENROUTER_API_KEY",
                "required": False,
                "fallback": "gemini",
                "category": "ai"
            },
            "ollama": {
                "env_var": None,  # Pas de clé nécessaire (local)
                "required": False,
                "fallback": None,
                "category": "ai"
            },
            
            # External APIs
            "news_api": {
                "env_var": "NEWS_API_KEY",
                "required": False,
                "fallback": "guardian",
                "category": "news"
            },
            "guardian": {
                "env_var": "GUARDIAN_API_KEY",
                "required": False,
                "fallback": "news_api",
                "category": "news"
            },
            "openweather": {
                "env_var": "OPENWEATHER_API_KEY",
                "required": False,
                "fallback": "weather_api",
                "category": "weather"
            },
            "weather_api": {
                "env_var": "WEATHER_API_KEY",
                "required": False,
                "fallback": "openweather",
                "category": "weather"
            },
            "d_id": {
                "env_var": "D_ID_API_KEY",
                "required": False,
                "fallback": None,
                "category": "video"
            },
            "coingecko": {
                "env_var": "COINGECKO_API_KEY",
                "required": False,
                "fallback": "alpha_vantage",
                "category": "finance"
            },
            "alpha_vantage": {
                "env_var": "ALPHA_VANTAGE_API_KEY",
                "required": False,
                "fallback": "yfinance",
                "category": "finance"
            },
            "yfinance": {
                "env_var": None,  # Pas de clé nécessaire
                "required": False,
                "fallback": None,
                "category": "finance"
            },
        }
    
    def check_api_health(self, api_name: str) -> Dict[str, Any]:
        """Vérifier la santé d'une API spécifique"""
        config = self.api_configs.get(api_name)
        if not config:
            return {
                "name": api_name,
                "available": False,
                "reason": "API not configured"
            }
        
        env_var = config.get("env_var")
        available = True
        reason = "OK"
        
        if env_var:
            api_key = os.getenv(env_var)
            if not api_key:
                available = False
                reason = f"Missing {env_var}"
                if config.get("fallback"):
                    reason += f" (fallback: {config['fallback']})"
        else:
            # API sans clé (comme Ollama, yfinance)
            reason = "No API key required"
        
        return {
            "name": api_name,
            "available": available,
            "reason": reason,
            "fallback": config.get("fallback"),
            "category": config.get("category")
        }
    
    def check_all_apis(self) -> Dict[str, Any]:
        """Vérifier toutes les APIs"""
        results = {}
        categories = {}
        
        for api_name in self.api_configs.keys():
            health = self.check_api_health(api_name)
            results[api_name] = health
            
            category = health["category"]
            if category not in categories:
                categories[category] = {
                    "total": 0,
                    "available": 0,
                    "apis": []
                }
            
            categories[category]["total"] += 1
            if health["available"]:
                categories[category]["available"] += 1
            categories[category]["apis"].append(health)
        
        # Statistiques globales
        total_apis = len(results)
        available_apis = sum(1 for r in results.values() if r["available"])
        
        return {
            "summary": {
                "total_apis": total_apis,
                "available_apis": available_apis,
                "unavailable_apis": total_apis - available_apis,
                "availability_rate": round((available_apis / total_apis * 100) if total_apis > 0 else 0, 2)
            },
            "by_category": categories,
            "details": results
        }
    
    def get_missing_keys(self) -> List[str]:
        """Obtenir la liste des clés API manquantes"""
        missing = []
        for api_name, config in self.api_configs.items():
            env_var = config.get("env_var")
            if env_var and not os.getenv(env_var):
                missing.append({
                    "api": api_name,
                    "env_var": env_var,
                    "fallback": config.get("fallback"),
                    "category": config.get("category")
                })
        return missing
    
    def get_recommendations(self) -> List[str]:
        """Obtenir des recommandations pour améliorer la configuration"""
        recommendations = []
        health = self.check_all_apis()
        
        # Vérifier chaque catégorie
        for category, data in health["by_category"].items():
            if data["available"] == 0:
                recommendations.append(
                    f"⚠️ Catégorie '{category}': Aucune API disponible. "
                    f"Configurez au moins une API ou utilisez Ollama (gratuit, local)"
                )
            elif data["available"] < data["total"]:
                recommendations.append(
                    f"💡 Catégorie '{category}': {data['available']}/{data['total']} APIs disponibles. "
                    f"Configurez plus d'APIs pour meilleur fallback"
                )
        
        # Vérifier AI providers
        ai_apis = [r for r in health["details"].values() if r["category"] == "ai"]
        available_ai = sum(1 for a in ai_apis if a["available"])
        if available_ai == 0:
            recommendations.append(
                "🔴 CRITIQUE: Aucun provider IA disponible. "
                "Installez Ollama (gratuit, local) ou configurez au moins une clé API IA"
            )
        elif available_ai == 1:
            recommendations.append(
                "⚠️ Seul 1 provider IA disponible. Ajoutez plus de providers pour fallback"
            )
        
        return recommendations


# Singleton
api_health_checker = APIHealthChecker()
