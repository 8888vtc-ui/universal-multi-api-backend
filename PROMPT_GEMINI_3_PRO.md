# 🚀 PROMPT COMPLET POUR GEMINI 3 PRO
## Amélioration du Backend Multi-API Universel

---

## 📋 CONTEXTE DU PROJET

Tu es un expert en architecture backend Python/FastAPI. Tu vas améliorer un **backend multi-API universel** qui agrège 17+ providers (IA, Finance, Médical, Entertainment, etc.) avec un système de fallback intelligent.

**Architecture actuelle** :
- Backend FastAPI (Python 3.12+)
- 17+ providers API intégrés
- Système de fallback entre providers
- Cache Redis (optionnel)
- Frontend Next.js qui consomme les APIs
- Vision : un backend pour 50+ sous-projets frontend

**Structure du projet** :
```
backend/
├── main.py                    # Application FastAPI
├── services/
│   ├── ai_router.py          # Router multi-IA (7 providers)
│   ├── cache.py              # Cache Redis
│   └── external_apis/        # 17+ providers externes
├── routers/                  # 18 endpoints FastAPI
├── models/
│   └── schemas.py            # Modèles Pydantic
└── requirements.txt
```

---

## 🎯 OBJECTIFS PRINCIPAUX

Améliorer le backend pour le rendre **production-ready** avec :
1. ✅ Gestion robuste des quotas (persistance Redis)
2. ✅ Rate limiting et sécurité
3. ✅ Circuit breaker pattern
4. ✅ Logging structuré et monitoring
5. ✅ Tests complets
6. ✅ Documentation maximale
7. ✅ Gestion d'erreurs avancée
8. ✅ Performance et optimisation

---

## 🔧 AMÉLIORATIONS À IMPLÉMENTER

### **1. PERSISTANCE DES QUOTAS DANS REDIS** ⚠️ CRITIQUE

**Problème actuel** : Les quotas (`requests_today`) sont en mémoire et se réinitialisent au redémarrage.

**Solution à implémenter** :
- Utiliser Redis pour stocker les compteurs de quotas par provider
- Clés Redis : `quota:{provider_name}:{date}` (ex: `quota:groq:2024-12-15`)
- Reset automatique à minuit (TTL ou job scheduler)
- Méthodes dans `CacheService` :
  ```python
  def increment_quota_usage(provider: str, amount: int = 1) -> int
  def get_quota_usage(provider: str) -> int
  def reset_quota(provider: str)
  def check_quota_available(provider: str, daily_quota: int) -> bool
  ```
- Modifier `AIProvider.can_handle_request()` pour utiliser Redis
- Ajouter un middleware ou background task pour reset quotidien

**Fichiers à modifier** :
- `services/cache.py` - Ajouter méthodes quota
- `services/ai_router.py` - Utiliser Redis pour quotas
- `routers/health.py` - Afficher quotas depuis Redis

---

### **2. RATE LIMITING** ⚠️ SÉCURITÉ

**Implémenter** :
- Rate limiting par IP et par endpoint
- Utiliser `slowapi` ou `fastapi-limiter`
- Limites recommandées :
  - `/api/chat` : 60 req/min par IP
  - `/api/embeddings` : 30 req/min par IP
  - Autres endpoints : 100 req/min par IP
- Stocker les compteurs dans Redis
- Retourner `429 Too Many Requests` avec headers `X-RateLimit-*`

**Fichiers à créer/modifier** :
- `services/rate_limiter.py` - Nouveau service
- `main.py` - Ajouter middleware rate limiting

---

### **3. CIRCUIT BREAKER PATTERN** 🔄

**Implémenter** :
- Circuit breaker pour chaque provider API
- États : CLOSED → OPEN → HALF_OPEN
- Seuil : 5 erreurs consécutives → OPEN
- Timeout : 60 secondes avant retry (HALF_OPEN)
- Utiliser la librairie `circuitbreaker` ou implémenter custom

