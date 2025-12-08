# ✅ Configuration Netlify via Dashboard (Solution Alternative)

## 🎯 Pourquoi Utiliser le Dashboard ?

Les commandes Netlify CLI sont **lentes ou bloquées** à cause de :
- ⚠️ Authentification qui timeout
- ⚠️ Projet non correctement lié
- ⚠️ Problèmes réseau

**Solution** : Utiliser le **Dashboard Web Netlify** (plus fiable et rapide)

---

## 📋 Étapes de Configuration

### 1. Accéder au Dashboard

**URL Directe** : https://app.netlify.com/projects/incomparable-semolina-c3a66d/settings/env

Ou :
1. Aller sur https://app.netlify.com
2. Cliquer sur le projet **"incomparable-semolina-c3a66d"**
3. **Site settings** → **Environment variables**

---

### 2. Ajouter les Variables d'Environnement

Cliquez sur **"Add variable"** et ajoutez :

#### Variable 1 : `NEXT_PUBLIC_API_URL`
- **Key** : `NEXT_PUBLIC_API_URL`
- **Value** : `https://universal-api-hub.fly.dev`
- **Scopes** : ✅ Production, ✅ Deploy previews, ✅ Branch deploys

#### Variable 2 : `NEXT_PUBLIC_APP_NAME`
- **Key** : `NEXT_PUBLIC_APP_NAME`
- **Value** : `WikiAsk`
- **Scopes** : ✅ Production, ✅ Deploy previews, ✅ Branch deploys

#### Variable 3 : `NEXT_PUBLIC_APP_SLOGAN`
- **Key** : `NEXT_PUBLIC_APP_SLOGAN`
- **Value** : `Ask Everything. Know Everything.`
- **Scopes** : ✅ Production, ✅ Deploy previews, ✅ Branch deploys

---

### 3. Sauvegarder et Redéployer

1. Cliquez sur **"Save"** pour chaque variable
2. Allez dans **"Deploys"** (menu de gauche)
3. Cliquez sur **"Trigger deploy"** → **"Deploy site"**
4. Attendez 2-3 minutes que le déploiement se termine

---

## ✅ Vérification

### Vérifier que les Variables sont Configurées

1. Retournez dans **Site settings** → **Environment variables**
2. Vous devriez voir les 3 variables listées

### Tester le Site

1. Allez sur https://wikiask.net
2. Ouvrez la console du navigateur (F12)
3. Vérifiez qu'il n'y a pas d'erreurs d'API
4. Testez un appel API (ex: poser une question à un expert)

---

## 🔧 Alternative : Script PowerShell avec API Netlify

Si vous préférez automatiser, vous pouvez utiliser l'API Netlify directement :

```powershell
# Nécessite un token Netlify (généré dans User settings → Applications)
$NETLIFY_TOKEN = "votre-token"
$SITE_ID = "2d6f74c0-6884-479f-9d56-19b6003a9b08"

$headers = @{
    "Authorization" = "Bearer $NETLIFY_TOKEN"
    "Content-Type" = "application/json"
}

# Ajouter variable
$body = @{
    key = "NEXT_PUBLIC_API_URL"
    values = @(
        @{
            value = "https://universal-api-hub.fly.dev"
            context = "production"
        },
        @{
            value = "https://universal-api-hub.fly.dev"
            context = "deploy-preview"
        },
        @{
            value = "https://universal-api-hub.fly.dev"
            context = "branch-deploy"
        }
    )
} | ConvertTo-Json -Depth 10

Invoke-RestMethod -Uri "https://api.netlify.com/api/v1/sites/$SITE_ID/env" -Method Post -Headers $headers -Body $body
```

**Pour obtenir un token** :
1. https://app.netlify.com/user/applications
2. Cliquez sur **"New access token"**
3. Copiez le token généré

---

## 📊 Résumé

| Méthode | Avantages | Inconvénients |
|---------|-----------|---------------|
| **Dashboard Web** | ✅ Rapide, fiable, visuel | ⚠️ Manuel |
| **CLI Netlify** | ✅ Automatisable | ❌ Bloqué/timeout |
| **API Netlify** | ✅ Automatisable, fiable | ⚠️ Nécessite token |

**Recommandation** : Utiliser le **Dashboard Web** pour l'instant, c'est le plus simple et fiable.

---

## 🎯 Checklist

- [ ] Accéder au Dashboard Netlify
- [ ] Ajouter `NEXT_PUBLIC_API_URL`
- [ ] Ajouter `NEXT_PUBLIC_APP_NAME`
- [ ] Ajouter `NEXT_PUBLIC_APP_SLOGAN`
- [ ] Configurer pour tous les scopes (production, preview, branch)
- [ ] Sauvegarder
- [ ] Redéployer le site
- [ ] Vérifier que le site fonctionne

---

**Date** : 07/12/2025  
**Status** : ✅ Solution alternative recommandée (Dashboard Web)



