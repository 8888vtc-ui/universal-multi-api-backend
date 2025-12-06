# 🚀 Guide de Migration Complète

**Date** : Décembre 2024  
**Version** : 2.3.0  
**Status** : ✅ Prêt pour Migration

---

## 📋 Vue d'Ensemble

Ce guide contient tout ce qui est nécessaire pour migrer le projet en production de manière sécurisée et efficace.

---

## 🎯 Étapes de Migration

### ÉTAPE 1 : Préparation (30 min)

#### 1.1 Générer JWT_SECRET_KEY

```bash
cd backend
python scripts/prepare_production.py
```

Ou manuellement :
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

#### 1.2 Configurer les Clés API

Éditer `backend/.env` :
```env
JWT_SECRET_KEY=<token-généré>
ENVIRONMENT=production
GROQ_API_KEY=your-key
MISTRAL_API_KEY=your-key
# ... autres clés
```

#### 1.3 Vérifier la Configuration

```bash
python scripts/check_api_config.py
python scripts/validate_production.py
```

---

### ÉTAPE 2 : Déploiement Automatique (15 min)

#### Option A : Script Automatique (Recommandé)

```bash
# Sur le serveur VPS
sudo bash backend/scripts/deploy.sh production
```

Le script va :
- Mettre à jour le système
- Installer les dépendances
- Cloner/mettre à jour le code
- Configurer Python et l'environnement virtuel
- Créer le service systemd
- Configurer Nginx
- Configurer SSL (si domaine configuré)
- Démarrer le service

#### Option B : Déploiement Manuel

Suivre le guide dans `DEPLOYMENT_GUIDE.md`

---

### ÉTAPE 3 : Vérification (10 min)

```bash
# Vérifier que tout fonctionne
sudo bash backend/scripts/verify_deployment.sh
```

Le script vérifie :
- Service actif
- Health checks
- Metrics
- Security headers
- Endpoints
- Nginx
- SSL
- Logs

---

### ÉTAPE 4 : Configuration Monitoring (Optionnel, 1h)

#### 4.1 Prometheus

```bash
# Installer Prometheus
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

#### 4.2 Grafana (Optionnel)

```bash
# Docker
docker run -d -p 3000:3000 grafana/grafana
```

---

## 📁 Fichiers Créés

### Scripts de Déploiement
- `backend/scripts/deploy.sh` - Déploiement automatique
- `backend/scripts/verify_deployment.sh` - Vérification post-déploiement
- `backend/scripts/backup.sh` - Backup automatique
- `backend/scripts/prepare_production.py` - Préparation production

### Documentation
- `MIGRATION_COMPLETE.md` - Ce guide
- `backend/scripts/checklist_migration.md` - Checklist complète
- `PROCHAINES_ETAPES.md` - Guide des prochaines étapes
- `DEPLOYMENT_GUIDE.md` - Guide de déploiement détaillé

---

## ✅ Checklist Complète

Voir `backend/scripts/checklist_migration.md` pour la checklist détaillée.

### Avant Migration
- [ ] JWT_SECRET_KEY généré
- [ ] Clés API configurées
- [ ] Tests passent
- [ ] Code commité
- [ ] Serveur VPS configuré

### Migration
- [ ] Script de déploiement exécuté
- [ ] Service démarré
- [ ] Nginx configuré
- [ ] SSL configuré (si domaine)

### Post-Migration
- [ ] Vérification effectuée
- [ ] Health checks OK
- [ ] Monitoring configuré
- [ ] Backup configuré

---

## 🔧 Commandes Utiles

### Service
```bash
# Status
systemctl status universal-api

# Logs
journalctl -u universal-api -f

# Restart
systemctl restart universal-api

# Stop
systemctl stop universal-api
```

### Health & Metrics
```bash
# Health check
curl http://localhost:8000/api/health

# Deep health
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

# Restaurer
tar -xzf /opt/backups/universal-api/backup_YYYYMMDD_HHMMSS.tar.gz -C /tmp/restore
```

---

## 🆘 Rollback

En cas de problème :

```bash
# 1. Arrêter le service
sudo systemctl stop universal-api

# 2. Restaurer la version précédente
cd /opt/universal-api
git checkout <previous-commit>

# 3. Redémarrer
sudo systemctl start universal-api

# 4. Vérifier
curl http://localhost:8000/api/health
```

---

## 📊 Monitoring

### Prometheus
- URL : http://votre-serveur:9090
- Métriques : http://localhost:8000/api/metrics/prometheus

### Grafana
- URL : http://votre-serveur:3000
- Default login : admin/admin

### Logs
```bash
# Logs du service
journalctl -u universal-api -f

# Logs Nginx
tail -f /var/log/nginx/universal-api-access.log
tail -f /var/log/nginx/universal-api-error.log
```

---

## 🔒 Sécurité

### Checklist Sécurité
- [ ] JWT_SECRET_KEY sécurisé (32+ caractères)
- [ ] Clés API non exposées
- [ ] .env non commité
- [ ] Firewall configuré
- [ ] SSH sécurisé
- [ ] SSL/HTTPS configuré
- [ ] Security headers présents

---

## 📝 Notes Importantes

1. **JWT_SECRET_KEY** : Ne jamais utiliser la valeur par défaut en production
2. **Clés API** : Configurer seulement celles que vous utilisez
3. **Backup** : Configurer un backup automatique régulier
4. **Monitoring** : Configurer des alertes pour les erreurs critiques
5. **SSL** : Toujours utiliser HTTPS en production

---

## 🎯 Prochaines Actions

1. ✅ Préparer la configuration (FAIT)
2. ⏳ Exécuter le script de déploiement
3. ⏳ Vérifier le déploiement
4. ⏳ Configurer le monitoring
5. ⏳ Configurer les backups automatiques

---

## 🆘 Support

### Documentation
- **Déploiement** : `DEPLOYMENT_GUIDE.md`
- **Checklist** : `backend/scripts/checklist_migration.md`
- **Prochaines étapes** : `PROCHAINES_ETAPES.md`

### Scripts
- **Déploiement** : `backend/scripts/deploy.sh`
- **Vérification** : `backend/scripts/verify_deployment.sh`
- **Backup** : `backend/scripts/backup.sh`
- **Préparation** : `backend/scripts/prepare_production.py`

---

**✅ Tout est prêt pour la migration !**

*Dernière mise à jour : Décembre 2024 - v2.3.0*


