"""
Task Executor - Exécuteur de tâches automatiques
Exécute des tâches basées sur les préférences utilisateur
"""
from typing import Dict, Any, List, Optional
from services.assistant.memory_store import memory_store
from services.assistant.preference_learner import preference_learner
from services.ai_router import ai_router


class TaskExecutor:
    """Exécuteur de tâches automatiques"""
    
    def __init__(self):
        self.memory_store = memory_store
        self.preference_learner = preference_learner
        self.ai_router = ai_router
    
    async def execute_task(
        self,
        user_id: str,
        task_type: str,
        parameters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Exécuter une tâche automatique
        
        Args:
            user_id: ID utilisateur
            task_type: Type de tâche (daily_summary, price_alert, news_digest, etc.)
            parameters: Paramètres spécifiques à la tâche
        
        Returns:
            Dict avec résultat de l'exécution
        """
        parameters = parameters or {}
        
        if task_type == "daily_summary":
            return await self._execute_daily_summary(user_id, parameters)
        elif task_type == "price_alert":
            return await self._execute_price_alert(user_id, parameters)
        elif task_type == "news_digest":
            return await self._execute_news_digest(user_id, parameters)
        elif task_type == "routine_suggestion":
            return await self._execute_routine_suggestion(user_id, parameters)
        else:
            return {
                "success": False,
                "error": f"Type de tâche inconnu: {task_type}"
            }
    
    async def _execute_daily_summary(
        self,
        user_id: str,
        parameters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Exécuter résumé quotidien"""
        # Obtenir interactions du jour
        interactions = self.memory_store.get_user_interactions(user_id, limit=100)
        
        if not interactions:
            return {
                "success": True,
                "summary": "Aucune activité aujourd'hui",
                "type": "daily_summary"
            }
        
        # Générer résumé avec IA
        try:
            interactions_text = "\n".join([
                f"- {i.get('category', 'unknown')}: {i.get('query', '')[:50]}"
                for i in interactions[:10]
            ])
            
            prompt = f"""
            Résume les activités de l'utilisateur aujourd'hui :
            
            {interactions_text}
            
            Donne un résumé concis et utile en français.
            """
            
            response = await self.ai_router.chat(prompt, max_tokens=200)
            summary = response.get("content", "")
            
            return {
                "success": True,
                "summary": summary,
                "interactions_count": len(interactions),
                "type": "daily_summary"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "type": "daily_summary"
            }
    
    async def _execute_price_alert(
        self,
        user_id: str,
        parameters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Exécuter alerte prix"""
        # Obtenir préférences finance
        preferences = self.preference_learner.get_user_preferences(user_id)
        finance_prefs = preferences.get("finance", {})
        
        if not finance_prefs:
            return {
                "success": False,
                "error": "Pas de préférences finance pour alerte prix",
                "type": "price_alert"
            }
        
        keywords = finance_prefs.get("keywords", [])
        crypto_keywords = [kw for kw in keywords if kw.lower() in ["bitcoin", "btc", "crypto", "ethereum", "eth"]]
        
        if not crypto_keywords:
            return {
                "success": False,
                "error": "Pas de cryptos suivies",
                "type": "price_alert"
            }
        
        # TODO: Intégrer avec API finance pour obtenir prix
        # Pour l'instant, retourner structure
        return {
            "success": True,
            "alerts": [
                {
                    "symbol": kw.upper(),
                    "message": f"Prix {kw} disponible",
                    "type": "price_alert"
                }
                for kw in crypto_keywords[:3]
            ],
            "type": "price_alert"
        }
    
    async def _execute_news_digest(
        self,
        user_id: str,
        parameters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Exécuter digest actualités"""
        preferences = self.preference_learner.get_user_preferences(user_id)
        news_prefs = preferences.get("news", {})
        
        if not news_prefs:
            return {
                "success": False,
                "error": "Pas de préférences news",
                "type": "news_digest"
            }
        
        keywords = news_prefs.get("keywords", [])
        
        # TODO: Intégrer avec API news
        return {
            "success": True,
            "digest": {
                "topics": keywords[:5],
                "message": "Digest actualités généré",
                "type": "news_digest"
            }
        }
    
    async def _execute_routine_suggestion(
        self,
        user_id: str,
        parameters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Exécuter suggestion routine"""
        from services.assistant.automation_engine import automation_engine
        
        optimization = await automation_engine.optimize_routine(user_id)
        
        return {
            "success": True,
            "suggestions": optimization.get("suggestions", []),
            "type": "routine_suggestion"
        }
    
    def get_available_tasks(self) -> List[Dict[str, str]]:
        """Obtenir les tâches disponibles"""
        return [
            {
                "id": "daily_summary",
                "name": "Résumé Quotidien",
                "description": "Résumé de vos activités du jour"
            },
            {
                "id": "price_alert",
                "name": "Alerte Prix",
                "description": "Alertes sur prix crypto/actions suivies"
            },
            {
                "id": "news_digest",
                "name": "Digest Actualités",
                "description": "Résumé actualités selon vos intérêts"
            },
            {
                "id": "routine_suggestion",
                "name": "Suggestion Routine",
                "description": "Suggestions pour optimiser votre routine"
            }
        ]


# Singleton instance
task_executor = TaskExecutor()


