"""
Video Translator - Traduction de vidéos existantes
"""
from typing import Dict, Any, Optional
import asyncio
from services.video.video_router import video_router
from services.external_apis.translation import TranslationRouter


class VideoTranslator:
    """Traducteur de vidéos"""
    
    def __init__(self):
        self.video_router = video_router
        self.translation_router = TranslationRouter()
    
    async def translate_video(
        self,
        original_text: str,
        target_language: str,
        source_language: Optional[str] = None,
        avatar_id: str = "anna",
        voice_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Traduire et créer une nouvelle vidéo dans une autre langue
        
        Args:
            original_text: Texte original
            target_language: Langue cible (fr, en, es, etc.)
            source_language: Langue source (auto-détectée si None)
            avatar_id: Avatar à utiliser
            voice_id: Voix spécifique (optionnel)
        
        Returns:
            Dict avec video_id traduit, texte traduit, etc.
        """
        # 1. Traduire le texte
        try:
            source_lang = source_language if source_language else "auto"
            translated_result = await self.translation_router.translate(
                text=original_text,
                source_lang=source_lang,
                target_lang=target_language
            )
            translated_text_content = translated_result.get("translation", original_text)
            detected_source_lang = translated_result.get("source_language", source_lang)
        except Exception as e:
            # Fallback: retourner texte original si traduction échoue
            print(f"Translation failed: {e}")
            translated_text_content = original_text
            detected_source_lang = source_language or "auto"
        
        # 2. Déterminer la voix selon la langue
        if not voice_id:
            voice_id = self._get_voice_for_language(target_language)
        
        # 3. Créer la vidéo traduite
        video_result = await self.video_router.create_talking_avatar(
            text=translated_text_content,
            avatar_id=avatar_id,
            voice_id=voice_id,
            language=target_language,
            use_free=False
        )
        
        return {
            "original_text": original_text,
            "translated_text": translated_text_content,
            "source_language": detected_source_lang,
            "target_language": target_language,
            "video_id": video_result.get("video_id"),
            "provider": video_result.get("provider"),
            "voice_id": voice_id
        }
    
    def _get_voice_for_language(self, language: str) -> str:
        """Obtenir une voix par défaut pour une langue"""
        voices = {
            "fr": "fr-FR-DeniseNeural",
            "en": "en-US-AriaNeural",
            "es": "es-ES-ElviraNeural",
            "de": "de-DE-KatjaNeural",
            "it": "it-IT-ElsaNeural",
            "pt": "pt-BR-FranciscaNeural",
            "ja": "ja-JP-NanamiNeural",
            "zh": "zh-CN-XiaoxiaoNeural"
        }
        
        # Prendre les 2 premiers caractères pour le code langue
        lang_code = language[:2].lower()
        return voices.get(lang_code, "en-US-AriaNeural")
    
    async def translate_multiple_languages(
        self,
        original_text: str,
        target_languages: list,
        avatar_id: str = "anna"
    ) -> Dict[str, Any]:
        """
        Traduire une vidéo dans plusieurs langues simultanément
        
        Args:
            original_text: Texte original
            target_languages: Liste de langues cibles (["fr", "en", "es"])
            avatar_id: Avatar à utiliser
        
        Returns:
            Dict avec vidéos dans chaque langue
        """
        # Créer toutes les traductions en parallèle
        translation_tasks = [
            self.translate_video(
                original_text=original_text,
                target_language=lang,
                avatar_id=avatar_id
            )
            for lang in target_languages
        ]
        
        results = await asyncio.gather(*translation_tasks, return_exceptions=True)
        
        videos_by_language = {}
        for lang, result in zip(target_languages, results):
            if isinstance(result, Exception):
                videos_by_language[lang] = {
                    "error": str(result),
                    "success": False
                }
            else:
                videos_by_language[lang] = {
                    **result,
                    "success": True
                }
        
        return {
            "original_text": original_text,
            "videos": videos_by_language,
            "total_languages": len(target_languages),
            "successful": sum(1 for v in videos_by_language.values() if v.get("success", False))
        }


# Singleton instance
video_translator = VideoTranslator()

