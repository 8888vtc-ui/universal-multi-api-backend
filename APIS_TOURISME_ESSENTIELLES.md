# ✈️ APIs Tourisme Essentielles - Configuration Serveur

**Date** : Décembre 2024  
**Pour** : Configuration serveur production - Guide Touristique

---

## 📋 APIs Tourisme Essentielles

### ✅ APIs Sans Clé (Déjà Fonctionnelles)

Ces APIs fonctionnent **sans clé API** :

1. **Nominatim (OpenStreetMap)** - Géocodage
   - Quota : 1 requête/seconde (gratuit, illimité)
   - Status : ✅ Toujours disponible
   - Variable : Aucune (fonctionne sans clé)

2. **Open-Meteo** - Météo
   - Quota : Illimité (gratuit)
   - Status : ✅ Toujours disponible
   - Variable : Aucune (fonctionne sans clé)

3. **REST Countries** - Informations pays
   - Quota : Illimité (gratuit)
   - Status : ✅ Toujours disponible
   - Variable : Aucune (fonctionne sans clé)

4. **Exchange Rate API** - Taux de change
   - Quota : 1,500 requêtes/mois (gratuit)
   - Status : ✅ Toujours disponible
   - Variable : Aucune (fonctionne sans clé)

5. **LibreTranslate** - Traduction
   - Quota : Illimité (gratuit, local)
   - Status : ✅ Toujours disponible
   - Variable : Aucune (fonctionne sans clé)

---

## 🔑 APIs Nécessitant des Clés API

### 1. Géocodage (Recommandé)

#### OpenCage ⭐ PRIORITÉ
- **Variable** : `OPENCAGE_API_KEY`
- **Quota** : 2,500 requêtes/jour (gratuit)
- **Lien** : https://opencagedata.com/api
- **Usage** : Géocodage précis et rapide

#### Positionstack
- **Variable** : `POSITIONSTACK_API_KEY`
- **Quota** : 25,000 requêtes/mois (gratuit)
- **Lien** : https://positionstack.com/signup
- **Usage** : Alternative géocodage

**Configuration** :
```env
OPENCAGE_API_KEY=votre_cle_opencage
POSITIONSTACK_API_KEY=votre_cle_positionstack
```

---

### 2. Météo (Recommandé)

#### WeatherAPI ⭐ PRIORITÉ
- **Variable** : `WEATHERAPI_KEY`
- **Quota** : 1 million requêtes/mois (gratuit)
- **Lien** : https://www.weatherapi.com/signup.aspx
- **Usage** : Météo précise et prévisions

**Configuration** :
```env
WEATHERAPI_KEY=votre_cle_weatherapi
```

---

### 3. Actualités (Recommandé)

#### NewsAPI.org ⭐ PRIORITÉ
- **Variable** : `NEWSAPI_ORG_KEY`
- **Quota** : 100 requêtes/jour (gratuit)
- **Lien** : https://newsapi.org/register
- **Usage** : Actualités sur les destinations

#### NewsData.io
- **Variable** : `NEWSDATA_IO_KEY`
- **Quota** : 200 requêtes/jour (gratuit)
- **Lien** : https://newsdata.io/register
- **Usage** : Alternative actualités

**Configuration** :
```env
NEWSAPI_ORG_KEY=votre_cle_newsapi_org
NEWSDATA_IO_KEY=votre_cle_newsdata_io
```

---

### 4. Traduction (Recommandé)

#### Google Translate ⭐ PRIORITÉ
- **Variable** : `GOOGLE_TRANSLATE_API_KEY`
- **Quota** : 500,000 caractères/mois (gratuit)
- **Lien** : https://console.cloud.google.com/
- **Usage** : Traduction précise multi-langues

#### DeepL
- **Variable** : `DEEPL_API_KEY`
- **Quota** : 500,000 caractères/mois (gratuit)
- **Lien** : https://www.deepl.com/pro-api
- **Usage** : Traduction de qualité supérieure

#### Yandex Translate
- **Variable** : `YANDEX_TRANSLATE_API_KEY`
- **Quota** : 10,000,000 caractères/mois (gratuit)
- **Lien** : https://translate.yandex.com/developers/keys
- **Usage** : Alternative traduction

**Configuration** :
```env
GOOGLE_TRANSLATE_API_KEY=votre_cle_google_translate
DEEPL_API_KEY=votre_cle_deepl
YANDEX_TRANSLATE_API_KEY=votre_cle_yandex
```

---

### 5. Restaurants & Attractions (Recommandé)

#### Yelp ⭐ PRIORITÉ
- **Variable** : `YELP_API_KEY`
- **Quota** : 5,000 requêtes/jour (gratuit)
- **Lien** : https://www.yelp.com/developers
- **Usage** : Restaurants, attractions, activités

**Configuration** :
```env
YELP_API_KEY=votre_cle_yelp
```

---

### 6. Vols & Aviation (Recommandé)

