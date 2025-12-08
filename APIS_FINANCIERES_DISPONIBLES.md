# 💰 APIs Financières Disponibles

## 📊 APIs Directes

### 1. **Finance Router** (`/api/finance/*`)

#### Cryptomonnaies
- `GET /api/finance/crypto/price/{coin_id}` - Prix d'une crypto (CoinGecko)
  - Exemple : `/api/finance/crypto/price/bitcoin`
  - Retourne : Prix, variation 24h, market cap

- `GET /api/finance/crypto/trending` - Cryptos tendance (CoinGecko)
  - Retourne : Liste des cryptos en tendance

#### Actions (Stocks)
- `GET /api/finance/stock/quote/{symbol}` - Prix d'une action
  - Exemple : `/api/finance/stock/quote/AAPL` (Apple)
  - Exemple : `/api/finance/stock/quote/MSFT` (Microsoft)
  - Exemple : `/api/finance/stock/quote/TSLA` (Tesla)
  - Retourne : Prix, variation, volume, market cap, P/E ratio

#### Marchés Généraux
- `GET /api/finance/market/summary` - Résumé des indices majeurs
  - Retourne : S&P 500, Dow Jones, NASDAQ avec prix et variations

**Providers** : CoinGecko, Alpha Vantage, Yahoo Finance (illimité)

---

### 2. **CoinCap Router** (`/api/coincap/*`)

- `GET /api/coincap/assets?search={query}` - Recherche cryptos
  - Exemple : `/api/coincap/assets?search=bitcoin`
  - Retourne : Liste de cryptos correspondantes

- `GET /api/coincap/assets/{asset_id}` - Info détaillée d'une crypto
  - Exemple : `/api/coincap/assets/bitcoin`
  - Retourne : Prix, market cap, volume, supply

- `GET /api/coincap/assets/{asset_id}/history` - Historique des prix
  - Exemple : `/api/coincap/assets/bitcoin/history?interval=d1`
  - Intervalles : m1, m5, m15, m30, h1, h2, h6, h12, d1

- `GET /api/coincap/markets` - Données des marchés
  - Retourne : Liste des marchés avec volumes

- `GET /api/coincap/exchanges` - Liste des exchanges
  - Retourne : Exchanges disponibles

**Provider** : CoinCap API (illimité)

---

### 3. **Exchange Rate Router** (`/api/exchange/*`)

- `GET /api/exchange/rates/{base}` - Taux de change
  - Exemple : `/api/exchange/rates/USD`
  - Retourne : Tous les taux de change depuis USD

- `GET /api/exchange/convert` - Conversion de devises
  - Exemple : `/api/exchange/convert?amount=100&from_currency=USD&to_currency=EUR`
  - Retourne : Montant converti

- `GET /api/exchange/currencies` - Liste des devises supportées
  - Retourne : Liste de toutes les devises

**Provider** : ExchangeRate API (1.5k/mois)

---

### 4. **News Router** (`/api/news/*`)

- `GET /api/news/search?q={query}` - Recherche d'actualités
  - Exemple : `/api/news/search?q=bitcoin&limit=5`
  - Retourne : Articles récents sur le sujet

- `GET /api/news/headlines` - Titres principaux
  - Exemple : `/api/news/headlines?country=us&category=business`
  - Retourne : Titres d'actualités financières

**Providers** : NewsAPI, NewsData (1k+/jour)

---

## 🚀 APIs Agrégées (Recommandées)

### 5. **Market Analysis** (`/api/aggregated/market/analysis`)

**POST** `/api/aggregated/market/analysis`

**Body** :
```json
{
  "symbol": "AAPL",  // OU
  "coin_id": "bitcoin",
  "include_news": true,
  "include_ai_analysis": true
}
```

**Retourne** :
- Prix actuel (stock ou crypto)
- Actualités récentes
- Analyse IA complète

**Performance** : ~800ms (tous appels en parallèle)

---

### 6. **Crypto Complete** (`/api/aggregated/crypto/complete`)

**GET** `/api/aggregated/crypto/complete?coin_id=bitcoin`

