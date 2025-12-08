# 🧪 Test Local avec Ollama - Guide Complet

**Date** : Décembre 2024  
**Version** : 2.3.0  
**Objectif** : Tester localement avant le déploiement, avec Ollama gratuit

---

## 🎯 Pourquoi Tester Localement avec Ollama ?

- ✅ **100% gratuit** - Pas besoin de clés API
- ✅ **Local** - Fonctionne sans internet (après installation)
- ✅ **Rapide** - Pas de latence réseau
- ✅ **Parfait pour tester** - Valide tout avant production
- ✅ **Ollama inclus** - IA locale gratuite

---

## 📋 Prérequis

- Python 3.9+
- Docker (optionnel, pour Ollama)
- 8GB+ RAM recommandé (pour Ollama)
- Windows/Mac/Linux

---

## 🚀 Installation Rapide

### Étape 1 : Installer Ollama (5 min)

#### Windows
```powershell
# Télécharger depuis https://ollama.com/download
# Installer l'exécutable
# Ollama démarrera automatiquement
```

#### Mac
```bash
# Avec Homebrew
brew install ollama

# Ou télécharger depuis https://ollama.com/download
```

#### Linux
```bash
# Installation automatique
curl -fsSL https://ollama.com/install.sh | sh

# Ou avec le script du projet
cd backend
bash install_ollama.sh
```

### Étape 2 : Télécharger un Modèle (10-20 min)

```bash
# Modèle léger (recommandé pour test)
ollama pull llama3.2:1b

# Ou modèle plus performant
ollama pull llama3.2:3b

# Ou modèle complet (plus lent mais meilleur)
ollama pull llama3.2
```

**Note** : Le premier téléchargement peut prendre du temps selon votre connexion.

### Étape 3 : Vérifier Ollama

```bash
# Tester Ollama
ollama run llama3.2:1b "Hello, how are you?"

# Vérifier que le serveur tourne
curl http://localhost:11434/api/tags
```

---

## ⚙️ Configuration du Backend

### Étape 1 : Configurer .env

```bash
cd backend

# Copier .env.example
cp .env.example .env

# Éditer .env
nano .env  # ou votre éditeur préféré
```

### Étape 2 : Configuration Minimale pour Test Local

Dans `.env`, configurez au minimum :

```env
# Obligatoire
JWT_SECRET_KEY=<générer avec: python -c "import secrets; print(secrets.token_urlsafe(32))">
ENVIRONMENT=development

# Ollama (gratuit, local)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2:1b

# Port
API_PORT=8000
API_HOST=0.0.0.0

# Optionnel (pour tester d'autres fonctionnalités)
# GROQ_API_KEY=  # Si vous voulez tester Groq aussi
# MISTRAL_API_KEY=  # Si vous voulez tester Mistral aussi
```

**Important** : Ollama fonctionne sans clé API, c'est gratuit et local !

---

## 🚀 Démarrer le Serveur

### Option 1 : Script de Démarrage (Recommandé)

```bash
cd backend
python scripts/start_server.py
```

### Option 2 : Directement

```bash
cd backend
python main.py
```

### Option 3 : Avec Uvicorn

```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

---

## ✅ Vérification

### 1. Vérifier que le Serveur Démarre

```bash
# Le serveur devrait afficher :
# 🚀 Universal Multi-API Backend v2.3.0
# 📡 Server: http://0.0.0.0:8000
# 📚 Docs: http://0.0.0.0:8000/docs
```

### 2. Tester les Endpoints

```bash
# Health check
curl http://localhost:8000/api/health

# API Info
curl http://localhost:8000/api/info

# Chat avec Ollama (gratuit, local)
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"Hello, how are you?","language":"en"}'
```

### 3. Tester depuis le Navigateur

Ouvrir :
- **Documentation** : http://localhost:8000/docs
- **Health** : http://localhost:8000/api/health
- **Metrics** : http://localhost:8000/api/metrics

---

## 🧪 Tests Complets

### Test 1 : Chat IA avec Ollama

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Explique-moi ce qu est l intelligence artificielle",
    "language": "fr"
  }'
```

### Test 2 : Health Checks

```bash
# Health simple
curl http://localhost:8000/api/health

# Deep health
curl http://localhost:8000/api/health/deep

# Kubernetes probes
curl http://localhost:8000/api/health/ready
curl http://localhost:8000/api/health/live
```

### Test 3 : Metrics

