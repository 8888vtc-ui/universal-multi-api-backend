#!/bin/bash
# Script pour créer le service systemd
# Usage: sudo bash setup_service.sh

set -e

# Vérifier si on est root
if [ "$EUID" -ne 0 ]; then 
    echo "❌ Veuillez exécuter en tant que root (sudo bash setup_service.sh)"
    exit 1
fi

# Demander le chemin du projet
read -p "Chemin complet du projet backend (ex: /home/apiuser/moteur-israelien/backend): " PROJECT_PATH

if [ ! -d "$PROJECT_PATH" ]; then
    echo "❌ Le répertoire $PROJECT_PATH n'existe pas"
    exit 1
fi

# Demander le nom d'utilisateur
read -p "Nom d'utilisateur (ex: apiuser): " USERNAME

if ! id "$USERNAME" &>/dev/null; then
    echo "❌ L'utilisateur $USERNAME n'existe pas"
    exit 1
fi

# Créer le fichier service
SERVICE_FILE="/etc/systemd/system/api-backend.service"

cat > "$SERVICE_FILE" << EOF
[Unit]
Description=Universal Multi-API Backend
After=network.target redis.service

[Service]
Type=simple
User=$USERNAME
WorkingDirectory=$PROJECT_PATH
Environment="PATH=$PROJECT_PATH/venv/bin"
ExecStart=$PROJECT_PATH/venv/bin/python $PROJECT_PATH/main.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

echo "✅ Service créé: $SERVICE_FILE"

# Recharger systemd
systemctl daemon-reload

# Activer le service
systemctl enable api-backend

echo "✅ Service activé (démarrage automatique au boot)"
echo ""
echo "📝 Commandes utiles:"
echo "  Démarrage: sudo systemctl start api-backend"
echo "  Arrêt: sudo systemctl stop api-backend"
echo "  Status: sudo systemctl status api-backend"
echo "  Logs: sudo journalctl -u api-backend -f"



