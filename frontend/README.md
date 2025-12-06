# 🚀 WikiAsk - Frontend

Moteur de recherche IA intelligent qui agrège 78+ APIs pour des résultats complets et précis.

## ✨ Fonctionnalités

- 🔍 **Recherche intelligente** avec auto-complétion
- ✨ **Recherche IA** (RAG) avec synthèse intelligente
- 💬 **Chat conversationnel** avec 10 providers IA
- 🌐 **Explorer 78+ APIs** avec testeur intégré
- 📊 **Dashboard analytics** pour les utilisateurs Pro
- 📱 **Design responsive** (Mobile/Tablet/Desktop)
- 🌙 **Dark mode** par défaut

## 🛠️ Technologies

- **Next.js 14.2.5** - Framework React
- **TypeScript** - Typage statique
- **Tailwind CSS** - Styling
- **Zustand** - State management
- **Lucide React** - Icônes

## 📦 Installation

```bash
npm install
```

## 🚀 Développement

```bash
npm run dev
```

Ouvrir [http://localhost:3000](http://localhost:3000)

## 🏗️ Build

```bash
npm run build
npm start
```

## 🌐 Déploiement

### Netlify (Recommandé)

1. **Via GitHub** :
   - Pousser le code sur GitHub
   - Connecter le repo à Netlify
   - Netlify détecte automatiquement la config

2. **Via CLI** :
   ```bash
   npm install -g netlify-cli
   netlify login
   netlify init
   netlify deploy --prod
   ```

### Variables d'environnement

Créer `.env.local` :
```env
NEXT_PUBLIC_API_URL=https://api.wikiask.net
NEXT_PUBLIC_APP_NAME=WikiAsk
NEXT_PUBLIC_APP_SLOGAN=Ask Everything. Know Everything.
```

Dans Netlify Dashboard → Site settings → Environment variables

## 📁 Structure

```
frontend/
├── app/              # Pages Next.js
├── components/        # Composants React
├── hooks/            # Hooks personnalisés
├── lib/              # Utilitaires et API client
├── store/            # Zustand store
├── public/           # Assets statiques
└── netlify.toml      # Configuration Netlify
```

## 🔗 Domaines

- **Production** : https://wikiask.net
- **API** : https://api.wikiask.net
- **Redirections** : wikiask.fr, wikiask.io → wikiask.net

## 📝 Scripts

- `npm run dev` - Développement
- `npm run build` - Build production
- `npm run start` - Serveur production
- `npm run lint` - Linter

## 🎨 Design

- **Thème** : Dark mode par défaut
- **Couleurs** : Indigo/Purple gradient
- **Style** : Glassmorphism moderne
- **Responsive** : Mobile-first

## 📄 License

Propriétaire - WikiAsk © 2024
