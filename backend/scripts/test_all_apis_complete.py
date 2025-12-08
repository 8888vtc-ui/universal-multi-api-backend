"""
Script de test complet pour TOUTES les APIs
Vérifie que le serveur est lancé et teste tous les endpoints
"""
import sys
import asyncio
import httpx
import time
from typing import List, Tuple, Dict

sys.stdout.reconfigure(encoding='utf-8')

BASE_URL = "http://localhost:8000"
TIMEOUT = 20.0

# Test cases pour TOUTES les APIs
TEST_CASES = [
    # Health & Status
    ("GET", "/api/health", "Health Check"),
    ("GET", "/api/health/deep", "Deep Health"),
    ("GET", "/api/metrics", "Metrics"),
    
    # JSONPlaceholder
    ("GET", "/api/jsonplaceholder/posts?limit=3", "JSONPlaceholder - Posts"),
    ("GET", "/api/jsonplaceholder/users", "JSONPlaceholder - Users"),
    
    # RandomUser
    ("GET", "/api/randomuser/users?count=2", "RandomUser - Generate Users"),
    
    # FakeStore
    ("GET", "/api/fakestore/products?limit=3", "FakeStore - Products"),
    ("GET", "/api/fakestore/categories", "FakeStore - Categories"),
    
    # Quotes
    ("GET", "/api/quotes/random", "Quotes - Random Quote"),
    ("GET", "/api/quotes/advice/random", "Quotes - Random Advice"),
    
    # Lorem
    ("GET", "/api/lorem/text?paragraphs=1", "Lorem - Text"),
    
    # Lorem Picsum
    ("GET", "/api/lorempicsum/image?width=200&height=200", "Lorem Picsum - Image URL"),
    
    # GitHub
    ("GET", "/api/github/users/octocat", "GitHub - User Info"),
    ("GET", "/api/github/search/repos?query=fastapi&limit=3", "GitHub - Search Repos"),
    
    # World Time
    ("GET", "/api/worldtime/timezone/Europe/Paris", "World Time - Timezone"),
    ("GET", "/api/worldtime/timezones", "World Time - List Timezones"),
    
    # CoinCap
    ("GET", "/api/coincap/assets?limit=5", "CoinCap - Assets"),
    ("GET", "/api/coincap/assets/bitcoin", "CoinCap - Bitcoin"),
    
    # TinyURL
    ("GET", "/api/tinyurl/shorten?url=https://example.com", "TinyURL - Shorten"),
    
    # Countries
    ("GET", "/api/countries/all", "Countries - All"),
    ("GET", "/api/countries/name/france", "Countries - Search by Name"),
    
    # Wikipedia
    ("GET", "/api/wikipedia/search?query=python&limit=2", "Wikipedia - Search"),
    
    # IP Geolocation
    ("GET", "/api/ip/my-ip", "IP Geolocation - My IP"),
    
    # AI Chat (simple test)
    ("POST", "/api/chat", "AI Chat", {"message": "Hello", "language": "en"}),
    
    # Finance
    ("GET", "/api/finance/crypto/price?symbol=bitcoin", "Finance - Crypto Price"),
    
    # Weather
    ("GET", "/api/weather/current?city=Paris", "Weather - Current"),
    
    # Translation
    ("POST", "/api/translation/translate", "Translation", {
        "text": "Hello",
        "target_lang": "fr",
        "source_lang": "en"
    }),
]

async def check_server_ready() -> bool:
    """Vérifie si le serveur est prêt"""
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{BASE_URL}/api/health")
            return response.status_code == 200
    except:
        return False

async def test_endpoint(
    client: httpx.AsyncClient,
    method: str,
    path: str,
    name: str,
    json_data: dict = None
) -> Tuple[bool, str, int]:
    """Teste un endpoint"""
    try:
        url = f"{BASE_URL}{path}"
        
        if method == "GET":
            response = await client.get(url, timeout=TIMEOUT)
        elif method == "POST":
            response = await client.post(url, json=json_data, timeout=TIMEOUT)
        else:
            response = await client.request(method, url, json=json_data, timeout=TIMEOUT)
        
        status = response.status_code
        
        if status in [200, 201, 202]:
            return True, f"[OK] {name}", status
        elif status == 503:
            return False, f"[WARN]  {name} - Service Unavailable (API key may be missing)", status
        elif status == 422:
            return False, f"[WARN]  {name} - Validation Error (check parameters)", status
        else:
            error_text = response.text[:100] if hasattr(response, 'text') else ""
            return False, f"[ERR] {name} - Status: {status}", status
            
    except httpx.TimeoutException:
        return False, f"⏱️  {name} - Timeout", 0
    except httpx.ConnectError:
        return False, f"🔌 {name} - Connection Error (server not running?)", 0
    except Exception as e:
        return False, f"[ERR] {name} - Error: {str(e)[:80]}", 0

