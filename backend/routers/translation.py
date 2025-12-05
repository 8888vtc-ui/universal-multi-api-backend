"""
Translation API Router
Endpoints for translation with intelligent fallback
"""
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional
from services.external_apis.translation import TranslationRouter

router = APIRouter(prefix="/api/translation", tags=["translation"])

# Initialize translation router
translation_router = TranslationRouter()


class TranslateRequest(BaseModel):
    text: str
    source_lang: Optional[str] = 'auto'
    target_lang: str = 'en'


class DetectRequest(BaseModel):
    text: str


@router.post("/translate")
async def translate_text(request: TranslateRequest):
    """
    Translate text with automatic provider fallback
    
    Supports: Google Translate, DeepL, Yandex, LibreTranslate
    """
    try:
        result = await translation_router.translate(
            text=request.text,
            source_lang=request.source_lang,
            target_lang=request.target_lang
        )
        return {"success": True, **result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/detect")
async def detect_language(request: DetectRequest):
    """Detect language of text"""
    try:
        result = await translation_router.detect_language(request.text)
        return {"success": True, **result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status")
async def get_translation_status():
    """Get translation router status and quota usage"""
    try:
        status = translation_router.get_status()
        return {"success": True, **status}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/languages")
async def get_supported_languages():
    """Get list of supported languages"""
    # Common language codes supported by most providers
    languages = {
        "ar": "Arabic",
        "zh": "Chinese",
        "en": "English",
        "fr": "French",
        "de": "German",
        "he": "Hebrew",
        "hi": "Hindi",
        "it": "Italian",
        "ja": "Japanese",
        "ko": "Korean",
        "pt": "Portuguese",
        "ru": "Russian",
        "es": "Spanish",
        "tr": "Turkish"
    }
    return {"success": True, "languages": languages}
