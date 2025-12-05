# 🔍 PROMPT POUR AUDIT COMPLET PAR OPUS

## 📋 CONTEXTE DU PROJET

Tu es un expert en architecture backend Python/FastAPI. Tu vas auditer un **backend multi-API universel** qui agrège 40+ providers (IA, Finance, Médical, Entertainment, etc.) avec un système de fallback intelligent.

**Architecture actuelle** :
- Backend FastAPI (Python 3.12+)
- 40+ providers API intégrés
- Système de fallback entre providers
- Cache Redis (optionnel)
- Authentification JWT
- Client API unifié (Python)
- Services avancés : Search, Video, Assistant, Analytics

**Structure du projet** :
```
backend/
├── main.py                    # Application FastAPI
├── routers/                   # 24 endpoints FastAPI
├── services/                  # Logique métier
│   ├── ai_router.py          # Router multi-IA (5 providers)
│   ├── api_health_checker.py # Vérification APIs
│   ├── api_fallback_manager.py # Gestion fallback
│   ├── cache.py              # Cache Redis
│   ├── circuit_breaker.py    # Circuit breaker
│   ├── retry_handler.py      # Retry logic
│   ├── rate_limiter.py       # Rate limiting
│   ├── auth.py               # Authentification JWT
│   ├── assistant/            # Assistant personnel
│   ├── analytics/            # Analytics
│   ├── video/                # Service vidéo
│   └── external_apis/        # 40+ providers externes
├── models/                   # Modèles Pydantic
├── middleware/               # Middleware
├── tests/                    # 61 tests
└── scripts/                  # Scripts utilitaires
```

---

## 🎯 OBJECTIFS DE L'AUDIT

Effectuer un **audit complet et critique** du projet pour identifier :

1. **Problèmes de sécurité**
2. **Bugs et erreurs**
3. **Problèmes de performance**
4. **Architecture et design patterns**
5. **Gestion d'erreurs**
6. **Tests et couverture**
7. **Documentation**
8. **Best practices**
9. **Variables d'environnement et configuration**
10. **Fallback et résilience**

---

## 🔍 POINTS À VÉRIFIER EN PRIORITÉ

### 1. **SÉCURITÉ** 🔴 CRITIQUE

- [ ] **Authentification JWT** : Vérifier la sécurité des tokens, expiration, refresh
- [ ] **Variables d'environnement** : Toutes les clés API sont-elles protégées ?
- [ ] **Validation des inputs** : Tous les endpoints valident-ils correctement ?
- [ ] **Rate limiting** : Est-il correctement implémenté partout ?
- [ ] **CORS** : Configuration sécurisée ?
- [ ] **Secrets management** : Les secrets sont-ils exposés quelque part ?
- [ ] **SQL Injection** : Protection contre les injections SQL (SQLite)
- [ ] **XSS/CSRF** : Protection contre les attaques

### 2. **GESTION DES ERREURS** ⚠️ IMPORTANT

- [ ] **Try/except** : Tous les appels API sont-ils dans des try/except ?
- [ ] **Messages d'erreur** : Les erreurs exposent-elles des informations sensibles ?
- [ ] **Logging** : Les erreurs sont-elles correctement loggées ?
- [ ] **HTTP Status Codes** : Les codes de statut sont-ils corrects ?
- [ ] **Fallback** : Le fallback fonctionne-t-il vraiment partout ?

### 3. **VARIABLES D'ENVIRONNEMENT** ⚠️ IMPORTANT

- [ ] **Vérification systématique** : Tous les providers vérifient-ils les clés API ?
- [ ] **Fallback garanti** : Y a-t-il toujours un fallback disponible ?
- [ ] **Health checks** : Les health checks sont-ils utilisés partout ?
- [ ] **Messages d'erreur** : Les erreurs de clés manquantes sont-elles claires ?

### 4. **PERFORMANCE** ⚠️ IMPORTANT

- [ ] **Async/await** : Tous les appels API sont-ils asynchrones ?
- [ ] **Cache** : Le cache Redis est-il utilisé efficacement ?
- [ ] **Quotas** : La gestion des quotas est-elle optimale ?
- [ ] **Concurrence** : Y a-t-il des problèmes de concurrence ?
- [ ] **Timeouts** : Les timeouts sont-ils configurés ?

### 5. **ARCHITECTURE** 💡 RECOMMANDÉ

