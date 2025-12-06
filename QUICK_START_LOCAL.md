# ⚡ Quick Start - Test Local avec Ollama

**Démarrage rapide en 5 minutes**

---

## 🚀 Installation Express

### 1. Installer Ollama (2 min)

**Windows/Mac** : Télécharger depuis https://ollama.com/download

**Linux** :
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### 2. Télécharger un Modèle (3-5 min)

```bash
# Modèle léger (recommandé)
ollama pull llama3.2:1b
```

### 3. Configurer le Backend (1 min)

```bash
cd backend
cp .env.example .env

# Éditer .env et ajouter :
# OLLAMA_BASE_URL=http://localhost:11434
# OLLAMA_MODEL=llama3.2:1b
```

### 4. Démarrer (1 min)

```bash
python scripts/start_server.py
```

**C'est tout ! 🎉**

---

## ✅ Tester

```bash
# Health
curl http://localhost:8000/api/health

# Chat avec Ollama (gratuit, local)
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"Hello","language":"en"}'

# Documentation
# Ouvrir http://localhost:8000/docs
```

---

## 📋 Configuration Minimale .env

```env
JWT_SECRET_KEY=<générer>
ENVIRONMENT=development
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2:1b
API_PORT=8000
```

**C'est suffisant pour tester !**

---

## 🎯 Avantages

- ✅ **100% gratuit** - Ollama est gratuit
- ✅ **Local** - Pas besoin d'internet (après installation)
- ✅ **Rapide** - Pas de latence réseau
- ✅ **Privé** - Données restent locales
- ✅ **Sans limites** - Pas de quotas

---

**Voir TEST_LOCAL_OLLAMA.md pour le guide complet**


