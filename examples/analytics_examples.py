"""
Exemples d'utilisation du Service Analytics
"""
import asyncio
import httpx
from typing import Dict, Any


BASE_URL = "http://localhost:8000"


async def example_1_get_metrics():
    """Exemple 1: Obtenir métriques"""
    print("\n" + "="*60)
    print("EXEMPLE 1: Métriques d'Utilisation")
    print("="*60)
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            f"{BASE_URL}/api/analytics/metrics",
            params={"days": 7}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n✅ Métriques récupérées!")
            print(f"   Période: {data.get('period_days')} jours")
            print(f"   Total requêtes: {data.get('total_requests', 0)}")
            print(f"   Temps réponse moyen: {data.get('avg_response_time_ms', 0)} ms")
            print(f"   Requêtes/jour: {data.get('requests_per_day', 0):.1f}")
            
            print(f"\n📊 Codes de statut:")
            for code, count in list(data.get('status_codes', {}).items())[:5]:
                print(f"   {code}: {count}")
            
            print(f"\n🔝 Top Endpoints:")
            for endpoint, count in list(data.get('endpoints', {}).items())[:5]:
                print(f"   {endpoint}: {count}")
        else:
            print(f"❌ Erreur: {response.status_code}")


async def example_2_get_errors():
    """Exemple 2: Obtenir erreurs"""
    print("\n" + "="*60)
    print("EXEMPLE 2: Statistiques d'Erreurs")
    print("="*60)
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            f"{BASE_URL}/api/analytics/errors",
            params={"days": 7}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n✅ Erreurs récupérées!")
            print(f"   Total erreurs: {data.get('total_errors', 0)}")
            print(f"   Erreurs/jour: {data.get('errors_per_day', 0):.1f}")
            
            print(f"\n⚠️  Types d'erreurs:")
            for error_type, count in list(data.get('error_types', {}).items())[:5]:
                print(f"   {error_type}: {count}")
            
            print(f"\n🔴 Endpoints avec erreurs:")
            for endpoint, count in list(data.get('error_endpoints', {}).items())[:5]:
                print(f"   {endpoint}: {count}")
        else:
            print(f"❌ Erreur: {response.status_code}")


async def example_3_get_top_endpoints():
    """Exemple 3: Top endpoints"""
    print("\n" + "="*60)
    print("EXEMPLE 3: Top Endpoints")
    print("="*60)
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            f"{BASE_URL}/api/analytics/endpoints/top",
            params={"days": 7, "limit": 10}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n✅ Top endpoints récupérés!")
            print(f"   Total: {data.get('total', 0)}")
            
            for i, endpoint in enumerate(data.get('endpoints', [])[:5], 1):
                print(f"\n   {i}. {endpoint.get('endpoint', 'unknown')}")
                print(f"      Requêtes: {endpoint.get('requests', 0)}")
                print(f"      Pourcentage: {endpoint.get('percentage', 0):.1f}%")
        else:
            print(f"❌ Erreur: {response.status_code}")


async def example_4_get_performance():
    """Exemple 4: Performance"""
    print("\n" + "="*60)
    print("EXEMPLE 4: Statistiques de Performance")
    print("="*60)
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            f"{BASE_URL}/api/analytics/performance",
            params={"days": 7}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n✅ Performance récupérée!")
            print(f"   Temps réponse moyen: {data.get('avg_response_time_ms', 0)} ms")
            print(f"   Temps réponse min: {data.get('min_response_time_ms', 0)} ms")
            print(f"   Temps réponse max: {data.get('max_response_time_ms', 0)} ms")
            print(f"   Total requêtes: {data.get('total_requests', 0)}")
        else:
            print(f"❌ Erreur: {response.status_code}")


async def example_5_get_dashboard():
    """Exemple 5: Dashboard complet"""
    print("\n" + "="*60)
    print("EXEMPLE 5: Dashboard Complet")
    print("="*60)
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            f"{BASE_URL}/api/analytics/dashboard",
            params={"days": 7}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n✅ Dashboard récupéré!")
            
            summary = data.get('summary', {})
            print(f"\n📊 Résumé:")
            print(f"   Total requêtes: {summary.get('total_requests', 0)}")
            print(f"   Total erreurs: {summary.get('total_errors', 0)}")
            print(f"   Taux d'erreur: {summary.get('error_rate', 0):.2f}%")
            print(f"   Temps réponse moyen: {summary.get('avg_response_time_ms', 0)} ms")
            
            top_endpoints = data.get('top_endpoints', [])
            if top_endpoints:
                print(f"\n🔝 Top 3 Endpoints:")
                for i, endpoint in enumerate(top_endpoints[:3], 1):
                    print(f"   {i}. {endpoint.get('endpoint', 'unknown')}: {endpoint.get('requests', 0)} requêtes")
        else:
            print(f"❌ Erreur: {response.status_code}")


async def example_6_health_check():
    """Exemple 6: Health check"""
    print("\n" + "="*60)
    print("EXEMPLE 6: Health Check Analytics")
    print("="*60)
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            f"{BASE_URL}/api/analytics/health"
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n✅ Health check réussi!")
            print(f"   Statut: {data.get('status', 'unknown')}")
            print(f"   Base de données: {data.get('database', 'unknown')}")
            print(f"   Requêtes aujourd'hui: {data.get('total_requests_today', 0)}")
        else:
            print(f"❌ Erreur: {response.status_code}")


async def main():
    """Exécuter tous les exemples"""
    print("\n" + "="*60)
    print("📊 EXEMPLES - ANALYTICS & MONITORING")
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
    
    # Exemples
    await example_6_health_check()
    await asyncio.sleep(1)
    
    await example_1_get_metrics()
    await asyncio.sleep(1)
    
    await example_2_get_errors()
    await asyncio.sleep(1)
    
    await example_3_get_top_endpoints()
    await asyncio.sleep(1)
    
    await example_4_get_performance()
    await asyncio.sleep(1)
    
    await example_5_get_dashboard()
    
    print("\n" + "="*60)
    print("✅ EXEMPLES TERMINÉS")
    print("="*60)
    print("\n💡 Pour voir des données:")
    print("   1. Effectuez quelques requêtes sur l'API")
    print("   2. Attendez quelques secondes")
    print("   3. Relancez les exemples pour voir les métriques")


if __name__ == "__main__":
    asyncio.run(main())



