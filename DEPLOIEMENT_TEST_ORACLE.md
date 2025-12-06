# 🆓 Déploiement Test sur Oracle Cloud (Gratuit)

**Guide complet pour tester le déploiement gratuitement**

---

## 🎯 Pourquoi Oracle Cloud Free Tier ?

- ✅ **Gratuit à vie** (pas juste un essai)
- ✅ 1GB RAM (suffisant pour tester)
- ✅ Ubuntu 22.04 disponible
- ✅ Parfait pour valider avant production

---

## 📋 Étape 1 : Créer le Compte (15 min)

### 1.1 Inscription

1. Aller sur https://www.oracle.com/cloud/free/
2. Cliquer sur "Start for Free"
3. Remplir le formulaire :
   - Nom, Email, Téléphone
   - Pays
   - Créer un mot de passe
4. Vérifier l'email
5. Ajouter une carte de crédit (ne sera pas débitée pour le plan gratuit)

### 1.2 Vérifier le Compte

- Attendre la validation (peut prendre quelques minutes)
- Se connecter au dashboard Oracle Cloud

---

## 🖥️ Étape 2 : Créer l'Instance (10 min)

### 2.1 Créer l'Instance

1. Dans le dashboard Oracle Cloud :
   - Menu hamburger (☰) > Compute > Instances
   - Cliquer "Create Instance"

2. Configuration :
   - **Name** : `universal-api-test`
   - **Image** : Ubuntu 22.04
   - **Shape** : VM.Standard.E2.1.Micro (Always Free Eligible)
   - **Networking** : Créer un VCN si nécessaire
   - **SSH Keys** : Générer ou uploader une clé SSH

3. Cliquer "Create"

### 2.2 Noter les Informations

- **IP Publique** : Noter l'adresse IP publique
- **Utilisateur** : `ubuntu` (pour Ubuntu)

---

## 🔥 Étape 3 : Configurer le Firewall (5 min)

### 3.1 Ouvrir le Port 8000

1. Networking > Virtual Cloud Networks
2. Sélectionner votre VCN
3. Security Lists > Default Security List
4. Ingress Rules > Add Ingress Rules
5. Ajouter :
   - **Source Type** : CIDR
   - **Source CIDR** : `0.0.0.0/0`
   - **IP Protocol** : TCP
   - **Destination Port Range** : `8000`
   - **Description** : API Backend
6. Save

---

## 🔐 Étape 4 : Se Connecter (2 min)

### 4.1 Récupérer la Clé SSH

1. Dans Oracle Cloud, aller à Compute > Instances
2. Cliquer sur votre instance
3. Dans "Instance Access", copier la commande SSH

### 4.2 Se Connecter

```bash
# Depuis votre machine locale
ssh -i ~/.ssh/your-key ubuntu@VOTRE_IP_PUBLIQUE
```

**Note** : Remplacez `VOTRE_IP_PUBLIQUE` par l'IP de votre instance.

---

## 🚀 Étape 5 : Déployer (20 min)

### 5.1 Préparer le Serveur

```bash
# Mettre à jour le système
sudo apt update && sudo apt upgrade -y

# Installer les dépendances
sudo apt install -y python3.9 python3-pip python3-venv git nginx curl wget
```

### 5.2 Cloner le Projet

```bash
# Créer le répertoire
sudo mkdir -p /opt
cd /opt

# Cloner depuis GitHub
sudo git clone https://github.com/8888vtc-ui/universal-multi-api-backend.git universal-api
cd universal-api/backend
```

### 5.3 Déployer

```bash
# Rendre les scripts exécutables
sudo chmod +x scripts/*.sh

# Exécuter le script de déploiement
sudo bash scripts/deploy.sh production
```

**Le script va automatiquement :**
- ✅ Installer toutes les dépendances
- ✅ Configurer Python
- ✅ Générer JWT_SECRET_KEY
- ✅ Créer le service systemd
- ✅ Configurer Nginx
- ✅ Démarrer le service

