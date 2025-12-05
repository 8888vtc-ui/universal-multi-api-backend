"""
Queue Manager pour générations vidéo asynchrones
"""
import asyncio
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import json


class VideoQueue:
    """Gestionnaire de queue pour générations vidéo"""
    
    def __init__(self):
        self.queue: Dict[str, Dict[str, Any]] = {}
        self.max_queue_size = 100
        self.cleanup_interval = 3600  # 1 heure
    
    def add_to_queue(
        self,
        video_id: str,
        status: str = "processing",
        provider: str = "d-id",
        created_at: Optional[datetime] = None
    ) -> None:
        """Ajouter une vidéo à la queue"""
        if len(self.queue) >= self.max_queue_size:
            # Nettoyer les anciennes entrées
            self._cleanup_old_entries()
        
        self.queue[video_id] = {
            "video_id": video_id,
            "status": status,
            "provider": provider,
            "created_at": created_at or datetime.now(),
            "updated_at": datetime.now()
        }
    
    def update_status(
        self,
        video_id: str,
        status: str,
        result_url: Optional[str] = None
    ) -> bool:
        """Mettre à jour le statut d'une vidéo"""
        if video_id in self.queue:
            self.queue[video_id]["status"] = status
            self.queue[video_id]["updated_at"] = datetime.now()
            if result_url:
                self.queue[video_id]["result_url"] = result_url
            return True
        return False
    
    def get_status(self, video_id: str) -> Optional[Dict[str, Any]]:
        """Obtenir le statut d'une vidéo"""
        if video_id in self.queue:
            entry = self.queue[video_id].copy()
            # Convertir datetime en string pour JSON
            entry["created_at"] = entry["created_at"].isoformat()
            entry["updated_at"] = entry["updated_at"].isoformat()
            return entry
        return None
    
    def _cleanup_old_entries(self, max_age_hours: int = 24) -> int:
        """Nettoyer les entrées anciennes"""
        now = datetime.now()
        to_remove = []
        
        for video_id, entry in self.queue.items():
            age = now - entry["created_at"]
            if age > timedelta(hours=max_age_hours):
                to_remove.append(video_id)
        
        for video_id in to_remove:
            del self.queue[video_id]
        
        return len(to_remove)
    
    def get_queue_stats(self) -> Dict[str, Any]:
        """Obtenir les statistiques de la queue"""
        status_counts = {}
        for entry in self.queue.values():
            status = entry["status"]
            status_counts[status] = status_counts.get(status, 0) + 1
        
        return {
            "total": len(self.queue),
            "by_status": status_counts,
            "max_size": self.max_queue_size
        }


# Singleton instance
video_queue = VideoQueue()

