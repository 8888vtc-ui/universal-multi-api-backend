# 🔑 Configuration Complète - Toutes les APIs et Clés

**Date** : Décembre 2024  
**Pour** : Configuration serveur production

---

## 📋 Fichier `.env` Complet pour le Serveur

```env
# ============================================
# ENVIRONNEMENT
# ============================================
ENVIRONMENT=production
API_HOST=0.0.0.0
API_PORT=8000
API_RELOAD=false
LOG_LEVEL=info
CORS_ORIGINS=http://localhost:3000,https://votre-domaine.com

# ============================================
# SÉCURITÉ
# ============================================
JWT_SECRET_KEY=votre_jwt_secret_key_genere_ici
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# ============================================
# 🤖 IA & LLM PROVIDERS
# ============================================
GROQ_API_KEY=votre_cle_groq
MISTRAL_API_KEY=votre_cle_mistral
GEMINI_API_KEY=votre_cle_gemini
OPENROUTER_API_KEY=votre_cle_openrouter
COHERE_API_KEY=votre_cle_cohere
AI21_API_KEY=votre_cle_ai21
ANTHROPIC_API_KEY=votre_cle_anthropic
PERPLEXITY_API_KEY=votre_cle_perplexity
HUGGINGFACE_API_TOKEN=votre_cle_huggingface
OLLAMA_BASE_URL=http://localhost:11434

# ============================================
# 💰 FINANCE APIs
# ============================================
# Déjà configurées ✅
FINNHUB_API_KEY=d4s2nu1r01qvsjbf5ti0d4s2nu1r01qvsjbf5tig
ALPHAVANTAGE_API_KEY=CVXV9XDIJNQJNI4B
TWELVE_DATA_API_KEY=80dae489f6a540fb94e55e66c067f53a
POLYGON_API_KEY=XdLxa1aElMtXguFg32VxeTegonov0IGFxsx

# Optionnelles
COINGECKO_API_KEY=votre_cle_coingecko

# ============================================
# 📰 NEWS & INFORMATION APIs
# ============================================
NEWSAPI_ORG_KEY=votre_cle_newsapi_org
NEWSDATA_IO_KEY=votre_cle_newsdata_io

# ============================================
# 🌤️ WEATHER APIs
# ============================================
OPENWEATHER_API_KEY=votre_cle_openweather
WEATHERAPI_KEY=votre_cle_weatherapi

# ============================================
# 🌍 TRANSLATION APIs
# ============================================
GOOGLE_TRANSLATE_API_KEY=votre_cle_google_translate
DEEPL_API_KEY=votre_cle_deepl
YANDEX_TRANSLATE_API_KEY=votre_cle_yandex

# ============================================
# 📍 GEOCODING APIs
# ============================================
OPENCAGE_API_KEY=votre_cle_opencage
POSITIONSTACK_API_KEY=votre_cle_positionstack

# ============================================
# 🎮 ENTERTAINMENT APIs
# ============================================
TMDB_API_KEY=votre_cle_tmdb
YELP_API_KEY=votre_cle_yelp
SPOTIFY_CLIENT_ID=votre_spotify_client_id
SPOTIFY_CLIENT_SECRET=votre_spotify_client_secret

# ============================================
# 🖼️ MEDIA APIs
# ============================================
UNSPLASH_ACCESS_KEY=votre_cle_unsplash
PEXELS_API_KEY=votre_cle_pexels
GIPHY_API_KEY=votre_cle_giphy
PIXABAY_API_KEY=votre_cle_pixabay

# ============================================
# 📚 BOOKS APIs
# ============================================
GOOGLE_BOOKS_API_KEY=votre_cle_google_books

# ============================================
# 🏥 MEDICAL APIs
# ============================================
# PubMed et OpenFDA fonctionnent sans clé API

# ============================================
# 🍎 NUTRITION APIs
# ============================================
SPOONACULAR_API_KEY=votre_cle_spoonacular
EDAMAM_APP_ID=votre_edamam_app_id
EDAMAM_APP_KEY=votre_edamam_app_key

# ============================================
# ⚽ SPORTS APIs
# ============================================
APISPORTS_KEY=votre_cle_apisports

# ============================================
# 🚀 SPACE APIs
# ============================================
NASA_API_KEY=votre_cle_nasa

# ============================================
# 📧 EMAIL APIs
# ============================================
SENDGRID_API_KEY=votre_cle_sendgrid
MAILGUN_API_KEY=votre_cle_mailgun
MAILGUN_DOMAIN=votre_domaine_mailgun
MAILJET_API_KEY=votre_cle_mailjet
MAILJET_API_SECRET=votre_secret_mailjet

# ============================================
# 💬 MESSAGING APIs
# ============================================
TELEGRAM_BOT_TOKEN=votre_token_telegram
LINE_CHANNEL_ACCESS_TOKEN=votre_token_line
KAKAO_REST_API_KEY=votre_cle_kakao

# ============================================
# 🎬 VIDEO & TTS APIs
# ============================================
DID_API_KEY=votre_cle_did
ELEVENLABS_API_KEY=votre_cle_elevenlabs

# ============================================
# 🔧 UTILITAIRES
# ============================================
# Redis (optionnel)
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=

# Cache TTL
CACHE_TTL_CHAT=3600
CACHE_TTL_EMBEDDINGS=86400

# Webhooks (optionnel)
WEBHOOK_1_URL=
WEBHOOK_1_SECRET=
WEBHOOK_1_EVENTS=

# ============================================
# EXCHANGE RATE (sans clé API)
# ============================================
EXCHANGERATE_API_KEY=
```

