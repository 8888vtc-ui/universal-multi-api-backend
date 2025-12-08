"""
Exemple d'utilisation de la recherche optimisée avec regroupement
"""
import asyncio
import httpx

BASE_URL = "http://localhost:8000"


async def example_optimized_search():
    """Exemple de recherche optimisée"""
    async with httpx.AsyncClient() as client:
        # 1. Détecter les catégories
        print("[INFO] Détection de catégories...")
        response = await client.get(
            f"{BASE_URL}/api/search/optimized/detect",
            params={"query": "prix bitcoin et actualités"}
        )
        print(f"Catégories détectées: {response.json()['detected_categories']}")
        print()
        
        # 2. Obtenir la stratégie
        print("🧠 Génération de stratégie...")
        response = await client.get(
            f"{BASE_URL}/api/search/optimized/strategy",
            params={"query": "prix bitcoin", "max_results": 5}
        )
        strategy = response.json()
        print(f"Catégories: {strategy['detected_categories']}")
        print(f"Temps estimé: {strategy['estimated_time_ms']}ms")
        print(f"APIs prioritaires: {strategy['priority_apis']}")
        print()
        
        # 3. Recherche optimisée
        print("[ROCKET] Recherche optimisée...")
        response = await client.post(
            f"{BASE_URL}/api/search/optimized/search",
            json={
                "query": "prix bitcoin et actualités",
                "max_results_per_category": 5,
                "use_cache": True
            }
        )
        result = response.json()
        print(f"Temps total: {result['performance']['total_time_ms']}ms")
        print(f"Catégories recherchées: {result['strategy']['categories_searched']}")
        print(f"Résultats: {len(result['results'])} catégories")
        print()


async def example_list_categories():
    """Exemple : Liste toutes les catégories"""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/api/search/optimized/categories")
        categories = response.json()
        print(f"📋 {len(categories)} catégories disponibles:")
        for cat in categories[:5]:  # Afficher les 5 premières
            print(f"  - {cat['category']}: {len(cat['apis'])} APIs")
        print()


if __name__ == "__main__":
    print("=" * 70)
    print("   EXEMPLES DE RECHERCHE OPTIMISÉE")
    print("=" * 70)
    print()
    
    asyncio.run(example_list_categories())
    asyncio.run(example_optimized_search())