#### Aviationstack ⭐ PRIORITÉ
- **Variable** : `AVIATIONSTACK_API_KEY`
- **Quota** : 1,000 requêtes/mois (gratuit)
- **Lien** : https://aviationstack.com/
- **Usage** : Recherche vols, statuts vols, horaires aéroports
- **Clé** : `6d42cb6dbbf72807d21b0275b3e3832f` ✅

**Configuration** :
```env
AVIATIONSTACK_API_KEY=6d42cb6dbbf72807d21b0275b3e3832f
```

---

## 📊 Configuration Complète pour le Serveur

### Fichier `.env` - Section Tourisme

```env
# ============================================
# ✈️ TOURISME APIs - ESSENTIELLES
# ============================================

# Géocodage (au moins 1 recommandé)
OPENCAGE_API_KEY=votre_cle_opencage
POSITIONSTACK_API_KEY=votre_cle_positionstack

# Météo (recommandé pour meilleure précision)
WEATHERAPI_KEY=votre_cle_weatherapi

# Actualités (au moins 1 recommandé)
NEWSAPI_ORG_KEY=votre_cle_newsapi_org
NEWSDATA_IO_KEY=votre_cle_newsdata_io

# Traduction (au moins 1 recommandé)
GOOGLE_TRANSLATE_API_KEY=votre_cle_google_translate
DEEPL_API_KEY=votre_cle_deepl
YANDEX_TRANSLATE_API_KEY=votre_cle_yandex

# Restaurants & Attractions
YELP_API_KEY=votre_cle_yelp

# Vols & Aviation
AVIATIONSTACK_API_KEY=6d42cb6dbbf72807d21b0275b3e3832f
```

---

## 🎯 Priorités Recommandées

### Priorité 1 (Minimum pour fonctionner)
- ✅ **Nominatim** (géocodage) - Déjà disponible sans clé
- ✅ **Open-Meteo** (météo) - Déjà disponible sans clé
- ✅ **REST Countries** (infos pays) - Déjà disponible sans clé
- ✅ **LibreTranslate** (traduction) - Déjà disponible sans clé

### Priorité 2 (Améliorer la qualité)
- 🔑 **OpenCage** - Géocodage plus rapide et précis
- 🔑 **WeatherAPI** - Météo plus détaillée
- 🔑 **NewsAPI.org** - Actualités sur destinations
- 🔑 **Google Translate** - Traduction meilleure qualité

### Priorité 3 (Fonctionnalités avancées)
- 🔑 **Yelp** - Restaurants et attractions
- 🔑 **DeepL** - Traduction premium
- 🔑 **Positionstack** - Fallback géocodage

---

## 📈 Résumé

### APIs Sans Clé (5)
- ✅ Nominatim (géocodage)
- ✅ Open-Meteo (météo)
- ✅ REST Countries (infos pays)
- ✅ Exchange Rate (devises)
- ✅ LibreTranslate (traduction)

### APIs Avec Clé (9)
- 🔑 OpenCage (géocodage)
- 🔑 Positionstack (géocodage)
- 🔑 WeatherAPI (météo)
- 🔑 NewsAPI.org (actualités)
- 🔑 NewsData.io (actualités)
- 🔑 Google Translate (traduction)
- 🔑 DeepL (traduction)
- 🔑 Yandex Translate (traduction)
- 🔑 Yelp (restaurants)
- 🔑 Aviationstack (vols) ✅ **CONFIGURÉ**

**Total** : **14 APIs tourisme** disponibles

---

## 🔗 Liens pour Obtenir les Clés

### Géocodage
- **OpenCage** : https://opencagedata.com/api
- **Positionstack** : https://positionstack.com/signup

### Météo
- **WeatherAPI** : https://www.weatherapi.com/signup.aspx

### Actualités
- **NewsAPI.org** : https://newsapi.org/register
- **NewsData.io** : https://newsdata.io/register

### Traduction
- **Google Translate** : https://console.cloud.google.com/
- **DeepL** : https://www.deepl.com/pro-api
- **Yandex** : https://translate.yandex.com/developers/keys

### Restaurants
- **Yelp** : https://www.yelp.com/developers

### Vols & Aviation
- **Aviationstack** : https://aviationstack.com/

---

## 💡 Endpoint Agrégé Tourisme

Le backend expose un endpoint spécialisé pour le tourisme :

**Endpoint** : `POST /api/aggregated/travel/recommendations`

**Combine automatiquement** :
- Géocodage (localisation)
- Météo (conditions actuelles)
- Actualités (news sur la destination)
- IA (recommandations personnalisées)
- Traduction (si nécessaire)

**Exemple** :
```json
POST /api/aggregated/travel/recommendations
{
  "destination": "Paris",
  "language": "fr",
  "include_weather": true,
  "include_news": true,
  "include_restaurants": true
}
```

**Résultat** : Informations complètes pour voyager en **1 seul appel** !

---

**Status** : ✅ **5 APIs sans clé** + **9 APIs avec clé** = **14 APIs tourisme disponibles**

**Clés Configurées** :
- ✅ `AVIATIONSTACK_API_KEY` : `6d42cb6dbbf72807d21b0275b3e3832f`

