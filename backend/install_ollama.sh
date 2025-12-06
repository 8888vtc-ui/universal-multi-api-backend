#!/bin/bash
# Script d'installation automatique d'Ollama + Llama
# Usage: sudo bash install_ollama.sh

set -e

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🦙 Installation d'Ollama + Llama${NC}"
echo "===================================="

# Vérifier si on est root
if [ "$EUID" -ne 0 ]; then 
    echo -e "${RED}❌ Veuillez exécuter en tant que root (sudo bash install_ollama.sh)${NC}"
    exit 1
fi

# Vérifier la RAM disponible
RAM_GB=$(free -g | awk '/^Mem:/{print $2}')
echo -e "${YELLOW}📊 RAM disponible: ${RAM_GB}GB${NC}"

if [ "$RAM_GB" -lt 8 ]; then
    echo -e "${RED}⚠️  Attention: Moins de 8GB RAM détecté. Llama 3.1 8B nécessite au moins 8GB.${NC}"
    read -p "Continuer quand même? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Mettre à jour le système
echo -e "${GREEN}[1/7] Mise à jour du système...${NC}"
apt update && apt upgrade -y

# Installer les dépendances
echo -e "${GREEN}[2/7] Installation des dépendances...${NC}"
apt install -y curl git build-essential

# Installer Ollama
echo -e "${GREEN}[3/7] Installation d'Ollama...${NC}"
curl -fsSL https://ollama.com/install.sh | sh

# Vérifier l'installation
if command -v ollama &> /dev/null; then
    echo -e "${GREEN}✅ Ollama installé avec succès${NC}"
    ollama --version
else
    echo -e "${RED}❌ Erreur lors de l'installation d'Ollama${NC}"
    exit 1
fi

# Créer l'utilisateur ollama
echo -e "${GREEN}[4/7] Création de l'utilisateur ollama...${NC}"
if ! id "ollama" &>/dev/null; then
    useradd -r -s /bin/false -m -d /usr/share/ollama ollama
    echo -e "${GREEN}✅ Utilisateur ollama créé${NC}"
else
    echo -e "${YELLOW}Utilisateur ollama existe déjà${NC}"
fi

# Configurer Ollama comme service systemd
echo -e "${GREEN}[5/7] Configuration du service systemd...${NC}"
cat > /etc/systemd/system/ollama.service << 'EOF'
[Unit]
Description=Ollama Service
After=network.target

[Service]
ExecStart=/usr/local/bin/ollama serve
User=ollama
Group=ollama
Restart=always
RestartSec=3
Environment="OLLAMA_HOST=0.0.0.0:11434"

[Install]
WantedBy=default.target
EOF

# Donner les permissions
chown -R ollama:ollama /usr/share/ollama 2>/dev/null || true

# Activer et démarrer le service
systemctl daemon-reload
systemctl enable ollama
systemctl start ollama

# Attendre que Ollama démarre
echo -e "${YELLOW}Attente du démarrage d'Ollama...${NC}"
sleep 5

# Vérifier que le service fonctionne
if systemctl is-active --quiet ollama; then
    echo -e "${GREEN}✅ Service Ollama démarré${NC}"
else
    echo -e "${RED}❌ Erreur: Le service Ollama ne démarre pas${NC}"
    systemctl status ollama
    exit 1
fi

# Configurer le firewall
echo -e "${GREEN}[6/7] Configuration du firewall...${NC}"
if command -v ufw &> /dev/null; then
    ufw allow 11434/tcp comment "Ollama"
    echo -e "${GREEN}✅ Port 11434 ouvert dans le firewall${NC}"
else
    echo -e "${YELLOW}UFW non installé, installation...${NC}"
    apt install -y ufw
    ufw allow 11434/tcp comment "Ollama"
    ufw allow 22/tcp comment "SSH"
    echo -e "${YELLOW}⚠️  N'oubliez pas d'activer le firewall: sudo ufw enable${NC}"
fi

# Télécharger Llama
echo -e "${GREEN}[7/7] Téléchargement de Llama 3.1 8B...${NC}"
echo -e "${YELLOW}📥 Cela peut prendre plusieurs minutes (modèle ~4.7GB)...${NC}"

# Télécharger en arrière-plan et afficher la progression
ollama pull llama3.1:8b &
OLLAMA_PID=$!

# Afficher un spinner pendant le téléchargement
spinner() {
    local pid=$1
    local spin='-\|/'
    local i=0
    while kill -0 $pid 2>/dev/null; do
        i=$(( (i+1) %4 ))
        printf "\r${YELLOW}Téléchargement en cours... ${spin:$i:1}${NC}"
        sleep 0.1
    done
    printf "\r"
}

spinner $OLLAMA_PID
wait $OLLAMA_PID

# Vérifier que le modèle est installé
if ollama list | grep -q "llama3.1:8b"; then
    echo -e "${GREEN}✅ Llama 3.1 8B installé avec succès${NC}"
else
    echo -e "${RED}❌ Erreur lors du téléchargement de Llama${NC}"
    exit 1
fi

# Afficher les modèles installés
echo ""
echo -e "${GREEN}📦 Modèles installés:${NC}"
ollama list

# Test rapide
echo ""
echo -e "${GREEN}🧪 Test rapide d'Ollama...${NC}"
echo -e "${YELLOW}Test: 'Bonjour, comment ça va?'${NC}"
ollama run llama3.1:8b "Bonjour, comment ça va?" --verbose 2>&1 | head -5

# Afficher les informations de connexion
echo ""
echo -e "${GREEN}✅ Installation terminée avec succès !${NC}"
echo ""
echo -e "${BLUE}📋 Informations de connexion:${NC}"
echo -e "  URL locale: http://localhost:11434"
echo -e "  URL externe: http://$(hostname -I | awk '{print $1}'):11434"
echo ""
echo -e "${BLUE}🔧 Commandes utiles:${NC}"
echo -e "  Status: sudo systemctl status ollama"
echo -e "  Logs: sudo journalctl -u ollama -f"
echo -e "  Redémarrer: sudo systemctl restart ollama"
echo -e "  Tester: ollama run llama3.1:8b 'Votre question'"
echo ""
echo -e "${BLUE}🔗 Pour votre backend, ajoutez dans .env:${NC}"
echo -e "  OLLAMA_BASE_URL=http://$(hostname -I | awk '{print $1}'):11434"
echo ""
echo -e "${YELLOW}⚠️  Sécurité: N'oubliez pas de sécuriser l'accès à Ollama en production !${NC}"



