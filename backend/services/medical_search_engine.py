"""
Medical Search System - Fast vs Deep Search
Optimized tiered medical data retrieval
"""
import asyncio
import time
from typing import Dict, Any, List, Optional
from enum import Enum
from dataclasses import dataclass


class SearchMode(str, Enum):
    """Search modes for medical queries"""
    FAST = "fast"          # ~0.5-1s - Local + 1 API
    STANDARD = "standard"  # ~1-3s - Local + 3 APIs principales
    DEEP = "deep"          # ~3-8s - Toutes les APIs (13+)


@dataclass
class SearchConfig:
    """Configuration for each search level"""
    name: str
    max_time_seconds: float
    apis: List[str]
    description: str


# ============================================
# SEARCH TIER CONFIGURATIONS
# ============================================

SEARCH_TIERS = {
    SearchMode.FAST: SearchConfig(
        name="Recherche Rapide",
        max_time_seconds=1.5,
        apis=["open_disease", "drugbank_open", "loinc"],  # Local only
        description="Réponse instantanée basée sur la base locale"
    ),
    SearchMode.STANDARD: SearchConfig(
        name="Recherche Standard", 
        max_time_seconds=4.0,
        apis=[
            # Local (instant)
            "open_disease", "drugbank_open", "loinc",
            # Fast APIs
            "pubmed", "openfda", "rxnorm"
        ],
        description="Recherche équilibrée avec sources principales"
    ),
    SearchMode.DEEP: SearchConfig(
        name="Recherche Approfondie",
        max_time_seconds=12.0,
        apis=[
            # Local (instant)
            "open_disease", "drugbank_open", "loinc",
            # Primary APIs
            "pubmed", "openfda", "rxnorm",
            # Secondary APIs
            "disease_sh", "europe_pmc", "clinical_trials",
            # Tertiary APIs
            "who_gho", "snomed_ct", "icd11", "orphanet", "open_targets"
        ],
        description="Scan complet de toutes les sources médicales mondiales"
    )
}


