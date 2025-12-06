# 🔧 Corrections Apportées au Déploiement Netlify

## ❌ Problèmes Identifiés

1. **Publish directory incorrect** : `.next` n'est pas le bon répertoire pour Next.js avec le plugin Netlify
2. **Redirect API incorrect** : Pointe vers `api.wikiask.net` qui n'existe pas encore

## ✅ Corrections Effectuées

### 1. Configuration netlify.toml

**AVANT** :
```toml
[build]
  command = "npm run build"
  publish = ".next"
```

**APRÈS** :
```toml
[build]
  command = "npm run build"
  # Le plugin Next.js gère automatiquement le publish directory
```

**Pourquoi** : Le plugin `@netlify/plugin-nextjs` gère automatiquement le répertoire de publication. Il ne faut pas spécifier `publish = ".next"`.

### 2. Redirect API

**AVANT** :
```toml
[[redirects]]
  from = "/api/*"
  to = "https://api.wikiask.net/api/:splat"
```

**APRÈS** :
```toml
[[redirects]]
  from = "/api/*"
  to = "https://universal-api-hub.fly.dev/api/:splat"
```

**Pourquoi** : `api.wikiask.net` n'est pas encore configuré. Utiliser directement Fly.io.

## 📋 Actions à Effectuer dans Netlify

### 1. Vérifier les Settings de Build

Dans Netlify Dashboard → Site settings → Build & deploy :

- **Build command** : `npm run build`
- **Publish directory** : **LAISSER VIDE** (le plugin gère)
- **Base directory** : (vide si le repo est directement le frontend)

### 2. Vérifier le Plugin

Le plugin `@netlify/plugin-nextjs` doit être installé automatiquement. Si ce n'est pas le cas :

1. Site settings → Plugins
2. Installer "Essential Next.js Plugin"

### 3. Variables d'Environnement

Vérifier que vous avez bien :
```
NEXT_PUBLIC_API_URL = https://universal-api-hub.fly.dev
NEXT_PUBLIC_APP_NAME = WikiAsk
NEXT_PUBLIC_APP_SLOGAN = Ask Everything. Know Everything.
```

### 4. Redéployer

Après ces corrections :
1. Pousser les changements sur GitHub
2. Netlify redéploiera automatiquement
3. OU : Trigger deploy manuel dans Netlify Dashboard

## 🔍 Vérification

Après le redéploiement, vérifier :

1. **Build réussit** : Vérifier les logs dans Netlify
2. **Site accessible** : Tester l'URL Netlify
3. **API fonctionne** : Tester un appel API depuis le frontend
4. **Pas d'erreurs console** : Ouvrir la console du navigateur

## ⚠️ Si le Build Échoue Encore

### Erreur : "Cannot find module"
- Vérifier que `package.json` est à la racine du repo
- Vérifier que toutes les dépendances sont dans `package.json`

### Erreur : "Build directory not found"
- Laisser le publish directory vide
- Le plugin Next.js gère automatiquement

### Erreur : "Plugin not found"
- Installer le plugin dans Netlify Dashboard
- Ou ajouter dans `netlify.toml` (déjà fait)

---

**Fichiers modifiés** :
- ✅ `netlify.toml` - Publish directory et redirect API corrigés

**Prochaine étape** : Pousser sur GitHub et redéployer !

