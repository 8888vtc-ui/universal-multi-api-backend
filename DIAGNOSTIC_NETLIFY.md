# 🔍 Diagnostic Netlify - Problèmes d'Accès

## ❌ Problème Identifié

Les commandes Netlify CLI semblent **bloquées** ou **lentes**. Les commandes sont annulées ou ne répondent pas.

## 🔍 Causes Possibles

### 1. **Authentification Expirée**
- Le token Netlify peut avoir expiré
- La session peut être invalide

### 2. **Problème de Réseau**
- Connexion lente ou instable
- Firewall bloquant les appels API Netlify
- Proxy d'entreprise

### 3. **Netlify CLI Non Installé ou Corrompu**
- Installation incomplète
- Version obsolète
- Cache corrompu

### 4. **Projet Non Lié Correctement**
- Le projet peut être lié mais avec un mauvais ID
- Fichier `.netlify` corrompu

---

## ✅ Solutions

### Solution 1 : Ré-authentifier Netlify

```powershell
# Se déconnecter
netlify logout

# Se reconnecter
netlify login
```

**Note** : Cela ouvrira un navigateur pour l'authentification.

---

### Solution 2 : Vérifier l'Installation

```powershell
# Vérifier si installé
npm list -g netlify-cli

# Réinstaller si nécessaire
npm uninstall -g netlify-cli
npm install -g netlify-cli
```

---

### Solution 3 : Utiliser le Dashboard Netlify (Alternative)

Si la CLI ne fonctionne pas, **utilisez le Dashboard Web** :

1. Aller sur : https://app.netlify.com/projects/incomparable-semolina-c3a66d
2. **Site settings** → **Environment variables**
3. Ajouter manuellement :
   - `NEXT_PUBLIC_API_URL` = `https://universal-api-hub.fly.dev`
   - `NEXT_PUBLIC_APP_NAME` = `WikiAsk`
   - `NEXT_PUBLIC_APP_SLOGAN` = `Ask Everything. Know Everything.`

**Avantages** :
- ✅ Pas besoin de CLI
- ✅ Interface graphique
- ✅ Plus rapide

---

### Solution 4 : Vérifier le Fichier de Configuration

Le projet devrait avoir un fichier `.netlify/state.json` dans `frontend/` :

```powershell
cd frontend
Get-Content .netlify/state.json
```

Si le fichier n'existe pas ou est corrompu :

```powershell
cd frontend
netlify link --id 2d6f74c0-6884-479f-9d56-19b6003a9b08
```

---

## 🎯 Recommandation Immédiate

**Utilisez le Dashboard Netlify** pour configurer les variables :

1. ✅ Plus fiable que la CLI
2. ✅ Pas de problème d'authentification
3. ✅ Interface visuelle
4. ✅ Changements immédiats

**URL** : https://app.netlify.com/projects/incomparable-semolina-c3a66d/settings/env

---

## 📋 Checklist de Vérification

- [ ] Netlify CLI installé : `npm list -g netlify-cli`
- [ ] Authentifié : `netlify whoami`
- [ ] Projet lié : `netlify status`
- [ ] Variables configurées : Dashboard Netlify
- [ ] Site accessible : https://wikiask.net

---

## 🔧 Script de Diagnostic

Créez un fichier `test-netlify.ps1` :

```powershell
Write-Host "=== Diagnostic Netlify ===" -ForegroundColor Cyan

# 1. Vérifier installation
Write-Host "`n1. Vérification installation..." -ForegroundColor Yellow
$netlify = Get-Command netlify -ErrorAction SilentlyContinue
if ($netlify) {
    Write-Host "   ✅ Netlify CLI installé: $($netlify.Source)" -ForegroundColor Green
} else {
    Write-Host "   ❌ Netlify CLI non installé" -ForegroundColor Red
    Write-Host "   💡 Installez avec: npm install -g netlify-cli" -ForegroundColor Yellow
    exit 1
}

# 2. Vérifier authentification
Write-Host "`n2. Vérification authentification..." -ForegroundColor Yellow
$whoami = netlify whoami 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "   ✅ Authentifié: $whoami" -ForegroundColor Green
} else {
    Write-Host "   ❌ Non authentifié" -ForegroundColor Red
    Write-Host "   💡 Connectez-vous avec: netlify login" -ForegroundColor Yellow
    exit 1
}

# 3. Vérifier projet lié
Write-Host "`n3. Vérification projet lié..." -ForegroundColor Yellow
cd frontend
$status = netlify status 2>&1
if ($status -match "Project already linked") {
    Write-Host "   ✅ Projet lié" -ForegroundColor Green
    Write-Host "   $status" -ForegroundColor Gray
} else {
    Write-Host "   ❌ Projet non lié" -ForegroundColor Red
    Write-Host "   💡 Liez avec: netlify link --id 2d6f74c0-6884-479f-9d56-19b6003a9b08" -ForegroundColor Yellow
}

# 4. Tester commande simple
Write-Host "`n4. Test commande env:list..." -ForegroundColor Yellow
$envList = netlify env:list 2>&1 | Select-Object -First 5
if ($LASTEXITCODE -eq 0) {
    Write-Host "   ✅ Commande fonctionne" -ForegroundColor Green
    Write-Host "   $envList" -ForegroundColor Gray
} else {
    Write-Host "   ❌ Commande échoue" -ForegroundColor Red
    Write-Host "   $envList" -ForegroundColor Red
}

