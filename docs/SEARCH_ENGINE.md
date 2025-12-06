# 🔍 Moteur de Recherche Universel - Documentation Complète

## Vue d'ensemble

Le **Moteur de Recherche Universel** est un endpoint unique qui agrège intelligemment **TOUTES les APIs disponibles** en un seul appel. Il permet de rechercher dans 10+ catégories différentes simultanément avec détection automatique d'intention.

---

## 🚀 Fonctionnalités Principales

### 1. Recherche Multi-Catégories
- Recherche parallèle dans toutes les catégories d'APIs
- Détection automatique d'intention
- Résultats agrégés avec scoring de pertinence

### 2. Cache Intelligent
- Cache Redis pour résultats fréquents (TTL: 5 minutes)
- Réduction de 30%+ des appels API
- Performance optimale pour requêtes répétées

### 3. Scoring de Pertinence
- Calcul dynamique basé sur :
  - Mots-clés dans le titre (poids fort)
  - Mots-clés dans le contenu (poids moyen)
  - Correspondance avec intention détectée (bonus)
- Tri automatique par pertinence décroissante

### 4. Métriques de Performance
- Temps de réponse en millisecondes
- Nombre de catégories recherchées
- Indicateur de cache

---

## 📡 Endpoints

### POST `/api/search/universal`

Recherche universelle complète dans toutes les catégories.

**Request Body:**
```json
{
  "query": "bitcoin prix",
  "categories": ["finance", "news"],  // Optionnel: auto-détection si omis
  "max_results_per_category": 5,
  "language": "fr"
}
```

**Response:**
```json
{
  "query": "bitcoin prix",
  "total_results": 12,
  "categories_searched": ["finance", "news"],
  "results": {
    "finance": [
      {
        "category": "finance",
        "title": "Prix Bitcoin",
        "content": {"bitcoin": {"usd": 50000}},
        "source": "CoinGecko",
        "relevance_score": 0.95,
        "url": "https://www.coingecko.com/en/coins/bitcoin"
      }
    ],
    "news": [
      {
        "category": "news",
        "title": "Bitcoin atteint 50k$",
        "content": {
          "description": "Le bitcoin a atteint...",
          "publishedAt": "2024-12-04",
          "source": "TechCrunch"
        },
        "source": "TechCrunch",
        "relevance_score": 0.88,
        "url": "https://example.com/article"
      }
    ]
  },
  "ai_summary": "Résumé IA des résultats trouvés...",
  "suggested_queries": [],
  "performance": {
    "total_time_ms": 1250.5,
    "categories_count": 2,
    "cached": false
  }
}
```

### GET `/api/search/quick?q=...`

Recherche rapide avec paramètres simplifiés.

**Query Parameters:**
- `q` (required): Query de recherche
- `categories` (optional): Catégories séparées par virgule (ex: "finance,news")
- `limit` (optional): Résultats par catégorie (défaut: 5)

**Exemple:**
```
GET /api/search/quick?q=bitcoin&categories=finance,news&limit=3
```

### GET `/api/search/categories`

Liste toutes les catégories de recherche disponibles.

**Response:**
```json
{
  "categories": [
    {
      "id": "finance",
      "name": "Finance",
      "description": "Cryptomonnaies, actions, marchés financiers",
      "keywords": ["bitcoin", "crypto", "stock", "bourse", "prix"]
    },
    {
      "id": "news",
      "name": "Actualités",
      "description": "Articles de presse, breaking news",
      "keywords": ["actualité", "news", "nouvelle", "événement"]
    }
    // ... autres catégories
  ],
  "total": 10
}
```

---

## 🎯 Catégories Disponibles

| Catégorie | Description | APIs Utilisées |
|-----------|-------------|----------------|
| **finance** | Cryptomonnaies, actions, marchés | CoinGecko, Yahoo Finance, Alpha Vantage |
| **news** | Articles de presse | NewsAPI, NewsData.io |
| **weather** | Météo et prévisions | Open-Meteo, WeatherAPI |
| **geocoding** | Géolocalisation | Nominatim, OpenCage, Positionstack |
| **medical** | Recherche médicale | PubMed, OpenFDA |
| **entertainment** | Films, restaurants, musique | TMDB, Yelp, Spotify |
| **nutrition** | Recettes, aliments | Spoonacular, Edamam, USDA |
| **space** | Données spatiales | NASA APIs |
| **sports** | Matchs, classements | API-Football |
| **media** | Photos, images | Unsplash, Pexels |

