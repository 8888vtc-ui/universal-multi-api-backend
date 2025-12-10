"""
Smart Query Analyzer V2 - FAIL-SAFE Query Detection
Never fails, always provides a reasonable interpretation
"""
from typing import Literal, Dict, Any
import re


class SmartQueryAnalyzer:
    """
    Robust query analyzer that NEVER fails.
    Always returns a valid mode, even for edge cases.
    """
    
    # DEEP mode - comprehensive search triggers
    DEEP_TRIGGERS = [
        # Academic context - ALWAYS deep
        "etudiant", "etudiante", "student", "students",
        "medecine", "medicine", "medical", "medicale",
        "infirmier", "infirmiere", "nurse", "nursing",
        "pharmacie", "pharmacy", "pharmacien",
        "these", "memoire", "dissertation",
        "cours", "examen", "exam", "revision",
        
        # Professional context
        "professionnel", "professional", "clinique", "clinical",
        "praticien", "practitioner", "docteur", "doctor",
        
        # Explicit comprehensive requests
        "rapport", "report", "complet", "complete",
        "detaille", "detailed", "en detail", "in detail",
        "approfondi", "approfondie", "in-depth", "exhaustif", "exhaustive",
        "thinking", "thinking mode", "mode thinking",
        "toutes les donnees", "all data", "tout savoir",
        "fiche", "document", "synthese", "synthesis",
        "resume complet", "full summary",
        
        # Research context
        "etude", "study", "studies", "recherche", "research",
        "scientifique", "scientific", "pubmed", "litterature",
        "evidence", "meta-analyse", "meta-analysis",
        "statistique", "statistic", "prevalence", "incidence",
        "epidemiologie", "epidemiology",
        
        # Detailed explanation requests
        "mecanisme", "mechanism", "physiopathologie", "pathophysiology",
        "etiologie", "etiology", "diagnostic differentiel",
        "protocole", "protocol", "guidelines", "recommandations",
        
        # Long form requests
        "explique-moi tout", "explain everything",
        "dis-moi tout", "tell me everything",
        "je veux tout savoir", "i want to know",
        "donne-moi toutes", "give me all"
    ]
    
    # FAST mode - simple conversations
    FAST_TRIGGERS = [
        # Greetings
        "bonjour", "bonsoir", "salut", "hello", "hi", "hey", "coucou",
        
        # Thanks
        "merci", "thanks", "thank you", "merci beaucoup",
        
        # Simple confirmations
        "oui", "non", "yes", "no", "ok", "okay", "d'accord", "entendu",
        
        # Goodbyes
        "au revoir", "bye", "goodbye", "a bientot", "ciao",
        
        # Simple acknowledgments
        "je comprends", "compris", "c'est note", "parfait", "super", "cool",
        "c'est tout", "that's all", "rien d'autre"
    ]
    
    # Medical keywords that require data
    MEDICAL_KEYWORDS = [
        # Symptoms
        "symptome", "symptom", "signe", "douleur", "mal", "fievre",
        
        # Diseases
        "maladie", "disease", "pathologie", "syndrome", "trouble",
        "diabete", "hypertension", "cancer", "infection", "virus",
        
        # Treatments
        "traitement", "treatment", "medicament", "medication", "therapie",
        "posologie", "dosage", "effet secondaire", "contre-indication",
        
        # Diagnosis
        "diagnostic", "diagnosis", "examen", "analyse", "bilan",
        
        # Body parts
        "coeur", "heart", "foie", "liver", "poumon", "lung", "cerveau", "brain",
        "estomac", "stomach", "rein", "kidney", "intestin"
    ]
    
    @classmethod
    def analyze(cls, query: str, expert_id: str = None) -> Dict[str, Any]:
        """
        Analyze query and return comprehensive analysis.
        NEVER FAILS - always returns valid result.
        
        Returns:
            {
                "intent": "data_needed" | "chat_only",
                "mode": "fast" | "standard" | "deep",
                "confidence": 0.0-1.0,
                "triggers_found": ["keyword1", "keyword2"],
                "is_medical": bool,
                "reasoning": "why this mode was chosen"
            }
        """
        # Normalize query
        query_lower = query.lower().strip()
        query_normalized = cls._normalize(query_lower)
        
        result = {
            "intent": "data_needed",
            "mode": "standard",
            "confidence": 0.7,
            "triggers_found": [],
            "is_medical": False,
            "reasoning": ""
        }
        
        # Check for DEEP triggers first (highest priority)
        deep_triggers = cls._find_triggers(query_normalized, cls.DEEP_TRIGGERS)
        if deep_triggers:
            result["mode"] = "deep"
            result["intent"] = "data_needed"
            result["confidence"] = 0.95
            result["triggers_found"] = deep_triggers
            result["reasoning"] = f"DEEP mode: triggers found ({', '.join(deep_triggers[:3])})"
            return result
        
        # Check for FAST triggers (greetings, thanks, etc.)
        fast_triggers = cls._find_triggers(query_normalized, cls.FAST_TRIGGERS)
        if fast_triggers and len(query_normalized) < 50:
            result["mode"] = "fast"
            result["intent"] = "chat_only"
            result["confidence"] = 0.9
            result["triggers_found"] = fast_triggers
            result["reasoning"] = f"FAST mode: simple conversation ({', '.join(fast_triggers[:2])})"
            return result
        
        # Check for medical keywords
        medical_triggers = cls._find_triggers(query_normalized, cls.MEDICAL_KEYWORDS)
        if medical_triggers:
            result["is_medical"] = True
            result["triggers_found"] = medical_triggers
            
            # Long medical queries = DEEP mode
            if len(query_normalized) > 80:
                result["mode"] = "deep"
                result["confidence"] = 0.85
                result["reasoning"] = f"DEEP mode: long medical query ({len(query_normalized)} chars)"
            else:
                result["mode"] = "standard"
                result["confidence"] = 0.8
                result["reasoning"] = f"STANDARD mode: medical query ({', '.join(medical_triggers[:2])})"
            return result
        
        # Fallback based on query length
        if len(query_normalized) < 30:
            result["mode"] = "fast"
            result["intent"] = "chat_only"
            result["confidence"] = 0.6
            result["reasoning"] = "FAST mode: short query (fallback)"
        elif len(query_normalized) > 100:
            result["mode"] = "deep"
            result["intent"] = "data_needed"
            result["confidence"] = 0.7
            result["reasoning"] = "DEEP mode: long query (fallback, >100 chars)"
        else:
            result["mode"] = "standard"
            result["confidence"] = 0.6
            result["reasoning"] = "STANDARD mode: default for medium queries"
        
        return result
    
    @classmethod
    def _normalize(cls, text: str) -> str:
        """Normalize text for matching"""
        # Remove accents for matching
        replacements = {
            'é': 'e', 'è': 'e', 'ê': 'e', 'ë': 'e',
            'à': 'a', 'â': 'a', 'ä': 'a',
            'ù': 'u', 'û': 'u', 'ü': 'u',
            'î': 'i', 'ï': 'i',
            'ô': 'o', 'ö': 'o',
            'ç': 'c'
        }
        for accent, replacement in replacements.items():
            text = text.replace(accent, replacement)
        return text
    
    @classmethod
    def _find_triggers(cls, text: str, triggers: list) -> list:
        """Find all matching triggers in text"""
        found = []
        for trigger in triggers:
            trigger_normalized = cls._normalize(trigger.lower())
            if trigger_normalized in text:
                found.append(trigger)
        return found
    
    @classmethod
    def get_search_mode(cls, query: str, expert_id: str = None) -> Literal["fast", "standard", "deep"]:
        """
        Convenience function - returns just the mode.
        NEVER FAILS.
        """
        return cls.analyze(query, expert_id)["mode"]
    
    @classmethod
    def get_intent(cls, query: str, expert_id: str = None) -> Literal["data_needed", "chat_only"]:
        """
        Convenience function - returns just the intent.
        NEVER FAILS.
        """
        return cls.analyze(query, expert_id)["intent"]


# Backward compatibility with old IntentDetector
class IntentDetector:
    """Backward compatible wrapper"""
    
    @classmethod
    def detect_intent(cls, query: str, expert_id: str = None) -> Literal["data_needed", "chat_only"]:
        return SmartQueryAnalyzer.get_intent(query, expert_id)
    
    @classmethod
    def get_search_mode(cls, query: str, expert_id: str = None) -> Literal["fast", "standard", "deep"]:
        return SmartQueryAnalyzer.get_search_mode(query, expert_id)


# Convenience functions
def detect_intent(query: str, expert_id: str = None) -> Literal["data_needed", "chat_only"]:
    return SmartQueryAnalyzer.get_intent(query, expert_id)


def get_search_mode(query: str, expert_id: str = None) -> Literal["fast", "standard", "deep"]:
    return SmartQueryAnalyzer.get_search_mode(query, expert_id)


def analyze_query(query: str, expert_id: str = None) -> Dict[str, Any]:
    """Full analysis with reasoning"""
    return SmartQueryAnalyzer.analyze(query, expert_id)