- [ ] **Séparation des responsabilités** : Les routers/services sont-ils bien séparés ?
- [ ] **Code dupliqué** : Y a-t-il du code dupliqué à factoriser ?
- [ ] **Dépendances** : Les dépendances sont-elles correctement gérées ?
- [ ] **Singleton pattern** : Les singletons sont-ils correctement implémentés ?
- [ ] **Error handling** : La gestion d'erreurs est-elle cohérente ?

### 6. **TESTS** 💡 RECOMMANDÉ

- [ ] **Couverture** : La couverture de tests est-elle suffisante ?
- [ ] **Tests d'intégration** : Y a-t-il des tests d'intégration pour les fallbacks ?
- [ ] **Tests de sécurité** : Y a-t-il des tests de sécurité ?
- [ ] **Mocks** : Les mocks sont-ils correctement utilisés ?

### 7. **DOCUMENTATION** 💡 RECOMMANDÉ

- [ ] **Docstrings** : Toutes les fonctions ont-elles des docstrings ?
- [ ] **Type hints** : Les type hints sont-ils complets ?
- [ ] **README** : La documentation est-elle à jour ?
- [ ] **Exemples** : Y a-t-il des exemples d'utilisation ?

---

## 📝 FORMAT DE RÉPONSE ATTENDU

Pour chaque point vérifié, fournir :

1. **Statut** : ✅ OK / ⚠️ À améliorer / ❌ Problème critique
2. **Description** : Explication du problème ou de la bonne pratique
3. **Fichiers concernés** : Liste des fichiers à modifier
4. **Recommandations** : Solutions concrètes avec exemples de code
5. **Priorité** : 🔴 Critique / ⚠️ Important / 💡 Recommandé

---

## 🎯 QUESTIONS SPÉCIFIQUES

1. **Le système de fallback est-il vraiment robuste ?**
   - Vérifier que tous les routers utilisent le fallback
   - Vérifier qu'il y a toujours un provider disponible
   - Tester les scénarios d'échec

2. **Les variables d'environnement sont-elles toutes vérifiées ?**
   - Parcourir tous les providers
   - Vérifier les messages d'erreur
   - Vérifier les fallbacks

3. **Y a-t-il des fuites de mémoire ou des ressources non libérées ?**
   - Vérifier les connexions HTTP
   - Vérifier les connexions Redis
   - Vérifier les fichiers temporaires

4. **La gestion des quotas est-elle correcte ?**
   - Vérifier la persistance dans Redis
   - Vérifier les reset quotidiens
   - Vérifier les edge cases

5. **Les tests couvrent-ils tous les cas critiques ?**
   - Tests de fallback
   - Tests d'erreurs
   - Tests de sécurité

---

## 📊 RÉSUMÉ ATTENDU

À la fin de l'audit, fournir :

1. **Résumé exécutif** : Vue d'ensemble des problèmes
2. **Liste des problèmes critiques** : À corriger immédiatement
3. **Liste des améliorations** : À faire prochainement
4. **Score global** : Note sur 10 avec justification
5. **Recommandations prioritaires** : Top 5 actions à faire

---

## 🔧 COMMANDES UTILES

Pour tester le projet :

```bash
# Vérifier les dépendances
python scripts/check_dependencies.py

# Vérifier la configuration des APIs
python scripts/check_api_config.py

# Lancer les tests
pytest

# Vérifier le setup
python scripts/verify_setup.py

# Lancer le serveur
uvicorn main:app --reload
```

---

## 📚 FICHIERS CLÉS À EXAMINER

### Sécurité
- `backend/services/auth.py` - Authentification JWT
- `backend/services/rate_limiter.py` - Rate limiting
- `backend/main.py` - Configuration CORS, middleware

### Fallback
- `backend/services/api_fallback_manager.py` - Gestion fallback
- `backend/services/api_health_checker.py` - Health checks
- `backend/services/ai_router.py` - Router IA avec fallback

### Gestion d'erreurs
- `backend/services/circuit_breaker.py` - Circuit breaker
- `backend/services/retry_handler.py` - Retry logic
- Tous les routers dans `backend/routers/`

### Tests
- `backend/tests/` - Tous les tests
- `backend/pytest.ini` - Configuration pytest

---

## ✅ CRITÈRES DE SUCCÈS

L'audit est réussi si :

1. ✅ Tous les problèmes critiques sont identifiés
2. ✅ Des solutions concrètes sont proposées
3. ✅ Les fichiers concernés sont listés
4. ✅ Un plan d'action priorisé est fourni
5. ✅ Le code est analysé en profondeur (pas juste superficiel)

---

**Merci de faire un audit complet, critique et constructif !** 🚀


