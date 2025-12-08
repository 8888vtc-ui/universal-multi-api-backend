# 🚀 Script de Déploiement Automatique

Script PowerShell pour déployer automatiquement le backend (Fly.io) et le frontend (Netlify) avec surveillance et vérification automatique.

## ✨ Fonctionnalités

- ✅ **Surveillance automatique** des modifications de fichiers
- ✅ **Déploiement automatique** backend (Fly.io) et frontend (Netlify)
- ✅ **Vérification automatique** que les déploiements sont pris en charge
- ✅ **Lecture des logs** en cas d'erreur
- ✅ **Correction automatique** des problèmes courants
- ✅ **Retry automatique** jusqu'à ce que le déploiement soit pris en charge

## 📋 Prérequis

### Backend (Fly.io)

```powershell
# Installer Fly CLI
iwr https://fly.io/install.ps1 -useb | iex

# Se connecter
fly auth login

# Vérifier la connexion
fly auth whoami
```

### Frontend (Netlify)

- Netlify connecté à votre repository GitHub
- Déploiement automatique activé dans Netlify Dashboard

### PowerShell

```powershell
# Autoriser l'exécution de scripts
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## 🚀 Utilisation

### Mode Surveillance (Recommandé)

Démarre la surveillance et déploie automatiquement à chaque modification :

```powershell
# Surveiller et déployer tout
.\auto-deploy.ps1 -Watch

# Surveiller uniquement le backend
.\auto-deploy.ps1 -Watch -Backend

# Surveiller uniquement le frontend
.\auto-deploy.ps1 -Watch -Frontend
```

### Déploiement Unique

Déploie une seule fois sans surveillance :

```powershell
# Déployer tout
.\auto-deploy.ps1

# Déployer uniquement le backend
.\auto-deploy.ps1 -Backend

# Déployer uniquement le frontend
.\auto-deploy.ps1 -Frontend
```

## 🔍 Comment ça fonctionne

### 1. Surveillance des fichiers

Le script surveille tous les fichiers dans le projet (sauf ceux dans `.git`, `node_modules`, etc.).

Quand une modification est détectée :
- Il détermine si c'est backend ou frontend
- Il attend 2 secondes pour éviter les déploiements multiples
- Il respecte un cooldown de 30 secondes entre déploiements

### 2. Déploiement Backend

1. **Vérification** : Fly CLI installé et connecté
2. **Déploiement** : `fly deploy --remote-only`
3. **Vérification** : Test de l'endpoint `/api/health`
4. **En cas d'erreur** :
   - Lecture des logs : `fly logs`
   - Analyse des erreurs
   - Correction automatique (redémarrage, vérification secrets)
   - Retry jusqu'à succès

### 3. Déploiement Frontend

1. **Vérification** : Changements détectés via `git status`
2. **Commit** : Commit automatique avec timestamp
3. **Push** : Push sur `origin main`
4. **Vérification** : Vérification que le commit est sur GitHub
5. **En cas d'erreur** :
   - Lecture des logs Netlify (si CLI installé)
   - Analyse des erreurs
   - Correction automatique (rebuild local)
   - Retry jusqu'à succès

### 4. Vérification et Correction

Le script vérifie automatiquement que les déploiements sont pris en charge :

**Backend** :
- Test de l'endpoint `/api/health`
- Vérification que le service répond
- Lecture des logs en cas d'échec
- Correction automatique (redémarrage, secrets)

**Frontend** :
- Vérification du commit sur GitHub
- Vérification Netlify (si CLI installé)
- Lecture des logs en cas d'échec
- Correction automatique (rebuild)

## ⚙️ Configuration

Modifiez les variables au début du script :

```powershell
$BACKEND_DIR = "backend"
$FRONTEND_DIR = "frontend"
$FLY_APP = "universal-api-hub"
$BACKEND_URL = "https://$FLY_APP.fly.dev"
```

## 🐛 Dépannage

### Le script ne détecte pas les modifications

- Vérifiez que vous êtes dans le bon répertoire
- Vérifiez que les fichiers ne sont pas dans les patterns ignorés
- Redémarrez le script

### Le backend ne se déploie pas

```powershell
# Vérifier la connexion Fly.io
fly auth whoami

