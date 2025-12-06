# 🚀 Universal Multi-API Backend

**Backend FastAPI complet avec 70+ APIs intégrées, IA multi-providers, et fonctionnalités avancées**

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📖 Vue d'ensemble

**Version** : 2.4.0  
**Date** : Décembre 2024  
**Score** : **10/10 - Enterprise Grade** 🏆

---

## 🎯 **CARACTÉRISTIQUES PRINCIPALES**

### 🤖 **10+ Providers IA**
| Provider | Quota Gratuit | Type |
|----------|---------------|------|
| Ollama | ♾️ Illimité | Local |
| Groq | 14,400/jour | Cloud |
| Mistral | 1M tokens/mois | Cloud |
| Google Gemini | 1,500/jour | Cloud |
| Cohere | 1,000/mois | Cloud |
| AI21 Labs | 10,000/mois | Cloud |
| Hugging Face | 30,000/mois | Cloud |
| Perplexity | 10,000/mois | Cloud |
| Anthropic Claude | Sur demande | Cloud |
| OpenRouter | 50/jour | Cloud |

### 💰 **Finance & Crypto**
- CoinGecko (10,000/mois)
- CoinCap (Illimité)
- Alpha Vantage (25/jour)
- Yahoo Finance (Illimité)
- Exchange Rate API (1,500/mois)

### 📰 **News & Media**
- NewsAPI (100/jour)
- NewsData.io (200/jour)
- OMDB - Films (1,000/jour)
- YouTube Data API (10,000/jour)
- Giphy (Illimité)
- Pixabay (5,000/heure)

### 📚 **Connaissances**
- Wikipedia (Illimité)
- Google Books (1,000/jour)
- Open Library (Illimité)
- Open Trivia DB (Illimité)
- Numbers API (Illimité)

### 🌍 **Géolocalisation**
- OpenMeteo (Illimité)
- WeatherAPI (1M/mois)
- REST Countries (Illimité)
- IP Geolocation (Illimité)
- World Time API (Illimité)

### 🎭 **Fun & Entertainment**
- JokeAPI (Illimité)
- Chuck Norris API (Illimité)
- Bored API (Illimité)
- Dog API (Illimité)
- Cat API (Illimité)
- Lorem Picsum (Illimité)
- Random User (Illimité)

### 🔧 **Utilitaires**
- TinyURL (Illimité)
- Export (JSON/CSV/Markdown)
- Name Analysis (Agify/Genderize)
- Search History
- Discord Webhooks

### 🔍 **Recherche Intelligente**
- **AI Search** : Combine IA + APIs pour des réponses enrichies
- **Optimized Search** : Groupement par catégorie
- **Universal Search** : Recherche cross-API

---

## 🏗️ **ARCHITECTURE**

```
┌─────────────────────────────────────────────────────────────┐
│              UNIVERSAL MULTI-API BACKEND v2.4.0             │
│                                                             │
│  ┌───────────────────────────────────────────────────────┐  │
│  │                    70+ APIs                           │  │
│  │  AI | Finance | News | Weather | Books | Fun | Utils  │  │
│  └───────────────────────────────────────────────────────┘  │
│                           │                                 │
│  ┌───────────────────────────────────────────────────────┐  │
│  │                INTELLIGENT LAYER                      │  │
│  │  • AI Search (IA + Data)                              │  │
│  │  • Optimized Search (Category Grouping)               │  │
│  │  • Fallback & Circuit Breaker                         │  │
│  │  • Cache (Redis + Memory)                             │  │
│  └───────────────────────────────────────────────────────┘  │
│                           │                                 │
│  ┌───────────────────────────────────────────────────────┐  │
│  │                  SECURITY LAYER                       │  │
│  │  JWT | Rate Limiting | CORS | Headers | Sanitization  │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 **DÉMARRAGE RAPIDE**

### Installation

```bash
# Cloner le projet
git clone https://github.com/8888vtc-ui/universal-multi-api-backend.git
cd universal-multi-api-backend

# Installer les dépendances
cd backend
pip install -r requirements.txt