```bash
# Metrics JSON
curl http://localhost:8000/api/metrics

# Prometheus
curl http://localhost:8000/api/metrics/prometheus
```

### Test 4 : Recherche Universelle

```bash
curl -X POST http://localhost:8000/api/search/universal \
  -H "Content-Type: application/json" \
  -d '{
    "query": "test",
    "categories": ["news"],
    "max_results_per_category": 3
  }'
```

---

## 🔧 Configuration Avancée Ollama

### Modèles Disponibles

```bash
# Lister les modèles disponibles
ollama list

# Modèles recommandés pour test :
# - llama3.2:1b (très rapide, léger)
# - llama3.2:3b (bon équilibre)
# - llama3.2 (complet, plus lent)
# - mistral (alternatif)
# - phi3 (Microsoft, léger)
```

### Changer le Modèle

Dans `.env` :
```env
OLLAMA_MODEL=llama3.2:3b  # Changer le modèle
```

Redémarrer le serveur.

---

## 📊 Performance Locale

### Avantages du Test Local

- ✅ **Rapide** - Pas de latence réseau
- ✅ **Gratuit** - Ollama est gratuit
- ✅ **Privé** - Données restent locales
- ✅ **Sans limites** - Pas de quotas API
- ✅ **Test complet** - Toutes les fonctionnalités

### Limitations

- ⚠️ **Ressources** - Ollama utilise de la RAM/CPU
- ⚠️ **Modèles** - Plus petits que les modèles cloud
- ⚠️ **Performance** - Dépend de votre machine

---

## 🐛 Dépannage

### Ollama Ne Démarre Pas

```bash
# Vérifier que Ollama tourne
ollama serve

# Ou redémarrer
ollama serve
```

### Le Serveur Ne Peut Pas Contacter Ollama

```bash
# Vérifier l'URL dans .env
cat backend/.env | grep OLLAMA

# Tester Ollama directement
curl http://localhost:11434/api/tags

# Vérifier le port
netstat -an | grep 11434
```

### Erreur "Model not found"

```bash
# Télécharger le modèle
ollama pull llama3.2:1b

# Vérifier les modèles disponibles
ollama list
```

### Problèmes de Mémoire

Si vous avez peu de RAM :
```bash
# Utiliser un modèle plus petit
ollama pull llama3.2:1b  # Au lieu de llama3.2

# Dans .env
OLLAMA_MODEL=llama3.2:1b
```

---

## 📋 Checklist de Test Local

### Avant de Commencer
- [ ] Python 3.9+ installé
- [ ] Ollama installé
- [ ] Modèle Ollama téléchargé
- [ ] .env configuré

### Démarrage
- [ ] Ollama démarré
- [ ] Serveur backend démarré
- [ ] Pas d'erreurs dans les logs

### Tests
- [ ] Health checks OK
- [ ] Chat avec Ollama fonctionne
- [ ] Documentation accessible
- [ ] Metrics accessibles
- [ ] Tous les endpoints testés

---

## 🎯 Workflow Recommandé

### 1. Test Local (Maintenant)
```bash
# Tester localement avec Ollama
# Valider toutes les fonctionnalités
# Corriger les bugs
```

### 2. Test sur Serveur Gratuit (Oracle Cloud)
```bash
# Déployer sur Oracle Cloud Free Tier
# Tester avec du trafic réel
# Valider la performance
```

### 3. Production (Hetzner)
```bash
# Déployer en production
# Avec toutes les clés API
# Monitoring configuré
```

---

## 💡 Astuces

### Optimiser Ollama

```bash
# Utiliser un modèle plus petit pour test
ollama pull llama3.2:1b

# Limiter la RAM utilisée
export OLLAMA_NUM_GPU=0  # Désactiver GPU si problème
```

### Tester avec Plusieurs Modèles

```bash
# Télécharger plusieurs modèles
ollama pull llama3.2:1b
ollama pull mistral
ollama pull phi3

# Changer dans .env pour tester
OLLAMA_MODEL=mistral
```

---

## 📚 Documentation

- **Ollama** : https://ollama.com
- **Modèles** : https://ollama.com/library
- **API** : http://localhost:8000/docs

---

## ✅ Résultat Attendu

Après ce test local, vous devriez avoir :
- ✅ Serveur fonctionnel localement
- ✅ Chat IA avec Ollama fonctionnel
- ✅ Tous les endpoints testés
- ✅ Confiance pour déployer

---

**Bon test local ! 🚀**

*Dernière mise à jour : Décembre 2024 - v2.3.0*






