# ⚡ Quick Start - Déploiement Rapide

**Pour ceux qui veulent déployer rapidement**

---

## 🚀 Déploiement en 5 Minutes

### 1. Créer le Serveur VPS (2 min)

- Aller sur [Hetzner Cloud](https://www.hetzner.com/cloud)
- Créer un compte
- Créer un serveur CPX31 (Ubuntu 22.04)
- Noter l'IP

### 2. Se Connecter (1 min)

```bash
ssh root@VOTRE_IP
```

### 3. Déployer (2 min)

```bash
# Installer Git
apt update && apt install -y git

# Cloner (remplacer par votre repo)
cd /opt
git clone VOTRE_REPO_URL universal-api
cd universal-api/backend

# Déployer
chmod +x scripts/*.sh
sudo bash scripts/deploy.sh production
```

### 4. Vérifier (30 sec)

```bash
# Vérification automatique
sudo bash scripts/verify_deployment.sh

# Test manuel
curl http://localhost:8000/api/health
```

**C'est tout ! 🎉**

---

## 📋 Commandes Essentielles

```bash
# Status
systemctl status universal-api

# Logs
journalctl -u universal-api -f

# Restart
systemctl restart universal-api

# Health
curl http://localhost:8000/api/health

# Metrics
curl http://localhost:8000/api/metrics
```

---

## 🔧 Configuration Rapide

### Changer le Domaine

Éditer `backend/scripts/deploy.sh` :
```bash
DOMAIN="${DOMAIN:-votre-domaine.com}"
```

Puis réexécuter le déploiement.

### Configurer SSL

```bash
certbot --nginx -d votre-domaine.com
```

---

## 📚 Documentation Complète

- **ETAPES_SUITE.md** : Guide détaillé étape par étape
- **MIGRATION_COMPLETE.md** : Guide complet de migration
- **DEPLOYMENT_GUIDE.md** : Guide de déploiement approfondi

---

**Bon déploiement ! 🚀**