class MedicalSearchEngine:
    """
    Intelligent medical search with tiered API access.
    Optimizes speed vs completeness based on user needs.
    """
    
    def __init__(self):
        self.providers = {}
        self.provider_latencies = {}  # Track API response times
        self._init_providers()
    
    def _init_providers(self):
        """Initialize all available providers"""
        # Local providers (instant - <10ms)
        try:
            from services.external_apis.medical_extended import open_disease
            self.providers["open_disease"] = {
                "instance": open_disease,
                "method": "get_disease_info",
                "tier": "local",
                "avg_latency_ms": 5
            }
        except:
            pass
        
        try:
            from services.external_apis.medical_world import drugbank_open, loinc
            self.providers["drugbank_open"] = {
                "instance": drugbank_open,
                "method": "get_drug_info",
                "tier": "local",
                "avg_latency_ms": 5
            }
            self.providers["loinc"] = {
                "instance": loinc,
                "method": "get_lab_info",
                "tier": "local",
                "avg_latency_ms": 5
            }
        except:
            pass
        
        # Primary APIs (fast - 100-500ms)
        try:
            from services.external_apis.medical import pubmed, openfda
            self.providers["pubmed"] = {
                "instance": pubmed,
                "method": "search_articles",
                "tier": "primary",
                "avg_latency_ms": 300
            }
            self.providers["openfda"] = {
                "instance": openfda,
                "method": "search_drugs",
                "tier": "primary",
                "avg_latency_ms": 400
            }
        except:
            pass
        
        try:
            from services.external_apis.medical_extended import rxnorm, disease_sh
            self.providers["rxnorm"] = {
                "instance": rxnorm,
                "method": "search_drug",
                "tier": "primary",
                "avg_latency_ms": 350
            }
            self.providers["disease_sh"] = {
                "instance": disease_sh,
                "method": "get_disease_info",
                "tier": "secondary",
                "avg_latency_ms": 200
            }
        except:
            pass
        
        # Secondary APIs (medium - 500-1000ms)
        try:
            from services.external_apis.medical_world import (
                europe_pmc, clinical_trials, snomed_ct, icd11, orphanet, open_targets
            )
            self.providers["europe_pmc"] = {
                "instance": europe_pmc,
                "method": "search_articles",
                "tier": "secondary",
                "avg_latency_ms": 600
            }
            self.providers["clinical_trials"] = {
                "instance": clinical_trials,
                "method": "search_trials",
                "tier": "secondary",
                "avg_latency_ms": 800
            }
            self.providers["snomed_ct"] = {
                "instance": snomed_ct,
                "method": "search_concept",
                "tier": "tertiary",
                "avg_latency_ms": 700
            }
            self.providers["icd11"] = {
                "instance": icd11,
                "method": "search_disease",
                "tier": "tertiary",
                "avg_latency_ms": 900
            }
            self.providers["orphanet"] = {
                "instance": orphanet,
                "method": "search_disease",
                "tier": "tertiary",
                "avg_latency_ms": 1000
            }
            self.providers["open_targets"] = {
                "instance": open_targets,
                "method": "search_disease",
                "tier": "tertiary",
                "avg_latency_ms": 800
            }
        except:
            pass
        
        try:
            from services.external_apis.medical_extended import who_gho
            self.providers["who_gho"] = {
                "instance": who_gho,
                "method": "get_indicators",
                "tier": "tertiary",
                "avg_latency_ms": 1200
            }
        except:
            pass
        
        print(f"[OK] Medical Search Engine: {len(self.providers)} providers loaded")
    
    async def search(
        self, 
        query: str, 
        mode: SearchMode = SearchMode.STANDARD,
        query_type: str = "general"  # general, drug, disease, lab
    ) -> Dict[str, Any]:
        """
        Perform a medical search with the specified mode.
        
        Args:
            query: The search query
            mode: FAST, STANDARD, or DEEP
            query_type: Type of query for optimization
            
        Returns:
            Dict with results, sources, and timing info
        """
        start_time = time.time()
        config = SEARCH_TIERS[mode]
        
        results = {
            "query": query,
            "mode": mode.value,
            "mode_name": config.name,
            "sources": {},
            "combined_data": {},
            "timing": {},
            "apis_called": 0,
            "apis_successful": 0
        }
        
        # Filter providers based on mode and query type
        apis_to_call = self._select_apis(config.apis, query_type)
        
        # Create tasks for parallel execution
        tasks = []
        task_names = []
        
        for api_name in apis_to_call:
            if api_name in self.providers:
                provider = self.providers[api_name]
                task = self._call_provider_safe(
                    api_name,
                    provider,
                    query,
                    timeout=config.max_time_seconds / 2  # Individual timeout
                )
                tasks.append(task)
                task_names.append(api_name)
        
        results["apis_called"] = len(tasks)
        
        # Execute all tasks in parallel with overall timeout
        try:
            task_results = await asyncio.wait_for(
                asyncio.gather(*tasks, return_exceptions=True),
                timeout=config.max_time_seconds
            )
            
            # Process results
            for i, (api_name, task_result) in enumerate(zip(task_names, task_results)):
                if isinstance(task_result, Exception):
                    results["sources"][api_name] = {"error": str(task_result)}
                elif task_result:
                    results["sources"][api_name] = task_result
                    results["apis_successful"] += 1
                    
                    # Merge into combined data
                    self._merge_result(results["combined_data"], api_name, task_result)
                    
        except asyncio.TimeoutError:
            results["timing"]["timeout"] = True
        
        # Calculate timing
        total_time = time.time() - start_time
        results["timing"]["total_seconds"] = round(total_time, 3)
        results["timing"]["total_ms"] = round(total_time * 1000)
        
        # Add search summary
        results["summary"] = self._generate_summary(results)
        
        return results
    
    def _select_apis(self, allowed_apis: List[str], query_type: str) -> List[str]:
        """Select optimal APIs based on query type"""
        # Prioritize based on query type
        priority_map = {
            "drug": ["drugbank_open", "rxnorm", "openfda", "pubmed"],
            "disease": ["open_disease", "pubmed", "europe_pmc", "clinical_trials", "orphanet"],
            "lab": ["loinc", "pubmed"],
            "general": allowed_apis
        }
        
        priority_apis = priority_map.get(query_type, allowed_apis)
        
        # Return APIs that are both in priority list and allowed list
        result = []
        for api in priority_apis:
            if api in allowed_apis and api in self.providers:
                result.append(api)
        
        # Add remaining allowed APIs
        for api in allowed_apis:
            if api not in result and api in self.providers:
                result.append(api)
        
        return result
    
    async def _call_provider_safe(
        self, 
        name: str, 
        provider: Dict, 
        query: str,
        timeout: float
    ) -> Optional[Dict]:
        """Safely call a provider with timeout"""
        try:
            start = time.time()
            
            instance = provider["instance"]
            method_name = provider["method"]
            method = getattr(instance, method_name)
            
            # Call with timeout
            result = await asyncio.wait_for(
                method(query),
                timeout=timeout
            )
            
            # Track latency
            latency = (time.time() - start) * 1000
            self.provider_latencies[name] = latency
            
            if result:
                result["_latency_ms"] = round(latency)
                result["_source"] = name
            
            return result
            
        except asyncio.TimeoutError:
            return {"error": "timeout", "_source": name}
        except Exception as e:
            return {"error": str(e), "_source": name}
    
    def _merge_result(self, combined: Dict, source: str, result: Dict):
        """Merge a result into the combined data"""
        # Extract useful data based on source
        if source == "open_disease" and result.get("found"):
            combined["disease_info"] = {
                k: v for k, v in result.items() 
                if k not in ["_latency_ms", "_source", "found", "source"]
            }
            combined["disease_info"]["_source"] = "Base locale"
        
        elif source == "drugbank_open" and result.get("found"):
            combined["drug_info"] = {
                k: v for k, v in result.items()
                if k not in ["_latency_ms", "_source", "found", "source"]
            }
            combined["drug_info"]["_source"] = "DrugBank"
        
        elif source == "pubmed" and result.get("articles"):
            combined["research_articles"] = result.get("articles", [])[:5]
            combined["research_count"] = result.get("count", 0)
        
        elif source == "europe_pmc" and result.get("articles"):
            if "research_articles" not in combined:
                combined["research_articles"] = []
            combined["research_articles"].extend(result.get("articles", [])[:3])
        
        elif source == "clinical_trials" and result.get("trials"):
            combined["clinical_trials"] = result.get("trials", [])[:5]
        
        elif source == "rxnorm" and result.get("drugs"):
            combined["rxnorm_data"] = result.get("drugs", [])[:5]
        
        elif source == "loinc" and result.get("found"):
            combined["lab_info"] = result
    
    def _generate_summary(self, results: Dict) -> Dict:
        """Generate a human-readable summary"""
        sources_used = [
            k for k, v in results["sources"].items() 
            if isinstance(v, dict) and not v.get("error")
        ]
        
        return {
            "sources_count": len(sources_used),
            "sources_list": sources_used,
            "success_rate": f"{results['apis_successful']}/{results['apis_called']}",
            "response_time": f"{results['timing'].get('total_ms', 0)}ms",
            "data_quality": "high" if len(sources_used) >= 3 else "medium" if sources_used else "low"
        }
    
    def get_mode_info(self, mode: SearchMode) -> Dict:
        """Get information about a search mode"""
        config = SEARCH_TIERS[mode]
        available_apis = [a for a in config.apis if a in self.providers]
        
        return {
            "mode": mode.value,
            "name": config.name,
            "description": config.description,
            "max_time": f"{config.max_time_seconds}s",
            "apis_available": len(available_apis),
            "apis": available_apis
        }
    
    def get_all_modes_info(self) -> List[Dict]:
        """Get information about all search modes"""
        return [self.get_mode_info(mode) for mode in SearchMode]


