"""
Context Helpers
Provides common context data for AI prompts (date, time, language, etc.)
"""
from datetime import datetime
import locale
import re
from typing import Optional

# Supported languages
SUPPORTED_LANGUAGES = {
    'fr': {'name': 'Français', 'code': 'fr_FR'},
    'en': {'name': 'English', 'code': 'en_US'},
    'es': {'name': 'Español', 'code': 'es_ES'},
    'de': {'name': 'Deutsch', 'code': 'de_DE'},
    'it': {'name': 'Italiano', 'code': 'it_IT'},
    'pt': {'name': 'Português', 'code': 'pt_BR'},
    'ar': {'name': 'العربية', 'code': 'ar_SA'},
    'he': {'name': 'עברית', 'code': 'he_IL'},
    'zh': {'name': '中文', 'code': 'zh_CN'},
    'ja': {'name': '日本語', 'code': 'ja_JP'},
    'ru': {'name': 'Русский', 'code': 'ru_RU'},
}

# Language detection patterns
LANGUAGE_PATTERNS = {
    'fr': [r'\b(bonjour|salut|merci|comment|pourquoi|quoi|quand|où|quel|quelle|est-ce|désolé|peux|peut|voulez|vous|tu|nous|ils|elles)\b', r'[àâäéèêëîïôûùüÿç]'],
    'en': [r'\b(hello|hi|hey|thanks|thank|what|why|when|where|how|which|could|would|should|please|tell|best|investment|invest|what is|what are|can you|will you|great|good|propose|suggest|help|lose|weight|want|need|looking|for)\b'],
    'es': [r'\b(hola|gracias|qué|por qué|cuándo|dónde|cómo|cuál)\b', r'[áéíóúüñ¿¡]'],
    'de': [r'\b(hallo|danke|was|warum|wann|wo|wie|welch)\b', r'[äöüß]'],
    'it': [r'\b(ciao|grazie|cosa|perché|quando|dove|come|quale)\b', r'[àèéìíîòóùú]'],
    'pt': [r'\b(olá|obrigado|que|por que|quando|onde|como|qual)\b', r'[ãõáéíóú]'],
    'ar': [r'[\u0600-\u06FF]'],  # Arabic script
    'he': [r'[\u0590-\u05FF]'],  # Hebrew script
    'zh': [r'[\u4e00-\u9fff]'],  # Chinese characters
    'ja': [r'[\u3040-\u30ff\u4e00-\u9fff]'],  # Japanese (hiragana, katakana, kanji)
    'ru': [r'[\u0400-\u04FF]'],  # Cyrillic
}


def detect_language(text: str) -> str:
    """
    Auto-detect language from text based on patterns
    Returns language code (fr, en, es, etc.)
    """
    text_lower = text.lower()
    
    # Score each language
    scores = {}
    for lang, patterns in LANGUAGE_PATTERNS.items():
        score = 0
        for pattern in patterns:
            matches = re.findall(pattern, text_lower, re.IGNORECASE | re.UNICODE)
            score += len(matches)
        scores[lang] = score
    
    # Return language with highest score, default to French
    if not any(scores.values()):
        return 'fr'
    
    return max(scores, key=scores.get)


def get_language_instruction(language: str) -> str:
    """
    Get instruction for AI to respond in specific language
    CRITICAL: This instruction is added to ALL expert prompts to ensure multilingual support
    """
    instructions = {
        'fr': "CRITIQUE - LANGUE: Tu DOIS répondre UNIQUEMENT en Français. N'utilise JAMAIS d'autres langues dans ta réponse. Utilise un ton naturel et conversationnel.",
        'en': "CRITICAL - LANGUAGE: You MUST respond ONLY in English. NEVER use other languages in your response. Use a natural and conversational tone.",
        'es': "CRÍTICO - IDIOMA: DEBES responder SOLO en Español. NUNCA uses otros idiomas en tu respuesta. Usa un tono natural y conversacional.",
        'de': "KRITISCH - SPRACHE: Du MUSST NUR auf Deutsch antworten. Verwende NIEMALS andere Sprachen in deiner Antwort. Verwende einen natürlichen und gesprächigen Ton.",
        'it': "CRITICO - LINGUA: Devi rispondere SOLO in Italiano. NON usare MAI altre lingue nella tua risposta. Usa un tono naturale e conversazionale.",
        'pt': "CRÍTICO - IDIOMA: Você DEVE responder APENAS em Português. NUNCA use outros idiomas em sua resposta. Use um tom natural e conversacional.",
        'ar': "حرج - اللغة: يجب أن ترد باللغة العربية فقط. لا تستخدم أبدًا لغات أخرى في ردك. استخدم نبرة طبيعية ومحادثة.",
        'he': "קריטי - שפה: עליך להשיב בעברית בלבד. לעולם אל תשתמש בשפות אחרות בתשובתך. השתמש בטון טבעי ושיחתי.",
        'zh': "关键 - 语言：你必须只用中文回复。永远不要在回复中使用其他语言。使用自然和对话的语气。",
        'ja': "重要 - 言語：日本語でのみ回答してください。回答で他の言語を使用しないでください。自然で会話的なトーンを使用してください。",
        'ru': "КРИТИЧНО - ЯЗЫК: Вы ДОЛЖНЫ отвечать ТОЛЬКО на русском языке. НИКОГДА не используйте другие языки в ответе. Используйте естественный и разговорный тон.",
    }
    return instructions.get(language, instructions['fr'])


