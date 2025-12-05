"""
Greeting Generator - Cartes de vœux vidéo personnalisées
"""
from typing import Dict, Any, Optional, List
from services.video.video_router import video_router
from datetime import datetime


class GreetingGenerator:
    """Générateur de cartes de vœux vidéo"""
    
    def __init__(self):
        self.video_router = video_router
    
    async def create_greeting(
        self,
        occasion: str,
        recipient_name: str,
        sender_name: Optional[str] = None,
        message: Optional[str] = None,
        language: str = "fr",
        avatar_id: str = "anna"
    ) -> Dict[str, Any]:
        """
        Créer une carte de vœux vidéo personnalisée
        
        Args:
            occasion: Type d'occasion (birthday, anniversary, new_year, etc.)
            recipient_name: Nom du destinataire
            sender_name: Nom de l'expéditeur (optionnel)
            message: Message personnalisé (optionnel)
            language: Langue
            avatar_id: Avatar à utiliser
        
        Returns:
            Dict avec video_id, message généré, etc.
        """
        # Générer le message
        greeting_text = self._generate_greeting_text(
            occasion=occasion,
            recipient_name=recipient_name,
            sender_name=sender_name,
            custom_message=message,
            language=language
        )
        
        # Créer la vidéo
        video_result = await self.video_router.create_talking_avatar(
            text=greeting_text,
            avatar_id=avatar_id,
            language=language,
            use_free=False
        )
        
        return {
            "greeting_id": f"greeting_{occasion}_{recipient_name.lower().replace(' ', '_')}",
            "occasion": occasion,
            "recipient": recipient_name,
            "sender": sender_name,
            "message": greeting_text,
            "video_id": video_result.get("video_id"),
            "provider": video_result.get("provider"),
            "created_at": datetime.now().isoformat()
        }
    
    def _generate_greeting_text(
        self,
        occasion: str,
        recipient_name: str,
        sender_name: Optional[str],
        custom_message: Optional[str],
        language: str
    ) -> str:
        """Générer le texte de la carte de vœux"""
        
        # Messages par occasion
        occasion_messages = {
            "birthday": {
                "fr": f"Bon anniversaire {recipient_name} !",
                "en": f"Happy birthday {recipient_name}!",
                "es": f"¡Feliz cumpleaños {recipient_name}!"
            },
            "anniversary": {
                "fr": f"Joyeux anniversaire {recipient_name} !",
                "en": f"Happy anniversary {recipient_name}!",
                "es": f"¡Feliz aniversario {recipient_name}!"
            },
            "new_year": {
                "fr": f"Bonne année {recipient_name} !",
                "en": f"Happy New Year {recipient_name}!",
                "es": f"¡Feliz Año Nuevo {recipient_name}!"
            },
            "christmas": {
                "fr": f"Joyeux Noël {recipient_name} !",
                "en": f"Merry Christmas {recipient_name}!",
                "es": f"¡Feliz Navidad {recipient_name}!"
            },
            "wedding": {
                "fr": f"Félicitations pour votre mariage {recipient_name} !",
                "en": f"Congratulations on your wedding {recipient_name}!",
                "es": f"¡Felicitaciones por tu boda {recipient_name}!"
            },
            "graduation": {
                "fr": f"Félicitations pour votre diplôme {recipient_name} !",
                "en": f"Congratulations on your graduation {recipient_name}!",
                "es": f"¡Felicitaciones por tu graduación {recipient_name}!"
            },
            "custom": {
                "fr": f"Bonjour {recipient_name} !",
                "en": f"Hello {recipient_name}!",
                "es": f"¡Hola {recipient_name}!"
            }
        }
        
        # Message de base selon l'occasion
        base_message = occasion_messages.get(
            occasion,
            occasion_messages["custom"]
        ).get(language, occasion_messages["custom"]["fr"])
        
        # Ajouter message personnalisé si fourni
        if custom_message:
            base_message += f" {custom_message}"
        
        # Ajouter signature si expéditeur fourni
        if sender_name:
            signatures = {
                "fr": f" Avec toute mon affection, {sender_name}.",
                "en": f" With love, {sender_name}.",
                "es": f" Con cariño, {sender_name}."
            }
            base_message += signatures.get(language, signatures["fr"])
        
        # Limiter à 500 caractères
        if len(base_message) > 500:
            base_message = base_message[:497] + "..."
        
        return base_message
    
    def get_available_occasions(self) -> List[Dict[str, str]]:
        """Obtenir les occasions disponibles"""
        return [
            {"id": "birthday", "name": "Anniversaire", "name_en": "Birthday"},
            {"id": "anniversary", "name": "Anniversaire de mariage", "name_en": "Anniversary"},
            {"id": "new_year", "name": "Nouvel An", "name_en": "New Year"},
            {"id": "christmas", "name": "Noël", "name_en": "Christmas"},
            {"id": "wedding", "name": "Mariage", "name_en": "Wedding"},
            {"id": "graduation", "name": "Diplôme", "name_en": "Graduation"},
            {"id": "custom", "name": "Personnalisé", "name_en": "Custom"}
        ]


# Singleton instance
greeting_generator = GreetingGenerator()

