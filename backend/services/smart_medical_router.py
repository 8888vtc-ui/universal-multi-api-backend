"""
Smart Medical Search Router
Routes queries to ONLY relevant APIs + mandatory ones
Optimizes performance by not calling unnecessary APIs
"""
import asyncio
import time
from typing import Dict, Any, List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class SmartSearchResult:
    """Result of smart medical search"""
    query: str
    detected_topics: List[str]
    apis_called: List[str]
    apis_with_data: List[str]
    mandatory_apis: List[str]
    topic_specific_apis: List[str]
    total_time_ms: float
    progress_log: List[str]
    data: Dict[str, Any]
    sources_summary: str


class SmartMedicalRouter:
    """
    Intelligent router that:
    1. Detects the topic of the query (diabetes, cancer, drugs, etc.)
    2. Selects ONLY relevant APIs for that topic
    3. ALWAYS includes mandatory APIs (PubMed, WHO, FDA, etc.)
    4. Executes searches in parallel for speed
    """
    
    def __init__(self):
        self.registry = None
        self.providers = {}
        self._init_registry()
        self._init_providers()
    
    def _init_registry(self):
        """Load the mega registry"""
        try:
            from services.external_apis.medical_mega_registry import MegaMedicalRegistry
            self.registry = MegaMedicalRegistry
            print(f"[OK] Smart Router: {self.registry.count_apis()['total']} APIs in registry")
        except Exception as e:
            print(f"[WARN] Could not load registry: {e}")
    
    def _init_providers(self):
        """Initialize available providers"""
        # Import all available providers
        provider_configs = [
            # Primary Literature
            ("pubmed", "services.external_apis.medical", "PubMedProvider", "search_articles"),
            ("openfda", "services.external_apis.medical", "OpenFDAProvider", "search_drugs"),
            
            # Extended APIs
            ("rxnorm", "services.external_apis.medical_extended", "rxnorm", "search_drug"),
            ("disease_sh", "services.external_apis.medical_extended", "disease_sh", "get_disease_info"),
            ("who_gho", "services.external_apis.medical_extended", "who_gho", "get_indicators"),
            ("open_disease", "services.external_apis.medical_extended", "open_disease", "get_disease_info"),
            
            # World APIs
            ("europe_pmc", "services.external_apis.medical_world", "europe_pmc", "search_articles"),
            ("clinical_trials", "services.external_apis.medical_world", "clinical_trials", "search_trials"),
            ("snomed_ct", "services.external_apis.medical_world", "snomed_ct", "search_concept"),
            ("orphanet", "services.external_apis.medical_world", "orphanet", "search_disease"),
            ("drugbank", "services.external_apis.medical_world", "drugbank_open", "get_drug_info"),
            ("loinc", "services.external_apis.medical_world", "loinc", "get_lab_info"),
            
            # Premium APIs
            ("mesh", "services.external_apis.medical_premium", "mesh_provider", "search_term"),
            ("ncbi_gene", "services.external_apis.medical_premium", "ncbi_gene", "search_gene"),
            ("drug_central", "services.external_apis.medical_premium", "drug_central", "get_drug_info"),
            ("kegg", "services.external_apis.medical_premium", "kegg_provider", "get_pathway"),
            ("omim", "services.external_apis.medical_premium", "omim_provider", "get_genetic_disease"),
            
            # Ultimate APIs
            ("semantic_scholar", "services.external_apis.medical_ultimate", "semantic_scholar", "search_papers"),
            ("clinvar", "services.external_apis.medical_ultimate", "clinvar", "search_variants"),
            ("reactome", "services.external_apis.medical_ultimate", "reactome", "search_pathways"),
            ("uniprot", "services.external_apis.medical_ultimate", "uniprot", "search_proteins"),
            ("gard", "services.external_apis.medical_ultimate", "gard", "search_rare_disease"),
        ]
        
        for api_id, module_path, provider_name, method_name in provider_configs:
            try:
                module = __import__(module_path, fromlist=[provider_name])
                provider = getattr(module, provider_name)
                
                # Handle class vs instance
                if isinstance(provider, type):
                    provider = provider()
                
                self.providers[api_id] = {
                    "instance": provider,
                    "method": method_name
                }
            except Exception as e:
                pass  # Provider not available
        
        print(f"[OK] Smart Router: {len(self.providers)} providers ready")
    
    def get_relevant_apis(self, query: str, force_all: bool = False) -> Tuple[List[str], List[str], List[str]]:
        """
        Get relevant APIs for a query.
        Returns: (mandatory_apis, topic_apis, detected_topics)
        ENSURES AT LEAST 15 APIs, or ALL if force_all=True.
        """
        if not self.registry:
            # Fallback: return all available providers
            return list(self.providers.keys()), [], ["general"]
        
        # Detect topics
        topics = self.registry.detect_topics(query)
        
        # Get relevant APIs from registry
        relevant = self.registry.get_relevant_apis(query)
        
        mandatory = []
        topic_specific = []
        selected_ids = set()
        
        for api in relevant:
            api_id = api.get("id")
            if api_id in self.providers:  # Only include available providers
                selected_ids.add(api_id)
                if api.get("reason") == "mandatory":
                    mandatory.append(api_id)
                else:
                    topic_specific.append(api_id)
        
        # --- ENSURE MINIMUM OR FORCE ALL ---
        total_selected = len(mandatory) + len(topic_specific)
        
        if force_all:
             # FORCE ALL AVAILABLE PROVIDERS
             available = [p for p in self.providers.keys() if p not in selected_ids]
             # Add strictly all
             for p in available:
                 topic_specific.append(p)
                 selected_ids.add(p)
                 
        else:
            # Min 15 logic
            min_apis = 15
            if total_selected < min_apis:
                # Get all available providers that are NOT selected
                available = [p for p in self.providers.keys() if p not in selected_ids]
                
                # Sort available to have somewhat deterministic behavior
                available.sort() 
                
                for i in range(min(min_apis - total_selected, len(available))):
                    extra_api = available[i]
                    topic_specific.append(extra_api)
                    selected_ids.add(extra_api)
        
        return mandatory, topic_specific, topics
    
    async def search_api(self, api_id: str, query: str) -> Tuple[str, Dict]:
        """Search a single API"""
        if api_id not in self.providers:
            return api_id, {"found": False, "error": "Provider not available"}
        
        provider = self.providers[api_id]
        start = time.time()
        
        try:
            method = getattr(provider["instance"], provider["method"])
            result = await asyncio.wait_for(method(query), timeout=15.0)
            elapsed = (time.time() - start) * 1000
            
            if isinstance(result, dict):
                result["_latency_ms"] = elapsed
                return api_id, result
            
            return api_id, {"found": False, "_latency_ms": elapsed}
            
        except asyncio.TimeoutError:
            return api_id, {"found": False, "error": "timeout", "_latency_ms": 15000}
        except Exception as e:
            return api_id, {"found": False, "error": str(e)}
    
    async def smart_search(self, query: str, force_all: bool = False) -> SmartSearchResult:
        """
        Perform intelligent search:
        1. Detect topics
        2. Get relevant APIs
        3. Call mandatory + topic APIs in parallel
        4. Return structured result
        """
        start_time = time.time()
        progress_log = []
        
        # Header
        progress_log.append("=" * 60)
        progress_log.append("🧠 RECHERCHE MEDICALE INTELLIGENTE")
        progress_log.append(f"📋 Requete: {query[:100]}...")
        if force_all:
            progress_log.append("🚀 MODE MAXIMAL: 74 APIs ACTIVÉES")
        progress_log.append("=" * 60)
        progress_log.append("")
        
        # Get relevant APIs
        mandatory, topic_specific, topics = self.get_relevant_apis(query, force_all=force_all)
        
        progress_log.append(f"🎯 Sujets detectes: {', '.join(topics)}")
        progress_log.append(f"⭐ APIs obligatoires: {len(mandatory)}")
        progress_log.append(f"🔍 APIs specifiques: {len(topic_specific)}")
        progress_log.append("")
        
        # Phase 1: Mandatory APIs
        progress_log.append("⭐ PHASE 1: APIs OBLIGATOIRES (toujours consultees)")
        progress_log.append("-" * 50)
        
        mandatory_results = {}
        if mandatory:
            tasks = [self.search_api(api_id, query) for api_id in mandatory]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            for api_id, result in zip(mandatory, results):
                if isinstance(result, tuple):
                    api_id, data = result
                    mandatory_results[api_id] = data
                    has_data = data.get("found") or data.get("count", 0) > 0 or data.get("articles")
                    status = "✅" if has_data else "⚪"
                    latency = data.get("_latency_ms", 0)
                    progress_log.append(f"  {status} {api_id}: {latency:.0f}ms")
        
        progress_log.append("")
        
        # Phase 2: Topic-specific APIs
        progress_log.append(f"🔍 PHASE 2: APIs SPECIFIQUES ({', '.join(topics)})")
        progress_log.append("-" * 50)
        
        topic_results = {}
        if topic_specific:
            tasks = [self.search_api(api_id, query) for api_id in topic_specific]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            for api_id, result in zip(topic_specific, results):
                if isinstance(result, tuple):
                    api_id, data = result
                    topic_results[api_id] = data
                    has_data = data.get("found") or data.get("count", 0) > 0 or data.get("articles")
                    status = "✅" if has_data else "⚪"
                    latency = data.get("_latency_ms", 0)
                    progress_log.append(f"  {status} {api_id}: {latency:.0f}ms")
        
        progress_log.append("")
        
        # Combine results
        all_data = {**mandatory_results, **topic_results}
        apis_with_data = [
            api_id for api_id, data in all_data.items()
            if data.get("found") or data.get("count", 0) > 0 or data.get("articles")
        ]
        
        # Summary
        total_time = (time.time() - start_time) * 1000
        
        progress_log.append("=" * 60)
        progress_log.append("📊 RESUME")
        progress_log.append("=" * 60)
        progress_log.append(f"⏱️  Temps total: {total_time:.0f}ms ({total_time/1000:.1f}s)")
        progress_log.append(f"🔍 APIs appelees: {len(mandatory) + len(topic_specific)}")
        progress_log.append(f"✅ APIs avec donnees: {len(apis_with_data)}")
        progress_log.append(f"📈 Economie: {77 - len(mandatory) - len(topic_specific)} APIs non appelees")
        
        # Sources summary
        sources = []
        if self.registry:
            for api_id in apis_with_data:
                api_info = self.registry.APIS.get(api_id, {})
                icon = api_info.get("icon", "📊")
                name = api_info.get("name", api_id)
                sources.append(f"{icon} {name}")
        
        sources_summary = "\n".join(sources) if sources else "Aucune source avec donnees"
        
        return SmartSearchResult(
            query=query,
            detected_topics=topics,
            apis_called=mandatory + topic_specific,
            apis_with_data=apis_with_data,
            mandatory_apis=mandatory,
            topic_specific_apis=topic_specific,
            total_time_ms=total_time,
            progress_log=progress_log,
            data=all_data,
            sources_summary=sources_summary
        )
    
    def format_context(self, result: SmartSearchResult) -> str:
        """Format search result as context for AI"""
        parts = []
        
        # Progress log
        parts.append("\n".join(result.progress_log))
        parts.append("")
        
        # Data
        parts.append("=" * 60)
        parts.append("📋 DONNEES COLLECTEES")
        parts.append("=" * 60)
        
        for api_id, data in result.data.items():
            if not (data.get("found") or data.get("count", 0) > 0 or data.get("articles")):
                continue
            
            api_info = self.registry.APIS.get(api_id, {}) if self.registry else {}
            icon = api_info.get("icon", "📊")
            name = api_info.get("name", api_id)
            
            parts.append(f"\n{icon} [{name.upper()}]:")
            
            # Format data
            if isinstance(data, dict):
                for key, value in list(data.items())[:5]:
                    if key.startswith("_") or key in ["source", "error"]:
                        continue
                    if isinstance(value, str) and len(value) < 300:
                        parts.append(f"  {key}: {value}")
                    elif isinstance(value, list) and len(value) > 0:
                        parts.append(f"  {key}: {len(value)} elements")
        
        # Sources
        parts.append("\n" + "=" * 60)
        parts.append("📚 SOURCES:")
        parts.append("=" * 60)
        parts.append(result.sources_summary)
        
        return "\n".join(parts)


# Singleton
smart_router = SmartMedicalRouter()


async def smart_medical_search(query: str) -> Tuple[str, SmartSearchResult]:
    """
    Convenience function for smart search.
    Returns (formatted_context, result)
    """
    result = await smart_router.smart_search(query)
    context = smart_router.format_context(result)
    return context, result


# Export count for display
def get_api_stats() -> Dict[str, Any]:
    """Get API statistics for display"""
    if smart_router.registry:
        stats = smart_router.registry.count_apis()
        stats["active_providers"] = len(smart_router.providers)
        return stats
    return {"total": len(smart_router.providers), "active_providers": len(smart_router.providers)}