# Vérifier l'application
cd backend
fly status
fly logs
```

### Le frontend ne se déploie pas

```powershell
# Vérifier Git
git status
git remote -v

# Vérifier Netlify (si CLI installé)
cd frontend
netlify status
```

### Erreurs de permissions PowerShell

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## 📝 Exemples

### Exemple 1 : Déploiement manuel

```powershell
# Déployer tout une fois
.\auto-deploy.ps1
```

### Exemple 2 : Surveillance continue

```powershell
# Démarrer la surveillance
.\auto-deploy.ps1 -Watch

# Le script surveille et déploie automatiquement
# Appuyez sur Ctrl+C pour arrêter
```

### Exemple 3 : Déploiement backend uniquement

```powershell
# Déployer uniquement le backend
.\auto-deploy.ps1 -Backend -Watch
```

## 🔒 Sécurité

- Le script ne modifie que les fichiers nécessaires
- Les secrets ne sont jamais affichés
- Les logs sensibles sont filtrés

## 📊 Logs

Le script affiche :
- ✅ **Vert** : Succès
- ⚠️ **Jaune** : Avertissement
- ❌ **Rouge** : Erreur
- 🔍 **Cyan** : Information
- 🔧 **Gris** : Debug

## 🎯 Workflow Recommandé

1. **Développement local** : Modifiez vos fichiers
2. **Surveillance active** : Lancez `.\auto-deploy.ps1 -Watch`
3. **Modification détectée** : Le script déploie automatiquement
4. **Vérification** : Le script vérifie que tout fonctionne
5. **Correction** : En cas d'erreur, le script essaie de corriger

## 💡 Astuces

- Laissez le script tourner en arrière-plan pendant le développement
- Vérifiez les logs si un déploiement échoue
- Le cooldown de 30 secondes évite les déploiements multiples
- Les fichiers dans `.git`, `node_modules`, etc. sont ignorés automatiquement

## 🆘 Support

En cas de problème :
1. Vérifiez les logs affichés par le script
2. Vérifiez les logs Fly.io : `fly logs`
3. Vérifiez le dashboard Netlify
4. Vérifiez que tous les prérequis sont installés

---

**Créé le** : 2025-12-07  
**Version** : 1.0.0



Script PowerShell pour déployer automatiquement le backend (Fly.io) et le frontend (Netlify) avec surveillance et vérification automatique.

## ✨ Fonctionnalités

- ✅ **Surveillance automatique** des modifications de fichiers
- ✅ **Déploiement automatique** backend (Fly.io) et frontend (Netlify)
- ✅ **Vérification automatique** que les déploiements sont pris en charge
- ✅ **Lecture des logs** en cas d'erreur
- ✅ **Correction automatique** des problèmes courants
- ✅ **Retry automatique** jusqu'à ce que le déploiement soit pris en charge

## 📋 Prérequis

### Backend (Fly.io)

```powershell
# Installer Fly CLI
iwr https://fly.io/install.ps1 -useb | iex

# Se connecter
fly auth login

# Vérifier la connexion
fly auth whoami
```

### Frontend (Netlify)

- Netlify connecté à votre repository GitHub
- Déploiement automatique activé dans Netlify Dashboard

### PowerShell

```powershell
# Autoriser l'exécution de scripts
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## 🚀 Utilisation

### Mode Surveillance (Recommandé)

Démarre la surveillance et déploie automatiquement à chaque modification :

```powershell
# Surveiller et déployer tout
.\auto-deploy.ps1 -Watch

# Surveiller uniquement le backend
.\auto-deploy.ps1 -Watch -Backend

# Surveiller uniquement le frontend
.\auto-deploy.ps1 -Watch -Frontend
```

### Déploiement Unique

Déploie une seule fois sans surveillance :

```powershell
# Déployer tout
.\auto-deploy.ps1

# Déployer uniquement le backend
.\auto-deploy.ps1 -Backend

# Déployer uniquement le frontend
.\auto-deploy.ps1 -Frontend
```

## 🔍 Comment ça fonctionne

### 1. Surveillance des fichiers

Le script surveille tous les fichiers dans le projet (sauf ceux dans `.git`, `node_modules`, etc.).

Quand une modification est détectée :
- Il détermine si c'est backend ou frontend
- Il attend 2 secondes pour éviter les déploiements multiples
- Il respecte un cooldown de 30 secondes entre déploiements

