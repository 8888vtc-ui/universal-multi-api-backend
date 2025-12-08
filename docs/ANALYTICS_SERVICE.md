# 📊 Analytics & Monitoring - Documentation Complète

## Vue d'ensemble

Le **Service Analytics & Monitoring** collecte automatiquement les métriques d'utilisation de l'API et fournit des données pour le dashboard. Il permet de suivre les performances, les erreurs, et l'utilisation des endpoints.

---

## 🚀 Fonctionnalités

### 1. Collecte Automatique
- Middleware qui enregistre toutes les requêtes automatiquement
- Temps de réponse mesuré pour chaque requête
- Codes de statut HTTP trackés
- Erreurs capturées et enregistrées

### 2. Métriques Disponibles
- Nombre total de requêtes
- Temps de réponse moyen/min/max
- Répartition par endpoint
- Répartition par code de statut
- Requêtes par jour
- Top endpoints

### 3. Analyse d'Erreurs
- Types d'erreurs
- Endpoints avec erreurs
- Erreurs par jour
- Taux d'erreur

### 4. Dashboard Complet
- Endpoint unique pour toutes les données
- Résumé avec métriques clés
- Prêt pour intégration frontend

---

## 📡 Endpoints

### GET `/api/analytics/metrics`

Obtenir les métriques d'utilisation.

**Query Parameters:**
- `days` (optional): Nombre de jours (défaut: 7, max: 30)
- `endpoint` (optional): Filtrer par endpoint spécifique

**Response:**
```json
{
  "success": true,
  "period_days": 7,
  "total_requests": 1250,
  "avg_response_time_ms": 145.32,
  "status_codes": {
    "200": 1150,
    "404": 50,
    "500": 50
  },
  "endpoints": {
    "/api/search/universal": 300,
    "/api/chat": 250,
    "/api/finance/crypto": 200
  },
  "methods": {
    "GET": 800,
    "POST": 450
  },
  "requests_by_day": {
    "2024-12-01": 180,
    "2024-12-02": 175
  },
  "requests_per_day": 178.57
}
```

### GET `/api/analytics/errors`

Obtenir les statistiques d'erreurs.

**Query Parameters:**
- `days` (optional): Nombre de jours (défaut: 7, max: 30)

**Response:**
```json
{
  "success": true,
  "period_days": 7,
  "total_errors": 50,
  "error_types": {
    "HTTPException": 30,
    "ValueError": 20
  },
  "error_endpoints": {
    "/api/video/avatar/create": 15,
    "/api/chat": 10
  },
  "errors_by_day": {
    "2024-12-01": 8,
    "2024-12-02": 7
  },
  "errors_per_day": 7.14
}
```

### GET `/api/analytics/endpoints/top`

Obtenir les endpoints les plus utilisés.

**Query Parameters:**
- `days` (optional): Nombre de jours (défaut: 7)
- `limit` (optional): Nombre d'endpoints (défaut: 10, max: 50)

**Response:**
```json
{
  "success": true,
  "endpoints": [
    {
      "endpoint": "/api/search/universal",
      "requests": 300,
      "percentage": 24.0
    },
    {
      "endpoint": "/api/chat",
      "requests": 250,
      "percentage": 20.0
    }
  ],
  "total": 10
}
```

### GET `/api/analytics/performance`

Obtenir les statistiques de performance.

**Query Parameters:**
- `days` (optional): Nombre de jours (défaut: 7)

**Response:**
```json
{
  "success": true,
  "avg_response_time_ms": 145.32,
  "min_response_time_ms": 12.5,
  "max_response_time_ms": 2500.0,
  "total_requests": 1250
}
```

### GET `/api/analytics/dashboard`

Obtenir toutes les données pour le dashboard.

**Query Parameters:**
- `days` (optional): Nombre de jours (défaut: 7)

**Response:**
```json
{
  "success": true,
  "period_days": 7,
  "metrics": { /* métriques complètes */ },
  "errors": { /* erreurs complètes */ },
  "top_endpoints": [ /* top endpoints */ ],
  "performance": { /* performance */ },
  "summary": {
    "total_requests": 1250,
    "total_errors": 50,
    "error_rate": 4.0,
    "avg_response_time_ms": 145.32
  }
}
```

---

## 🔧 Configuration

### Middleware Automatique

Le middleware `AnalyticsMiddleware` est automatiquement ajouté à l'application et collecte :
- Toutes les requêtes vers `/api/*`
- Temps de réponse
- Code de statut
- User ID (si présent dans headers `X-User-ID`)
- IP address

### Base de Données

Les métriques sont stockées dans SQLite :
- Fichier: `./data/analytics.db`
- Tables: `metrics`, `errors`
- Index automatiques pour performance

---

## 💡 Exemples d'Utilisation

### Exemple 1: Obtenir métriques
```python
import httpx

async def get_metrics():
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "http://localhost:8000/api/analytics/metrics",
            params={"days": 7}
        )
        return response.json()
```

### Exemple 2: Dashboard complet
```python
async def get_dashboard():
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "http://localhost:8000/api/analytics/dashboard",
            params={"days": 30}
        )
        return response.json()
```

### Exemple 3: Top endpoints
```python
async def get_top_endpoints():
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "http://localhost:8000/api/analytics/endpoints/top",
            params={"days": 7, "limit": 5}
        )
        return response.json()
```

---

## 📊 Métriques Collectées

### Par Requête
- Timestamp
- Endpoint
- Méthode HTTP
- Code de statut
- Temps de réponse (ms)
- User ID (optionnel)
- IP address

### Par Erreur
- Timestamp
- Endpoint
- Type d'erreur
- Message d'erreur
- User ID (optionnel)

---

## 🔒 Confidentialité

- IP addresses stockées pour analytics uniquement
- User IDs optionnels (peuvent être anonymisés)
- Données stockées localement (SQLite)
- Pas de partage externe

---

## 📈 Améliorations Futures

- [ ] Export données (CSV, JSON)
- [ ] Alertes automatiques (email, webhook)
- [ ] Graphiques temps réel
- [ ] Comparaison périodes
- [ ] Prédictions de charge
- [ ] Intégration Grafana/Prometheus

---

**Dernière mise à jour**: Décembre 2024  
**Version**: 1.0.0


<<<<<<< Updated upstream
=======





>>>>>>> Stashed changes
