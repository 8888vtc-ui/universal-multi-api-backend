# 🔌 Guide d'Intégration dans vos Projets

## ✅ Oui ! Une seule variable = Toutes les APIs

En ajoutant le client API unifié dans **n'importe quel projet**, vous pouvez appeler **toutes les APIs** du backend.

---

## 🎯 Principe

```
Votre Projet (Bot Backgammon, App Web, etc.)
    ↓
    [Client API Unifié]
    ↓
Backend Multi-API (Port 8000)
    ↓
    [Toutes les APIs disponibles]
```

**Une seule installation** → **Accès à toutes les APIs** !

---

## 📦 Installation dans votre Projet

### Option 1 : Depuis le répertoire local

```bash
# Dans votre projet (ex: bot-backgammon/)
pip install -e ../universal-api-client
```

### Option 2 : Depuis Git (quand publié)

```bash
pip install git+https://github.com/VOTRE_USER/universal-api-client.git
```

### Option 3 : Depuis PyPI (quand publié)

```bash
pip install universal-api-client
```

---

## 🚀 Utilisation dans votre Code

### Exemple : Bot Backgammon

```python
# bot_backgammon.py
from universal_api_client import UniversalAPIClient

class BotBackgammon:
    def __init__(self):
        # Une seule ligne pour accéder à TOUTES les APIs !
        self.api = UniversalAPIClient(base_url="http://localhost:8000")
        self.api.login("user@example.com", "password")
    
    def analyser_position(self, position):
        # Utiliser l'IA
        return self.api.chat(f"Analyse: {position}")
    
    def traduire_message(self, message, langue):
        # Utiliser la traduction
        return self.api.translate(message, target_lang=langue)
    
    def obtenir_meteo(self, ville):
        # Utiliser la météo
        return self.api.get_weather(ville)
    
    def rechercher_strategies(self):
        # Utiliser les news
        return self.api.get_news(query="backgammon strategy")
    
    def creer_tutoriel(self, texte):
        # Utiliser la vidéo IA
        return self.api.create_video(texte)
    
    # ... et toutes les autres APIs !
```

---

## 📋 Liste Complète des APIs Disponibles

### ✅ Authentification
- `register()` - Inscription
- `login()` - Connexion
- `logout()` - Déconnexion

### ✅ IA & Chat
- `chat()` - Chat avec IA
- `embeddings()` - Générer embeddings

### ✅ Recherche
- `search()` - Recherche universelle
- `quick_search()` - Recherche rapide

### ✅ Vidéo IA
- `create_video()` - Créer vidéo avatar
- `get_video_status()` - Statut vidéo
- `generate_course()` - Générer cours

### ✅ Assistant Personnel
- `assistant_chat()` - Chat assistant
- `get_recommendations()` - Recommandations
- `optimize_routine()` - Optimiser routine

### ✅ Finance
- `get_stock_price()` - Prix action
- `get_crypto_price()` - Prix crypto

### ✅ Météo
- `get_weather()` - Météo d'une ville

### ✅ News
- `get_news()` - Actualités

### ✅ Traduction
- `translate()` - Traduire texte

### ✅ Géocodage
- `geocode()` - Géocoder adresse
- `reverse_geocode()` - Géocodage inverse

### ✅ Analytics
- `get_metrics()` - Métriques
- `get_dashboard()` - Dashboard

### ✅ Endpoints Agrégés
- `get_location_info()` - Infos complètes localisation
- `get_comprehensive_info()` - Infos complètes sujet

**Total : 30+ méthodes = Toutes les APIs !**

---

## 💡 Exemples Concrets par Type de Projet

### Bot Backgammon

```python
from universal_api_client import UniversalAPIClient

api = UniversalAPIClient()
api.login("user@example.com", "password")

# Analyser position avec IA
analyse = api.chat("Analyse cette position de backgammon...")

# Traduire pour joueurs internationaux
message_fr = api.translate("Hello", target_lang="fr")

# Obtenir stratégies depuis news
strategies = api.get_news(query="backgammon strategy")
```

### Application Web (React/Next.js)

