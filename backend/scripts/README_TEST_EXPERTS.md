# 🧪 Test Automatique des Experts/Bots

## Description

Script de test automatique qui vérifie que tous les experts/bots fonctionnent correctement et produisent des réponses réalistes et fonctionnelles.

## Utilisation

### Test local (serveur sur localhost:8000)

```bash
cd backend
python scripts/test_all_experts_auto.py
```

### Test sur serveur de production

```bash
python scripts/test_all_experts_auto.py --url https://universal-api-hub.fly.dev
```

### Sauvegarder le rapport

```bash
python scripts/test_all_experts_auto.py --output rapport_test.json
```

## Ce que le script teste

1. ✅ **Accessibilité du serveur** - Vérifie que le serveur répond
2. ✅ **Liste des experts** - Récupère tous les experts disponibles
3. ✅ **Chaque expert individuellement** - Teste chaque expert avec une question appropriée
4. ✅ **Chat général** - Teste l'endpoint `/api/chat`
5. ✅ **Validation des réponses** - Vérifie que les réponses sont:
   - Non vides
   - Assez longues (> 20 caractères)
   - Sans mots d'erreur
   - Pertinentes par rapport à la question
   - Dans le style de l'expert

## Rapport généré

Le script génère un rapport détaillé avec:
- Nombre de tests réussis/échoués
- Taux de succès
- Temps moyen de réponse
- Score de validation moyen
- Détails de chaque test
- Liste des erreurs et avertissements

## Exemple de sortie

```
🚀 Démarrage des tests automatiques des experts...
📍 Serveur: http://localhost:8000

1️⃣ Vérification du serveur...
✅ Serveur accessible

2️⃣ Récupération de la liste des experts...
✅ 16 experts trouvés

3️⃣ Test de chaque expert...
============================================================

🧪 Test: Recherche Santé (health)
   Question: Quels sont les bienfaits du sommeil ?...
   ✅ Succès (score: 0.95, temps: 1234ms)

...

📊 RAPPORT DE TEST
============================================================

✅ Tests réussis: 15/16
❌ Tests échoués: 1
📈 Taux de succès: 93.8%
⏱️  Temps moyen de réponse: 1456ms
⭐ Score de validation moyen: 0.92
⏰ Temps total: 45.2s
```

## Questions de test par expert

Chaque expert est testé avec une question appropriée à son domaine:

- **health**: "Quels sont les bienfaits du sommeil ?"
- **finance**: "Quel est le cours du Bitcoin ?"
- **weather**: "Météo Paris demain ?"
- **tech**: "C'est quoi ChatGPT ?"
- etc.

## Intégration CI/CD

Le script peut être intégré dans un pipeline CI/CD:

```yaml
- name: Test Experts
  run: |
    python backend/scripts/test_all_experts_auto.py --url ${{ secrets.API_URL }} --output test_report.json
```

## Codes de retour

- `0`: Tous les tests ont réussi
- `1`: Au moins un test a échoué



## Description

Script de test automatique qui vérifie que tous les experts/bots fonctionnent correctement et produisent des réponses réalistes et fonctionnelles.

## Utilisation

### Test local (serveur sur localhost:8000)

```bash
cd backend
python scripts/test_all_experts_auto.py
```

### Test sur serveur de production

```bash
python scripts/test_all_experts_auto.py --url https://universal-api-hub.fly.dev
```

### Sauvegarder le rapport

```bash
python scripts/test_all_experts_auto.py --output rapport_test.json
```

## Ce que le script teste

1. ✅ **Accessibilité du serveur** - Vérifie que le serveur répond
2. ✅ **Liste des experts** - Récupère tous les experts disponibles
3. ✅ **Chaque expert individuellement** - Teste chaque expert avec une question appropriée
4. ✅ **Chat général** - Teste l'endpoint `/api/chat`
5. ✅ **Validation des réponses** - Vérifie que les réponses sont:
   - Non vides
   - Assez longues (> 20 caractères)
   - Sans mots d'erreur
   - Pertinentes par rapport à la question
   - Dans le style de l'expert

## Rapport généré

Le script génère un rapport détaillé avec:
- Nombre de tests réussis/échoués
- Taux de succès
- Temps moyen de réponse
- Score de validation moyen
- Détails de chaque test
- Liste des erreurs et avertissements

## Exemple de sortie

```
🚀 Démarrage des tests automatiques des experts...
📍 Serveur: http://localhost:8000

1️⃣ Vérification du serveur...
✅ Serveur accessible

2️⃣ Récupération de la liste des experts...
✅ 16 experts trouvés

3️⃣ Test de chaque expert...
============================================================

🧪 Test: Recherche Santé (health)
   Question: Quels sont les bienfaits du sommeil ?...
   ✅ Succès (score: 0.95, temps: 1234ms)

...

📊 RAPPORT DE TEST
============================================================

✅ Tests réussis: 15/16
❌ Tests échoués: 1
📈 Taux de succès: 93.8%
⏱️  Temps moyen de réponse: 1456ms
⭐ Score de validation moyen: 0.92
⏰ Temps total: 45.2s
```

## Questions de test par expert

Chaque expert est testé avec une question appropriée à son domaine:

- **health**: "Quels sont les bienfaits du sommeil ?"
- **finance**: "Quel est le cours du Bitcoin ?"
- **weather**: "Météo Paris demain ?"
- **tech**: "C'est quoi ChatGPT ?"
- etc.

## Intégration CI/CD

Le script peut être intégré dans un pipeline CI/CD:

```yaml
- name: Test Experts
  run: |
    python backend/scripts/test_all_experts_auto.py --url ${{ secrets.API_URL }} --output test_report.json
```

## Codes de retour

- `0`: Tous les tests ont réussi
- `1`: Au moins un test a échoué