**Retourne** :
- Prix actuel
- Market cap
- Actualités
- Analyse IA

**Performance** : ~800ms

---

## 📋 Mapping Requête → API

### Pour "bitcoin", "btc", "ethereum", "eth"
1. ✅ `/api/finance/crypto/price/bitcoin` (CoinGecko)
2. ✅ `/api/coincap/assets?search=bitcoin` (CoinCap)
3. ✅ `/api/news/search?q=bitcoin` (Actualités)

### Pour "nasdaq", "apple", "aapl", "msft", "tesla"
1. ✅ `/api/finance/stock/quote/AAPL` (Yahoo Finance)
2. ✅ `/api/finance/market/summary` (Pour NASDAQ global)
3. ✅ `/api/news/search?q=apple` (Actualités)

### Pour "marché", "bourse", "indices"
1. ✅ `/api/finance/market/summary` (Yahoo Finance)
2. ✅ `/api/news/search?q=market` (Actualités)

### Pour "euro", "dollar", "devise"
1. ✅ `/api/exchange/rates/USD` (Exchange Rate)
2. ✅ `/api/exchange/convert?amount=100&from_currency=USD&to_currency=EUR`

---

## 💡 Recommandations pour l'Expert Financier

### Stratégie Multi-API

1. **Détecter le type de requête** :
   - Crypto → CoinGecko + CoinCap + News
   - Action → Yahoo Finance + News
   - Marché → Market Summary + News
   - Devise → Exchange Rate

2. **Appels en parallèle** :
   - Utiliser `asyncio.gather()` pour appeler plusieurs APIs simultanément
   - Fallback automatique si une API échoue

3. **Utiliser les APIs agrégées** :
   - `/api/aggregated/market/analysis` pour analyses complètes
   - `/api/aggregated/crypto/complete` pour cryptos

4. **Combiner avec News** :
   - Toujours inclure `/api/news/search` pour contexte actuel
   - Les actualités aident l'IA à comprendre le contexte

---

## 🔧 Exemple d'Implémentation

```python
async def fetch_finance_data_smart(query: str) -> str:
    """Récupère les données financières intelligemment"""
    
    query_lower = query.lower()
    
    # Détecter le type
    if any(kw in query_lower for kw in ["bitcoin", "btc", "ethereum", "eth", "crypto"]):
        # Crypto
        tasks = [
            _fetch_api("finance", f"/api/finance/crypto/price/bitcoin"),
            _fetch_api("coincap", f"/api/coincap/assets?search=bitcoin"),
            _fetch_api("news", f"/api/news/search?q=bitcoin")
        ]
    elif any(kw in query_lower for kw in ["nasdaq", "apple", "aapl", "msft", "stock", "action"]):
        # Stock
        symbol = extract_symbol(query)  # "AAPL" depuis "apple"
        tasks = [
            _fetch_api("finance", f"/api/finance/stock/quote/{symbol}"),
            _fetch_api("finance", f"/api/finance/market/summary"),
            _fetch_api("news", f"/api/news/search?q={symbol}")
        ]
    elif any(kw in query_lower for kw in ["marché", "bourse", "indices", "market"]):
        # Market
        tasks = [
            _fetch_api("finance", f"/api/finance/market/summary"),
            _fetch_api("news", f"/api/news/search?q=market")
        ]
    else:
        # Général - essayer plusieurs
        tasks = [
            _fetch_api("finance", f"/api/finance/market/summary"),
            _fetch_api("news", f"/api/news/search?q={query}")
        ]
    
    # Appeler en parallèle
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Combiner les résultats
    context = "\n\n".join([r for r in results if r and not isinstance(r, Exception)])
    
    return context
```

---

## ✅ Résumé

**APIs disponibles pour l'expert financier** :
1. ✅ Finance (CoinGecko, Alpha Vantage, Yahoo Finance)
2. ✅ CoinCap (cryptos détaillées)
3. ✅ Exchange Rate (devises)
4. ✅ News (actualités financières)
5. ✅ Aggregated (analyses complètes)

