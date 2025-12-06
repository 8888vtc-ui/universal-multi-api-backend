#!/bin/bash
# Script d'installation automatique pour Hetzner/Ubuntu
# Usage: bash deploy.sh

set -e

echo "🚀 Installation du Backend Multi-API"
echo "===================================="

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Vérifier si on est root
if [ "$EUID" -ne 0 ]; then 
    echo -e "${RED}❌ Veuillez exécuter en tant que root (sudo bash deploy.sh)${NC}"
    exit 1
fi

# Mettre à jour le système
echo -e "${GREEN}[1/8] Mise à jour du système...${NC}"
apt update && apt upgrade -y

# Installer Python 3.12
echo -e "${GREEN}[2/8] Installation de Python 3.12...${NC}"
apt install -y software-properties-common
add-apt-repository -y ppa:deadsnakes/ppa
apt update
apt install -y python3.12 python3.12-venv python3.12-dev python3-pip

# Installer Redis
echo -e "${GREEN}[3/8] Installation de Redis...${NC}"
apt install -y redis-server
systemctl enable redis-server
systemctl start redis-server

# Installer Nginx
echo -e "${GREEN}[4/8] Installation de Nginx...${NC}"
apt install -y nginx

# Installer Certbot (SSL)
echo -e "${GREEN}[5/8] Installation de Certbot...${NC}"
apt install -y certbot python3-certbot-nginx

# Installer Git
echo -e "${GREEN}[6/8] Installation de Git...${NC}"
apt install -y git

# Créer utilisateur pour l'application
echo -e "${GREEN}[7/8] Création de l'utilisateur apiuser...${NC}"
if id "apiuser" &>/dev/null; then
    echo "Utilisateur apiuser existe déjà"
else
    adduser --disabled-password --gecos "" apiuser
fi

# Installer les dépendances système
echo -e "${GREEN}[8/8] Installation des dépendances système...${NC}"
apt install -y build-essential libssl-dev libffi-dev

echo -e "${GREEN}✅ Installation de base terminée !${NC}"
echo ""
echo -e "${YELLOW}📝 Prochaines étapes manuelles :${NC}"
echo "1. Se connecter en tant qu'apiuser: su - apiuser"
echo "2. Cloner/uploader votre code dans /home/apiuser/moteur-israelien/backend"
echo "3. Créer l'environnement virtuel: python3.12 -m venv venv"
echo "4. Activer: source venv/bin/activate"
echo "5. Installer dépendances: pip install -r requirements.txt"
echo "6. Créer .env avec vos clés API"
echo "7. Créer le service systemd (voir GUIDE_HEBERGEMENT.md)"
echo "8. Configurer Nginx (voir GUIDE_HEBERGEMENT.md)"
echo ""
echo -e "${GREEN}🎉 Installation terminée !${NC}"