**Fichiers à créer/modifier** :
- `services/circuit_breaker.py` - Nouveau service
- `services/ai_router.py` - Intégrer circuit breaker
- `services/external_apis/*/router.py` - Intégrer dans tous les routers

---

### **4. RETRY AVEC BACKOFF EXPONENTIEL** 🔁

**Implémenter** :
- Retry automatique avec backoff exponentiel
- Max 3 tentatives par provider
- Délais : 1s, 2s, 4s
- Utiliser `tenacity` ou implémenter custom
- Ne retry que sur erreurs temporaires (5xx, timeout, rate limit)

**Fichiers à créer/modifier** :
- `services/retry_handler.py` - Nouveau service
- Intégrer dans tous les appels API externes

---

### **5. LOGGING STRUCTURÉ** 📊

**Implémenter** :
- Logging structuré avec JSON (pour parsing)
- Niveaux : DEBUG, INFO, WARNING, ERROR, CRITICAL
- Contextes à logger :
  - Provider utilisé
  - Temps de réponse
  - Quota restant
  - Erreurs avec stack trace
  - Requêtes utilisateur (sans données sensibles)
- Utiliser `python-json-logger` ou `structlog`
- Rotation des logs (logrotate ou Python)

**Fichiers à créer/modifier** :
- `services/logger.py` - Configuration logging
- Tous les fichiers - Remplacer `print()` par logger

---

### **6. MONITORING ET MÉTRIQUES** 📈

**Implémenter** :
- Endpoint `/api/metrics` (format Prometheus)
- Métriques à tracker :
  - Requêtes totales par endpoint
  - Temps de réponse (p50, p95, p99)
  - Taux d'erreur par provider
  - Quotas utilisés/restants
  - Cache hit/miss ratio
- Utiliser `prometheus-fastapi-instrumentator`
- Dashboard optionnel avec Grafana

**Fichiers à créer/modifier** :
- `services/metrics.py` - Nouveau service
- `routers/metrics.py` - Nouveau endpoint
- `main.py` - Ajouter instrumentation

---

### **7. GESTION D'ERREURS AVANCÉE** ⚠️

**Implémenter** :
- Exception handlers globaux FastAPI
- Classes d'exceptions custom :
  - `ProviderUnavailableError`
  - `QuotaExceededError`
  - `RateLimitExceededError`
  - `CircuitBreakerOpenError`
- Messages d'erreur user-friendly
- Codes d'erreur standardisés
- Logging automatique des erreurs

**Fichiers à créer/modifier** :
- `exceptions.py` - Nouvelles classes
- `main.py` - Exception handlers
- Tous les routers - Utiliser exceptions custom

---

### **8. VALIDATION ET SÉCURITÉ** 🔒

**Implémenter** :
- Validation stricte des inputs (Pydantic)
- Sanitization des inputs utilisateur
- Protection contre injection
- Headers de sécurité (CORS, CSP, etc.)
- Validation des API keys au démarrage
- Masquer les clés API dans les logs

**Fichiers à modifier** :
- `models/schemas.py` - Validation renforcée
- `main.py` - Headers sécurité
- `services/*` - Validation API keys

---

### **9. TESTS COMPLETS** 🧪

**Implémenter** :
- Tests unitaires (pytest)
- Tests d'intégration
- Tests de performance (load testing)
- Coverage minimum : 80%
- Tests à créer :
  - `tests/test_ai_router.py`
  - `tests/test_cache.py`
  - `tests/test_rate_limiter.py`
  - `tests/test_circuit_breaker.py`
  - `tests/test_routers/` (tous les endpoints)

**Fichiers à créer** :
- `tests/` - Structure complète
- `pytest.ini` - Configuration
- `.github/workflows/tests.yml` - CI/CD

---

### **10. DOCUMENTATION MAXIMALE** 📚

