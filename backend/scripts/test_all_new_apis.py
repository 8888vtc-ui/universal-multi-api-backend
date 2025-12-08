"""
Test script for all newly added free APIs
"""
import sys
import asyncio
import httpx
from typing import List, Tuple

sys.stdout.reconfigure(encoding='utf-8')

BASE_URL = "http://localhost:8000"

# Test cases for each API
TEST_CASES = [
    # JSONPlaceholder
    ("GET", "/api/jsonplaceholder/posts?limit=5", "JSONPlaceholder - Posts"),
    ("GET", "/api/jsonplaceholder/users", "JSONPlaceholder - Users"),
    ("GET", "/api/jsonplaceholder/todos?user_id=1", "JSONPlaceholder - Todos"),
    
    # RandomUser
    ("GET", "/api/randomuser/users?count=3", "RandomUser - Generate Users"),
    
    # FakeStore
    ("GET", "/api/fakestore/products?limit=5", "FakeStore - Products"),
    ("GET", "/api/fakestore/categories", "FakeStore - Categories"),
    
    # Quotes
    ("GET", "/api/quotes/random", "Quotes - Random Quote"),
    ("GET", "/api/quotes/advice/random", "Quotes - Random Advice"),
    
    # Lorem
    ("GET", "/api/lorem/text?paragraphs=2", "Lorem - Text"),
    
    # Lorem Picsum
    ("GET", "/api/lorempicsum/image?width=400&height=300", "Lorem Picsum - Image URL"),
    
    # GitHub
    ("GET", "/api/github/users/octocat", "GitHub - User Info"),
    ("GET", "/api/github/search/repos?query=fastapi&limit=5", "GitHub - Search Repos"),
    
    # World Time
    ("GET", "/api/worldtime/timezone/Europe/Paris", "World Time - Timezone"),
    ("GET", "/api/worldtime/timezones", "World Time - List Timezones"),
    
    # CoinCap
    ("GET", "/api/coincap/assets?limit=10", "CoinCap - Assets"),
    ("GET", "/api/coincap/assets/bitcoin", "CoinCap - Bitcoin"),
    
    # TinyURL
    ("GET", "/api/tinyurl/shorten?url=https://example.com", "TinyURL - Shorten"),
    
    # Existing APIs (quick check)
    ("GET", "/api/countries/all", "Countries - All"),
    ("GET", "/api/wikipedia/search?query=python&limit=3", "Wikipedia - Search"),
    ("GET", "/api/ip/my-ip", "IP Geolocation - My IP"),
]

async def test_endpoint(client: httpx.AsyncClient, method: str, path: str, name: str) -> Tuple[bool, str]:
    """Test a single endpoint"""
    try:
        url = f"{BASE_URL}{path}"
        response = await client.request(method, url, timeout=15.0)
        
        if response.status_code in [200, 201, 202]:
            return True, f"[OK] {name} - Status: {response.status_code}"
        elif response.status_code == 503:
            return False, f"[WARN]  {name} - Service Unavailable (API key may be missing)"
        else:
            return False, f"[ERR] {name} - Status: {response.status_code}, Error: {response.text[:100]}"
    except httpx.TimeoutException:
        return False, f"⏱️  {name} - Timeout"
    except Exception as e:
        return False, f"[ERR] {name} - Error: {str(e)[:100]}"

async def main():
    """Run all tests"""
    print("=" * 70)
    print("   🧪 TEST DE TOUTES LES NOUVELLES APIs GRATUITES")
    print("=" * 70)
    print()
    
    results = []
    async with httpx.AsyncClient() as client:
        for method, path, name in TEST_CASES:
            success, message = await test_endpoint(client, method, path, name)
            results.append((success, message))
            print(message)
            await asyncio.sleep(0.5)  # Rate limiting
    
    print()
    print("=" * 70)
    print("   📊 RÉSULTATS")
    print("=" * 70)
    
    passed = sum(1 for success, _ in results if success)
    failed = len(results) - passed
    
    print(f"[OK] Réussis: {passed}/{len(results)}")
    print(f"[ERR] Échoués: {failed}/{len(results)}")
    print()
    
    if failed > 0:
        print("[WARN]  Endpoints échoués:")
        for success, message in results:
            if not success:
                print(f"   {message}")
    
    print()
    print("=" * 70)
    
    if failed == 0:
        print("   🎉 TOUS LES TESTS SONT PASSÉS !")
    else:
        print(f"   [WARN]  {failed} test(s) ont échoué (peut être dû à des clés API manquantes)")
    print("=" * 70)

if __name__ == "__main__":
    asyncio.run(main())






