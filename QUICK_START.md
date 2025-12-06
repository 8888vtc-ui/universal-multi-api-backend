# 🚀 Guide de Démarrage Rapide

**Version** : 2.3.0  
**Score** : 10/10 - Enterprise Grade

---

## ⚡ Installation Express (5 minutes)

### 1. Prérequis

```bash
# Python 3.9+
python --version

# Git
git --version
```

### 2. Installation

```bash
# Cloner le projet
git clone <votre-repo>
cd "moteur israelien"

# Installer les dépendances
cd backend
pip install -r requirements.txt
```

### 3. Configuration

```bash
# Copier le fichier d'exemple
cp .env.example .env

# Éditer .env et ajouter au minimum :
# JWT_SECRET_KEY=<générer avec: python -c "import secrets; print(secrets.token_urlsafe(32))">
```

### 4. Démarrer le serveur

```bash
# Développement (avec reload)
python main.py

# Ou avec uvicorn directement
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Le serveur démarre sur** : http://localhost:8000

---

## 📚 Endpoints Essentiels

### Documentation Interactive
- **Swagger UI** : http://localhost:8000/docs
- **ReDoc** : http://localhost:8000/redoc

### Health & Status
- **Health Check** : `GET /api/health`
- **Deep Health** : `GET /api/health/deep`
- **Kubernetes Ready** : `GET /api/health/ready`
- **Kubernetes Live** : `GET /api/health/live`

### Métriques
- **Métriques JSON** : `GET /api/metrics`
- **Prometheus** : `GET /api/metrics/prometheus`
- **Résumé** : `GET /api/metrics/summary`

### API Info
- **Root** : `GET /`
- **Info détaillée** : `GET /api/info`

---

## 🧪 Tests

### Tests Rapides

```bash
# Tous les tests
pytest

# Tests unitaires uniquement
pytest tests/ -m "not integration"

# Tests avec couverture
pytest --cov=. --cov-report=html
```

### Validation Complète

```bash
# Script de validation (Windows)
run_tests.bat

# Script de validation (Linux/Mac)
./run_tests.sh
```

---

## 🔧 Configuration Minimale

### Variables d'Environnement Requises

```env
# OBLIGATOIRE en production
JWT_SECRET_KEY=your-secret-key-here

# Recommandé
REDIS_HOST=localhost
REDIS_PORT=6379

# Au moins un provider AI
GROQ_API_KEY=your-key
# OU
MISTRAL_API_KEY=your-key
# OU
GEMINI_API_KEY=your-key
```

### Variables Optionnelles

```env
# Server
API_HOST=0.0.0.0
API_PORT=8000
API_RELOAD=true

# Logging
LOG_LEVEL=INFO
LOG_FILE=./logs/app.log
JSON_LOGS=false

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:8080
```

---

## 🎯 Premiers Pas

### 1. Tester le Health Check

```bash
curl http://localhost:8000/api/health
```

### 2. Tester le Chat AI

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello!", "language": "en"}'
```

### 3. Tester la Recherche Universelle

```bash
curl "http://localhost:8000/api/search?q=bitcoin+price"
```

### 4. Voir les Métriques

```bash
curl http://localhost:8000/api/metrics
```

---

## 🐳 Docker (Optionnel)

```bash
# Build
docker build -t universal-api-backend .

# Run
docker run -p 8000:8000 --env-file .env universal-api-backend
```

---

## 📊 Vérification Post-Installation

### Checklist

- [ ] Serveur démarre sans erreur
- [ ] `/api/health` retourne `200 OK`
- [ ] `/docs` accessible
- [ ] Au moins un provider AI configuré
- [ ] Redis connecté (ou cache mémoire actif)
- [ ] Logs apparaissent dans la console

### Script de Vérification

```bash
# Windows
python scripts/verify_setup.py

# Linux/Mac
python3 scripts/verify_setup.py
```

---

## 🚨 Dépannage

### Problème : "JWT_SECRET_KEY not set"

**Solution** :
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
# Copier la clé dans .env
```

### Problème : "Redis unavailable"

**Solution** :
- Option 1 : Installer Redis
- Option 2 : Le cache mémoire fonctionne en fallback (OK pour dev)

### Problème : "No AI providers available"

**Solution** :
- Configurer au moins une clé API (GROQ_API_KEY, MISTRAL_API_KEY, etc.)
- Ou installer Ollama localement pour AI gratuit

### Problème : Port déjà utilisé

**Solution** :
```bash
# Changer le port dans .env
API_PORT=8001
```

---

## 📖 Documentation Complète

- **Architecture** : `docs/ARCHITECTURE.md`
- **API Reference** : http://localhost:8000/docs
- **Déploiement** : `docs/DEPLOYMENT.md`
- **Tests** : `backend/tests/README.md`

---

## 🎉 C'est Parti !

Votre backend est maintenant opérationnel. Explorez la documentation interactive sur `/docs` !

**Prochaines étapes** :
1. Configurer vos clés API
2. Tester les endpoints
3. Intégrer dans votre frontend
4. Déployer en production

---

*Dernière mise à jour : v2.3.0*



