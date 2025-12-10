# 📡 TOUTES LES APIs DU PROJET - Liste Complète par Catégorie

**Date** : Décembre 2024  
**Version** : 2.3.0  
**Total** : **50+ APIs** intégrées

---

## 🤖 1. INTELLIGENCE ARTIFICIELLE (10 Providers)

### Chat & LLM
1. **Groq**
   - Quota : 14,000 requêtes/jour (gratuit)
   - Variable : `GROQ_API_KEY`
   - Router : `chat.py`, `embeddings.py`
   - Status : ✅ Intégré

2. **Mistral AI**
   - Quota : 1M tokens/mois (gratuit)
   - Variable : `MISTRAL_API_KEY`
   - Router : `chat.py`, `embeddings.py`
   - Status : ✅ Intégré

3. **Google Gemini**
   - Quota : 1,500 requêtes/jour (gratuit)
   - Variable : `GEMINI_API_KEY`
   - Router : `chat.py`, `embeddings.py`
   - Status : ✅ Intégré

4. **OpenRouter**
   - Quota : 50 requêtes/jour (gratuit)
   - Variable : `OPENROUTER_API_KEY`
   - Router : `chat.py`, `embeddings.py`
   - Status : ✅ Intégré

5. **Ollama** (Local)
   - Quota : Illimité (local)
   - Variable : `OLLAMA_BASE_URL` (optionnel)
   - Router : `chat.py`, `embeddings.py`
   - Status : ✅ Intégré

6. **Anthropic Claude**
   - Quota : Variable selon plan
   - Variable : `ANTHROPIC_API_KEY`
   - Router : `chat.py`
   - Status : ✅ Intégré

7. **Perplexity**
   - Quota : Variable selon plan
   - Variable : `PERPLEXITY_API_KEY`
   - Router : `chat.py`
   - Status : ✅ Intégré

8. **AI21**
   - Quota : Variable selon plan
   - Variable : `AI21_API_KEY`
   - Router : `chat.py`
   - Status : ✅ Intégré

### Embeddings & Vectorisation
9. **Cohere**
   - Quota : Variable selon plan
   - Variable : `COHERE_API_KEY`
   - Router : `embeddings.py`
   - Status : ✅ Intégré

10. **Hugging Face**
    - Quota : 100,000+ modèles disponibles
    - Variable : `HUGGINGFACE_API_TOKEN`
    - Router : `embeddings.py`
    - Status : ✅ Intégré

### Services IA Avancés
- **BoltAI Router** : Router IA avancé avec agents experts
  - Router : `boltai.py`
  - Status : ✅ Intégré

---

## 💰 2. FINANCE (9 Providers)

### Crypto
1. **CoinGecko**
   - Quota : 10,000 requêtes/mois (gratuit)
   - Variable : `COINGECKO_API_KEY` (optionnel)
   - Router : `finance.py`
   - Status : ✅ Intégré

2. **CoinCap**
   - Quota : Illimité (gratuit)
   - Variable : Aucune
   - Router : `coincap.py`
   - Status : ✅ Intégré

### Stocks & Marchés
3. **Alpha Vantage** ✅ CONFIGURÉ
   - Quota : 25 requêtes/jour (gratuit)
   - Variable : `ALPHAVANTAGE_API_KEY` = `CVXV9XDIJNQJNI4B`
   - Router : `finance.py`
   - Status : ✅ Intégré

4. **Yahoo Finance**
   - Quota : Illimité (via yfinance)
   - Variable : Aucune
   - Router : `finance.py`
   - Status : ✅ Intégré

5. **Finnhub** ✅ CONFIGURÉ
   - Quota : 60 requêtes/minute, illimité/jour (gratuit)
   - Variable : `FINNHUB_API_KEY` = `d4s2nu1r01qvsjbf5ti0d4s2nu1r01qvsjbf5tig`
   - Router : `finance.py`
   - Status : ✅ Intégré

6. **Twelve Data** ✅ CONFIGURÉ
   - Quota : 800 requêtes/jour (gratuit)
   - Variable : `TWELVE_DATA_API_KEY` = `80dae489f6a540fb94e55e66c067f53a`
   - Router : `finance.py`
   - Status : ✅ Intégré

7. **Polygon.io** ✅ CONFIGURÉ
   - Quota : 5 requêtes/minute, illimité/jour (gratuit)
   - Variable : `POLYGON_API_KEY` = `XdLxa1aElMtXguFg32VxeTegonov0IGFxsx`
   - Router : `finance.py`
   - Status : ✅ Intégré

