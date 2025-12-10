"""
Test DEEP Mode Medical Search
Runs tests until optimal results are achieved
"""
import asyncio
import httpx
import time
import json
from datetime import datetime

# Configuration
API_URL = "https://universal-api-hub.fly.dev/api/expert/health/chat"
TIMEOUT = 120  # 2 minutes for deep search

# Test questions for DEEP mode
DEEP_TEST_QUESTIONS = [
    "Quels sont les traitements du diabète de type 2 et leurs effets secondaires?",
    # "What are the latest treatments for breast cancer?",
    # "Expliquez les interactions médicamenteuses de la metformine",
]

async def test_deep_mode(question: str, test_num: int) -> dict:
    """Test a single question in DEEP mode"""
    print(f"\n{'='*60}")
    print(f"TEST #{test_num}: DEEP MODE")
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
                    "search_mode": "deep"  # Force DEEP mode
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
                
                # Vérifications qualité
                checks = {
                    "word_count_500+": word_count >= 500,
                    "has_sections": "##" in result or "**" in result,
                    "has_sources": "[" in result and "]" in result,
                    "has_pubmed": "PUBMED" in result.upper() or "pubmed" in result.lower(),
                    "has_disclaimer": "professionnel" in result.lower() or "médecin" in result.lower() or "consultez" in result.lower(),
                    "no_hebrew": not any(ord(c) > 0x0590 and ord(c) < 0x05FF for c in result),
                    "in_french": "de" in result.lower() and "le" in result.lower(),
                }
                
                print(f"\n📊 VÉRIFICATIONS QUALITÉ:")
                passed = 0
                for check, status in checks.items():
                    icon = "✅" if status else "❌"
                    print(f"  {icon} {check}: {status}")
                    if status:
                        passed += 1
                
                quality_score = (passed / len(checks)) * 100
                print(f"\n🎯 Score qualité: {quality_score:.0f}% ({passed}/{len(checks)})")
                
                # Afficher un extrait
                print(f"\n📖 EXTRAIT (500 premiers caractères):")
                print("-" * 40)
                print(result[:500] + "...")
                print("-" * 40)
                
                # Afficher la fin (sources)
                print(f"\n📚 FIN DE RÉPONSE (500 derniers caractères):")
                print("-" * 40)
                print("..." + result[-500:])
                print("-" * 40)
                
                return {
                    "success": True,
                    "time_seconds": elapsed,
                    "word_count": word_count,
                    "quality_score": quality_score,
                    "checks": checks,
                    "response_preview": result[:1000],
                    "response_end": result[-500:]
                }
                
            else:
                print(f"\n❌ ERREUR HTTP: {response.status_code}")
                print(f"Réponse: {response.text[:500]}")
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}",
                    "time_seconds": elapsed
                }
                
    except httpx.TimeoutException:
        elapsed = time.time() - start_time
        print(f"\n❌ TIMEOUT après {elapsed:.1f}s")
        return {
            "success": False,
            "error": "Timeout",
            "time_seconds": elapsed
        }
    except Exception as e:
        elapsed = time.time() - start_time
        print(f"\n❌ ERREUR: {type(e).__name__}: {e}")
        return {
            "success": False,
            "error": str(e),
            "time_seconds": elapsed
        }


async def run_all_tests():
    """Run all DEEP mode tests"""
    print("=" * 60)
    print("🔬 TEST MODE DEEP - 77 APIs MÉDICALES")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    results = []
    
    for i, question in enumerate(DEEP_TEST_QUESTIONS, 1):
        result = await test_deep_mode(question, i)
        results.append({
            "question": question,
            **result
        })
        
        # Wait between tests
        if i < len(DEEP_TEST_QUESTIONS):
            print("\n⏳ Attente 5s avant prochain test...")
            await asyncio.sleep(5)
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 60)
    
    success_count = sum(1 for r in results if r.get("success"))
    avg_time = sum(r.get("time_seconds", 0) for r in results) / len(results)
    avg_words = sum(r.get("word_count", 0) for r in results if r.get("success")) / max(success_count, 1)
    avg_quality = sum(r.get("quality_score", 0) for r in results if r.get("success")) / max(success_count, 1)
    
    print(f"✅ Tests réussis: {success_count}/{len(results)}")
    print(f"⏱️ Temps moyen: {avg_time:.1f}s")
    print(f"📝 Mots moyens: {avg_words:.0f}")
    print(f"🎯 Qualité moyenne: {avg_quality:.0f}%")
    
    # Optimal check
    print("\n" + "=" * 60)
    if success_count == len(results) and avg_quality >= 80 and avg_words >= 500:
        print("🏆 RÉSULTAT OPTIMAL ATTEINT!")
    else:
        print("⚠️ OPTIMISATION NÉCESSAIRE:")
        if success_count < len(results):
            print("  - Certains tests ont échoué")
        if avg_quality < 80:
            print(f"  - Qualité insuffisante ({avg_quality:.0f}% < 80%)")
        if avg_words < 500:
            print(f"  - Nombre de mots insuffisant ({avg_words:.0f} < 500)")
    print("=" * 60)
    
    return results


if __name__ == "__main__":
    asyncio.run(run_all_tests())
