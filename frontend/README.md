# 🇮🇱 Guide Touristique Israélien

**Type** : Sous-Projet Frontend  
**Backend** : Moteur Multi-API Universel  
**Version** : 1.0.0

---

## 🎯 **CONCEPT**

Ce projet est un **sous-projet frontend** qui consomme les APIs du **backend multi-API universel**.

### **Architecture**

```
Backend Central (Port 8000)
    ↓ (APIs REST)
Frontend Guide Israélien (Port 3000)
    ↓
Utilisateurs finaux
```

**Le frontend NE contient PAS les APIs**, il les consomme depuis le backend central.

---

## 📱 **FONCTIONNALITÉS**

### **Chat IA Bilingue**
- Interface en hébreu (RTL) et anglais
- Conseils voyage personnalisés
- Recommandations kasher et Shabbat
- Alertes sécurité

### **Intégrations Backend**
- **IA** : Chat conversationnel (Groq, Mistral, Gemini)
- **Météo** : Prévisions destinations (OpenWeather)
- **Devises** : Conversion Shekel ↔ autres (ExchangeRate)
- **Restaurants** : Recherche kasher (Yelp)

---

## 🏗️ **ARCHITECTURE**

### **Frontend (Next.js 14)**

```
frontend/
├── app/
│   ├── page.tsx              # Page principale
│   ├── layout.tsx            # Layout racine
│   └── globals.css           # Styles globaux
├── components/
│   ├── Header.tsx            # En-tête + switch langue
│   ├── ChatInterface.tsx     # Interface chat
│   └── MessageBubble.tsx     # Bulles messages
├── hooks/
│   └── useChat.ts            # Hook custom chat
└── lib/
    ├── api.ts                # Client API (consomme backend)
    └── i18n.ts               # Traductions HE/EN
```

### **Consommation du Backend**

```typescript
// lib/api.ts
const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function sendMessage(message: string, language: string) {
  const response = await fetch(`${API_URL}/api/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message, language })
  });
  
  return response.json();
}
```

**Le frontend appelle simplement les endpoints du backend, il ne gère PAS les APIs directement.**

---

## 🚀 **INSTALLATION**

### **Prérequis**
- Node.js 18+
- Backend multi-API en cours d'exécution (port 8000)

### **Installation**

```bash
cd frontend
npm install
```

### **Configuration**

Créer `.env.local` :

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_DEFAULT_LANGUAGE=he
```

### **Démarrage**

```bash
npm run dev
```

**Application** : http://localhost:3000

---

## 🔌 **DÉPENDANCES AU BACKEND**

Ce frontend **NÉCESSITE** que le backend soit en cours d'exécution.

### **Endpoints Utilisés**

| Endpoint | Usage |
|----------|-------|
| `POST /api/chat` | Chat IA conversationnel |
| `GET /api/health` | Vérification santé backend |
| `GET /api/entertainment/restaurants/search` | Recherche restaurants kasher |

**Sans le backend, le frontend ne fonctionne pas.**

---

## 🎨 **FONCTIONNALITÉS**

### **Actuelles**
- ✅ Chat IA bilingue (hébreu RTL + anglais)
- ✅ Interface moderne responsive
- ✅ Dark mode automatique
- ✅ Historique conversation
- ✅ Support hébreu natif

### **À Venir**
- [ ] Intégration météo temps réel
- [ ] Conversion devises automatique
- [ ] Recherche restaurants kasher
- [ ] Alertes sécurité destinations
- [ ] Système RAG (mémoire)
- [ ] Mode hors-ligne (PWA)

---

## 📊 **RELATION AVEC LE BACKEND**

### **Ce que fait le Frontend**
- 🎨 Interface utilisateur
- 🌍 Gestion langues (HE/EN)
- 💬 Affichage messages
- 📱 Responsive design

### **Ce que fait le Backend**
- 🤖 Intelligence artificielle
- 🌤️ Données météo
- 💱 Taux de change
- 🍽️ Données restaurants
- 🔄 Fallback providers
- 📊 Gestion quotas

**Séparation claire des responsabilités !**

---

## 🚀 **DÉPLOIEMENT**

### **Frontend (Vercel)**

```bash
# Déployer sur Vercel
vercel

# Configurer les variables d'environnement
NEXT_PUBLIC_API_URL=https://votre-backend.com
```

### **Backend (VPS)**

Le backend doit être déployé séparément sur un VPS ou service cloud.

**Les deux doivent être accessibles pour que l'application fonctionne.**

---

## 🎯 **AUTRES SOUS-PROJETS**

Ce frontend est **l'un des 50+ sous-projets** prévus qui utilisent le même backend :

1. **Guide Touristique Israélien** ← Ce projet
2. Assistant Finance
3. Recherche Médicale
4. Guide Loisirs
5. ... 46+ autres

**Tous partagent le même backend central.**

---

## 📝 **DÉVELOPPEMENT**

### **Ajouter une Nouvelle Fonctionnalité**

1. Vérifier si l'API existe dans le backend
2. Si non, demander l'ajout au backend
3. Consommer l'endpoint dans `lib/api.ts`
4. Créer le composant frontend
5. Intégrer dans l'interface

**Ne jamais ajouter de logique API dans le frontend !**

---

## 🎉 **SUCCÈS**

Ce sous-projet démontre :

✅ **Architecture modulaire** (frontend ↔ backend)  
✅ **Réutilisation des APIs** (backend partagé)  
✅ **Développement rapide** (APIs déjà prêtes)  
✅ **Scalabilité** (facile d'ajouter features)  

**Le frontend consomme, le backend fournit ! 🚀**
