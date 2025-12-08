# 🔑 Liens pour Obtenir les Clés API Finance

## ⚠️ APIs Nécessitant une Clé API (Gratuites)

### 1. **Finnhub** ⭐ PRIORITÉ
- **Quota gratuit** : 60 appels/minute, illimité par jour
- **Fonctionnalités** : Stocks, Actualités, Profils d'entreprises
- **Lien** : https://finnhub.io/
- **Étapes** :
  1. Aller sur https://finnhub.io/
  2. Cliquer sur "Get Free API Key"
  3. Créer un compte (gratuit)
  4. Copier la clé API
  5. Ajouter dans `.env` : `FINNHUB_API_KEY=votre_cle_ici`

---

### 2. **Twelve Data**
- **Quota gratuit** : 800 appels/jour, 8 appels/minute
- **Fonctionnalités** : Stocks, Crypto, Forex
- **Lien** : https://twelvedata.com/
- **Étapes** :
  1. Aller sur https://twelvedata.com/
  2. Cliquer sur "Get Free API Key"
  3. Créer un compte (gratuit)
  4. Copier la clé API
  5. Ajouter dans `.env` : `TWELVE_DATA_API_KEY=votre_cle_ici`

---

### 3. **Polygon.io**
- **Quota gratuit** : 5 appels/minute, illimité par jour
- **Fonctionnalités** : Stocks, Options, Forex, Données historiques
- **Lien** : https://polygon.io/
- **Étapes** :
  1. Aller sur https://polygon.io/
  2. Cliquer sur "Get Started" ou "Sign Up"
  3. Créer un compte (gratuit)
  4. Copier la clé API depuis le dashboard
  5. Ajouter dans `.env` : `POLYGON_API_KEY=votre_cle_ici`

---

### 4. **Alpha Vantage**
- **Quota gratuit** : 25 appels/jour
- **Fonctionnalités** : Stocks, Forex, Crypto
- **Lien** : https://www.alphavantage.co/support/#api-key
- **Étapes** :
  1. Aller sur https://www.alphavantage.co/support/#api-key
  2. Remplir le formulaire (nom, email)
  3. Cliquer sur "GET FREE API KEY"
  4. Vérifier votre email et copier la clé API
  5. Ajouter dans `.env` : `ALPHAVANTAGE_API_KEY=votre_cle_ici`

---

## 📋 Résumé des Liens

| API | Lien | Quota Gratuit |
|-----|------|---------------|
| **Finnhub** | https://finnhub.io/ | 60/min, illimité/jour |
| **Twelve Data** | https://twelvedata.com/ | 800/jour, 8/min |
| **Polygon.io** | https://polygon.io/ | 5/min, illimité/jour |
| **Alpha Vantage** | https://www.alphavantage.co/support/#api-key | 25/jour |

---

## 🔧 Configuration

Une fois les clés obtenues, ajouter dans `backend/.env` :

```env
# APIs Finance (optionnel mais recommandé)
FINNHUB_API_KEY=votre_cle_finnhub
TWELVE_DATA_API_KEY=votre_cle_twelve_data
POLYGON_API_KEY=votre_cle_polygon
ALPHAVANTAGE_API_KEY=votre_cle_alphavantage
```

Puis redéployer sur Fly.io :

```bash
cd backend
flyctl deploy --remote-only
```

---

## ⚡ Priorité Recommandée

1. **Finnhub** ⭐ (le plus généreux : 60/min, illimité/jour)
2. **Polygon.io** (5/min, illimité/jour)
3. **Twelve Data** (800/jour)
4. **Alpha Vantage** (25/jour seulement)

---

**Date** : 07/12/2025



## ⚠️ APIs Nécessitant une Clé API (Gratuites)

### 1. **Finnhub** ⭐ PRIORITÉ
- **Quota gratuit** : 60 appels/minute, illimité par jour
- **Fonctionnalités** : Stocks, Actualités, Profils d'entreprises
- **Lien** : https://finnhub.io/
- **Étapes** :
  1. Aller sur https://finnhub.io/
  2. Cliquer sur "Get Free API Key"
  3. Créer un compte (gratuit)
  4. Copier la clé API
  5. Ajouter dans `.env` : `FINNHUB_API_KEY=votre_cle_ici`

---

### 2. **Twelve Data**
- **Quota gratuit** : 800 appels/jour, 8 appels/minute
- **Fonctionnalités** : Stocks, Crypto, Forex
- **Lien** : https://twelvedata.com/
- **Étapes** :
  1. Aller sur https://twelvedata.com/
  2. Cliquer sur "Get Free API Key"
  3. Créer un compte (gratuit)
  4. Copier la clé API
  5. Ajouter dans `.env` : `TWELVE_DATA_API_KEY=votre_cle_ici`

---

### 3. **Polygon.io**
- **Quota gratuit** : 5 appels/minute, illimité par jour
- **Fonctionnalités** : Stocks, Options, Forex, Données historiques
- **Lien** : https://polygon.io/
- **Étapes** :
  1. Aller sur https://polygon.io/
  2. Cliquer sur "Get Started" ou "Sign Up"
  3. Créer un compte (gratuit)
  4. Copier la clé API depuis le dashboard
  5. Ajouter dans `.env` : `POLYGON_API_KEY=votre_cle_ici`

---

### 4. **Alpha Vantage**
- **Quota gratuit** : 25 appels/jour
- **Fonctionnalités** : Stocks, Forex, Crypto
- **Lien** : https://www.alphavantage.co/support/#api-key
- **Étapes** :
  1. Aller sur https://www.alphavantage.co/support/#api-key
  2. Remplir le formulaire (nom, email)
  3. Cliquer sur "GET FREE API KEY"
  4. Vérifier votre email et copier la clé API
  5. Ajouter dans `.env` : `ALPHAVANTAGE_API_KEY=votre_cle_ici`

---

## 📋 Résumé des Liens

| API | Lien | Quota Gratuit |
|-----|------|---------------|
| **Finnhub** | https://finnhub.io/ | 60/min, illimité/jour |
| **Twelve Data** | https://twelvedata.com/ | 800/jour, 8/min |
| **Polygon.io** | https://polygon.io/ | 5/min, illimité/jour |
| **Alpha Vantage** | https://www.alphavantage.co/support/#api-key | 25/jour |

---

## 🔧 Configuration

Une fois les clés obtenues, ajouter dans `backend/.env` :

```env
# APIs Finance (optionnel mais recommandé)
FINNHUB_API_KEY=votre_cle_finnhub
TWELVE_DATA_API_KEY=votre_cle_twelve_data
POLYGON_API_KEY=votre_cle_polygon
ALPHAVANTAGE_API_KEY=votre_cle_alphavantage
```

Puis redéployer sur Fly.io :

```bash
cd backend
flyctl deploy --remote-only
```

---

## ⚡ Priorité Recommandée

1. **Finnhub** ⭐ (le plus généreux : 60/min, illimité/jour)
2. **Polygon.io** (5/min, illimité/jour)
3. **Twelve Data** (800/jour)
4. **Alpha Vantage** (25/jour seulement)

---

**Date** : 07/12/2025



