"""
Search History Service - Track and manage user search history
"""
import json
import os
import time
from typing import Dict, Any, List, Optional
from collections import defaultdict
from datetime import datetime

class SearchHistoryService:
    """Service for managing search history"""
    
    def __init__(self, storage_path: str = "data/search_history.json"):
        self.storage_path = storage_path
        self.history: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        self.max_history_per_user = 100
        self._ensure_storage()
        self._load_history()
        print("[OK] Search History Service initialized")
    
    def _ensure_storage(self):
        """Ensure storage directory exists"""
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
    
    def _load_history(self):
        """Load history from file"""
        try:
            if os.path.exists(self.storage_path):
                with open(self.storage_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.history = defaultdict(list, data)
        except Exception as e:
            print(f"[WARN] Could not load search history: {e}")
    
    def _save_history(self):
        """Save history to file"""
        try:
            with open(self.storage_path, 'w', encoding='utf-8') as f:
                json.dump(dict(self.history), f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"[WARN] Could not save search history: {e}")
    
    def add_search(
        self,
        user_id: str,
        query: str,
        search_type: str = "general",
        results_count: int = 0,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Add a search to history"""
        entry = {
            "id": f"{user_id}_{int(time.time() * 1000)}",
            "query": query,
            "type": search_type,
            "results_count": results_count,
            "timestamp": datetime.utcnow().isoformat(),
            "metadata": metadata or {}
        }
        
        # Add to history
        self.history[user_id].insert(0, entry)
        
        # Trim to max history
        if len(self.history[user_id]) > self.max_history_per_user:
            self.history[user_id] = self.history[user_id][:self.max_history_per_user]
        
        # Save
        self._save_history()
        
        return entry
    
    def get_history(
        self,
        user_id: str,
        limit: int = 20,
        search_type: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get search history for a user"""
        history = self.history.get(user_id, [])
        
        if search_type:
            history = [h for h in history if h.get("type") == search_type]
        
        return history[:limit]
    
    def get_popular_searches(
        self,
        limit: int = 10,
        search_type: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get most popular searches across all users"""
        query_counts: Dict[str, int] = defaultdict(int)
        
        for user_history in self.history.values():
            for entry in user_history:
                if search_type and entry.get("type") != search_type:
                    continue
                query_counts[entry["query"].lower()] += 1
        
        # Sort by count
        sorted_queries = sorted(
            query_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )[:limit]
        
        return [
            {"query": q, "count": c}
            for q, c in sorted_queries
        ]
    
    def get_recent_searches(
        self,
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        """Get most recent searches across all users"""
        all_searches = []
        for user_id, user_history in self.history.items():
            for entry in user_history:
                entry_copy = entry.copy()
                entry_copy["user_id"] = user_id
                all_searches.append(entry_copy)
        
        # Sort by timestamp
        all_searches.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
        
        return all_searches[:limit]
    
    def delete_search(self, user_id: str, search_id: str) -> bool:
        """Delete a specific search from history"""
        if user_id not in self.history:
            return False
        
        original_len = len(self.history[user_id])
        self.history[user_id] = [
            h for h in self.history[user_id]
            if h.get("id") != search_id
        ]
        
        if len(self.history[user_id]) < original_len:
            self._save_history()
            return True
        return False
    
    def clear_history(self, user_id: str) -> bool:
        """Clear all history for a user"""
        if user_id in self.history:
            del self.history[user_id]
            self._save_history()
            return True
        return False
    
    def get_stats(self, user_id: Optional[str] = None) -> Dict[str, Any]:
        """Get search statistics"""
        if user_id:
            user_history = self.history.get(user_id, [])
            search_types = defaultdict(int)
            for entry in user_history:
                search_types[entry.get("type", "general")] += 1
            
            return {
                "user_id": user_id,
                "total_searches": len(user_history),
                "search_types": dict(search_types),
                "first_search": user_history[-1]["timestamp"] if user_history else None,
                "last_search": user_history[0]["timestamp"] if user_history else None
            }
        
        # Global stats
        total_searches = sum(len(h) for h in self.history.values())
        total_users = len(self.history)
        
        return {
            "total_users": total_users,
            "total_searches": total_searches,
            "avg_searches_per_user": round(total_searches / max(total_users, 1), 2)
        }


# Singleton instance
search_history_service = SearchHistoryService()






