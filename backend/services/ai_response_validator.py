"""
AI Response Validator Service
Valide et améliore les réponses générées par l'IA pour éviter les informations erronées
"""
import re
import logging
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime

logger = logging.getLogger(__name__)


class AIResponseValidator:
    """Service de validation des réponses IA"""
    
    # Mots-clés indiquant des réponses potentiellement problématiques
    RED_FLAGS = [
        r"je ne veux pas",
        r"je refuse de",
        r"impossible de traiter",
    ]
    
    # Patterns de réponses vagues ou non utiles
    VAGUE_PATTERNS = [
        r"^c'est possible",
        r"^peut-être",
        r"^probablement",
        r"^il se peut que",
        r"^cela dépend",
    ]
    
    # Patterns de réponses trop courtes (moins de 20 caractères)
    MIN_LENGTH = 20
    
    # Patterns de réponses contenant des informations médicales/financières sans disclaimer
    MEDICAL_KEYWORDS = [
        "diagnostic", "traitement", "médicament", "maladie", "symptôme",
        "thérapie", "prescription", "dosage", "effet secondaire"
    ]
    
    FINANCIAL_KEYWORDS = [
        "investir", "achat", "vente", "prix", "cours", "trading",
        "portefeuille", "rendement", "profit"
    ]
    
    # Mots-clés politiques/électoraux nécessitant une vérification de date
    POLITICAL_KEYWORDS = [
        "élection", "election", "président", "president", "biden", "trump",
        "vote", "candidat", "candidate", "résultat", "result", "gagné", "won",
        "perdu", "lost", "victoire", "victory", "défaite", "defeat",
        "présidentiel", "presidential", "scrutin", "ballot", "suffrage"
    ]
    
    # Dates d'événements politiques importants (à mettre à jour)
    KNOWN_ELECTION_DATES = {
        "usa_2024": "2024-11-05",  # Élection présidentielle américaine 2024
        "usa_2020": "2020-11-03",  # Élection présidentielle américaine 2020
    }
    
    def __init__(self):
        self.validation_history: List[Dict[str, Any]] = []
    
    def validate_response(
        self, 
        response: str, 
        query: str,
        context: Optional[str] = None,
        expert_type: Optional[str] = None
    ) -> Tuple[bool, Dict[str, Any]]:
        """
        Valide une réponse IA
        
        Returns:
            Tuple[bool, Dict]: (is_valid, validation_details)
        """
        validation_result = {
            "is_valid": True,
            "warnings": [],
            "suggestions": [],
            "confidence_score": 1.0,
            "issues": []
        }
        
        if not response or len(response.strip()) < self.MIN_LENGTH:
            validation_result["is_valid"] = False
            validation_result["issues"].append("Réponse trop courte ou vide")
            validation_result["confidence_score"] = 0.0
            return False, validation_result
        
        # Vérifier les red flags
        response_lower = response.lower()
        for flag in self.RED_FLAGS:
            if re.search(flag, response_lower, re.IGNORECASE):
                validation_result["warnings"].append("Réponse indique un manque de confiance")
                validation_result["confidence_score"] *= 0.7
        
        # Vérifier les patterns vagues
        for pattern in self.VAGUE_PATTERNS:
            if re.match(pattern, response_lower, re.IGNORECASE):
                validation_result["warnings"].append("Réponse trop vague")
                validation_result["confidence_score"] *= 0.8
        
        # Vérifier les informations politiques/électorales
        political_check = self._check_political_info(response, query)
        if political_check["needs_verification"]:
            validation_result["warnings"].append(
                f"Information politique/électorale détectée: {political_check['warning']}"
            )
            validation_result["suggestions"].append(
                "Vérifier la date actuelle et les sources officielles. Les informations électorales peuvent être obsolètes."
            )
            validation_result["confidence_score"] *= 0.5  # Forte pénalité pour les infos politiques non vérifiées
        
        # Vérifier les disclaimers pour les domaines sensibles
        if expert_type in ["health", "medical"] or any(kw in query.lower() for kw in self.MEDICAL_KEYWORDS):
            if not self._has_medical_disclaimer(response):
                validation_result["warnings"].append("Réponse médicale sans disclaimer approprié")
                validation_result["suggestions"].append("Ajouter un disclaimer médical")
                validation_result["confidence_score"] *= 0.9
        
        if expert_type in ["finance", "crypto"] or any(kw in query.lower() for kw in self.FINANCIAL_KEYWORDS):
            if not self._has_financial_disclaimer(response):
                validation_result["warnings"].append("Réponse financière sans disclaimer approprié")
                validation_result["suggestions"].append("Ajouter un disclaimer financier")
                validation_result["confidence_score"] *= 0.9
        
        # Vérifier la cohérence avec le contexte
        if context:
            coherence_score = self._check_coherence(response, context, query)
            if coherence_score < 0.5:
                validation_result["warnings"].append("Réponse peu cohérente avec le contexte")
                validation_result["confidence_score"] *= coherence_score
        
        # Vérifier la présence de sources/citations si nécessaire
        if self._needs_sources(query):
            if not self._has_sources(response):
                validation_result["warnings"].append("Réponse factuelle sans sources mentionnées")
                validation_result["suggestions"].append("Ajouter des sources ou citations")
        
        # Détecter les contradictions internes
        contradictions = self._detect_contradictions(response)
        if contradictions:
            validation_result["warnings"].append(f"Contradictions détectées: {contradictions}")
            validation_result["confidence_score"] *= 0.6
        
        # Détecter les affirmations factuelles sans sources
        factual_claims = [
            r"est\s+\d+",  # "est 2024", "est 100"
            r"a\s+(gagné|perdu|remporté)",  # "a gagné"
            r"(premier|dernier|seul|unique)\s+",  # "premier", "seul"
        ]
        has_factual_claim = any(re.search(pattern, response_lower) for pattern in factual_claims)
        if has_factual_claim and not self._has_sources(response):
            validation_result["warnings"].append("Affirmation factuelle sans source")
            validation_result["confidence_score"] *= 0.7
        
        # Détecter les dates futures suspectes
        future_dates = re.findall(r"\b(20[3-9]\d|2[1-9]\d{2})\b", response)
        current_year = datetime.now().year
        for year_str in future_dates:
            try:
                year = int(year_str)
                if year > current_year + 1:  # Plus d'1 an dans le futur = suspect
                    validation_result["warnings"].append(f"Date future suspecte: {year}")
                    validation_result["confidence_score"] *= 0.5
            except ValueError:
                pass
        
        # Détecter les répétitions dans la réponse
        sentences = [s.strip() for s in response.split('.') if len(s.strip()) > 20]
        if len(sentences) > 1:
            unique_sentences = set(s.lower() for s in sentences)
            if len(unique_sentences) < len(sentences) * 0.7:  # Plus de 30% de répétition
                validation_result["warnings"].append("Répétitions détectées dans la réponse")
                validation_result["confidence_score"] *= 0.8
        
        # Score final
        if validation_result["confidence_score"] < 0.5:
            validation_result["is_valid"] = False
            validation_result["issues"].append("Score de confiance trop faible")
        
        # Enregistrer dans l'historique
        self.validation_history.append({
            "timestamp": datetime.now().isoformat(),
            "query": query[:100],
            "response_length": len(response),
            "validation_result": validation_result
        })
        
        return validation_result["is_valid"], validation_result
    
    def _has_medical_disclaimer(self, response: str) -> bool:
        """Vérifie si la réponse contient un disclaimer médical approprié"""
        disclaimer_keywords = [
            "avis médical", "professionnel de santé", "consultez un médecin",
            "ne remplace pas", "à titre informatif", "conseil médical",
            "disclaimer", "avertissement", "information générale"
        ]
        response_lower = response.lower()
        return any(kw in response_lower for kw in disclaimer_keywords)
    
    def _has_financial_disclaimer(self, response: str) -> bool:
        """Vérifie si la réponse contient un disclaimer financier approprié"""
        disclaimer_keywords = [
            "conseil financier", "investissement", "risque",
            "ne constitue pas", "à titre informatif", "disclaimer",
            "avertissement", "pas un conseil", "analyse personnelle"
        ]
        response_lower = response.lower()
        return any(kw in response_lower for kw in disclaimer_keywords)
    
    def _check_coherence(self, response: str, context: str, query: str) -> float:
        """Vérifie la cohérence entre la réponse et le contexte"""
        # Simple check: présence de mots-clés du contexte dans la réponse
        context_words = set(context.lower().split()[:20])  # Premiers 20 mots
        response_words = set(response.lower().split())
        
        common_words = context_words.intersection(response_words)
        if len(context_words) == 0:
            return 1.0
        
        coherence = len(common_words) / len(context_words)
        return min(coherence * 2, 1.0)  # Normaliser
    
    def _needs_sources(self, query: str) -> bool:
        """Détermine si la requête nécessite des sources"""
        factual_keywords = [
            "statistique", "chiffre", "donnée", "étude", "recherche",
            "selon", "source", "référence", "citation"
        ]
        query_lower = query.lower()
        return any(kw in query_lower for kw in factual_keywords)
    
    def _has_sources(self, response: str) -> bool:
        """Vérifie si la réponse mentionne des sources"""
        source_indicators = [
            "selon", "source", "référence", "étude", "recherche",
            "d'après", "publié", "cité", "mentionné"
        ]
        response_lower = response.lower()
        return any(indicator in response_lower for indicator in source_indicators)
    
    def _check_political_info(self, response: str, query: str) -> Dict[str, Any]:
        """Vérifie les informations politiques/électorales"""
        response_lower = response.lower()
        query_lower = query.lower()
        
        # Détecter si la réponse ou la requête concerne la politique
        has_political_content = any(
            kw in response_lower or kw in query_lower 
            for kw in self.POLITICAL_KEYWORDS
        )
        
        if not has_political_content:
            return {"needs_verification": False, "warning": ""}
        
        # Vérifier si des dates sont mentionnées
        date_patterns = [
            r"\d{4}",  # Année
            r"\d{1,2}[/-]\d{1,2}[/-]\d{2,4}",  # Date format
        ]
        
        has_date = any(re.search(pattern, response) for pattern in date_patterns)
        
        # Vérifier si des affirmations définitives sont faites sans source
        definitive_patterns = [
            r"a gagné", r"a perdu", r"a remporté", r"a été élu",
            r"won", r"lost", r"elected", r"victory", r"defeat"
        ]
        
        has_definitive_claim = any(
            re.search(pattern, response_lower, re.IGNORECASE) 
            for pattern in definitive_patterns
        )
        
        warning = ""
        if has_definitive_claim and not has_date:
            warning = "Affirmation électorale sans date précise - risque d'information obsolète"
        elif has_definitive_claim:
            warning = "Affirmation électorale détectée - nécessite vérification de la date actuelle"
        else:
            warning = "Contenu politique détecté - nécessite vérification"
        
        return {
            "needs_verification": True,
            "warning": warning,
            "has_date": has_date,
            "has_definitive_claim": has_definitive_claim
        }
    
    def _detect_contradictions(self, response: str) -> List[str]:
        """Détecte les contradictions internes dans la réponse"""
        contradictions = []
        
        # Patterns de contradiction
        contradiction_pairs = [
            (r"toujours", r"jamais"),
            (r"tous", r"aucun"),
            (r"oui", r"non"),
            (r"vrai", r"faux"),
        ]
        
        response_lower = response.lower()
        for pattern1, pattern2 in contradiction_pairs:
            if re.search(pattern1, response_lower) and re.search(pattern2, response_lower):
                contradictions.append(f"{pattern1} vs {pattern2}")
        
        return contradictions
    
    def enhance_system_prompt(
        self, 
        base_prompt: str, 
        query: str,
        expert_type: Optional[str] = None
    ) -> str:
        """Améliore le prompt système pour obtenir de meilleures réponses"""
        enhancements = []
        
        # Détecter si la requête concerne la politique
        query_lower = query.lower()
        is_political_query = any(kw in query_lower for kw in self.POLITICAL_KEYWORDS)
        
        # Règles strictes anti-hallucinations
        enhancements.append(
            "RÈGLES CRITIQUES:\n"
            "1. Réponds avec assurance et confiance\n"
            "2. Utilise tes connaissances quand tu n'as pas de données externes\n"
            "3. Ne dis jamais 'je ne sais pas' ou 'je ne peux pas'\n"
            "4. Réponds de manière naturelle et fluide\n"
            "5. Évite les messages techniques ou d'avertissement"
        )
        
        # Instructions de précision
        enhancements.append(
            "IMPORTANT: Fournis uniquement des informations que tu es certain d'être correctes. "
            "Si tu n'es pas sûr, dis-le clairement."
        )
        
        # Instructions spéciales pour les informations politiques/électorales
        if is_political_query:
            current_date = datetime.now().strftime("%Y-%m-%d")
            enhancements.append(
                f"INFORMATIONS POLITIQUES/ÉLECTORALES:\n"
                f"- La date actuelle est: {current_date}\n"
                f"- Pour les résultats d'élections, indique la date de l'élection\n"
                f"- Réponds avec assurance en utilisant tes connaissances"
            )
        
        # Ajouter des instructions selon le type d'expert
        if expert_type in ["health", "medical"]:
            enhancements.append(
                "ATTENTION: Pour toute information médicale, ajoute toujours un disclaimer "
                "indiquant que ceci ne remplace pas un avis médical professionnel."
            )
        
        if expert_type in ["finance", "crypto"]:
            enhancements.append(
                "ATTENTION: Pour toute information financière, ajoute toujours un disclaimer "
                "indiquant que ceci ne constitue pas un conseil financier personnalisé."
            )
        
        # Instructions de qualité
        enhancements.append(
            "Sois précis, factuel et cite tes sources quand c'est possible. "
            "Évite les réponses vagues ou trop générales. "
            "Pour les informations sensibles (politique, élections), vérifie toujours la date actuelle."
        )
        
        enhanced_prompt = base_prompt
        if enhancements:
            enhanced_prompt += "\n\n" + "\n".join(enhancements)
        
        return enhanced_prompt
    
    def get_validation_stats(self) -> Dict[str, Any]:
        """Retourne des statistiques sur les validations"""
        if not self.validation_history:
            return {"total": 0, "average_confidence": 0.0}
        
        total = len(self.validation_history)
        avg_confidence = sum(
            v["validation_result"]["confidence_score"] 
            for v in self.validation_history
        ) / total
        
        invalid_count = sum(
            1 for v in self.validation_history 
            if not v["validation_result"]["is_valid"]
        )
        
        return {
            "total": total,
            "average_confidence": avg_confidence,
            "invalid_count": invalid_count,
            "invalid_percentage": (invalid_count / total * 100) if total > 0 else 0
        }


# Instance globale
ai_response_validator = AIResponseValidator()