def get_current_datetime_context(language: str = 'fr') -> str:
    """
    Returns a formatted string with current date and time
    in the specified language.
    
    This ensures all AI experts know the current date/time
    and can answer questions like "What happened today?" correctly.
    """
    now = datetime.now()
    
    # Date formatting by language
    date_formats = {
        'fr': f"{get_day_name(now.weekday(), 'fr')} {now.day} {get_month_name(now.month, 'fr')} {now.year}",
        'en': f"{get_day_name(now.weekday(), 'en')}, {get_month_name(now.month, 'en')} {now.day}, {now.year}",
        'es': f"{get_day_name(now.weekday(), 'es')} {now.day} de {get_month_name(now.month, 'es')} de {now.year}",
        'de': f"{get_day_name(now.weekday(), 'de')}, {now.day}. {get_month_name(now.month, 'de')} {now.year}",
        'it': f"{get_day_name(now.weekday(), 'it')} {now.day} {get_month_name(now.month, 'it')} {now.year}",
        'pt': f"{get_day_name(now.weekday(), 'pt')}, {now.day} de {get_month_name(now.month, 'pt')} de {now.year}",
        'ar': f"{now.year}/{now.month}/{now.day}",
        'he': f"{now.day}/{now.month}/{now.year}",
        'zh': f"{now.year}年{now.month}月{now.day}日",
        'ja': f"{now.year}年{now.month}月{now.day}日",
        'ru': f"{now.day} {get_month_name(now.month, 'ru')} {now.year}",
    }
    
    date_str = date_formats.get(language, date_formats['fr'])
    
    # Headers by language
    headers = {
        'fr': "[INFORMATIONS TEMPORELLES - À UTILISER DANS TES RÉPONSES]",
        'en': "[TIME INFORMATION - USE IN YOUR RESPONSES]",
        'es': "[INFORMACIÓN TEMPORAL - USAR EN TUS RESPUESTAS]",
        'de': "[ZEITINFORMATIONEN - IN DEINEN ANTWORTEN VERWENDEN]",
        'it': "[INFORMAZIONI TEMPORALI - DA USARE NELLE TUE RISPOSTE]",
        'pt': "[INFORMAÇÕES TEMPORAIS - USAR NAS SUAS RESPOSTAS]",
        'ar': "[معلومات الوقت - استخدم في ردودك]",
        'he': "[מידע זמן - השתמש בתשובותיך]",
        'zh': "[时间信息 - 在您的回复中使用]",
        'ja': "[時間情報 - 回答に使用してください]",
        'ru': "[ВРЕМЕННАЯ ИНФОРМАЦИЯ - ИСПОЛЬЗОВАТЬ В ОТВЕТАХ]",
    }
    
    date_labels = {
        'fr': "Date actuelle", 'en': "Current date", 'es': "Fecha actual",
        'de': "Aktuelles Datum", 'it': "Data attuale", 'pt': "Data atual",
        'ar': "التاريخ الحالي", 'he': "תאריך נוכחי", 'zh': "当前日期",
        'ja': "現在の日付", 'ru': "Текущая дата",
    }
    
    time_labels = {
        'fr': "Heure actuelle", 'en': "Current time", 'es': "Hora actual",
        'de': "Aktuelle Uhrzeit", 'it': "Ora attuale", 'pt': "Hora atual",
        'ar': "الوقت الحالي", 'he': "שעה נוכחית", 'zh': "当前时间",
        'ja': "現在の時刻", 'ru': "Текущее время",
    }
    
    header = headers.get(language, headers['fr'])
    date_label = date_labels.get(language, date_labels['fr'])
    time_label = time_labels.get(language, time_labels['fr'])
    
    return f"""{header}
{date_label}: {date_str}
{time_label}: {now.strftime('%H:%M')} (Europe/Paris)"""


def get_day_name(weekday: int, lang: str) -> str:
    """Get day name in specified language"""
    days = {
        'fr': ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi', 'dimanche'],
        'en': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
        'es': ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo'],
        'de': ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag', 'Sonntag'],
        'it': ['lunedì', 'martedì', 'mercoledì', 'giovedì', 'venerdì', 'sabato', 'domenica'],
        'pt': ['segunda-feira', 'terça-feira', 'quarta-feira', 'quinta-feira', 'sexta-feira', 'sábado', 'domingo'],
        'ru': ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресенье'],
    }
    return days.get(lang, days['fr'])[weekday]


def get_month_name(month: int, lang: str) -> str:
    """Get month name in specified language"""
    months = {
        'fr': ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre'],
        'en': ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
        'es': ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre'],
        'de': ['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember'],
        'it': ['gennaio', 'febbraio', 'marzo', 'aprile', 'maggio', 'giugno', 'luglio', 'agosto', 'settembre', 'ottobre', 'novembre', 'dicembre'],
        'pt': ['janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro'],
        'ru': ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря'],
    }
    return months.get(lang, months['fr'])[month - 1]


def get_system_context(language: str = 'fr') -> str:
    """
    Returns system context including date and platform info
    """
    date_context = get_current_datetime_context(language)
    lang_instruction = get_language_instruction(language)
    
    return f"""{date_context}

{lang_instruction}

[INFORMATIONS SYSTÈME]
Plateforme: WikiAsk
Version: 2.4.0
Modèle: Expert AI avec données temps réel"""


