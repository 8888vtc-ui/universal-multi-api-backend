# 🎯 GUIDE : Utiliser le Backend Multi-API dans Vos Projets

**Objectif** : Utiliser ce backend dans tous vos projets (bot backgammon, apps web, scripts Python, etc.) sans réimplémenter les APIs.

---

## 🚀 **CONCEPT SIMPLE**

```
Vos Projets (Bot Backgammon, App Web, Script Python, etc.)
    ↓
    Appel HTTP simple
    ↓
Backend Multi-API (Port 8000)
    ↓
    Gère tout (APIs, quotas, fallback, cache)
    ↓
    Retourne la réponse
```

**Vous n'avez qu'à faire des appels HTTP, c'est tout !**

---

## 📦 **EXEMPLES D'UTILISATION**

### **1. Bot Backgammon (Python)**

```python
# bot_backgammon.py
import httpx
import asyncio

# URL de votre backend (local ou distant)
API_URL = "http://localhost:8000"

async def ask_ai(question: str):
    """Demander quelque chose à l'IA"""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{API_URL}/api/chat",
            json={
                "message": question,
                "language": "en"
            }
        )
        return response.json()["response"]

async def get_weather(city: str):
    """Obtenir la météo"""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{API_URL}/api/weather",
            params={"city": city}
        )
        return response.json()

# Exemple d'utilisation dans votre bot
async def main():
    # Votre bot peut utiliser l'IA pour analyser les coups
    analysis = await ask_ai("Quel est le meilleur coup au backgammon dans cette situation?")
    print(analysis)
    
    # Ou obtenir la météo pour un contexte
    weather = await get_weather("Paris")
    print(weather)

if __name__ == "__main__":
    asyncio.run(main())
```

---

### **2. Script Node.js**

```javascript
// script.js
const API_URL = process.env.API_URL || 'http://localhost:8000';

async function askAI(question) {
    const response = await fetch(`${API_URL}/api/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            message: question,
            language: 'en'
        })
    });
    const data = await response.json();
    return data.response;
}

async function getCryptoPrice(coin) {
    const response = await fetch(`${API_URL}/api/finance/crypto/price/${coin}`);
    return await response.json();
}