## 🎯 Pourquoi Utiliser le Dashboard ?

Les commandes Netlify CLI sont **lentes ou bloquées** à cause de :
- ⚠️ Authentification qui timeout
- ⚠️ Projet non correctement lié
- ⚠️ Problèmes réseau

**Solution** : Utiliser le **Dashboard Web Netlify** (plus fiable et rapide)

---

## 📋 Étapes de Configuration

### 1. Accéder au Dashboard

**URL Directe** : https://app.netlify.com/projects/incomparable-semolina-c3a66d/settings/env

Ou :
1. Aller sur https://app.netlify.com
2. Cliquer sur le projet **"incomparable-semolina-c3a66d"**
3. **Site settings** → **Environment variables**

---

### 2. Ajouter les Variables d'Environnement

Cliquez sur **"Add variable"** et ajoutez :

#### Variable 1 : `NEXT_PUBLIC_API_URL`
- **Key** : `NEXT_PUBLIC_API_URL`
- **Value** : `https://universal-api-hub.fly.dev`
- **Scopes** : ✅ Production, ✅ Deploy previews, ✅ Branch deploys

#### Variable 2 : `NEXT_PUBLIC_APP_NAME`
- **Key** : `NEXT_PUBLIC_APP_NAME`
- **Value** : `WikiAsk`
- **Scopes** : ✅ Production, ✅ Deploy previews, ✅ Branch deploys

#### Variable 3 : `NEXT_PUBLIC_APP_SLOGAN`
- **Key** : `NEXT_PUBLIC_APP_SLOGAN`
- **Value** : `Ask Everything. Know Everything.`
- **Scopes** : ✅ Production, ✅ Deploy previews, ✅ Branch deploys

---

### 3. Sauvegarder et Redéployer

1. Cliquez sur **"Save"** pour chaque variable
2. Allez dans **"Deploys"** (menu de gauche)
3. Cliquez sur **"Trigger deploy"** → **"Deploy site"**
4. Attendez 2-3 minutes que le déploiement se termine

---

## ✅ Vérification

### Vérifier que les Variables sont Configurées

1. Retournez dans **Site settings** → **Environment variables**
2. Vous devriez voir les 3 variables listées

### Tester le Site

1. Allez sur https://wikiask.net
2. Ouvrez la console du navigateur (F12)
3. Vérifiez qu'il n'y a pas d'erreurs d'API
4. Testez un appel API (ex: poser une question à un expert)

---

## 🔧 Alternative : Script PowerShell avec API Netlify

Si vous préférez automatiser, vous pouvez utiliser l'API Netlify directement :

```powershell
# Nécessite un token Netlify (généré dans User settings → Applications)
$NETLIFY_TOKEN = "votre-token"
$SITE_ID = "2d6f74c0-6884-479f-9d56-19b6003a9b08"

$headers = @{
    "Authorization" = "Bearer $NETLIFY_TOKEN"
    "Content-Type" = "application/json"
}

# Ajouter variable
$body = @{
    key = "NEXT_PUBLIC_API_URL"
    values = @(
        @{
            value = "https://universal-api-hub.fly.dev"
            context = "production"
        },
        @{
            value = "https://universal-api-hub.fly.dev"
            context = "deploy-preview"
        },
        @{
            value = "https://universal-api-hub.fly.dev"
            context = "branch-deploy"
        }
    )
} | ConvertTo-Json -Depth 10

Invoke-RestMethod -Uri "https://api.netlify.com/api/v1/sites/$SITE_ID/env" -Method Post -Headers $headers -Body $body
```

**Pour obtenir un token** :
1. https://app.netlify.com/user/applications
2. Cliquez sur **"New access token"**
3. Copiez le token généré

---

## 📊 Résumé

| Méthode | Avantages | Inconvénients |
|---------|-----------|---------------|
| **Dashboard Web** | ✅ Rapide, fiable, visuel | ⚠️ Manuel |
| **CLI Netlify** | ✅ Automatisable | ❌ Bloqué/timeout |
| **API Netlify** | ✅ Automatisable, fiable | ⚠️ Nécessite token |

**Recommandation** : Utiliser le **Dashboard Web** pour l'instant, c'est le plus simple et fiable.

---

## 🎯 Checklist

- [ ] Accéder au Dashboard Netlify
- [ ] Ajouter `NEXT_PUBLIC_API_URL`
- [ ] Ajouter `NEXT_PUBLIC_APP_NAME`
- [ ] Ajouter `NEXT_PUBLIC_APP_SLOGAN`
- [ ] Configurer pour tous les scopes (production, preview, branch)
- [ ] Sauvegarder
- [ ] Redéployer le site
- [ ] Vérifier que le site fonctionne

---

**Date** : 07/12/2025  
**Status** : ✅ Solution alternative recommandée (Dashboard Web)



