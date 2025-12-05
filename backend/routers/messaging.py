"""
Messaging API Router
Endpoints for Telegram, LINE, Kakao messaging
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
from services.external_apis.messaging import MessagingRouter

router = APIRouter(prefix="/api/messaging", tags=["messaging"])

# Initialize messaging router
messaging_router = MessagingRouter()


class SendMessageRequest(BaseModel):
    platform: str
    chat_id: str
    text: str
    parse_mode: Optional[str] = None
    reply_markup: Optional[Dict[str, Any]] = None


@router.post("/send")
async def send_message(request: SendMessageRequest):
    """
    Send message via messaging platform
    
    Supported platforms: telegram, line (future), kakao (future)
    """
    try:
        result = await messaging_router.send_message(
            platform=request.platform,
            chat_id=request.chat_id,
            text=request.text,
            parse_mode=request.parse_mode,
            reply_markup=request.reply_markup
        )
        return {"success": True, **result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{platform}/info")
async def get_bot_info(platform: str):
    """Get bot information for specified platform"""
    try:
        result = await messaging_router.get_bot_info(platform)
        return {"success": True, **result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status")
async def get_messaging_status():
    """Get messaging router status"""
    try:
        status = messaging_router.get_status()
        return {"success": True, **status}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/platforms")
async def get_available_platforms():
    """Get list of available messaging platforms"""
    status = messaging_router.get_status()
    return {
        "success": True,
        "platforms": status['available'],
        "count": status['platforms']
    }
