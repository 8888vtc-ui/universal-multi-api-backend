# 📋 Instructions de Déploiement - À Exécuter sur le Serveur

**Pour déployer rapidement sur votre serveur VPS**

---

## 🚀 Option 1 : Script Automatique (Recommandé)

### Étape 1 : Se Connecter au Serveur

```bash
ssh root@VOTRE_IP_SERVEUR
```

### Étape 2 : Télécharger et Exécuter le Script

```bash
# Télécharger le script
curl -o deploy.sh https://raw.githubusercontent.com/8888vtc-ui/universal-multi-api-backend/main/backend/scripts/deploy_complete.sh

# Ou créer le fichier manuellement
nano deploy.sh
# Copier le contenu de backend/scripts/deploy_complete.sh

# Rendre exécutable
chmod +x deploy.sh

# Exécuter
sudo bash deploy.sh
```

**Le script va automatiquement :**
- ✅ Mettre à jour le système
- ✅ Installer toutes les dépendances
- ✅ Cloner le projet depuis GitHub
- ✅ Configurer Python et l'environnement virtuel
- ✅ Générer JWT_SECRET_KEY automatiquement
- ✅ Créer le service systemd
- ✅ Configurer Nginx
- ✅ Démarrer le service

**Durée** : ~15-20 minutes

---

## 🔧 Option 2 : Déploiement Manuel

### Étape 1 : Préparer le Serveur

```bash
# Mettre à jour
apt update && apt upgrade -y

# Installer dépendances
apt install -y python3.9 python3-pip python3-venv git nginx curl wget
```

### Étape 2 : Cloner le Projet

```bash
cd /opt
git clone https://github.com/8888vtc-ui/universal-multi-api-backend.git universal-api
cd universal-api/backend
```

### Étape 3 : Configurer

```bash
# Créer environnement virtuel
python3 -m venv venv
source venv/bin/activate

# Installer dépendances
pip install --upgrade pip
pip install -r requirements.txt

# Configurer .env
cp .env.example .env
nano .env  # Éditer avec vos clés API
```

### Étape 4 : Utiliser le Script de Déploiement

```bash
chmod +x scripts/*.sh
sudo bash scripts/deploy.sh production
```

---

## ✅ Vérification

### Après le Déploiement

```bash
# Vérifier le service
systemctl status universal-api

# Tester les endpoints
curl http://localhost:8000/api/health
curl http://localhost:8000/api/info
curl http://localhost:8000/api/metrics

# Vérification complète
sudo bash scripts/verify_deployment.sh
```

---

## 🔒 Configuration SSL (Si Vous Avez un Domaine)

```bash
# Installer Certbot
apt install -y certbot python3-certbot-nginx

# Obtenir certificat SSL
certbot --nginx -d votre-domaine.com
```

---

## 📊 Informations Importantes

### URLs
- **Locale** : http://localhost:8000
- **Publique** : http://VOTRE_IP:8000
- **Documentation** : http://VOTRE_IP:8000/docs

### Fichiers Importants
- **Configuration** : `/opt/universal-api/backend/.env`
- **Logs** : `journalctl -u universal-api -f`
- **Service** : `systemctl status universal-api`

### Commandes Utiles
```bash
# Redémarrer
systemctl restart universal-api

# Logs
journalctl -u universal-api -f

# Status
systemctl status universal-api
```

---

## 🆘 Dépannage

### Le Service Ne Démarre Pas

```bash
# Vérifier les logs
journalctl -u universal-api -n 50

# Vérifier .env
cat /opt/universal-api/backend/.env

# Vérifier Python
cd /opt/universal-api/backend
source venv/bin/activate
python --version
```

### Port Non Accessible

```bash
# Vérifier le firewall
ufw status
ufw allow 8000

# Vérifier que le service écoute
netstat -tlnp | grep 8000
```

---

## 📝 Notes

1. **JWT_SECRET_KEY** : Généré automatiquement par le script
2. **Clés API** : Configurez-les dans `.env` si nécessaire
3. **Firewall** : Assurez-vous que le port 8000 est ouvert
4. **Domaine** : Configurez DNS avant SSL

---

**Bon déploiement ! 🚀**