# ============================================
# SINGLETON & CONVENIENCE FUNCTIONS
# ============================================

medical_search_engine = MedicalSearchEngine()


async def fast_medical_search(query: str, query_type: str = "general") -> Dict[str, Any]:
    """
    Quick medical search (~0.5-1s)
    Uses only local database - instant results
    """
    return await medical_search_engine.search(query, SearchMode.FAST, query_type)


async def standard_medical_search(query: str, query_type: str = "general") -> Dict[str, Any]:
    """
    Standard medical search (~1-3s)
    Uses local + main APIs (PubMed, FDA, RxNorm)
    """
    return await medical_search_engine.search(query, SearchMode.STANDARD, query_type)


async def deep_medical_search(query: str, query_type: str = "general") -> Dict[str, Any]:
    """
    Comprehensive medical search (~3-10s)
    Scans ALL 13+ medical APIs worldwide
    """
    return await medical_search_engine.search(query, SearchMode.DEEP, query_type)


# ============================================
# API COUNT SUMMARY
# ============================================

def get_api_summary() -> Dict[str, Any]:
    """Get summary of all available medical APIs"""
    engine = medical_search_engine
    
    local_apis = [p for p, info in engine.providers.items() if info.get("tier") == "local"]
    primary_apis = [p for p, info in engine.providers.items() if info.get("tier") == "primary"]
    secondary_apis = [p for p, info in engine.providers.items() if info.get("tier") == "secondary"]
    tertiary_apis = [p for p, info in engine.providers.items() if info.get("tier") == "tertiary"]
    
    return {
        "total_apis": len(engine.providers),
        "local": {"count": len(local_apis), "apis": local_apis, "latency": "<10ms"},
        "primary": {"count": len(primary_apis), "apis": primary_apis, "latency": "100-500ms"},
        "secondary": {"count": len(secondary_apis), "apis": secondary_apis, "latency": "500-1000ms"},
        "tertiary": {"count": len(tertiary_apis), "apis": tertiary_apis, "latency": "1000ms+"},
        "modes": {
            "fast": {"apis": 3, "time": "~1s", "sources": "Local only"},
            "standard": {"apis": 6, "time": "~3s", "sources": "Local + Main APIs"},
            "deep": {"apis": "13+", "time": "~8s", "sources": "All worldwide sources"}
        }
    }
