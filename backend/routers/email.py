"""
Email API Router
Send emails with fallback
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from services.external_apis.email import EmailRouter

router = APIRouter(prefix="/api/email", tags=["email"])

email_router = EmailRouter()


class EmailRequest(BaseModel):
    to_email: EmailStr
    from_email: EmailStr
    subject: str
    content: str
    content_type: str = 'text/plain'


@router.post("/send")
async def send_email(request: EmailRequest):
    """
    Send email
    
    Supports: SendGrid (100/day), Mailgun (5k/month), Mailjet (6k/month)
    """
    try:
        result = await email_router.send_email(
            to_email=request.to_email,
            from_email=request.from_email,
            subject=request.subject,
            content=request.content,
            content_type=request.content_type
        )
        return {"success": True, **result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status")
async def get_email_status():
    """Get email router status"""
    try:
        status = email_router.get_status()
        return {"success": True, **status}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
