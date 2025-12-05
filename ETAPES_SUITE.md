# 🎯 Étapes pour la Suite - Guide Pratique

**Date** : Décembre 2024  
**Version** : 2.3.0  
**Status** : ✅ Prêt pour Déploiement

---

## 📋 Vue d'Ensemble

Ce guide vous accompagne étape par étape pour déployer votre projet en production.

---

## 🚀 ÉTAPE 1 : Préparer le Serveur VPS (30 min)

### 1.1 Choisir un VPS

**Recommandation** : Hetzner CPX31 (15€/mois)
- 2 vCPU
- 4 GB RAM
- 80 GB SSD
- Parfait pour ce projet

**Alternatives** :
- DigitalOcean Droplet (12$/mois)
- OVH VPS (8€/mois)
- Scaleway (10€/mois)

### 1.2 Créer le Serveur

1. Créer un compte sur Hetzner (ou autre)
2. Créer un nouveau serveur :
   - **OS** : Ubuntu 22.04 LTS
   - **Type** : CPX31 (2 vCPU, 4GB RAM)
   - **Localisation** : Choisir la plus proche
3. Noter l'adresse IP du serveur

### 1.3 Configurer SSH

```bash
# Sur votre machine locale
ssh-keygen -t rsa -b 4096

# Copier la clé publique sur le serveur
ssh-copy-id root@VOTRE_IP_SERVEUR

# Tester la connexion
ssh root@VOTRE_IP_SERVEUR
```

---

## 🔧 ÉTAPE 2 : Préparer le Code (10 min)

### 2.1 Vérifier la Configuration Locale

```bash
cd backend
python scripts/prepare_production_auto.py
```

Vérifier que :
- JWT_SECRET_KEY est généré
- .env est configuré
- Clés API nécessaires sont présentes

### 2.2 Commit et Push (si Git)

```bash
# Commit les changements
git add .
git commit -m "Préparation production"
git push origin main
```

---

## 📦 ÉTAPE 3 : Déployer sur le Serveur (15 min)

### 3.1 Se Connecter au Serveur

```bash
ssh root@VOTRE_IP_SERVEUR
```

### 3.2 Cloner le Projet

```bash
# Installer Git si nécessaire
apt update && apt install -y git

# Cloner le projet
cd /opt
git clone VOTRE_REPO_URL universal-api
cd universal-api
```

**Note** : Si vous n'utilisez pas Git, vous pouvez :
- Transférer les fichiers avec `scp`
- Utiliser `rsync`
- Créer une archive et la transférer

### 3.3 Exécuter le Script de Déploiement

```bash
cd backend
chmod +x scripts/*.sh

# Déployer
sudo bash scripts/deploy.sh production
```

Le script va :
- ✅ Installer toutes les dépendances
- ✅ Configurer Python et l'environnement virtuel
- ✅ Créer le service systemd
- ✅ Configurer Nginx
- ✅ Démarrer le service

**Durée** : ~10-15 minutes

---

## ✅ ÉTAPE 4 : Vérifier le Déploiement (10 min)

### 4.1 Vérification Automatique

```bash
sudo bash backend/scripts/verify_deployment.sh
```

Le script vérifie :
- Service actif
- Health checks
- Metrics
- Security headers
- Endpoints

### 4.2 Vérification Manuelle

```bash
# Vérifier le service
systemctl status universal-api

# Vérifier les logs
journalctl -u universal-api -f

# Tester les endpoints
curl http://localhost:8000/api/health
curl http://localhost:8000/api/metrics
```

### 4.3 Tester depuis l'Extérieur

```bash
# Depuis votre machine locale
curl http://VOTRE_IP_SERVEUR/api/health
```

---

## 🌐 ÉTAPE 5 : Configurer le Domaine (Optionnel, 30 min)

### 5.1 Configurer DNS

1. Aller sur votre registrar (GoDaddy, Namecheap, etc.)
2. Ajouter un enregistrement A :
   - **Type** : A
   - **Nom** : @ (ou www)
   - **Valeur** : VOTRE_IP_SERVEUR
   - **TTL** : 3600

### 5.2 Configurer SSL/HTTPS

```bash
# Sur le serveur
# Le script deploy.sh configure déjà Nginx
# Il suffit d'exécuter certbot

certbot --nginx -d votre-domaine.com

# Ou si le domaine n'est pas encore configuré dans deploy.sh
# Éditer le script et changer DOMAIN="votre-domaine.com"
```

### 5.3 Vérifier HTTPS

