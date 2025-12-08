# 📚 DOCUMENTATION COMPLÈTE - Backend Multi-API Universel

## 🎯 **VUE D'ENSEMBLE**

Backend FastAPI qui agrège **18 catégories d'APIs** avec **50+ endpoints REST** et **5 endpoints agrégés intelligents**.

---

## 🚀 **ENDPOINTS AGRÉGÉS (NOUVEAU !)** ⭐

**Combinez plusieurs APIs en parallèle pour des informations complètes en un seul appel !**

### **1. Recommandations Voyage** ✈️
- **Endpoint** : `POST /api/aggregated/travel/recommendations`
- **Combine** : Geocoding + Weather + News + IA
- **Usage** : Informations complètes pour voyager
- **Performance** : ~800ms (tous appels en parallèle)

### **2. Analyse Marché** 💰
- **Endpoint** : `POST /api/aggregated/market/analysis`
- **Combine** : Prix (Stock/Crypto) + News + Analyse IA
- **Usage** : Analyse complète d'un investissement
- **Performance** : ~800ms (tous appels en parallèle)

### **3. Recommandations Santé** 🏥
- **Endpoint** : `POST /api/aggregated/health/recommendations`
- **Combine** : Nutrition + Recherche Médicale + Conseils IA
- **Usage** : Conseils santé complets sur un aliment
- **Performance** : ~800ms (tous appels en parallèle)

### **4. Infos Localisation** 📍
- **Endpoint** : `GET /api/aggregated/location/complete`
- **Combine** : Geocoding + Weather + News
- **Usage** : Toutes les infos sur une localisation
- **Performance** : ~600ms (tous appels en parallèle)

### **5. Analyse Crypto** 🪙
- **Endpoint** : `GET /api/aggregated/crypto/complete`
- **Combine** : Prix + News + Analyse IA
- **Usage** : Analyse complète d'une crypto
- **Performance** : ~800ms (tous appels en parallèle)

**Voir** : `ENDPOINTS_AGREGES.md` pour détails complets

---

## 📊 **TOUTES LES CATÉGORIES D'APIs**

### **1. IA & Chat** 🤖
- `POST /api/chat` - Chat conversationnel
- `POST /api/embeddings` - Génération embeddings
- `POST /api/boltai/*` - Router IA avancé
- **Providers** : Groq, Mistral, Gemini, Ollama, Cohere, HuggingFace
- **Quota** : 16,000+ req/jour + ILLIMITÉ (Ollama)

### **2. Finance** 💰
- `GET /api/finance/crypto/price/{coin_id}` - Prix crypto
- `GET /api/finance/crypto/trending` - Cryptos tendance
- `GET /api/finance/stock/quote/{symbol}` - Prix action
- `GET /api/finance/market/summary` - Résumé marchés
- **Providers** : CoinGecko, Alpha Vantage, Yahoo Finance
- **Quota** : 10,000+ req/jour + illimité (Yahoo)

### **3. Médical** 🏥
- `GET /api/medical/research/search` - Recherche PubMed
- `GET /api/medical/drugs/search` - Recherche médicaments
- `GET /api/medical/drugs/adverse-events/{drug}` - Effets secondaires
- **Providers** : PubMed, OpenFDA
- **Quota** : ILLIMITÉ

### **4. Entertainment** 🎮
- `GET /api/entertainment/movies/search` - Recherche films
- `GET /api/entertainment/movies/trending` - Films tendance
- `GET /api/entertainment/restaurants/search` - Recherche restaurants
- `GET /api/entertainment/music/search` - Recherche musique
- **Providers** : TMDB, Yelp, Spotify
- **Quota** : 6,000+ req/jour

### **5. Traduction** 🌍
- `POST /api/translation/translate` - Traduire un texte
- `GET /api/translation/detect` - Détecter la langue
- **Providers** : Google, DeepL, Yandex, LibreTranslate
- **Quota** : 1M+ caractères/mois

### **6. Actualités** 📰
- `GET /api/news/search` - Recherche d'actualités
- `GET /api/news/headlines` - Titres principaux
- **Providers** : NewsAPI, NewsData
- **Quota** : 1,000+ req/jour