**Durée** : ~15-20 minutes

---

## ✅ Étape 6 : Vérifier (10 min)

### 6.1 Vérification Automatique

```bash
# Exécuter le script de vérification
sudo bash scripts/verify_deployment.sh
```

### 6.2 Tests Manuels

```bash
# Depuis le serveur
curl http://localhost:8000/api/health
curl http://localhost:8000/api/info
curl http://localhost:8000/api/metrics

# Depuis votre machine locale
curl http://VOTRE_IP_PUBLIQUE:8000/api/health
curl http://VOTRE_IP_PUBLIQUE:8000/api/docs
```

### 6.3 Vérifier les Logs

```bash
# Logs du service
sudo journalctl -u universal-api -f

# Status
sudo systemctl status universal-api
```

---

## 🧪 Étape 7 : Tests Complets (15 min)

### 7.1 Tester les Endpoints

```bash
# Health
curl http://VOTRE_IP_PUBLIQUE:8000/api/health

# Deep Health
curl http://VOTRE_IP_PUBLIQUE:8000/api/health/deep

# Metrics
curl http://VOTRE_IP_PUBLIQUE:8000/api/metrics

# Chat (si API configurée)
curl -X POST http://VOTRE_IP_PUBLIQUE:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"test","language":"en"}'
```

### 7.2 Tester depuis le Navigateur

Ouvrir dans votre navigateur :
- **Documentation** : http://VOTRE_IP_PUBLIQUE:8000/docs
- **Health** : http://VOTRE_IP_PUBLIQUE:8000/api/health
- **Metrics** : http://VOTRE_IP_PUBLIQUE:8000/api/metrics

---

## 📊 Checklist de Validation

### Fonctionnalités
- [ ] Service démarré
- [ ] Health checks OK
- [ ] Metrics accessibles
- [ ] Documentation accessible
- [ ] Endpoints fonctionnels

### Performance
- [ ] Temps de réponse < 1s
- [ ] Pas d'erreurs dans les logs
- [ ] Service stable

### Sécurité
- [ ] Security headers présents
- [ ] JWT_SECRET_KEY configuré
- [ ] Firewall configuré

---

## 🎯 Après Validation

Une fois le test validé :

1. ✅ **Noter les résultats** du test
2. ✅ **Identifier les problèmes** (s'il y en a)
3. ✅ **Corriger** si nécessaire
4. ✅ **Déployer en production** sur un VPS payant (Hetzner recommandé)

---

## 🆘 Dépannage

### Le Service Ne Démarre Pas

```bash
# Vérifier les logs
sudo journalctl -u universal-api -n 50

# Vérifier .env
cat /opt/universal-api/backend/.env

# Redémarrer
sudo systemctl restart universal-api
```

### Port Non Accessible

```bash
# Vérifier le firewall Oracle Cloud
# Networking > Security Lists > Ingress Rules

# Vérifier que le service écoute
sudo netstat -tlnp | grep 8000
```

### Problèmes de Mémoire (1GB RAM)

Si vous avez des problèmes de mémoire :

```bash
# Vérifier l'utilisation
free -h

# Optimiser (si nécessaire)
# Réduire les workers dans .env
# API_WORKERS=1
```

---

## 📝 Notes Importantes

1. **Oracle Cloud Free Tier** : Gratuit à vie, mais limité à 1GB RAM
2. **Performance** : Suffisant pour tester, pas pour production
3. **Firewall** : N'oubliez pas d'ouvrir le port 8000
4. **SSH** : Gardez votre clé SSH en sécurité

---

## 🎉 Résultat Attendu

Après ce test, vous devriez avoir :
- ✅ Application déployée et fonctionnelle
- ✅ Tous les endpoints testés
- ✅ Validation complète
- ✅ Confiance pour déployer en production

---

**Bon test ! 🚀**

*Dernière mise à jour : Décembre 2024*


