# Scripts d'Optimisation et Benchmark

## benchmark.py

Script de benchmark pour tester les performances des endpoints.

### Usage

```bash
python scripts/benchmark.py
```

### Fonctionnalités

- Benchmark séquentiel de plusieurs endpoints
- Benchmark concurrent (requêtes parallèles)
- Statistiques détaillées (moyenne, médiane, P95, P99)
- Taux de succès et erreurs
- Requêtes par seconde

### Exemple de sortie

```
📊 Benchmark: GET /api/health
   Iterations: 100
   ✅ Succès: 100.0%
   ⏱️  Temps moyen: 12.34 ms
   📈 P95: 15.67 ms
   ⚠️  Erreurs: 0
```

## optimize.py

Script d'analyse et d'optimisation.

### Usage

```bash
python scripts/optimize.py
```

### Fonctionnalités

- Analyse de la base de données analytics
- Vérification des index
- Statistiques d'utilisation
- Détection des endpoints lents
- Suggestions d'optimisation
- Vérification de santé du système

### Exemple de sortie

```
📊 Analyse Base de Données Analytics
✅ Index existants: 2
📈 Statistiques:
   Métriques: 1,250
   Erreurs: 50
   Taille: 2.34 MB

💡 SUGGESTIONS D'OPTIMISATION
1. [Cache] Utiliser Redis pour cache des réponses fréquentes
   Impact: high | Effort: medium
```

## Intégration CI/CD

Ces scripts peuvent être intégrés dans un pipeline CI/CD :

```yaml
# Exemple GitHub Actions
- name: Run Benchmarks
  run: python scripts/benchmark.py

- name: Check Optimization
  run: python scripts/optimize.py
```



