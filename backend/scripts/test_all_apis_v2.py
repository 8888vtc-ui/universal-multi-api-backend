"""
Test complet de toutes les APIs v2.4.0
Teste 70+ APIs incluant les nouvelles
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

import asyncio
import httpx
import time
from typing import Dict, List, Tuple

BASE_URL = "http://localhost:8000"

# Définition de tous les tests
TESTS = {
    # === Health & Status ===
    "health": {"method": "GET", "path": "/api/health"},
    "health_deep": {"method": "GET", "path": "/api/health/deep"},
    "metrics": {"method": "GET", "path": "/api/metrics"},
    
    # === AI ===
    "chat": {"method": "POST", "path": "/api/chat", "json": {"message": "Hello", "language": "en"}},
    "ai_search": {"method": "POST", "path": "/api/ai-search/search", "json": {"query": "test"}},
    
    # === Finance ===
    "coincap": {"method": "GET", "path": "/api/coincap/assets?limit=5"},
    "exchange_rates": {"method": "GET", "path": "/api/exchange/rates/USD"},
    "exchange_convert": {"method": "GET", "path": "/api/exchange/convert?amount=100&from_currency=USD&to_currency=EUR"},
    
    # === Knowledge ===
    "wikipedia": {"method": "GET", "path": "/api/wikipedia/search?query=Python&limit=3"},
    "books_google": {"method": "GET", "path": "/api/books/search?query=Python&limit=3"},
    "openlibrary": {"method": "GET", "path": "/api/openlibrary/search?query=Python&limit=3"},
    "trivia": {"method": "GET", "path": "/api/trivia/questions?amount=5"},
    "trivia_categories": {"method": "GET", "path": "/api/trivia/categories"},
    "numbers_random": {"method": "GET", "path": "/api/numbers/random"},
    "numbers_fact": {"method": "GET", "path": "/api/numbers/fact/42"},
    
    # === Countries & Location ===
    "countries_all": {"method": "GET", "path": "/api/countries/all"},
    "ip_my": {"method": "GET", "path": "/api/ip/my-ip"},
    "worldtime": {"method": "GET", "path": "/api/worldtime/timezones"},
    
    # === Fun & Entertainment ===
    "jokes_random": {"method": "GET", "path": "/api/jokes/random"},
    "jokes_chuck": {"method": "GET", "path": "/api/jokes/chuck"},
    "bored": {"method": "GET", "path": "/api/bored/activity"},
    "dogs": {"method": "GET", "path": "/api/animals/dogs/random"},
    "cats": {"method": "GET", "path": "/api/animals/cats/random"},
    "dogs_breeds": {"method": "GET", "path": "/api/animals/dogs/breeds"},
    
    # === Content Generation ===
    "quotes_random": {"method": "GET", "path": "/api/quotes/random"},
    "quotes_advice": {"method": "GET", "path": "/api/quotes/advice/random"},
    "lorem_text": {"method": "GET", "path": "/api/lorem/text"},
    "lorempicsum": {"method": "GET", "path": "/api/lorempicsum/list?limit=3"},
    
    # === Dev Tools ===
    "jsonplaceholder_posts": {"method": "GET", "path": "/api/jsonplaceholder/posts?limit=3"},
    "randomuser": {"method": "GET", "path": "/api/randomuser/users?count=3"},
    "fakestore": {"method": "GET", "path": "/api/fakestore/products?limit=3"},
    "github_search": {"method": "GET", "path": "/api/github/search/repos?query=python&limit=3"},
    
    # === Name Analysis ===
    "name_analyze": {"method": "GET", "path": "/api/name/analyze?name=John"},
    "name_age": {"method": "GET", "path": "/api/name/age?name=Marie"},
    "name_gender": {"method": "GET", "path": "/api/name/gender?name=Alex"},
    
    # === Search ===
    "search_categories": {"method": "GET", "path": "/api/search/optimized/categories"},
    "search_detect": {"method": "GET", "path": "/api/search/optimized/detect?query=bitcoin price"},
    
    # === History ===
    "history_stats": {"method": "GET", "path": "/api/history/"},
    
    # === Export ===
    "export_formats": {"method": "GET", "path": "/api/export/formats"},
}


async def run_test(client: httpx.AsyncClient, name: str, config: dict) -> Tuple[str, bool, str, float]:
    """Exécute un test et retourne le résultat"""
    method = config["method"]
    path = config["path"]
    
    start = time.time()
    try:
        if method == "GET":
            response = await client.get(f"{BASE_URL}{path}", timeout=15.0)
        elif method == "POST":
            response = await client.post(
                f"{BASE_URL}{path}",
                json=config.get("json", {}),
                timeout=15.0
            )
        
        duration = (time.time() - start) * 1000
        
        if response.status_code == 200:
            return name, True, "OK", duration
        else:
            return name, False, f"Status {response.status_code}", duration
            
    except httpx.TimeoutException:
        return name, False, "Timeout", (time.time() - start) * 1000
    except Exception as e:
        return name, False, str(e)[:50], (time.time() - start) * 1000


async def main():
    print("=" * 70)
    print("   🧪 TEST COMPLET DES APIs v2.4.0")
    print("=" * 70)
    print()
    
    # Vérifier que le serveur est accessible
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{BASE_URL}/api/health", timeout=5.0)
            if response.status_code != 200:
                print("❌ Serveur non accessible. Lancez: python main.py")
                return
    except:
        print("❌ Serveur non accessible. Lancez: python main.py")
        return
    
    print(f"✅ Serveur accessible sur {BASE_URL}")
    print(f"📊 Tests à exécuter: {len(TESTS)}")
    print()
    
    # Exécuter les tests
    results = []
    async with httpx.AsyncClient() as client:
        # Exécuter par lots de 5 pour ne pas surcharger
        test_items = list(TESTS.items())
        batch_size = 5
        
        for i in range(0, len(test_items), batch_size):
            batch = test_items[i:i+batch_size]
            tasks = [run_test(client, name, config) for name, config in batch]
            batch_results = await asyncio.gather(*tasks)
            results.extend(batch_results)
            
            # Afficher la progression
            for name, success, message, duration in batch_results:
                icon = "✅" if success else "❌"
                print(f"  {icon} {name:25} {message:20} ({duration:.0f}ms)")
    
    # Résumé
    print()
    print("=" * 70)
    print("   📊 RÉSUMÉ")
    print("=" * 70)
    
    successes = sum(1 for _, success, _, _ in results if success)
    failures = len(results) - successes
    total_time = sum(d for _, _, _, d in results)
    
    print(f"""
    ✅ Succès:     {successes}/{len(results)} ({100*successes/len(results):.1f}%)
    ❌ Échecs:     {failures}
    ⏱️  Temps total: {total_time/1000:.2f}s
    ⚡ Temps moyen: {total_time/len(results):.0f}ms
    """)
    
    if failures > 0:
        print("  APIs en échec:")
        for name, success, message, _ in results:
            if not success:
                print(f"    - {name}: {message}")
    
    print()
    if failures == 0:
        print("  🎉 TOUS LES TESTS PASSENT !")
    elif failures <= 3:
        print("  ⚠️ Quelques échecs mineurs (APIs optionnelles ?)")
    else:
        print("  ❌ Plusieurs échecs - vérifier la configuration")
    
    return successes, failures


if __name__ == "__main__":
    asyncio.run(main())

