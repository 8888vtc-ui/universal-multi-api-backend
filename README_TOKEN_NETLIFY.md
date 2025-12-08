# 🔑 Utilisation du Token Netlify

## 📋 Comment Obtenir un Token Netlify

1. **Aller sur** : https://app.netlify.com/user/applications
2. **Cliquer sur** : "New access token"
3. **Donner un nom** : "WikiAsk Configuration" (ou autre)
4. **Copier le token** : Il ne sera affiché qu'une seule fois !

---

## 🚀 Utilisation du Script

### Option 1 : Ligne de commande

```powershell
.\configure-netlify-api.ps1 -NetlifyToken "votre-token-ici"
```

### Option 2 : Avec Force (mettre à jour les variables existantes)

```powershell
.\configure-netlify-api.ps1 -NetlifyToken "votre-token-ici" -Force
```

---

## 🔒 Sécurité

⚠️ **IMPORTANT** : Ne partagez JAMAIS votre token !

- Le token donne accès à votre compte Netlify
- Stockez-le de manière sécurisée
- Ne le commitez pas dans Git
- Utilisez des variables d'environnement si possible

### Utiliser une Variable d'Environnement

```powershell
# Définir la variable (une seule fois)
$env:NETLIFY_TOKEN = "votre-token"

# Utiliser le script
.\configure-netlify-api.ps1 -NetlifyToken $env:NETLIFY_TOKEN
```

---

## ✅ Ce que le Script Fait

1. ✅ Vérifie que le token est valide
2. ✅ Vérifie l'accès au site Netlify
3. ✅ Liste les variables existantes
4. ✅ Configure les 3 variables :
   - `NEXT_PUBLIC_API_URL`
   - `NEXT_PUBLIC_APP_NAME`
   - `NEXT_PUBLIC_APP_SLOGAN`
5. ✅ Configure pour tous les contextes (production, preview, branch)
6. ✅ Vérifie que tout est bien configuré

---

## 🎯 Variables Configurées

| Variable | Valeur | Contextes |
|----------|--------|-----------|
| `NEXT_PUBLIC_API_URL` | `https://universal-api-hub.fly.dev` | production, deploy-preview, branch-deploy |
| `NEXT_PUBLIC_APP_NAME` | `WikiAsk` | production, deploy-preview, branch-deploy |
| `NEXT_PUBLIC_APP_SLOGAN` | `Ask Everything. Know Everything.` | production, deploy-preview, branch-deploy |

---

## 🔧 Dépannage

### Erreur : "Token invalide"
- Vérifiez que vous avez copié le token complet
- Générez un nouveau token si nécessaire

### Erreur : "Impossible d'accéder au site"
- Vérifiez que le SITE_ID est correct
- Vérifiez que le token a les bonnes permissions

### Variables déjà existantes
- Utilisez `-Force` pour les mettre à jour
- Ou supprimez-les manuellement dans le Dashboard

---

**Date** : 07/12/2025  
**Status** : ✅ Script prêt à utiliser



## 📋 Comment Obtenir un Token Netlify

1. **Aller sur** : https://app.netlify.com/user/applications
2. **Cliquer sur** : "New access token"
3. **Donner un nom** : "WikiAsk Configuration" (ou autre)
4. **Copier le token** : Il ne sera affiché qu'une seule fois !

---

## 🚀 Utilisation du Script

### Option 1 : Ligne de commande

```powershell
.\configure-netlify-api.ps1 -NetlifyToken "votre-token-ici"
```

### Option 2 : Avec Force (mettre à jour les variables existantes)

```powershell
.\configure-netlify-api.ps1 -NetlifyToken "votre-token-ici" -Force
```

---

## 🔒 Sécurité

⚠️ **IMPORTANT** : Ne partagez JAMAIS votre token !

- Le token donne accès à votre compte Netlify
- Stockez-le de manière sécurisée
- Ne le commitez pas dans Git
- Utilisez des variables d'environnement si possible

### Utiliser une Variable d'Environnement

```powershell
# Définir la variable (une seule fois)
$env:NETLIFY_TOKEN = "votre-token"

# Utiliser le script
.\configure-netlify-api.ps1 -NetlifyToken $env:NETLIFY_TOKEN
```

---

## ✅ Ce que le Script Fait

1. ✅ Vérifie que le token est valide
2. ✅ Vérifie l'accès au site Netlify
3. ✅ Liste les variables existantes
4. ✅ Configure les 3 variables :
   - `NEXT_PUBLIC_API_URL`
   - `NEXT_PUBLIC_APP_NAME`
   - `NEXT_PUBLIC_APP_SLOGAN`
5. ✅ Configure pour tous les contextes (production, preview, branch)
6. ✅ Vérifie que tout est bien configuré

---

## 🎯 Variables Configurées

| Variable | Valeur | Contextes |
|----------|--------|-----------|
| `NEXT_PUBLIC_API_URL` | `https://universal-api-hub.fly.dev` | production, deploy-preview, branch-deploy |
| `NEXT_PUBLIC_APP_NAME` | `WikiAsk` | production, deploy-preview, branch-deploy |
| `NEXT_PUBLIC_APP_SLOGAN` | `Ask Everything. Know Everything.` | production, deploy-preview, branch-deploy |

---

## 🔧 Dépannage

### Erreur : "Token invalide"
- Vérifiez que vous avez copié le token complet
- Générez un nouveau token si nécessaire

### Erreur : "Impossible d'accéder au site"
- Vérifiez que le SITE_ID est correct
- Vérifiez que le token a les bonnes permissions

### Variables déjà existantes
- Utilisez `-Force` pour les mettre à jour
- Ou supprimez-les manuellement dans le Dashboard

---

**Date** : 07/12/2025  
**Status** : ✅ Script prêt à utiliser



