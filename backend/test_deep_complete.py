"""
Test DEEP Mode Medical Search - COMPLETE
Tests APIs, quality, content, duration
"""
import asyncio
import httpx
import time
import json
from datetime import datetime

# Configuration
API_URL = "https://universal-api-hub.fly.dev/api/expert/health/chat"
SMART_ROUTER_TEST_URL = "https://universal-api-hub.fly.dev/api/health"
TIMEOUT = 120

# Test questions
DEEP_TEST_QUESTIONS = [
    "Quels sont les traitements du diabète de type 2 et leurs effets secondaires?",
]


async def test_smart_router_apis(question: str) -> dict:
    """Test SmartMedicalRouter directly to see API stats"""
    print("\n" + "=" * 60)
    print("🔬 TEST SmartMedicalRouter - APIs INTERROGÉES")
    print("=" * 60)
    
    try:
        async with httpx.AsyncClient(timeout=60) as client:
            # Test the health endpoint with search
            response = await client.get(
                f"{SMART_ROUTER_TEST_URL}?q={question[:50]}"
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "success": True,
                    "data": data
                }
            else:
                return {"success": False, "error": f"HTTP {response.status_code}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


async def test_deep_mode_complete(question: str, test_num: int) -> dict:
    """Test complet du mode DEEP"""
    print(f"\n{'='*60}")
    print(f"TEST #{test_num}: MODE DEEP COMPLET")
    print(f"{'='*60}")
    print(f"📋 Question: {question[:80]}...")
    print(f"⏳ Envoi de la requête (timeout: {TIMEOUT}s)...")
    
    start_time = time.time()
    
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            response = await client.post(
                API_URL,
                json={
                    "message": question,
                    "language": "fr",
                    "search_mode": "deep"
                }
            )
            
            elapsed = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                result = data.get("response", "")
                word_count = len(result.split())
                
                print(f"\n✅ RÉPONSE REÇUE")
                print(f"⏱️ Temps: {elapsed:.1f}s")
                print(f"📝 Mots: {word_count}")
                
                # Analyse du contenu
                content_analysis = {
                    "sections_found": [],
                    "sources_mentioned": [],
                    "apis_mentioned": []
                }
                
                # Détecter les sections
                section_markers = ["##", "**", "📋", "1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"]
                for marker in section_markers:
                    if marker in result:
                        content_analysis["sections_found"].append(marker)
                
                # Détecter les sources mentionnées
                source_keywords = [
                    "PUBMED", "FDA", "WHO", "OMS", "RxNorm", "CDC", 
                    "Europe PMC", "ClinicalTrials", "DrugBank", "SNOMED",
                    "ICD-11", "LOINC", "HAS", "NICE", "EMA", "Orphanet",
                    "ANALYSE IA", "SOURCE"
                ]
                for source in source_keywords:
                    if source.upper() in result.upper():
                        content_analysis["sources_mentioned"].append(source)
                
                # Vérifications qualité
                checks = {
                    "word_count_450+": word_count >= 450,
                    "word_count_1000_max": word_count <= 1000,
                    "has_sections": len(content_analysis["sections_found"]) >= 2,
                    "has_sources": len(content_analysis["sources_mentioned"]) >= 3,
                    "has_pubmed": "PUBMED" in result.upper(),
                    "has_structure": "##" in result or "**" in result,
                    "has_disclaimer": any(w in result.lower() for w in ["professionnel", "médecin", "consultez", "éducatives"]),
                    "no_hebrew": not any(ord(c) > 0x0590 and ord(c) < 0x05FF for c in result),
                    "in_french": "de" in result.lower() and "le" in result.lower(),
                    "time_acceptable": elapsed < 60,
                }
                
                print(f"\n📊 ANALYSE DU CONTENU:")
                print(f"  📑 Sections détectées: {len(content_analysis['sections_found'])}")
                print(f"  📚 Sources mentionnées: {len(content_analysis['sources_mentioned'])}")
                if content_analysis['sources_mentioned']:
                    print(f"     → {', '.join(content_analysis['sources_mentioned'][:10])}")
                
                print(f"\n📊 VÉRIFICATIONS QUALITÉ:")
                passed = 0
                for check, status in checks.items():
                    icon = "✅" if status else "❌"
                    print(f"  {icon} {check}: {status}")
                    if status:
                        passed += 1
                
                quality_score = (passed / len(checks)) * 100
                print(f"\n🎯 Score qualité: {quality_score:.0f}% ({passed}/{len(checks)})")
                
                # Extrait du contenu
                print(f"\n📖 DÉBUT DE RÉPONSE:")
                print("-" * 40)
                print(result[:600])
                print("-" * 40)
                
                print(f"\n📚 FIN DE RÉPONSE:")
                print("-" * 40)
                print(result[-400:])
                print("-" * 40)
                
                return {
                    "success": True,
                    "time_seconds": elapsed,
                    "word_count": word_count,
                    "quality_score": quality_score,
                    "checks": checks,
                    "content_analysis": content_analysis,
                    "sources_count": len(content_analysis["sources_mentioned"]),
                    "full_response": result
                }
                
            else:
                print(f"\n❌ ERREUR HTTP: {response.status_code}")
                return {"success": False, "error": f"HTTP {response.status_code}", "time_seconds": elapsed}
                
    except httpx.TimeoutException:
        elapsed = time.time() - start_time
        print(f"\n❌ TIMEOUT après {elapsed:.1f}s")
        return {"success": False, "error": "Timeout", "time_seconds": elapsed}
    except Exception as e:
        elapsed = time.time() - start_time
        print(f"\n❌ ERREUR: {e}")
        return {"success": False, "error": str(e), "time_seconds": elapsed}


async def run_complete_tests():
    """Run all tests"""
    print("=" * 60)
    print("🔬 TEST COMPLET MODE DEEP - 77 APIs MÉDICALES")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    results = []
    
    for i, question in enumerate(DEEP_TEST_QUESTIONS, 1):
        result = await test_deep_mode_complete(question, i)
        results.append({"question": question, **result})
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ COMPLET DES TESTS")
    print("=" * 60)
    
    success_count = sum(1 for r in results if r.get("success"))
    avg_time = sum(r.get("time_seconds", 0) for r in results) / len(results)
    avg_words = sum(r.get("word_count", 0) for r in results if r.get("success")) / max(success_count, 1)
    avg_quality = sum(r.get("quality_score", 0) for r in results if r.get("success")) / max(success_count, 1)
    avg_sources = sum(r.get("sources_count", 0) for r in results if r.get("success")) / max(success_count, 1)
    
    print(f"\n📈 MÉTRIQUES:")
    print(f"  ✅ Tests réussis: {success_count}/{len(results)}")
    print(f"  ⏱️ Temps moyen: {avg_time:.1f}s")
    print(f"  📝 Mots moyens: {avg_words:.0f}")
    print(f"  📚 Sources mentionnées: {avg_sources:.0f}")
    print(f"  🎯 Qualité moyenne: {avg_quality:.0f}%")
    
    # Quality assessment
    print("\n" + "=" * 60)
    print("🏆 ÉVALUATION FINALE")
    print("=" * 60)
    
    all_pass = True
    criteria = [
        ("Tests réussis", success_count == len(results), f"{success_count}/{len(results)}"),
        ("Temps < 60s", avg_time < 60, f"{avg_time:.1f}s"),
        ("Mots >= 450", avg_words >= 450, f"{avg_words:.0f}"),
        ("Qualité >= 90%", avg_quality >= 90, f"{avg_quality:.0f}%"),
        ("Sources >= 3", avg_sources >= 3, f"{avg_sources:.0f}"),
    ]
    
    for name, passed, value in criteria:
        icon = "✅" if passed else "❌"
        print(f"  {icon} {name}: {value}")
        if not passed:
            all_pass = False
    
    print("\n" + "=" * 60)
    if all_pass:
        print("🏆 TOUS LES CRITÈRES SONT SATISFAITS!")
        print("✅ Le mode DEEP est OPTIMAL et prêt pour la production!")
    else:
        print("⚠️ Certains critères ne sont pas satisfaits.")
        print("   Optimisation supplémentaire nécessaire.")
    print("=" * 60)
    
    return results


if __name__ == "__main__":
    asyncio.run(run_complete_tests())
