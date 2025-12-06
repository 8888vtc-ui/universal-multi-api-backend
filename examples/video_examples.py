"""
Exemples d'utilisation du Service Vidéo IA
"""
import asyncio
import httpx
from typing import Dict, Any


BASE_URL = "http://localhost:8000"


async def example_1_create_avatar():
    """Exemple 1: Créer un avatar parlant simple"""
    print("\n" + "="*60)
    print("EXEMPLE 1: Créer Avatar Parlant")
    print("="*60)
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            f"{BASE_URL}/api/video/avatar/create",
            json={
                "text": "Bonjour ! Je suis un avatar IA qui parle français.",
                "avatar_id": "anna",
                "voice_id": "fr-FR-DeniseNeural",
                "language": "fr"
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n✅ Vidéo créée!")
            print(f"   Video ID: {data['video_id']}")
            print(f"   Provider: {data['provider']}")
            print(f"   Temps estimé: {data.get('estimated_time_seconds', 120)}s")
            print(f"\n💡 Utilisez /api/video/status/{data['video_id']} pour vérifier")
            return data['video_id']
        else:
            print(f"❌ Erreur: {response.status_code}")
            print(response.text)
            return None


async def example_2_check_status(video_id: str):
    """Exemple 2: Vérifier le statut d'une vidéo"""
    print("\n" + "="*60)
    print("EXEMPLE 2: Vérifier Statut Vidéo")
    print("="*60)
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            f"{BASE_URL}/api/video/status/{video_id}",
            params={"provider": "d-id"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n📊 Statut: {data['status']}")
            if data['status'] == "done":
                print(f"✅ Vidéo prête!")
                print(f"   URL: {data['result_url']}")
            elif data['status'] == "processing":
                print(f"⏳ En cours de génération...")
            else:
                print(f"❌ Erreur: {data.get('status')}")
        else:
            print(f"❌ Erreur: {response.status_code}")


async def example_3_generate_course():
    """Exemple 3: Générer un cours automatiquement"""
    print("\n" + "="*60)
    print("EXEMPLE 3: Générer Cours Automatique")
    print("="*60)
    
    async with httpx.AsyncClient(timeout=300.0) as client:  # 5 min timeout
        response = await client.post(
            f"{BASE_URL}/api/video/course/generate",
            params={
                "topic": "Python basics",
                "duration_minutes": 3,
                "language": "fr",
                "avatar_id": "anna",
                "include_quiz": True
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n✅ Cours généré!")
            print(f"   Topic: {data['topic']}")
            print(f"   Sections: {data['total_sections']}")
            print(f"   Quiz: {'Oui' if data.get('quiz') else 'Non'}")
            
            if data.get('sections'):
                print(f"\n📚 Sections créées:")
                for i, section in enumerate(data['sections'][:3], 1):
                    if section.get('video'):
                        print(f"   {i}. {section['section'].get('title', 'Section')} - Video ID: {section['video'].get('video_id')}")
        else:
            print(f"❌ Erreur: {response.status_code}")
            print(response.text)


async def example_4_create_greeting():
    """Exemple 4: Créer une carte de vœux"""
    print("\n" + "="*60)
    print("EXEMPLE 4: Carte de Vœux")
    print("="*60)
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            f"{BASE_URL}/api/video/greeting/create",
            params={
                "occasion": "birthday",
                "recipient_name": "Marie",
                "sender_name": "Jean",
                "message": "Que cette nouvelle année soit remplie de bonheur !",
                "language": "fr",
                "avatar_id": "anna"
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n✅ Carte de vœux créée!")
            print(f"   Occasion: {data['occasion']}")
            print(f"   Pour: {data['recipient']}")
            print(f"   De: {data['sender']}")
            print(f"   Message: {data['message']}")
            print(f"   Video ID: {data['video_id']}")
        else:
            print(f"❌ Erreur: {response.status_code}")


async def example_5_translate_video():
    """Exemple 5: Traduire une vidéo"""
    print("\n" + "="*60)
    print("EXEMPLE 5: Traduire Vidéo")
    print("="*60)
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            f"{BASE_URL}/api/video/translate",
            params={
                "text": "Hello, how are you?",
                "target_language": "fr",
                "source_language": "en",
                "avatar_id": "anna"
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n✅ Vidéo traduite!")
            print(f"   Original: {data['original_text']}")
            print(f"   Traduit: {data['translated_text']}")
            print(f"   Langue source: {data['source_language']}")
            print(f"   Langue cible: {data['target_language']}")
            print(f"   Video ID: {data['video_id']}")
        else:
            print(f"❌ Erreur: {response.status_code}")


async def example_6_translate_multiple():
    """Exemple 6: Traduire dans plusieurs langues"""
    print("\n" + "="*60)
    print("EXEMPLE 6: Traduction Multi-Langues")
    print("="*60)
    
    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(
            f"{BASE_URL}/api/video/translate/multiple",
            params={
                "text": "Welcome to our service!",
                "languages": "fr,en,es",
                "avatar_id": "anna"
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n✅ Traductions créées!")
            print(f"   Original: {data['original_text']}")
            print(f"   Langues: {data['total_languages']}")
            print(f"   Réussies: {data['successful']}")
            
            for lang, video_data in data['videos'].items():
                if video_data.get('success'):
                    print(f"\n   {lang.upper()}:")
                    print(f"      Texte: {video_data.get('translated_text', '')[:50]}...")
                    print(f"      Video ID: {video_data.get('video_id')}")
        else:
            print(f"❌ Erreur: {response.status_code}")


async def example_7_service_status():
    """Exemple 7: Statut du service"""
    print("\n" + "="*60)
    print("EXEMPLE 7: Statut Service")
    print("="*60)
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(f"{BASE_URL}/api/video/status")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n📊 Statut Service Vidéo:")
            print(f"   Disponible: {'Oui' if data['available'] else 'Non'}")
            print(f"   Providers: {', '.join(data.get('providers', []))}")
            print(f"   D-ID: {'Oui' if data.get('d_id_available') else 'Non'}")
            print(f"   TTS: {'Oui' if data.get('tts_available') else 'Non'}")
            
            if 'queue' in data:
                print(f"\n📋 Queue:")
                print(f"   Total: {data['queue']['total']}")
                print(f"   Par statut: {data['queue']['by_status']}")
            
            if 'storage' in data:
                print(f"\n💾 Stockage:")
                print(f"   Vidéos: {data['storage']['total_videos']}")
                print(f"   Taille: {data['storage']['total_size_mb']} MB")
        else:
            print(f"❌ Erreur: {response.status_code}")


async def main():
    """Exécuter tous les exemples"""
    print("\n" + "="*60)
    print("🎬 EXEMPLES - SERVICE VIDÉO IA")
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
    
    # Exemples qui nécessitent une clé API D-ID
    print("⚠️  Note: Certains exemples nécessitent une clé API D-ID configurée")
    print("   Ajoutez DID_API_KEY dans votre .env\n")
    
    # Exemples simples (sans API key)
    await example_7_service_status()
    await example_4_create_greeting()  # Génère juste le texte
    
    # Exemples avec API (nécessitent clé D-ID)
    # video_id = await example_1_create_avatar()
    # if video_id:
    #     await asyncio.sleep(2)
    #     await example_2_check_status(video_id)
    
    print("\n" + "="*60)
    print("✅ EXEMPLES TERMINÉS")
    print("="*60)
    print("\n💡 Pour tester avec D-ID:")
    print("   1. Obtenez une clé sur https://www.d-id.com/")
    print("   2. Ajoutez DID_API_KEY dans .env")
    print("   3. Relancez les exemples")


if __name__ == "__main__":
    asyncio.run(main())



