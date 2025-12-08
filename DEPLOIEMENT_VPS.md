# 🚀 Déploiement sur VPS - Guide Pratique

**Date** : Décembre 2024  
**Version** : 2.3.0  
**Dépôt** : https://github.com/8888vtc-ui/universal-multi-api-backend

---

## 📋 Prérequis

- ✅ Code poussé sur GitHub
- ✅ Serveur VPS créé (Ubuntu 22.04)
- ✅ Accès SSH au serveur
- ✅ Connaissances de base Linux

---

## 🎯 Déploiement en 5 Étapes

### ÉTAPE 1 : Se Connecter au Serveur (2 min)

```bash
# Depuis votre machine locale
ssh root@VOTRE_IP_SERVEUR

# Ou avec un utilisateur spécifique
ssh utilisateur@VOTRE_IP_SERVEUR
```

**Note** : Remplacez `VOTRE_IP_SERVEUR` par l'adresse IP de votre serveur VPS.

---

### ÉTAPE 2 : Préparer le Serveur (5 min)

```bash
# Mettre à jour le système
apt update && apt upgrade -y

# Installer les dépendances de base
apt install -y python3.9 python3-pip python3-venv git nginx curl wget

# Vérifier Python
python3 --version  # Doit être 3.9 ou supérieur
```

---

### ÉTAPE 3 : Cloner le Projet (2 min)

```bash
# Créer le répertoire
mkdir -p /opt
cd /opt

# Cloner le dépôt GitHub
git clone https://github.com/8888vtc-ui/universal-multi-api-backend.git universal-api

# Aller dans le répertoire backend
cd universal-api/backend
```

---

### ÉTAPE 4 : Configurer l'Application (5 min)

```bash
# Créer l'environnement virtuel
python3 -m venv venv

# Activer l'environnement virtuel
source venv/bin/activate

# Installer les dépendances
pip install --upgrade pip
pip install -r requirements.txt

# Copier .env.example vers .env
cp .env.example .env

# Éditer .env avec vos clés API
nano .env
```

**Important** : Dans `.env`, configurez au minimum :
```env
JWT_SECRET_KEY=<générer avec: python3 -c "import secrets; print(secrets.token_urlsafe(32))">
ENVIRONMENT=production
API_PORT=8000
API_HOST=0.0.0.0
```

---

### ÉTAPE 5 : Déployer avec le Script Automatique (10 min)

```bash
# Rendre les scripts exécutables
chmod +x scripts/*.sh

# Exécuter le script de déploiement
sudo bash scripts/deploy.sh production
```

Le script va automatiquement :
- ✅ Installer toutes les dépendances
- ✅ Configurer Python et l'environnement virtuel
- ✅ Créer le service systemd
- ✅ Configurer Nginx
- ✅ Démarrer le service

**Durée** : ~10-15 minutes

---

## ✅ Vérification Post-Déploiement

### Vérification Automatique

```bash
# Exécuter le script de vérification
sudo bash scripts/verify_deployment.sh
```

### Vérification Manuelle

```bash
# Vérifier le service
systemctl status universal-api

# Vérifier les logs
journalctl -u universal-api -f

# Tester les endpoints
curl http://localhost:8000/api/health
curl http://localhost:8000/api/info
curl http://localhost:8000/api/metrics
```

---

## 🌐 Configuration Nginx (Déjà Fait par le Script)

Le script `deploy.sh` configure automatiquement Nginx. Si vous devez le faire manuellement :

```bash
# Le fichier de configuration est créé ici :
/etc/nginx/sites-available/universal-api

# Tester la configuration
nginx -t

# Recharger Nginx
systemctl reload nginx
```

---

## 🔒 Configuration SSL/HTTPS (Optionnel)

Si vous avez un domaine :

```bash
# Installer Certbot
apt install -y certbot python3-certbot-nginx

# Obtenir un certificat SSL
certbot --nginx -d votre-domaine.com

# Le certificat sera renouvelé automatiquement
```

---

## 📊 Monitoring (Optionnel)

### Prometheus

```bash
# Télécharger Prometheus
cd /opt
wget https://github.com/prometheus/prometheus/releases/download/v2.45.0/prometheus-2.45.0.linux-amd64.tar.gz
tar xvfz prometheus-*.tar.gz
cd prometheus-*

# Configurer
cat > prometheus.yml << EOF
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'universal-api'
    static_configs:
      - targets: ['localhost:8000']
    metrics_path: '/api/metrics/prometheus'
EOF

# Démarrer
./prometheus --config.file=prometheus.yml
```

---

## 🔧 Commandes Utiles

### Service

```bash
# Status
systemctl status universal-api

# Démarrer
systemctl start universal-api

# Arrêter
systemctl stop universal-api

# Redémarrer
systemctl restart universal-api

# Logs en temps réel
journalctl -u universal-api -f

# Logs des 100 dernières lignes
journalctl -u universal-api -n 100
```

### Mise à Jour

```bash
# Aller dans le répertoire
cd /opt/universal-api

# Mettre à jour le code
git pull origin main

# Activer l'environnement virtuel
cd backend
source venv/bin/activate

# Mettre à jour les dépendances (si nécessaire)
pip install -r requirements.txt

# Redémarrer le service
systemctl restart universal-api
```

### Backup

```bash
# Backup manuel
cd /opt/universal-api/backend
sudo bash scripts/backup.sh

# Les backups sont stockés dans
/opt/backups/universal-api/
```

---

## 🆘 Dépannage

### Le service ne démarre pas

```bash
# Vérifier les logs
journalctl -u universal-api -n 50

# Vérifier .env
cat backend/.env

# Vérifier les permissions
ls -la backend/
```

### Port 8000 non accessible

```bash
# Vérifier le firewall
ufw status
ufw allow 8000

# Vérifier que le service écoute
netstat -tlnp | grep 8000
```

### Nginx ne fonctionne pas

```bash
# Tester la configuration
nginx -t

# Vérifier les logs
tail -f /var/log/nginx/error.log

# Redémarrer
systemctl restart nginx
```

---

## 📋 Checklist de Déploiement

### Avant Déploiement
- [ ] Serveur VPS créé
- [ ] Accès SSH configuré
- [ ] Clés API préparées

### Déploiement
- [ ] Serveur mis à jour
- [ ] Dépendances installées
- [ ] Projet cloné
- [ ] .env configuré
- [ ] Script deploy.sh exécuté
- [ ] Service démarré

### Post-Déploiement
- [ ] Vérification effectuée
- [ ] Health checks OK
- [ ] Endpoints testés
- [ ] Nginx configuré
- [ ] SSL configuré (si domaine)

---

## 🎯 Prochaines Étapes

1. ✅ Déploiement terminé (FAIT)
2. ⏳ Configurer le monitoring (Prometheus)
3. ⏳ Configurer les backups automatiques
4. ⏳ Tests de charge
5. ⏳ Optimisations

---

## 📚 Documentation

- **ETAPES_SUITE.md** : Guide étape par étape
- **MIGRATION_COMPLETE.md** : Guide complet
- **DEPLOYMENT_GUIDE.md** : Guide détaillé
- **QUICK_START_DEPLOYMENT.md** : Déploiement rapide

---

**Bon déploiement ! 🚀**

*Dernière mise à jour : Décembre 2024 - v2.3.0*