---

## 📊 Résumé par Catégorie

### ✅ Clés Déjà Configurées (Finance)
- `FINNHUB_API_KEY` : `d4s2nu1r01qvsjbf5ti0d4s2nu1r01qvsjbf5tig`
- `ALPHAVANTAGE_API_KEY` : `CVXV9XDIJNQJNI4B`
- `TWELVE_DATA_API_KEY` : `80dae489f6a540fb94e55e66c067f53a`
- `POLYGON_API_KEY` : `XdLxa1aElMtXguFg32VxeTegonov0IGFxsx`

### 🔴 Clés Essentielles (Minimum Requis)
- `JWT_SECRET_KEY` (générer avec : `python -c "import secrets; print(secrets.token_urlsafe(32))"`)
- Au moins 1 provider IA : `GROQ_API_KEY` ou `MISTRAL_API_KEY` ou `GEMINI_API_KEY`

### 🟡 Clés Recommandées (Pour Fonctionnalités Complètes)
- `NEWSAPI_ORG_KEY` ou `NEWSDATA_IO_KEY` (actualités)
- `OPENWEATHER_API_KEY` ou `WEATHERAPI_KEY` (météo)
- `OPENCAGE_API_KEY` ou `POSITIONSTACK_API_KEY` (géocodage)

### 🟢 Clés Optionnelles (Fonctionnalités Avancées)
- Toutes les autres selon vos besoins

---

## 🔗 Liens pour Obtenir les Clés API

### 🤖 IA & LLM
- **Groq** : https://console.groq.com/
- **Mistral** : https://console.mistral.ai/
- **Gemini** : https://makersuite.google.com/app/apikey
- **OpenRouter** : https://openrouter.ai/keys
- **Cohere** : https://dashboard.cohere.com/
- **Anthropic** : https://console.anthropic.com/
- **Perplexity** : https://www.perplexity.ai/settings/api
- **Hugging Face** : https://huggingface.co/settings/tokens

### 📰 News
- **NewsAPI.org** : https://newsapi.org/register
- **NewsData.io** : https://newsdata.io/register

### 🌤️ Weather
- **OpenWeatherMap** : https://openweathermap.org/api
- **WeatherAPI** : https://www.weatherapi.com/signup.aspx

### 🌍 Translation
- **Google Translate** : https://console.cloud.google.com/
- **DeepL** : https://www.deepl.com/pro-api
- **Yandex** : https://translate.yandex.com/developers/keys

### 📍 Geocoding
- **OpenCage** : https://opencagedata.com/api
- **PositionStack** : https://positionstack.com/signup

### 🎮 Entertainment
- **TMDB** : https://www.themoviedb.org/settings/api
- **Yelp** : https://www.yelp.com/developers
- **Spotify** : https://developer.spotify.com/dashboard

### 🖼️ Media
- **Unsplash** : https://unsplash.com/developers
- **Pexels** : https://www.pexels.com/api/
- **Giphy** : https://developers.giphy.com/
- **Pixabay** : https://pixabay.com/api/docs/

### 📚 Books
- **Google Books** : https://console.cloud.google.com/

### 🍎 Nutrition
- **Spoonacular** : https://spoonacular.com/food-api
- **Edamam** : https://developer.edamam.com/

### ⚽ Sports
- **API-Sports** : https://api-sports.io/

### 🚀 Space
- **NASA** : https://api.nasa.gov/

### 📧 Email
- **SendGrid** : https://app.sendgrid.com/settings/api_keys
- **Mailgun** : https://app.mailgun.com/app/account/security/api_keys
- **Mailjet** : https://app.mailjet.com/account/api_keys

### 💬 Messaging
- **Telegram** : https://core.telegram.org/bots/tutorial
- **Line** : https://developers.line.biz/
- **Kakao** : https://developers.kakao.com/

### 🎬 Video & TTS
- **D-ID** : https://studio.d-id.com/
- **ElevenLabs** : https://elevenlabs.io/

---

## 📝 Instructions d'Installation sur le Serveur

### 1. Créer le fichier `.env`

```bash
cd /chemin/vers/backend
nano .env
```

### 2. Copier le contenu ci-dessus et remplacer les valeurs

### 3. Générer JWT_SECRET_KEY

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

Copier le résultat dans `JWT_SECRET_KEY=`

### 4. Ajouter les clés API une par une

Remplacer `votre_cle_xxx` par les vraies clés obtenues depuis les liens ci-dessus.

### 5. Vérifier la configuration

```bash
python3 scripts/check_api_config.py
python3 scripts/validate_production.py
```

---

## ⚠️ Notes Importantes

1. **Sécurité** : Ne jamais commiter le fichier `.env` dans Git
2. **Priorités** : Commencer par les clés essentielles, puis ajouter les autres selon les besoins
3. **Quotas** : Vérifier les quotas gratuits de chaque API
4. **Fallback** : Le système utilise automatiquement le fallback si une API échoue

---

**Total APIs** : 50+ APIs disponibles  
**Clés Configurées** : 4 (Finance)  
**Clés à Ajouter** : Selon vos besoins

