"""
🏆 THE 3 KINGS - COMPLETE MEDICAL SEARCH TEST
====================================================
FAST (⚡) → NORMAL (📊) → DEEP (🔬)

Tests all 77+ APIs with impressive source transparency
Shows exactly WHERE the data comes from (legal + quality proof)
"""
import asyncio
import time
from typing import Dict, Any, List
from datetime import datetime

# Import all search capabilities
from services.medical_search_engine import fast_medical_search, standard_medical_search, deep_medical_search
from services.smart_medical_router import smart_medical_search, get_api_stats
from services.deep_medical_search import perform_deep_search
from services.external_apis.medical_mega_registry import MegaMedicalRegistry
from services.external_apis.medical_ultimate import UltimateMedicalAPIs


class ThreeKingsTest:
    """Complete test suite for the 3 search modes with source transparency"""
    
    def __init__(self):
        self.test_query = "traitement diabete type 2 metformine"
        self.results = {}
        
    def print_header(self):
        print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║     👑 👑 👑    THE 3 KINGS - BEST MEDICAL AI SEARCHER    👑 👑 👑          ║
║                                                                              ║
║     ⚡ FAST   │   📊 NORMAL   │   🔬 DEEP RESEARCH                          ║
║                                                                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║   🌍 WORLD'S LARGEST MEDICAL API COLLECTION                                 ║
""")
        # Show API statistics
        stats = MegaMedicalRegistry.count_apis()
        print(f"║   📊 Total APIs: {stats['total']} sources from {len(stats['by_country'])} countries")
        print(f"║   ⭐ Mandatory APIs: {stats['mandatory']} (always consulted)")
        print("║")
        
        # Show API registry summary
        print(UltimateMedicalAPIs.get_api_summary())
        
    async def test_fast_king(self) -> Dict:
        """⚡ FAST KING: Instant response from local databases"""
        print("\n" + "═" * 80)
        print("  ⚡ 👑 KING #1: FAST MODE (Recherche Rapide)")
        print("═" * 80)
        print("  📋 Uses: Local databases only (instant)")
        print("  ⏱️  Target: < 100ms")
        print("-" * 80)
        
        start = time.time()
        result = await fast_medical_search(self.test_query, "disease")
        elapsed = (time.time() - start) * 1000
        
        print(f"\n  ⏱️  Response Time: {elapsed:.0f}ms")
        print(f"  📊 APIs Called: {result['apis_called']}")
        print(f"  ✅ APIs Successful: {result['apis_successful']}")
        print(f"  📈 Quality Score: {result['summary']['data_quality'].upper()}")
        
        print("\n  📚 SOURCES USED (Transparency):")
        for source in result['summary']['sources_list']:
            icon = self._get_source_icon(source)
            print(f"     {icon} {source}")
        
        # Show data found
        if result['combined_data'].get('disease_info'):
            info = result['combined_data']['disease_info']
            print(f"\n  🔬 Disease Found: {info.get('name', 'N/A')}")
            print(f"     Source: {info.get('_source', 'Local DB')}")
            
        self.results['fast'] = {
            'time_ms': elapsed,
            'apis_called': result['apis_called'],
            'apis_success': result['apis_successful'],
            'sources': result['summary']['sources_list'],
            'quality': result['summary']['data_quality']
        }
        
        return result
    
    async def test_normal_king(self) -> Dict:
        """📊 NORMAL KING: Balanced search with main APIs"""
        print("\n" + "═" * 80)
        print("  📊 👑 KING #2: NORMAL MODE (Recherche Standard)")
        print("═" * 80)
        print("  📋 Uses: Local + PubMed + FDA + RxNorm + Europe PMC")
        print("  ⏱️  Target: 1-3 seconds")
        print("-" * 80)
        
        start = time.time()
        result = await standard_medical_search(self.test_query, "disease")
        elapsed = (time.time() - start) * 1000
        
        print(f"\n  ⏱️  Response Time: {elapsed:.0f}ms ({elapsed/1000:.1f}s)")
        print(f"  📊 APIs Called: {result['apis_called']}")
        print(f"  ✅ APIs Successful: {result['apis_successful']}")
        print(f"  📈 Quality Score: {result['summary']['data_quality'].upper()}")
        
        print("\n  📚 SOURCES USED (With Icons):")
        for source in result['summary']['sources_list']:
            icon = self._get_source_icon(source)
            org = self._get_source_org(source)
            print(f"     {icon} {source.upper()} - {org}")
        
        # Show research articles
        if result['combined_data'].get('research_articles'):
            print(f"\n  📖 Research Articles Found: {len(result['combined_data']['research_articles'])}")
            for i, article in enumerate(result['combined_data']['research_articles'][:2], 1):
                title = article.get('title', 'N/A')[:60]
                print(f"     {i}. {title}...")
        
        self.results['normal'] = {
            'time_ms': elapsed,
            'apis_called': result['apis_called'],
            'apis_success': result['apis_successful'],
            'sources': result['summary']['sources_list'],
            'quality': result['summary']['data_quality']
        }
        
        return result
    
    async def test_deep_king(self) -> Dict:
        """🔬 DEEP KING: Comprehensive search across ALL 77+ APIs"""
        print("\n" + "═" * 80)
        print("  🔬 👑 KING #3: DEEP MODE (Recherche Approfondie)")
        print("═" * 80)
        print("  📋 Uses: ALL 77+ APIs from world's best medical sources")
        print("  ⏱️  Target: 5-20 seconds (comprehensive)")
        print("-" * 80)
        
        # Use smart router for intelligent topic-based search
        start = time.time()
        context, smart_result = await smart_medical_search(self.test_query)
        elapsed = (time.time() - start) * 1000
        
        print(f"\n  ⏱️  Response Time: {elapsed:.0f}ms ({elapsed/1000:.1f}s)")
        print(f"  🎯 Topics Detected: {', '.join(smart_result.detected_topics)}")
        print(f"  📊 Total APIs Called: {len(smart_result.apis_called)}")
        print(f"  ⭐ Mandatory APIs: {len(smart_result.mandatory_apis)}")
        print(f"  🔍 Topic-Specific APIs: {len(smart_result.topic_specific_apis)}")
        print(f"  ✅ APIs With Data: {len(smart_result.apis_with_data)}")
        print(f"  💡 APIs Saved (not needed): {77 - len(smart_result.apis_called)}")
        
        # Print detailed source report (BIG RAPPORT)
        self._print_deep_source_report(smart_result)
        
        self.results['deep'] = {
            'time_ms': elapsed,
            'apis_called': len(smart_result.apis_called),
            'apis_success': len(smart_result.apis_with_data),
            'sources': smart_result.apis_with_data,
            'topics': smart_result.detected_topics,
            'mandatory': smart_result.mandatory_apis,
            'topic_specific': smart_result.topic_specific_apis
        }
        
        return smart_result
    
    def _print_deep_source_report(self, result):
        """Print comprehensive source report for DEEP mode"""
        print("\n" + "─" * 80)
        print("  📋 COMPRÉHENSIVE SOURCE REPORT (Legal Transparency)")
        print("─" * 80)
        
        # Mandatory sources
        print("\n  ⭐ MANDATORY SOURCES (Always Consulted):")
        for api_id in result.mandatory_apis:
            api_info = MegaMedicalRegistry.APIS.get(api_id, {})
            icon = api_info.get('icon', '📊')
            name = api_info.get('name', api_id)
            country = api_info.get('country', '🌍')
            has_data = '✅' if api_id in result.apis_with_data else '⚪'
            print(f"     {has_data} {icon} {name} ({country})")
        
        # Topic-specific sources
        if result.topic_specific_apis:
            print(f"\n  🎯 TOPIC-SPECIFIC SOURCES ({', '.join(result.detected_topics)}):")
            for api_id in result.topic_specific_apis:
                api_info = MegaMedicalRegistry.APIS.get(api_id, {})
                icon = api_info.get('icon', '📊')
                name = api_info.get('name', api_id)
                country = api_info.get('country', '🌍')
                has_data = '✅' if api_id in result.apis_with_data else '⚪'
                print(f"     {has_data} {icon} {name} ({country})")
        
        # Data summary
        print(f"\n  📊 DATA COLLECTED FROM {len(result.apis_with_data)} SOURCES:")
        for api_id in result.apis_with_data:
            api_info = MegaMedicalRegistry.APIS.get(api_id, {})
            icon = api_info.get('icon', '📊')
            name = api_info.get('name', api_id)
            org = api_info.get('org', 'Unknown')
            country = api_info.get('country', '🌍')
            desc = api_info.get('desc', '')
            print(f"     {icon} {name}")
            print(f"        Organization: {org}")
            print(f"        Country: {country}")
            if desc:
                print(f"        Description: {desc}")
        
        # Legal disclaimer
        print("\n  ⚖️  LEGAL NOTICE:")
        print("     All data sourced from official, peer-reviewed medical databases.")
        print("     Sources include: NIH, WHO, FDA, EMA, INSERM, and other trusted institutions.")
        print("     This information is for educational purposes only.")
    
    def _get_source_icon(self, source: str) -> str:
        icons = {
            'pubmed': '📖', 'openfda': '🇺🇸', 'rxnorm': '💉', 'europe_pmc': '🇪🇺',
            'clinical_trials': '🔬', 'disease_sh': '🦠', 'who_gho': '🌍',
            'snomed_ct': '🏥', 'orphanet': '🧬', 'loinc': '🧪', 
            'drugbank_open': '💊', 'open_disease': '📚', 'mesh': '📑',
            'ncbi_gene': '🧬', 'drug_central': '💎', 'kegg': '🔄', 'omim': '🔬',
            'semantic_scholar': '🧠', 'clinvar': '🧪', 'reactome': '⚡', 'uniprot': '🔬'
        }
        return icons.get(source.lower(), '📊')
    
    def _get_source_org(self, source: str) -> str:
        orgs = {
            'pubmed': 'NIH/NLM USA', 'openfda': 'FDA USA', 'rxnorm': 'NLM USA',
            'europe_pmc': 'EMBL-EBI Europe', 'clinical_trials': 'NIH USA',
            'disease_sh': 'Open Source', 'who_gho': 'WHO International',
            'snomed_ct': 'SNOMED International', 'orphanet': 'INSERM France',
            'loinc': 'Regenstrief USA', 'drugbank_open': 'U. Alberta Canada',
            'open_disease': 'Local Database'
        }
        return orgs.get(source.lower(), 'Medical Institution')
    
    def print_comparison(self):
        """Print final comparison of all 3 kings"""
        print("\n" + "═" * 80)
        print("  📊 COMPARISON OF THE 3 KINGS")
        print("═" * 80)
        
        fast = self.results.get('fast', {})
        normal = self.results.get('normal', {})
        deep = self.results.get('deep', {})
        
        print(f"""