---

## 🔍 Détection Automatique d'Intention

Le moteur détecte automatiquement l'intention de recherche à partir des mots-clés :

**Exemples:**
- `"bitcoin prix"` → Détecte: `finance`
- `"actualité technologie"` → Détecte: `news`
- `"météo Paris"` → Détecte: `weather`
- `"bitcoin actualité"` → Détecte: `finance` + `news`

Si aucune intention n'est détectée, le moteur recherche dans **toutes les catégories**.

---

## ⚡ Performance

### Cache Redis
- **TTL**: 5 minutes
- **Réduction**: 30%+ des appels API
- **Temps de réponse**: < 1ms depuis cache

### Recherche Parallèle
- Toutes les catégories recherchées simultanément
- Temps de réponse moyen: **1-2 secondes**
- Avec cache: **< 1ms**

### Métriques
Chaque réponse inclut des métriques de performance :
```json
{
  "performance": {
    "total_time_ms": 1250.5,  // Temps total en millisecondes
    "categories_count": 2,     // Nombre de catégories recherchées
    "cached": false            // Si résultat vient du cache
  }
}
```

---

## 📊 Scoring de Pertinence

Le score de pertinence est calculé dynamiquement :

1. **Score de base**: 0.5
2. **Bonus titre**: +0.3 par mot-clé trouvé (max 0.9)
3. **Bonus contenu**: +0.1 par mot-clé trouvé (max 0.3)
4. **Bonus catégorie**: +0.1 si catégorie correspond à intention

**Score final**: Normalisé entre 0 et 1

Les résultats sont **automatiquement triés** par score décroissant.

---

## 💡 Exemples d'Utilisation

### Exemple 1: Recherche Finance
```python
import httpx

async def search_bitcoin():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/api/search/universal",
            json={
                "query": "bitcoin prix",
                "categories": ["finance"],
                "max_results_per_category": 5
            }
        )
        return response.json()

# Résultat: Prix Bitcoin, cryptos tendance, etc.
```

### Exemple 2: Recherche Multi-Catégories
```python
async def search_comprehensive(query: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/api/search/universal",
            json={
                "query": query,
                # Pas de categories: auto-détection
                "max_results_per_category": 3,
                "language": "fr"
            }
        )
        return response.json()
```

### Exemple 3: Recherche Rapide
```python
async def quick_search(query: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "http://localhost:8000/api/search/quick",
            params={
                "q": query,
                "limit": 5
            }
        )
        return response.json()
```

---

## 🛠️ Configuration

### Variables d'Environnement

```bash
# Redis Cache (optionnel mais recommandé)
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=  # Optionnel
```

### Cache TTL

Le TTL du cache est configuré à **300 secondes (5 minutes)** dans le code. Pour modifier :

```python
# Dans backend/routers/search.py
cache_service.set("search", cache_key, response.dict(), ttl=300)  # Modifier ici
```

---

## 🧪 Tests

### Exécuter les Tests
```bash
cd backend
pytest tests/test_search.py -v
```

### Tests d'Intégration
```bash
pytest tests/test_search_integration.py -v -m integration
```

### Tests avec Couverture
```bash
pytest --cov=routers.search --cov-report=html
```

---

## 📈 Améliorations Futures

- [ ] Pagination avancée
- [ ] Filtres par date/source
- [ ] Recherche sémantique avec embeddings
- [ ] Historique de recherche utilisateur
- [ ] Recommandations personnalisées
- [ ] Export résultats (JSON, CSV)

---

## 🐛 Dépannage

### Cache ne fonctionne pas
- Vérifier que Redis est démarré: `redis-cli ping`
- Vérifier les variables d'environnement Redis
- Le système fonctionne sans cache (mode dégradé)

### Résultats vides
- Vérifier que les APIs sont configurées (clés API)
- Certaines APIs peuvent avoir des quotas limités
- Le moteur continue même si certaines APIs échouent

### Performance lente
- Vérifier le cache Redis
- Réduire `max_results_per_category`
- Spécifier des catégories au lieu d'auto-détection

---

## 📚 Ressources

- [Documentation Backend](../backend/README.md)
- [Tests](../backend/tests/README.md)
- [API Swagger](http://localhost:8000/docs) (quand serveur démarré)

---

**Dernière mise à jour**: Décembre 2024  
**Version**: 1.0.0