### Devises
8. **Exchange Rate API**
   - Quota : 1,500 requêtes/mois (gratuit)
   - Variable : Aucune
   - Router : `exchange.py`
   - Status : ✅ Intégré

### Fallback
9. **Finance Fallback**
   - Quota : Illimité (local, données statiques + cache)
   - Variable : Aucune
   - Router : `finance.py`
   - Status : ✅ Intégré

---

## ✈️ 3. TOURISME & VOYAGE (14 Providers)

### Géocodage
1. **Nominatim (OpenStreetMap)**
   - Quota : 1 requête/seconde (illimité)
   - Variable : Aucune
   - Router : `geocoding.py`
   - Status : ✅ Intégré

2. **OpenCage**
   - Quota : 2,500 requêtes/jour (gratuit)
   - Variable : `OPENCAGE_API_KEY`
   - Router : `geocoding.py`
   - Status : ✅ Intégré

3. **Positionstack**
   - Quota : 25,000 requêtes/mois (gratuit)
   - Variable : `POSITIONSTACK_API_KEY`
   - Router : `geocoding.py`
   - Status : ✅ Intégré

### Météo
4. **Open-Meteo**
   - Quota : Illimité (gratuit)
   - Variable : Aucune
   - Router : `weather.py`
   - Status : ✅ Intégré

5. **WeatherAPI**
   - Quota : 1 million requêtes/mois (gratuit)
   - Variable : `WEATHERAPI_KEY`
   - Router : `weather.py`
   - Status : ✅ Intégré

### Informations Pays
6. **REST Countries**
   - Quota : Illimité (gratuit)
   - Variable : Aucune
   - Router : `countries.py`
   - Status : ✅ Intégré

### Taux de Change
7. **Exchange Rate API**
   - Quota : 1,500 requêtes/mois (gratuit)
   - Variable : Aucune
   - Router : `exchange.py`
   - Status : ✅ Intégré

### Traduction
8. **LibreTranslate**
   - Quota : Illimité (local)
   - Variable : Aucune
   - Router : `translation.py`
   - Status : ✅ Intégré

9. **Google Translate**
   - Quota : 500,000 caractères/mois (gratuit)
   - Variable : `GOOGLE_TRANSLATE_API_KEY`
   - Router : `translation.py`
   - Status : ✅ Intégré

10. **DeepL**
    - Quota : 500,000 caractères/mois (gratuit)
    - Variable : `DEEPL_API_KEY`
    - Router : `translation.py`
    - Status : ✅ Intégré

11. **Yandex Translate**
    - Quota : 10,000,000 caractères/mois (gratuit)
    - Variable : `YANDEX_TRANSLATE_API_KEY`
    - Router : `translation.py`
    - Status : ✅ Intégré

### Restaurants & Attractions
12. **Yelp**
    - Quota : 5,000 requêtes/jour (gratuit)
    - Variable : `YELP_API_KEY`
    - Router : `entertainment.py`
    - Status : ✅ Intégré

### Actualités
13. **NewsAPI.org**
    - Quota : 100 requêtes/jour (gratuit)
    - Variable : `NEWSAPI_ORG_KEY`
    - Router : `news.py`
    - Status : ✅ Intégré

14. **NewsData.io**
    - Quota : 200 requêtes/jour (gratuit)
    - Variable : `NEWSDATA_IO_KEY`
    - Router : `news.py`
    - Status : ✅ Intégré

### Vols & Aviation
15. **Aviationstack** ✅ CONFIGURÉ (Provider à créer)
    - Quota : 1,000 requêtes/mois (gratuit)
    - Variable : `AVIATIONSTACK_API_KEY` = `6d42cb6dbbf72807d21b0275b3e3832f`
    - Router : À créer
    - Status : ⚠️ Clé configurée, provider non installé

---

## 🏥 4. MÉDICAL (2 Providers)

1. **PubMed**
   - Quota : Illimité (gratuit)
   - Variable : Aucune
   - Router : `medical.py`
   - Status : ✅ Intégré

2. **OpenFDA**
   - Quota : Illimité (gratuit)
   - Variable : Aucune
   - Router : `medical.py`
   - Status : ✅ Intégré

---

## 🎮 5. ENTERTAINMENT (3 Providers)

