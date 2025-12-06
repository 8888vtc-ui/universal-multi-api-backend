# 📚 Exemples d'Utilisation

**Version** : 2.3.0  
**Guide** : Exemples pratiques pour utiliser toutes les fonctionnalités

---

## 📁 Fichiers d'Exemples

### 🆕 Nouveautés v2.3.0

- **`examples/api_examples.py`** ⭐ - Exemples des nouvelles fonctionnalités
  - Health checks (simple, deep, Kubernetes)
  - Métriques Prometheus
  - Request tracing (X-Request-ID)
  - Security headers
  - Gestion d'erreurs
  - Performance

### Fonctionnalités Existantes

- **`examples/search_examples.py`** - Moteur de recherche universel
- **`examples/assistant_examples.py`** - Assistant personnel IA
- **`examples/video_examples.py`** - Service vidéo IA
- **`examples/analytics_examples.py`** - Analytics & monitoring

---

## 🚀 Utilisation

### Prérequis

1. **Démarrer le serveur** :
   ```bash
   cd backend
   python main.py
   # Ou utiliser le script amélioré
   python scripts/start_server.py
   ```

2. **Exécuter les exemples** :
   ```bash
   # Exemples API v2.3.0
   python examples/api_examples.py
   
   # Exemples recherche
   python examples/search_examples.py
   
   # Exemples assistant
   python examples/assistant_examples.py
   ```

---

## 📖 Exemples par Catégorie

### 1. Health Checks

```python
import httpx

# Health check simple
response = await client.get("http://localhost:8000/api/health")

# Deep health check (tous les services)
response = await client.get("http://localhost:8000/api/health/deep")

# Kubernetes probes
response = await client.get("http://localhost:8000/api/health/ready")
response = await client.get("http://localhost:8000/api/health/live")
```

### 2. Métriques

```python
# Métriques JSON
response = await client.get("http://localhost:8000/api/metrics")

# Format Prometheus
response = await client.get("http://localhost:8000/api/metrics/prometheus")

# Résumé
response = await client.get("http://localhost:8000/api/metrics/summary")
```

### 3. Request Tracing

```python
# Sans ID (généré automatiquement)
response = await client.get("http://localhost:8000/api/health")
request_id = response.headers["X-Request-ID"]

# Avec ID personnalisé
response = await client.get(
    "http://localhost:8000/api/health",
    headers={"X-Request-ID": "my-custom-id-123"}
)
```

### 4. Security Headers

```python
response = await client.get("http://localhost:8000/api/health")

# Vérifier les headers
print(response.headers["X-Content-Type-Options"])  # nosniff
print(response.headers["X-Frame-Options"])         # DENY
print(response.headers["X-XSS-Protection"])      # 1; mode=block
print(response.headers["X-API-Version"])          # 2.3.0
```

### 5. Chat IA

```python
response = await client.post(
    "http://localhost:8000/api/chat",
    json={
        "message": "Bonjour!",
        "language": "fr"
    }
)
```

### 6. Recherche Universelle

```python
response = await client.post(
    "http://localhost:8000/api/search/universal",
    json={
        "query": "bitcoin prix",
        "max_results_per_category": 5
    }
)
```

---

## 🔧 Script de Démarrage Amélioré

Utilisez `scripts/start_server.py` pour un démarrage avec vérifications :

```bash
python scripts/start_server.py
```

**Fonctionnalités** :
- ✅ Vérifie les prérequis
- ✅ Vérifie la disponibilité du port
- ✅ Détecte si le serveur est déjà démarré
- ✅ Messages informatifs

---

## 📊 Intégration avec Prometheus

### Configuration Prometheus

```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'universal-api'
    static_configs:
      - targets: ['localhost:8000']
    metrics_path: '/api/metrics/prometheus'
    scrape_interval: 15s
```

### Exemple de Requête

```bash
curl http://localhost:8000/api/metrics/prometheus
```

---

## 🐳 Intégration Kubernetes

### Health Checks

```yaml
livenessProbe:
  httpGet:
    path: /api/health/live
    port: 8000
  initialDelaySeconds: 30
  periodSeconds: 10

readinessProbe:
  httpGet:
    path: /api/health/ready
    port: 8000
  initialDelaySeconds: 10
  periodSeconds: 5
```

---

## 📝 Notes

- Tous les exemples utilisent `httpx` pour les requêtes async
- Les exemples vérifient automatiquement que le serveur est démarré
- Les Request IDs sont automatiquement générés si non fournis
- Les Security Headers sont ajoutés à toutes les réponses

---

## 🔗 Liens Utiles

- **Documentation API** : http://localhost:8000/docs
- **Guide de démarrage** : [QUICK_START.md](QUICK_START.md)
- **Guide de déploiement** : [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)

---

*Dernière mise à jour : v2.3.0*



