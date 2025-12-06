# 🔍 Diagnostic Complet - Problèmes de Déploiement

## ❓ Questions à Répondre

Pour mieux diagnostiquer, j'ai besoin de savoir :

1. **Où exactement ça ne fonctionne pas ?**
   - [ ] Le build local échoue ?
   - [ ] Le build Netlify échoue ?
   - [ ] Le site déployé ne s'affiche pas ?
   - [ ] Les appels API ne fonctionnent pas ?
   - [ ] Erreurs dans la console du navigateur ?

2. **Quelle est l'erreur exacte ?**
   - Message d'erreur dans Netlify ?
   - Message d'erreur dans la console ?
   - Page blanche ?
   - 404 ?

3. **Quelle est l'URL de votre site Netlify ?**
   - Format : `https://wikiask-XXXX.netlify.app`

## 🔧 Vérifications à Faire

### 1. Vérifier le Build Local

```bash
cd frontend
npm install
npm run build
```

**Si ça échoue** : Le problème est dans le code
**Si ça fonctionne** : Le problème est dans la config Netlify

### 2. Vérifier les Logs Netlify

Dans Netlify Dashboard :
1. Aller dans **Deploys**
2. Cliquer sur le dernier déploiement
3. Voir les **Deploy log**
4. Copier les erreurs

### 3. Vérifier les Variables d'Environnement

Dans Netlify Dashboard → Site settings → Environment variables :

Vérifier que vous avez :
```
NEXT_PUBLIC_API_URL = https://universal-api-hub.fly.dev
NEXT_PUBLIC_APP_NAME = WikiAsk
NEXT_PUBLIC_APP_SLOGAN = Ask Everything. Know Everything.
```

### 4. Vérifier la Configuration Netlify

Dans Netlify Dashboard → Site settings → Build & deploy :

- **Build command** : `npm run build`
- **Publish directory** : **VIDE** (laisser vide)
- **Base directory** : **VIDE** (si repo = frontend directement)

### 5. Vérifier le Plugin Next.js

Dans Netlify Dashboard → Site settings → Plugins :

- Le plugin "Essential Next.js Plugin" doit être installé
- Si absent, l'installer

## 🐛 Problèmes Courants et Solutions

### Problème 1 : Build échoue avec "Cannot find module"

**Solution** :
```bash
# Vérifier que package.json est correct
# Vérifier que node_modules existe
npm install
```

### Problème 2 : "Build directory not found"

**Solution** :
- Laisser le **Publish directory** VIDE dans Netlify
- Le plugin Next.js gère automatiquement

### Problème 3 : Page blanche

**Solution** :
- Vérifier la console du navigateur (F12)
- Vérifier les variables d'environnement
- Vérifier que l'API backend est accessible

### Problème 4 : Erreurs CORS

**Solution** :
- Vérifier que `CORS_ORIGINS` sur Fly.io inclut votre URL Netlify
- Ajouter : `https://VOTRE-URL.netlify.app`

### Problème 5 : "404 Not Found" sur les routes

**Solution** :
- Vérifier que le plugin Next.js est installé
- Vérifier que `netlify.toml` est correct

## 📋 Checklist de Dépannage

- [ ] Build local fonctionne (`npm run build`)
- [ ] Toutes les dépendances installées (`npm install`)
- [ ] Variables d'environnement configurées dans Netlify
- [ ] Publish directory VIDE dans Netlify
- [ ] Plugin Next.js installé
- [ ] Build command : `npm run build`
- [ ] Pas d'erreurs dans les logs Netlify
- [ ] Backend accessible (`https://universal-api-hub.fly.dev/api/health`)
- [ ] Console du navigateur sans erreurs

## 🆘 Besoin d'Aide

Pour m'aider à diagnostiquer, envoyez-moi :

1. **L'URL de votre site Netlify**
2. **Les logs de build Netlify** (copier-coller)
3. **Les erreurs de la console** (F12 → Console)
4. **Une capture d'écran** de la page si possible

---

**Je peux vous aider à résoudre le problème une fois que j'ai ces informations !** 🔧

