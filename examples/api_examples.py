#!/usr/bin/env python3
"""
Exemples d'utilisation de l'API
Démontre les nouvelles fonctionnalités v2.3.0
"""
import asyncio
import httpx
from typing import Dict, Any

BASE_URL = "http://localhost:8000"


async def example_1_health_checks():
    """Exemple 1: Health Checks"""
    print("\n" + "="*60)
    print("🏥 EXEMPLE 1: Health Checks")
    print("="*60)
    
    async with httpx.AsyncClient(timeout=10.0) as client:
        # Health check simple
        print("\n1. Health Check Simple:")
        response = await client.get(f"{BASE_URL}/api/health")
        if response.status_code == 200:
            print(f"   ✅ Status: {response.json().get('status')}")
        else:
            print(f"   ❌ Erreur: {response.status_code}")
        
        # Deep health check
        print("\n2. Deep Health Check:")
        response = await client.get(f"{BASE_URL}/api/health/deep")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Status global: {data.get('status')}")
            print(f"   ⏱️  Durée: {data.get('duration_ms')}ms")
            checks = data.get('checks', {})
            for name, check in checks.items():
                status = check.get('status', 'unknown')
                print(f"   - {name}: {status}")
        else:
            print(f"   ❌ Erreur: {response.status_code}")
        
        # Kubernetes readiness
        print("\n3. Kubernetes Readiness:")
        response = await client.get(f"{BASE_URL}/api/health/ready")
        print(f"   Status: {response.status_code} ({'Ready' if response.status_code == 200 else 'Not Ready'})")
        
        # Kubernetes liveness
        print("\n4. Kubernetes Liveness:")
        response = await client.get(f"{BASE_URL}/api/health/live")
        print(f"   Status: {response.status_code} ({'Alive' if response.status_code == 200 else 'Dead'})")


async def example_2_metrics():
    """Exemple 2: Métriques Prometheus"""
    print("\n" + "="*60)
    print("📊 EXEMPLE 2: Métriques")
    print("="*60)
    
    async with httpx.AsyncClient(timeout=10.0) as client:
        # Métriques JSON
        print("\n1. Métriques JSON:")
        response = await client.get(f"{BASE_URL}/api/metrics")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Uptime: {data.get('uptime_seconds')}s")
            print(f"   📈 Total requests: {data.get('total_requests')}")
            print(f"   ❌ Total errors: {sum(data.get('errors_by_type', {}).values())}")
        else:
            print(f"   ❌ Erreur: {response.status_code}")
        
        # Métriques Prometheus
        print("\n2. Métriques Prometheus:")
        response = await client.get(f"{BASE_URL}/api/metrics/prometheus")
        if response.status_code == 200:
            content = response.text
            lines = content.split('\n')[:10]  # Premières 10 lignes
            print("   Format Prometheus (extrait):")
            for line in lines:
                if line.strip():
                    print(f"   {line}")
        else:
            print(f"   ❌ Erreur: {response.status_code}")
        
        # Résumé
        print("\n3. Résumé des Métriques:")
        response = await client.get(f"{BASE_URL}/api/metrics/summary")
        if response.status_code == 200:
            data = response.json()
            print(f"   ⏱️  Uptime: {data.get('uptime_hours')}h")
            print(f"   📊 Error rate: {data.get('error_rate_percent')}%")
            print(f"   🏆 Top endpoints:")
            for endpoint, count in list(data.get('top_endpoints', {}).items())[:3]:
                print(f"      - {endpoint}: {count} requests")


async def example_3_request_tracing():
    """Exemple 3: Request Tracing (X-Request-ID)"""
    print("\n" + "="*60)
    print("🔍 EXEMPLE 3: Request Tracing")
    print("="*60)
    
    async with httpx.AsyncClient(timeout=10.0) as client:
        # Requête sans ID
        print("\n1. Requête sans Request ID (généré automatiquement):")
        response = await client.get(f"{BASE_URL}/api/health")
        request_id = response.headers.get("X-Request-ID")
        print(f"   ✅ Request ID généré: {request_id}")
        
        # Requête avec ID personnalisé
        print("\n2. Requête avec Request ID personnalisé:")
        custom_id = "my-custom-request-123"
        response = await client.get(
            f"{BASE_URL}/api/health",
            headers={"X-Request-ID": custom_id}
        )
        returned_id = response.headers.get("X-Request-ID")
        print(f"   ✅ Request ID retourné: {returned_id}")
        print(f"   {'✅ Match' if returned_id == custom_id else '❌ Mismatch'}")
        
        # Vérifier les headers de sécurité
        print("\n3. Security Headers:")
        security_headers = [
            "X-Content-Type-Options",
            "X-Frame-Options",
            "X-XSS-Protection",
            "Referrer-Policy",
            "X-API-Version"
        ]
        for header in security_headers:
            value = response.headers.get(header, "Non présent")
            print(f"   - {header}: {value}")


