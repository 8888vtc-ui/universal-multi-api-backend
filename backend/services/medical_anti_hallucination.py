"""
Medical Anti-Hallucination System
Ensures factual accuracy and proper source attribution for medical information
"""
import re
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
from enum import Enum


class SourceType(str, Enum):
    """Types of medical information sources"""
    PUBMED = "PUBMED"
    FDA = "FDA"
    RXNORM = "RxNorm"
    WHO = "OMS/WHO"
    CLINICAL_TRIALS = "ClinicalTrials.gov"
    EUROPE_PMC = "Europe PMC"
    SNOMED = "SNOMED CT"
    ICD11 = "ICD-11"
    ORPHANET = "Orphanet"
    LOCAL_DB = "Base locale"
    AI_KNOWLEDGE = "ANALYSE IA"
    UNKNOWN = "Source non vérifiée"


class MedicalFactChecker:
    """
    Validates medical information and ensures proper source attribution.
    Detects potential hallucinations and flags unverified claims.
    """
    
    def __init__(self):
        # Keywords that require source verification
        self.requires_source_keywords = [
            # Statistics & numbers
            r"\d+\s*%",  # Percentages
            r"\d+\s*/\s*\d+",  # Fractions
            r"\d+\s*(mg|g|ml|L|UI|mmol)",  # Dosages
            r"\d+\s*(million|milliard|billion)",  # Large numbers
            
            # Medical claims
            r"étude\s+(montre|démontre|prouve)",
            r"study\s+(shows|demonstrates|proves)",
            r"selon\s+(une\s+)?étude",
            r"according\s+to\s+(a\s+)?study",
            r"recherche\s+(montre|indique)",
            r"research\s+(shows|indicates)",
            
            # Specific claims
            r"(efficace|effective)\s+à\s+\d+",
            r"réduit\s+(de\s+)?\d+",
            r"reduce[sd]?\s+(by\s+)?\d+",
            r"taux\s+de\s+(succès|survie|mortalité)",
            r"(survival|mortality|success)\s+rate",
        ]
        
        # Dangerous claims that should be flagged
        self.dangerous_claims = [
            r"(guérit|cure[sd]?)\s+(le\s+)?cancer",
            r"(remplace|replace[sd]?)\s+(le\s+)?traitement",
            r"(arrêtez|stop)\s+(votre\s+)?médicament",
            r"100\s*%\s+(efficace|effective|sûr|safe)",
            r"sans\s+(aucun\s+)?effet\s+secondaire",
            r"no\s+side\s+effect",
            r"miracle",
            r"(toujours|always)\s+(fonctionne|works)",
        ]
        
        # Terms that indicate uncertainty (encouraged)
        self.uncertainty_markers = [
            "peut", "pourrait", "might", "may", "could",
            "suggère", "suggests", "indicates",
            "certaines études", "some studies",
            "selon les données disponibles", "based on available data",
            "généralement", "typically", "usually",
            "environ", "approximately", "about",
            "estimation", "estimate"
        ]
    
    def check_response(self, response: str, context_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Analyze a response for potential issues and source attribution needs.
        
        Returns:
            Dict with:
            - is_safe: bool - Whether the response is safe to send
            - warnings: List - Potential issues found
            - suggestions: List - Improvements needed
            - source_attribution: Dict - What sources should be cited
        """
        result = {
            "is_safe": True,
            "warnings": [],
            "suggestions": [],
            "source_attribution": {},
            "confidence_score": 1.0
        }
        
        # Check for dangerous claims
        for pattern in self.dangerous_claims:
            if re.search(pattern, response, re.IGNORECASE):
                result["is_safe"] = False
                result["warnings"].append(f"Claim dangereuse détectée: {pattern}")
                result["confidence_score"] -= 0.3
        
        # Check for claims requiring sources
        unverified_claims = []
        for pattern in self.requires_source_keywords:
            matches = re.findall(pattern, response, re.IGNORECASE)
            if matches:
                # Check if source is mentioned nearby
                for match in matches:
                    if not self._has_source_nearby(response, match):
                        unverified_claims.append(str(match))
        
        if unverified_claims:
            result["suggestions"].append(
                f"Les affirmations suivantes devraient mentionner leur source: {', '.join(unverified_claims[:3])}"
            )
            result["confidence_score"] -= 0.1 * len(unverified_claims)
        
        # Check for uncertainty markers (good practice)
        has_uncertainty = any(marker in response.lower() for marker in self.uncertainty_markers)
        if not has_uncertainty and len(response) > 200:
            result["suggestions"].append(
                "Consider adding uncertainty markers for claims that aren't 100% certain"
            )
        
        # Determine source attribution based on context data
        if context_data:
            result["source_attribution"] = self._determine_sources(context_data)
        
        # Normalize confidence score
        result["confidence_score"] = max(0.0, min(1.0, result["confidence_score"]))
        
        return result
    
    def _has_source_nearby(self, text: str, claim: str, window: int = 100) -> bool:
        """Check if a source citation is near a claim"""
        source_patterns = [
            r"\[PUBMED\]", r"\[FDA\]", r"\[OMS\]", r"\[WHO\]",
            r"\[ANALYSE IA\]", r"\[RxNorm\]", r"\[Source:",
            r"selon", r"according to", r"d'après"
        ]
        
        # Find claim position
        pos = text.lower().find(str(claim).lower())
        if pos == -1:
            return True  # Claim not found, assume OK
        
        # Check window around claim
        start = max(0, pos - window)
        end = min(len(text), pos + len(str(claim)) + window)
        window_text = text[start:end]
        
        return any(re.search(p, window_text, re.IGNORECASE) for p in source_patterns)
    
    def _determine_sources(self, context_data: Dict[str, Any]) -> Dict[str, List[str]]:
        """Determine which sources were used based on context data"""
        sources = {}
        
        source_mapping = {
            "pubmed": SourceType.PUBMED,
            "fda": SourceType.FDA,
            "openfda": SourceType.FDA,
            "rxnorm": SourceType.RXNORM,
            "who": SourceType.WHO,
            "disease_sh": SourceType.WHO,
            "clinical_trials": SourceType.CLINICAL_TRIALS,
            "europe_pmc": SourceType.EUROPE_PMC,
            "snomed": SourceType.SNOMED,
            "icd11": SourceType.ICD11,
            "orphanet": SourceType.ORPHANET,
            "local_database": SourceType.LOCAL_DB,
            "open_disease": SourceType.LOCAL_DB
        }
        
        for key, value in context_data.items():
            if isinstance(value, dict) and value.get("count", 0) > 0:
                source_type = source_mapping.get(key.lower(), SourceType.UNKNOWN)
                if source_type not in sources:
                    sources[source_type.value] = []
                sources[source_type.value].append(key)
        
        # If no external sources, mark as AI knowledge
        if not sources:
            sources[SourceType.AI_KNOWLEDGE.value] = ["Connaissances générales de l'IA"]
        
        return sources
    
    def add_source_tags(self, response: str, sources_used: Dict[str, Any]) -> str:
        """
        Add source attribution tags to a response.
        """
        # Determine primary source
        if not sources_used:
            primary_source = SourceType.AI_KNOWLEDGE.value
        else:
            # Prioritize verified sources
            priority_order = [
                SourceType.PUBMED.value,
                SourceType.EUROPE_PMC.value,
                SourceType.FDA.value,
                SourceType.RXNORM.value,
                SourceType.WHO.value,
                SourceType.CLINICAL_TRIALS.value,
                SourceType.LOCAL_DB.value,
                SourceType.AI_KNOWLEDGE.value
            ]
            
            primary_source = SourceType.AI_KNOWLEDGE.value
            for source in priority_order:
                if source in sources_used:
                    primary_source = source
                    break
        
        # Add source footer
        source_footer = f"\n\n📊 **Source principale**: [{primary_source}]"
        
        if len(sources_used) > 1:
            other_sources = [s for s in sources_used.keys() if s != primary_source]
            source_footer += f"\n📚 **Sources complémentaires**: {', '.join(f'[{s}]' for s in other_sources)}"
        
        return response + source_footer


class MedicalAntiHallucination:
    """
    Complete anti-hallucination system for medical information.
    Combines fact-checking with source attribution and confidence scoring.
    """
    
    def __init__(self):
        self.fact_checker = MedicalFactChecker()
        
        # Medical terms that MUST have accurate information
        self.critical_terms = {
            "dosage", "posologie", "dose",
            "contre-indication", "contraindication",
            "interaction", "effet secondaire", "side effect",
            "surdosage", "overdose",
            "allergie", "allergy",
            "urgence", "emergency", "urgent"
        }
    
    def enhance_medical_prompt(self, base_prompt: str) -> str:
        """Add anti-hallucination instructions to a medical prompt"""
        anti_hallucination_rules = """

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🛡️ SYSTÈME ANTI-HALLUCINATION MÉDICALE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. VÉRIFICATION DES SOURCES (OBLIGATOIRE):
   - Chaque affirmation chiffrée → Précise la source
   - Études citées → Indique [PUBMED] ou [Europe PMC]
   - Médicaments → Indique [FDA] ou [RxNorm]
   - Statistiques épidémiologiques → Indique [OMS/WHO]
   - Connaissances générales → Indique [ANALYSE IA]

2. FORMULATION DES INCERTITUDES:
   - Si donnée approximative → "environ", "approximativement"
   - Si études contradictoires → "certaines études suggèrent"
   - Si pas de donnée temps réel → "selon mes connaissances"
   - Si domaine évolutif → "les recommandations actuelles indiquent"

3. INTERDICTIONS ABSOLUES (HALLUCINATIONS):
   ❌ Inventer des noms d'études spécifiques
   ❌ Créer des pourcentages précis sans source
   ❌ Affirmer des posologies sans vérification
   ❌ Promettre des résultats "garantis" ou "100%"
   ❌ Inventer des interactions médicamenteuses

4. BONNES PRATIQUES:
   ✅ "D'après les données disponibles..." plutôt que "Il est prouvé que..."
   ✅ "La posologie habituelle est..." plutôt que "Prenez exactement..."
   ✅ "Les études suggèrent..." plutôt que "Les études prouvent..."
   ✅ Citer 2-3 sources si données multiples

5. FOOTER SOURCE (TOUJOURS AJOUTER):
   À la fin de chaque réponse médicale, ajoute:
   📊 Sources: [PUBMED/FDA/OMS/ANALYSE IA selon les données utilisées]
"""
        return base_prompt + anti_hallucination_rules
    
    def validate_response(self, response: str, context: Dict[str, Any] = None) -> Tuple[str, Dict[str, Any]]:
        """
        Validate and potentially modify a medical response.
        
        Returns:
            Tuple of (modified_response, validation_report)
        """
        # Run fact check
        check_result = self.fact_checker.check_response(response, context)
        
        # If unsafe, add warning
        if not check_result["is_safe"]:
            warning = "\n\n⚠️ **Attention**: Cette réponse contient des affirmations qui nécessitent une vérification médicale professionnelle."
            response = response + warning
        
        # Add source attribution
        if context:
            sources = self.fact_checker._determine_sources(context)
            response = self.fact_checker.add_source_tags(response, sources)
        else:
            response = response + f"\n\n📊 **Source**: [ANALYSE IA - Connaissances générales]"
        
        return response, check_result
    
    def get_source_summary(self, context: Dict[str, Any]) -> str:
        """Generate a summary of sources used"""
        if not context:
            return "📊 Sources: [ANALYSE IA]"
        
        sources = self.fact_checker._determine_sources(context)
        
        if not sources:
            return "📊 Sources: [ANALYSE IA]"
        
        source_list = ", ".join(f"[{s}]" for s in sources.keys())
        return f"📊 Sources: {source_list}"


# Singleton instances
medical_fact_checker = MedicalFactChecker()
medical_anti_hallucination = MedicalAntiHallucination()


def validate_medical_response(response: str, context: Dict[str, Any] = None) -> Tuple[str, Dict[str, Any]]:
    """Convenience function to validate a medical response"""
    return medical_anti_hallucination.validate_response(response, context)


def enhance_medical_prompt(prompt: str) -> str:
    """Convenience function to enhance a medical prompt with anti-hallucination rules"""
    return medical_anti_hallucination.enhance_medical_prompt(prompt)