**Implémenter** :
- Docstrings complètes (Google style)
- Type hints partout
- README technique détaillé
- Guide de contribution
- Architecture decision records (ADRs)
- Diagrammes (Mermaid) dans la doc
- Exemples d'utilisation pour chaque endpoint
- Changelog (CHANGELOG.md)

**Fichiers à créer/modifier** :
- Tous les fichiers Python - Docstrings
- `docs/ARCHITECTURE.md`
- `docs/CONTRIBUTING.md`
- `docs/API.md`
- `CHANGELOG.md`

---

### **11. OPTIMISATION PERFORMANCE** ⚡

**Implémenter** :
- Async/await partout (pas de blocking calls)
- Connection pooling pour HTTP clients
- Cache agressif (TTL adaptatifs)
- Compression des réponses (gzip)
- Pagination pour grandes listes
- Lazy loading des providers

**Fichiers à modifier** :
- Tous les services - Optimiser async
- `main.py` - Middleware compression

---

### **12. CONFIGURATION ET ENVIRONNEMENT** ⚙️

**Implémenter** :
- Configuration centralisée (Pydantic Settings)
- Validation des variables d'environnement au démarrage
- Fichiers de config par environnement (.env.dev, .env.prod)
- `.env.example` complet avec descriptions
- Secrets management (optionnel : Vault, AWS Secrets)

**Fichiers à créer/modifier** :
- `config.py` - Configuration centralisée
- `.env.example` - Complet avec docs
- `main.py` - Validation au démarrage

---

### **13. HEALTH CHECKS AVANCÉS** ❤️

**Implémenter** :
- `/api/health` - Health check basique
- `/api/health/detailed` - Health check détaillé
- Vérifier :
  - Redis connectivity
  - Chaque provider API (ping)
  - Quotas disponibles
  - Circuit breakers status
- Retourner status code approprié (200, 503)

**Fichiers à modifier** :
- `routers/health.py` - Health checks avancés

---

### **14. BACKGROUND TASKS** 🔄

**Implémenter** :
- Task pour reset quotas quotidiens (minuit)
- Task pour health check périodique des providers
- Task pour nettoyage cache (expired keys)
- Utiliser `asyncio` ou `celery` (optionnel)

**Fichiers à créer/modifier** :
- `services/background_tasks.py` - Nouveau service
- `main.py` - Lancer tasks au démarrage

---

### **15. API VERSIONING** 📌

**Implémenter** :
- Versioning des APIs (`/api/v1/`, `/api/v2/`)
- Support de plusieurs versions simultanées
- Dépréciation progressive

**Fichiers à modifier** :
- `main.py` - Router versioning
- Tous les routers - Préfixe version

---

## 📝 AUTRES RECOMMANDATIONS SUPPLÉMENTAIRES

### **16. AUTHENTIFICATION & AUTORISATION** 🔐
- JWT tokens pour API privée
- API keys pour B2B
- Rate limiting différencié par utilisateur
- Endpoint `/api/auth/login`, `/api/auth/refresh`

### **17. WEBHOOKS & NOTIFICATIONS** 🔔
- Système de webhooks pour événements
- Notifications quand quota faible
- Alertes erreurs critiques

### **18. ANALYTICS & USAGE TRACKING** 📊
- Tracking anonymisé des endpoints utilisés
- Analytics par sous-projet frontend
- Dashboard usage (optionnel)

### **19. MULTI-TENANCY** 🏢
- Support multi-tenant (isolation données)
- Quotas par tenant
- Billing par tenant

### **20. OPENAPI/SCHEMA VALIDATION** ✅
- Validation automatique des schémas
- Génération de clients SDK
- Mock server pour tests

### **21. GRACEFUL SHUTDOWN** 🛑
- Shutdown propre (finir requêtes en cours)
- Nettoyage ressources
- Signal handlers

### **22. DATABASE PERSISTENCE** 💾
- Optionnel : SQLite/PostgreSQL pour logs persistants
- Historique des requêtes
- Analytics long terme

