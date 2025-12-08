# 🚀 Guide : Pousser sur GitHub et Déployer sur Netlify

## ✅ Étape 1 : Créer le Repository GitHub

1. Aller sur [github.com](https://github.com)
2. Cliquer sur **"New repository"**
3. Remplir :
   - **Repository name** : `wikiask-frontend` (ou `wikiask`)
   - **Description** : "WikiAsk - Moteur de recherche IA intelligent"
   - **Visibility** : Public ou Private (selon votre choix)
   - **NE PAS** cocher "Initialize with README" (on a déjà un README)
4. Cliquer sur **"Create repository"**

## ✅ Étape 2 : Pousser le Code sur GitHub

Dans le terminal, depuis le dossier `frontend` :

```bash
# Ajouter le remote GitHub
git remote add origin https://github.com/VOTRE-USERNAME/wikiask-frontend.git

# Renommer la branche en main (si nécessaire)
git branch -M main

# Pousser le code
git push -u origin main
```

**Note** : Remplacez `VOTRE-USERNAME` par votre nom d'utilisateur GitHub.

## ✅ Étape 3 : Connecter à Netlify

### Option A : Via l'Interface Web (Recommandé)

1. Aller sur [netlify.com](https://netlify.com)
2. Se connecter avec votre compte GitHub
3. Cliquer sur **"Add new site"** → **"Import an existing project"**
4. Choisir **"GitHub"**
5. Autoriser Netlify à accéder à vos repos
6. Sélectionner le repository `wikiask-frontend`
7. Netlify détecte automatiquement :
   - **Build command** : `npm run build`
   - **Publish directory** : `.next`
   - **Framework** : Next.js
8. Cliquer sur **"Deploy site"**

### Option B : Via CLI

```bash
# Se connecter à Netlify
netlify login

# Lier le site
netlify link

# Déployer
netlify deploy --prod
```

## ✅ Étape 4 : Configurer les Variables d'Environnement

Dans Netlify Dashboard :

1. Aller dans **Site settings** → **Environment variables**
2. Ajouter :
   ```
   NEXT_PUBLIC_API_URL = https://api.wikiask.net
   NEXT_PUBLIC_APP_NAME = WikiAsk
   NEXT_PUBLIC_APP_SLOGAN = Ask Everything. Know Everything.
   ```
3. Cliquer sur **"Save"**
4. **Redéployer** le site (Deploys → Trigger deploy → Deploy site)

## ✅ Étape 5 : Configurer les Domaines

### Ajouter wikiask.net

1. Dans Netlify Dashboard → **Site settings** → **Domain management**
2. Cliquer sur **"Add custom domain"**
3. Entrer `wikiask.net`
4. Suivre les instructions pour vérifier le domaine

### Configurer DNS

Chez votre registrar (où vous avez acheté le domaine) :

**Pour wikiask.net** :
```
Type: A
Name: @
Value: 75.2.60.5
```

**OU** (si votre registrar supporte CNAME pour la racine) :
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

### Ajouter les autres domaines

1. **wikiask.fr** → Ajouter dans Netlify (redirection automatique vers .net)
2. **wikiask.io** → Ajouter dans Netlify (redirection automatique vers .net)

## ✅ Étape 6 : Vérifier le Déploiement

1. Attendre que le build se termine (2-3 minutes)
2. Vérifier l'URL Netlify : `https://wikiask-XXXX.netlify.app`
3. Tester les fonctionnalités
4. Une fois le DNS configuré, tester `https://wikiask.net`

## 🔄 Déploiements Automatiques

Désormais, chaque `git push` déclenchera automatiquement un nouveau déploiement !

```bash
# Faire des modifications
git add .
git commit -m "Description des changements"
git push

# Netlify déploie automatiquement ! 🚀
```

## 📊 Preview Deployments

Pour chaque Pull Request, Netlify crée automatiquement un preview deployment avec une URL unique. Parfait pour tester avant de merger !

## ✅ Checklist Finale

- [ ] Repository GitHub créé
- [ ] Code poussé sur GitHub
- [ ] Site connecté à Netlify
- [ ] Variables d'environnement configurées
- [ ] Domaine wikiask.net ajouté
- [ ] DNS configuré
- [ ] SSL activé (automatique)
- [ ] Site accessible sur wikiask.net
- [ ] Redirections .fr et .io fonctionnent

---

**Prêt à déployer !** 🎉