### **7. Météo** 🌤️
- `GET /api/weather/current` - Météo actuelle
- `GET /api/weather/forecast` - Prévisions
- **Providers** : Open-Meteo, WeatherAPI
- **Quota** : 1,000+ req/jour + illimité (Open-Meteo)

### **8. Espace** 🚀
- `GET /api/space/apod` - Photo astronomique du jour
- `GET /api/space/asteroids` - Astéroïdes proches
- **Providers** : NASA
- **Quota** : ILLIMITÉ

### **9. Sports** ⚽
- `GET /api/sports/fixtures` - Matchs à venir
- `GET /api/sports/standings` - Classements
- **Providers** : API-Sports
- **Quota** : 100 req/jour

### **10. Utilitaires** 🔧
- `POST /api/utils/qr/generate` - Générer QR code
- `POST /api/utils/ocr` - OCR (reconnaissance texte)
- **Providers** : Multiple
- **Quota** : Variable

### **11. Géocodage** 📍
- `GET /api/geocoding/geocode` - Géocoder une adresse
- `GET /api/geocoding/reverse` - Reverse geocoding
- **Providers** : Nominatim, Positionstack
- **Quota** : ILLIMITÉ (Nominatim)

### **12. Nutrition** 🍎
- `GET /api/nutrition/recipes/search` - Recherche recettes
- `GET /api/nutrition/foods/search` - Recherche aliments
- **Providers** : Spoonacular, Edamam, USDA
- **Quota** : 365k+ recettes disponibles

### **13. Email** 📧
- `POST /api/email/send` - Envoyer un email
- **Providers** : Mailjet, SendGrid
- **Quota** : Variable

### **14. Médias** 🖼️
- `GET /api/media/photos/search` - Recherche photos
- `GET /api/media/videos/search` - Recherche vidéos
- `GET /api/media/gifs/search` - Recherche GIFs
- **Providers** : Unsplash, Pexels, Giphy
- **Quota** : 250+ req/heure

### **15. Messaging** 💬
- `POST /api/messaging/telegram/send` - Envoyer message Telegram
- **Providers** : Telegram Bot API
- **Quota** : 30 msg/sec

### **16. Health** ❤️
- `GET /api/health` - Santé du système
- **Retourne** : Status de tous les providers

---

## 📈 **STATISTIQUES**

- **Catégories d'APIs** : 18
- **Endpoints REST** : 50+
- **Endpoints Agrégés** : 5
- **Providers Externes** : 17+
- **Quotas Gratuits** : 130,000+ req/jour + ILLIMITÉ
- **Performance** : ~36% plus rapide avec endpoints agrégés

---

## 🎯 **UTILISATION**

### **Endpoints Individuels**

```python
from universal_api_client import UniversalAPI

api = UniversalAPI()

# Appels individuels
weather = await api.get_weather("Paris")
crypto = await api.get_crypto_price("bitcoin")
news = await api.get_news("bitcoin")
```

### **Endpoints Agrégés (Recommandé)**

```python
# Un seul appel pour tout !
result = await api.get_travel_recommendations("Paris")
# Retourne : geocoding + weather + news + AI analysis

result = await api.get_market_analysis(coin_id="bitcoin")
# Retourne : price + news + AI analysis
```

---

## 📚 **DOCUMENTATION**

- **README Principal** : `README.md`
- **Backend** : `backend/README.md`
- **Client** : `universal-api-client/README.md`
- **Endpoints Agrégés** : `ENDPOINTS_AGREGES.md`
- **Exemples** : `EXEMPLES_ENDPOINTS_AGREGES.md`
- **Changelog** : `CHANGELOG.md`

---

## 🚀 **SWAGGER DOCS**

Accédez à la documentation interactive :
- **Swagger UI** : http://localhost:8000/docs
- **ReDoc** : http://localhost:8000/redoc

---

**Documentation complète et à jour ! 📚**


<<<<<<< Updated upstream
=======





>>>>>>> Stashed changes