1. **TMDB** (Films & Séries)
   - Quota : 1,000 requêtes/jour (gratuit)
   - Variable : `TMDB_API_KEY`
   - Router : `entertainment.py`
   - Status : ✅ Intégré

2. **Yelp** (Restaurants)
   - Quota : 5,000 requêtes/jour (gratuit)
   - Variable : `YELP_API_KEY`
   - Router : `entertainment.py`
   - Status : ✅ Intégré

3. **Spotify** (Musique)
   - Quota : Variable selon plan
   - Variable : `SPOTIFY_CLIENT_ID`, `SPOTIFY_CLIENT_SECRET`
   - Router : `entertainment.py`
   - Status : ✅ Intégré

---

## 🍎 6. NUTRITION (3 Providers)

1. **Spoonacular**
   - Quota : Variable selon plan
   - Variable : `SPOONACULAR_API_KEY`
   - Router : `nutrition.py`
   - Status : ✅ Intégré

2. **Edamam**
   - Quota : Variable selon plan
   - Variable : `EDAMAM_APP_ID`, `EDAMAM_APP_KEY`
   - Router : `nutrition.py`
   - Status : ✅ Intégré

3. **USDA**
   - Quota : Illimité (gratuit)
   - Variable : `USDA_API_KEY` (optionnel, "DEMO_KEY" par défaut)
   - Router : `nutrition.py`
   - Status : ✅ Intégré

---

## 🖼️ 7. MÉDIAS (4 Providers)

1. **Unsplash** (Photos)
   - Quota : Variable selon plan
   - Variable : `UNSPLASH_ACCESS_KEY`
   - Router : `media.py`
   - Status : ✅ Intégré

2. **Pexels** (Photos & Vidéos)
   - Quota : Variable selon plan
   - Variable : `PEXELS_API_KEY`
   - Router : `media.py`
   - Status : ✅ Intégré

3. **Giphy** (GIFs)
   - Quota : Illimité (gratuit avec clé beta)
   - Variable : `GIPHY_API_KEY`
   - Router : `giphy.py`
   - Status : ✅ Intégré

4. **Pixabay** (Photos & Vidéos)
   - Quota : Variable selon plan
   - Variable : `PIXABAY_API_KEY`
   - Router : `pixabay.py`
   - Status : ✅ Intégré

---

## 📧 8. EMAIL (3 Providers)

1. **SendGrid**
   - Quota : Variable selon plan
   - Variable : `SENDGRID_API_KEY`
   - Router : `email.py`
   - Status : ✅ Intégré

2. **Mailgun**
   - Quota : Variable selon plan
   - Variable : `MAILGUN_API_KEY`, `MAILGUN_DOMAIN`
   - Router : `email.py`
   - Status : ✅ Intégré

3. **Mailjet**
   - Quota : Variable selon plan
   - Variable : `MAILJET_API_KEY`, `MAILJET_API_SECRET`
   - Router : `email.py`
   - Status : ✅ Intégré

---

## 💬 9. MESSAGING (3 Providers)

1. **Telegram**
   - Quota : Illimité (gratuit)
   - Variable : `TELEGRAM_BOT_TOKEN`
   - Router : `messaging.py`
   - Status : ✅ Intégré

2. **Line**
   - Quota : Variable selon plan
   - Variable : `LINE_CHANNEL_ACCESS_TOKEN`
   - Router : `messaging.py`
   - Status : ✅ Intégré

3. **Kakao**
   - Quota : Variable selon plan
   - Variable : `KAKAO_REST_API_KEY`
   - Router : `messaging.py`
   - Status : ✅ Intégré

---

## 🎬 10. VIDÉO & TTS (2 Providers)

1. **D-ID** (Avatars parlants)
   - Quota : Variable selon plan
   - Variable : `DID_API_KEY`
   - Router : `video.py`
   - Status : ✅ Intégré

2. **ElevenLabs** (Text-to-Speech)
   - Quota : Variable selon plan
   - Variable : `ELEVENLABS_API_KEY`
   - Router : `video.py`
   - Status : ✅ Intégré

---

## 🚀 11. ESPACE (1 Provider)

1. **NASA APIs**
   - Quota : Illimité (gratuit)
   - Variable : `NASA_API_KEY` (optionnel, "DEMO_KEY" par défaut)
   - Router : `space.py`
   - Status : ✅ Intégré

---

## ⚽ 12. SPORTS (1 Provider)

