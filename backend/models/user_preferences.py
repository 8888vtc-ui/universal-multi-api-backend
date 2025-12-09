"""
User Preferences Models
Modèles pour stocker les préférences et interactions utilisateur
"""
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from datetime import datetime


class UserInteraction(BaseModel):
    """Interaction utilisateur"""
    timestamp: datetime
    query: str
    category: str  # finance, news, weather, etc.
    action: str  # search, click, like, etc.
    result_id: Optional[str] = None
    feedback: Optional[str] = None  # positive, negative, neutral


class UserPreference(BaseModel):
    """Préférence utilisateur"""
    category: str
    keywords: List[str]
    weight: float  # 0.0 à 1.0
    last_updated: datetime


class UserProfile(BaseModel):
    """Profil utilisateur complet"""
    user_id: str
    preferences: Dict[str, UserPreference]
    interactions: List[UserInteraction]
    learned_patterns: Dict[str, Any]
    created_at: datetime
    last_updated: datetime
