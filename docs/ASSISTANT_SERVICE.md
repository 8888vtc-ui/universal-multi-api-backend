# 🤖 Assistant Personnel IA - Documentation Complète

## Vue d'ensemble

L'**Assistant Personnel IA** apprend de vos interactions et anticipe vos besoins. Il offre des recommandations personnalisées, analyse votre routine, et peut exécuter des tâches automatiques.

---

## 🚀 Fonctionnalités

### 1. Apprentissage des Préférences
- Apprentissage automatique depuis vos interactions
- Détection de patterns (catégories, mots-clés, heures)
- Préférences mises à jour automatiquement

### 2. Recommandations Intelligentes
- Recommandations basées sur vos préférences
- Suggestions cross-domaines (finance → news, etc.)
- Suggestions enrichies par IA

### 3. Analyse de Routine
- Analyse de vos habitudes d'utilisation
- Détection de patterns temporels
- Suggestions d'optimisation

### 4. Automatisation
- Exécution de tâches automatiques
- Résumés quotidiens
- Alertes personnalisées

---

## 📡 Endpoints

### POST `/api/assistant/learn`

Apprendre d'une interaction utilisateur.

**Request Body:**
```json
{
  "user_id": "user123",
  "query": "bitcoin prix",
  "category": "finance",
  "action": "search",
  "feedback": "positive"
}
```

**Response:**
```json
{
  "success": true,
  "learned": true,
  "preferences_updated": true,
  "total_interactions": 25
}
```

### GET `/api/assistant/recommendations`

Obtenir des recommandations personnalisées.

**Query Parameters:**
- `user_id` (required): ID utilisateur
- `limit` (optional): Nombre de recommandations (défaut: 10)
- `categories` (optional): Catégories séparées par virgule

**Response:**
```json
{
  "success": true,
  "recommendations": [
    {
      "category": "finance",
      "query": "bitcoin crypto trading",
      "weight": 0.85,
      "reason": "Basé sur vos recherches fréquentes en finance",
      "ai_suggestion": "Consultez les tendances crypto du jour",
      "related_categories": ["news"]
    }
  ],
  "total": 10,
  "user_preferences": {
    "finance": {"weight": 0.85},
    "news": {"weight": 0.60}
  }
}
```

### POST `/api/assistant/routine/optimize`

Optimiser la routine quotidienne.

**Query Parameters:**
- `user_id` (required): ID utilisateur

**Response:**
```json
{
  "success": true,
  "optimized": true,
  "current_routine": {
    "total_interactions": 45,
    "interactions_per_day": 6.4,
    "most_active_hour": 14,
    "categories_used": {"finance": 20, "news": 15}
  },
  "suggestions": [
    {
      "title": "Regrouper les recherches",
      "description": "Effectuer plusieurs recherches en une fois",
      "impact": "high"
    }
  ],
  "potential_time_saved_minutes": 5
}
```

### POST `/api/assistant/task/execute`

Exécuter une tâche automatique.

**Query Parameters:**
- `user_id` (required): ID utilisateur
- `task_type` (required): Type de tâche
- `parameters` (optional): Paramètres JSON

**Tâches disponibles:**
- `daily_summary`: Résumé quotidien
- `price_alert`: Alertes prix
- `news_digest`: Digest actualités
- `routine_suggestion`: Suggestions routine

**Exemple:**
```
POST /api/assistant/task/execute?user_id=user123&task_type=daily_summary
```

### GET `/api/assistant/profile/{user_id}`

Obtenir le profil complet d'un utilisateur.

**Response:**
```json
{
  "success": true,
  "user_id": "user123",
  "total_interactions": 100,
  "category_counts": {"finance": 40, "news": 30},
  "preferences": {
    "finance": {
      "weight": 0.85,
      "keywords": ["bitcoin", "crypto", "trading"]
    }
  },
  "learned_patterns": {
    "preferred_hour": 14,
    "preferred_day": 2
  }
}
```

---

## 🧠 Comment ça fonctionne

### Apprentissage
1. Chaque interaction est sauvegardée
2. Toutes les 10 interactions, les préférences sont recalculées
3. Patterns détectés (catégories, mots-clés, heures)

### Recommandations
1. Analyse des préférences utilisateur
2. Génération de suggestions basées sur historique
3. Suggestions cross-domaines (catégories liées)
4. Enrichissement avec IA

### Routine
1. Analyse des interactions des 7 derniers jours
2. Détection de patterns temporels
3. Suggestions d'optimisation avec IA

---

## 💡 Exemples d'Utilisation

### Exemple 1: Apprendre d'une interaction
```python
import httpx

async def learn_interaction():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/api/assistant/learn",
            json={
                "user_id": "user123",
                "query": "bitcoin prix",
                "category": "finance",
                "action": "search"
            }
        )
        return response.json()
```

### Exemple 2: Obtenir recommandations
```python
async def get_recommendations():
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "http://localhost:8000/api/assistant/recommendations",
            params={
                "user_id": "user123",
                "limit": 5
            }
        )
        return response.json()
```

### Exemple 3: Optimiser routine
```python
async def optimize_routine():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/api/assistant/routine/optimize",
            params={"user_id": "user123"}
        )
        return response.json()
```

---

## 📊 Données Stockées

### Interactions
- Requêtes utilisateur
- Catégories utilisées
- Actions effectuées
- Feedback (optionnel)
- Timestamps

### Préférences
- Catégories préférées (avec poids)
- Mots-clés fréquents
- Patterns temporels

### Patterns Appris
- Heure préférée
- Jour préféré
- Fréquence d'utilisation

---

## 🔒 Confidentialité

- Données stockées localement (SQLite)
- Pas de partage de données
- Conformité RGPD de base
- Anonymisation possible

---

## 📈 Améliorations Futures

- [ ] Intégration Google Calendar
- [ ] Intégration Todoist
- [ ] Webhooks pour notifications
- [ ] Dashboard utilisateur
- [ ] Export données utilisateur

---

**Dernière mise à jour**: Décembre 2024  
**Version**: 1.0.0



