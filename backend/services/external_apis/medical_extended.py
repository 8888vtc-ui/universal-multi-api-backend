"""
Extended Medical APIs - Disease.sh, RxNorm, WHO
Free APIs for comprehensive medical data
"""
import httpx
from typing import Dict, Any, List, Optional
from datetime import datetime


class DiseaseSHProvider:
    """Disease.sh - COVID-19 and infectious disease data (unlimited, free)"""
    
    def __init__(self):
        self.base_url = "https://disease.sh/v3"
        self.available = True
        
    async def get_covid_global(self) -> Dict[str, Any]:
        """Get global COVID-19 statistics"""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(f"{self.base_url}/covid-19/all")
                if response.status_code == 200:
                    data = response.json()
                    return {
                        "cases": data.get("cases", 0),
                        "deaths": data.get("deaths", 0),
                        "recovered": data.get("recovered", 0),
                        "active": data.get("active", 0),
                        "critical": data.get("critical", 0),
                        "today_cases": data.get("todayCases", 0),
                        "today_deaths": data.get("todayDeaths", 0),
                        "updated": datetime.fromtimestamp(data.get("updated", 0)/1000).isoformat()
                    }
                raise Exception(f"Disease.sh returned {response.status_code}")
        except Exception as e:
            raise Exception(f"Disease.sh error: {e}")
    
    async def get_covid_country(self, country: str) -> Dict[str, Any]:
        """Get COVID-19 stats for a specific country"""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(f"{self.base_url}/covid-19/countries/{country}")
                if response.status_code == 200:
                    data = response.json()
                    return {
                        "country": data.get("country"),
                        "cases": data.get("cases", 0),
                        "deaths": data.get("deaths", 0),
                        "recovered": data.get("recovered", 0),
                        "active": data.get("active", 0),
                        "critical": data.get("critical", 0),
                        "cases_per_million": data.get("casesPerOneMillion", 0),
                        "deaths_per_million": data.get("deathsPerOneMillion", 0),
                        "population": data.get("population", 0),
                        "continent": data.get("continent"),
                        "updated": datetime.fromtimestamp(data.get("updated", 0)/1000).isoformat()
                    }
                raise Exception(f"Country not found or API error: {response.status_code}")
        except Exception as e:
            raise Exception(f"Disease.sh country error: {e}")
    
    async def get_disease_info(self, disease: str = "covid-19") -> Dict[str, Any]:
        """Get information about infectious diseases"""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                # Get historical data for context
                response = await client.get(
                    f"{self.base_url}/covid-19/historical/all",
                    params={"lastdays": 30}
                )
                if response.status_code == 200:
                    data = response.json()
                    return {
                        "disease": disease,
                        "historical_cases": data.get("cases", {}),
                        "historical_deaths": data.get("deaths", {}),
                        "historical_recovered": data.get("recovered", {})
                    }
                return {"disease": disease, "data": "limited"}
        except Exception as e:
            raise Exception(f"Disease.sh historical error: {e}")


