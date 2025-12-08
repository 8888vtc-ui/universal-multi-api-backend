# 🧪 Test de Charge - 5000 Questions/Réponses

## Description

Script de test de charge qui génère 5000 questions/réponses pour détecter les erreurs et générer un rapport détaillé.

## Fonctionnalités

✅ **Test automatique de 5000 questions**
- Teste tous les experts avec des questions variées
- Détecte automatiquement les erreurs
- S'arrête dès qu'une erreur critique est détectée

✅ **Détection d'erreurs**
- Timeouts
- Réponses vides
- Erreurs HTTP (500, etc.)
- Réponses invalides
- Réponses trop courtes
- Erreurs de format JSON

✅ **Rapport détaillé**
- Statistiques complètes
- Erreurs par type
- Erreurs par expert
- Liste des erreurs critiques
- Temps de réponse moyen

## Utilisation

### Lancer le test (5000 questions)

```bash
cd backend
python scripts/test_stress_5000.py --url http://localhost:8000 --max 5000 --output stress_test_report.json
```

### Lancer avec un nombre réduit (pour test rapide)

```bash
python scripts/test_stress_5000.py --max 100 --output quick_test.json
```

### Ne pas s'arrêter sur erreur critique

```bash
python scripts/test_stress_5000.py --no-stop --max 5000
```

### Test sur serveur de production

```bash
python scripts/test_stress_5000.py --url https://universal-api-hub.fly.dev --max 5000
```

## Types d'erreurs détectées

### Erreurs critiques (arrêtent le test)
- `server_unavailable` - Serveur inaccessible
- `timeout` - Timeout après 30s
- `invalid_response_format` - Format JSON invalide
- `empty_response` - Réponse vide
- `api_error_500` - Erreur serveur 500

### Erreurs non critiques (continuent le test)
- `response_too_short` - Réponse < 10 caractères
- `error_in_response` - Mots d'erreur dans la réponse
- `slow_response` - Temps > 15 secondes
- `http_error_*` - Autres erreurs HTTP

## Rapport généré

Le rapport JSON contient:

```json
{
  "summary": {
    "total_questions": 5000,
    "successful": 4850,
    "failed": 150,
    "success_rate": "97.0%",
    "timeouts": 10,
    "average_response_time_ms": 5234.56,
    "questions_per_second": 2.34
  },
  "errors_by_type": {
    "timeout": 10,
    "empty_response": 5,
    ...
  },
  "errors_by_expert": {
    "health": 2,
    "finance": 1,
    ...
  },
  "critical_errors": [...],
  "all_errors": [...]
}
```

## Monitoring

Pour suivre la progression en temps réel:

```bash
python scripts/monitor_stress_test.py
```

## Temps estimé

- **5000 questions**: ~30-60 minutes (selon la vitesse du serveur)
- **100 questions**: ~1-2 minutes
- **1000 questions**: ~5-10 minutes

## Exemple de sortie

```
🚀 Démarrage du test de charge (5000 questions)...
📍 Serveur: http://localhost:8000
⏱️  Timeout: 30.0s
🛑 Arrêt sur erreur critique: Oui

📋 Récupération de la liste des experts...
✅ 16 experts trouvés

🧪 DÉBUT DES TESTS
✅ Question 100: health - OK (temps: 5234ms)
✅ Question 200: finance - OK (temps: 4123ms)
...

❌ ERREUR Question 1234:
   Expert: health
   Question: Quels sont les bienfaits du sommeil ?...
   Type: timeout
   Message: Timeout après 30s

🛑 ERREUR CRITIQUE DÉTECTÉE - Arrêt du test

📊 RAPPORT DE TEST DE CHARGE
==========================================================
📈 STATISTIQUES GÉNÉRALES
   Total de questions: 1234
   ✅ Réussies: 1200
   ❌ Échouées: 34
   📊 Taux de succès: 97.24%
   ⏱️  Temps moyen: 5234ms
   ⏰ Temps total: 1234.56s
   🚀 Questions/seconde: 1.00

⚠️  ERREURS DÉTECTÉES
   Timeouts: 10
   Réponses invalides: 5
   Réponses lentes (>15s): 2

📋 ERREURS PAR TYPE:
   - timeout: 10
   - empty_response: 5
   ...

🚨 ERREURS CRITIQUES (1):
   Question 1234: timeout - Timeout après 30s
```

## Correction des erreurs

Le rapport indique:
1. **Quelles erreurs** ont été détectées
2. **Quels experts** ont des problèmes
3. **Quand** les erreurs se produisent
4. **Pourquoi** (timeout, serveur, etc.)

Utilisez ces informations pour:
- Optimiser les temps de réponse
- Corriger les bugs
- Améliorer la robustesse
- Identifier les experts problématiques



