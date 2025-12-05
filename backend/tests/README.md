# Tests - Moteur de Recherche Universel

## Structure des Tests

```
tests/
├── __init__.py
├── test_search.py              # Tests unitaires
└── test_search_integration.py  # Tests d'intégration
```

## Installation

```bash
pip install -r requirements.txt
```

Les dépendances de test sont incluses dans `requirements.txt` :
- `pytest==7.4.3`
- `pytest-asyncio==0.21.1`
- `pytest-cov==4.1.0`

## Exécution des Tests

### Tous les tests
```bash
pytest
```

### Tests unitaires uniquement
```bash
pytest tests/test_search.py -v
```

### Tests d'intégration uniquement
```bash
pytest tests/test_search_integration.py -v -m integration
```

### Tests avec couverture de code
```bash
pytest --cov=routers.search --cov-report=html
```

### Tests rapides (sans intégration)
```bash
pytest -m "not integration and not slow"
```

## Types de Tests

### Tests Unitaires (`test_search.py`)
- ✅ Détection d'intention
- ✅ Modèles Pydantic (SearchRequest, SearchResult)
- ✅ Fonctions de recherche individuelles (avec mocks)
- ✅ Gestion d'erreurs
- ✅ Cas limites

**Avantages** : Rapides, ne nécessitent pas d'APIs réelles

### Tests d'Intégration (`test_search_integration.py`)
- ✅ Recherche universelle avec vraies APIs
- ✅ Performance
- ✅ Gestion d'erreurs avec APIs réelles

**Note** : Peuvent échouer si les clés API ne sont pas configurées (c'est normal)

## Marqueurs Pytest

- `@pytest.mark.unit` : Tests unitaires
- `@pytest.mark.integration` : Tests d'intégration
- `@pytest.mark.slow` : Tests lents (> 1s)

## Exemples d'Exécution

### Test spécifique
```bash
pytest tests/test_search.py::TestDetectSearchIntent::test_detect_finance_intent -v
```

### Tests avec output détaillé
```bash
pytest -v -s
```

### Tests en parallèle (si pytest-xdist installé)
```bash
pytest -n auto
```

## Configuration

Le fichier `pytest.ini` configure :
- Mode asyncio automatique
- Marqueurs personnalisés
- Options par défaut

## Résolution de Problèmes

### Erreur "Module not found"
```bash
# S'assurer d'être dans le dossier backend
cd backend
pytest
```

### Erreur "asyncio"
```bash
# Vérifier que pytest-asyncio est installé
pip install pytest-asyncio
```

### Tests d'intégration échouent
C'est normal si les clés API ne sont pas configurées. Les tests d'intégration sont marqués pour être ignorés en cas d'erreur.

## Prochaines Étapes

1. ✅ Tests unitaires créés
2. ✅ Tests d'intégration créés
3. ⏳ Tests de performance
4. ⏳ Tests de charge
5. ⏳ Documentation complète