class RxNormProvider:
    """RxNorm NIH - Drug terminology and information (unlimited, free)"""
    
    def __init__(self):
        self.base_url = "https://rxnav.nlm.nih.gov/REST"
        self.available = True
        
    async def search_drug(self, drug_name: str) -> Dict[str, Any]:
        """Search for drug information by name"""
        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                # Get drug concepts
                response = await client.get(
                    f"{self.base_url}/drugs.json",
                    params={"name": drug_name}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    drug_group = data.get("drugGroup", {})
                    concept_group = drug_group.get("conceptGroup", [])
                    
                    drugs = []
                    for group in concept_group:
                        for prop in group.get("conceptProperties", []):
                            drugs.append({
                                "rxcui": prop.get("rxcui"),
                                "name": prop.get("name"),
                                "synonym": prop.get("synonym"),
                                "tty": prop.get("tty")  # Term type
                            })
                    
                    return {
                        "query": drug_name,
                        "count": len(drugs),
                        "drugs": drugs[:10]  # Limit to 10
                    }
                raise Exception(f"RxNorm returned {response.status_code}")
        except Exception as e:
            raise Exception(f"RxNorm search error: {e}")
    
    async def get_drug_interactions(self, rxcui: str) -> Dict[str, Any]:
        """Get drug interactions by RxCUI"""
        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                response = await client.get(
                    f"{self.base_url}/interaction/interaction.json",
                    params={"rxcui": rxcui}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    interactions = []
                    
                    for group in data.get("interactionTypeGroup", []):
                        for itype in group.get("interactionType", []):
                            for pair in itype.get("interactionPair", []):
                                interactions.append({
                                    "severity": pair.get("severity"),
                                    "description": pair.get("description"),
                                    "drugs_involved": [
                                        c.get("minConceptItem", {}).get("name")
                                        for c in pair.get("interactionConcept", [])
                                    ]
                                })
                    
                    return {
                        "rxcui": rxcui,
                        "interaction_count": len(interactions),
                        "interactions": interactions[:10]
                    }
                return {"rxcui": rxcui, "interactions": []}
        except Exception as e:
            raise Exception(f"RxNorm interactions error: {e}")
    
    async def get_drug_class(self, rxcui: str) -> Dict[str, Any]:
        """Get therapeutic class of a drug"""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    f"{self.base_url}/rxclass/class/byRxcui.json",
                    params={"rxcui": rxcui}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    classes = []
                    
                    for entry in data.get("rxclassDrugInfoList", {}).get("rxclassDrugInfo", []):
                        class_info = entry.get("rxclassMinConceptItem", {})
                        classes.append({
                            "class_id": class_info.get("classId"),
                            "class_name": class_info.get("className"),
                            "class_type": class_info.get("classType")
                        })
                    
                    return {
                        "rxcui": rxcui,
                        "classes": classes
                    }
                return {"rxcui": rxcui, "classes": []}
        except Exception as e:
            raise Exception(f"RxNorm class error: {e}")


class WHOGHOProvider:
    """WHO Global Health Observatory - Health statistics (unlimited, free)"""
    
    def __init__(self):
        self.base_url = "https://ghoapi.azureedge.net/api"
        self.available = True
        
    async def get_indicators(self, limit: int = 20) -> Dict[str, Any]:
        """Get list of available health indicators"""
        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                response = await client.get(
                    f"{self.base_url}/Indicator",
                    params={"$top": limit}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    indicators = [
                        {
                            "code": ind.get("IndicatorCode"),
                            "name": ind.get("IndicatorName"),
                            "language": ind.get("Language")
                        }
                        for ind in data.get("value", [])
                    ]
                    return {
                        "count": len(indicators),
                        "indicators": indicators
                    }
                raise Exception(f"WHO API returned {response.status_code}")
        except Exception as e:
            raise Exception(f"WHO indicators error: {e}")
    
    async def get_country_health_stats(self, country_code: str, indicator: str = "WHOSIS_000001") -> Dict[str, Any]:
        """Get health statistics for a country"""
        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                response = await client.get(
                    f"{self.base_url}/{indicator}",
                    params={
                        "$filter": f"SpatialDim eq '{country_code}'",
                        "$top": 10
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    stats = [
                        {
                            "year": stat.get("TimeDim"),
                            "value": stat.get("NumericValue"),
                            "dimension": stat.get("Dim1"),
                            "indicator": indicator
                        }
                        for stat in data.get("value", [])
                    ]
                    return {
                        "country": country_code,
                        "indicator": indicator,
                        "stats": stats
                    }
                return {"country": country_code, "stats": []}
        except Exception as e:
            raise Exception(f"WHO country stats error: {e}")
    
    async def get_life_expectancy(self, country_code: str) -> Dict[str, Any]:
        """Get life expectancy data for a country"""
        # WHOSIS_000001 is the life expectancy indicator
        return await self.get_country_health_stats(country_code, "WHOSIS_000001")


class MedlinePlusProvider:
    """MedlinePlus Connect - Health topics and conditions (unlimited, free)"""
    
    def __init__(self):
        self.base_url = "https://connect.medlineplus.gov/service"
        self.available = True
        
    async def search_health_topic(self, query: str, language: str = "en") -> Dict[str, Any]:
        """Search for health topics"""
        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                # MedlinePlus uses ICD codes, but we can search by problem
                response = await client.get(
                    f"{self.base_url}",
                    params={
                        "mainSearchCriteria.v.c": query,
                        "mainSearchCriteria.v.cs": "2.16.840.1.113883.6.103",  # ICD-9
                        "informationRecipient.languageCode.c": language,
                        "knowledgeResponseType": "application/json"
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    entries = data.get("feed", {}).get("entry", [])
                    
                    topics = []
                    for entry in entries:
                        topics.append({
                            "title": entry.get("title", {}).get("_value"),
                            "summary": entry.get("summary", {}).get("_value"),
                            "link": next(
                                (l.get("href") for l in entry.get("link", []) if l.get("rel") == "alternate"),
                                None
                            )
                        })
                    
                    return {
                        "query": query,
                        "count": len(topics),
                        "topics": topics
                    }
                return {"query": query, "topics": []}
        except Exception as e:
            # MedlinePlus can be finicky, return empty gracefully
            return {"query": query, "topics": [], "error": str(e)}


class OpenDiseaseProvider:
    """Aggregated disease information from multiple sources"""
    
    def __init__(self):
        self.available = True
        # Disease database (common conditions with basic info)
        self.disease_db = {
            "diabetes": {
                "name": "Diabète (Diabetes Mellitus)",
                "description": "Maladie métabolique caractérisée par une hyperglycémie chronique",
                "types": ["Type 1 (auto-immun)", "Type 2 (résistance à l'insuline)", "Gestationnel"],
                "symptoms": ["Soif excessive", "Urination fréquente", "Fatigue", "Vision floue", "Perte de poids"],
                "risk_factors": ["Obésité", "Sédentarité", "Antécédents familiaux", "Âge > 45 ans"],
                "prevention": ["Alimentation équilibrée", "Activité physique régulière", "Maintien poids santé"],
                "prevalence": "9.3% de la population mondiale (537 millions)",
                "when_to_consult": ["Symptômes de diabète", "Glycémie élevée", "Antécédents familiaux"]
            },
            "hypertension": {
                "name": "Hypertension artérielle",
                "description": "Élévation chronique de la pression artérielle",
                "types": ["Primaire (essentielle)", "Secondaire"],
                "symptoms": ["Souvent asymptomatique", "Maux de tête", "Vertiges", "Essoufflement"],
                "risk_factors": ["Âge", "Surpoids", "Sel", "Alcool", "Stress", "Sédentarité"],
                "prevention": ["Réduire le sel", "Exercice", "Limiter alcool", "Gérer le stress"],
                "prevalence": "1.28 milliard d'adultes dans le monde",
                "when_to_consult": ["PA > 140/90 mmHg", "Maux de tête persistants", "Troubles visuels"]
            },
            "asthma": {
                "name": "Asthme",
                "description": "Maladie inflammatoire chronique des voies respiratoires",
                "types": ["Allergique", "Non allergique", "Professionnel", "D'effort"],
                "symptoms": ["Essoufflement", "Sifflements", "Toux", "Oppression thoracique"],
                "risk_factors": ["Allergies", "Antécédents familiaux", "Pollution", "Infections respiratoires"],
                "prevention": ["Éviter les déclencheurs", "Traitement de fond", "Vaccinations"],
                "prevalence": "262 millions de personnes dans le monde",
                "when_to_consult": ["Crise d'asthme", "Symptômes fréquents", "Traitement inefficace"]
            },
            "depression": {
                "name": "Dépression (Trouble dépressif majeur)",
                "description": "Trouble de l'humeur caractérisé par une tristesse persistante",
                "types": ["Majeure", "Persistante (dysthymie)", "Saisonnière", "Post-partum"],
                "symptoms": ["Tristesse persistante", "Perte d'intérêt", "Fatigue", "Troubles du sommeil", "Difficultés concentration"],
                "risk_factors": ["Antécédents personnels/familiaux", "Stress chronique", "Traumatismes", "Maladies chroniques"],
                "prevention": ["Activité physique", "Liens sociaux", "Gestion du stress", "Sommeil régulier"],
                "prevalence": "280 millions de personnes dans le monde",
                "when_to_consult": ["Symptômes > 2 semaines", "Pensées suicidaires", "Impact sur le quotidien"]
            },
            "migraine": {
                "name": "Migraine",
                "description": "Céphalée primaire récurrente, souvent unilatérale et pulsatile",
                "types": ["Sans aura", "Avec aura", "Chronique", "Menstruelle"],
                "symptoms": ["Douleur pulsatile", "Nausées", "Photophobie", "Phonophobie", "Aura visuelle"],
                "risk_factors": ["Génétique", "Hormones", "Stress", "Alimentation", "Manque de sommeil"],
                "prevention": ["Identifier les déclencheurs", "Régularité du sommeil", "Hydratation", "Gestion du stress"],
                "prevalence": "1 milliard de personnes dans le monde",
                "when_to_consult": ["Première migraine sévère", "Changement de pattern", "Migraine + fièvre"]
            }
        }
        
    async def get_disease_info(self, disease: str) -> Dict[str, Any]:
        """Get information about a disease"""
        disease_lower = disease.lower()
        
        # Check exact match
        if disease_lower in self.disease_db:
            return {
                "found": True,
                "source": "medical_database",
                **self.disease_db[disease_lower]
            }
        
        # Check partial match
        for key, info in self.disease_db.items():
            if disease_lower in key or key in disease_lower:
                return {
                    "found": True,
                    "source": "medical_database",
                    **info
                }
        
        # Not in local database
        return {
            "found": False,
            "query": disease,
            "message": "Maladie non trouvée dans la base locale. Utilisation des connaissances IA."
        }
    
    async def search_symptoms(self, symptoms: List[str]) -> Dict[str, Any]:
        """Search possible conditions by symptoms"""
        matching_conditions = []
        
        for disease, info in self.disease_db.items():
            disease_symptoms = [s.lower() for s in info.get("symptoms", [])]
            matches = sum(1 for s in symptoms if any(s.lower() in ds for ds in disease_symptoms))
            
            if matches > 0:
                matching_conditions.append({
                    "disease": info["name"],
                    "matching_symptoms": matches,
                    "total_symptoms": len(symptoms),
                    "match_percentage": round(matches / len(symptoms) * 100, 1)
                })
        
        # Sort by match percentage
        matching_conditions.sort(key=lambda x: x["match_percentage"], reverse=True)
        
        return {
            "searched_symptoms": symptoms,
            "possible_conditions": matching_conditions[:5],
            "disclaimer": "Cette liste est indicative. Consultez un médecin pour un diagnostic."
        }


# Singleton instances
disease_sh = DiseaseSHProvider()
rxnorm = RxNormProvider()
who_gho = WHOGHOProvider()
medlineplus = MedlinePlusProvider()
open_disease = OpenDiseaseProvider()
