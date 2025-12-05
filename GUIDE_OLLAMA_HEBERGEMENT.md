# 🦙 GUIDE HÉBERGEMENT OLLAMA + LLAMA
## Pourquoi Railway ne fonctionne pas et les meilleures alternatives

---

## ❌ **POURQUOI RAILWAY NE FONCTIONNE PAS**

### **Problèmes avec Railway pour Ollama :**

1. **Pas d'accès root** : Railway est un PaaS (Platform as a Service)
   - ❌ Impossible d'installer Ollama (nécessite accès système)
   - ❌ Pas de contrôle sur l'environnement système

2. **Limites de ressources** :
   - ❌ RAM limitée (généralement < 2GB)
   - ❌ Llama 3.1 nécessite **4-8GB RAM minimum**
   - ❌ Pas de GPU disponible

3. **Pas de persistance** :
   - ❌ Les modèles Llama sont gros (4-8GB)
   - ❌ Pas de stockage persistant pour les modèles

4. **Timeout** :
   - ❌ Ollama peut prendre du temps à répondre
   - ❌ Railway a des timeouts stricts

---

## ✅ **SOLUTION : VPS DÉDIÉ**

**Vous avez BESOIN d'un VPS où vous contrôlez tout !**

---

## 🎯 **MEILLEURES OPTIONS POUR OLLAMA + LLAMA**

### **📊 EXIGENCES MINIMALES**

Pour faire tourner **Llama 3.1** avec Ollama :

- **RAM** : **8GB minimum** (16GB recommandé)
- **CPU** : **4 vCPU minimum** (8 vCPU recommandé)
- **Stockage** : **100GB minimum** (pour modèles + système)
- **OS** : Ubuntu 22.04 LTS (recommandé)

---

### **🏆 TOP 3 RECOMMANDATIONS**

#### **1. Hetzner Cloud CPX21** ⭐ MEILLEUR CHOIX
- **Prix** : **9.50€/mois** (ou 6.50€/mois avec réservation annuelle)
- **Spécifications** :
  - CPU : 3 vCPU AMD EPYC
  - RAM : **8GB** ✅
  - Stockage : 160GB NVMe SSD ✅
  - Réseau : 20TB/mois
- **Avantages** :
  - ✅ Parfait pour Llama 3.1 (8GB RAM)
  - ✅ Excellent rapport qualité/prix
  - ✅ Performance CPU excellente
  - ✅ Stockage rapide (NVMe)
- **Modèles supportés** :
  - Llama 3.1 8B (parfait)
  - Llama 3.1 70B (trop gros, nécessite 16GB+)
- **URL** : https://www.hetzner.com/cloud

---

#### **2. Hetzner Cloud CPX31** (Si besoin de plus de puissance)
- **Prix** : **15.21€/mois**
- **Spécifications** :
  - CPU : 4 vCPU AMD EPYC Genoa
  - RAM : **8GB**
  - Stockage : 160GB NVMe SSD
- **Quand choisir** : Si vous voulez plus de CPU pour traitement parallèle

---

#### **3. Hetzner Cloud CCX23** (Si vous voulez Llama 70B)
- **Prix** : **23.44€/mois**
- **Spécifications** :
  - CPU : 4 vCPU AMD EPYC
  - RAM : **16GB** ✅✅
  - Stockage : 240GB NVMe SSD
- **Quand choisir** : Pour Llama 3.1 70B ou plusieurs modèles en parallèle

---

### **💰 ALTERNATIVES ÉCONOMIQUES**

#### **Contabo VPS L** (Si budget serré)
- **Prix** : **8.99€/mois**
- **Spécifications** :
  - CPU : 6 vCPU
  - RAM : **8GB**
  - Stockage : 200GB SSD
- **Avantages** :
  - ✅ Moins cher
  - ✅ Plus de stockage
- **Inconvénients** :
  - ⚠️ Performance CPU moins bonne que Hetzner
  - ⚠️ Support moins réactif
- **URL** : https://www.contabo.com

---

## 📋 **GUIDE D'INSTALLATION COMPLET**

### **Étape 1 : Créer le serveur Hetzner**

1. Aller sur https://www.hetzner.com/cloud
2. Créer un compte
3. Créer un nouveau projet
4. Ajouter un serveur :
   - **Type** : **CPX21** (9.50€/mois) ou **CPX31** (15.21€/mois)
   - **OS** : Ubuntu 22.04 LTS
   - **Localisation** : Falkenstein (Allemagne) ou Nuremberg
   - **SSH Key** : Ajouter votre clé SSH

### **Étape 2 : Se connecter au serveur**

```bash
ssh root@VOTRE_IP
```

### **Étape 3 : Installer Ollama**

```bash
# Mettre à jour le système
apt update && apt upgrade -y

# Installer les dépendances
apt install -y curl git build-essential

# Installer Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Vérifier l'installation
ollama --version
```

### **Étape 4 : Télécharger Llama 3.1**

```bash
# Télécharger Llama 3.1 8B (recommandé pour 8GB RAM)
ollama pull llama3.1:8b

# OU Llama 3.1 70B (nécessite 16GB+ RAM)
# ollama pull llama3.1:70b

# Vérifier les modèles installés
ollama list
```

### **Étape 5 : Tester Ollama**

```bash
# Test simple
ollama run llama3.1:8b "Bonjour, comment ça va?"

# Démarrer Ollama en service (pour qu'il tourne toujours)
# Voir étape suivante
```

### **Étape 6 : Configurer Ollama comme service systemd**

```bash
# Créer le fichier service
sudo nano /etc/systemd/system/ollama.service
```

