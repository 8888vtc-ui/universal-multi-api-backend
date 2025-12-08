# 🧠 Recherche Intelligente IA + Data

## Vue d'ensemble

Le **Moteur de Recherche IA + Data** combine l'intelligence artificielle avec la recherche multi-sources pour fournir des réponses enrichies et contextualisées.

---

## 🎯 Principe

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Requête    │ ──► │ IA Analyse  │ ──► │ APIs Data   │ ──► │ IA Synthèse │
│  Utilisateur│     │  Intention  │     │ Multi-Source│     │  Enrichie   │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
```

### Flux détaillé :

1. **IA Analyse** : Comprend la requête (intention, entités, contexte)
2. **Planification** : Sélectionne les APIs pertinentes
3. **Recherche** : Exécute les requêtes en parallèle
4. **IA Synthèse** : Résume, analyse et enrichit les résultats

---

## 📡 Endpoints

### 1. Recherche Principale

```http
POST /api/ai-search/search
```

**Requête** :
```json
{
    "query": "Dois-je investir dans Bitcoin aujourd'hui?",
    "use_cache": true,
    "include_raw_data": true
}
```

**Réponse** :
```json
{
    "query": "Dois-je investir dans Bitcoin aujourd'hui?",
    "intent": "recommendation",
    "sources_count": 3,
    "ai_synthesis": "Le Bitcoin est actuellement à $95,000 (+2.5% sur 24h). Les actualités montrent un intérêt institutionnel croissant avec l'approbation des ETF. Cependant, la volatilité reste élevée. Pour un investissement, considérez votre tolérance au risque et diversifiez votre portefeuille.",
    "ai_recommendations": [
        "Ne jamais investir plus que ce que vous pouvez perdre",
        "Diversifiez entre plusieurs actifs",
        "Suivez les tendances du marché régulièrement"
    ],
    "confidence_score": 0.85,
    "execution_time_ms": 1250.5,
    "cached": false,
    "data": {
        "coincap": {...},
        "news": {...}
    }
}
```

### 2. Analyse de Requête

```http
GET /api/ai-search/analyze?query=prix bitcoin
```

**Réponse** :
```json
{
    "query": "prix bitcoin",
    "intent": "realtime",
    "entities": ["bitcoin", "prix"],
    "categories": ["finance_crypto"],
    "freshness": "live",
    "confidence": 0.9,
    "ai_analyzed": true
}
```

### 3. Recherche Rapide

```http
POST /api/ai-search/quick?query=météo Paris&max_sources=2
```

**Réponse** :
```json
{
    "query": "météo Paris",
    "intent": "realtime",
    "synthesis": "À Paris, il fait actuellement 15°C avec un ciel partiellement nuageux. Prévisions: pluie légère attendue en soirée.",
    "recommendations": ["Prenez un parapluie", "Températures fraîches le matin"],
    "sources": 2,
    "execution_time_ms": 450.2
}
```

### 4. Liste des Intentions

```http
GET /api/ai-search/intents
```

### 5. Liste des Catégories

```http
GET /api/ai-search/categories
```

### 6. Exemples

```http
GET /api/ai-search/examples
```

---

## 🎯 Types d'Intentions

| Intention | Description | Mots-clés |
|-----------|-------------|-----------|
| `information` | Recherche factuelle | "qu'est-ce que", "définition", "histoire" |
| `realtime` | Données temps réel | "prix", "météo", "actualité" |
| `comparison` | Comparer options | "vs", "meilleur", "différence" |
| `recommendation` | Obtenir conseils | "dois-je", "conseille", "suggère" |
| `action` | Effectuer une action | "traduire", "raccourcir", "créer" |
| `exploration` | Découvrir | "random", "surprends-moi" |
| `analysis` | Analyser données | "tendance", "évolution", "statistique" |

---

## 📂 Catégories d'APIs

| Catégorie | APIs |
|-----------|------|
| `finance_crypto` | CoinCap, CoinGecko |
| `finance_stocks` | Yahoo Finance, Alpha Vantage |
| `news` | NewsAPI, The Guardian |
| `weather` | OpenMeteo, OpenWeatherMap |
| `wikipedia` | Wikipedia |
| `books` | Google Books |
| `countries` | REST Countries |
| `translation` | LibreTranslate, DeepL |
| `images` | Unsplash, Pexels, Lorem Picsum |
| `quotes` | Quotable, Advice Slip |
| `github` | GitHub API |
| `entertainment` | TMDB, OMDB |

---

## 🚀 Exemples d'Utilisation

### Python

```python
import httpx
import asyncio

async def ai_search(query: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/api/ai-search/search",
            json={"query": query, "use_cache": True}
        )
        return response.json()

# Exemple
result = asyncio.run(ai_search("Dois-je investir dans Bitcoin?"))
print(result["ai_synthesis"])
print(result["ai_recommendations"])
```

### cURL

```bash
# Recherche IA
curl -X POST "http://localhost:8000/api/ai-search/search" \
  -H "Content-Type: application/json" \
  -d '{"query": "Météo Paris demain", "use_cache": true}'

# Analyse
curl "http://localhost:8000/api/ai-search/analyze?query=prix%20bitcoin"

# Recherche rapide
curl -X POST "http://localhost:8000/api/ai-search/quick?query=actualités%20tech&max_sources=2"
```

---

## 📊 Performance

| Métrique | Valeur |
|----------|--------|
| Temps moyen (sans cache) | 1-2 secondes |
| Temps moyen (avec cache) | < 100ms |
| Sources interrogées | 2-6 par requête |
| Score de confiance | 0.5 - 1.0 |

---

## 💡 Avantages

1. **Réponses intelligentes** : Pas juste des données brutes
2. **Multi-sources** : Combine plusieurs APIs pour une vue complète
3. **Contextuel** : L'IA comprend l'intention de l'utilisateur
4. **Recommandations** : Conseils personnalisés basés sur les données
5. **Cache optimisé** : Réponses rapides pour requêtes fréquentes
6. **Score de confiance** : Évalue la qualité des résultats

---

## 🔧 Configuration

### Variables d'environnement

```env
# AI Providers (au moins un requis)
GROQ_API_KEY=...
MISTRAL_API_KEY=...
ANTHROPIC_API_KEY=...

# Cache (optionnel mais recommandé)
REDIS_URL=redis://localhost:6379
```

---

## 🎓 Cas d'Usage

### 1. Assistant de Recherche

```json
{
    "query": "Qu'est-ce que le machine learning et comment l'apprendre?"
}
```
→ Synthèse Wikipedia + recommandations de livres + ressources

### 2. Veille Marché

```json
{
    "query": "Analyse du marché crypto aujourd'hui"
}
```
→ Prix temps réel + actualités + analyse IA des tendances

### 3. Aide à la Décision

```json
{
    "query": "Python vs JavaScript pour le backend?"
}
```
→ Comparaison objective + cas d'usage + recommandations

### 4. Exploration

```json
{
    "query": "Découvrir un pays intéressant"
}
```
→ Pays aléatoire + infos + citation inspirante

---

## ✅ Résumé

Le **Moteur de Recherche IA + Data** offre :

- 🧠 **IA** pour comprendre et synthétiser
- 📡 **Multi-sources** pour des données complètes
- ⚡ **Performance** avec cache intelligent
- 💡 **Recommandations** personnalisées
- 🎯 **Pertinence** grâce à la détection d'intention

**Endpoint principal** : `POST /api/ai-search/search`






