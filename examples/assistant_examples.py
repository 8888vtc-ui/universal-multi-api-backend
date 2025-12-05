"""
Exemples d'utilisation de l'Assistant Personnel IA
"""
import asyncio
import httpx
from typing import Dict, Any


BASE_URL = "http://localhost:8000"


async def example_1_learn_interaction():
    """Exemple 1: Apprendre d'une interaction"""
    print("\n" + "="*60)
    print("EXEMPLE 1: Apprendre d'une Interaction")
    print("="*60)
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            f"{BASE_URL}/api/assistant/learn",
            json={
                "user_id": "user123",
                "query": "bitcoin prix",
                "category": "finance",
                "action": "search",
                "feedback": "positive"
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n✅ Interaction apprise!")
            print(f"   Préférences mises à jour: {data.get('preferences_updated', False)}")
            print(f"   Total interactions: {data.get('total_interactions', 0)}")
        else:
            print(f"❌ Erreur: {response.status_code}")
            print(response.text)


async def example_2_get_recommendations():
    """Exemple 2: Obtenir recommandations"""
    print("\n" + "="*60)
    print("EXEMPLE 2: Recommandations Personnalisées")
    print("="*60)
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            f"{BASE_URL}/api/assistant/recommendations",
            params={
                "user_id": "user123",
                "limit": 5
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n✅ Recommandations générées!")
            print(f"   Total: {data.get('total', 0)}")
            
            for i, rec in enumerate(data.get('recommendations', [])[:3], 1):
                print(f"\n   {i}. {rec.get('category', 'unknown').upper()}")
                print(f"      Query: {rec.get('query', '')}")
                print(f"      Poids: {rec.get('weight', 0):.2f}")
                print(f"      Raison: {rec.get('reason', '')}")
                if rec.get('ai_suggestion'):
                    print(f"      💡 IA: {rec.get('ai_suggestion')}")
        else:
            print(f"❌ Erreur: {response.status_code}")


async def example_3_analyze_routine():
    """Exemple 3: Analyser routine"""
    print("\n" + "="*60)
    print("EXEMPLE 3: Analyser Routine")
    print("="*60)
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            f"{BASE_URL}/api/assistant/routine/analyze",
            params={
                "user_id": "user123",
                "days": 7
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('routine_analyzed'):
                analysis = data.get('analysis', {})
                print(f"\n✅ Routine analysée!")
                print(f"   Interactions totales: {analysis.get('total_interactions', 0)}")
                print(f"   Par jour: {analysis.get('interactions_per_day', 0):.1f}")
                print(f"   Heure active: {analysis.get('most_active_hour')}h")
                print(f"   Catégories: {', '.join(analysis.get('categories_used', {}).keys())}")
            else:
                print(f"⚠️  {data.get('message', 'Pas assez de données')}")
        else:
            print(f"❌ Erreur: {response.status_code}")


async def example_4_optimize_routine():
    """Exemple 4: Optimiser routine"""
    print("\n" + "="*60)
    print("EXEMPLE 4: Optimiser Routine")
    print("="*60)
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            f"{BASE_URL}/api/assistant/routine/optimize",
            params={"user_id": "user123"}
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('optimized'):
                print(f"\n✅ Routine optimisée!")
                print(f"   Temps économisé: {data.get('potential_time_saved_minutes', 0)} min")
                
                suggestions = data.get('suggestions', [])
                print(f"\n💡 Suggestions ({len(suggestions)}):")
                for i, sug in enumerate(suggestions[:3], 1):
                    print(f"   {i}. [{sug.get('impact', 'medium').upper()}] {sug.get('title', '')}")
                    print(f"      {sug.get('description', '')}")
            else:
                print(f"⚠️  {data.get('message', 'Impossible d\'optimiser')}")
        else:
            print(f"❌ Erreur: {response.status_code}")


async def example_5_execute_task():
    """Exemple 5: Exécuter tâche automatique"""
    print("\n" + "="*60)
    print("EXEMPLE 5: Exécuter Tâche Automatique")
    print("="*60)
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            f"{BASE_URL}/api/assistant/task/execute",
            params={
                "user_id": "user123",
                "task_type": "daily_summary"
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print(f"\n✅ Tâche exécutée!")
                print(f"   Type: {data.get('type', 'unknown')}")
                if data.get('summary'):
                    print(f"\n📝 Résumé:")
                    print(f"   {data.get('summary', '')[:200]}...")
            else:
                print(f"❌ Erreur: {data.get('error', 'Unknown')}")
        else:
            print(f"❌ Erreur: {response.status_code}")


async def example_6_get_profile():
    """Exemple 6: Obtenir profil utilisateur"""
    print("\n" + "="*60)
    print("EXEMPLE 6: Profil Utilisateur")
    print("="*60)
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            f"{BASE_URL}/api/assistant/profile/user123"
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n✅ Profil récupéré!")
            print(f"   User ID: {data.get('user_id', 'unknown')}")
            print(f"   Interactions: {data.get('total_interactions', 0)}")
            
            prefs = data.get('preferences', {})
            if prefs:
                print(f"\n📊 Préférences ({len(prefs)}):")
                for cat, info in list(prefs.items())[:3]:
                    if not cat.startswith("_"):
                        weight = info.get('weight', 0) if isinstance(info, dict) else 0
                        print(f"   - {cat}: {weight:.2f}")
        else:
            print(f"❌ Erreur: {response.status_code}")


async def example_7_get_available_tasks():
    """Exemple 7: Tâches disponibles"""
    print("\n" + "="*60)
    print("EXEMPLE 7: Tâches Disponibles")
    print("="*60)
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            f"{BASE_URL}/api/assistant/tasks/available"
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n✅ Tâches disponibles: {data.get('total', 0)}")
            
            for task in data.get('tasks', []):
                print(f"\n   📋 {task.get('name', 'Unknown')}")
                print(f"      ID: {task.get('id', '')}")
                print(f"      Description: {task.get('description', '')}")
        else:
            print(f"❌ Erreur: {response.status_code}")


async def main():
    """Exécuter tous les exemples"""
    print("\n" + "="*60)
    print("🤖 EXEMPLES - ASSISTANT PERSONNEL IA")
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
    await example_1_learn_interaction()
    await asyncio.sleep(1)
    
    await example_2_get_recommendations()
    await asyncio.sleep(1)
    
    await example_3_analyze_routine()
    await asyncio.sleep(1)
    
    await example_4_optimize_routine()
    await asyncio.sleep(1)
    
    await example_5_execute_task()
    await asyncio.sleep(1)
    
    await example_6_get_profile()
    await asyncio.sleep(1)
    
    await example_7_get_available_tasks()
    
    print("\n" + "="*60)
    print("✅ EXEMPLES TERMINÉS")
    print("="*60)
    print("\n💡 Pour tester complètement:")
    print("   1. Effectuez plusieurs interactions avec /learn")
    print("   2. Attendez quelques interactions pour voir les préférences se former")
    print("   3. Utilisez /recommendations pour voir les suggestions")


if __name__ == "__main__":
    asyncio.run(main())