**Contenu** :
```ini
[Unit]
Description=Ollama Service
After=network.target

[Service]
ExecStart=/usr/local/bin/ollama serve
User=ollama
Group=ollama
Restart=always
RestartSec=3

[Install]
WantedBy=default.target
```

**Activer le service** :
```bash
# Créer l'utilisateur ollama
sudo useradd -r -s /bin/false -m -d /usr/share/ollama ollama

# Donner les permissions
sudo chown -R ollama:ollama /usr/share/ollama

# Activer et démarrer
sudo systemctl daemon-reload
sudo systemctl enable ollama
sudo systemctl start ollama
sudo systemctl status ollama
```

### **Étape 7 : Configurer le firewall**

```bash
# Autoriser le port Ollama (11434)
sudo ufw allow 11434/tcp

# Autoriser SSH
sudo ufw allow 22/tcp

# Activer le firewall
sudo ufw enable
```

### **Étape 8 : Tester depuis l'extérieur**

```bash
# Depuis votre machine locale
curl http://VOTRE_IP:11434/api/tags

# Devrait retourner la liste des modèles
```

---

## 🔧 **CONFIGURER VOTRE BACKEND POUR OLLAMA**

### **Modifier votre `.env`**

```bash
# Dans votre backend/.env
OLLAMA_BASE_URL=http://VOTRE_IP:11434
# OU si vous utilisez un domaine
# OLLAMA_BASE_URL=http://ollama.votre-domaine.com:11434
```

### **Vérifier que ça fonctionne**

```bash
# Dans votre backend
python -c "
import httpx
response = httpx.get('http://VOTRE_IP:11434/api/tags')
print(response.json())
"
```

---

## 🚀 **OPTIMISATION POUR PERFORMANCE**

### **1. Utiliser plusieurs modèles en parallèle**

```bash
# Télécharger plusieurs modèles
ollama pull llama3.1:8b
ollama pull mistral:7b
ollama pull codellama:7b

# Votre backend peut utiliser celui qui répond le mieux
```

### **2. Optimiser la mémoire**

```bash
# Limiter le nombre de modèles chargés en mémoire
# Ollama charge automatiquement les modèles les plus utilisés

# Voir l'utilisation mémoire
ollama ps
```

### **3. Utiliser un reverse proxy (Nginx)**

Pour sécuriser l'accès à Ollama :

```bash
# Installer Nginx
sudo apt install -y nginx

# Créer la config
sudo nano /etc/nginx/sites-available/ollama
```

**Contenu** :
```nginx
server {
    listen 80;
    server_name votre-domaine.com;

    location / {
        proxy_pass http://localhost:11434;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

---

## 📊 **COMPARAISON DES OPTIONS**

| Provider | Prix | RAM | CPU | Stockage | Note pour Ollama |
|----------|------|-----|-----|----------|------------------|
| **Hetzner CPX21** | 9.50€ | 8GB | 3 vCPU | 160GB | ⭐⭐⭐⭐⭐ Parfait |
| **Hetzner CPX31** | 15.21€ | 8GB | 4 vCPU | 160GB | ⭐⭐⭐⭐⭐ Plus de CPU |
| **Hetzner CCX23** | 23.44€ | 16GB | 4 vCPU | 240GB | ⭐⭐⭐⭐⭐ Pour Llama 70B |
| **Contabo VPS L** | 8.99€ | 8GB | 6 vCPU | 200GB | ⭐⭐⭐⭐ Économique |

---

## 💡 **MA RECOMMANDATION FINALE**

### **Pour Ollama + Llama 3.1 8B**

**Hetzner Cloud CPX21 à 9.50€/mois** ⭐

**Pourquoi** :
- ✅ 8GB RAM = parfait pour Llama 3.1 8B
- ✅ 160GB stockage = suffisant pour plusieurs modèles
- ✅ Performance excellente
- ✅ Prix raisonnable
- ✅ Fiable et stable

### **Si vous voulez Llama 70B**

**Hetzner Cloud CCX23 à 23.44€/mois**

**Pourquoi** :
- ✅ 16GB RAM nécessaire pour Llama 70B
- ✅ Plus de stockage pour gros modèles

---

## 🎯 **PLAN D'ACTION**

1. ✅ Créer un compte Hetzner Cloud
2. ✅ Créer un serveur CPX21 (9.50€/mois)
3. ✅ Installer Ollama (script ci-dessus)
4. ✅ Télécharger Llama 3.1 8B
5. ✅ Configurer votre backend pour utiliser Ollama
6. ✅ Tester depuis vos projets (bot backgammon, etc.)

---

## 🔒 **SÉCURITÉ**

### **Important : Sécuriser Ollama**

Par défaut, Ollama est accessible à tous sur le port 11434. Pour la production :

1. **Utiliser un reverse proxy avec authentification**
2. **Restreindre l'accès par IP** (firewall)
3. **Utiliser HTTPS** (Let's Encrypt)
4. **Ne pas exposer Ollama directement** (utiliser votre backend comme proxy)

---

## 📝 **SCRIPT D'INSTALLATION AUTOMATIQUE**

Je peux créer un script qui fait tout automatiquement :
- Installation Ollama
- Téléchargement Llama
- Configuration service systemd
- Configuration Nginx
- Configuration firewall

**Voulez-vous que je crée ce script ?**

---

## ✅ **RÉSUMÉ**

- ❌ **Railway** : Ne fonctionne PAS pour Ollama
- ✅ **Hetzner CPX21** : Meilleur choix (9.50€/mois)
- ✅ **8GB RAM minimum** pour Llama 3.1 8B
- ✅ **VPS nécessaire** pour installer Ollama
- ✅ **Ollama local** = illimité, gratuit, privé !

**Avec Ollama + Llama local, vous n'avez plus besoin de quotas d'API ! 🎉**


