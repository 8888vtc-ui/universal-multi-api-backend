#!/usr/bin/env python3
"""
Script de Test Complet
Teste tous les aspects du backend
"""
import asyncio
import sys
import os
from pathlib import Path
from datetime import datetime

# Ajouter le répertoire parent au path
sys.path.insert(0, str(Path(__file__).parent.parent))

import httpx
from typing import Dict, List, Tuple

BASE_URL = os.getenv("API_URL", "http://localhost:8000")

# Colors
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"

def print_success(msg):
    print(f"{GREEN}✅ {msg}{RESET}")

def print_error(msg):
    print(f"{RED}❌ {msg}{RESET}")

def print_warning(msg):
    print(f"{YELLOW}⚠️  {msg}{RESET}")

def print_info(msg):
    print(f"{BLUE}ℹ️  {msg}{RESET}")


class TestRunner:
    """Runner de tests complet"""
    
    def __init__(self):
        self.results: List[Tuple[str, bool, str]] = []
        self.start_time = datetime.now()
    
    async def check_server(self) -> bool:
        """Vérifier que le serveur est accessible"""
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{BASE_URL}/api/health")
                if response.status_code == 200:
                    return True
        except:
            pass
        return False
    
    async def test_health_endpoints(self):
        """Tester les endpoints de health"""
        print("\n" + "="*60)
        print("🏥 TEST: Health Endpoints")
        print("="*60)
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            # Health simple
            try:
                response = await client.get(f"{BASE_URL}/api/health")
                if response.status_code == 200:
                    print_success("Health check simple: OK")
                    self.results.append(("Health Simple", True, ""))
                else:
                    print_error(f"Health check: {response.status_code}")
                    self.results.append(("Health Simple", False, f"Status {response.status_code}"))
            except Exception as e:
                print_error(f"Health check: {e}")
                self.results.append(("Health Simple", False, str(e)))
            
            # Deep health
            try:
                response = await client.get(f"{BASE_URL}/api/health/deep")
                if response.status_code == 200:
                    data = response.json()
                    status = data.get("status", "unknown")
                    print_success(f"Deep health: {status}")
                    self.results.append(("Deep Health", True, status))
                else:
                    print_error(f"Deep health: {response.status_code}")
                    self.results.append(("Deep Health", False, f"Status {response.status_code}"))
            except Exception as e:
                print_error(f"Deep health: {e}")
                self.results.append(("Deep Health", False, str(e)))
            
            # Kubernetes probes
            for probe in ["ready", "live"]:
                try:
                    response = await client.get(f"{BASE_URL}/api/health/{probe}")
                    if response.status_code in [200, 503]:
                        print_success(f"Kubernetes {probe}: OK")
                        self.results.append((f"K8s {probe}", True, ""))
                    else:
                        print_warning(f"Kubernetes {probe}: {response.status_code}")
                        self.results.append((f"K8s {probe}", False, f"Status {response.status_code}"))
                except Exception as e:
                    print_error(f"Kubernetes {probe}: {e}")
                    self.results.append((f"K8s {probe}", False, str(e)))
    
    async def test_metrics_endpoints(self):
        """Tester les endpoints de métriques"""
        print("\n" + "="*60)
        print("📊 TEST: Metrics Endpoints")
        print("="*60)
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            endpoints = [
                ("/api/metrics", "JSON"),
                ("/api/metrics/prometheus", "Prometheus"),
                ("/api/metrics/summary", "Summary")
            ]
            
            for endpoint, name in endpoints:
                try:
                    response = await client.get(f"{BASE_URL}{endpoint}")
                    if response.status_code == 200:
                        print_success(f"{name} metrics: OK")
                        self.results.append((f"Metrics {name}", True, ""))
                    else:
                        print_error(f"{name} metrics: {response.status_code}")
                        self.results.append((f"Metrics {name}", False, f"Status {response.status_code}"))
                except Exception as e:
                    print_error(f"{name} metrics: {e}")
                    self.results.append((f"Metrics {name}", False, str(e)))
    
    async def test_security_headers(self):
        """Tester les security headers"""
        print("\n" + "="*60)
        print("🔐 TEST: Security Headers")
        print("="*60)
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                response = await client.get(f"{BASE_URL}/api/health")
                
                required_headers = [
                    "X-Content-Type-Options",
                    "X-Frame-Options",
                    "X-XSS-Protection",
                    "Referrer-Policy",
                    "X-API-Version",
                    "X-Request-ID"
                ]
                
                missing = []
                for header in required_headers:
                    if header not in response.headers:
                        missing.append(header)
                
                if not missing:
                    print_success("Tous les security headers présents")
                    self.results.append(("Security Headers", True, ""))
                else:
                    print_warning(f"Headers manquants: {', '.join(missing)}")
                    self.results.append(("Security Headers", False, f"Manquants: {missing}"))
            except Exception as e:
                print_error(f"Security headers: {e}")
                self.results.append(("Security Headers", False, str(e)))
    
    async def test_api_endpoints(self):
        """Tester les endpoints API principaux"""
        print("\n" + "="*60)
        print("🔌 TEST: API Endpoints")
        print("="*60)
        
        async with httpx.AsyncClient(timeout=15.0) as client:
            # Root endpoint
            try:
                response = await client.get(f"{BASE_URL}/")
                if response.status_code == 200:
                    data = response.json()
                    print_success(f"Root endpoint: {data.get('name')} v{data.get('version')}")
                    self.results.append(("Root Endpoint", True, ""))
                else:
                    print_error(f"Root endpoint: {response.status_code}")
                    self.results.append(("Root Endpoint", False, f"Status {response.status_code}"))
            except Exception as e:
                print_error(f"Root endpoint: {e}")
                self.results.append(("Root Endpoint", False, str(e)))
            
            # API info
            try:
                response = await client.get(f"{BASE_URL}/api/info")
                if response.status_code == 200:
                    data = response.json()
                    print_success(f"API Info: {data.get('version')} ({data.get('environment')})")
                    self.results.append(("API Info", True, ""))
                else:
                    print_error(f"API Info: {response.status_code}")
                    self.results.append(("API Info", False, f"Status {response.status_code}"))
            except Exception as e:
                print_error(f"API Info: {e}")
                self.results.append(("API Info", False, str(e)))
            
            # Chat (si AI providers disponibles)
            try:
                response = await client.post(
                    f"{BASE_URL}/api/chat",
                    json={"message": "Hello", "language": "en"},
                    timeout=30.0
                )
                if response.status_code == 200:
                    print_success("Chat endpoint: OK")
                    self.results.append(("Chat Endpoint", True, ""))
                elif response.status_code == 503:
                    print_warning("Chat endpoint: Service unavailable (pas de providers AI)")
                    self.results.append(("Chat Endpoint", False, "No AI providers"))
                else:
                    print_error(f"Chat endpoint: {response.status_code}")
                    self.results.append(("Chat Endpoint", False, f"Status {response.status_code}"))
            except Exception as e:
                print_warning(f"Chat endpoint: {e}")
                self.results.append(("Chat Endpoint", False, str(e)))
    
    async def test_error_handling(self):
        """Tester la gestion d'erreurs"""
        print("\n" + "="*60)
        print("⚠️  TEST: Error Handling")
        print("="*60)
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            # 404
            try:
                response = await client.get(f"{BASE_URL}/api/nonexistent")
                if response.status_code == 404:
                    data = response.json()
                    if "request_id" in data:
                        print_success("404 avec request_id: OK")
                        self.results.append(("Error 404", True, ""))
                    else:
                        print_warning("404 sans request_id")
                        self.results.append(("Error 404", False, "No request_id"))
                else:
                    print_warning(f"404 test: {response.status_code}")
                    self.results.append(("Error 404", False, f"Status {response.status_code}"))
            except Exception as e:
                print_error(f"404 test: {e}")
                self.results.append(("Error 404", False, str(e)))
    
    def print_summary(self):
        """Afficher le résumé des tests"""
        print("\n" + "="*60)
        print("📊 RÉSUMÉ DES TESTS")
        print("="*60)
        
        total = len(self.results)
        passed = sum(1 for _, success, _ in self.results if success)
        failed = total - passed
        
        print(f"\nTotal: {total} tests")
        print_success(f"Réussis: {passed}")
        if failed > 0:
            print_error(f"Échoués: {failed}")
        
        print("\nDétail:")
        for name, success, error in self.results:
            if success:
                print_success(f"  {name}")
            else:
                print_error(f"  {name}: {error}")
        
        duration = (datetime.now() - self.start_time).total_seconds()
        print(f"\n⏱️  Durée: {duration:.2f}s")
        
        if failed == 0:
            print_success("\n🎉 Tous les tests sont passés !")
            return 0
        else:
            print_warning(f"\n⚠️  {failed} test(s) ont échoué")
            return 1


async def main():
    """Fonction principale"""
    print("\n" + "="*70)
    print("🧪 TESTS COMPLETS - Universal Multi-API Backend v2.3.0")
    print("="*70)
    
    runner = TestRunner()
    
    # Vérifier que le serveur est accessible
    print("\n🔍 Vérification du serveur...")
    if not await runner.check_server():
        print_error(f"Le serveur n'est pas accessible sur {BASE_URL}")
        print_info("Démarrez le serveur avec: cd backend && python main.py")
        return 1
    
    print_success(f"Serveur accessible sur {BASE_URL}")
    
    # Exécuter tous les tests
    await runner.test_health_endpoints()
    await runner.test_metrics_endpoints()
    await runner.test_security_headers()
    await runner.test_api_endpoints()
    await runner.test_error_handling()
    
    # Résumé
    return runner.print_summary()


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
