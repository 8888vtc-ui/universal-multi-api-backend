# 🚀 Guide de Déploiement sur Fly.io

## ✨ Pourquoi Fly.io ?

**Avantages par rapport à Oracle Cloud :**
- ✅ **Déploiement en 5 minutes** (vs 30+ minutes)
- ✅ **SSL automatique** (HTTPS gratuit)
- ✅ **Scaling automatique** (0 → N instances)
- ✅ **Pas de configuration serveur** (pas de SSH, Nginx, etc.)
- ✅ **Gratuit jusqu'à 3 machines partagées**
- ✅ **CDN global** (latence réduite)
- ✅ **Rollback automatique** en cas d'erreur
- ✅ **Logs en temps réel** via CLI

---

## 📋 Prérequis

1. **Compte Fly.io** : https://fly.io/app/sign-up (gratuit)
2. **Fly CLI** installé sur votre machine
3. **Git** pour versionner le code

---

## 🔧 Étape 1 : Installer Fly CLI

### Windows (PowerShell)

```powershell
# Télécharger et installer Fly CLI
iwr https://fly.io/install.ps1 -useb | iex
```

### Vérifier l'installation

```powershell
fly version
```

---

## 🔐 Étape 2 : Se connecter à Fly.io

```powershell
# Se connecter (ouvre le navigateur)
fly auth login

# Vérifier votre compte
fly auth whoami
```

---

## 📦 Étape 3 : Initialiser le projet

```powershell
# Aller dans le dossier backend
cd "D:\moteur israelien\backend"

# Initialiser Fly.io (si pas déjà fait)
fly launch --no-deploy
```

**Note** : Si `fly.toml` existe déjà, cette étape peut être ignorée.

---

## ⚙️ Étape 4 : Configurer les variables d'environnement

### Créer un fichier `.env` sur Fly.io

```powershell
# Définir les variables d'environnement
fly secrets set JWT_SECRET_KEY=$(python -c "import secrets; print(secrets.token_urlsafe(64))")
fly secrets set ENVIRONMENT=production
fly secrets set API_HOST=0.0.0.0
fly secrets set API_PORT=8000
fly secrets set CORS_ORIGINS=https://votre-app.fly.dev,http://localhost:3000
```

### Ajouter vos clés API

```powershell
# Exemple avec Groq
fly secrets set GROQ_API_KEY=votre_cle_groq

# Ajouter toutes vos clés API
fly secrets set MISTRAL_API_KEY=votre_cle_mistral
fly secrets set GEMINI_API_KEY=votre_cle_gemini
fly secrets set COHERE_API_KEY=votre_cle_cohere
fly secrets set AI21_API_KEY=votre_cle_ai21
fly secrets set ANTHROPIC_API_KEY=votre_cle_anthropic
fly secrets set PERPLEXITY_API_KEY=votre_cle_perplexity
fly secrets set HUGGINGFACE_API_TOKEN=votre_cle_hf
# ... ajouter toutes les autres clés
```

### Voir les secrets configurés

```powershell
fly secrets list
```

---

## 🚀 Étape 5 : Déployer

```powershell
# Déployer l'application
fly deploy

# Ou avec logs en temps réel
fly deploy --verbose
```

**Le déploiement prend 3-5 minutes** et inclut :
- ✅ Build de l'image Docker
- ✅ Push vers le registry Fly.io
- ✅ Déploiement sur les machines
- ✅ Configuration SSL automatique
- ✅ Health checks

---

## ✅ Étape 6 : Vérifier le déploiement

### Voir l'URL de votre app

```powershell
fly status
```

Vous obtiendrez quelque chose comme : `https://universal-api-hub.fly.dev`

### Tester les endpoints

```powershell
# Health check
curl https://universal-api-hub.fly.dev/api/health

# Documentation
# Ouvrir dans le navigateur : https://universal-api-hub.fly.dev/docs
```

---

## 📊 Commandes Utiles

### Gérer l'application

```powershell
# Voir le statut
fly status

# Voir les logs en temps réel
fly logs

# Voir les logs filtrés
fly logs --app universal-api-hub

# Redémarrer l'app
fly apps restart universal-api-hub

# Arrêter l'app (économie de ressources)
fly scale count 0

# Démarrer l'app
fly scale count 1
```

### Gérer les secrets