Write-Host "`n=== Fin du diagnostic ===" -ForegroundColor Cyan
```

---

**Date** : 07/12/2025  
**Status** : ⚠️ CLI Netlify semble bloquée, utiliser Dashboard comme alternative



## ❌ Problème Identifié

Les commandes Netlify CLI semblent **bloquées** ou **lentes**. Les commandes sont annulées ou ne répondent pas.

## 🔍 Causes Possibles

### 1. **Authentification Expirée**
- Le token Netlify peut avoir expiré
- La session peut être invalide

### 2. **Problème de Réseau**
- Connexion lente ou instable
- Firewall bloquant les appels API Netlify
- Proxy d'entreprise

### 3. **Netlify CLI Non Installé ou Corrompu**
- Installation incomplète
- Version obsolète
- Cache corrompu

### 4. **Projet Non Lié Correctement**
- Le projet peut être lié mais avec un mauvais ID
- Fichier `.netlify` corrompu

---

## ✅ Solutions

### Solution 1 : Ré-authentifier Netlify

```powershell
# Se déconnecter
netlify logout

# Se reconnecter
netlify login
```

**Note** : Cela ouvrira un navigateur pour l'authentification.

---

### Solution 2 : Vérifier l'Installation

```powershell
# Vérifier si installé
npm list -g netlify-cli

# Réinstaller si nécessaire
npm uninstall -g netlify-cli
npm install -g netlify-cli
```

---

### Solution 3 : Utiliser le Dashboard Netlify (Alternative)

Si la CLI ne fonctionne pas, **utilisez le Dashboard Web** :

1. Aller sur : https://app.netlify.com/projects/incomparable-semolina-c3a66d
2. **Site settings** → **Environment variables**
3. Ajouter manuellement :
   - `NEXT_PUBLIC_API_URL` = `https://universal-api-hub.fly.dev`
   - `NEXT_PUBLIC_APP_NAME` = `WikiAsk`
   - `NEXT_PUBLIC_APP_SLOGAN` = `Ask Everything. Know Everything.`

**Avantages** :
- ✅ Pas besoin de CLI
- ✅ Interface graphique
- ✅ Plus rapide

---

### Solution 4 : Vérifier le Fichier de Configuration

Le projet devrait avoir un fichier `.netlify/state.json` dans `frontend/` :

```powershell
cd frontend
Get-Content .netlify/state.json
```

Si le fichier n'existe pas ou est corrompu :

```powershell
cd frontend
netlify link --id 2d6f74c0-6884-479f-9d56-19b6003a9b08
```

---

## 🎯 Recommandation Immédiate

**Utilisez le Dashboard Netlify** pour configurer les variables :

1. ✅ Plus fiable que la CLI
2. ✅ Pas de problème d'authentification
3. ✅ Interface visuelle
4. ✅ Changements immédiats

**URL** : https://app.netlify.com/projects/incomparable-semolina-c3a66d/settings/env

---

## 📋 Checklist de Vérification

- [ ] Netlify CLI installé : `npm list -g netlify-cli`
- [ ] Authentifié : `netlify whoami`
- [ ] Projet lié : `netlify status`
- [ ] Variables configurées : Dashboard Netlify
- [ ] Site accessible : https://wikiask.net

---

## 🔧 Script de Diagnostic

Créez un fichier `test-netlify.ps1` :

```powershell
Write-Host "=== Diagnostic Netlify ===" -ForegroundColor Cyan

# 1. Vérifier installation
Write-Host "`n1. Vérification installation..." -ForegroundColor Yellow
$netlify = Get-Command netlify -ErrorAction SilentlyContinue
if ($netlify) {
    Write-Host "   ✅ Netlify CLI installé: $($netlify.Source)" -ForegroundColor Green
} else {
    Write-Host "   ❌ Netlify CLI non installé" -ForegroundColor Red
    Write-Host "   💡 Installez avec: npm install -g netlify-cli" -ForegroundColor Yellow
    exit 1
}

# 2. Vérifier authentification
Write-Host "`n2. Vérification authentification..." -ForegroundColor Yellow
$whoami = netlify whoami 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "   ✅ Authentifié: $whoami" -ForegroundColor Green
} else {
    Write-Host "   ❌ Non authentifié" -ForegroundColor Red
    Write-Host "   💡 Connectez-vous avec: netlify login" -ForegroundColor Yellow
    exit 1
}

# 3. Vérifier projet lié
Write-Host "`n3. Vérification projet lié..." -ForegroundColor Yellow
cd frontend
$status = netlify status 2>&1
if ($status -match "Project already linked") {
    Write-Host "   ✅ Projet lié" -ForegroundColor Green
    Write-Host "   $status" -ForegroundColor Gray
} else {
    Write-Host "   ❌ Projet non lié" -ForegroundColor Red
    Write-Host "   💡 Liez avec: netlify link --id 2d6f74c0-6884-479f-9d56-19b6003a9b08" -ForegroundColor Yellow
}

# 4. Tester commande simple
Write-Host "`n4. Test commande env:list..." -ForegroundColor Yellow
$envList = netlify env:list 2>&1 | Select-Object -First 5
if ($LASTEXITCODE -eq 0) {
    Write-Host "   ✅ Commande fonctionne" -ForegroundColor Green
    Write-Host "   $envList" -ForegroundColor Gray
} else {
    Write-Host "   ❌ Commande échoue" -ForegroundColor Red
    Write-Host "   $envList" -ForegroundColor Red
}

Write-Host "`n=== Fin du diagnostic ===" -ForegroundColor Cyan
```

---

**Date** : 07/12/2025  
**Status** : ⚠️ CLI Netlify semble bloquée, utiliser Dashboard comme alternative



