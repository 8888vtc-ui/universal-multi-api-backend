# 🎬 Service Vidéo IA - Architecture Technique

## Structure des Fichiers

```
services/video/
├── __init__.py
├── did_provider.py      # Provider D-ID (avatars parlants)
├── tts_provider.py      # Text-to-Speech (Coqui, ElevenLabs)
├── video_router.py      # Router avec fallback intelligent
├── queue_manager.py     # Gestion queue asynchrone
└── storage_manager.py   # Stockage temporaire vidéos
```

## Composants

### 1. DIDProvider
- Intégration API D-ID
- Authentification Basic Auth
- Création vidéos avatars parlants
- Vérification statut

### 2. TTSProvider
- Coqui TTS (gratuit, local)
- ElevenLabs (si disponible)
- Génération audio à partir de texte

### 3. VideoRouter
- Fallback automatique entre providers
- Gestion intelligente des providers
- Support multi-langues

### 4. VideoQueue
- Queue en mémoire pour suivi générations
- Nettoyage automatique (24h)
- Statistiques de queue

### 5. VideoStorage
- Stockage local vidéos temporaires
- Nettoyage automatique après 24h
- Métadonnées JSON

## Flux de Génération

1. **Requête** → `POST /api/video/avatar/create`
2. **Validation** → Texte, avatar, voix
3. **Création** → Appel provider (D-ID)
4. **Queue** → Ajout à la queue (status: processing)
5. **Background** → Vérification statut périodique
6. **Stockage** → Sauvegarde URL quand terminé
7. **Statut** → `GET /api/video/status/{video_id}`

## Configuration

### Variables d'Environnement
```bash
DID_API_KEY=your_key_here
ELEVENLABS_API_KEY=your_key_here  # Optionnel
```

### Stockage
- **Chemin**: `./storage/videos/`
- **TTL**: 24 heures
- **Nettoyage**: Automatique ou manuel via `/cleanup`

## Limitations

- **Queue max**: 100 vidéos simultanées
- **Texte max**: 500 caractères
- **Stockage**: Local uniquement (pas de CDN)
- **Wav2Lip**: En développement

## Améliorations Futures

- [ ] Wav2Lip intégration complète
- [ ] CDN pour stockage vidéos
- [ ] Queue Redis pour scalabilité
- [ ] Webhooks pour notifications
- [ ] Compression vidéo


<<<<<<< Updated upstream
=======





>>>>>>> Stashed changes
