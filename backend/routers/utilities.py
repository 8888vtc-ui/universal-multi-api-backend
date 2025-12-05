"""
Utilities API Router
QR Codes, OCR, URL Shorteners
"""
from fastapi import APIRouter, HTTPException, Query, File, UploadFile
from pydantic import BaseModel
from typing import Optional
from services.external_apis.utilities import QRRouter, OCRRouter
import base64

router = APIRouter(prefix="/api/utils", tags=["utilities"])

# Initialize routers
qr_router = QRRouter()
ocr_router = OCRRouter()


class QRRequest(BaseModel):
    text: str
    size: Optional[int] = 300
    format: Optional[str] = 'png'


class OCRRequest(BaseModel):
    image_url: Optional[str] = None
    image_base64: Optional[str] = None
    language: Optional[str] = 'eng'


@router.post("/qr/generate")
async def generate_qr_code(request: QRRequest):
    """
    Generate QR code
    
    Supports: QuickChart, goQR (both free, unlimited)
    """
    try:
        result = await qr_router.generate_qr(
            text=request.text,
            size=request.size,
            format=request.format
        )
        return {"success": True, **result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/ocr/extract")
async def extract_text_from_image(request: OCRRequest):
    """
    Extract text from image using OCR
    
    Supports: OCR.space (500/day), Optiic (free)
    """
    try:
        result = await ocr_router.extract_text(
            image_url=request.image_url,
            image_base64=request.image_base64,
            language=request.language
        )
        return {"success": True, **result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/ocr/upload")
async def upload_and_extract(
    file: UploadFile = File(...),
    language: str = Query('eng', description="Language code")
):
    """Upload image file and extract text"""
    try:
        # Read file and convert to base64
        contents = await file.read()
        image_base64 = base64.b64encode(contents).decode('utf-8')
        
        result = await ocr_router.extract_text(
            image_base64=image_base64,
            language=language
        )
        return {"success": True, **result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/qr/status")
async def get_qr_status():
    """Get QR code router status"""
    try:
        status = qr_router.get_status()
        return {"success": True, **status}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/ocr/status")
async def get_ocr_status():
    """Get OCR router status"""
    try:
        status = ocr_router.get_status()
        return {"success": True, **status}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
