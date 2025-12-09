"""
Medical Router - Unified medical data aggregator
Combines PubMed, OpenFDA, RxNorm, Disease.sh, WHO, and local database
"""
import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime


class MedicalRouter:
    """Intelligent router for medical data from multiple sources"""
    
    def __init__(self):
        self.providers = {}
        self._init_providers()
    
    def _init_providers(self):
        """Initialize all medical providers"""
        # Import existing providers
        try:
            from services.external_apis.medical import pubmed, openfda
            self.providers["pubmed"] = pubmed
            self.providers["openfda"] = openfda
            print("[OK] PubMed and OpenFDA providers loaded")
        except Exception as e:
            print(f"[WARN] Medical providers not loaded: {e}")
        
        # Import extended providers
        try:
            from services.external_apis.medical_extended import (
                disease_sh, rxnorm, who_gho, medlineplus, open_disease
            )
            self.providers["disease_sh"] = disease_sh
            self.providers["rxnorm"] = rxnorm
            self.providers["who_gho"] = who_gho
            self.providers["medlineplus"] = medlineplus
            self.providers["open_disease"] = open_disease
            print("[OK] Extended medical providers loaded")
        except Exception as e:
            print(f"[WARN] Extended medical providers not loaded: {e}")
    
    async def get_comprehensive_health_info(self, query: str, query_type: str = "general") -> Dict[str, Any]:
        """
        Get comprehensive health information from all sources
        
        query_type: "disease", "drug", "symptom", "general"
        """
        results = {
            "query": query,
            "query_type": query_type,
            "timestamp": datetime.now().isoformat(),
            "sources": {},
            "combined_info": {}
        }
        
        tasks = []
        
        # Determine which APIs to call based on query type
        if query_type == "drug":
            tasks.append(self._get_drug_info(query))
        elif query_type == "disease":
            tasks.append(self._get_disease_info(query))
        elif query_type == "symptom":
            tasks.append(self._get_symptom_info(query))
        else:
            # General query - try all relevant sources
            tasks.append(self._get_disease_info(query))
            tasks.append(self._get_research_articles(query))
        
        # Execute all tasks concurrently
        task_results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Merge results
        for result in task_results:
            if isinstance(result, dict) and not isinstance(result, Exception):
                results["sources"].update(result.get("sources", {}))
                results["combined_info"].update(result.get("info", {}))
        
        # Add summary
        results["data_quality"] = self._assess_data_quality(results)
        
        return results
    
    async def _get_drug_info(self, drug_name: str) -> Dict[str, Any]:
        """Get comprehensive drug information"""
        sources = {}
        info = {}
        
        # OpenFDA drug info
        if "openfda" in self.providers:
            try:
                fda_data = await self.providers["openfda"].search_drugs(drug_name, limit=5)
                if fda_data.get("drugs"):
                    sources["openfda"] = fda_data
                    info["fda_approved"] = True
                    info["brand_names"] = [d.get("brand_name") for d in fda_data["drugs"]]
            except:
                pass
        
        # RxNorm drug terminology
        if "rxnorm" in self.providers:
            try:
                rxnorm_data = await self.providers["rxnorm"].search_drug(drug_name)
                if rxnorm_data.get("drugs"):
                    sources["rxnorm"] = rxnorm_data
                    # Get interactions for first result
                    if rxnorm_data["drugs"]:
                        rxcui = rxnorm_data["drugs"][0].get("rxcui")
                        if rxcui:
                            interactions = await self.providers["rxnorm"].get_drug_interactions(rxcui)
                            sources["rxnorm_interactions"] = interactions
                            info["has_interactions"] = interactions.get("interaction_count", 0) > 0
            except:
                pass
        
        return {"sources": sources, "info": info}
    
    async def _get_disease_info(self, disease: str) -> Dict[str, Any]:
        """Get comprehensive disease information"""
        sources = {}
        info = {}
        
        # Local disease database (fast, always available)
        if "open_disease" in self.providers:
            try:
                disease_data = await self.providers["open_disease"].get_disease_info(disease)
                if disease_data.get("found"):
                    sources["local_database"] = disease_data
                    info["basic_info"] = disease_data
            except:
                pass
        
        # PubMed research articles
        if "pubmed" in self.providers:
            try:
                pubmed_data = await self.providers["pubmed"].search_articles(disease, max_results=5)
                if pubmed_data.get("articles"):
                    sources["pubmed"] = pubmed_data
                    info["research_count"] = pubmed_data.get("count", 0)
            except:
                pass
        
        # WHO global health stats (if country-related)
        # This would need country context
        
        return {"sources": sources, "info": info}
    
    async def _get_symptom_info(self, symptoms_text: str) -> Dict[str, Any]:
        """Analyze symptoms and find possible conditions"""
        sources = {}
        info = {}
        
        # Parse symptoms from text
        symptoms = [s.strip() for s in symptoms_text.replace(",", ";").split(";") if s.strip()]
        
        if "open_disease" in self.providers:
            try:
                symptom_analysis = await self.providers["open_disease"].search_symptoms(symptoms)
                sources["symptom_analysis"] = symptom_analysis
                info["possible_conditions"] = symptom_analysis.get("possible_conditions", [])
            except:
                pass
        
        return {"sources": sources, "info": info}
    
    async def _get_research_articles(self, query: str) -> Dict[str, Any]:
        """Get research articles from PubMed"""
        sources = {}
        info = {}
        
        if "pubmed" in self.providers:
            try:
                articles = await self.providers["pubmed"].search_articles(query, max_results=5)
                sources["pubmed"] = articles
                info["articles"] = articles.get("articles", [])
            except:
                pass
        
        return {"sources": sources, "info": info}
    
    async def get_covid_data(self, country: Optional[str] = None) -> Dict[str, Any]:
        """Get COVID-19 data globally or by country"""
        if "disease_sh" not in self.providers:
            return {"error": "Disease.sh provider not available"}
        
        try:
            if country:
                data = await self.providers["disease_sh"].get_covid_country(country)
            else:
                data = await self.providers["disease_sh"].get_covid_global()
            
            return {
                "source": "disease.sh",
                "data_type": "covid19",
                "data": data
            }
        except Exception as e:
            return {"error": str(e)}
    
    async def get_drug_interactions(self, drug_name: str) -> Dict[str, Any]:
        """Get drug interactions"""
        if "rxnorm" not in self.providers:
            return {"error": "RxNorm provider not available"}
        
        try:
            # First, find the drug
            drug_search = await self.providers["rxnorm"].search_drug(drug_name)
            
            if not drug_search.get("drugs"):
                return {"error": f"Drug '{drug_name}' not found"}
            
            rxcui = drug_search["drugs"][0].get("rxcui")
            if not rxcui:
                return {"error": "No RxCUI found for drug"}
            
            # Get interactions
            interactions = await self.providers["rxnorm"].get_drug_interactions(rxcui)
            
            return {
                "drug": drug_name,
                "rxcui": rxcui,
                "source": "rxnorm_nih",
                "interactions": interactions
            }
        except Exception as e:
            return {"error": str(e)}
    
    def _assess_data_quality(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Assess the quality and completeness of the data"""
        sources_used = list(results.get("sources", {}).keys())
        
        quality = {
            "sources_count": len(sources_used),
            "sources_used": sources_used,
            "has_research": "pubmed" in sources_used,
            "has_official_data": "openfda" in sources_used or "rxnorm" in sources_used,
            "has_local_data": "local_database" in sources_used,
            "confidence": "high" if len(sources_used) >= 2 else "medium" if sources_used else "low"
        }
        
        return quality
    
    def get_available_providers(self) -> List[str]:
        """Get list of available providers"""
        return list(self.providers.keys())
    
    def get_status(self) -> Dict[str, Any]:
        """Get router status"""
        return {
            "providers_count": len(self.providers),
            "providers": self.get_available_providers(),
            "status": "healthy" if self.providers else "no_providers"
        }


# Singleton instance
medical_router = MedicalRouter()


# Convenience functions
async def get_health_info(query: str, query_type: str = "general") -> Dict[str, Any]:
    """Quick access to health information"""
    return await medical_router.get_comprehensive_health_info(query, query_type)


async def get_drug_info(drug_name: str) -> Dict[str, Any]:
    """Quick access to drug information"""
    return await medical_router.get_comprehensive_health_info(drug_name, "drug")


async def get_disease_info(disease: str) -> Dict[str, Any]:
    """Quick access to disease information"""
    return await medical_router.get_comprehensive_health_info(disease, "disease")
