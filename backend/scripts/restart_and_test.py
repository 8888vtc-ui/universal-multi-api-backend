"""
Script pour arrêter, redémarrer le serveur et tester toutes les APIs
"""
import sys
import os
import subprocess
import time
import httpx
import asyncio

sys.stdout.reconfigure(encoding='utf-8')

def kill_server():
    """Arrête tous les processus Python qui pourraient être le serveur"""
    try:
        # Windows
        if os.name == 'nt':
            subprocess.run(['taskkill', '/F', '/IM', 'python.exe'], 
                         capture_output=True, stderr=subprocess.DEVNULL)
        else:
            # Linux/Mac
            subprocess.run(['pkill', '-f', 'main.py'], 
                         capture_output=True, stderr=subprocess.DEVNULL)
        print("[OK] Anciens processus arrêtés")
        time.sleep(2)
    except:
        pass

def start_server():
    """Démarre le serveur en arrière-plan"""
    try:
        os.chdir('backend')
        if os.name == 'nt':
            # Windows
            subprocess.Popen(['python', 'main.py'], 
                           creationflags=subprocess.CREATE_NEW_CONSOLE)
        else:
            # Linux/Mac
            subprocess.Popen(['python', 'main.py'], 
                           stdout=subprocess.DEVNULL, 
                           stderr=subprocess.DEVNULL)
        print("[OK] Serveur lancé")
        time.sleep(8)  # Attendre que le serveur démarre
    except Exception as e:
        print(f"[ERR] Erreur au démarrage: {e}")

async def test_endpoint(client, method, path, name, json_data=None):
    """Teste un endpoint"""
    try:
        url = f"http://localhost:8000{path}"
        if method == "GET":
            response = await client.get(url, timeout=10.0)
        else:
            response = await client.post(url, json=json_data, timeout=10.0)
        
        if response.status_code in [200, 201]:
            return True, f"[OK] {name}"
        elif response.status_code == 404:
            return False, f"[ERR] {name} - 404 (route non trouvée)"
        else:
            return False, f"[WARN]  {name} - Status: {response.status_code}"
    except Exception as e:
        return False, f"[ERR] {name} - Error: {str(e)[:50]}"

async def run_tests():
    """Lance tous les tests"""
    print("\n" + "="*70)
    print("   🧪 TESTS DES NOUVELLES APIs")
    print("="*70 + "\n")
    
    tests = [
        ("GET", "/api/jsonplaceholder/posts?limit=2", "JSONPlaceholder"),
        ("GET", "/api/randomuser/users?count=1", "RandomUser"),
        ("GET", "/api/fakestore/products?limit=2", "FakeStore"),
        ("GET", "/api/quotes/random", "Quotes"),
        ("GET", "/api/lorem/text?paragraphs=1", "Lorem"),
        ("GET", "/api/lorempicsum/image?width=100&height=100", "Lorem Picsum"),
        ("GET", "/api/github/users/octocat", "GitHub"),
        ("GET", "/api/worldtime/timezone/Europe/Paris", "World Time"),
        ("GET", "/api/coincap/assets?limit=3", "CoinCap"),
        ("GET", "/api/tinyurl/shorten?url=https://example.com", "TinyURL"),
        ("GET", "/api/countries/name/france", "Countries"),
        ("GET", "/api/wikipedia/search?query=python&limit=1", "Wikipedia"),
        ("GET", "/api/ip/my-ip", "IP Geolocation"),
    ]
    
    results = []
    async with httpx.AsyncClient() as client:
        for method, path, name in tests:
            success, message = await test_endpoint(client, method, path, name)
            results.append((success, message))
            print(message)
            await asyncio.sleep(0.5)
    
    print("\n" + "="*70)
    passed = sum(1 for s, _ in results if s)
    print(f"[OK] Réussis: {passed}/{len(results)}")
    print("="*70 + "\n")

if __name__ == "__main__":
    print("="*70)
    print("   🔄 REDÉMARRAGE ET TEST DU SERVEUR")
    print("="*70)
    
    print("\n1️⃣ Arrêt de l'ancien serveur...")
    kill_server()
    
    print("\n2️⃣ Démarrage du nouveau serveur...")
    start_server()
    
    print("\n3️⃣ Vérification que le serveur est prêt...")
    for i in range(10):
        try:
            response = httpx.get("http://localhost:8000/api/health", timeout=2)
            if response.status_code == 200:
                print("[OK] Serveur prêt!")
                break
        except:
            pass
        time.sleep(1)
    else:
        print("[WARN]  Le serveur ne répond pas, mais on continue les tests...")
    
    print("\n4️⃣ Lancement des tests...")
    asyncio.run(run_tests())
    
    print("\n💡 Pour arrêter le serveur, utilisez Ctrl+C ou fermez la fenêtre")






