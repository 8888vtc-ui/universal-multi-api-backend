# 🚀 Étapes pour Déployer sur Netlify

## ✅ Étape 1 : Code sur GitHub (TERMINÉ)

✅ Repository : https://github.com/8888vtc-ui/WikiAsk
✅ Code poussé avec succès

## 📋 Étape 2 : Connecter à Netlify

### Option A : Via l'Interface Web (Recommandé - 5 minutes)

1. **Aller sur Netlify** : https://app.netlify.com
2. **Se connecter** avec votre compte GitHub
3. **Cliquer sur** : "Add new site" → "Import an existing project"
4. **Choisir** : "GitHub"
5. **Autoriser** Netlify à accéder à vos repos GitHub
6. **Sélectionner** le repository : `8888vtc-ui/WikiAsk`
7. **Netlify détecte automatiquement** :
   - ✅ Build command : `npm run build`
   - ✅ Publish directory : `.next`
   - ✅ Framework : Next.js
8. **Cliquer sur** : "Deploy site"

### Option B : Via CLI (Alternative)

```bash
# Se connecter
netlify login

# Lier le site
netlify link

# Déployer
netlify deploy --prod
```

## ⚙️ Étape 3 : Configurer les Variables d'Environnement

**IMPORTANT** : À faire après le premier déploiement

1. Dans Netlify Dashboard → **Site settings** → **Environment variables**
2. Cliquer sur **"Add variable"**
3. Ajouter ces 3 variables :

```
NEXT_PUBLIC_API_URL = https://api.wikiask.net
NEXT_PUBLIC_APP_NAME = WikiAsk
NEXT_PUBLIC_APP_SLOGAN = Ask Everything. Know Everything.
```

4. Cliquer sur **"Save"**
5. **Redéployer** : Deploys → Trigger deploy → Deploy site

## 🌐 Étape 4 : Configurer les Domaines

### 4.1 Ajouter wikiask.net

1. Netlify Dashboard → **Site settings** → **Domain management**
2. Cliquer sur **"Add custom domain"**
3. Entrer : `wikiask.net`
4. Suivre les instructions pour vérifier le domaine

### 4.2 Configurer DNS chez votre Registrar

**Pour wikiask.net** (racine) :
```
Type: A
Name: @
Value: 75.2.60.5
```

**OU** (si votre registrar supporte CNAME pour racine) :
```
Type: CNAME
Name: @
Value: wikiask.netlify.app
```

**Pour www.wikiask.net** :
```
Type: CNAME
Name: www
Value: wikiask.netlify.app
```

### 4.3 Ajouter les autres domaines

1. **wikiask.fr** → Ajouter dans Netlify (redirection auto vers .net)
2. **wikiask.io** → Ajouter dans Netlify (redirection auto vers .net)

Les redirections sont déjà configurées dans `netlify.toml` ✅

## ✅ Étape 5 : Vérifier le Déploiement

1. **Attendre** que le build se termine (2-3 minutes)
2. **Vérifier** l'URL Netlify : `https://wikiask-XXXX.netlify.app`
3. **Tester** les fonctionnalités
4. **Une fois DNS configuré** : Tester `https://wikiask.net`

## 🔄 Déploiements Automatiques

Désormais, chaque `git push` déclenchera automatiquement un nouveau déploiement !

```bash
git add .
git commit -m "Description des changements"
git push
# Netlify déploie automatiquement ! 🚀
```

## 📊 Preview Deployments

Pour chaque Pull Request, Netlify crée automatiquement un preview deployment avec une URL unique.

## ✅ Checklist Finale

- [x] Code sur GitHub
- [ ] Site connecté à Netlify
- [ ] Variables d'environnement configurées
- [ ] Domaine wikiask.net ajouté
- [ ] DNS configuré
- [ ] SSL activé (automatique)
- [ ] Site accessible sur wikiask.net

## 🆘 En cas de problème

### Build échoue
- Vérifier les logs dans Netlify Dashboard
- Vérifier que `npm run build` fonctionne localement

### Domaines ne fonctionnent pas
- Vérifier les DNS (peut prendre 24-48h)
- Vérifier dans Netlify Dashboard → Domain management

### API ne répond pas
- Vérifier `NEXT_PUBLIC_API_URL` dans les variables d'environnement
- Vérifier que `api.wikiask.net` est bien configuré sur Fly.io

---

**Prochaine étape** : Aller sur https://app.netlify.com et connecter le repository ! 🚀