# Configurer l'environnement
cp .env.example .env
# Éditer .env avec vos clés API

# Lancer le serveur
python main.py
```

### Accès

- **API** : http://localhost:8000
- **Documentation** : http://localhost:8000/docs
- **Health Check** : http://localhost:8000/api/health
- **Metrics** : http://localhost:8000/api/metrics

---

## 📡 **ENDPOINTS PRINCIPAUX**

### 🤖 IA & Chat
```
POST /api/chat/            - Chat avec fallback IA
POST /api/ai-search/search - Recherche intelligente IA + Data
GET  /api/embeddings/      - Génération d'embeddings
```

### 💰 Finance
```
GET /api/finance/crypto/price/{symbol}  - Prix crypto
GET /api/finance/stock/quote/{symbol}   - Cotation action
GET /api/coincap/assets                 - Top cryptos
GET /api/exchange/convert               - Conversion devises
```

### 📚 Connaissances
```
GET /api/wikipedia/search      - Recherche Wikipedia
GET /api/books/search          - Recherche livres Google
GET /api/openlibrary/search    - Recherche Open Library
GET /api/trivia/questions      - Questions quiz
GET /api/numbers/random        - Facts sur nombres
```

### 🎭 Fun
```
GET /api/jokes/random          - Blague aléatoire
GET /api/jokes/chuck           - Chuck Norris facts
GET /api/bored/activity        - Suggestion d'activité
GET /api/animals/dogs/random   - Image chien
GET /api/animals/cats/random   - Image chat
```

### 🔧 Utilitaires
```
GET  /api/name/analyze         - Analyse de prénom
POST /api/export/json          - Export JSON
POST /api/export/csv           - Export CSV
GET  /api/history/{user_id}    - Historique recherches
```

---

## 📊 **STATISTIQUES**

| Métrique | Valeur |
|----------|--------|
| **APIs Intégrées** | 70+ |
| **Providers IA** | 10 |
| **Endpoints** | 150+ |
| **Requêtes gratuites/jour** | 200,000+ |
| **Catégories** | 15 |

---

## 🔒 **SÉCURITÉ**

- ✅ JWT Authentication
- ✅ Rate Limiting (SlowAPI)
- ✅ CORS Configuration
- ✅ Security Headers
- ✅ Input Sanitization
- ✅ Request ID Tracing
- ✅ Prometheus Metrics

---

## 📁 **STRUCTURE**

```
backend/
├── main.py                    # Application FastAPI
├── routers/                   # 60+ routers
│   ├── chat.py               # IA Chat
│   ├── finance.py            # Finance
│   ├── jokes.py              # Blagues
│   ├── trivia.py             # Quiz
│   └── ...
├── services/
│   ├── ai_router.py          # Routeur IA multi-provider
│   ├── ai_search_engine.py   # Moteur recherche IA
│   ├── search_optimizer.py   # Optimisation recherche
│   ├── search_history.py     # Historique
│   └── external_apis/        # Providers
├── middleware/                # Security middleware
└── scripts/                   # Scripts utilitaires
```

---

## 🔧 **CONFIGURATION**

### Variables d'Environnement Requises

```env
# IA (au moins un)
GROQ_API_KEY=your_key
MISTRAL_API_KEY=your_key
GEMINI_API_KEY=your_key

# Optionnels
COHERE_API_KEY=your_key
AI21_API_KEY=your_key
ANTHROPIC_API_KEY=your_key
HUGGINGFACE_API_TOKEN=your_key
PERPLEXITY_API_KEY=your_key

# Sécurité
JWT_SECRET_KEY=your_secret
```

---

## 📈 **PROCHAINES ÉTAPES**

1. **Déploiement** : VPS, Docker, ou Cloud
2. **Monitoring** : Prometheus + Grafana
3. **Frontend** : Applications spécialisées
4. **Documentation** : Guides d'intégration

---

## 📜 **LICENCE**

MIT License - Voir [LICENSE](LICENSE)

---

## 👨‍💻 **AUTEUR**

Développé avec ❤️ pour un usage universel

---

*Backend v2.4.0 - 70+ APIs - Enterprise Grade*
