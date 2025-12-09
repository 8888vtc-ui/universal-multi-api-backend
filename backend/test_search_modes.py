"""Test Medical Search Modes - Fast vs Standard vs Deep"""
import asyncio
from services.medical_search_engine import (
    fast_medical_search, 
    standard_medical_search, 
    deep_medical_search,
    get_api_summary
)

async def test_search_modes():
    print("=" * 70)
    print("TESTING MEDICAL SEARCH MODES - Comparison")
    print("=" * 70)
    
    query = "diabetes"
    
    # Show API summary
    summary = get_api_summary()
    print(f"\n📊 APIs DISPONIBLES: {summary['total_apis']} total")
    print(f"   Local ({summary['local']['latency']}): {', '.join(summary['local']['apis'])}")
    print(f"   Primary ({summary['primary']['latency']}): {', '.join(summary['primary']['apis'])}")
    print(f"   Secondary ({summary['secondary']['latency']}): {', '.join(summary['secondary']['apis'])}")
    print(f"   Tertiary ({summary['tertiary']['latency']}): {', '.join(summary['tertiary']['apis'])}")
    
    # Test FAST mode
    print("\n\n" + "=" * 70)
    print("1. MODE RAPIDE (FAST) - Local only")
    print("=" * 70)
    
    fast_result = await fast_medical_search(query, "disease")
    
    print(f"\n   ⏱️  Temps: {fast_result['timing']['total_ms']}ms")
    print(f"   📊 APIs appelées: {fast_result['apis_called']}")
    print(f"   ✅ APIs success: {fast_result['apis_successful']}")
    print(f"   📋 Sources: {', '.join(fast_result['summary']['sources_list'])}")
    
    if fast_result['combined_data'].get('disease_info'):
        print(f"   🔬 Maladie trouvée: {fast_result['combined_data']['disease_info'].get('name', 'N/A')}")
    
    # Test STANDARD mode
    print("\n\n" + "=" * 70)
    print("2. MODE STANDARD - Local + Main APIs")
    print("=" * 70)
    
    standard_result = await standard_medical_search(query, "disease")
    
    print(f"\n   ⏱️  Temps: {standard_result['timing']['total_ms']}ms")
    print(f"   📊 APIs appelées: {standard_result['apis_called']}")
    print(f"   ✅ APIs success: {standard_result['apis_successful']}")
    print(f"   📋 Sources: {', '.join(standard_result['summary']['sources_list'])}")
    
    if standard_result['combined_data'].get('research_articles'):
        print(f"   📚 Articles PubMed: {len(standard_result['combined_data']['research_articles'])}")
    
    # Test DEEP mode
    print("\n\n" + "=" * 70)
    print("3. MODE APPROFONDI (DEEP) - All 13+ APIs")
    print("=" * 70)
    
    deep_result = await deep_medical_search(query, "disease")
    
    print(f"\n   ⏱️  Temps: {deep_result['timing']['total_ms']}ms")
    print(f"   📊 APIs appelées: {deep_result['apis_called']}")
    print(f"   ✅ APIs success: {deep_result['apis_successful']}")
    print(f"   📋 Sources: {', '.join(deep_result['summary']['sources_list'])}")
    
    if deep_result['combined_data'].get('clinical_trials'):
        print(f"   🧪 Essais cliniques: {len(deep_result['combined_data']['clinical_trials'])}")
    
    # Summary comparison
    print("\n\n" + "=" * 70)
    print("📊 COMPARAISON DES MODES")
    print("=" * 70)
    
    print(f"""
    ┌─────────────────┬────────────────┬────────────────┬────────────────┐
    │     Mode        │     FAST       │    STANDARD    │     DEEP       │
    ├─────────────────┼────────────────┼────────────────┼────────────────┤
    │ Temps           │ {fast_result['timing']['total_ms']:>10}ms  │ {standard_result['timing']['total_ms']:>10}ms  │ {deep_result['timing']['total_ms']:>10}ms  │
    │ APIs appelées   │ {fast_result['apis_called']:>10}     │ {standard_result['apis_called']:>10}     │ {deep_result['apis_called']:>10}     │
    │ APIs success    │ {fast_result['apis_successful']:>10}     │ {standard_result['apis_successful']:>10}     │ {deep_result['apis_successful']:>10}     │
    │ Qualité data    │ {fast_result['summary']['data_quality']:>10}     │ {standard_result['summary']['data_quality']:>10}     │ {deep_result['summary']['data_quality']:>10}     │
    └─────────────────┴────────────────┴────────────────┴────────────────┘
    """)
    
    print("""
    💡 RECOMMANDATIONS:
    ├─ FAST     → Chat temps réel, réponses instantanées
    ├─ STANDARD → Requêtes normales, bon équilibre
    └─ DEEP     → Recherche approfondie, génération de rapports
    """)

if __name__ == "__main__":
    asyncio.run(test_search_modes())
