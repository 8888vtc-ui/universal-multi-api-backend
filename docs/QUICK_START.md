# ⚡ Guide de Démarrage Rapide

## Installation en 5 minutes

### 1. Prérequis
```bash
# Vérifier Python
python --version  # Doit être 3.10+

# Installer Git si nécessaire
```

### 2. Installation
```bash
# Cloner (ou télécharger)
cd backend

# Créer environnement virtuel
python -m venv venv

# Activer
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Installer dépendances
pip install -r requirements.txt
```

### 3. Configuration minimale
Créer `.env` :
```env
# Minimum requis (optionnel, fonctionne sans)
GROQ_API_KEY=your_key_here
```

### 4. Lancer
```bash
python main.py
```

✅ **C'est tout !** Le serveur est sur `http://localhost:8000`

---

## Premiers Pas

### 1. Vérifier que ça fonctionne
```bash
curl http://localhost:8000/api/health
```

### 2. Voir la documentation
Ouvrir dans le navigateur :
```
http://localhost:8000/docs
```

### 3. Tester un endpoint
```bash
# Chat avec IA
curl -X POST "http://localhost:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Bonjour!", "language": "fr"}'
```

---

## Endpoints Essentiels

### Health Check
```
GET /api/health
```

### Chat IA
```
POST /api/chat
{
  "message": "Votre message",
  "language": "fr"
}
```

### Recherche Universelle
```
POST /api/search/universal
{
  "query": "bitcoin prix",
  "max_results_per_category": 5
}
```

### Analytics
```
GET /api/analytics/dashboard?days=7
```

---

## Configuration Recommandée

Pour utiliser toutes les fonctionnalités, ajouter dans `.env` :

```env
# AI Providers (au moins un)
GROQ_API_KEY=your_key
MISTRAL_API_KEY=your_key
GEMINI_API_KEY=your_key

# External APIs (optionnel)
NEWS_API_KEY=your_key
WEATHER_API_KEY=your_key
D_ID_API_KEY=your_key

# Cache (optionnel mais recommandé)
REDIS_URL=redis://localhost:6379
```

---

## Problèmes Courants

### Port déjà utilisé
```bash
# Changer le port dans main.py ou :
uvicorn main:app --port 8001
```

### Module non trouvé
```bash
# Réinstaller dépendances
pip install -r requirements.txt --force-reinstall
```

### Erreur Redis
⚠️ Normal si Redis n'est pas installé. Le cache sera désactivé.

---

## Prochaines Étapes

1. ✅ Lire [DEPLOYMENT.md](DEPLOYMENT.md) pour déploiement
2. ✅ Explorer [README.md](../README.md) pour fonctionnalités
3. ✅ Voir [docs/](../docs/) pour documentation complète

---

**Besoin d'aide ?** Voir la documentation complète dans `docs/`


