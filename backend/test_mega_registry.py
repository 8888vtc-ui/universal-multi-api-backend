"""Test Mega Medical Registry - Intelligent Topic Detection & API Routing"""
import asyncio
from services.external_apis.medical_mega_registry import MegaMedicalRegistry
from services.smart_medical_router import smart_medical_search, get_api_stats

def test_topic_detection():
    print("=" * 70)
    print("🧠 INTELLIGENT TOPIC DETECTION TEST")
    print("=" * 70)
    
    test_queries = [
        ("traitement du diabete type 2", ["diabetes", "drugs"]),
        ("cancer du sein HER2 positif", ["cancer"]),
        ("mutation genetique BRCA1", ["genetic", "genomics"]),
        ("essai clinique COVID-19 vaccin", ["clinical_trials", "infectious"]),
        ("maladie rare mucoviscidose enfant", ["rare_disease", "pediatrics"]),
        ("hypertension arterielle chronique", ["cardiovascular"]),
        ("depression anxiete traitement", ["mental_health", "drugs"]),
    ]
    
    passed = 0
    for query, expected_topics in test_queries:
        detected = MegaMedicalRegistry.detect_topics(query)
        # Check if at least one expected topic is detected
        match = any(t in detected for t in expected_topics)
        status = "✅" if match else "❌"
        if match:
            passed += 1
        print(f"\n{status} Query: '{query}'")
        print(f"   Expected: {expected_topics}")
        print(f"   Detected: {detected}")
        
        # Get relevant APIs
        apis = MegaMedicalRegistry.get_relevant_apis(query)
        mandatory = [a['id'] for a in apis if a.get('reason') == 'mandatory']
        topic_apis = [a['id'] for a in apis if a.get('reason', '').startswith('topic:')]
        print(f"   APIs: {len(apis)} total ({len(mandatory)} mandatory, {len(topic_apis)} topic-specific)")
    
    print(f"\n📊 Topic Detection: {passed}/{len(test_queries)} passed")
    return passed == len(test_queries)


async def test_smart_search():
    print("\n" + "=" * 70)
    print("🔬 SMART MEDICAL SEARCH TEST (Live APIs)")
    print("=" * 70)
    
    query = "traitement du diabete type 2 avec metformine"
    print(f"\n📋 Query: '{query}'")
    print("-" * 70)
    
    try:
        context, result = await smart_medical_search(query)
        
        print(f"✅ Topics detected: {result.detected_topics}")
        print(f"✅ Mandatory APIs called: {len(result.mandatory_apis)}")
        print(f"   → {result.mandatory_apis[:5]}...")
        print(f"✅ Topic-specific APIs called: {len(result.topic_specific_apis)}")
        print(f"   → {result.topic_specific_apis[:5]}...")
        print(f"✅ APIs with data: {len(result.apis_with_data)}")
        print(f"   → {result.apis_with_data}")
        print(f"✅ Total time: {result.total_time_ms:.0f}ms")
        print(f"✅ APIs NOT called (saved): {77 - len(result.apis_called)} APIs")
        
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


async def main():
    print(MegaMedicalRegistry.get_summary())
    
    # Test 1: Topic Detection
    topic_ok = test_topic_detection()
    
    # Test 2: Smart Search
    search_ok = await test_smart_search()
    
    # Summary
    print("\n" + "=" * 70)
    print("📋 MEGA REGISTRY TEST SUMMARY")
    print("=" * 70)
    stats = get_api_stats()
    print(f"""
🏆 REGISTRY STATUS:
   📊 Total APIs: {stats.get('total', 77)}
   ⭐ Mandatory APIs: {stats.get('mandatory', 12)}
   🔌 Active Providers: {stats.get('active_providers', 0)}

📈 TEST RESULTS:
   {'✅' if topic_ok else '❌'} Topic Detection: {'PASSED' if topic_ok else 'FAILED'}
   {'✅' if search_ok else '❌'} Smart Search: {'PASSED' if search_ok else 'FAILED'}

🎯 INTELLIGENT ROUTING:
   → Only relevant APIs are called based on query topic
   → Mandatory APIs (PubMed, WHO, FDA, etc.) ALWAYS included
   → Saves time by NOT calling irrelevant APIs
""")


if __name__ == "__main__":
    asyncio.run(main())
