# 🌐 API Client Unifié - Documentation

## Vue d'ensemble

Le **Universal API Client** est un client Python unifié qui simplifie l'utilisation de tous les endpoints du backend Multi-API.

---

## 🎯 Avantages

### Avant (sans client)
```python
import httpx

# Configuration manuelle
client = httpx.Client(base_url="http://localhost:8000")
headers = {"Authorization": "Bearer token"}

# Requête manuelle
response = client.post(
    "/api/chat",
    json={"message": "Hello"},
    headers=headers
)
data = response.json()
```

### Après (avec client unifié)
```python
from universal_api_client import UniversalAPIClient

client = UniversalAPIClient()
client.login("user@example.com", "password")

# Simple et direct
response = client.chat("Hello")
```

---

## 📦 Installation

```bash
# Depuis le répertoire
cd universal-api-client
pip install -e .

# Ou depuis PyPI (quand publié)
pip install universal-api-client
```

---

## 🚀 Quick Start

```python
from universal_api_client import UniversalAPIClient

# 1. Initialiser
client = UniversalAPIClient(base_url="http://localhost:8000")

# 2. Authentifier
client.login("user@example.com", "password")

# 3. Utiliser
response = client.chat("Hello!")
print(response["response"])

# 4. Fermer
client.close()
```

---

## 📚 Toutes les Méthodes

### Authentification
- `register(email, username, password)` - Inscription
- `login(email, password)` - Connexion
- `logout()` - Déconnexion
- `get_current_user()` - Utilisateur actuel
- `refresh_token(refresh_token)` - Rafraîchir token

### IA & Chat
- `chat(message, system_prompt, provider)` - Chat IA
- `embeddings(text, model)` - Générer embeddings

### Recherche
- `search(query, categories, limit)` - Recherche universelle
- `quick_search(query)` - Recherche rapide
- `get_search_categories()` - Catégories disponibles

### Vidéo IA
- `create_video(text, avatar_id, voice_id, language, use_free)` - Créer vidéo
- `get_video_status(video_id)` - Statut vidéo
- `get_video_voices()` - Voix disponibles
- `generate_course(topic, duration_minutes, language)` - Générer cours

### Assistant
- `assistant_chat(message, context)` - Chat assistant
- `get_recommendations(limit)` - Recommandations
- `get_user_profile()` - Profil utilisateur
- `optimize_routine(routine_data)` - Optimiser routine

### Analytics
- `get_metrics(days, endpoint)` - Métriques
- `get_errors(days)` - Erreurs
- `get_performance(days)` - Performance
- `get_dashboard()` - Dashboard complet

### Finance
- `get_stock_price(symbol)` - Prix action
- `get_crypto_price(symbol)` - Prix crypto

### Météo
- `get_weather(city, country)` - Météo

### News
- `get_news(query, category, limit)` - Actualités

### Traduction
- `translate(text, target_lang, source_lang)` - Traduire

### Géocodage
- `geocode(address)` - Géocoder
- `reverse_geocode(lat, lon)` - Géocodage inverse

### Endpoints Agrégés
- `get_location_info(address, include_weather, include_news)` - Infos localisation
- `get_comprehensive_info(query, ...)` - Infos complètes

### Health
- `health_check()` - Vérifier santé serveur

---

## 🔧 Configuration

### Variables d'environnement

```bash
export API_BASE_URL=http://localhost:8000
export ACCESS_TOKEN=your-jwt-token
export API_KEY=your-api-key
```

### Configuration programmatique

```python
client = UniversalAPIClient(
    base_url="http://localhost:8000",
    access_token="your-token",
    timeout=60.0
)
```

---

## 🛡️ Gestion des Erreurs

```python
from universal_api_client import (
    UniversalAPIClient,
    APIError,
    AuthenticationError,
    RateLimitError
)

try:
    client = UniversalAPIClient()
    response = client.chat("Hello!")
except AuthenticationError as e:
    print(f"Erreur auth: {e}")
    # Réessayer avec nouveau token
except RateLimitError as e:
    print(f"Rate limit: {e}")
    # Attendre et réessayer
except APIError as e:
    print(f"Erreur API: {e.status_code} - {e.message}")
```

---

## 💡 Exemples Avancés

### Context Manager

```python
with UniversalAPIClient() as client:
    client.login("user@example.com", "password")
    response = client.chat("Hello!")
    # Fermeture automatique
```

### Workflow Complet

```python
client = UniversalAPIClient()

# 1. Authentification
client.login("user@example.com", "password")

# 2. Recherche
results = client.search("bitcoin")

# 3. Chat avec contexte
response = client.chat(
    f"Explique-moi: {results['results'][0]['title']}",
    system_prompt="Tu es un expert en finance"
)

# 4. Créer vidéo
video = client.create_video(response["response"])

# 5. Analytics
metrics = client.get_metrics()

client.close()
```

---

## 📊 Comparaison

| Fonctionnalité | Sans Client | Avec Client |
|----------------|-------------|-------------|
| Lignes de code | ~20 | ~5 |
| Gestion tokens | Manuelle | Automatique |
| Gestion erreurs | Manuelle | Exceptions typées |
| Type hints | Non | Oui |
| Documentation | Externe | Intégrée |

---

## 🔗 Liens

- [Code Source](../universal-api-client/)
- [Exemples](../universal-api-client/examples/)
- [Backend Documentation](../README.md)

---

**Dernière mise à jour** : Décembre 2024



