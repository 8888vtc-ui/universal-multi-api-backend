"""
Test DEEP Medical Search - Test recherche approfondie
Vérifie que le mode LONG affiche bien le log de recherche
"""
import httpx
import asyncio
import time


PRODUCTION_URL = "https://universal-api-hub.fly.dev"


async def test_deep_search():
    """Test le mode recherche approfondie"""
    
    print("\n" + "=" * 70)
    print("🔬 TEST RECHERCHE MEDICALE APPROFONDIE")
    print("=" * 70)
    
    # Query qui devrait déclencher le mode DEEP
    deep_queries = [
        "Je suis etudiant en medecine. Explique-moi le diabete de type 2 en detail avec toutes les donnees disponibles.",
        "Fais-moi un rapport complet sur l'hypertension arterielle avec les dernieres etudes.",
    ]
    
    async with httpx.AsyncClient(timeout=120.0) as client:
        
        # Health check
        print("\n📡 Verification du serveur...")
        try:
            response = await client.get(f"{PRODUCTION_URL}/api/health")
            if response.status_code == 200:
                print("✅ Serveur accessible")
            else:
                print(f"❌ Erreur serveur: {response.status_code}")
                return
        except Exception as e:
            print(f"❌ Serveur inaccessible: {e}")
            return
        
        # Test deep queries
        for i, query in enumerate(deep_queries, 1):
            print(f"\n{'=' * 70}")
            print(f"📋 TEST {i}/{len(deep_queries)}")
            print(f"{'=' * 70}")
            print(f"\n🔍 Requete: {query[:60]}...")
            print("\n⏳ Recherche en cours (peut prendre 30-60 secondes)...")
            
            start_time = time.time()
            
            try:
                response = await client.post(
                    f"{PRODUCTION_URL}/api/expert/health/chat",
                    json={
                        "message": query,
                        "session_id": f"deep_test_{int(time.time())}"
                    }
                )
                
                elapsed = time.time() - start_time
                
                if response.status_code == 200:
                    data = response.json()
                    response_text = data.get("response", "")
                    sources = data.get("sources", [])
                    
                    print(f"\n✅ Reponse recue en {elapsed:.1f}s")
                    print(f"📊 Longueur: {len(response_text)} caracteres")
                    print(f"📚 Sources: {sources}")
                    
                    # Vérifier la qualité
                    print("\n" + "-" * 50)
                    print("🔍 ANALYSE DE LA RÉPONSE:")
                    print("-" * 50)
                    
                    # Check for research log
                    has_log = any(x in response_text for x in [
                        "RECHERCHE", "APIs", "PubMed", "FDA", 
                        "Phase", "consultees", "RAPPORT"
                    ])
                    print(f"{'✅' if has_log else '⚠️'} Log de recherche: {'Present' if has_log else 'Absent'}")
                    
                    # Check for structure
                    has_structure = "##" in response_text or "**" in response_text or "📌" in response_text
                    print(f"{'✅' if has_structure else '⚠️'} Structure: {'Presente' if has_structure else 'Absente'}")
                    
                    # Check for sources
                    source_tags = ["[PUBMED]", "[FDA]", "[OMS]", "[RxNorm]", "[ANALYSE IA]"]
                    found_sources = [s for s in source_tags if s in response_text]
                    print(f"{'✅' if found_sources else '⚠️'} Sources citees: {found_sources if found_sources else 'Aucune'}")
                    
                    # Check for disclaimer
                    has_disclaimer = any(x in response_text.lower() for x in [
                        "medecin", "professionnel", "consultation", "avis medical"
                    ])
                    print(f"{'✅' if has_disclaimer else '⚠️'} Disclaimer: {'Present' if has_disclaimer else 'Absent'}")
                    
                    # Print preview
                    print("\n" + "-" * 50)
                    print("📄 APERÇU DE LA RÉPONSE:")
                    print("-" * 50)
                    
                    # Show first 1500 chars
                    preview = response_text[:1500]
                    print(preview)
                    if len(response_text) > 1500:
                        print(f"\n... [{len(response_text) - 1500} caracteres de plus] ...")
                    
                else:
                    print(f"❌ Erreur HTTP: {response.status_code}")
                    print(f"   Details: {response.text[:500]}")
                    
            except Exception as e:
                print(f"❌ Erreur: {e}")
            
            # Pause entre les tests
            if i < len(deep_queries):
                print("\n⏳ Pause de 5 secondes...")
                await asyncio.sleep(5)


async def main():
    await test_deep_search()
    
    print("\n" + "=" * 70)
    print("✅ TEST TERMINE")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())