1. **API-Sports**
   - Quota : Variable selon plan
   - Variable : `APISPORTS_KEY`
   - Router : `sports.py`
   - Status : ✅ Intégré

---

## 🔧 13. UTILITAIRES (Multiple Services)

1. **OCR** (Tesseract, EasyOCR)
   - Quota : Illimité (local)
   - Variable : Aucune
   - Router : `utilities.py`
   - Status : ✅ Intégré

2. **QR Code** (Génération & Lecture)
   - Quota : Illimité (local)
   - Variable : Aucune
   - Router : `utilities.py`
   - Status : ✅ Intégré

3. **URL Shortener** (TinyURL)
   - Quota : Variable selon plan
   - Variable : Aucune (fonctionne sans clé)
   - Router : `tinyurl.py`
   - Status : ✅ Intégré

4. **IP Geolocation**
   - Quota : Variable selon plan
   - Variable : Aucune (fonctionne sans clé)
   - Router : `ip_geolocation.py`
   - Status : ✅ Intégré

---

## 📚 14. LIVRES & CONNAISSANCES (3 Providers)

1. **Google Books**
   - Quota : 1,000 requêtes/jour (gratuit)
   - Variable : `GOOGLE_BOOKS_API_KEY` (optionnel)
   - Router : `books.py`
   - Status : ✅ Intégré

2. **Open Library**
   - Quota : Illimité (gratuit)
   - Variable : Aucune
   - Router : `openlibrary.py`
   - Status : ✅ Intégré

3. **Wikipedia**
   - Quota : Illimité (gratuit)
   - Variable : Aucune
   - Router : `wikipedia.py`
   - Status : ✅ Intégré

---

## 🎲 15. DIVERTISSEMENT & DONNÉES TEST (Multiple Providers)

1. **JSONPlaceholder** (Données test)
   - Quota : Illimité (gratuit)
   - Variable : Aucune
   - Router : `jsonplaceholder.py`
   - Status : ✅ Intégré

2. **FakeStore** (E-commerce test)
   - Quota : Illimité (gratuit)
   - Variable : Aucune
   - Router : `fakestore.py`
   - Status : ✅ Intégré

3. **Random User** (Génération profils)
   - Quota : Illimité (gratuit)
   - Variable : Aucune
   - Router : `randomuser.py`
   - Status : ✅ Intégré

4. **Jokes** (Blagues)
   - Quota : Illimité (gratuit)
   - Variable : Aucune
   - Router : `jokes.py`
   - Status : ✅ Intégré

5. **Quotes** (Citations)
   - Quota : Illimité (gratuit)
   - Variable : Aucune
   - Router : `quotes.py`
   - Status : ✅ Intégré

6. **Trivia** (Questions)
   - Quota : Illimité (gratuit)
   - Variable : Aucune
   - Router : `trivia.py`
   - Status : ✅ Intégré

7. **Bored** (Activités)
   - Quota : Illimité (gratuit)
   - Variable : Aucune
   - Router : `bored.py`
   - Status : ✅ Intégré

8. **Animals** (Animaux)
   - Quota : Illimité (gratuit)
   - Variable : Aucune
   - Router : `animals.py`
   - Status : ✅ Intégré

9. **Numbers** (Facts numériques)
   - Quota : Illimité (gratuit)
   - Variable : Aucune
   - Router : `numbers.py`
   - Status : ✅ Intégré

10. **World Time** (Fuseaux horaires)
    - Quota : Illimité (gratuit)
    - Variable : Aucune
    - Router : `worldtime.py`
    - Status : ✅ Intégré

11. **Lorem Picsum** (Images placeholder)
    - Quota : Illimité (gratuit)
    - Variable : Aucune
    - Router : `lorempicsum.py`
    - Status : ✅ Intégré

12. **Lorem Ipsum** (Texte placeholder)
    - Quota : Illimité (gratuit)
    - Variable : Aucune
    - Router : `lorem.py`
    - Status : ✅ Intégré

13. **GitHub** (Repositories)
    - Quota : Variable selon plan
    - Variable : Aucune (fonctionne sans clé)
    - Router : `github.py`
    - Status : ✅ Intégré

14. **Name Analysis** (Analyse de noms)
    - Quota : Variable selon plan
    - Variable : Aucune
    - Router : `nameanalysis.py`
    - Status : ✅ Intégré

---

## 🔍 16. SERVICES INTERNES & AVANCÉS

