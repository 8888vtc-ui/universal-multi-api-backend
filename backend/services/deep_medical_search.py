"""
Deep Medical Research Engine
Comprehensive search across ALL medical APIs with live progress
Shows user exactly where we're searching - transparency = trust
"""
import asyncio
import time
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum


@dataclass
class SearchProgress:
    """Progress of a single API search"""
    api_name: str
    display_name: str
    status: str  # "searching", "found", "no_data", "error"
    results_count: int = 0
    data: Optional[Dict] = None
    time_ms: float = 0


@dataclass
class DeepSearchResult:
    """Complete result of deep medical search"""
    query: str
    total_time_ms: float
    apis_searched: List[str]
    apis_with_data: List[str]
    progress_log: List[str]
    combined_data: Dict[str, Any]
    report_sections: Dict[str, str]
    sources_summary: str
    quality_score: float


class DeepMedicalSearch:
    """
    Comprehensive medical search engine that:
    1. Searches ALL relevant medical APIs
    2. Provides real-time progress updates
    3. Builds a comprehensive report
    4. Shows transparency on sources
    """
    
    # API configurations with display names
    API_CONFIG = {
        # Local databases (instant)
        "open_disease": {
            "display": "Base de maladies locale",
            "icon": "📚",
            "type": "local"
        },
        "drugbank_open": {
            "display": "DrugBank (Medicaments)",
            "icon": "💊",
            "type": "local"
        },
        "loinc": {
            "display": "LOINC (Laboratoire)",
            "icon": "🧪",
            "type": "local"
        },
        
        # Primary APIs (fast)
        "pubmed": {
            "display": "PubMed NCBI (35M+ etudes)",
            "icon": "📖",
            "type": "primary"
        },
        "openfda": {
            "display": "FDA USA (Medicaments approuves)",
            "icon": "🇺🇸",
            "type": "primary"
        },
        "rxnorm": {
            "display": "RxNorm NIH (Terminologie)",
            "icon": "💉",
            "type": "primary"
        },
        
        # Secondary APIs (medium)
        "europe_pmc": {
            "display": "Europe PMC (Litterature EU)",
            "icon": "🇪🇺",
            "type": "secondary"
        },
        "clinical_trials": {
            "display": "ClinicalTrials.gov (400K+ essais)",
            "icon": "🔬",
            "type": "secondary"
        },
        "disease_sh": {
            "display": "Disease.sh (Epidemiologie)",
            "icon": "🦠",
            "type": "secondary"
        },
        
        # Tertiary APIs (comprehensive)
        "who_gho": {
            "display": "OMS/WHO (Stats mondiales)",
            "icon": "🌍",
            "type": "tertiary"
        },
        "snomed_ct": {
            "display": "SNOMED CT (Classification)",
            "icon": "🏥",
            "type": "tertiary"
        },
        "orphanet": {
            "display": "Orphanet (6000+ maladies rares)",
            "icon": "🧬",
            "type": "tertiary"
        },
        
        # Premium APIs (specialized - NEW)
        "mesh": {
            "display": "MeSH NLM (30K+ termes medicaux)",
            "icon": "📑",
            "type": "premium"
        },
        "ncbi_gene": {
            "display": "NCBI Gene (Genetique)",
            "icon": "🔬",
            "type": "premium"
        },
        "drug_central": {
            "display": "DrugCentral (Pharmacologie)",
            "icon": "💎",
            "type": "premium"
        },
        "kegg": {
            "display": "KEGG (Voies metaboliques)",
            "icon": "🔄",
            "type": "premium"
        },
        "omim": {
            "display": "OMIM (Maladies genetiques)",
            "icon": "🧬",
            "type": "premium"
        },
        
        # Elite APIs (NEW - World's Best)
        "semantic_scholar": {
            "display": "Semantic Scholar (200M+ articles IA)",
            "icon": "🧠",
            "type": "elite"
        },
        "clinvar": {
            "display": "ClinVar (Variants genetiques)",
            "icon": "🧪",
            "type": "elite"
        },
        "reactome": {
            "display": "Reactome (2600+ voies biologiques)",
            "icon": "⚡",
            "type": "elite"
        },
        "uniprot": {
            "display": "UniProt (Proteines)",
            "icon": "🔬",
            "type": "elite"
        },
        "gard": {
            "display": "GARD NIH (7000+ maladies rares)",
            "icon": "🏥",
            "type": "elite"
        }
    }
    
    def __init__(self):
        self.providers = {}
        self._init_providers()
    
    def _init_providers(self):
        """Initialize all available providers"""
        # Local providers
        try:
            from services.external_apis.medical_extended import open_disease
            self.providers["open_disease"] = {
                "instance": open_disease,
                "method": "get_disease_info"
            }
        except:
            pass
        
        try:
            from services.external_apis.medical_world import drugbank_open, loinc
            self.providers["drugbank_open"] = {
                "instance": drugbank_open,
                "method": "get_drug_info"
            }
            self.providers["loinc"] = {
                "instance": loinc,
                "method": "get_lab_info"
            }
        except:
            pass
        
        # Primary APIs
        try:
            from services.external_apis.medical import PubMedProvider, OpenFDAProvider
            self.providers["pubmed"] = {
                "instance": PubMedProvider(),
                "method": "search_articles"
            }
            self.providers["openfda"] = {
                "instance": OpenFDAProvider(),
                "method": "search_drugs"
            }
        except:
            pass
        
        try:
            from services.external_apis.medical_extended import rxnorm, disease_sh, who_gho
            self.providers["rxnorm"] = {
                "instance": rxnorm,
                "method": "search_drug"
            }
            self.providers["disease_sh"] = {
                "instance": disease_sh,
                "method": "get_disease_info"
            }
            self.providers["who_gho"] = {
                "instance": who_gho,
                "method": "get_indicators"
            }
        except:
            pass
        
        # World APIs
        try:
            from services.external_apis.medical_world import (
                europe_pmc, clinical_trials, snomed_ct, orphanet
            )
            self.providers["europe_pmc"] = {
                "instance": europe_pmc,
                "method": "search_articles"
            }
            self.providers["clinical_trials"] = {
                "instance": clinical_trials,
                "method": "search_trials"
            }
            self.providers["snomed_ct"] = {
                "instance": snomed_ct,
                "method": "search_concept"
            }
            self.providers["orphanet"] = {
                "instance": orphanet,
                "method": "search_disease"
            }
        except:
            pass
        
        # Premium APIs (NEW)
        try:
            from services.external_apis.medical_premium import (
                mesh_provider, ncbi_gene, drug_central, kegg_provider, omim_provider
            )
            self.providers["mesh"] = {
                "instance": mesh_provider,
                "method": "search_term"
            }
            self.providers["ncbi_gene"] = {
                "instance": ncbi_gene,
                "method": "search_gene"
            }
            self.providers["drug_central"] = {
                "instance": drug_central,
                "method": "get_drug_info"
            }
            self.providers["kegg"] = {
                "instance": kegg_provider,
                "method": "get_pathway"
            }
            self.providers["omim"] = {
                "instance": omim_provider,
                "method": "get_genetic_disease"
            }
        except Exception as e:
            print(f"[WARN] Premium APIs not loaded: {e}")
        
        # Elite APIs (World's Best)
        try:
            from services.external_apis.medical_ultimate import (
                semantic_scholar, clinvar, reactome, uniprot, gard
            )
            self.providers["semantic_scholar"] = {
                "instance": semantic_scholar,
                "method": "search_papers"
            }
            self.providers["clinvar"] = {
                "instance": clinvar,
                "method": "search_variants"
            }
            self.providers["reactome"] = {
                "instance": reactome,
                "method": "search_pathways"
            }
            self.providers["uniprot"] = {
                "instance": uniprot,
                "method": "search_proteins"
            }
            self.providers["gard"] = {
                "instance": gard,
                "method": "search_rare_disease"
            }
        except Exception as e:
            print(f"[WARN] Elite APIs not loaded: {e}")
        
        print(f"[OK] Deep Medical Search: {len(self.providers)} APIs ready")
    
    async def search_single_api(self, api_name: str, query: str) -> SearchProgress:
        """Search a single API and return progress"""
        config = self.API_CONFIG.get(api_name, {})
        display_name = config.get("display", api_name)
        
        if api_name not in self.providers:
            return SearchProgress(
                api_name=api_name,
                display_name=display_name,
                status="unavailable"
            )
        
        provider = self.providers[api_name]
        start_time = time.time()
        
        try:
            method = getattr(provider["instance"], provider["method"])
            result = await asyncio.wait_for(method(query), timeout=15.0)
            
            elapsed = (time.time() - start_time) * 1000
            
            # Check if we got data
            has_data = False
            count = 0
            
            if isinstance(result, dict):
                if result.get("found"):
                    has_data = True
                    count = 1
                elif result.get("count", 0) > 0:
                    has_data = True
                    count = result.get("count", 0)
                elif result.get("articles"):
                    has_data = True
                    count = len(result.get("articles", []))
                elif result.get("trials"):
                    has_data = True
                    count = len(result.get("trials", []))
            
            return SearchProgress(
                api_name=api_name,
                display_name=display_name,
                status="found" if has_data else "no_data",
                results_count=count,
                data=result if has_data else None,
                time_ms=elapsed
            )
            
        except asyncio.TimeoutError:
            return SearchProgress(
                api_name=api_name,
                display_name=display_name,
                status="timeout",
                time_ms=15000
            )
        except Exception as e:
            return SearchProgress(
                api_name=api_name,
                display_name=display_name,
                status="error",
                time_ms=(time.time() - start_time) * 1000
            )
    
    def generate_progress_message(self, progress: SearchProgress) -> str:
        """Generate user-friendly progress message"""
        config = self.API_CONFIG.get(progress.api_name, {})
        icon = config.get("icon", "🔍")
        
        if progress.status == "searching":
            return f"{icon} Recherche sur {progress.display_name}..."
        elif progress.status == "found":
            return f"{icon} ✅ {progress.display_name}: {progress.results_count} resultat(s) ({progress.time_ms:.0f}ms)"
        elif progress.status == "no_data":
            return f"{icon} ⚪ {progress.display_name}: Aucune donnee"
        elif progress.status == "timeout":
            return f"{icon} ⏱️ {progress.display_name}: Timeout"
        elif progress.status == "error":
            return f"{icon} ❌ {progress.display_name}: Erreur"
        else:
            return f"{icon} {progress.display_name}: {progress.status}"
    
    async def deep_search(self, query: str) -> DeepSearchResult:
        """
        Perform comprehensive search across ALL medical APIs.
        Returns detailed results with progress log.
        """
        start_time = time.time()
        progress_log = []
        all_results = {}
        
        # Header
        progress_log.append("=" * 50)
        progress_log.append("🔬 RECHERCHE MEDICALE APPROFONDIE")
        progress_log.append(f"📋 Requete: {query}")
        progress_log.append("=" * 50)
        progress_log.append("")
        
        # Phase 1: Local databases (instant)
        progress_log.append("📚 PHASE 1: Bases de donnees locales")
        progress_log.append("-" * 40)
        
        local_apis = [k for k, v in self.API_CONFIG.items() if v.get("type") == "local"]
        for api_name in local_apis:
            if api_name in self.providers:
                result = await self.search_single_api(api_name, query)
                all_results[api_name] = result
                progress_log.append(self.generate_progress_message(result))
        
        progress_log.append("")
        
        # Phase 2: Primary APIs (parallel)
        progress_log.append("🌐 PHASE 2: APIs principales (PubMed, FDA, RxNorm)")
        progress_log.append("-" * 40)
        
        primary_apis = [k for k, v in self.API_CONFIG.items() if v.get("type") == "primary"]
        primary_tasks = []
        for api_name in primary_apis:
            if api_name in self.providers:
                primary_tasks.append((api_name, self.search_single_api(api_name, query)))
        
        if primary_tasks:
            results = await asyncio.gather(*[t[1] for t in primary_tasks], return_exceptions=True)
            for (api_name, _), result in zip(primary_tasks, results):
                if isinstance(result, Exception):
                    result = SearchProgress(api_name=api_name, display_name=api_name, status="error")
                all_results[api_name] = result
                progress_log.append(self.generate_progress_message(result))
        
        progress_log.append("")
        
        # Phase 3: Secondary APIs (parallel)
        progress_log.append("🔬 PHASE 3: APIs secondaires (Europe PMC, Essais cliniques)")
        progress_log.append("-" * 40)
        
        secondary_apis = [k for k, v in self.API_CONFIG.items() if v.get("type") == "secondary"]
        secondary_tasks = []
        for api_name in secondary_apis:
            if api_name in self.providers:
                secondary_tasks.append((api_name, self.search_single_api(api_name, query)))
        
        if secondary_tasks:
            results = await asyncio.gather(*[t[1] for t in secondary_tasks], return_exceptions=True)
            for (api_name, _), result in zip(secondary_tasks, results):
                if isinstance(result, Exception):
                    result = SearchProgress(api_name=api_name, display_name=api_name, status="error")
                all_results[api_name] = result
                progress_log.append(self.generate_progress_message(result))
        
        progress_log.append("")
        
        # Phase 4: Tertiary APIs (parallel)
        progress_log.append("🌍 PHASE 4: APIs tertiaires (OMS, SNOMED, Orphanet)")
        progress_log.append("-" * 40)
        
        tertiary_apis = [k for k, v in self.API_CONFIG.items() if v.get("type") == "tertiary"]
        tertiary_tasks = []
        for api_name in tertiary_apis:
            if api_name in self.providers:
                tertiary_tasks.append((api_name, self.search_single_api(api_name, query)))
        
        if tertiary_tasks:
            results = await asyncio.gather(*[t[1] for t in tertiary_tasks], return_exceptions=True)
            for (api_name, _), result in zip(tertiary_tasks, results):
                if isinstance(result, Exception):
                    result = SearchProgress(api_name=api_name, display_name=api_name, status="error")
                all_results[api_name] = result
                progress_log.append(self.generate_progress_message(result))
        
        progress_log.append("")
        
        # Phase 5: Premium APIs (specialized - NEW)
        progress_log.append("💎 PHASE 5: APIs Premium (MeSH, Gene, KEGG, OMIM)")
        progress_log.append("-" * 40)
        
        premium_apis = [k for k, v in self.API_CONFIG.items() if v.get("type") == "premium"]
        premium_tasks = []
        for api_name in premium_apis:
            if api_name in self.providers:
                premium_tasks.append((api_name, self.search_single_api(api_name, query)))
        
        if premium_tasks:
            results = await asyncio.gather(*[t[1] for t in premium_tasks], return_exceptions=True)
            for (api_name, _), result in zip(premium_tasks, results):
                if isinstance(result, Exception):
                    result = SearchProgress(api_name=api_name, display_name=api_name, status="error")
                all_results[api_name] = result
                progress_log.append(self.generate_progress_message(result))
        
        progress_log.append("")
        
        # Phase 6: Elite APIs (World's Best - NEW)
        progress_log.append("🏆 PHASE 6: APIs Elite (Semantic Scholar, Reactome, UniProt)")
        progress_log.append("-" * 40)
        
        elite_apis = [k for k, v in self.API_CONFIG.items() if v.get("type") == "elite"]
        elite_tasks = []
        for api_name in elite_apis:
            if api_name in self.providers:
                elite_tasks.append((api_name, self.search_single_api(api_name, query)))
        
        if elite_tasks:
            results = await asyncio.gather(*[t[1] for t in elite_tasks], return_exceptions=True)
            for (api_name, _), result in zip(elite_tasks, results):
                if isinstance(result, Exception):
                    result = SearchProgress(api_name=api_name, display_name=api_name, status="error")
                all_results[api_name] = result
                progress_log.append(self.generate_progress_message(result))
        
        progress_log.append("")
        
        # Summary
        total_time = (time.time() - start_time) * 1000
        apis_searched = list(all_results.keys())
        apis_with_data = [k for k, v in all_results.items() if v.status == "found"]
        
        progress_log.append("=" * 50)
        progress_log.append("📊 RESUME DE LA RECHERCHE")
        progress_log.append("=" * 50)
        progress_log.append(f"⏱️  Temps total: {total_time:.0f}ms ({total_time/1000:.1f}s)")
        progress_log.append(f"🔍 APIs consultees: {len(apis_searched)}")
        progress_log.append(f"✅ APIs avec donnees: {len(apis_with_data)}")
        progress_log.append(f"📈 Taux de succes: {len(apis_with_data)/max(1, len(apis_searched))*100:.0f}%")
        progress_log.append("")
        
        # Build combined data
        combined_data = {}
        for api_name, result in all_results.items():
            if result.status == "found" and result.data:
                combined_data[api_name] = result.data
        
        # Build sources summary
        sources_list = []
        for api_name in apis_with_data:
            config = self.API_CONFIG.get(api_name, {})
            icon = config.get("icon", "📊")
            display = config.get("display", api_name)
            sources_list.append(f"{icon} {display}")
        
        sources_summary = "\n".join(sources_list) if sources_list else "Aucune source avec donnees"
        
        return DeepSearchResult(
            query=query,
            total_time_ms=total_time,
            apis_searched=apis_searched,
            apis_with_data=apis_with_data,
            progress_log=progress_log,
            combined_data=combined_data,
            report_sections={},
            sources_summary=sources_summary,
            quality_score=len(apis_with_data) / max(1, len(apis_searched))
        )
    
    def format_context_for_ai(self, result: DeepSearchResult) -> str:
        """Format the search results as context for AI"""
        context_parts = []
        
        # Progress log header
        context_parts.append("\n".join(result.progress_log))
        
        # Actual data
        context_parts.append("\n" + "=" * 50)
        context_parts.append("📋 DONNEES COLLECTEES")
        context_parts.append("=" * 50 + "\n")
        
        for api_name, data in result.combined_data.items():
            config = self.API_CONFIG.get(api_name, {})
            display = config.get("display", api_name)
            icon = config.get("icon", "📊")
            
            context_parts.append(f"\n{icon} [{display.upper()}]:")
            
            # Format data based on type
            if isinstance(data, dict):
                if data.get("articles"):
                    for i, article in enumerate(data["articles"][:3], 1):
                        title = article.get("title", "N/A")[:100]
                        context_parts.append(f"  {i}. {title}")
                elif data.get("trials"):
                    for i, trial in enumerate(data["trials"][:3], 1):
                        title = trial.get("title", "N/A")[:100]
                        context_parts.append(f"  {i}. {title}")
                elif data.get("name"):
                    context_parts.append(f"  Nom: {data.get('name')}")
                    if data.get("description"):
                        context_parts.append(f"  Description: {data.get('description')[:200]}...")
                    if data.get("symptoms"):
                        context_parts.append(f"  Symptomes: {', '.join(data.get('symptoms', [])[:5])}")
                    if data.get("treatments"):
                        context_parts.append(f"  Traitements: {', '.join(data.get('treatments', [])[:5])}")
                else:
                    # Generic dict formatting
                    for key, value in list(data.items())[:5]:
                        if key not in ["_latency_ms", "_source", "source"]:
                            if isinstance(value, str) and len(value) < 200:
                                context_parts.append(f"  {key}: {value}")
        
        # Source attribution
        context_parts.append("\n" + "=" * 50)
        context_parts.append("📚 SOURCES UTILISEES:")
        context_parts.append("=" * 50)
        context_parts.append(result.sources_summary)
        
        return "\n".join(context_parts)


