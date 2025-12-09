"""
Performance Test - Complete System Speed Analysis
Tests all components: Memory, APIs, AI routing
"""
import asyncio
import time
from typing import Dict, Any

# Test configuration
TEST_QUERIES = [
    ("health", "Quels sont les symptômes du diabète ?", "disease"),
    ("finance", "Prix du Bitcoin ?", "crypto"),
    ("general", "Qui est Albert Einstein ?", "general"),
]


async def test_memory_performance():
    """Test memory system performance"""
    print("\n" + "=" * 60)
    print("1. TEST MÉMOIRE V2")
    print("=" * 60)
    
    from services.enhanced_memory import enhanced_memory
    
    session_id = f"perf_test_{int(time.time())}"
    expert_id = "health"
    
    # Test 1: Add message speed
    start = time.time()
    for i in range(10):
        enhanced_memory.add_message(
            session_id=session_id,
            expert_id=expert_id,
            role="user" if i % 2 == 0 else "assistant",
            message=f"Test message {i} - Lorem ipsum dolor sit amet"
        )
    add_time = (time.time() - start) * 1000
    print(f"   ├─ Ajouter 10 messages: {add_time:.1f}ms ({add_time/10:.1f}ms/msg)")
    
    # Test 2: Build context speed
    start = time.time()
    context = enhanced_memory.build_smart_context(session_id, expert_id)
    context_time = (time.time() - start) * 1000
    print(f"   ├─ Build smart context: {context_time:.1f}ms")
    print(f"   ├─ Context length: {len(context)} chars")
    
    # Test 3: Profile retrieval
    start = time.time()
    profile = enhanced_memory.get_or_create_profile(session_id)
    profile_time = (time.time() - start) * 1000
    print(f"   ├─ Get profile: {profile_time:.1f}ms")
    
    # Test 4: Topics retrieval
    start = time.time()
    topics = enhanced_memory.get_topics_discussed(session_id, expert_id)
    topics_time = (time.time() - start) * 1000
    print(f"   └─ Get topics: {topics_time:.1f}ms ({len(topics)} topics)")
    
    total = add_time + context_time + profile_time + topics_time
    print(f"\n   📊 TOTAL MÉMOIRE: {total:.1f}ms")
    
    return total


async def test_medical_search_performance():
    """Test medical search modes"""
    print("\n" + "=" * 60)
    print("2. TEST RECHERCHE MÉDICALE (3 MODES)")
    print("=" * 60)
    
    from services.medical_search_engine import (
        fast_medical_search,
        standard_medical_search,
        deep_medical_search
    )
    
    query = "diabetes"
    results = {}
    
    # FAST mode
    start = time.time()
    fast_result = await fast_medical_search(query, "disease")
    fast_time = (time.time() - start) * 1000
    results["fast"] = fast_time
    print(f"   ├─ FAST mode: {fast_time:.0f}ms ({fast_result['apis_successful']}/{fast_result['apis_called']} APIs)")
    
    # STANDARD mode
    start = time.time()
    std_result = await standard_medical_search(query, "disease")
    std_time = (time.time() - start) * 1000
    results["standard"] = std_time
    print(f"   ├─ STANDARD mode: {std_time:.0f}ms ({std_result['apis_successful']}/{std_result['apis_called']} APIs)")
    
    # DEEP mode
    start = time.time()
    deep_result = await deep_medical_search(query, "disease")
    deep_time = (time.time() - start) * 1000
    results["deep"] = deep_time
    print(f"   └─ DEEP mode: {deep_time:.0f}ms ({deep_result['apis_successful']}/{deep_result['apis_called']} APIs)")
    
    print(f"\n   📊 Ratio FAST/DEEP: {fast_time/deep_time:.1%}")
    
    return results


async def test_ai_router_performance():
    """Test AI router response time"""
    print("\n" + "=" * 60)
    print("3. TEST AI ROUTER")
    print("=" * 60)
    
    try:
        from services.ai_router import ai_router
        
        # Simple prompt test
        start = time.time()
        result = await ai_router.route(
            prompt="Dis juste 'OK' pour tester.",
            system_prompt="Tu es un assistant. Réponds en un mot."
        )
        ai_time = (time.time() - start) * 1000
        
        print(f"   ├─ Provider: {result['source']}")
        print(f"   ├─ Response time: {ai_time:.0f}ms")
        print(f"   └─ Response length: {len(result['response'])} chars")
        
        return ai_time
    except Exception as e:
        print(f"   └─ [ERROR] AI Router: {e}")
        return 0


