#!/usr/bin/env python3
"""
Script de Test Manuel des Endpoints
Teste tous les endpoints critiques manuellement
"""
import asyncio
import sys
import os
from pathlib import Path
import json

# Ajouter le répertoire parent au path
sys.path.insert(0, str(Path(__file__).parent.parent))

import httpx
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("API_URL", "http://localhost:8000")

# Colors
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"
RESET = "\033[0m"
BOLD = "\033[1m"

def print_success(msg):
    print(f"{GREEN}✅ {msg}{RESET}")

def print_error(msg):
    print(f"{RED}❌ {msg}{RESET}")

def print_info(msg):
    print(f"{BLUE}ℹ️  {msg}{RESET}")

def print_section(msg):
    print(f"\n{CYAN}{BOLD}{'='*70}{RESET}")
    print(f"{CYAN}{BOLD}{msg}{RESET}")
    print(f"{CYAN}{BOLD}{'='*70}{RESET}\n")


async def test_endpoint(method: str, endpoint: str, data: dict = None, expected_status: int = 200):
    """Tester un endpoint"""
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            if method == "GET":
                response = await client.get(f"{BASE_URL}{endpoint}")
            elif method == "POST":
                response = await client.post(f"{BASE_URL}{endpoint}", json=data)
            else:
                return False, f"Méthode {method} non supportée"
            
            success = response.status_code == expected_status
            try:
                response_data = response.json() if response.headers.get("content-type", "").startswith("application/json") else response.text
            except:
                response_data = response.text[:200]
            
            return success, response_data, response.status_code
        except Exception as e:
            return False, str(e), 0


async def main():
    """Fonction principale"""
    print_section("🧪 TESTS MANUELS DES ENDPOINTS")
    
    # Vérifier que le serveur est accessible
    print_info("Vérification du serveur...")
    success, _, status = await test_endpoint("GET", "/api/health")
    if not success:
        print_error(f"Le serveur n'est pas accessible (Status: {status})")
        print_info("Démarrez le serveur avec: cd backend && python scripts/start_server.py")
        return 1
    
    print_success("Serveur accessible !\n")
    
    # Tests des endpoints
    tests = [
        # Health & Status
        ("GET", "/", "Root endpoint"),
        ("GET", "/api/health", "Health check"),
        ("GET", "/api/health/deep", "Deep health"),
        ("GET", "/api/health/ready", "Kubernetes ready"),
        ("GET", "/api/health/live", "Kubernetes live"),
        
        # Info
        ("GET", "/api/info", "API Info"),
        
        # Metrics
        ("GET", "/api/metrics", "Metrics JSON"),
        ("GET", "/api/metrics/prometheus", "Metrics Prometheus"),
        ("GET", "/api/metrics/summary", "Metrics Summary"),
        
        # Chat (si disponible) - language doit être "he" ou "en"
        ("POST", "/api/chat", "Chat IA", {"message": "Hello, how are you?", "language": "en"}),
        
        # Finance (si disponible) - endpoint correct
        ("GET", "/api/finance/stock/quote/AAPL", "Finance Quote"),
        
        # Search (si disponible) - POST avec body
        ("POST", "/api/search/universal", "Universal Search", {"query": "test", "categories": ["news"], "max_results_per_category": 3}),
    ]
    
    results = []
    
    for test in tests:
        if len(test) == 3:
            method, endpoint, name = test
            data = None
            expected = 200
        elif len(test) == 4:
            method, endpoint, name, data = test
            expected = 200
        else:
            method, endpoint, name, data, expected = test
        
        print(f"Test: {name}...", end=" ")
        success, response_data, status = await test_endpoint(method, endpoint, data, expected)
        
        if success:
            print_success("OK")
            if isinstance(response_data, dict):
                # Afficher un résumé
                if "version" in response_data:
                    print_info(f"  Version: {response_data.get('version')}")
                if "status" in response_data:
                    print_info(f"  Status: {response_data.get('status')}")
                if "environment" in response_data:
                    print_info(f"  Environment: {response_data.get('environment')}")
            results.append((name, True, ""))
        else:
            if status == 503:
                print(f"{YELLOW}⚠️  Service unavailable{RESET}")
                results.append((name, False, "Service unavailable"))
            elif status == 404:
                print_error(f"Not found (404)")
                results.append((name, False, "Not found"))
            else:
                print_error(f"Failed (Status: {status})")
                error_msg = str(response_data)[:100] if response_data else "Unknown error"
                results.append((name, False, error_msg))
    
    # Résumé
    print_section("📊 RÉSUMÉ DES TESTS")
    
    passed = sum(1 for _, success, _ in results if success)
    failed = len(results) - passed
    
    print(f"Total: {len(results)} tests")
    print_success(f"Réussis: {passed}")
    if failed > 0:
        print_error(f"Échoués: {failed}")
    
    print("\nDétail:")
    for name, success, error in results:
        if success:
            print_success(f"  {name}")
        else:
            print_error(f"  {name}: {error}")
    
    # URLs utiles
    print_section("🔗 URLS UTILES")
    print_info(f"📚 Documentation: {BASE_URL}/docs")
    print_info(f"📖 ReDoc: {BASE_URL}/redoc")
    print_info(f"❤️  Health: {BASE_URL}/api/health")
    print_info(f"📊 Metrics: {BASE_URL}/api/metrics")
    
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)

