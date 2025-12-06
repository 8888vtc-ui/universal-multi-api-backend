"""
Exemples d'utilisation du Moteur de Recherche Universel
"""
import asyncio
import httpx
from typing import Dict, Any


BASE_URL = "http://localhost:8000"


async def example_1_finance_search():
    """Exemple 1: Recherche finance simple"""
    print("\n" + "="*60)
    print("EXEMPLE 1: Recherche Finance")
    print("="*60)
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            f"{BASE_URL}/api/search/universal",
            json={
                "query": "bitcoin prix",
                "categories": ["finance"],
                "max_results_per_category": 3,
                "language": "fr"
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n✅ Requête: {data['query']}")
            print(f"📊 Total résultats: {data['total_results']}")
            print(f"⏱️  Temps: {data['performance']['total_time_ms']}ms")
            print(f"💾 Cache: {'Oui' if data['performance']['cached'] else 'Non'}")
            
            if "finance" in data["results"]:
                print("\n💰 Résultats Finance:")
                for i, result in enumerate(data["results"]["finance"][:3], 1):
                    print(f"  {i}. {result['title']} (Score: {result['relevance_score']:.2f})")
        else:
            print(f"❌ Erreur: {response.status_code}")
            print(response.text)


async def example_2_multi_category():
    """Exemple 2: Recherche multi-catégories avec auto-détection"""
    print("\n" + "="*60)
    print("EXEMPLE 2: Recherche Multi-Catégories")
    print("="*60)
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            f"{BASE_URL}/api/search/universal",
            json={
                "query": "bitcoin actualité météo Paris",
                # Pas de categories: auto-détection
                "max_results_per_category": 2,
                "language": "fr"
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n✅ Requête: {data['query']}")
            print(f"📊 Catégories détectées: {', '.join(data['categories_searched'])}")
            print(f"📊 Total résultats: {data['total_results']}")
            
            for category, results in data["results"].items():
                if results:
                    print(f"\n📁 {category.upper()}:")
                    for result in results[:2]:
                        print(f"  • {result['title'][:50]}...")
        else:
            print(f"❌ Erreur: {response.status_code}")


async def example_3_quick_search():
    """Exemple 3: Recherche rapide (GET)"""
    print("\n" + "="*60)
    print("EXEMPLE 3: Recherche Rapide")
    print("="*60)
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            f"{BASE_URL}/api/search/quick",
            params={
                "q": "bitcoin",
                "categories": "finance,news",
                "limit": 2
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n✅ Requête: {data['query']}")
            print(f"📊 Total: {data['total_results']} résultats")
            print(f"⏱️  Temps: {data['performance']['total_time_ms']}ms")
        else:
            print(f"❌ Erreur: {response.status_code}")


async def example_4_list_categories():
    """Exemple 4: Lister les catégories disponibles"""
    print("\n" + "="*60)
    print("EXEMPLE 4: Liste des Catégories")
    print("="*60)
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(f"{BASE_URL}/api/search/categories")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n📋 {data['total']} catégories disponibles:\n")
            for cat in data["categories"]:
                print(f"  • {cat['name']} ({cat['id']})")
                print(f"    {cat['description']}")
                print(f"    Mots-clés: {', '.join(cat['keywords'][:3])}...")
                print()
        else:
            print(f"❌ Erreur: {response.status_code}")


async def example_5_cache_test():
    """Exemple 5: Tester le cache"""
    print("\n" + "="*60)
    print("EXEMPLE 5: Test du Cache")
    print("="*60)
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        # Première requête (pas de cache)
        print("\n1️⃣ Première requête (sans cache)...")
        response1 = await client.post(
            f"{BASE_URL}/api/search/universal",
            json={
                "query": "test cache",
                "categories": ["finance"],
                "max_results_per_category": 2
            }
        )
        
        if response1.status_code == 200:
            data1 = response1.json()
            time1 = data1['performance']['total_time_ms']
            cached1 = data1['performance']['cached']
            print(f"   Temps: {time1}ms | Cache: {cached1}")
        
        # Deuxième requête identique (avec cache)
        print("\n2️⃣ Deuxième requête identique (avec cache)...")
        await asyncio.sleep(0.5)  # Petit délai
        
        response2 = await client.post(
            f"{BASE_URL}/api/search/universal",
            json={
                "query": "test cache",
                "categories": ["finance"],
                "max_results_per_category": 2
            }
        )
        
        if response2.status_code == 200:
            data2 = response2.json()
            time2 = data2['performance']['total_time_ms']
            cached2 = data2['performance']['cached']
            print(f"   Temps: {time2}ms | Cache: {cached2}")
            
            if cached2:
                speedup = time1 / time2 if time2 > 0 else float('inf')
                print(f"\n🚀 Accélération: {speedup:.1f}x plus rapide avec cache!")


async def example_6_medical_search():
    """Exemple 6: Recherche médicale"""
    print("\n" + "="*60)
    print("EXEMPLE 6: Recherche Médicale")
    print("="*60)
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            f"{BASE_URL}/api/search/universal",
            json={
                "query": "diabète traitement",
                "categories": ["medical"],
                "max_results_per_category": 3,
                "language": "fr"
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n✅ Requête: {data['query']}")
            
            if "medical" in data["results"]:
                print(f"\n🏥 Résultats Médicaux ({len(data['results']['medical'])}):")
                for i, result in enumerate(data["results"]["medical"], 1):
                    print(f"\n  {i}. {result['title']}")
                    print(f"     Source: {result['source']}")
                    print(f"     Score: {result['relevance_score']:.2f}")
                    if result.get('url'):
                        print(f"     URL: {result['url']}")
        else:
            print(f"❌ Erreur: {response.status_code}")


async def main():
    """Exécuter tous les exemples"""
    print("\n" + "="*60)
    print("🔍 EXEMPLES - MOTEUR DE RECHERCHE UNIVERSEL")
    print("="*60)
    print("\n⚠️  Assurez-vous que le serveur backend est démarré!")
    print("   Commande: cd backend && python main.py\n")
    
    try:
        # Vérifier que le serveur est accessible
        async with httpx.AsyncClient(timeout=5.0) as client:
            await client.get(f"{BASE_URL}/api/health")
    except Exception as e:
        print(f"❌ Erreur: Impossible de se connecter au serveur ({BASE_URL})")
        print(f"   {e}\n")
        return
    
    # Exécuter les exemples
    examples = [
        example_1_finance_search,
        example_2_multi_category,
        example_3_quick_search,
        example_4_list_categories,
        example_5_cache_test,
        example_6_medical_search
    ]
    
    for example in examples:
        try:
            await example()
            await asyncio.sleep(1)  # Pause entre exemples
        except Exception as e:
            print(f"\n❌ Erreur dans {example.__name__}: {e}")
    
    print("\n" + "="*60)
    print("✅ EXEMPLES TERMINÉS")
    print("="*60)


if __name__ == "__main__":
    asyncio.run(main())