async def example_4_api_info():
    """Exemple 4: Informations API"""
    print("\n" + "="*60)
    print("ℹ️  EXEMPLE 4: Informations API")
    print("="*60)
    
    async with httpx.AsyncClient(timeout=10.0) as client:
        # Root endpoint
        print("\n1. Root Endpoint:")
        response = await client.get(f"{BASE_URL}/")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Name: {data.get('name')}")
            print(f"   📦 Version: {data.get('version')}")
            print(f"   🤖 AI Providers: {data.get('features', {}).get('ai_providers')}")
            print(f"   💾 Cache: {data.get('features', {}).get('cache')}")
        
        # Info détaillée
        print("\n2. Info Détaillée:")
        response = await client.get(f"{BASE_URL}/api/info")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Version: {data.get('version')}")
            print(f"   🌍 Environment: {data.get('environment')}")
            print(f"   🐍 Python: {data.get('python_version')}")
            print(f"   📊 Routes: {data.get('routes_count')}")
            
            features = data.get('features', {})
            ai = features.get('ai', {})
            print(f"   🤖 AI Providers disponibles: {ai.get('available_count')}")


async def example_5_error_handling():
    """Exemple 5: Gestion d'erreurs"""
    print("\n" + "="*60)
    print("⚠️  EXEMPLE 5: Gestion d'Erreurs")
    print("="*60)
    
    async with httpx.AsyncClient(timeout=10.0) as client:
        # Erreur 404
        print("\n1. Erreur 404 (endpoint inexistant):")
        response = await client.get(f"{BASE_URL}/api/nonexistent")
        print(f"   Status: {response.status_code}")
        if response.status_code == 404:
            data = response.json()
            print(f"   ✅ Error: {data.get('error')}")
            print(f"   🔍 Request ID: {data.get('request_id')}")
        
        # Erreur de validation
        print("\n2. Erreur de Validation (chat sans message):")
        response = await client.post(
            f"{BASE_URL}/api/chat",
            json={}  # Message manquant
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 422:
            data = response.json()
            print(f"   ✅ Validation Error détectée")
            print(f"   🔍 Request ID: {data.get('request_id')}")


async def example_6_performance():
    """Exemple 6: Performance (Response Time)"""
    print("\n" + "="*60)
    print("⚡ EXEMPLE 6: Performance")
    print("="*60)
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        # Mesurer le temps de réponse
        import time
        
        endpoints = [
            "/api/health",
            "/api/info",
            "/api/metrics/summary"
        ]
        
        print("\nTemps de réponse des endpoints:")
        for endpoint in endpoints:
            start = time.time()
            response = await client.get(f"{BASE_URL}{endpoint}")
            duration = (time.time() - start) * 1000
            
            response_time = response.headers.get("X-Response-Time", "N/A")
            print(f"   {endpoint}:")
            print(f"      - Temps mesuré: {duration:.1f}ms")
            print(f"      - Header X-Response-Time: {response_time}")
            print(f"      - Status: {response.status_code}")


async def main():
    """Exécuter tous les exemples"""
    print("\n" + "="*70)
    print("🚀 EXEMPLES D'UTILISATION - API v2.3.0")
    print("="*70)
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
        example_1_health_checks,
        example_2_metrics,
        example_3_request_tracing,
        example_4_api_info,
        example_5_error_handling,
        example_6_performance
    ]
    
    for example in examples:
        try:
            await example()
            await asyncio.sleep(1)  # Pause entre exemples
        except Exception as e:
            print(f"\n❌ Erreur dans {example.__name__}: {e}")
    
    print("\n" + "="*70)
    print("✅ EXEMPLES TERMINÉS")
    print("="*70)
    print("\n💡 Pour tester complètement:")
    print("   1. Vérifiez les logs du serveur pour voir les Request IDs")
    print("   2. Scrapez /api/metrics/prometheus avec Prometheus")
    print("   3. Utilisez /api/health/deep pour monitoring")
    print("   4. Vérifiez les security headers dans les réponses")


if __name__ == "__main__":
    asyncio.run(main())


<<<<<<< Updated upstream
=======





>>>>>>> Stashed changes
