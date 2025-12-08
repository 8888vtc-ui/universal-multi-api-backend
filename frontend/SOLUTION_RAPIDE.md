# ⚡ Solution Rapide - Déploiement Netlify

## ✅ Le Build Local Fonctionne !

Votre build local compile sans erreur. Le problème est dans la configuration Netlify.

## 🔧 Solution en 3 Étapes

### Étape 1 : Vérifier la Configuration Netlify

Dans Netlify Dashboard → **Site settings** → **Build & deploy** :

**Build settings** :
- **Build command** : `npm run build`
- **Publish directory** : **LAISSER VIDE** ⚠️ IMPORTANT
- **Base directory** : **LAISSER VIDE**

**Pourquoi** : Le plugin Next.js gère automatiquement le répertoire.

### Étape 2 : Installer le Plugin Next.js

Dans Netlify Dashboard → **Site settings** → **Plugins** :

1. Cliquer sur **"Add plugin"**
2. Chercher **"Essential Next.js Plugin"**
3. Cliquer sur **"Install"**

**OU** via le fichier `netlify.toml` (déjà configuré) :
```toml
[[plugins]]
  package = "@netlify/plugin-nextjs"
```

### Étape 3 : Vérifier les Variables d'Environnement

Dans Netlify Dashboard → **Site settings** → **Environment variables** :

Vérifier que vous avez exactement :
```
NEXT_PUBLIC_API_URL = https://universal-api-hub.fly.dev
NEXT_PUBLIC_APP_NAME = WikiAsk
NEXT_PUBLIC_APP_SLOGAN = Ask Everything. Know Everything.
```

⚠️ **IMPORTANT** : Pas d'espaces autour du `=`

## 🚀 Redéployer

Après ces vérifications :

1. **Option A** : Pousser un changement sur GitHub
   ```bash
   git add .
   git commit -m "Fix Netlify config"
   git push
   ```

2. **Option B** : Redéployer manuellement dans Netlify
   - Deploys → Trigger deploy → Deploy site

## 🔍 Vérifier les Logs

Si ça ne fonctionne toujours pas :

1. Aller dans **Deploys**
2. Cliquer sur le dernier déploiement
3. Voir les **Deploy log**
4. **Copier les erreurs** et me les envoyer

## 📋 Checklist Rapide

- [ ] Build command : `npm run build`
- [ ] Publish directory : **VIDE**
- [ ] Plugin Next.js installé
- [ ] Variables d'environnement correctes
- [ ] Redéployé après les changements

---

**Si ça ne fonctionne toujours pas, envoyez-moi les logs de build Netlify !** 🔧





