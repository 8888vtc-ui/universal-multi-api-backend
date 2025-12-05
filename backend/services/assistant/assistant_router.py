"""
Assistant Router - Router principal pour l'assistant personnel IA
"""
from typing import Dict, Any, List, Optional
import asyncio
from services.assistant.memory_store import memory_store
from services.assistant.preference_learner import preference_learner
from services.ai_router import ai_router


class AssistantRouter:
    """Router principal pour l'assistant personnel"""
    
    def __init__(self):
        self.memory_store = memory_store
        self.preference_learner = preference_learner
        self.ai_router = ai_router
    
    async def learn_from_interaction(
        self,
        user_id: str,
        query: str,
        category: str,
        action: str = "search",
        feedback: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Apprendre d'une interaction utilisateur
        
        Args:
            user_id: ID utilisateur
            query: Requête de l'utilisateur
            category: Catégorie (finance, news, etc.)
            action: Action effectuée
            feedback: Feedback utilisateur (positive, negative, neutral)
        
        Returns:
            Dict avec confirmation d'apprentissage
        """
        # Sauvegarder l'interaction
        self.memory_store.save_interaction(
            user_id=user_id,
            query=query,
            category=category,
            action=action,
            feedback=feedback
        )
        
        # Apprendre les préférences (toutes les 10 interactions)
        interactions = self.memory_store.get_user_interactions(user_id, limit=10)
        if len(interactions) % 10 == 0:
            preferences = self.preference_learner.learn_from_interactions(user_id)
            return {
                "learned": True,
                "preferences_updated": True,
                "total_interactions": len(interactions)
            }
        
        return {
            "learned": True,
            "preferences_updated": False,
            "total_interactions": len(interactions)
        }
    
    async def get_recommendations(
        self,
        user_id: str,
        limit: int = 10,
        categories: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Obtenir des recommandations personnalisées cross-domaines
        
        Args:
            user_id: ID utilisateur
            limit: Nombre de recommandations
            categories: Catégories à filtrer (optionnel)
        
        Returns:
            Dict avec recommandations enrichies
        """
        # Obtenir les préférences
        preferences = self.preference_learner.get_user_preferences(user_id)
        
        if not preferences:
            return {
                "recommendations": [],
                "message": "Pas assez d'interactions pour générer des recommandations"
            }
        
        # Filtrer par catégories si spécifié
        if categories:
            preferences = {k: v for k, v in preferences.items() if k in categories}
        
        # Trier par poids décroissant
        sorted_prefs = sorted(
            preferences.items(),
            key=lambda x: x[1].get("weight", 0),
            reverse=True
        )
        
        # Générer recommandations basées sur préférences
        recommendations = []
        for category, prefs in sorted_prefs[:limit]:
            if category.startswith("_"):  # Ignorer patterns internes
                continue
            
            keywords = prefs.get("keywords", [])
            if keywords:
                # Créer une recommandation basée sur les mots-clés
                recommendation_query = " ".join(keywords[:3])
                
                # Enrichir avec suggestions IA
                ai_suggestion = await self._generate_ai_suggestion(
                    category=category,
                    keywords=keywords,
                    user_preferences=preferences
                )
                
                recommendations.append({
                    "category": category,
                    "query": recommendation_query,
                    "weight": prefs.get("weight", 0),
                    "reason": f"Basé sur vos recherches fréquentes en {category}",
                    "ai_suggestion": ai_suggestion,
                    "related_categories": self._find_related_categories(category, preferences)
                })
        
        # Ajouter recommandations cross-domaines
        cross_domain = await self._generate_cross_domain_recommendations(
            preferences=preferences,
            limit=limit // 2
        )
        recommendations.extend(cross_domain)
        
        # Trier par poids et limiter
        recommendations.sort(key=lambda x: x.get("weight", 0), reverse=True)
        
        return {
            "recommendations": recommendations[:limit],
            "total": len(recommendations),
            "user_preferences": {
                k: {"weight": v.get("weight", 0)} 
                for k, v in preferences.items() 
                if not k.startswith("_")
            }
        }
    
    async def _generate_ai_suggestion(
        self,
        category: str,
        keywords: List[str],
        user_preferences: Dict[str, Any]
    ) -> Optional[str]:
        """Générer une suggestion IA basée sur les préférences"""
        try:
            prompt = f"""
            L'utilisateur recherche souvent dans la catégorie "{category}" avec les mots-clés: {', '.join(keywords[:5])}
            
            Donne une suggestion courte (1 phrase) pour une recherche intéressante dans cette catégorie.
            Réponds uniquement avec la suggestion, sans explication.
            """
            
            response = await self.ai_router.chat(prompt, max_tokens=50)
            return response.get("content", "").strip()
        except:
            return None
    
    def _find_related_categories(
        self,
        category: str,
        preferences: Dict[str, Any]
    ) -> List[str]:
        """Trouver des catégories liées"""
        # Mapping de catégories liées
        related_map = {
            "finance": ["news", "weather"],
            "news": ["finance", "weather"],
            "weather": ["location", "news"],
            "medical": ["nutrition"],
            "nutrition": ["medical"],
            "entertainment": ["media", "news"]
        }
        
        related = related_map.get(category, [])
        # Filtrer pour ne garder que celles avec préférences
        return [cat for cat in related if cat in preferences]
    
    async def _generate_cross_domain_recommendations(
        self,
        preferences: Dict[str, Any],
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """Générer des recommandations cross-domaines"""
        recommendations = []
        
        # Si utilisateur aime finance, suggérer news finance
        if "finance" in preferences and "news" not in preferences:
            recommendations.append({
                "category": "news",
                "query": "actualité finance",
                "weight": preferences["finance"].get("weight", 0) * 0.7,
                "reason": "Basé sur votre intérêt pour la finance",
                "cross_domain": True,
                "source_category": "finance"
            })
        
        # Si utilisateur aime weather, suggérer location
        if "weather" in preferences and "location" not in preferences:
            recommendations.append({
                "category": "location",
                "query": "lieux intéressants",
                "weight": preferences["weather"].get("weight", 0) * 0.6,
                "reason": "Basé sur votre intérêt pour la météo",
                "cross_domain": True,
                "source_category": "weather"
            })
        
        # Si utilisateur aime medical, suggérer nutrition
        if "medical" in preferences and "nutrition" not in preferences:
            recommendations.append({
                "category": "nutrition",
                "query": "aliments santé",
                "weight": preferences["medical"].get("weight", 0) * 0.8,
                "reason": "Basé sur votre intérêt pour la santé",
                "cross_domain": True,
                "source_category": "medical"
            })
        
        return recommendations[:limit]
    
    def get_user_profile(self, user_id: str) -> Dict[str, Any]:
        """Obtenir le profil complet d'un utilisateur"""
        stats = self.memory_store.get_user_stats(user_id)
        preferences = self.preference_learner.get_user_preferences(user_id)
        patterns = self.memory_store.get_learned_patterns(user_id)
        
        return {
            **stats,
            "preferences": preferences,
            "learned_patterns": patterns
        }
    
    def get_status(self) -> Dict[str, Any]:
        """Obtenir le statut de l'assistant"""
        return {
            "service": "Personal AI Assistant",
            "available": True,
            "features": [
                "Apprentissage préférences",
                "Recommandations personnalisées",
                "Mémoire conversationnelle",
                "Patterns temporels"
            ]
        }


# Singleton instance
assistant_router = AssistantRouter()

