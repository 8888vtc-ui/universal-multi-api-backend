"""
Preference Learner - Apprentissage des préférences utilisateur
Algorithme simple d'apprentissage basé sur fréquence et patterns
"""
from typing import Dict, Any, List, Optional
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from services.assistant.memory_store import memory_store


class PreferenceLearner:
    """Apprentissage des préférences utilisateur"""
    
    def __init__(self):
        self.memory_store = memory_store
    
    def learn_from_interactions(self, user_id: str) -> Dict[str, Any]:
        """
        Apprendre les préférences à partir des interactions
        
        Returns:
            Dict avec préférences apprises par catégorie
        """
        interactions = self.memory_store.get_user_interactions(user_id, limit=1000)
        
        if not interactions:
            return {}
        
        # Analyser les patterns
        preferences = {}
        
        # 1. Catégories préférées (fréquence)
        category_counts = Counter([i['category'] for i in interactions if i.get('category')])
        total = sum(category_counts.values())
        
        if total > 0:
            for category, count in category_counts.most_common(10):
                preferences[category] = {
                    "weight": count / total,
                    "frequency": count,
                    "last_used": self._get_last_use(interactions, category)
                }
        
        # 2. Mots-clés fréquents par catégorie
        keywords_by_category = defaultdict(Counter)
        for interaction in interactions:
            category = interaction.get('category')
            query = interaction.get('query', '')
            if category and query:
                words = query.lower().split()
                keywords_by_category[category].update(words)
        
        # Ajouter keywords aux préférences
        for category, keywords in keywords_by_category.items():
            if category in preferences:
                # Top 10 mots-clés
                top_keywords = [word for word, count in keywords.most_common(10)]
                preferences[category]["keywords"] = top_keywords
        
        # 3. Patterns temporels (jour de la semaine, heure)
        time_patterns = self._analyze_time_patterns(interactions)
        if time_patterns:
            preferences["_time_patterns"] = time_patterns
        
        # Sauvegarder les préférences apprises
        self.memory_store.save_preferences(user_id, preferences)
        
        return preferences
    
    def _get_last_use(self, interactions: List[Dict], category: str) -> Optional[str]:
        """Obtenir la dernière utilisation d'une catégorie"""
        for interaction in interactions:
            if interaction.get('category') == category:
                return interaction.get('timestamp')
        return None
    
    def _analyze_time_patterns(self, interactions: List[Dict]) -> Dict[str, Any]:
        """Analyser les patterns temporels"""
        if not interactions:
            return {}
        
        # Analyser les heures d'utilisation
        hours = []
        days = []
        
        for interaction in interactions:
            timestamp_str = interaction.get('timestamp')
            if timestamp_str:
                try:
                    timestamp = datetime.fromisoformat(timestamp_str)
                    hours.append(timestamp.hour)
                    days.append(timestamp.weekday())  # 0 = lundi
                except:
                    pass
        
        patterns = {}
        
        if hours:
            hour_counter = Counter(hours)
            most_common_hour = hour_counter.most_common(1)[0][0]
            patterns["preferred_hour"] = most_common_hour
        
        if days:
            day_counter = Counter(days)
            most_common_day = day_counter.most_common(1)[0][0]
            patterns["preferred_day"] = most_common_day
        
        return patterns
    
    def get_user_preferences(self, user_id: str) -> Dict[str, Any]:
        """Obtenir les préférences d'un utilisateur"""
        # Si pas de préférences, apprendre depuis interactions
        preferences = self.memory_store.get_preferences(user_id)
        
        if not preferences:
            preferences = self.learn_from_interactions(user_id)
        
        return preferences
    
    def update_preference(
        self,
        user_id: str,
        category: str,
        weight: float,
        keywords: List[str] = None
    ) -> None:
        """Mettre à jour manuellement une préférence"""
        preferences = self.get_user_preferences(user_id)
        
        preferences[category] = {
            "weight": weight,
            "keywords": keywords or [],
            "last_updated": datetime.now().isoformat()
        }
        
        self.memory_store.save_preferences(user_id, preferences)


# Singleton instance
preference_learner = PreferenceLearner()

