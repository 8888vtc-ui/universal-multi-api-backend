"""
Input Sanitization Service
Protection contre XSS, SQL Injection, et autres attaques
"""
import re
import html
import logging
from typing import Any, Optional, Dict, List, Union
import unicodedata

logger = logging.getLogger(__name__)


def sanitize(value: str, max_length: int = 10000) -> str:
    """
    Quick sanitization function for common use
    
    Usage:
        from services.sanitizer import sanitize
        clean_text = sanitize(user_input, max_length=5000)
    """
    return Sanitizer.sanitize_string(value, max_length)


class Sanitizer:
    """Service de sanitization des inputs"""
    
    # Patterns dangereux
    SQL_INJECTION_PATTERNS = [
        r"(\b(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|TRUNCATE)\b)",
        r"(--)",
        r"(/\*.*\*/)",
        r"(\b(OR|AND)\b\s+\d+\s*=\s*\d+)",
        r"('\s*(OR|AND)\s+')",
        r"(;\s*(SELECT|INSERT|UPDATE|DELETE|DROP))",
    ]
    
    XSS_PATTERNS = [
        r"<script[^>]*>.*?</script>",
        r"javascript:",
        r"on\w+\s*=",
        r"<iframe[^>]*>",
        r"<object[^>]*>",
        r"<embed[^>]*>",
        r"<link[^>]*>",
        r"<meta[^>]*>",
    ]
    
    # Caractères de contrôle dangereux
    DANGEROUS_CHARS = [
        '\x00', '\x01', '\x02', '\x03', '\x04', '\x05', '\x06', '\x07',
        '\x08', '\x0b', '\x0c', '\x0e', '\x0f', '\x10', '\x11', '\x12',
        '\x13', '\x14', '\x15', '\x16', '\x17', '\x18', '\x19', '\x1a',
        '\x1b', '\x1c', '\x1d', '\x1e', '\x1f', '\x7f'
    ]
    
    @classmethod
    def sanitize_string(cls, value: str, max_length: int = 10000) -> str:
        """
        Sanitize une chaîne de caractères
        
        - Échappe les caractères HTML
        - Supprime les caractères de contrôle
        - Limite la longueur
        - Normalise Unicode
        """
        if not isinstance(value, str):
            return str(value)
        
        # Limiter la longueur
        value = value[:max_length]
        
        # Normaliser Unicode (NFC)
        value = unicodedata.normalize('NFC', value)
        
        # Supprimer les caractères de contrôle
        for char in cls.DANGEROUS_CHARS:
            value = value.replace(char, '')
        
        # Échapper HTML
        value = html.escape(value, quote=True)
        
        return value.strip()
    
    @classmethod
    def sanitize_html(cls, value: str) -> str:
        """
        Sanitize HTML - supprime tous les tags
        """
        # Supprimer tous les tags HTML
        clean = re.sub(r'<[^>]+>', '', value)
        return cls.sanitize_string(clean)
    
    @classmethod
    def check_sql_injection(cls, value: str) -> bool:
        """
        Vérifier si la valeur contient des patterns SQL injection
        Retourne True si suspect
        """
        for pattern in cls.SQL_INJECTION_PATTERNS:
            if re.search(pattern, value, re.IGNORECASE):
                return True
        return False
    
    @classmethod
    def check_xss(cls, value: str) -> bool:
        """
        Vérifier si la valeur contient des patterns XSS
        Retourne True si suspect
        """
        for pattern in cls.XSS_PATTERNS:
            if re.search(pattern, value, re.IGNORECASE):
                return True
        return False
    
    @classmethod
    def sanitize_dict(cls, data: Dict[str, Any], max_depth: int = 10) -> Dict[str, Any]:
        """Sanitize récursivement un dictionnaire"""
        if max_depth <= 0:
            return {}
        
        result = {}
        for key, value in data.items():
            # Sanitize la clé
            clean_key = cls.sanitize_string(str(key), max_length=100)
            
            # Sanitize la valeur selon son type
            if isinstance(value, str):
                result[clean_key] = cls.sanitize_string(value)
            elif isinstance(value, dict):
                result[clean_key] = cls.sanitize_dict(value, max_depth - 1)
            elif isinstance(value, list):
                result[clean_key] = cls.sanitize_list(value, max_depth - 1)
            else:
                result[clean_key] = value
        
        return result
    
    @classmethod
    def sanitize_list(cls, data: List[Any], max_depth: int = 10) -> List[Any]:
        """Sanitize récursivement une liste"""
        if max_depth <= 0:
            return []
        
        result = []
        for item in data:
            if isinstance(item, str):
                result.append(cls.sanitize_string(item))
            elif isinstance(item, dict):
                result.append(cls.sanitize_dict(item, max_depth - 1))
            elif isinstance(item, list):
                result.append(cls.sanitize_list(item, max_depth - 1))
            else:
                result.append(item)
        
        return result
    
    @classmethod
    def sanitize_email(cls, email: str) -> str:
        """Sanitize et valider un email"""
        email = cls.sanitize_string(email, max_length=254)
        email = email.lower().strip()
        
        # Pattern email basique
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            raise ValueError("Invalid email format")
        
        return email
    
    @classmethod
    def sanitize_url(cls, url: str) -> str:
        """Sanitize une URL"""
        url = cls.sanitize_string(url, max_length=2048)
        
        # Vérifier le protocole
        if not url.startswith(('http://', 'https://')):
            raise ValueError("URL must start with http:// or https://")
        
        # Vérifier les patterns dangereux
        dangerous = ['javascript:', 'data:', 'vbscript:']
        for d in dangerous:
            if d in url.lower():
                raise ValueError(f"Dangerous URL pattern: {d}")
        
        return url
    
    @classmethod
    def sanitize_filename(cls, filename: str) -> str:
        """Sanitize un nom de fichier"""
        # Supprimer les caractères dangereux pour les systèmes de fichiers
        dangerous_chars = ['/', '\\', '..', '<', '>', ':', '"', '|', '?', '*', '\x00']
        
        for char in dangerous_chars:
            filename = filename.replace(char, '_')
        
        # Limiter la longueur
        return cls.sanitize_string(filename, max_length=255)
    
    @classmethod
    def validate_and_sanitize(cls, value: str, field_type: str = "text") -> str:
        """
        Valide et sanitize selon le type de champ
        
        Args:
            value: Valeur à sanitizer
            field_type: Type de champ (text, email, url, filename, html)
        """
        if field_type == "email":
            return cls.sanitize_email(value)
        elif field_type == "url":
            return cls.sanitize_url(value)
        elif field_type == "filename":
            return cls.sanitize_filename(value)
        elif field_type == "html":
            return cls.sanitize_html(value)
        else:
            return cls.sanitize_string(value)


# Singleton
sanitizer = Sanitizer()


# Helper functions
def sanitize(value: str, max_length: int = 10000) -> str:
    """Sanitize une chaîne"""
    return sanitizer.sanitize_string(value, max_length)


def sanitize_dict(data: Dict[str, Any]) -> Dict[str, Any]:
    """Sanitize un dictionnaire"""
    return sanitizer.sanitize_dict(data)


def is_safe(value: str) -> bool:
    """Vérifier si une valeur est safe (pas de XSS/SQL injection)"""
    return not sanitizer.check_sql_injection(value) and not sanitizer.check_xss(value)