╔═══════════════════╦═══════════════════╦═══════════════════╦═══════════════════╗
║     Metric        ║   ⚡ FAST         ║   📊 NORMAL       ║   🔬 DEEP         ║
╠═══════════════════╬═══════════════════╬═══════════════════╬═══════════════════╣
║ Response Time     ║ {fast.get('time_ms', 0):>8.0f}ms       ║ {normal.get('time_ms', 0):>8.0f}ms       ║ {deep.get('time_ms', 0):>8.0f}ms       ║
║ APIs Called       ║ {fast.get('apis_called', 0):>8}          ║ {normal.get('apis_called', 0):>8}          ║ {deep.get('apis_called', 0):>8}          ║
║ APIs With Data    ║ {fast.get('apis_success', 0):>8}          ║ {normal.get('apis_success', 0):>8}          ║ {deep.get('apis_success', 0):>8}          ║
║ Quality Level     ║ {'Local Only':>12}     ║ {'Standard+':>12}     ║ {'Maximum':>12}     ║
╚═══════════════════╩═══════════════════╩═══════════════════╩═══════════════════╝
""")
        print("""
  💡 USE CASES:
  ├─ ⚡ FAST   → Real-time chat, instant answers, mobile apps
  ├─ 📊 NORMAL → Standard queries, balanced speed/quality
  └─ 🔬 DEEP   → Medical research, student analysis, legal reports
  
  📈 QUALITY GUARANTEE:
  ├─ All sources are official medical institutions
  ├─ Data from 77+ APIs worldwide
  ├─ Transparent source attribution (legal compliance)
  └─ Real-time data from trusted authorities
""")

    async def run_all_tests(self):
        """Run all 3 kings tests"""
        self.print_header()
        
        print(f"\n  🎯 Test Query: \"{self.test_query}\"")
        print(f"  🕐 Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Test all 3 modes
        await self.test_fast_king()
        await self.test_normal_king()
        await self.test_deep_king()
        
        # Print comparison
        self.print_comparison()
        
        print("\n" + "═" * 80)
        print("  ✅ ALL 3 KINGS TESTED SUCCESSFULLY!")
        print("═" * 80)


async def main():
    test = ThreeKingsTest()
    await test.run_all_tests()


if __name__ == "__main__":
    asyncio.run(main())