**Total** : 5+ endpoints utilisables pour enrichir les réponses de l'expert financier !



## 📊 APIs Directes

### 1. **Finance Router** (`/api/finance/*`)

#### Cryptomonnaies
- `GET /api/finance/crypto/price/{coin_id}` - Prix d'une crypto (CoinGecko)
  - Exemple : `/api/finance/crypto/price/bitcoin`
  - Retourne : Prix, variation 24h, market cap

- `GET /api/finance/crypto/trending` - Cryptos tendance (CoinGecko)
  - Retourne : Liste des cryptos en tendance

#### Actions (Stocks)
- `GET /api/finance/stock/quote/{symbol}` - Prix d'une action
  - Exemple : `/api/finance/stock/quote/AAPL` (Apple)
  - Exemple : `/api/finance/stock/quote/MSFT` (Microsoft)
  - Exemple : `/api/finance/stock/quote/TSLA` (Tesla)
  - Retourne : Prix, variation, volume, market cap, P/E ratio

#### Marchés Généraux
- `GET /api/finance/market/summary` - Résumé des indices majeurs
  - Retourne : S&P 500, Dow Jones, NASDAQ avec prix et variations

**Providers** : CoinGecko, Alpha Vantage, Yahoo Finance (illimité)

---

### 2. **CoinCap Router** (`/api/coincap/*`)

- `GET /api/coincap/assets?search={query}` - Recherche cryptos
  - Exemple : `/api/coincap/assets?search=bitcoin`
  - Retourne : Liste de cryptos correspondantes

- `GET /api/coincap/assets/{asset_id}` - Info détaillée d'une crypto
  - Exemple : `/api/coincap/assets/bitcoin`
  - Retourne : Prix, market cap, volume, supply

- `GET /api/coincap/assets/{asset_id}/history` - Historique des prix
  - Exemple : `/api/coincap/assets/bitcoin/history?interval=d1`
  - Intervalles : m1, m5, m15, m30, h1, h2, h6, h12, d1

- `GET /api/coincap/markets` - Données des marchés
  - Retourne : Liste des marchés avec volumes

- `GET /api/coincap/exchanges` - Liste des exchanges
  - Retourne : Exchanges disponibles

**Provider** : CoinCap API (illimité)

---

### 3. **Exchange Rate Router** (`/api/exchange/*`)

- `GET /api/exchange/rates/{base}` - Taux de change
  - Exemple : `/api/exchange/rates/USD`
  - Retourne : Tous les taux de change depuis USD

- `GET /api/exchange/convert` - Conversion de devises
  - Exemple : `/api/exchange/convert?amount=100&from_currency=USD&to_currency=EUR`
  - Retourne : Montant converti

- `GET /api/exchange/currencies` - Liste des devises supportées
  - Retourne : Liste de toutes les devises

**Provider** : ExchangeRate API (1.5k/mois)

---

### 4. **News Router** (`/api/news/*`)

- `GET /api/news/search?q={query}` - Recherche d'actualités
  - Exemple : `/api/news/search?q=bitcoin&limit=5`
  - Retourne : Articles récents sur le sujet

- `GET /api/news/headlines` - Titres principaux
  - Exemple : `/api/news/headlines?country=us&category=business`
  - Retourne : Titres d'actualités financières

**Providers** : NewsAPI, NewsData (1k+/jour)

---

## 🚀 APIs Agrégées (Recommandées)

### 5. **Market Analysis** (`/api/aggregated/market/analysis`)

**POST** `/api/aggregated/market/analysis`

**Body** :
```json
{
  "symbol": "AAPL",  // OU
  "coin_id": "bitcoin",
  "include_news": true,
  "include_ai_analysis": true
}
```

**Retourne** :
- Prix actuel (stock ou crypto)
- Actualités récentes
- Analyse IA complète

**Performance** : ~800ms (tous appels en parallèle)

---

### 6. **Crypto Complete** (`/api/aggregated/crypto/complete`)

**GET** `/api/aggregated/crypto/complete?coin_id=bitcoin`

**Retourne** :
- Prix actuel
- Market cap
- Actualités
- Analyse IA

