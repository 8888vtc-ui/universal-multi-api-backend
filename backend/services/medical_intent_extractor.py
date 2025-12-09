"""
Medical Intent Extractor - Extract what the user is asking for
Détecte l'intention de la requête médicale (symptômes, traitement, diagnostic, etc.)
"""
from typing import Dict, List, Optional
import re


class MedicalIntentExtractor:
    """Extract what the user wants: symptoms, treatment, diagnosis, etc."""
    
    INTENT_KEYWORDS = {
        "symptoms": [
            "symptome", "symptom", "signe", "manifestation", "presentation",
            "comment se manifeste", "quels sont les signes", "comment reconnaitre",
            "symptôme", "symptômes", "signes", "ressent", "sensation"
        ],
        "treatment": [
            "traitement", "treatment", "therapie", "therapy", "medicament",
            "medication", "soin", "care", "comment traiter", "comment soigner",
            "posologie", "dosage", "prescription", "médicament", "soigner",
            "guérir", "guerir", "remède", "remede"
        ],
        "diagnosis": [
            "diagnostic", "diagnosis", "comment diagnostiquer", "examen",
            "test", "analyse", "bilan", "depistage", "screening", "dépistage",
            "detecter", "détecter"
        ],
        "causes": [
            "cause", "origine", "etiology", "etiologie", "pourquoi", "why",
            "facteur de risque", "risk factor", "comment on attrape",
            "provoque", "déclenche", "raison"
        ],
        "prevention": [
            "prevention", "prevenir", "prévenir", "eviter", "éviter", "avoid",
            "protection", "comment prevenir", "comment eviter", "protéger"
        ],
        "side_effects": [
            "effet secondaire", "side effect", "effet indesirable", "effet indésirable",
            "contre-indication", "contraindication", "interaction", "danger",
            "risque", "effets secondaires"
        ],
        "prognosis": [
            "pronostic", "prognosis", "evolution", "évolution", "guerison", "guérison",
            "recovery", "survie", "survival", "espérance", "durée"
        ],
        "general": [
            "c'est quoi", "qu'est-ce que", "what is", "definition", "définition",
            "explique", "explain", "informe", "information", "parle moi de"
        ]
    }
    
    # Entités médicales communes
    MEDICAL_ENTITIES = [
        # Maladies courantes
        "diabete", "diabetes", "diabète", "hypertension", "cancer", "asthme", "asthma",
        "grippe", "flu", "rhume", "cold", "covid", "coronavirus", "migraine",
        "arthrite", "arthritis", "alzheimer", "parkinson", "depression", "dépression",
        "anxiete", "anxiety", "anxiété", "obesite", "obesity", "obésité",
        "cholesterol", "cholestérol", "anémie", "anemie", "anemia",
        # Médicaments courants
        "aspirine", "aspirin", "paracetamol", "acetaminophen", "ibuprofene",
        "ibuprofen", "insuline", "insulin", "metformine", "metformin",
        "doliprane", "advil", "efferalgan", "amoxicilline", "amoxicillin",
        "omeprazole", "pantoprazole", "atorvastatine", "simvastatine",
        # Vitamines et suppléments
        "vitamine", "vitamin", "magnesium", "magnésium", "fer", "iron",
        "calcium", "zinc", "omega", "oméga"
    ]
    
    @classmethod
    def extract_intent(cls, query: str) -> Dict[str, any]:
        """
        Extract what the user is asking for
        
        Returns:
            {
                "primary_intent": "symptoms" | "treatment" | "diagnosis" | ...,
                "secondary_intents": ["intent1", "intent2"],
                "entities": ["diabetes", "aspirin"],
                "confidence": 0.0-1.0
            }
        """
        query_lower = query.lower()
        found_intents = []
        
        # Find all matching intents
        for intent, keywords in cls.INTENT_KEYWORDS.items():
            for keyword in keywords:
                if keyword in query_lower:
                    if intent not in found_intents:
                        found_intents.append(intent)
                    break
        
        # Extract medical entities (diseases, drugs, etc.)
        entities = cls._extract_entities(query)
        
        # Determine primary intent
        primary_intent = found_intents[0] if found_intents else "general"
        secondary_intents = found_intents[1:] if len(found_intents) > 1 else []
        
        # Calculate confidence
        confidence = min(0.9, 0.5 + len(found_intents) * 0.1 + len(entities) * 0.1)
        
        return {
            "primary_intent": primary_intent,
            "secondary_intents": secondary_intents,
            "entities": entities,
            "confidence": confidence,
            "all_intents": found_intents
        }
    
    @classmethod
    def _extract_entities(cls, query: str) -> List[str]:
        """Extract medical entities (diseases, drugs, etc.)"""
        entities = []
        query_lower = query.lower()
        
        for term in cls.MEDICAL_ENTITIES:
            if term in query_lower:
                # Éviter les doublons (ex: diabete/diabète)
                base_term = term.replace("é", "e").replace("è", "e")
                if not any(base_term in e.replace("é", "e").replace("è", "e") for e in entities):
                    entities.append(term)
        
        return entities
    
    @classmethod
    def filter_data_by_intent(cls, data: Dict, intent: str) -> Dict:
        """
        Filter API data to keep only relevant information based on intent
        
        Args:
            data: Raw API response
            intent: Primary intent (symptoms, treatment, etc.)
        
        Returns:
            Filtered data containing only relevant information
        """
        if not data or not isinstance(data, dict):
            return data
        
        filtered = {}
        
        # Map intent to data keys
        intent_to_keys = {
            "symptoms": [
                "symptoms", "signs", "manifestations", "clinical_presentation",
                "symptomes", "signes", "presentation_clinique"
            ],
            "treatment": [
                "treatment", "therapy", "medications", "drugs", "posology",
                "traitement", "therapie", "medicaments", "posologie"
            ],
            "diagnosis": [
                "diagnosis", "diagnostic", "tests", "exams", "criteria",
                "examens", "analyses", "criteres"
            ],
            "causes": [
                "causes", "etiology", "risk_factors", "pathophysiology",
                "etiologie", "facteurs_risque", "origine"
            ],
            "prevention": [
                "prevention", "preventive", "protection", "prophylaxis",
                "mesures_preventives"
            ],
            "side_effects": [
                "side_effects", "adverse_events", "contraindications", "interactions",
                "effets_secondaires", "contre_indications"
            ],
            "prognosis": [
                "prognosis", "outcome", "survival", "recovery",
                "pronostic", "evolution", "guerison"
            ],
            "general": []  # Keep all for general
        }
        
        relevant_keys = intent_to_keys.get(intent, [])
        
        if intent == "general":
            # Keep all data
            return data
        
        # Extract relevant fields
        for key in relevant_keys:
            if key in data:
                filtered[key] = data[key]
        
        # Also check nested structures
        for key, value in data.items():
            if isinstance(value, dict):
                nested_filtered = cls.filter_data_by_intent(value, intent)
                if nested_filtered:
                    filtered[key] = nested_filtered
            elif isinstance(value, list):
                # Filter list items
                filtered_list = []
                for item in value:
                    if isinstance(item, dict):
                        nested = cls.filter_data_by_intent(item, intent)
                        if nested:
                            filtered_list.append(nested)
                    else:
                        filtered_list.append(item)
                if filtered_list:
                    filtered[key] = filtered_list
        
        # Always keep basic info
        for key in ["name", "title", "description", "summary", "source", "nom", "titre"]:
            if key in data and key not in filtered:
                filtered[key] = data[key]
        
        return filtered
    
    @classmethod
    def get_focus_fields(cls, intent: str) -> List[str]:
        """Get the fields to focus on for a given intent"""
        focus_map = {
            "symptoms": ["symptoms", "signs", "manifestations"],
            "treatment": ["treatment", "medications", "dosage", "therapy"],
            "diagnosis": ["diagnosis", "tests", "criteria", "exams"],
            "causes": ["causes", "etiology", "risk_factors"],
            "prevention": ["prevention", "preventive_measures"],
            "side_effects": ["side_effects", "adverse_events", "contraindications"],
            "prognosis": ["prognosis", "outcome", "survival"],
            "general": []
        }
        return focus_map.get(intent, [])


# Quick test function
def test_extractor():
    queries = [
        "Quels sont les symptômes du diabète ?",
        "Comment traiter une migraine ?",
        "Effets secondaires de l'aspirine",
        "C'est quoi l'hypertension ?"
    ]
    
    for query in queries:
        result = MedicalIntentExtractor.extract_intent(query)
        print(f"\nQuery: {query}")
        print(f"Intent: {result['primary_intent']}")
        print(f"Entities: {result['entities']}")
        print(f"Confidence: {result['confidence']:.2f}")


if __name__ == "__main__":
    test_extractor()
