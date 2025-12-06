# 🎨 Conception Frontend - aska.ai

## 🌐 Domaine & Branding

**Domaine** : `aska.ai`  
**Slogan** : "Ask Anything. Get Everything."  
**Positionnement** : Moteur de recherche IA intelligent qui agrège 78+ APIs

---

## 📐 Architecture des Pages

### 🏠 Page d'Accueil (`/`)

**Hero Section**
```
┌─────────────────────────────────────────┐
│  [aska.ai Logo]  [Menu] [Sign In]      │
├─────────────────────────────────────────┤
│                                         │
│     🔍 aska.ai                          │
│     Ask Anything. Get Everything.       │
│                                         │
│  [Barre de recherche intelligente]     │
│  [Rechercher] [Recherche IA] [Voice]   │
│                                         │
│  ✨ Recherche IA  |  📊 Explorer  |    │
│     💬 Chat       |  📚 Historique      │
└─────────────────────────────────────────┘
```

**Fonctionnalités principales** :
- Barre de recherche centrale (style Google/Perplexity)
- 3 modes : Recherche simple, Recherche IA, Chat
- Suggestions intelligentes
- Historique rapide

---

## 🎯 Structure des Menus

### Menu Principal (Header)

```
┌─────────────────────────────────────────────────────┐
│ [Logo] aska.ai  │  Recherche  │  Explorer  │  Docs │
│                 │  Chat       │  Historique │  API  │
│                 │  Pricing    │  About      │  [👤] │
└─────────────────────────────────────────────────────┘
```

### Menu Latéral (Sidebar) - Mode Dashboard

```
┌─────────────────┐
│  aska.ai        │
├─────────────────┤
│ 🏠 Accueil      │
│ 🔍 Recherche    │
│ ✨ Recherche IA │
│ 💬 Chat         │
│ 📊 Explorer     │
│ 📚 Historique   │
│ ⚙️  Paramètres  │
│ 💳 Abonnement   │
│ 📖 Documentation│
│ 🆘 Support      │
└─────────────────┘
```

---

## 📄 Pages Principales

### 1. **Page Recherche** (`/search`)

**Layout** :
```
┌─────────────────────────────────────────────┐
│ [Barre de recherche] [Filtres] [Options]   │
├─────────────────────────────────────────────┤
│                                             │
│  Résultats (3 colonnes)                     │
│  ┌──────┐ ┌──────┐ ┌──────┐                │
│  │ IA   │ │ Web  │ │ APIs │                │
│  │ Synth│ │ Rés. │ │ Data │                │
│  └──────┘ └──────┘ └──────┘                │
│                                             │
│  [Sources] [Export] [Partager]              │
└─────────────────────────────────────────────┘
```

**Fonctionnalités** :
- Résultats en 3 colonnes : Synthèse IA, Résultats Web, Données APIs
- Filtres par catégorie (News, Finance, Images, etc.)
- Export JSON/CSV/Markdown
- Partage social

---

### 2. **Page Chat** (`/chat`)

**Layout** :
```
┌─────────────────────────────────────────────┐
│ [Nouveau] [Historique] [Paramètres]        │
├─────────────────────────────────────────────┤
│                                             │
│  💬 Conversation                            │
│  ┌─────────────────────────────────────┐  │
│  │ User: "Quel est le prix du Bitcoin?"│  │
│  │ AI: [Réponse avec sources]          │  │
│  │      📊 CoinGecko: $45,230          │  │
│  │      📈 24h: +2.5%                  │  │
│  └─────────────────────────────────────┘  │
│                                             │
│  [Input] [Envoyer] [Voice] [Attach]        │
└─────────────────────────────────────────────┘
```

**Fonctionnalités** :
- Chat conversationnel
- Sources citées
- Export conversation
- Historique des chats

---

### 3. **Page Explorer** (`/explore`)

