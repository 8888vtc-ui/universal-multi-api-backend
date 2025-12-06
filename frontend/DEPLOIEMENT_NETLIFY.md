# 🚀 Guide de Déploiement WikiAsk sur Netlify

## ✅ Configuration Prête

Tous les fichiers de configuration Netlify sont créés :
- ✅ `netlify.toml` - Configuration Netlify
- ✅ `next.config.js` - Adapté pour Netlify
- ✅ Redirections configurées
- ✅ Headers de sécurité

## 📋 Étapes de Déploiement

### Option 1 : Déploiement via Netlify CLI (Recommandé)

#### 1. Installer Netlify CLI
```bash
npm install -g netlify-cli
```

#### 2. Se connecter à Netlify
```bash
netlify login
```

#### 3. Initialiser le projet
```bash
cd frontend
netlify init
```

Répondre aux questions :
- **Create & configure a new site** : Oui
- **Team** : Votre équipe
- **Site name** : `wikiask` (ou laissez Netlify générer)
- **Build command** : `npm run build`
- **Directory to deploy** : `.next`

#### 4. Déployer
```bash
netlify deploy --prod
```

### Option 2 : Déploiement via GitHub (Recommandé pour CI/CD)

#### 1. Créer un repository GitHub
```bash
cd frontend
git init
git add .
git commit -m "Initial commit - WikiAsk frontend"
git remote add origin https://github.com/votre-username/wikiask.git
git push -u origin main
```

#### 2. Connecter à Netlify
1. Aller sur [netlify.com](https://netlify.com)
2. Cliquer sur **"Add new site"** → **"Import an existing project"**
3. Choisir **GitHub**
4. Sélectionner le repository `wikiask`
5. Configurer :
   - **Build command** : `npm run build`
   - **Publish directory** : `.next`
   - **Base directory** : `frontend` (si repo à la racine)

#### 3. Configurer les variables d'environnement
Dans Netlify Dashboard → Site settings → Environment variables :
```
NEXT_PUBLIC_API_URL=https://api.wikiask.net
NEXT_PUBLIC_APP_NAME=WikiAsk
NEXT_PUBLIC_APP_SLOGAN=Ask Everything. Know Everything.
```

## 🌐 Configuration des Domaines

### 1. Ajouter le domaine principal (wikiask.net)

Dans Netlify Dashboard :
1. **Site settings** → **Domain management**
2. **Add custom domain** → Entrer `wikiask.net`
3. **Verify domain ownership**

### 2. Configurer DNS chez votre registrar

Pour **wikiask.net** :
```
Type: A
Name: @
Value: 75.2.60.5 (IP Netlify - vérifier dans le dashboard)

OU

Type: CNAME
Name: @
Value: wikiask.netlify.app
```

Pour **www.wikiask.net** :
```
Type: CNAME
Name: www
Value: wikiask.netlify.app
```

### 3. Ajouter les autres domaines

Dans Netlify Dashboard :
1. **Add custom domain** → `wikiask.fr`
2. **Add custom domain** → `wikiask.io`
3. Les redirections vers `.net` sont automatiques (configurées dans `netlify.toml`)

### 4. SSL automatique

Netlify configure automatiquement SSL (Let's Encrypt) pour tous les domaines ✅

## 🔧 Configuration Backend (Fly.io)

### Configurer le sous-domaine API

```bash
cd backend
fly certs add api.wikiask.net
```

### Mettre à jour CORS
```bash
fly secrets set CORS_ORIGINS="https://wikiask.net,https://www.wikiask.net,https://wikiask.fr,https://wikiask.io"
```

### Configuration DNS pour API

Chez votre registrar :
```
Type: CNAME
Name: api
Value: universal-api-hub.fly.dev
```

## ✅ Checklist Déploiement

### Frontend (Netlify)
- [ ] Installer Netlify CLI
- [ ] Se connecter (`netlify login`)
- [ ] Initialiser le projet (`netlify init`)
- [ ] Déployer (`netlify deploy --prod`)
- [ ] Ajouter `wikiask.net` dans Netlify Dashboard
- [ ] Configurer DNS chez le registrar
- [ ] Vérifier SSL (automatique)
- [ ] Tester https://wikiask.net

### Backend (Fly.io)
- [ ] Configurer `api.wikiask.net` sur Fly.io
- [ ] Ajouter le certificat SSL (`fly certs add`)
- [ ] Configurer DNS CNAME
- [ ] Mettre à jour CORS_ORIGINS
- [ ] Tester https://api.wikiask.net/api/health

### Tests
- [ ] Frontend accessible sur wikiask.net
- [ ] API accessible sur api.wikiask.net
- [ ] Redirections .fr et .io fonctionnent
- [ ] SSL valide sur tous les domaines
- [ ] CORS fonctionne correctement
- [ ] Les appels API fonctionnent depuis le frontend

## 🎯 URLs Finales

- **Frontend** : https://wikiask.net
- **API** : https://api.wikiask.net
- **Redirections** : 
  - https://wikiask.fr → https://wikiask.net
  - https://wikiask.io → https://wikiask.net
  - https://www.wikiask.net → https://wikiask.net

## 📊 Fonctionnalités Netlify

- ✅ **SSL automatique** (Let's Encrypt)
- ✅ **CDN global** (Edge Network)
- ✅ **Déploiements instantanés**
- ✅ **Preview deployments** (pour chaque PR)
- ✅ **Form handling** (si besoin)
- ✅ **Analytics** (optionnel, payant)
- ✅ **Functions** (serverless, si besoin)

## 🔄 CI/CD Automatique

Avec GitHub connecté :
- Chaque `git push` déclenche un nouveau déploiement
- Les Pull Requests créent des preview deployments
- Rollback facile depuis le dashboard

## 🐛 Dépannage

### Build échoue
```bash
# Vérifier les logs
netlify logs

# Build local pour tester
npm run build
```

### Domaines ne fonctionnent pas
- Vérifier les DNS (peut prendre 24-48h)
- Vérifier dans Netlify Dashboard → Domain management

### API ne répond pas
- Vérifier `NEXT_PUBLIC_API_URL` dans les variables d'environnement
- Vérifier CORS sur le backend
- Vérifier que `api.wikiask.net` est bien configuré

---

**Prêt à déployer sur Netlify !** 🚀

