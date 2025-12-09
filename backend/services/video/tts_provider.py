"""
Text-to-Speech Providers
Support pour Coqui TTS (gratuit) et ElevenLabs (déjà intégré)
"""
import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()


class TTSProvider:
    """Provider TTS avec fallback"""
    
    def __init__(self):
        self.providers = []
        self._init_providers()
    
    def _init_providers(self):
        """Initialiser les providers TTS disponibles"""
        # Coqui TTS (gratuit, local)
        try:
            from TTS.api import TTS
            self.coqui_available = True
            self.coqui_tts = TTS(model_name="tts_models/fr/css10/vits", progress_bar=False)
            self.providers.append("coqui")
            print("[OK] Coqui TTS initialized")
        except ImportError:
            self.coqui_available = False
            print("[WARN] Coqui TTS not available (install: pip install TTS)")
        
        # ElevenLabs (si disponible)
        elevenlabs_key = os.getenv("ELEVENLABS_API_KEY")
        if elevenlabs_key and elevenlabs_key != "your_elevenlabs_api_key_here":
            self.elevenlabs_available = True
            self.providers.append("elevenlabs")
            print("[OK] ElevenLabs TTS available")
        else:
            self.elevenlabs_available = False
    
    async def generate_speech(
        self,
        text: str,
        language: str = "fr",
        voice: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Générer audio à partir de texte
        
        Args:
            text: Texte à convertir
            language: Langue (fr, en, es, etc.)
            voice: ID de la voix (optionnel)
        
        Returns:
            Dict avec audio_url ou audio_data
        """
        # Essayer Coqui TTS d'abord (gratuit)
        if self.coqui_available:
            try:
                import tempfile
                import os
                
                # Générer audio avec Coqui
                with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
                    output_path = tmp_file.name
                
                self.coqui_tts.tts_to_file(
                    text=text,
                    file_path=output_path,
                    language=language[:2] if len(language) >= 2 else "fr"
                )
                
                return {
                    "audio_path": output_path,
                    "provider": "coqui",
                    "format": "wav"
                }
            except Exception as e:
                print(f"[WARN] Coqui TTS failed: {e}")
        
        # Fallback vers ElevenLabs si disponible
        if self.elevenlabs_available:
            try:
                from services.external_apis import elevenlabs  # Si intégré
                # Utiliser ElevenLabs
                # TODO: Intégrer ElevenLabs si disponible
                pass
            except:
                pass
        
        raise Exception("No TTS provider available")
    
    def get_available_voices(self, language: str = "fr") -> list:
        """Obtenir les voix disponibles"""
        voices = []
        
        if self.coqui_available:
            voices.append({
                "id": f"coqui-{language}",
                "name": f"Coqui {language.upper()}",
                "provider": "coqui"
            })
        
        if self.elevenlabs_available:
            voices.append({
                "id": "elevenlabs-default",
                "name": "ElevenLabs Default",
                "provider": "elevenlabs"
            })
        
        return voices


# Singleton instance
tts_provider = TTSProvider()