**Layout** :
```
┌─────────────────────────────────────────────┐
│  Explorer 78+ APIs                          │
├─────────────────────────────────────────────┤
│                                             │
│  [Catégories]                               │
│  🤖 AI (10)  💰 Finance (5)  📰 News (6)   │
│  🌍 Geo (6)  📚 Books (3)  🎭 Fun (8)      │
│                                             │
│  [Grille d'APIs]                           │
│  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐          │
│  │Groq │ │Mistr│ │Wiki │ │Jokes│          │
│  │14K/d│ │100K │ │Free │ │Free │          │
│  └─────┘ └─────┘ └─────┘ └─────┘          │
│                                             │
│  [Tester] [Documentation] [Stats]          │
└─────────────────────────────────────────────┘
```

**Fonctionnalités** :
- Vue par catégories
- Test direct des APIs
- Documentation inline
- Statistiques d'utilisation

---

### 4. **Page Historique** (`/history`)

**Layout** :
```
┌─────────────────────────────────────────────┐
│  Historique des Recherches                 │
├─────────────────────────────────────────────┤
│  [Filtres: Date, Type, Catégorie]          │
│                                             │
│  📅 Aujourd'hui                             │
│  • "Prix Bitcoin" - Recherche IA - 14:30    │
│  • "Météo Paris" - Recherche simple - 12:15 │
│                                             │
│  📅 Hier                                    │
│  • "Blague Python" - Chat - 18:45          │
│                                             │
│  [Exporter tout] [Effacer]                 │
└─────────────────────────────────────────────┘
```

---

### 5. **Page Documentation** (`/docs`)

**Layout** :
```
┌─────────────────────────────────────────────┐
│  Documentation API                          │
├─────────────────────────────────────────────┤
│  [Sidebar Navigation]                       │
│  • Quick Start                              │
│  • Authentication                           │
│  • Endpoints                                │
│    - AI Chat                                │
│    - Search                                 │
│    - APIs                                   │
│  • Examples                                 │
│  • SDKs                                     │
│                                             │
│  [Contenu Documentation]                    │
│  [Code Examples]                            │
│  [Try it]                                   │
└─────────────────────────────────────────────┘
```

---

### 6. **Page Pricing** (`/pricing`)

**Layout** :
```
┌─────────────────────────────────────────────┐
│  Tarifs                                     │
├─────────────────────────────────────────────┤
│                                             │
│  [Free] [Starter] [Pro] [Business]         │
│                                             │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐     │
│  │ Free    │ │ Starter │ │ Pro     │     │
│  │ 0€/mois │ │ 9€/mois │ │ 29€/mois│     │
│  │ 50/jour │ │ 500/jour│ │ 5K/jour │     │
│  │ [Start] │ │ [Start] │ │ [Start] │     │
│  └─────────┘ └─────────┘ └─────────┘     │
│                                             │
└─────────────────────────────────────────────┘
```

---

## 🎨 Design System

### Couleurs

```css
Primary: #6366F1 (Indigo)
Accent: #8B5CF6 (Purple)
Success: #10B981 (Green)
Warning: #F59E0B (Amber)
Error: #EF4444 (Red)

Background: #0F172A (Dark Slate)
Card: #1E293B (Slate)
Border: #334155 (Slate)
Text: #F1F5F9 (Slate)
Text Muted: #94A3B8 (Slate)
```

### Typographie

```
Heading: Inter Bold
Body: Inter Regular
Code: JetBrains Mono
```

### Composants

- **SearchBar** : Grande barre centrale avec suggestions
- **ResultCard** : Carte de résultat avec source, preview
- **ChatBubble** : Bulle de chat (user/assistant)
- **APICard** : Carte API avec statut, quota, test
- **StatsWidget** : Widget statistiques
- **ExportButton** : Bouton export (JSON/CSV/MD)

---

## 🚀 Fonctionnalités Clés

### 1. Recherche Intelligente

- **Auto-complétion** : Suggestions en temps réel
- **Recherche vocale** : Voice input (Web Speech API)
- **Recherche image** : Upload d'image pour recherche visuelle
- **Recherche multi-langue** : FR, EN, ES, DE, etc.

### 2. Résultats Enrichis