```powershell
# Lister les secrets
fly secrets list

# Ajouter un secret
fly secrets set NOUVEAU_SECRET=valeur

# Supprimer un secret
fly secrets unset NOUVEAU_SECRET
```

### Scaling

```powershell
# Augmenter le nombre d'instances
fly scale count 3

# Augmenter la RAM
fly scale memory 1024

# Voir les options de scaling
fly scale show
```

### SSH dans le conteneur

```powershell
# Se connecter en SSH
fly ssh console

# Exécuter une commande
fly ssh console -C "python --version"
```

---

## 🔄 Mettre à jour le code

```powershell
# 1. Modifier le code
# 2. Commit Git (optionnel mais recommandé)
git add .
git commit -m "Update backend"

# 3. Redéployer
fly deploy

# Ou déployer depuis un autre dossier
fly deploy --config backend/fly.toml
```

---

## 🐛 Dépannage

### L'app ne démarre pas

```powershell
# Voir les logs d'erreur
fly logs

# Voir les détails de l'app
fly status

# Vérifier les secrets
fly secrets list
```

### Erreur de build

```powershell
# Build local pour tester
fly deploy --local-only

# Voir les logs de build
fly logs --build
```

### Erreur de connexion

```powershell
# Vérifier que l'app est running
fly status

# Vérifier les health checks
fly checks list
```

### Rollback vers une version précédente

```powershell
# Voir les releases
fly releases

# Rollback vers une release spécifique
fly releases rollback <RELEASE_ID>
```

---

## 💰 Coûts Fly.io

### Plan Gratuit (Hobby)

- ✅ **3 machines partagées** (gratuit)
- ✅ **3 GB de stockage** (gratuit)
- ✅ **160 GB de bande passante** (gratuit)
- ✅ **SSL automatique** (gratuit)

### Plan Payant (à partir de $5/mois)

- Plus de machines
- Machines dédiées (meilleures performances)
- Plus de stockage
- Support prioritaire

**Pour ce projet** : Le plan gratuit est largement suffisant pour commencer !

---

## 🌐 Configuration DNS personnalisée

### Ajouter un domaine personnalisé

```powershell
# Ajouter un domaine
fly certs add api.votre-domaine.com

# Vérifier les certificats
fly certs show
```

Fly.io génère automatiquement les certificats SSL via Let's Encrypt.

---

## 📈 Monitoring

### Métriques

```powershell
# Voir les métriques
fly metrics

# Métriques en temps réel
fly dashboard
```

### Logs avancés

```powershell
# Logs avec filtres
fly logs --region cdg
fly logs --app universal-api-hub --instance <INSTANCE_ID>
```

---

## 🔒 Sécurité

### Variables sensibles

✅ **Toujours utiliser `fly secrets`** pour les clés API, jamais dans le code !

```powershell
# ✅ Bon
fly secrets set API_KEY=secret123

# ❌ Mauvais (ne jamais faire ça)
# Dans le code : API_KEY = "secret123"
```

### Firewall

Fly.io gère automatiquement le firewall. Les ports sont exposés uniquement via HTTPS.

---

## 🎯 Checklist de Déploiement

```
□ Fly CLI installé
□ Compte Fly.io créé
□ Connecté à Fly.io (fly auth login)
□ fly.toml configuré
□ Secrets configurés (JWT_SECRET_KEY, clés API)
□ Déploiement réussi (fly deploy)
□ Health check OK (https://votre-app.fly.dev/api/health)
□ Documentation accessible (https://votre-app.fly.dev/docs)
```

---

## 🚀 Comparaison : Fly.io vs Oracle Cloud

| Critère | Fly.io | Oracle Cloud |
|---------|--------|--------------|
| **Temps de déploiement** | 5 min | 30+ min |
| **Configuration** | Automatique | Manuelle (SSH, Nginx, etc.) |
| **SSL** | Automatique | Manuel (Let's Encrypt) |
| **Scaling** | Automatique | Manuel |
| **Coût** | Gratuit (3 machines) | Gratuit (1 machine) |
| **Complexité** | ⭐ Facile | ⭐⭐⭐ Complexe |
| **Maintenance** | Minimale | Élevée |

---

## 📚 Ressources

- **Documentation Fly.io** : https://fly.io/docs/
- **Pricing** : https://fly.io/docs/about/pricing/
- **Status** : https://status.fly.io/

---

**Votre backend est maintenant déployé sur Fly.io ! 🎉**

Accès : `https://universal-api-hub.fly.dev`





