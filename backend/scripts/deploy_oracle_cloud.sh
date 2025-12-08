#!/bin/bash
# Script d'installation automatique Universal API Hub pour Oracle Linux 9
# À exécuter sur le serveur Oracle Cloud

set -e

echo "=========================================="
echo "  Installation Universal API Hub"
echo "=========================================="

# 1. Mise à jour système
echo "[1/9] Mise à jour du système..."
sudo dnf update -y
sudo dnf install -y git curl wget gcc gcc-c++ make

# 2. Python 3.11
echo "[2/9] Installation Python 3.11..."
sudo dnf install -y python3.11 python3.11-pip python3.11-devel
sudo alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1

# Vérifier Python
python3 --version

# 3. Node.js 18
echo "[3/9] Installation Node.js 18..."
if [ ! -d "$HOME/.nvm" ]; then
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
    export NVM_DIR="$HOME/.nvm"
    [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
fi

nvm install 18
nvm use 18
nvm alias default 18

# Ajouter nvm au .bashrc pour les prochaines sessions
if ! grep -q "NVM_DIR" ~/.bashrc; then
    echo 'export NVM_DIR="$HOME/.nvm"' >> ~/.bashrc
    echo '[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"' >> ~/.bashrc
fi

# Vérifier Node.js
node --version
npm --version

# 4. Nginx
echo "[4/9] Installation Nginx..."
sudo dnf install -y nginx
sudo systemctl start nginx
sudo systemctl enable nginx

# Vérifier Nginx
sudo systemctl status nginx --no-pager || true

# 5. Cloner le projet
echo "[5/9] Clonage du projet..."
cd ~
if [ -d "universal-multi-api-backend" ]; then
    echo "Projet déjà cloné, mise à jour..."
    cd universal-multi-api-backend
    git pull
    cd ~
else
    git clone https://github.com/8888vtc-ui/universal-multi-api-backend.git
fi

cd universal-multi-api-backend/backend

# 6. Créer environnement virtuel
echo "[6/9] Configuration Python..."
if [ ! -d "venv" ]; then
    python3.11 -m venv venv
fi

source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# 7. Créer fichier .env si n'existe pas
echo "[7/9] Configuration .env..."
if [ ! -f ".env" ]; then
    # Générer JWT_SECRET_KEY
    JWT_SECRET=$(python3 -c "import secrets; print(secrets.token_urlsafe(64))")
    
    cat > .env << EOF
# Environnement
ENVIRONMENT=production
API_HOST=0.0.0.0
API_PORT=8000

# JWT Secret (généré automatiquement)
JWT_SECRET_KEY=${JWT_SECRET}

# CORS
CORS_ORIGINS=http://localhost:3000,http://79.72.29.109,https://79.72.29.109

# Redis (optionnel - désactivé par défaut)
# REDIS_URL=redis://localhost:6379

# APIs (ajouter vos clés)
# GROQ_API_KEY=votre_cle
# MISTRAL_API_KEY=votre_cle
# GEMINI_API_KEY=votre_cle
# COHERE_API_KEY=votre_cle
# AI21_API_KEY=votre_cle
# ANTHROPIC_API_KEY=votre_cle
# PERPLEXITY_API_KEY=votre_cle
# HUGGINGFACE_API_TOKEN=votre_cle
# ... autres clés
EOF
    echo "✅ Fichier .env créé avec JWT_SECRET_KEY généré automatiquement."
    echo "⚠️  N'oubliez pas d'ajouter vos clés API dans .env"
else
    echo "⚠️  Fichier .env existe déjà, pas de modification."
fi

# 8. Firewall
echo "[8/9] Configuration firewall..."
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --permanent --add-service=ssh
sudo firewall-cmd --reload

# 9. Créer service systemd
echo "[9/9] Configuration service systemd..."
sudo tee /etc/systemd/system/universal-api.service > /dev/null << 'EOF'
[Unit]
Description=Universal Multi-API Backend
After=network.target

[Service]
Type=simple
User=opc
WorkingDirectory=/home/opc/universal-multi-api-backend/backend
Environment="PATH=/home/opc/universal-multi-api-backend/backend/venv/bin"
ExecStart=/home/opc/universal-multi-api-backend/backend/venv/bin/python main.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable universal-api

echo ""
echo "=========================================="
echo "  ✅ Installation terminée!"
echo "=========================================="
echo ""
echo "📋 Prochaines étapes:"
echo ""
echo "1. Éditer le fichier .env pour ajouter vos clés API:"
echo "   nano ~/universal-multi-api-backend/backend/.env"
echo ""
echo "2. Démarrer le service:"
echo "   sudo systemctl start universal-api"
echo ""
echo "3. Vérifier le statut:"
echo "   sudo systemctl status universal-api"
echo ""
echo "4. Voir les logs:"
echo "   sudo journalctl -u universal-api -f"
echo ""
echo "5. Configurer Nginx (exécuter configure_nginx_oracle.sh)"
echo ""






