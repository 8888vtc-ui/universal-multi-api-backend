"""
Automation Engine - Moteur d'automatisation intelligente
Analyse la routine utilisateur et suggère des optimisations
"""
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from services.assistant.memory_store import memory_store
from services.ai_router import ai_router


class AutomationEngine:
    """Moteur d'automatisation intelligente"""
    
    def __init__(self):
        self.memory_store = memory_store
        self.ai_router = ai_router
    
    async def analyze_routine(
        self,
        user_id: str,
        days: int = 7
    ) -> Dict[str, Any]:
        """
        Analyser la routine utilisateur
        
        Args:
            user_id: ID utilisateur
            days: Nombre de jours à analyser
        
        Returns:
            Dict avec analyse de routine
        """
        # Obtenir interactions des derniers jours
        interactions = self.memory_store.get_user_interactions(user_id, limit=1000)
        
        if not interactions:
            return {
                "routine_analyzed": False,
                "message": "Pas assez de données pour analyser la routine"
            }
        
        # Filtrer par date
        cutoff_date = datetime.now() - timedelta(days=days)
        recent_interactions = [
            i for i in interactions
            if datetime.fromisoformat(i['timestamp']) > cutoff_date
        ]
        
        if not recent_interactions:
            return {
                "routine_analyzed": False,
                "message": f"Pas d'interactions dans les {days} derniers jours"
            }
        
        # Analyser patterns
        analysis = {
            "total_interactions": len(recent_interactions),
            "interactions_per_day": len(recent_interactions) / days,
            "most_active_hour": self._get_most_active_hour(recent_interactions),
            "most_active_day": self._get_most_active_day(recent_interactions),
            "categories_used": self._get_categories_used(recent_interactions),
            "routine_patterns": self._detect_routine_patterns(recent_interactions)
        }
        
        return {
            "routine_analyzed": True,
            "analysis": analysis,
            "period_days": days
        }
    
    def _get_most_active_hour(self, interactions: List[Dict]) -> Optional[int]:
        """Obtenir l'heure la plus active"""
        hours = []
        for interaction in interactions:
            try:
                timestamp = datetime.fromisoformat(interaction['timestamp'])
                hours.append(timestamp.hour)
            except:
                pass
        
        if hours:
            from collections import Counter
            return Counter(hours).most_common(1)[0][0]
        return None
    
    def _get_most_active_day(self, interactions: List[Dict]) -> Optional[int]:
        """Obtenir le jour de la semaine le plus actif (0=lundi)"""
        days = []
        for interaction in interactions:
            try:
                timestamp = datetime.fromisoformat(interaction['timestamp'])
                days.append(timestamp.weekday())
            except:
                pass
        
        if days:
            from collections import Counter
            return Counter(days).most_common(1)[0][0]
        return None
    
    def _get_categories_used(self, interactions: List[Dict]) -> Dict[str, int]:
        """Obtenir les catégories utilisées"""
        from collections import Counter
        categories = [i.get('category') for i in interactions if i.get('category')]
        return dict(Counter(categories))
    
    def _detect_routine_patterns(self, interactions: List[Dict]) -> List[Dict[str, Any]]:
        """Détecter des patterns de routine"""
        patterns = []
        
        # Pattern: Recherche quotidienne à la même heure
        hour_groups = {}
        for interaction in interactions:
            try:
                timestamp = datetime.fromisoformat(interaction['timestamp'])
                hour = timestamp.hour
                if hour not in hour_groups:
                    hour_groups[hour] = []
                hour_groups[hour].append(interaction)
            except:
                pass
        
        for hour, group in hour_groups.items():
            if len(group) >= 3:  # Au moins 3 fois à cette heure
                patterns.append({
                    "type": "daily_time",
                    "hour": hour,
                    "frequency": len(group),
                    "description": f"Recherche régulière à {hour}h"
                })
        
        return patterns
    
    async def optimize_routine(
        self,
        user_id: str
    ) -> Dict[str, Any]:
        """
        Optimiser la routine utilisateur avec suggestions IA
        
        Args:
            user_id: ID utilisateur
        
        Returns:
            Dict avec suggestions d'optimisation
        """
        # Analyser la routine
        routine_analysis = await self.analyze_routine(user_id)
        
        if not routine_analysis.get("routine_analyzed"):
            return {
                "optimized": False,
                "message": routine_analysis.get("message", "Impossible d'analyser")
            }
        
        analysis = routine_analysis["analysis"]
        
        # Générer suggestions avec IA
        suggestions = await self._generate_optimization_suggestions(analysis)
        
        return {
            "optimized": True,
            "current_routine": analysis,
            "suggestions": suggestions,
            "potential_time_saved_minutes": self._calculate_time_saved(suggestions)
        }
    
    async def _generate_optimization_suggestions(
        self,
        analysis: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Générer des suggestions d'optimisation avec IA"""
        try:
            prompt = f"""
            Analyse cette routine utilisateur et donne 3-5 suggestions concises pour l'optimiser :
            
            - Interactions par jour: {analysis.get('interactions_per_day', 0):.1f}
            - Heure la plus active: {analysis.get('most_active_hour')}h
            - Catégories utilisées: {', '.join(analysis.get('categories_used', {}).keys())}
            
            Donne des suggestions pratiques et actionnables.
            Format JSON :
            {{
                "suggestions": [
                    {{
                        "title": "Titre",
                        "description": "Description",
                        "impact": "high/medium/low"
                    }}
                ]
            }}
            """
            
            response = await self.ai_router.chat(prompt, max_tokens=500)
            content = response.get("content", "")
            
            # Parser JSON
            import json
            import re
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group(0))
                return data.get("suggestions", [])
        except:
            pass
        
        # Fallback: suggestions basiques
        return [
            {
                "title": "Regrouper les recherches",
                "description": "Effectuer plusieurs recherches en une seule fois",
                "impact": "medium"
            },
            {
                "title": "Utiliser les endpoints agrégés",
                "description": "Utiliser /api/aggregated/* pour informations complètes",
                "impact": "high"
            }
        ]
    
    def _calculate_time_saved(self, suggestions: List[Dict[str, Any]]) -> int:
        """Calculer le temps potentiellement économisé"""
        # Estimation basique: 2 min par suggestion high, 1 min medium, 0.5 min low
        time_saved = 0
        for suggestion in suggestions:
            impact = suggestion.get("impact", "low")
            if impact == "high":
                time_saved += 2
            elif impact == "medium":
                time_saved += 1
            else:
                time_saved += 0.5
        
        return int(time_saved)


# Singleton instance
automation_engine = AutomationEngine()