- **Synthèse IA** : Résumé intelligent des résultats
- **Sources multiples** : Wikipedia, News, APIs, etc.
- **Visualisations** : Graphiques pour données financières
- **Images/GIFs** : Résultats visuels (Giphy, Pixabay)

### 3. Personnalisation

- **Thèmes** : Dark/Light mode
- **Préférences** : Langue, région, providers favoris
- **Raccourcis** : Keyboard shortcuts
- **Widgets** : Dashboard personnalisable

### 4. Social & Partage

- **Partage** : Twitter, LinkedIn, Email
- **Export** : JSON, CSV, Markdown, PDF
- **Embed** : Code embed pour sites web
- **API Key** : Génération de clés API

---

## 📱 Responsive Design

### Desktop (>1024px)
- Sidebar fixe
- 3 colonnes de résultats
- Menu horizontal

### Tablet (768px-1024px)
- Sidebar collapsible
- 2 colonnes de résultats
- Menu hamburger

### Mobile (<768px)
- Menu bottom navigation
- 1 colonne de résultats
- Touch-optimized

---

## 🔐 Authentification

### Pages Auth

- `/login` : Connexion (Email/Password, OAuth)
- `/register` : Inscription
- `/forgot-password` : Mot de passe oublié
- `/verify-email` : Vérification email

### User Menu

```
[Avatar] ▼
├── Mon Profil
├── Paramètres
├── Abonnement
├── API Keys
├── Facturation
└── Déconnexion
```

---

## 📊 Dashboard (Utilisateurs Pro)

### Page Dashboard (`/dashboard`)

```
┌─────────────────────────────────────────────┐
│  Dashboard                                  │
├─────────────────────────────────────────────┤
│  [Stats Cards]                              │
│  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐           │
│  │ 450 │ │ 23K │ │ 98% │ │ 12h │           │
│  │Req  │ │Quota│ │Uptime│ │Avg  │           │
│  └─────┘ └─────┘ └─────┘ └─────┘           │
│                                             │
│  [Graphiques]                               │
│  • Requêtes par jour                        │
│  • APIs les plus utilisées                  │
│  • Coûts par provider                       │
│                                             │
│  [Activité récente]                         │
└─────────────────────────────────────────────┘
```

---

## 🎯 Navigation Flow

```
Accueil (/)
  ├── Recherche (/search)
  │   └── Résultat détaillé (/search/[id])
  ├── Chat (/chat)
  │   └── Conversation (/chat/[id])
  ├── Explorer (/explore)
  │   └── API Detail (/explore/[api])
  ├── Historique (/history)
  ├── Documentation (/docs)
  ├── Pricing (/pricing)
  └── Dashboard (/dashboard) [Pro]
```

---

## 🛠️ Technologies

- **Framework** : Next.js 14 (App Router)
- **Styling** : Tailwind CSS
- **UI Components** : shadcn/ui
- **Icons** : Lucide React
- **State** : Zustand
- **Forms** : React Hook Form
- **Charts** : Recharts
- **Code Highlight** : Prism.js

---

## 🎨 Mockups Clés

### Hero Section
- Grande barre de recherche centrale
- Gradient background animé
- Stats en cards (70+ APIs, 10 AI Providers, etc.)
- CTA "Commencer gratuitement"

### Search Results
- 3 colonnes : IA | Web | APIs
- Filtres latéraux
- Pagination
- Export/Share buttons

### Chat Interface
- Messages avec sources
- Markdown rendering
- Code syntax highlighting
- File attachments

---

## 🚀 MVP Features (Phase 1)

1. ✅ Page d'accueil avec recherche
2. ✅ Page résultats (3 colonnes)
3. ✅ Page chat
4. ✅ Page explorer (liste APIs)
5. ✅ Authentification basique
6. ✅ Historique simple

## 🎯 Phase 2

1. Dashboard analytics
2. Export avancé
3. Partage social
4. Recherche vocale
5. Thèmes personnalisés

---

**Cette architecture crée une expérience utilisateur moderne et intuitive pour aska.ai !** 🚀