# Singleton
deep_medical_search = DeepMedicalSearch()


async def perform_deep_search(query: str) -> Tuple[str, DeepSearchResult]:
    """
    Convenience function to perform DEEP search using SmartMedicalRouter.
    
    Uses the MEGA Registry with 77 APIs:
    - Intelligent topic detection
    - Mandatory APIs ALWAYS queried
    - Topic-specific APIs added based on query
    - FORCE ALL MODE: Use all available APIs if possible
    
    Returns (formatted_context, full_result)
    """
    try:
        # Query Expansion for short queries
        search_query = query
        words = query.split()
        if len(words) < 5:
            # Add broad medical terms to ensure wide coverage
            search_query = f"{query} symptoms treatment diagnosis research guidelines clinical trials epidemiology statistics mechanism"
            print(f"[Deep] Expanded query: '{query}' -> '{search_query}'")

        # Try to use SmartMedicalRouter with 77 APIs
        from services.smart_medical_router import SmartMedicalRouter, smart_router
        
        # smart_router singleton is already imported as smart_router usually, 
        # but let's use the instance method on the class if needed or just the global one if accessible.
        # Actually in deep_medical_search.py we import it inside the function.
        # Let's assume we can get the singleton from the module or just instantiate provided one.
        # Oh wait, perform_deep_search import it inside try block.
        
        # We need to access the singleton instance 'smart_router' from the module
        # smart_router.smart_search is the method.
        
        # FORCE ALL APIs = True
        smart_result = await smart_router.smart_search(search_query, force_all=True)
        
        # Update result query to original query for display, or keep expanded?
        # Let's keep original query in the result object for UI
        smart_result.query = query
        
        # Convert to DeepSearchResult format
        result = DeepSearchResult(
            query=smart_result.query,
            total_time_ms=smart_result.total_time_ms,
            apis_searched=smart_result.apis_called,
            apis_with_data=smart_result.apis_with_data,
            progress_log=smart_result.progress_log,
            combined_data=smart_result.data,
            report_sections={},
            sources_summary=smart_result.sources_summary,
            quality_score=len(smart_result.apis_with_data) / max(len(smart_result.apis_called), 1)
        )
        
        # Build enhanced context with source attribution
        context_parts = []
        context_parts.append("=" * 60)
        context_parts.append("🔬 RECHERCHE MEDICALE APPROFONDIE - 77 APIs MONDIALES")
        context_parts.append("=" * 60)
        context_parts.append(f"\n📋 Requête: {query}")
        context_parts.append(f"🎯 Sujets détectés: {', '.join(smart_result.detected_topics)}")
        context_parts.append(f"📊 APIs consultées: {len(smart_result.apis_called)}")
        context_parts.append(f"✅ APIs avec données: {len(smart_result.apis_with_data)}")
        context_parts.append(f"⏱️ Temps total: {smart_result.total_time_ms:.0f}ms")
        context_parts.append("")
        context_parts.append("📚 SOURCES DE DONNÉES:")
        context_parts.append("-" * 40)
        context_parts.append(f"⭐ Obligatoires: {', '.join(smart_result.mandatory_apis)}")
        context_parts.append(f"🔍 Spécifiques: {', '.join(smart_result.topic_specific_apis)}")
        context_parts.append("")
        
        # Add data from each source
        # Add data from each source with RICH formatting
        context_parts.append("\n📚 DONNÉES DÉTAILLÉES PAR SOURCE:")
        
        # Sort APIs: Priority ones first
        priority_order = ["openfda", "pubmed", "rxnorm", "disease_sh", "who_gho", "open_disease"]
        sorted_apis = sorted(smart_result.data.keys(), key=lambda x: priority_order.index(x) if x in priority_order else 999)
        
        for api_id in sorted_apis:
            data = smart_result.data[api_id]
            # Check for validity
            if not isinstance(data, dict): continue
            has_content = data.get("found") or data.get("count", 0) > 0 or data.get("total", 0) > 0 or data.get("articles") or data.get("drugs")
            if not has_content: continue

            context_parts.append(f"\n📌 [{api_id.upper()}]")
            
            # --- Specific Formatting ---
            if api_id == "openfda":
                drugs = data.get("drugs", [])
                if not drugs and "results" in data: drugs = data["results"]
                
                context_parts.append(f"  ℹ️ Base de données FDA des médicaments approuvés.")
                for i, drug in enumerate(drugs[:10], 1): # Extended to 10
                    brand = "N/A"
                    generic = "N/A"
                    if isinstance(drug, dict):
                         # Try flattened or nested
                         brand_raw = drug.get("brand_name")
                         if not brand_raw and "openfda" in drug: brand_raw = drug["openfda"].get("brand_name")
                         if isinstance(brand_raw, list): brand = brand_raw[0]
                         else: brand = str(brand_raw) if brand_raw else "N/A"
                         
                         gen_raw = drug.get("generic_name")
                         if not gen_raw and "openfda" in drug: gen_raw = drug["openfda"].get("generic_name")
                         if isinstance(gen_raw, list): generic = gen_raw[0]
                         else: generic = str(gen_raw) if gen_raw else "N/A"
                         
                         context_parts.append(f"  {i}. {brand} ({generic})")
                         # Indications
                         ind = drug.get("indications_and_usage")
                         if ind:
                             if isinstance(ind, list): ind = ind[0]
                             ind_str = str(ind)[:400].replace("\n", " ")
                             context_parts.append(f"     Info: {ind_str}...")
                         
                         # Warnings (Boxed Warning)
                         warn = drug.get("boxed_warning")
                         if warn:
                             if isinstance(warn, list): warn = warn[0]
                             context_parts.append(f"     ⚠️ AVERTISSEMENT: {str(warn)[:300]}...")
            
            elif api_id == "pubmed":
                articles = data.get("articles", [])
                context_parts.append(f"  ℹ️ Littérature biomédicale (NCBI/NLM).")
                for i, art in enumerate(articles[:8], 1): # Extended to 8
                    title = art.get("title", "Sans titre")
                    date = art.get("pubdate", "Date inconnue")
                    context_parts.append(f"  {i}. {title} ({date})")
                    if art.get("abstract"):
                         abs_text = str(art['abstract'])
                         if len(abs_text) > 400: abs_text = abs_text[:400] + "..."
                         context_parts.append(f"     Abstract: {abs_text}")
                    # Add authors if available
                    if art.get("authors"):
                        authors = art.get("authors")
                        if isinstance(authors, list):
                            context_parts.append(f"     Auteurs: {', '.join(authors[:3])} et al.")


            elif api_id == "disease_sh":
                for k, v in data.items():
                    if k in ["cases", "deaths", "recovered", "active"]:
                        context_parts.append(f"  {k}: {v}")
                if not any(k in data for k in ["cases", "deaths"]):
                     context_parts.append(f"  Data: {str(data)[:300]}")

            else:
                # Generic clean format
                items_shown = 0
                for k, v in data.items():
                    if k in ["_latency_ms", "_source", "source", "found", "count", "total", "success"]: continue
                    if items_shown >= 6: break # Max 6 fields
                    
                    if isinstance(v, (str, int, float, bool)):
                        v_str = str(v)
                        if len(v_str) > 300: v_str = v_str[:300] + "..."
                        context_parts.append(f"  {k}: {v_str}")
                        items_shown += 1
                    elif isinstance(v, list):
                        list_str = ', '.join(map(str, v[:3]))
                        if list_str:
                            context_parts.append(f"  {k}: {list_str}")
                            items_shown += 1
        
        context_parts.append("\n" + "=" * 60)
        context_parts.append(smart_result.sources_summary)
        
        context = "\n".join(context_parts)
        
        # CHECK WORD COUNT (Target: 1000 words)
        words = len(context.split())
        if words < 1000:
            context_parts.append("\n" + "=" * 60)
            context_parts.append(f"📦 ANNEXE TECHNIQUE ET DONNÉES BRUTES (Extension {words} -> 1000 mots)")
            context_parts.append("=" * 60)
            
            # Add verbose data from other APIs to reach word count
            # We iterate over all valid data
            for api_id, data in smart_result.data.items():
                if isinstance(data, dict) and (data.get("found") or data.get("count", 0) > 0 or data.get("articles")):
                    # Skip if already heavily featured (optional, but raw data is always good padding)
                    context_parts.append(f"\n📄 DONNÉES BRUTES [{api_id.upper()}]:")
                    # Pretty print the dict somewhat
                    import json
                    try:
                        # Convert to string with indentation but limit length per source
                        dump = json.dumps(data, default=str, indent=2)
                        context_parts.append(dump[:3000]) 
                    except:
                        context_parts.append(str(data)[:3000])
        
        context = "\n".join(context_parts)
        return context, result
        
    except Exception as e:
        # Fallback to original DeepMedicalSearch
        print(f"[WARN] SmartMedicalRouter failed, falling back: {e}")
        result = await deep_medical_search.deep_search(query)
        context = deep_medical_search.format_context_for_ai(result)
        return context, result