// Utilisation
(async () => {
    const answer = await askAI("Explique-moi le backgammon");
    console.log(answer);
    
    const btc = await getCryptoPrice("bitcoin");
    console.log("Bitcoin:", btc);
})();
```

---

### **3. Application Web (React/Vue/etc.)**

```typescript
// api-client.ts
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export class ApiClient {
    static async chat(message: string, language = 'en') {
        const res = await fetch(`${API_URL}/api/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message, language })
        });
        return res.json();
    }
    
    static async getWeather(city: string) {
        const res = await fetch(`${API_URL}/api/weather?city=${city}`);
        return res.json();
    }
    
    static async translate(text: string, targetLang: string) {
        const res = await fetch(`${API_URL}/api/translation/translate`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text, target_language: targetLang })
        });
        return res.json();
    }
}

// Dans votre composant
import { ApiClient } from './api-client';

function MyComponent() {
    const handleClick = async () => {
        const response = await ApiClient.chat("Bonjour!");
        console.log(response.response);
    };
    
    return <button onClick={handleClick}>Chat</button>;
}
```

---

### **4. Script Shell / cURL**

```bash
#!/bin/bash
# script.sh

API_URL="http://localhost:8000"

# Demander à l'IA
ask_ai() {
    curl -X POST "${API_URL}/api/chat" \
        -H "Content-Type: application/json" \
        -d "{\"message\": \"$1\", \"language\": \"en\"}" \
        | jq -r '.response'
}

# Obtenir la météo
get_weather() {
    curl "${API_URL}/api/weather?city=$1" | jq
}

# Utilisation
answer=$(ask_ai "Qu'est-ce que le backgammon?")
echo "$answer"

get_weather "Paris"
```

---

### **5. Bot Discord/Telegram (Python)**

```python
# discord_bot.py
import discord
import httpx
from discord.ext import commands

API_URL = "http://localhost:8000"
bot = commands.Bot(command_prefix='!')

@bot.command()
async def ask(ctx, *, question: str):
    """Pose une question à l'IA"""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{API_URL}/api/chat",
            json={"message": question, "language": "fr"}
        )
        answer = response.json()["response"]
        await ctx.send(answer)

@bot.command()
async def weather(ctx, city: str):
    """Obtenir la météo"""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{API_URL}/api/weather",
            params={"city": city}
        )
        data = response.json()
        await ctx.send(f"Météo à {city}: {data['temperature']}°C")

bot.run("YOUR_BOT_TOKEN")
```

---

## 🎮 **CAS D'USAGE : BOT BACKGAMMON**

### **Fonctionnalités possibles avec votre backend :**

```python
# bot_backgammon_advanced.py
import httpx
import asyncio

API_URL = "http://localhost:8000"

class BackgammonBot:
    def __init__(self):
        self.api_url = API_URL
    
    async def analyze_move(self, board_state: str):
        """Analyser un coup avec l'IA"""
        prompt = f"""
        Analyse cette position de backgammon et recommande le meilleur coup:
        {board_state}
        
        Réponds en format JSON avec:
        - best_move: le meilleur coup
        - reasoning: pourquoi ce coup
        - win_probability: probabilité de gagner
        """
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.api_url}/api/chat",
                json={"message": prompt, "language": "en"}
            )
            return response.json()["response"]
    
    async def explain_rules(self, rule: str):
        """Expliquer une règle du backgammon"""
        prompt = f"Explique la règle du backgammon: {rule}"
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.api_url}/api/chat",
                json={"message": prompt, "language": "fr"}
            )
            return response.json()["response"]
    
    async def get_player_stats(self, player_name: str):
        """Obtenir des stats sur un joueur (si vous avez une API)"""
        # Vous pourriez utiliser l'IA pour analyser des données
        # ou utiliser d'autres endpoints de votre backend
        pass
    
    async def translate_move(self, move: str, target_lang: str):
        """Traduire un coup dans une autre langue"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.api_url}/api/translation/translate",
                json={"text": move, "target_language": target_lang}
            )
            return response.json()["translated_text"]

# Utilisation
async def main():
    bot = BackgammonBot()
    
    # Analyser un coup
    analysis = await bot.analyze_move("Position: 5-3, 4-2")
    print(analysis)
    
    # Expliquer une règle
    explanation = await bot.explain_rules("doubler")
    print(explanation)
    
    # Traduire
    translated = await bot.translate_move("Roll dice", "fr")
    print(translated)  # "Lancer les dés"

asyncio.run(main())
```

---

## 📚 **CLIENT LIBRARY SIMPLE (Optionnel)**

Créez un petit package réutilisable :

```python
# my_api_client/__init__.py
import httpx
from typing import Optional, Dict, Any

class UniversalAPIClient:
    """Client simple pour votre backend multi-API"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.client = httpx.AsyncClient()
    
    async def chat(self, message: str, language: str = "en") -> str:
        """Chat avec l'IA"""
        response = await self.client.post(
            f"{self.base_url}/api/chat",
            json={"message": message, "language": language}
        )
        return response.json()["response"]
    
    async def get_weather(self, city: str) -> Dict[str, Any]:
        """Obtenir la météo"""
        response = await self.client.get(
            f"{self.base_url}/api/weather",
            params={"city": city}
        )
        return response.json()
    
    async def translate(self, text: str, target_lang: str) -> str:
        """Traduire un texte"""
        response = await self.client.post(
            f"{self.api_url}/api/translation/translate",
            json={"text": text, "target_language": target_lang}
        )
        return response.json()["translated_text"]
    
    async def get_crypto_price(self, coin: str) -> Dict[str, Any]:
        """Obtenir le prix d'une crypto"""
        response = await self.client.get(
            f"{self.base_url}/api/finance/crypto/price/{coin}"
        )
        return response.json()
    
    async def close(self):
        """Fermer le client"""
        await self.client.aclose()

# Utilisation dans tous vos projets
# from my_api_client import UniversalAPIClient
# 
# client = UniversalAPIClient()
# answer = await client.chat("Hello!")
# await client.close()
```

---

## 🌐 **UTILISATION DISTANTE (Production)**

### **Option 1 : Backend sur VPS**

```python
# Dans vos projets, utilisez l'URL distante
API_URL = "https://votre-backend.com"  # Au lieu de localhost:8000
```

### **Option 2 : Backend local avec ngrok (pour tests)**

```bash
# Terminal 1 : Lancer votre backend
cd backend
python main.py

# Terminal 2 : Exposer avec ngrok
ngrok http 8000

# Utiliser l'URL ngrok dans vos projets
API_URL = "https://abc123.ngrok.io"
```

---

## 🔧 **CONFIGURATION RAPIDE**

### **1. Démarrer le backend une fois**

```bash
cd backend
python main.py
# Backend disponible sur http://localhost:8000
```

### **2. Dans vos autres projets, juste faire des appels HTTP**

**C'est tout !** Pas besoin de :
- ❌ Réinstaller les dépendances API
- ❌ Gérer les clés API dans chaque projet
- ❌ Implémenter le fallback
- ❌ Gérer les quotas
- ❌ Gérer le cache

**Tout est géré par le backend central !**

---

## 📋 **ENDPOINTS DISPONIBLES**

### **IA & Chat**
- `POST /api/chat` - Chat avec l'IA
- `POST /api/embeddings` - Créer des embeddings

### **Finance**
- `GET /api/finance/crypto/price/{coin}` - Prix crypto
- `GET /api/finance/stock/quote/{symbol}` - Prix action

### **Météo**
- `GET /api/weather?city={city}` - Météo d'une ville

### **Traduction**
- `POST /api/translation/translate` - Traduire un texte

### **Et plus...**
Voir la documentation complète : `http://localhost:8000/docs`

---

## 💡 **AVANTAGES POUR VOS PROJETS**

✅ **Simplicité** : Juste des appels HTTP  
✅ **Réutilisation** : Même backend pour tous vos projets  
✅ **Économie** : Pas besoin de clés API partout  
✅ **Maintenance** : Mise à jour centralisée  
✅ **Performance** : Cache partagé  
✅ **Fiabilité** : Fallback automatique  

---

## 🚨 **BONNES PRATIQUES**

### **1. Gérer les erreurs**

```python
async def safe_chat(message: str):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{API_URL}/api/chat",
                json={"message": message, "language": "en"},
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()["response"]
    except httpx.TimeoutException:
        return "Timeout: Le backend ne répond pas"
    except httpx.HTTPStatusError:
        return "Erreur: Le backend a retourné une erreur"
    except Exception as e:
        return f"Erreur: {str(e)}"
```

### **2. Utiliser des variables d'environnement**

```python
import os
API_URL = os.getenv("UNIVERSAL_API_URL", "http://localhost:8000")
```

### **3. Pool de connexions (pour performance)**

```python
# Créer un client réutilisable
client = httpx.AsyncClient(base_url=API_URL)

# Utiliser partout dans votre app
response = await client.post("/api/chat", json={...})

# Fermer à la fin
await client.aclose()
```

---

## 🎯 **RÉSUMÉ**

**Pour utiliser ce backend dans vos projets :**

1. ✅ Démarrer le backend une fois (`python main.py`)
2. ✅ Dans vos projets, faire des appels HTTP simples
3. ✅ Profiter ! 🎉

**C'est vraiment aussi simple que ça !**

---

## 📞 **EXEMPLE COMPLET : Bot Backgammon**

```python
# bot_backgammon.py - Exemple complet
import httpx
import asyncio
from typing import Dict, Any

class BackgammonBot:
    def __init__(self, api_url: str = "http://localhost:8000"):
        self.api_url = api_url
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def get_ai_advice(self, situation: str) -> str:
        """Obtenir des conseils de l'IA"""
        try:
            response = await self.client.post(
                f"{self.api_url}/api/chat",
                json={
                    "message": f"Conseil backgammon: {situation}",
                    "language": "fr"
                }
            )
            response.raise_for_status()
            return response.json()["response"]
        except Exception as e:
            return f"Erreur: {e}"
    
    async def translate_rules(self, text: str, lang: str = "en") -> str:
        """Traduire les règles"""
        try:
            response = await self.client.post(
                f"{self.api_url}/api/translation/translate",
                json={"text": text, "target_language": lang}
            )
            response.raise_for_status()
            return response.json()["translated_text"]
        except Exception as e:
            return text  # Retourner original si erreur
    
    async def close(self):
        """Fermer le client"""
        await self.client.aclose()

# Utilisation
async def main():
    bot = BackgammonBot()
    
    advice = await bot.get_ai_advice("J'ai un 5-3, que faire?")
    print(advice)
    
    translated = await bot.translate_rules("Double the stakes", "fr")
    print(translated)
    
    await bot.close()

if __name__ == "__main__":
    asyncio.run(main())
```

---

**Voilà ! Vous pouvez maintenant utiliser ce backend dans TOUS vos projets sans vous compliquer la vie ! 🚀**