async def test_full_pipeline():
    """Test complete expert chat pipeline (without actual AI call)"""
    print("\n" + "=" * 60)
    print("4. TEST PIPELINE COMPLET (sans LLM)")
    print("=" * 60)
    
    from services.enhanced_memory import enhanced_memory
    from services.expert_config import get_expert
    
    session_id = f"pipeline_test_{int(time.time())}"
    expert_id = "health"
    message = "Je suis étudiant en médecine. Quels sont les symptômes du diabète de type 2 ?"
    
    timings = {}
    
    # Step 1: Memory operations
    start = time.time()
    enhanced_memory.add_message(session_id, expert_id, "user", message)
    memory_context = enhanced_memory.build_smart_context(session_id, expert_id)
    timings["memory"] = (time.time() - start) * 1000
    
    # Step 2: Get expert config
    start = time.time()
    expert = get_expert(expert_id)
    timings["config"] = (time.time() - start) * 1000
    
    # Step 3: Medical search (FAST mode)
    start = time.time()
    try:
        from services.medical_search_engine import fast_medical_search
        search_result = await fast_medical_search("diabetes", "disease")
        timings["search"] = (time.time() - start) * 1000
    except:
        timings["search"] = 0
    
    # Step 4: Build prompt
    start = time.time()
    system_prompt = expert.system_prompt.replace("{context}", memory_context)
    timings["prompt"] = (time.time() - start) * 1000
    
    print(f"   ├─ Memory operations: {timings['memory']:.1f}ms")
    print(f"   ├─ Get Expert config: {timings['config']:.1f}ms")
    print(f"   ├─ Medical search (FAST): {timings['search']:.0f}ms")
    print(f"   ├─ Build prompt: {timings['prompt']:.1f}ms")
    
    total = sum(timings.values())
    print(f"   └─ TOTAL (sans LLM): {total:.0f}ms")
    
    # Check user profile detection
    profile = enhanced_memory.get_or_create_profile(session_id)
    if profile.get("user_type"):
        print(f"\n   ✅ Profil détecté: {profile['user_type']}")
    
    return timings


async def main():
    print("\n" + "=" * 70)
    print("🚀 PERFORMANCE TEST - SYSTÈME COMPLET")
    print("=" * 70)
    
    all_results = {}
    
    # Test 1: Memory
    try:
        all_results["memory_total"] = await test_memory_performance()
    except Exception as e:
        print(f"   [ERROR] Memory test: {e}")
        all_results["memory_total"] = 0
    
    # Test 2: Medical Search
    try:
        all_results["search"] = await test_medical_search_performance()
    except Exception as e:
        print(f"   [ERROR] Search test: {e}")
        all_results["search"] = {}
    
    # Test 3: AI Router (optional - needs API key)
    try:
        all_results["ai_router"] = await test_ai_router_performance()
    except Exception as e:
        print(f"   [SKIP] AI Router: {e}")
        all_results["ai_router"] = 0
    
    # Test 4: Full Pipeline
    try:
        all_results["pipeline"] = await test_full_pipeline()
    except Exception as e:
        print(f"   [ERROR] Pipeline test: {e}")
        all_results["pipeline"] = {}
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 RÉSUMÉ DES PERFORMANCES")
    print("=" * 70)
    
    pipeline = all_results.get("pipeline", {})
    search = all_results.get("search", {})
    
    print(f"""
    ┌──────────────────────────────┬────────────────┐
    │ Composant                    │ Temps          │
    ├──────────────────────────────┼────────────────┤
    │ Mémoire V2 (total)           │ {all_results.get('memory_total', 0):>10.0f}ms  │
    │ Recherche FAST               │ {search.get('fast', 0):>10.0f}ms  │
    │ Recherche STANDARD           │ {search.get('standard', 0):>10.0f}ms  │
    │ Recherche DEEP               │ {search.get('deep', 0):>10.0f}ms  │
    │ AI Router (1 call)           │ {all_results.get('ai_router', 0):>10.0f}ms  │
    │ Pipeline (sans LLM)          │ {sum(pipeline.values()) if pipeline else 0:>10.0f}ms  │
    └──────────────────────────────┴────────────────┘
    """)
    
    # Recommendations
    print("💡 OPTIMISATIONS RECOMMANDÉES:")
    if search.get('fast', 0) < 100:
        print("   ✅ Mode FAST optimal pour chat temps réel")
    if all_results.get('memory_total', 0) < 100:
        print("   ✅ Mémoire V2 très rapide")
    if all_results.get('ai_router', 0) > 2000:
        print("   ⚠️  LLM est le goulot - considérer streaming")
    
    print("\n   📈 Temps estimé total par requête:")
    estimated_fast = sum(pipeline.values()) + search.get('fast', 0) + all_results.get('ai_router', 1000)
    estimated_deep = sum(pipeline.values()) + search.get('deep', 0) + all_results.get('ai_router', 1000)
    print(f"      FAST mode: ~{estimated_fast:.0f}ms")
    print(f"      DEEP mode: ~{estimated_deep:.0f}ms")


if __name__ == "__main__":
    asyncio.run(main())
