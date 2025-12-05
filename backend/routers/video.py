"""
Video AI Router
Endpoints pour création de vidéos avec avatars IA parlants
"""
from fastapi import APIRouter, HTTPException, Query, BackgroundTasks
from typing import Optional, Dict, Any
from pydantic import BaseModel
from services.video.video_router import video_router
from services.video.queue_manager import video_queue
from services.video.storage_manager import video_storage
from services.video.course_generator import course_generator
from services.video.greeting_generator import greeting_generator
from services.video.video_translator import video_translator
import asyncio

router = APIRouter(prefix="/api/video", tags=["video"])


class CreateAvatarRequest(BaseModel):
    """Request pour créer un avatar parlant"""
    text: str
    avatar_id: str = "anna"
    voice_id: str = "fr-FR-DeniseNeural"
    language: str = "fr"
    use_free: bool = False  # Utiliser solutions gratuites uniquement


class VideoStatusResponse(BaseModel):
    """Response pour statut vidéo"""
    video_id: str
    status: str  # processing, done, error
    result_url: Optional[str] = None
    provider: str
    created_at: Optional[str] = None


@router.post("/avatar/create")
async def create_talking_avatar(request: CreateAvatarRequest, background_tasks: BackgroundTasks):
    """
    🎬 Créer une vidéo avec avatar parlant
    
    Génère une vidéo avec un avatar IA qui prononce le texte fourni.
    
    **Providers disponibles:**
    - D-ID (3$/100 vidéos) - Professionnel, rapide
    - Wav2Lip (gratuit, local) - En développement
    
    **Avatars disponibles:**
    - anna, sara, tom, etc. (D-ID)
    
    **Voix disponibles:**
    - fr-FR-DeniseNeural (Français)
    - en-US-AriaNeural (Anglais)
    - es-ES-ElviraNeural (Espagnol)
    
    **Validation:**
    - Texte: 1-500 caractères
    - Durée estimée: 1-2 minutes
    """
    try:
        # Validation texte
        text = request.text.strip()
        if not text:
            raise HTTPException(
                status_code=400,
                detail="Le texte ne peut pas être vide"
            )
        
        if len(text) > 500:
            raise HTTPException(
                status_code=400,
                detail="Texte trop long (max 500 caractères)"
            )
        
        if len(text) < 1:
            raise HTTPException(
                status_code=400,
                detail="Texte trop court (min 1 caractère)"
            )
        
        # Validation avatar_id
        valid_avatars = ["anna", "sara", "tom", "amy", "josh"]
        if request.avatar_id not in valid_avatars:
            raise HTTPException(
                status_code=400,
                detail=f"Avatar invalide. Disponibles: {', '.join(valid_avatars)}"
            )
        
        # Créer la vidéo
        result = await video_router.create_talking_avatar(
            text=text,
            avatar_id=request.avatar_id,
            voice_id=request.voice_id,
            language=request.language,
            use_free=request.use_free
        )
        
        video_id = result.get("video_id")
        provider = result.get("provider", "d-id")
        
        # Ajouter à la queue
        video_queue.add_to_queue(
            video_id=video_id,
            status="processing",
            provider=provider
        )
        
        # Sauvegarder les infos
        video_storage.save_video_info(
            video_id=video_id,
            provider=provider,
            video_url=result.get("status_url")
        )
        
        # Tâche de fond: vérifier le statut périodiquement
        background_tasks.add_task(check_video_status_periodically, video_id, provider)
        
        return {
            "success": True,
            "video_id": video_id,
            "status_url": result.get("status_url"),
            "provider": provider,
            "message": "Vidéo en cours de génération. Utilisez /status/{video_id} pour vérifier.",
            "estimated_time_seconds": 120  # 2 minutes estimées
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def check_video_status_periodically(video_id: str, provider: str, max_checks: int = 30):
    """Vérifier le statut d'une vidéo périodiquement en arrière-plan"""
    for i in range(max_checks):
        await asyncio.sleep(10)  # Attendre 10 secondes entre chaque vérification
        
        try:
            status = await video_router.get_video_status(video_id, provider)
            current_status = status.get("status", "unknown")
            
            # Mettre à jour la queue
            video_queue.update_status(
                video_id=video_id,
                status=current_status,
                result_url=status.get("result_url")
            )
            
            # Si terminé, mettre à jour le stockage
            if current_status == "done":
                result_url = status.get("result_url")
                if result_url:
                    video_storage.save_video_info(
                        video_id=video_id,
                        provider=provider,
                        video_url=result_url
                    )
                break
            
            if current_status == "error":
                break
        
        except Exception as e:
            print(f"Error checking video status: {e}")
            break


@router.get("/status/{video_id}")
async def get_video_status(
    video_id: str,
    provider: str = Query("d-id", description="Provider utilisé (d-id, wav2lip)")
):
    """
    📊 Obtenir le statut d'une vidéo
    
    Vérifie si la vidéo est prête et retourne l'URL de téléchargement si disponible.
    
    **Status possibles:**
    - `processing`: Vidéo en cours de génération
    - `done`: Vidéo prête (result_url disponible)
    - `error`: Erreur lors de la génération
    """
    try:
        # Vérifier d'abord dans la queue locale
        queue_status = video_queue.get_status(video_id)
        
        if queue_status and queue_status.get("status") == "done":
            # Retourner depuis la queue
            storage_info = video_storage.get_video_info(video_id)
            return VideoStatusResponse(
                video_id=video_id,
                status="done",
                result_url=storage_info.get("video_url") if storage_info else None,
                provider=provider,
                created_at=queue_status.get("created_at")
            )
        
        # Sinon, vérifier avec le provider
        status = await video_router.get_video_status(video_id, provider)
        current_status = status.get("status", "unknown")
        
        # Mettre à jour la queue
        video_queue.update_status(
            video_id=video_id,
            status=current_status,
            result_url=status.get("result_url")
        )
        
        # Si terminé, sauvegarder
        if current_status == "done":
            result_url = status.get("result_url")
            if result_url:
                video_storage.save_video_info(
                    video_id=video_id,
                    provider=provider,
                    video_url=result_url
                )
        
        return VideoStatusResponse(
            video_id=video_id,
            status=current_status,
            result_url=status.get("result_url"),
            provider=status.get("provider", provider),
            created_at=status.get("created_at")
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/audio/generate")
async def generate_audio(
    text: str = Query(..., description="Texte à convertir en audio"),
    language: str = Query("fr", description="Langue (fr, en, es, etc.)")
):
    """
    🔊 Générer audio à partir de texte
    
    Utilise Coqui TTS (gratuit) ou ElevenLabs si disponible.
    """
    try:
        result = await video_router.generate_audio(text, language)
        return {
            "success": True,
            "audio_path": result.get("audio_path"),
            "provider": result.get("provider"),
            "format": result.get("format")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status")
async def get_video_service_status():
    """
    ℹ️ Obtenir le statut du service vidéo
    
    Retourne les providers disponibles, leur statut, et les statistiques de la queue.
    """
    status = video_router.get_status()
    queue_stats = video_queue.get_queue_stats()
    storage_stats = video_storage.get_storage_stats()
    
    return {
        "service": "Video AI",
        "available": len(status["providers"]) > 0,
        **status,
        "queue": queue_stats,
        "storage": storage_stats
    }


@router.get("/voices")
async def get_available_voices(
    language: str = Query("fr", description="Langue pour filtrer les voix")
):
    """
    🎤 Obtenir les voix disponibles
    
    Liste toutes les voix TTS disponibles pour une langue donnée.
    """
    try:
        from services.video.tts_provider import tts_provider
        voices = tts_provider.get_available_voices(language)
        return {
            "voices": voices,
            "language": language,
            "total": len(voices)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/cleanup")
async def cleanup_expired_videos():
    """
    🧹 Nettoyer les vidéos expirées
    
    Supprime automatiquement les vidéos de plus de 24h.
    """
    try:
        cleaned_videos = video_storage.cleanup_expired()
        cleaned_queue = video_queue._cleanup_old_entries()
        
        return {
            "success": True,
            "cleaned_videos": cleaned_videos,
            "message": f"{cleaned_videos} vidéos expirées supprimées"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/")
async def video_info():
    """
    📚 Informations sur le service vidéo
    """
    return {
        "service": "Video AI - Avatars Parlants",
        "version": "1.0.0",
        "description": "Service pour créer des vidéos avec avatars IA parlants",
        "features": [
            "Avatars parlants (D-ID)",
            "Text-to-Speech (Coqui TTS, ElevenLabs)",
            "Multi-langues",
            "Fallback automatique"
        ],
        "endpoints": {
            "create": "/api/video/avatar/create",
            "status": "/api/video/status/{video_id}",
            "audio": "/api/video/audio/generate",
            "voices": "/api/video/voices"
        },
        "pricing": {
            "free": "5 vidéos/mois (30 sec max) - Wav2Lip",
            "basic": "9€/mois - 50 vidéos (D-ID)",
            "pro": "29€/mois - 500 vidéos (D-ID)",
            "api": "0.10€/vidéo (D-ID)"
        }
    }