async def main():
    """Fonction principale"""
    print("=" * 70)
    print("   🧪 TEST COMPLET DE TOUTES LES APIs")
    print("=" * 70)
    print()
    
    # Vérifier si le serveur est lancé
    print("[INFO] Vérification du serveur...")
    if not await check_server_ready():
        print()
        print("[ERR] Le serveur n'est pas lancé ou n'est pas accessible!")
        print()
        print("💡 Pour lancer le serveur:")
        print("   cd backend")
        print("   python main.py")
        print()
        print("   OU")
        print()
        print("   python scripts/start_server.py")
        print()
        print("⏳ Attente de 5 secondes pour vérifier à nouveau...")
        await asyncio.sleep(5)
        
        if not await check_server_ready():
            print("[ERR] Le serveur n'est toujours pas accessible.")
            print("   Veuillez lancer le serveur avant d'exécuter les tests.")
            sys.exit(1)
    
    print("[OK] Serveur accessible!")
    print()
    print("=" * 70)
    print("   [ROCKET] DÉMARRAGE DES TESTS")
    print("=" * 70)
    print()
    
    results: List[Tuple[bool, str, int]] = []
    
    async with httpx.AsyncClient() as client:
        for i, test_case in enumerate(TEST_CASES, 1):
            if len(test_case) == 4:
                method, path, name, json_data = test_case
            else:
                method, path, name = test_case
                json_data = None
            
            success, message, status = await test_endpoint(
                client, method, path, name, json_data
            )
            results.append((success, message, status))
            
            # Afficher le résultat
            status_icon = "[OK]" if success else ("[WARN]" if status in [503, 422] else "[ERR]")
            print(f"{i:2d}. {message}")
            
            # Petit délai pour éviter le rate limiting
            await asyncio.sleep(0.3)
    
    print()
    print("=" * 70)
    print("   📊 RÉSULTATS FINAUX")
    print("=" * 70)
    
    passed = sum(1 for success, _, _ in results if success)
    warnings = sum(1 for success, _, status in results if not success and status in [503, 422])
    failed = len(results) - passed - warnings
    
    print(f"[OK] Réussis:     {passed}/{len(results)} ({passed*100//len(results)}%)")
    print(f"[WARN]  Avertissements: {warnings}/{len(results)} (clés API manquantes)")
    print(f"[ERR] Échoués:     {failed}/{len(results)}")
    print()
    
    if warnings > 0:
        print("[WARN]  Endpoints avec avertissements (clés API manquantes):")
        for success, message, status in results:
            if not success and status in [503, 422]:
                print(f"   {message}")
        print()
    
    if failed > 0:
        print("[ERR] Endpoints échoués:")
        for success, message, status in results:
            if not success and status not in [503, 422]:
                print(f"   {message}")
        print()
    
    print("=" * 70)
    
    if failed == 0:
        if warnings == 0:
            print("   🎉 TOUS LES TESTS SONT PASSÉS !")
        else:
            print(f"   [OK] {passed} tests réussis, {warnings} nécessitent des clés API")
    else:
        print(f"   [WARN]  {failed} test(s) ont échoué")
    
    print("=" * 70)
    print()
    
    # Résumé par catégorie
    print("📋 Résumé par catégorie:")
    categories = {
        "Health": 0,
        "Test Data": 0,
        "Content": 0,
        "Images": 0,
        "Development": 0,
        "Utilities": 0,
        "Finance": 0,
        "Location": 0,
        "AI": 0,
        "Other": 0
    }
    
    for success, message, _ in results:
        if success:
            if "Health" in message or "Metrics" in message:
                categories["Health"] += 1
            elif "JSONPlaceholder" in message or "RandomUser" in message or "FakeStore" in message:
                categories["Test Data"] += 1
            elif "Quotes" in message or "Lorem" in message:
                categories["Content"] += 1
            elif "Picsum" in message or "Pixabay" in message:
                categories["Images"] += 1
            elif "GitHub" in message:
                categories["Development"] += 1
            elif "Time" in message or "TinyURL" in message or "IP" in message:
                categories["Utilities"] += 1
            elif "CoinCap" in message or "Finance" in message:
                categories["Finance"] += 1
            elif "Countries" in message or "Weather" in message:
                categories["Location"] += 1
            elif "Chat" in message or "AI" in message:
                categories["AI"] += 1
            else:
                categories["Other"] += 1
    
    for category, count in categories.items():
        if count > 0:
            print(f"   {category}: {count} test(s) réussis")
    
    print()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n[STOP] Tests interrompus par l'utilisateur")
        sys.exit(0)