```bash
curl https://votre-domaine.com/api/health
```

---

## 📊 ÉTAPE 6 : Configurer le Monitoring (Optionnel, 1h)

### 6.1 Installer Prometheus

```bash
# Sur le serveur
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

# Démarrer (ou créer un service systemd)
./prometheus --config.file=prometheus.yml
```

### 6.2 Installer Grafana (Optionnel)

```bash
# Avec Docker
docker run -d -p 3000:3000 grafana/grafana

# Accéder à http://VOTRE_IP:3000
# Login: admin/admin
# Ajouter Prometheus comme source de données
```

---

## 💾 ÉTAPE 7 : Configurer les Backups (30 min)

### 7.1 Backup Manuel

```bash
# Sur le serveur
sudo bash backend/scripts/backup.sh
```

### 7.2 Backup Automatique (Cron)

```bash
# Éditer crontab
crontab -e

# Ajouter (backup quotidien à 2h du matin)
0 2 * * * /opt/universal-api/backend/scripts/backup.sh >> /var/log/backup.log 2>&1
```

---

## 🔄 ÉTAPE 8 : Mises à Jour Futures

### 8.1 Mettre à Jour le Code

```bash
# Sur le serveur
cd /opt/universal-api
git pull origin main

# Redémarrer le service
systemctl restart universal-api
```

### 8.2 Vérifier après Mise à Jour

```bash
sudo bash backend/scripts/verify_deployment.sh
```

---

## 📋 Checklist Complète

### Avant Déploiement
- [ ] Serveur VPS créé
- [ ] SSH configuré
- [ ] Code préparé localement
- [ ] JWT_SECRET_KEY généré
- [ ] Clés API configurées

### Déploiement
- [ ] Code cloné sur le serveur
- [ ] Script deploy.sh exécuté
- [ ] Service démarré
- [ ] Nginx configuré
- [ ] Vérification effectuée

### Post-Déploiement
- [ ] Domaine configuré (si applicable)
- [ ] SSL/HTTPS configuré (si domaine)
- [ ] Monitoring configuré (optionnel)
- [ ] Backups configurés
- [ ] Tests effectués

---

## 🆘 Problèmes Courants

### Le service ne démarre pas

```bash
# Vérifier les logs
journalctl -u universal-api -f

# Vérifier .env
cat backend/.env

# Vérifier les permissions
ls -la backend/
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

### Port 8000 non accessible

```bash
# Vérifier le firewall
ufw status
ufw allow 8000

# Vérifier que le service écoute
netstat -tlnp | grep 8000
```

---

## 📞 Commandes de Référence

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

# Logs
journalctl -u universal-api -f
```

### Health & Metrics
```bash
# Health
curl http://localhost:8000/api/health

# Deep Health
curl http://localhost:8000/api/health/deep

# Metrics
curl http://localhost:8000/api/metrics

# Prometheus
curl http://localhost:8000/api/metrics/prometheus
```

### Backup
```bash
# Backup manuel
sudo bash backend/scripts/backup.sh

# Liste des backups
ls -lh /opt/backups/universal-api/
```

---

## 🎯 Timeline Recommandée

### Jour 1 (2-3h)
- ✅ Étape 1 : Préparer le serveur VPS
- ✅ Étape 2 : Préparer le code
- ✅ Étape 3 : Déployer sur le serveur
- ✅ Étape 4 : Vérifier le déploiement

### Jour 2 (1-2h)
- ⏳ Étape 5 : Configurer le domaine (si applicable)
- ⏳ Étape 6 : Configurer le monitoring (optionnel)
- ⏳ Étape 7 : Configurer les backups

### Semaine 1
- ⏳ Tests utilisateurs
- ⏳ Optimisations
- ⏳ Documentation utilisateur

---

## ✅ Prochaine Action Immédiate

**Commencez par l'Étape 1** : Préparer le serveur VPS

1. Créer un compte Hetzner (ou autre)
2. Créer un serveur Ubuntu 22.04
3. Noter l'adresse IP
4. Configurer SSH

Ensuite, passez à l'Étape 2 et suivez le guide.

---

## 📚 Documentation Complémentaire

- **MIGRATION_COMPLETE.md** : Guide complet de migration
- **DEPLOYMENT_GUIDE.md** : Guide de déploiement détaillé
- **PRET_POUR_DEPLOIEMENT.md** : Checklist finale
- **PROCHAINES_ETAPES.md** : Roadmap générale

---

**🎉 Bon déploiement !**

*Dernière mise à jour : Décembre 2024 - v2.3.0*

