"""
Storage Manager pour vidéos temporaires
Stockage local avec nettoyage automatique après 24h
"""
import os
import shutil
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from pathlib import Path


class VideoStorage:
    """Gestionnaire de stockage pour vidéos temporaires"""
    
    def __init__(self, base_path: str = "./storage/videos"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
        self.max_age_hours = 24  # Vidéos supprimées après 24h
    
    def save_video_info(
        self,
        video_id: str,
        provider: str,
        video_url: Optional[str] = None,
        local_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """Sauvegarder les infos d'une vidéo"""
        video_dir = self.base_path / video_id
        video_dir.mkdir(exist_ok=True)
        
        info = {
            "video_id": video_id,
            "provider": provider,
            "video_url": video_url,
            "local_path": local_path,
            "created_at": datetime.now().isoformat(),
            "expires_at": (datetime.now() + timedelta(hours=self.max_age_hours)).isoformat()
        }
        
        # Sauvegarder dans un fichier JSON
        info_file = video_dir / "info.json"
        import json
        with open(info_file, 'w') as f:
            json.dump(info, f, indent=2)
        
        return info
    
    def get_video_info(self, video_id: str) -> Optional[Dict[str, Any]]:
        """Obtenir les infos d'une vidéo"""
        info_file = self.base_path / video_id / "info.json"
        
        if info_file.exists():
            import json
            with open(info_file, 'r') as f:
                return json.load(f)
        return None
    
    def cleanup_expired(self) -> int:
        """Nettoyer les vidéos expirées"""
        cleaned = 0
        now = datetime.now()
        
        for video_dir in self.base_path.iterdir():
            if video_dir.is_dir():
                info_file = video_dir / "info.json"
                if info_file.exists():
                    import json
                    with open(info_file, 'r') as f:
                        info = json.load(f)
                    
                    expires_at = datetime.fromisoformat(info.get("expires_at", "2000-01-01"))
                    if now > expires_at:
                        # Supprimer le dossier
                        shutil.rmtree(video_dir)
                        cleaned += 1
        
        return cleaned
    
    def get_storage_stats(self) -> Dict[str, Any]:
        """Obtenir les statistiques de stockage"""
        total_videos = 0
        total_size = 0
        
        for video_dir in self.base_path.iterdir():
            if video_dir.is_dir():
                total_videos += 1
                # Calculer la taille
                for file in video_dir.rglob("*"):
                    if file.is_file():
                        total_size += file.stat().st_size
        
        return {
            "total_videos": total_videos,
            "total_size_mb": round(total_size / (1024 * 1024), 2),
            "max_age_hours": self.max_age_hours
        }


# Singleton instance
video_storage = VideoStorage()


<<<<<<< Updated upstream
=======





>>>>>>> Stashed changes