## Description

Script de test de charge qui génère 5000 questions/réponses pour détecter les erreurs et générer un rapport détaillé.

## Fonctionnalités

✅ **Test automatique de 5000 questions**
- Teste tous les experts avec des questions variées
- Détecte automatiquement les erreurs
- S'arrête dès qu'une erreur critique est détectée

✅ **Détection d'erreurs**
- Timeouts
- Réponses vides
- Erreurs HTTP (500, etc.)
- Réponses invalides
- Réponses trop courtes
- Erreurs de format JSON

✅ **Rapport détaillé**
- Statistiques complètes
- Erreurs par type
- Erreurs par expert
- Liste des erreurs critiques
- Temps de réponse moyen

## Utilisation

### Lancer le test (5000 questions)

```bash
cd backend
python scripts/test_stress_5000.py --url http://localhost:8000 --max 5000 --output stress_test_report.json
```

### Lancer avec un nombre réduit (pour test rapide)

```bash
python scripts/test_stress_5000.py --max 100 --output quick_test.json
```

### Ne pas s'arrêter sur erreur critique

```bash
python scripts/test_stress_5000.py --no-stop --max 5000
```

### Test sur serveur de production

```bash
python scripts/test_stress_5000.py --url https://universal-api-hub.fly.dev --max 5000
```

## Types d'erreurs détectées

### Erreurs critiques (arrêtent le test)
- `server_unavailable` - Serveur inaccessible
- `timeout` - Timeout après 30s
- `invalid_response_format` - Format JSON invalide
- `empty_response` - Réponse vide
- `api_error_500` - Erreur serveur 500

### Erreurs non critiques (continuent le test)
- `response_too_short` - Réponse < 10 caractères
- `error_in_response` - Mots d'erreur dans la réponse
- `slow_response` - Temps > 15 secondes
- `http_error_*` - Autres erreurs HTTP

## Rapport généré

Le rapport JSON contient:

```json
{
  "summary": {
    "total_questions": 5000,
    "successful": 4850,
    "failed": 150,
    "success_rate": "97.0%",
    "timeouts": 10,
    "average_response_time_ms": 5234.56,
    "questions_per_second": 2.34
  },
  "errors_by_type": {
    "timeout": 10,
    "empty_response": 5,
    ...
  },
  "errors_by_expert": {
    "health": 2,
    "finance": 1,
    ...
  },
  "critical_errors": [...],
  "all_errors": [...]
}
```

## Monitoring

Pour suivre la progression en temps réel:

```bash
python scripts/monitor_stress_test.py
```

## Temps estimé

- **5000 questions**: ~30-60 minutes (selon la vitesse du serveur)
- **100 questions**: ~1-2 minutes
- **1000 questions**: ~5-10 minutes

## Exemple de sortie

```
🚀 Démarrage du test de charge (5000 questions)...
📍 Serveur: http://localhost:8000
⏱️  Timeout: 30.0s
🛑 Arrêt sur erreur critique: Oui

📋 Récupération de la liste des experts...
✅ 16 experts trouvés

🧪 DÉBUT DES TESTS
✅ Question 100: health - OK (temps: 5234ms)
✅ Question 200: finance - OK (temps: 4123ms)
...

❌ ERREUR Question 1234:
   Expert: health
   Question: Quels sont les bienfaits du sommeil ?...
   Type: timeout
   Message: Timeout après 30s

🛑 ERREUR CRITIQUE DÉTECTÉE - Arrêt du test

📊 RAPPORT DE TEST DE CHARGE
==========================================================
📈 STATISTIQUES GÉNÉRALES
   Total de questions: 1234
   ✅ Réussies: 1200
   ❌ Échouées: 34
   📊 Taux de succès: 97.24%
   ⏱️  Temps moyen: 5234ms
   ⏰ Temps total: 1234.56s
   🚀 Questions/seconde: 1.00

⚠️  ERREURS DÉTECTÉES
   Timeouts: 10
   Réponses invalides: 5
   Réponses lentes (>15s): 2

📋 ERREURS PAR TYPE:
   - timeout: 10
   - empty_response: 5
   ...

🚨 ERREURS CRITIQUES (1):
   Question 1234: timeout - Timeout après 30s
```

## Correction des erreurs

Le rapport indique:
1. **Quelles erreurs** ont été détectées
2. **Quels experts** ont des problèmes
3. **Quand** les erreurs se produisent
4. **Pourquoi** (timeout, serveur, etc.)

Utilisez ces informations pour:
- Optimiser les temps de réponse
- Corriger les bugs
- Améliorer la robustesse
- Identifier les experts problématiques



