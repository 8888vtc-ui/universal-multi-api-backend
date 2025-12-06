# 🚀 Guide de Déploiement Oracle Cloud

## 📋 Informations Serveur

- **Instance** : `instance-20251205-1016`
- **IP Publique** : `79.72.29.109`
- **IP Privée** : `10.0.0.192`
- **OS** : Oracle Linux 9
- **Utilisateur SSH** : `opc`

---

## 🔌 Étape 1 : Connexion SSH

### Sur Windows (PowerShell)

```powershell
# Se connecter au serveur
ssh -i "$env:USERPROFILE\Downloads\ssh-key-2025-12-05.key" opc@79.72.29.109
```

**Note** : Si vous avez déplacé les clés dans `.ssh\oracle\` :

```powershell
ssh -i "$env:USERPROFILE\.ssh\oracle\ssh-key-2025-12-05.key" opc@79.72.29.109
```

---

## 📥 Étape 2 : Transférer les Scripts

### Depuis votre machine locale (PowerShell)

```powershell
# Depuis le dossier du projet
cd "D:\moteur israelien"

# Transférer les scripts
scp -i "$env:USERPROFILE\Downloads\ssh-key-2025-12-05.key" backend/scripts/deploy_oracle_cloud.sh opc@79.72.29.109:~/
scp -i "$env:USERPROFILE\Downloads\ssh-key-2025-12-05.key" backend/scripts/configure_nginx_oracle.sh opc@79.72.29.109:~/
```

---

## 🚀 Étape 3 : Exécuter l'Installation

### Une fois connecté en SSH :

```bash
# Rendre les scripts exécutables
chmod +x deploy_oracle_cloud.sh
chmod +x configure_nginx_oracle.sh

# Exécuter l'installation (5-10 minutes)
./deploy_oracle_cloud.sh
```

Le script va :
- ✅ Installer Python 3.11
- ✅ Installer Node.js 18
- ✅ Installer Nginx
- ✅ Cloner le projet GitHub
- ✅ Créer l'environnement virtuel Python
- ✅ Installer les dépendances
- ✅ Créer le fichier `.env` avec JWT_SECRET_KEY généré
- ✅ Configurer le firewall
- ✅ Créer le service systemd

---

## ⚙️ Étape 4 : Configurer le .env

```bash
# Éditer le fichier .env
nano ~/universal-multi-api-backend/backend/.env
```

### Ajouter vos clés API :

```env
# APIs (ajouter vos clés)
GROQ_API_KEY=votre_cle_groq
MISTRAL_API_KEY=votre_cle_mistral
GEMINI_API_KEY=votre_cle_gemini
COHERE_API_KEY=votre_cle_cohere
AI21_API_KEY=votre_cle_ai21
ANTHROPIC_API_KEY=votre_cle_anthropic
PERPLEXITY_API_KEY=votre_cle_perplexity
HUGGINGFACE_API_TOKEN=votre_cle_hf
```

**Sauvegarder** : `Ctrl+O`, puis `Enter`, puis `Ctrl+X`

---

## 🌐 Étape 5 : Configurer Nginx

```bash
# Exécuter la configuration Nginx
./configure_nginx_oracle.sh
```

---

## ▶️ Étape 6 : Démarrer le Backend

```bash
# Démarrer le service
sudo systemctl start universal-api

# Vérifier le statut
sudo systemctl status universal-api

# Voir les logs en temps réel
sudo journalctl -u universal-api -f
```

**Pour quitter les logs** : `Ctrl+C`

---

## ✅ Étape 7 : Vérification

### Depuis votre navigateur :

1. **Health Check** : http://79.72.29.109/api/health
2. **Documentation** : http://79.72.29.109/docs
3. **API Root** : http://79.72.29.109/
4. **Metrics** : http://79.72.29.109/api/metrics

### Depuis la ligne de commande :

```bash
# Test depuis le serveur
curl http://localhost:8000/api/health

# Test depuis votre machine (PowerShell)
curl http://79.72.29.109/api/health
```

---

## 🔧 Commandes Utiles

### Gérer le service

```bash
# Démarrer
sudo systemctl start universal-api

# Arrêter
sudo systemctl stop universal-api

# Redémarrer
sudo systemctl restart universal-api

# Statut
sudo systemctl status universal-api

# Logs en temps réel
sudo journalctl -u universal-api -f

# Dernières 50 lignes de logs
sudo journalctl -u universal-api -n 50
```

### Mettre à jour le code

```bash
cd ~/universal-multi-api-backend
git pull
cd backend
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart universal-api
```

### Vérifier les processus

```bash
# Vérifier que le backend tourne
ps aux | grep python

# Vérifier les ports
sudo netstat -tulpn | grep :8000
```

---

## 🐛 Dépannage

### Le service ne démarre pas

```bash
# Voir les erreurs détaillées
sudo journalctl -u universal-api -n 100

# Vérifier le fichier .env
cat ~/universal-multi-api-backend/backend/.env

# Tester manuellement
cd ~/universal-multi-api-backend/backend
source venv/bin/activate
python main.py
```

### Nginx ne fonctionne pas

```bash
# Vérifier la config
sudo nginx -t

# Voir les logs d'erreur
sudo tail -f /var/log/nginx/error.log

# Redémarrer Nginx
sudo systemctl restart nginx

# Vérifier le statut
sudo systemctl status nginx
```

### Port déjà utilisé

```bash
# Vérifier les ports
sudo netstat -tulpn | grep :8000

# Tuer le processus si nécessaire
sudo kill -9 PID_DU_PROCESSUS
```

### Connexion SSH refusée

```bash
# Vérifier le firewall
sudo firewall-cmd --list-all

# Vérifier que SSH est autorisé
sudo firewall-cmd --list-services | grep ssh
```

---

## 📊 Résumé des URLs

| Service | URL |
|---------|-----|
| **Backend API** | http://79.72.29.109/api |
| **Health Check** | http://79.72.29.109/api/health |
| **Documentation** | http://79.72.29.109/docs |
| **Metrics** | http://79.72.29.109/api/metrics |
| **Root** | http://79.72.29.109/ |

---

## 🎯 Checklist de Déploiement

```
□ Connexion SSH réussie
□ Scripts transférés sur le serveur
□ Installation exécutée (deploy_oracle_cloud.sh)
□ Fichier .env configuré avec clés API
□ Nginx configuré (configure_nginx_oracle.sh)
□ Service démarré (sudo systemctl start universal-api)
□ Health check OK (http://79.72.29.109/api/health)
□ Documentation accessible (http://79.72.29.109/docs)
```

---

## 🚀 Prochaines Étapes

1. ✅ Backend déployé et fonctionnel
2. 🔜 Configurer SSL (Let's Encrypt) pour HTTPS
3. 🔜 Déployer le frontend
4. 🔜 Configurer un domaine personnalisé
5. 🔜 Monitoring (Prometheus/Grafana)

---

**Votre backend est maintenant accessible sur http://79.72.29.109 !** 🎉


