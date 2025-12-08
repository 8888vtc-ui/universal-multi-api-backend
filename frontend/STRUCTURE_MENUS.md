# 📋 Structure Complète des Menus - aska.ai

## 🎯 Menu Principal (Header)

### Desktop View

```
┌─────────────────────────────────────────────────────────────────────┐
│ [Logo aska.ai]  │  🔍 Recherche  │  ✨ IA Search  │  💬 Chat      │
│                 │  📊 Explorer   │  📚 Historique │  📖 Docs      │
│                 │  💳 Pricing    │  [👤 User Menu] │  [☰ Menu]    │
└─────────────────────────────────────────────────────────────────────┘
```

### Mobile View (Bottom Navigation)

```
┌─────────────────────────────────────┐
│  🔍    ✨    💬    📊    👤         │
│ Recherche  IA   Chat  Explorer  Me │
└─────────────────────────────────────┘
```

---

## 📑 Menu Détaillé

### 1. **Recherche** (Dropdown)

```
🔍 Recherche
├── Recherche Simple
├── Recherche IA (RAG)
├── Recherche Vocale 🎤
├── Recherche Image 📷
└── Recherche Avancée ⚙️
```

### 2. **Explorer** (Dropdown)

```
📊 Explorer
├── 🤖 AI Providers (10)
│   ├── Groq
│   ├── Mistral
│   ├── Anthropic
│   └── ...
├── 💰 Finance (5)
│   ├── CoinGecko
│   ├── CoinCap
│   └── ...
├── 📰 News (6)
├── 🌍 Géolocalisation (6)
├── 📚 Connaissance (6)
├── 🎭 Divertissement (8)
└── 🔧 Utilitaires (10)
```

### 3. **User Menu** (Dropdown)

```
👤 [Nom Utilisateur]
├── 📊 Dashboard
├── ⚙️  Paramètres
│   ├── Profil
│   ├── Préférences
│   ├── Notifications
│   └── Sécurité
├── 💳 Abonnement
│   ├── Plan actuel
│   ├── Upgrade
│   └── Facturation
├── 🔑 API Keys
│   ├── Générer clé
│   ├── Gérer clés
│   └── Documentation
├── 📈 Analytics
├── 📚 Historique
├── 🆘 Support
└── 🚪 Déconnexion
```

### 4. **Menu Hamburger** (Mobile)

```
☰ Menu
├── 🏠 Accueil
├── 🔍 Recherche
├── ✨ Recherche IA
├── 💬 Chat
├── 📊 Explorer
├── 📚 Historique
├── 📖 Documentation
├── 💳 Pricing
├── ⚙️  Paramètres
├── 🆘 Support
└── [User Section]
    ├── Dashboard
    ├── Profil
    └── Déconnexion
```

---

## 🎨 Sidebar (Mode Dashboard)

### Pour utilisateurs connectés

```
┌─────────────────────┐
│  aska.ai            │
│  [Logo]             │
├─────────────────────┤
│ 🏠 Accueil          │
│ 🔍 Recherche        │
│ ✨ Recherche IA     │
│ 💬 Chat             │
├─────────────────────┤
│ 📊 Explorer          │
│   ├── 🤖 AI         │
│   ├── 💰 Finance    │
│   ├── 📰 News       │
│   └── ...           │
├─────────────────────┤
│ 📚 Historique        │
│ ⚙️  Paramètres       │
│ 💳 Abonnement        │
│ 🔑 API Keys          │
├─────────────────────┤
│ 📖 Documentation     │
│ 🆘 Support           │
└─────────────────────┘
```

---

## 🔍 Menu Contextuel (Right-Click)

### Sur un résultat de recherche

```
┌─────────────────────┐
│ 📋 Copier           │
│ 🔗 Copier le lien   │
│ 📤 Partager         │
│ ⭐ Sauvegarder      │
│ 📥 Exporter         │
│ 🚫 Masquer          │
└─────────────────────┘
```

### Sur une API dans Explorer

```
┌─────────────────────┐
│ 🧪 Tester           │
│ 📖 Documentation    │
│ ⭐ Favoris          │
│ 📊 Statistiques     │
│ 🔗 Copier endpoint  │
└─────────────────────┘
```

---

## 🎯 Breadcrumbs

### Navigation hiérarchique

```
Accueil > Explorer > Finance > CoinGecko > Détails
Accueil > Recherche > "Bitcoin" > Résultat #3
Accueil > Chat > Conversation #12
```

---

## 🔔 Notifications Menu

```
🔔 (3)
├── ✅ Recherche terminée
├── ⚠️  Quota presque atteint
└── 🎉 Nouvelle fonctionnalité
```

---

## 🌐 Langue & Région

```
🌐 FR ▼
├── 🇫🇷 Français
├── 🇬🇧 English
├── 🇪🇸 Español
└── 🇩🇪 Deutsch
```

---

## 🎨 Thème

```
🌙 Dark Mode ▼
├── 🌙 Dark
├── ☀️ Light
└── 🎨 Auto (système)
```

---

## 📱 Menu Mobile (Bottom Sheet)

```
┌─────────────────────────┐
│  aska.ai                │
│  [Fermer]               │
├─────────────────────────┤
│ 🏠 Accueil              │
│ 🔍 Recherche            │
│ ✨ Recherche IA         │
│ 💬 Chat                 │
│ 📊 Explorer             │
│ 📚 Historique           │
├─────────────────────────┤
│ ⚙️  Paramètres          │
│ 💳 Abonnement           │
│ 📖 Documentation        │
│ 🆘 Support              │
└─────────────────────────┘
```

---

## 🎯 Quick Actions (Floating)

### Bouton flottant (FAB)

```
    [➕]
    │
    ├── 🔍 Nouvelle recherche
    ├── 💬 Nouveau chat
    ├── 📊 Explorer API
    └── 📚 Voir historique
```

---

## 📊 Menu Statistiques (Widget)

```
📊 Stats
├── Requêtes aujourd'hui: 45/500
├── Quota restant: 91%
├── APIs utilisées: 12
└── Temps moyen: 1.2s
```

---

## 🔐 Menu Sécurité

```
🔒 Sécurité
├── 🔑 Changer mot de passe
├── 📧 Vérifier email
├── 📱 2FA (Authentification)
├── 🔐 Sessions actives
└── 📋 Logs de sécurité
```

---

## 💡 Menu Aide

```
❓ Aide
├── 📖 Documentation
├── 🎥 Tutoriels vidéo
├── 💬 Chat support
├── 📧 Email support
├── 🐛 Signaler un bug
└── 💡 Suggestions
```

---

**Cette structure de menus offre une navigation intuitive et complète !** 🎯