### 2. Déploiement Backend

1. **Vérification** : Fly CLI installé et connecté
2. **Déploiement** : `fly deploy --remote-only`
3. **Vérification** : Test de l'endpoint `/api/health`
4. **En cas d'erreur** :
   - Lecture des logs : `fly logs`
   - Analyse des erreurs
   - Correction automatique (redémarrage, vérification secrets)
   - Retry jusqu'à succès

### 3. Déploiement Frontend

1. **Vérification** : Changements détectés via `git status`
2. **Commit** : Commit automatique avec timestamp
3. **Push** : Push sur `origin main`
4. **Vérification** : Vérification que le commit est sur GitHub
5. **En cas d'erreur** :
   - Lecture des logs Netlify (si CLI installé)
   - Analyse des erreurs
   - Correction automatique (rebuild local)
   - Retry jusqu'à succès

### 4. Vérification et Correction

Le script vérifie automatiquement que les déploiements sont pris en charge :

**Backend** :
- Test de l'endpoint `/api/health`
- Vérification que le service répond
- Lecture des logs en cas d'échec
- Correction automatique (redémarrage, secrets)

**Frontend** :
- Vérification du commit sur GitHub
- Vérification Netlify (si CLI installé)
- Lecture des logs en cas d'échec
- Correction automatique (rebuild)

## ⚙️ Configuration

Modifiez les variables au début du script :

```powershell
$BACKEND_DIR = "backend"
$FRONTEND_DIR = "frontend"
$FLY_APP = "universal-api-hub"
$BACKEND_URL = "https://$FLY_APP.fly.dev"
```

## 🐛 Dépannage

### Le script ne détecte pas les modifications

- Vérifiez que vous êtes dans le bon répertoire
- Vérifiez que les fichiers ne sont pas dans les patterns ignorés
- Redémarrez le script

### Le backend ne se déploie pas

```powershell
# Vérifier la connexion Fly.io
fly auth whoami

# Vérifier l'application
cd backend
fly status
fly logs
```

### Le frontend ne se déploie pas

```powershell
# Vérifier Git
git status
git remote -v

# Vérifier Netlify (si CLI installé)
cd frontend
netlify status
```

### Erreurs de permissions PowerShell

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## 📝 Exemples

### Exemple 1 : Déploiement manuel

```powershell
# Déployer tout une fois
.\auto-deploy.ps1
```

### Exemple 2 : Surveillance continue

```powershell
# Démarrer la surveillance
.\auto-deploy.ps1 -Watch

# Le script surveille et déploie automatiquement
# Appuyez sur Ctrl+C pour arrêter
```

### Exemple 3 : Déploiement backend uniquement

```powershell
# Déployer uniquement le backend
.\auto-deploy.ps1 -Backend -Watch
```

## 🔒 Sécurité

- Le script ne modifie que les fichiers nécessaires
- Les secrets ne sont jamais affichés
- Les logs sensibles sont filtrés

## 📊 Logs

Le script affiche :
- ✅ **Vert** : Succès
- ⚠️ **Jaune** : Avertissement
- ❌ **Rouge** : Erreur
- 🔍 **Cyan** : Information
- 🔧 **Gris** : Debug

## 🎯 Workflow Recommandé

1. **Développement local** : Modifiez vos fichiers
2. **Surveillance active** : Lancez `.\auto-deploy.ps1 -Watch`
3. **Modification détectée** : Le script déploie automatiquement
4. **Vérification** : Le script vérifie que tout fonctionne
5. **Correction** : En cas d'erreur, le script essaie de corriger

## 💡 Astuces

- Laissez le script tourner en arrière-plan pendant le développement
- Vérifiez les logs si un déploiement échoue
- Le cooldown de 30 secondes évite les déploiements multiples
- Les fichiers dans `.git`, `node_modules`, etc. sont ignorés automatiquement

## 🆘 Support

En cas de problème :
1. Vérifiez les logs affichés par le script
2. Vérifiez les logs Fly.io : `fly logs`
3. Vérifiez le dashboard Netlify
4. Vérifiez que tous les prérequis sont installés

---

**Créé le** : 2025-12-07  
**Version** : 1.0.0



