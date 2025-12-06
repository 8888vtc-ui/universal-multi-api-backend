"""
Webhooks API Router
Discord, Slack webhooks for notifications
"""
from fastapi import APIRouter, HTTPException, Body
from services.external_apis.webhooks.discord import DiscordWebhookProvider
from services.external_apis.webhooks.slack import SlackWebhookProvider
from typing import Optional, Dict, Any
from pydantic import BaseModel

router = APIRouter(prefix="/api/webhooks", tags=["webhooks"])

discord_provider = DiscordWebhookProvider()
slack_provider = SlackWebhookProvider()


class DiscordMessageRequest(BaseModel):
    webhook_url: str
    content: str
    username: Optional[str] = None
    avatar_url: Optional[str] = None


class DiscordEmbedRequest(BaseModel):
    webhook_url: str
    title: str
    description: str
    color: Optional[int] = None
    fields: Optional[list] = None
    footer: Optional[Dict[str, str]] = None


@router.post("/discord/message")
async def send_discord_message(request: DiscordMessageRequest):
    """Send message to Discord webhook"""
    try:
        result = await discord_provider.send_message(
            webhook_url=request.webhook_url,
            content=request.content,
            username=request.username,
            avatar_url=request.avatar_url
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/discord/embed")
async def send_discord_embed(request: DiscordEmbedRequest):
    """Send embed message to Discord webhook"""
    try:
        result = await discord_provider.send_embed(
            webhook_url=request.webhook_url,
            title=request.title,
            description=request.description,
            color=request.color,
            fields=request.fields,
            footer=request.footer
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class SlackMessageRequest(BaseModel):
    webhook_url: str
    text: str
    channel: Optional[str] = None
    username: Optional[str] = None


@router.post("/slack/message")
async def send_slack_message(request: SlackMessageRequest):
    """Send message to Slack webhook"""
    try:
        result = await slack_provider.send_message(
            webhook_url=request.webhook_url,
            text=request.text,
            channel=request.channel,
            username=request.username
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/slack/rich")
async def send_slack_rich(
    webhook_url: str = Body(..., description="Slack Webhook URL"),
    blocks: list = Body(..., description="Slack blocks array"),
    channel: Optional[str] = Body(None, description="Channel override")
):
    """Send rich message with blocks to Slack webhook"""
    try:
        result = await slack_provider.send_rich_message(webhook_url, blocks, channel)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