### **23. CACHING STRATÉGIE** 🗄️
- Cache multi-niveaux (memory + Redis)
- Cache warming
- Invalidation intelligente
- Cache tags pour invalidation groupée

### **24. LOAD BALANCING** ⚖️
- Support multi-instances
- Session affinity si nécessaire
- Health checks pour load balancer

### **25. INTERNATIONALISATION** 🌍
- Support i18n pour messages d'erreur
- Timezone handling
- Format dates/nombres localisés

---

## 🎯 PRIORITÉS D'IMPLÉMENTATION

### **Phase 1 : CRITIQUE (Semaine 1)**
1. ✅ Persistance quotas Redis
2. ✅ Rate limiting
3. ✅ Circuit breaker
4. ✅ Retry avec backoff
5. ✅ Logging structuré

### **Phase 2 : IMPORTANT (Semaine 2)**
6. ✅ Gestion erreurs avancée
7. ✅ Monitoring & métriques
8. ✅ Tests complets
9. ✅ Health checks avancés
10. ✅ Configuration centralisée

### **Phase 3 : AMÉLIORATION (Semaine 3)**
11. ✅ Documentation maximale
12. ✅ Optimisation performance
13. ✅ Background tasks
14. ✅ API versioning
15. ✅ Sécurité renforcée

---

## 📋 CONTRAINTES TECHNIQUES

- **Python** : 3.12+
- **FastAPI** : 0.115.0
- **Redis** : Disponible (optionnel mais recommandé)
- **Compatibilité** : Garder rétrocompatibilité avec frontend existant
- **Performance** : < 200ms pour 95% des requêtes
- **Uptime** : 99.9% avec fallback

---

## 🎨 STYLE DE CODE

- **PEP 8** strict
- **Type hints** partout
- **Docstrings** Google style
- **Async/await** pour I/O
- **Error handling** explicite
- **Tests** avant chaque commit

---

## 📦 DEPENDENCIES À AJOUTER

```txt
# Rate limiting
slowapi==0.1.9

# Circuit breaker
circuitbreaker==2.0.0

# Retry
tenacity==8.2.3

# Logging
python-json-logger==2.0.7
structlog==24.1.0

# Monitoring
prometheus-fastapi-instrumentator==7.0.0

# Testing
pytest==8.0.0
pytest-asyncio==0.23.3
pytest-cov==4.1.0
httpx==0.27.0  # Pour tests

# Configuration
pydantic-settings==2.6.0  # Déjà présent
```

---

## ✅ CHECKLIST DE VALIDATION

Avant de considérer le travail terminé, vérifier :

- [ ] Tous les quotas sont persistés dans Redis
- [ ] Rate limiting fonctionne sur tous les endpoints
- [ ] Circuit breaker testé avec providers défaillants
- [ ] Retry avec backoff testé
- [ ] Logs structurés en JSON
- [ ] Métriques Prometheus disponibles
- [ ] Tests avec coverage > 80%
- [ ] Documentation complète (docstrings + README)
- [ ] Health checks détaillés
- [ ] Configuration validée au démarrage
- [ ] Pas de régression (frontend fonctionne toujours)
- [ ] Performance maintenue (< 200ms p95)

---

## 🚀 DÉMARRAGE

1. Analyser le code existant
2. Implémenter les améliorations par priorité
3. Tester chaque fonctionnalité
4. Documenter chaque changement
5. Valider avec le checklist

**Commence par la Phase 1 (CRITIQUE) et progresse méthodiquement.**

---

## 💡 NOTES IMPORTANTES

- **Ne pas casser** la compatibilité avec le frontend existant
- **Toujours** utiliser async/await pour les appels I/O
- **Toujours** logger les erreurs avec contexte
- **Toujours** valider les inputs
- **Toujours** gérer les cas d'erreur
- **Documenter** chaque décision importante

---

**Bon courage ! 🚀**