**Performance** : ~800ms

---

## 📋 Mapping Requête → API

### Pour "bitcoin", "btc", "ethereum", "eth"
1. ✅ `/api/finance/crypto/price/bitcoin` (CoinGecko)
2. ✅ `/api/coincap/assets?search=bitcoin` (CoinCap)
3. ✅ `/api/news/search?q=bitcoin` (Actualités)

### Pour "nasdaq", "apple", "aapl", "msft", "tesla"
1. ✅ `/api/finance/stock/quote/AAPL` (Yahoo Finance)
2. ✅ `/api/finance/market/summary` (Pour NASDAQ global)
3. ✅ `/api/news/search?q=apple` (Actualités)

### Pour "marché", "bourse", "indices"
1. ✅ `/api/finance/market/summary` (Yahoo Finance)
2. ✅ `/api/news/search?q=market` (Actualités)

### Pour "euro", "dollar", "devise"
1. ✅ `/api/exchange/rates/USD` (Exchange Rate)
2. ✅ `/api/exchange/convert?amount=100&from_currency=USD&to_currency=EUR`

---

## 💡 Recommandations pour l'Expert Financier

### Stratégie Multi-API

1. **Détecter le type de requête** :
   - Crypto → CoinGecko + CoinCap + News
   - Action → Yahoo Finance + News
   - Marché → Market Summary + News
   - Devise → Exchange Rate

2. **Appels en parallèle** :
   - Utiliser `asyncio.gather()` pour appeler plusieurs APIs simultanément
   - Fallback automatique si une API échoue

3. **Utiliser les APIs agrégées** :
   - `/api/aggregated/market/analysis` pour analyses complètes
   - `/api/aggregated/crypto/complete` pour cryptos

4. **Combiner avec News** :
   - Toujours inclure `/api/news/search` pour contexte actuel
   - Les actualités aident l'IA à comprendre le contexte

---

## 🔧 Exemple d'Implémentation

```python
async def fetch_finance_data_smart(query: str) -> str:
    """Récupère les données financières intelligemment"""
    
    query_lower = query.lower()
    
    # Détecter le type
    if any(kw in query_lower for kw in ["bitcoin", "btc", "ethereum", "eth", "crypto"]):
        # Crypto
        tasks = [
            _fetch_api("finance", f"/api/finance/crypto/price/bitcoin"),
            _fetch_api("coincap", f"/api/coincap/assets?search=bitcoin"),
            _fetch_api("news", f"/api/news/search?q=bitcoin")
        ]
    elif any(kw in query_lower for kw in ["nasdaq", "apple", "aapl", "msft", "stock", "action"]):
        # Stock
        symbol = extract_symbol(query)  # "AAPL" depuis "apple"
        tasks = [
            _fetch_api("finance", f"/api/finance/stock/quote/{symbol}"),
            _fetch_api("finance", f"/api/finance/market/summary"),
            _fetch_api("news", f"/api/news/search?q={symbol}")
        ]
    elif any(kw in query_lower for kw in ["marché", "bourse", "indices", "market"]):
        # Market
        tasks = [
            _fetch_api("finance", f"/api/finance/market/summary"),
            _fetch_api("news", f"/api/news/search?q=market")
        ]
    else:
        # Général - essayer plusieurs
        tasks = [
            _fetch_api("finance", f"/api/finance/market/summary"),
            _fetch_api("news", f"/api/news/search?q={query}")
        ]
    
    # Appeler en parallèle
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Combiner les résultats
    context = "\n\n".join([r for r in results if r and not isinstance(r, Exception)])
    
    return context
```

---

## ✅ Résumé

**APIs disponibles pour l'expert financier** :
1. ✅ Finance (CoinGecko, Alpha Vantage, Yahoo Finance)
2. ✅ CoinCap (cryptos détaillées)
3. ✅ Exchange Rate (devises)
4. ✅ News (actualités financières)
5. ✅ Aggregated (analyses complètes)

**Total** : 5+ endpoints utilisables pour enrichir les réponses de l'expert financier !



