"""
Video Router - Gestion intelligente des providers vidéo
Fallback automatique entre D-ID et Wav2Lip
"""
import os
from typing import Dict, Any, Optional
from .did_provider import did_provider
from .tts_provider import tts_provider


class VideoRouter:
    """Router intelligent pour génération vidéo avec fallback"""
    
    def __init__(self):
        self.providers = []
        self._init_providers()
    
    def _init_providers(self):
        """Initialiser les providers disponibles"""
        # D-ID (payant mais professionnel)
        if did_provider.available:
            self.providers.append({
                "name": "d-id",
                "instance": did_provider,
                "priority": 1,
                "cost_per_video": 0.03  # 3$/100 vidéos
            })
        
        # Wav2Lip (gratuit, local - à implémenter)
        # TODO: Implémenter Wav2Lip local
        self.wav2lip_available = False
        
        if not self.providers:
            print("⚠️  No video providers available")
    
    async def create_talking_avatar(
        self,
        text: str,
        avatar_id: str = "anna",
        voice_id: str = "fr-FR-DeniseNeural",
        language: str = "fr",
        use_free: bool = False
    ) -> Dict[str, Any]:
        """
        Créer une vidéo avec avatar parlant
        
        Args:
            text: Texte à prononcer
            avatar_id: ID de l'avatar
            voice_id: ID de la voix
            language: Langue
            use_free: Forcer l'utilisation de solutions gratuites
        
        Returns:
            Dict avec video_id, status_url, etc.
        """
        # Si use_free, essayer Wav2Lip d'abord
        if use_free and self.wav2lip_available:
            # TODO: Implémenter Wav2Lip
            pass
        
        # Utiliser D-ID si disponible
        if did_provider.available:
            try:
                result = await did_provider.create_talking_avatar(
                    text=text,
                    avatar_id=avatar_id,
                    voice_id=voice_id,
                    language=language
                )
                return result
            except Exception as e:
                print(f"⚠️  D-ID failed: {e}")
                # Fallback vers Wav2Lip si disponible
                if self.wav2lip_available:
                    # TODO: Implémenter fallback Wav2Lip
                    pass
        
        raise Exception("No video provider available")
    
    async def get_video_status(self, video_id: str, provider: str = "d-id") -> Dict[str, Any]:
        """Obtenir le statut d'une vidéo"""
        if provider == "d-id" and did_provider.available:
            return await did_provider.get_video_status(video_id)
        
        raise Exception(f"Provider {provider} not available")
    
    async def generate_audio(
        self,
        text: str,
        language: str = "fr"
    ) -> Dict[str, Any]:
        """Générer audio à partir de texte"""
        return await tts_provider.generate_speech(text, language)
    
    def get_status(self) -> Dict[str, Any]:
        """Obtenir le statut du router"""
        return {
            "providers": [p["name"] for p in self.providers],
            "d_id_available": did_provider.available,
            "wav2lip_available": self.wav2lip_available,
            "tts_available": tts_provider.coqui_available or tts_provider.elevenlabs_available
        }


# Singleton instance
video_router = VideoRouter()