### Moteur de Recherche
- **Universal Search** : Recherche cross-APIs intelligente
  - Router : `search.py`
  - Status : ✅ Intégré

- **AI Search** : Recherche avec IA
  - Router : `ai_search.py`
  - Status : ✅ Intégré

### Endpoints Agrégés
- **Aggregated APIs** : Combine plusieurs APIs en parallèle
  - Router : `aggregated.py`
  - Endpoints :
    - `/api/aggregated/travel/recommendations`
    - `/api/aggregated/market/analysis`
    - `/api/aggregated/health/recommendations`
    - `/api/aggregated/location/complete`
    - `/api/aggregated/crypto/complete`
  - Status : ✅ Intégré

### Assistant Personnel
- **Assistant IA** : Assistant personnel intelligent
  - Router : `assistant.py`
  - Status : ✅ Intégré

- **Expert Chat** : Chat avec agents experts spécialisés
  - Router : `expert_chat.py`
  - Status : ✅ Intégré

### Analytics & Monitoring
- **Analytics** : Métriques et statistiques
  - Router : `analytics.py`
  - Status : ✅ Intégré

- **Metrics** : Métriques Prometheus
  - Router : `metrics.py`
  - Status : ✅ Intégré

- **Health Check** : Vérification santé système
  - Router : `health.py`, `health_check.py`, `health_deep.py`
  - Status : ✅ Intégré

### Authentification
- **Auth** : JWT Authentication
  - Router : `auth.py`
  - Status : ✅ Intégré

### Export
- **Export** : Export de données
  - Router : `export.py`
  - Status : ✅ Intégré

### History
- **History** : Historique des conversations
  - Router : `history.py`
  - Status : ✅ Intégré

---

## 📊 RÉSUMÉ PAR CATÉGORIE

| Catégorie | Nombre d'APIs | Routers | Status |
|-----------|---------------|---------|--------|
| **🤖 IA** | 10 | `chat.py`, `embeddings.py`, `boltai.py` | ✅ |
| **💰 Finance** | 9 | `finance.py`, `exchange.py`, `coincap.py` | ✅ |
| **✈️ Tourisme** | 15 | `geocoding.py`, `weather.py`, `countries.py`, `translation.py`, `news.py`, `entertainment.py` | ✅ |
| **🏥 Médical** | 2 | `medical.py` | ✅ |
| **🎮 Entertainment** | 3 | `entertainment.py` | ✅ |
| **🍎 Nutrition** | 3 | `nutrition.py` | ✅ |
| **🖼️ Médias** | 4 | `media.py`, `giphy.py`, `pixabay.py` | ✅ |
| **📧 Email** | 3 | `email.py` | ✅ |
| **💬 Messaging** | 3 | `messaging.py` | ✅ |
| **🎬 Vidéo** | 2 | `video.py` | ✅ |
| **🚀 Espace** | 1 | `space.py` | ✅ |
| **⚽ Sports** | 1 | `sports.py` | ✅ |
| **🔧 Utilitaires** | 4+ | `utilities.py`, `tinyurl.py`, `ip_geolocation.py` | ✅ |
| **📚 Livres** | 3 | `books.py`, `openlibrary.py`, `wikipedia.py` | ✅ |
| **🎲 Divertissement** | 14 | Multiple routers | ✅ |
| **🔍 Services Internes** | 10+ | Multiple routers | ✅ |

---

## 📈 STATISTIQUES GLOBALES

- **Total APIs** : **50+ APIs** intégrées
- **Total Routers** : **50+ Routers**
- **Total Endpoints** : **150+ Endpoints**
- **Catégories** : **16 catégories principales**

---

## ✅ CLÉS API CONFIGURÉES

### Finance (4 clés)
- `FINNHUB_API_KEY` = `d4s2nu1r01qvsjbf5ti0d4s2nu1r01qvsjbf5tig`
- `ALPHAVANTAGE_API_KEY` = `CVXV9XDIJNQJNI4B`
- `TWELVE_DATA_API_KEY` = `80dae489f6a540fb94e55e66c067f53a`
- `POLYGON_API_KEY` = `XdLxa1aElMtXguFg32VxeTegonov0IGFxsx`

### Tourisme (1 clé)
- `AVIATIONSTACK_API_KEY` = `6d42cb6dbbf72807d21b0275b3e3832f`

**Total Clés Configurées** : **5 clés API**

---

**Dernière mise à jour** : Décembre 2024

