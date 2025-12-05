# ✅ Checklist Complète de Migration

**Date** : Décembre 2024  
**Version** : 2.3.0

---

## 📋 Pré-Migration

### Configuration
- [ ] JWT_SECRET_KEY généré et sécurisé (32+ caractères)
- [ ] Toutes les clés API configurées dans .env
- [ ] ENVIRONMENT=production dans .env
- [ ] Variables d'environnement vérifiées
- [ ] .env.example mis à jour

### Tests
- [ ] 77 tests unitaires passent (100%)
- [ ] Tests d'intégration passent
- [ ] Tests manuels validés
- [ ] Validation production OK
- [ ] Serveur testé localement

### Code
- [ ] Code commité et pushé
- [ ] Branche main/master stable
- [ ] Pas de code de debug
- [ ] Logs configurés correctement
- [ ] Documentation à jour

### Infrastructure
- [ ] Serveur VPS/Cloud configuré
- [ ] SSH configuré et sécurisé
- [ ] Firewall configuré
- [ ] Domaine configuré (si applicable)
- [ ] DNS configuré (si applicable)

---

## 🚀 Migration

### Préparation Serveur
- [ ] Système mis à jour (apt update && apt upgrade)
- [ ] Python 3.9+ installé
- [ ] Git installé
- [ ] Nginx installé
- [ ] Certbot installé (pour SSL)

### Déploiement
- [ ] Code cloné/mis à jour
- [ ] Environnement virtuel créé
- [ ] Dépendances installées
- [ ] .env configuré avec toutes les clés
- [ ] Répertoires créés (data, logs)
- [ ] Permissions configurées

### Configuration
- [ ] Service systemd créé
- [ ] Service activé et démarré
- [ ] Nginx configuré
- [ ] SSL/HTTPS configuré (si domaine)
- [ ] Firewall ouvert (ports 80, 443, 22)

### Vérification
- [ ] Service démarré (systemctl status)
- [ ] Health check OK (curl /api/health)
- [ ] Metrics accessibles (/api/metrics)
- [ ] Documentation accessible (/docs)
- [ ] Logs vérifiés (journalctl)

---

## 🔒 Sécurité

### Configuration
- [ ] JWT_SECRET_KEY sécurisé
- [ ] Clés API non exposées
- [ ] .env non commité dans Git
- [ ] Firewall configuré
- [ ] SSH sécurisé (clés, pas de password)

### Headers
- [ ] Security headers présents
- [ ] CORS configuré correctement
- [ ] Rate limiting actif
- [ ] Input sanitization active

---

## 📊 Monitoring

### Prometheus
- [ ] Prometheus installé
- [ ] Configuration prometheus.yml créée
- [ ] Service Prometheus démarré
- [ ] Métriques accessibles

### Grafana (Optionnel)
- [ ] Grafana installé
- [ ] Prometheus ajouté comme source
- [ ] Dashboards créés
- [ ] Alertes configurées

### Logs
- [ ] Logs centralisés
- [ ] Rotation des logs configurée
- [ ] Logs accessibles (journalctl)

---

## 🔄 Post-Migration

### Tests
- [ ] Health check fonctionne
- [ ] Tous les endpoints testés
- [ ] Chat IA fonctionnel
- [ ] Finance API fonctionnelle
- [ ] Universal Search fonctionnel
- [ ] Tests de charge effectués

### Documentation
- [ ] URLs de production documentées
- [ ] Credentials sauvegardés sécurisés
- [ ] Procédure de rollback documentée
- [ ] Contacts d'urgence notés

### Backup
- [ ] Script de backup créé
- [ ] Backup automatique configuré
- [ ] Test de restauration effectué
- [ ] Backup stocké hors site

---

## 🆘 Rollback

### Préparation
- [ ] Version précédente identifiée
- [ ] Backup de la base de données
- [ ] Backup de la configuration
- [ ] Procédure de rollback testée

### En Cas de Problème
- [ ] Arrêter le service (systemctl stop)
- [ ] Restaurer la version précédente
- [ ] Restaurer la configuration
- [ ] Redémarrer le service
- [ ] Vérifier le fonctionnement

---

## 📝 Notes

### Commandes Utiles
```bash
# Status
systemctl status universal-api

# Logs
journalctl -u universal-api -f

# Restart
systemctl restart universal-api

# Health check
curl http://localhost:8000/api/health

# Metrics
curl http://localhost:8000/api/metrics
```

### Contacts
- **Support** : [votre-email]
- **Urgence** : [contact-urgence]

---

**Date de migration** : _______________  
**Responsable** : _______________  
**Status** : ⏳ En attente / ✅ Complété