```python
# Backend Python de votre app web
from universal_api_client import UniversalAPIClient

api = UniversalAPIClient()

# Endpoint de votre app web
@app.route("/api/chat")
def chat_endpoint():
    response = api.chat(request.json["message"])
    return jsonify(response)
```

### Application Mobile (Backend Python)

```python
# API backend pour votre app mobile
from universal_api_client import UniversalAPIClient

api = UniversalAPIClient()

# Endpoint pour l'app mobile
@app.route("/mobile/search")
def mobile_search():
    query = request.args.get("q")
    results = api.search(query)
    return jsonify(results)
```

### Script d'Automatisation

```python
from universal_api_client import UniversalAPIClient

api = UniversalAPIClient()
api.login("user@example.com", "password")

# Automatiser des tâches avec toutes les APIs
def daily_report():
    # Météo
    weather = api.get_weather("Paris")
    
    # News
    news = api.get_news(query="technology", limit=5)
    
    # Finance
    btc = api.get_crypto_price("BTC")
    
    # Créer résumé avec IA
    summary = api.chat(f"Résume: {weather}, {news}, {btc}")
    
    return summary
```

---

## ⚙️ Configuration

### Variables d'environnement

Dans votre projet, créer `.env` :

```env
API_BASE_URL=http://localhost:8000
ACCESS_TOKEN=your-jwt-token
```

Puis dans votre code :

```python
from universal_api_client import UniversalAPIClient
import os

# Le client utilise automatiquement les variables d'environnement
api = UniversalAPIClient()  # Utilise API_BASE_URL et ACCESS_TOKEN
```

---

## 🔒 Sécurité

### Stockage des Credentials

**Ne jamais** commiter les credentials dans le code :

```python
# ❌ MAUVAIS
api = UniversalAPIClient(
    base_url="http://localhost:8000",
    access_token="hardcoded-token"  # ❌ JAMAIS !
)

# ✅ BON
import os
api = UniversalAPIClient(
    base_url=os.getenv("API_BASE_URL"),
    access_token=os.getenv("ACCESS_TOKEN")
)
```

---

## 📊 Avantages

### Avant (sans client)

```python
# Pour chaque API, configuration manuelle
import httpx

client = httpx.Client(base_url="http://localhost:8000")
headers = {"Authorization": "Bearer token"}

# Chat
response = client.post("/api/chat", json={"message": "Hello"}, headers=headers)

# Météo
response = client.get("/api/weather/current", params={"city": "Paris"}, headers=headers)

# Traduction
response = client.post("/api/translation/translate", json={...}, headers=headers)

# ... répéter pour chaque API
```

### Après (avec client unifié)

```python
from universal_api_client import UniversalAPIClient

api = UniversalAPIClient()
api.login("user@example.com", "password")

# Toutes les APIs en une ligne !
chat = api.chat("Hello")
weather = api.get_weather("Paris")
translation = api.translate("Hello", target_lang="fr")
# ... et 27+ autres méthodes !
```

**Gain** : 90% moins de code, 100% plus simple !

---

## 🎯 Checklist d'Intégration

- [ ] Installer le client : `pip install -e ../universal-api-client`
- [ ] Importer : `from universal_api_client import UniversalAPIClient`
- [ ] Initialiser : `api = UniversalAPIClient(base_url="...")`
- [ ] Authentifier : `api.login("email", "password")`
- [ ] Utiliser les APIs : `api.chat()`, `api.search()`, etc.
- [ ] Configurer variables d'environnement (optionnel)
- [ ] Tester dans votre projet

---

## 📚 Documentation

- [Client API Unifié](API_CLIENT_UNIFIE.md) - Documentation complète
- [Exemples](../universal-api-client/examples/) - Exemples de code
- [Backend Documentation](../README.md) - Documentation backend

---

## ✅ Conclusion

**OUI** : En ajoutant le client dans votre projet, vous pouvez appeler **n'importe quelle API** du backend !

**Une seule installation** → **30+ méthodes** → **Toutes les APIs disponibles** !

---

**Dernière mise à jour** : Décembre 2024


<<<<<<< Updated upstream
=======





>>>>>>> Stashed changes
