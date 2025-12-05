# 🎬 Service Vidéo IA - Documentation Complète

## Vue d'ensemble

Le **Service Vidéo IA** permet de créer des vidéos avec des **avatars IA parlants** (alternative HeyGen). Il supporte plusieurs providers avec fallback automatique.

---

## 🚀 Fonctionnalités

### 1. Avatars Parlants
- Génération de vidéos avec avatars IA
- Support multi-langues
- Voix naturelles et réalistes

### 2. Text-to-Speech
- Coqui TTS (gratuit, local)
- ElevenLabs (si disponible)
- Multi-langues

### 3. Fallback Intelligent
- D-ID (payant, professionnel)
- Wav2Lip (gratuit, local - en développement)
- Fallback automatique si un provider échoue

---

## 📡 Endpoints

### POST `/api/video/avatar/create`

Créer une vidéo avec avatar parlant.

**Request Body:**
```json
{
  "text": "Bonjour, je suis un avatar IA qui parle !",
  "avatar_id": "anna",
  "voice_id": "fr-FR-DeniseNeural",
  "language": "fr",
  "use_free": false
}
```

**Response:**
```json
{
  "success": true,
  "video_id": "abc123",
  "status_url": "https://api.d-id.com/talks/abc123",
  "provider": "d-id",
  "message": "Vidéo en cours de génération. Utilisez /status pour vérifier."
}
```

### GET `/api/video/status/{video_id}`

Obtenir le statut d'une vidéo.

**Query Parameters:**
- `provider` (optionnel): Provider utilisé (d-id, wav2lip)

**Response:**
```json
{
  "video_id": "abc123",
  "status": "done",
  "result_url": "https://d-id.com/videos/abc123.mp4",
  "provider": "d-id",
  "created_at": "2024-12-04T10:00:00Z"
}
```

**Status possibles:**
- `processing`: Vidéo en cours de génération
- `done`: Vidéo prête
- `error`: Erreur lors de la génération

### POST `/api/video/audio/generate`

Générer audio à partir de texte (sans vidéo).

**Query Parameters:**
- `text` (required): Texte à convertir
- `language` (optionnel): Langue (fr, en, es)

**Response:**
```json
{
  "success": true,
  "audio_path": "/tmp/audio_123.wav",
  "provider": "coqui",
  "format": "wav"
}
```

### GET `/api/video/voices`

Obtenir les voix disponibles.

**Query Parameters:**
- `language` (optionnel): Filtrer par langue

**Response:**
```json
{
  "voices": [
    {
      "id": "coqui-fr",
      "name": "Coqui FR",
      "provider": "coqui"
    }
  ],
  "language": "fr",
  "total": 1
}
```

### GET `/api/video/status`

Statut du service vidéo.

**Response:**
```json
{
  "service": "Video AI",
  "available": true,
  "providers": ["d-id"],
  "d_id_available": true,
  "wav2lip_available": false,
  "tts_available": true
}
```

---

## 🎭 Avatars Disponibles (D-ID)

- `anna` - Avatar féminin
- `sara` - Avatar féminin
- `tom` - Avatar masculin
- Et plus...

Voir [D-ID Documentation](https://docs.d-id.com/) pour la liste complète.

---

## 🎤 Voix Disponibles

### Microsoft (D-ID)
- `fr-FR-DeniseNeural` - Français (féminin)
- `fr-FR-HenriNeural` - Français (masculin)
- `en-US-AriaNeural` - Anglais (féminin)
- `en-US-GuyNeural` - Anglais (masculin)
- `es-ES-ElviraNeural` - Espagnol (féminin)

### Coqui TTS
- Voix automatiques selon la langue

---

## ⚙️ Configuration

### Variables d'Environnement

```bash
# D-ID API Key (obligatoire pour D-ID)
DID_API_KEY=your_did_api_key_here

# ElevenLabs (optionnel)
ELEVENLABS_API_KEY=your_elevenlabs_key
```

### Installation Coqui TTS

```bash
pip install TTS
```

---

## 💡 Exemples d'Utilisation

### Exemple 1: Créer un avatar parlant
```python
import httpx

async def create_avatar():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/api/video/avatar/create",
            json={
                "text": "Bonjour ! Je suis un avatar IA.",
                "avatar_id": "anna",
                "voice_id": "fr-FR-DeniseNeural",
                "language": "fr"
            }
        )
        data = response.json()
        video_id = data["video_id"]
        print(f"Vidéo créée: {video_id}")
        return video_id
```

### Exemple 2: Vérifier le statut
```python
async def check_status(video_id: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"http://localhost:8000/api/video/status/{video_id}",
            params={"provider": "d-id"}
        )
        data = response.json()
        
        if data["status"] == "done":
            print(f"Vidéo prête: {data['result_url']}")
        else:
            print(f"Statut: {data['status']}")
```

### Exemple 3: Générer audio uniquement
```python
async def generate_audio():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/api/video/audio/generate",
            params={
                "text": "Bonjour, ceci est un test audio.",
                "language": "fr"
            }
        )
        data = response.json()
        print(f"Audio généré: {data['audio_path']}")
```

---

## 💰 Tarification

### D-ID
- **Coût**: 3$/100 vidéos (0.03€/vidéo)
- **Qualité**: Professionnelle
- **Temps**: 1-2 minutes par vidéo

### Wav2Lip (Gratuit)
- **Coût**: Gratuit (local)
- **Qualité**: Bonne
- **Temps**: Variable selon hardware

### Coqui TTS
- **Coût**: Gratuit
- **Qualité**: Bonne
- **Temps**: < 5 secondes

---

## 🐛 Dépannage

### "D-ID API key not configured"
- Ajouter `DID_API_KEY` dans `.env`
- Obtenir une clé sur [D-ID](https://www.d-id.com/)

### "Coqui TTS not available"
- Installer: `pip install TTS`
- Peut nécessiter des dépendances système

### Vidéo en "processing" longtemps
- Normal: génération prend 1-2 minutes
- Vérifier avec `/status` régulièrement

### Erreur 401 (Unauthorized)
- Vérifier que la clé D-ID est correcte
- Vérifier le format de l'authentification

---

## 🎓 Fonctionnalités Avancées

### Génération Cours Automatique
- `POST /api/video/course/generate` - Génère un cours complet avec IA
- Contenu généré automatiquement
- Vidéos pour chaque section
- Quiz interactif optionnel

### Cartes de Vœux
- `POST /api/video/greeting/create` - Crée une carte de vœux personnalisée
- Support pour: anniversaire, nouvel an, noël, mariage, diplôme
- Messages personnalisables
- Multi-langues

### Traduction Vidéo
- `POST /api/video/translate` - Traduit et crée vidéo dans autre langue
- `POST /api/video/translate/multiple` - Traduction multi-langues simultanée
- Voix automatiques selon langue
- Support 10+ langues

**Voir** : [examples/video_examples.py](../examples/video_examples.py) pour exemples complets

---

## 📈 Améliorations Futures

- [ ] Wav2Lip intégration complète
- [ ] CDN pour stockage vidéos
- [ ] Queue Redis pour scalabilité
- [ ] Webhooks pour notifications
- [ ] Compression vidéo

---

**Dernière mise à jour**: Décembre 2024  
**Version**: 1.0.0

