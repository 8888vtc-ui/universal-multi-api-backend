"""
D-ID Provider - Avatars parlants
Coût: 3$/100 vidéos
"""
import os
import httpx
import base64
from typing import Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()


class DIDProvider:
    """D-ID API provider pour avatars parlants"""
    
    def __init__(self):
        self.api_key = os.getenv("DID_API_KEY")
        self.base_url = "https://api.d-id.com"
        self.available = bool(self.api_key and self.api_key != "your_did_api_key_here")
        
        if self.available:
            print("[OK] D-ID provider initialized")
        else:
            print("[WARN] D-ID not available (no API key)")
    
    async def create_talking_avatar(
        self,
        text: str,
        avatar_id: str = "anna",
        voice_id: str = "fr-FR-DeniseNeural",
        language: str = "fr"
    ) -> Dict[str, Any]:
        """
        Créer une vidéo avec avatar parlant
        
        Args:
            text: Texte à prononcer
            avatar_id: ID de l'avatar (anna, sara, etc.)
            voice_id: ID de la voix
            language: Langue (fr, en, es, etc.)
        
        Returns:
            Dict avec video_id, status_url, etc.
        """
        if not self.available:
            raise Exception("D-ID API key not configured")
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            # Encoder l'API key en base64 pour Basic auth
            auth_string = base64.b64encode(f"{self.api_key}:".encode()).decode()
            
            # Créer la requête de génération
            response = await client.post(
                f"{self.base_url}/talks",
                headers={
                    "Authorization": f"Basic {auth_string}",
                    "Content-Type": "application/json"
                },
                json={
                    "source_url": f"https://d-id-public-bucket.s3.amazonaws.com/{avatar_id}.jpg",
                    "script": {
                        "type": "text",
                        "input": text,
                        "provider": {
                            "type": "microsoft",
                            "voice_id": voice_id
                        },
                        "ssml": False
                    },
                    "config": {
                        "stitch": True,
                        "result_format": "mp4"
                    }
                }
            )
            
            if response.status_code == 201:
                data = response.json()
                return {
                    "video_id": data.get("id"),
                    "status_url": data.get("status_url"),
                    "created_at": data.get("created_at"),
                    "provider": "d-id"
                }
            else:
                raise Exception(f"D-ID API error: {response.status_code} - {response.text}")
    
    async def get_video_status(self, video_id: str) -> Dict[str, Any]:
        """Obtenir le statut d'une vidéo"""
        if not self.available:
            raise Exception("D-ID API key not configured")
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            auth_string = base64.b64encode(f"{self.api_key}:".encode()).decode()
            response = await client.get(
                f"{self.base_url}/talks/{video_id}",
                headers={
                    "Authorization": f"Basic {auth_string}"
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "status": data.get("status"),  # done, error, processing
                    "result_url": data.get("result_url"),
                    "created_at": data.get("created_at"),
                    "provider": "d-id"
                }
            else:
                raise Exception(f"D-ID status error: {response.status_code}")
    
    async def get_video_url(self, video_id: str) -> Optional[str]:
        """Obtenir l'URL de téléchargement de la vidéo"""
        status = await self.get_video_status(video_id)
        if status["status"] == "done":
            return status.get("result_url")
        return None


# Singleton instance
did_provider = DIDProvider()

