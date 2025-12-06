#!/bin/bash
# Script de Déploiement Complet - À Exécuter sur le Serveur VPS
# Usage: bash deploy_complete.sh

set -e  # Arrêter en cas d'erreur

# Configuration
REPO_URL="https://github.com/8888vtc-ui/universal-multi-api-backend.git"
APP_DIR="/opt/universal-api"
BACKEND_DIR="$APP_DIR/backend"
SERVICE_NAME="universal-api"
ENVIRONMENT="production"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_section() {
    echo ""
    echo "============================================================"
    echo "$1"
    echo "============================================================"
    echo ""
}

# Vérifier que le script est exécuté en root
if [ "$EUID" -ne 0 ]; then 
    print_error "Ce script doit être exécuté en root (sudo)"
    exit 1
fi

print_section "🚀 DÉPLOIEMENT COMPLET - Universal Multi-API Backend"

# 1. Mise à jour du système
print_section "📦 Mise à jour du système"
apt update && apt upgrade -y
print_success "Système mis à jour"

# 2. Installation des dépendances
print_section "📦 Installation des dépendances"
apt install -y python3.9 python3-pip python3-venv git nginx certbot python3-certbot-nginx curl wget
print_success "Dépendances installées"

# 3. Créer l'utilisateur si nécessaire
print_section "👤 Configuration utilisateur"
if ! id -u appuser >/dev/null 2>&1; then
    useradd -m -s /bin/bash appuser
    print_success "Utilisateur appuser créé"
else
    print_info "Utilisateur appuser existe déjà"
fi

# 4. Cloner/Mettre à jour le repository
print_section "📥 Clonage/Mise à jour du code"
if [ -d "$APP_DIR" ]; then
    print_info "Répertoire existe, mise à jour..."
    cd "$APP_DIR"
    git pull origin main || git pull origin master
    print_success "Code mis à jour"
else
    print_info "Clonage du repository..."
    mkdir -p "$APP_DIR"
    git clone "$REPO_URL" "$APP_DIR"
    print_success "Code cloné"
fi

# 5. Créer l'environnement virtuel
print_section "🐍 Configuration Python"
cd "$BACKEND_DIR"
if [ ! -d "venv" ]; then
    python3 -m venv venv
    print_success "Environnement virtuel créé"
else
    print_info "Environnement virtuel existe déjà"
fi

source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
print_success "Dépendances Python installées"

# 6. Configuration .env
print_section "⚙️  Configuration .env"
if [ ! -f "$BACKEND_DIR/.env" ]; then
    if [ -f "$BACKEND_DIR/.env.example" ]; then
        cp "$BACKEND_DIR/.env.example" "$BACKEND_DIR/.env"
        print_warning ".env créé depuis .env.example"
        
        # Générer JWT_SECRET_KEY automatiquement
        NEW_JWT=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")
        sed -i "s/JWT_SECRET_KEY=.*/JWT_SECRET_KEY=$NEW_JWT/" "$BACKEND_DIR/.env" || echo "JWT_SECRET_KEY=$NEW_JWT" >> "$BACKEND_DIR/.env"
        print_success "JWT_SECRET_KEY généré automatiquement"
        
        # Configurer ENVIRONMENT
        sed -i "s/ENVIRONMENT=.*/ENVIRONMENT=$ENVIRONMENT/" "$BACKEND_DIR/.env" || echo "ENVIRONMENT=$ENVIRONMENT" >> "$BACKEND_DIR/.env"
        print_success "ENVIRONMENT configuré: $ENVIRONMENT"
        
        print_warning "⚠️  IMPORTANT: Éditez .env avec vos clés API si nécessaire"
        print_info "Fichier: $BACKEND_DIR/.env"
    else
        print_error ".env.example non trouvé"
        exit 1
    fi
else
    print_info ".env existe déjà"
    # Vérifier JWT_SECRET_KEY
    if ! grep -q "JWT_SECRET_KEY=" "$BACKEND_DIR/.env" || grep -q "JWT_SECRET_KEY=your-secret-key-here" "$BACKEND_DIR/.env"; then
        NEW_JWT=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")
        sed -i "s/JWT_SECRET_KEY=.*/JWT_SECRET_KEY=$NEW_JWT/" "$BACKEND_DIR/.env" || echo "JWT_SECRET_KEY=$NEW_JWT" >> "$BACKEND_DIR/.env"
        print_success "JWT_SECRET_KEY généré automatiquement"
    fi
fi

# 7. Créer les répertoires nécessaires
print_section "📁 Création des répertoires"
mkdir -p "$BACKEND_DIR/data" "$BACKEND_DIR/logs"
chown -R appuser:appuser "$APP_DIR"
print_success "Répertoires créés"

# 8. Créer le service systemd
print_section "🔧 Configuration systemd"
cat > /etc/systemd/system/$SERVICE_NAME.service << EOF
[Unit]
Description=Universal Multi-API Backend
After=network.target

[Service]
Type=simple
User=appuser
Group=appuser
WorkingDirectory=$BACKEND_DIR
Environment="PATH=$BACKEND_DIR/venv/bin"
EnvironmentFile=$BACKEND_DIR/.env
ExecStart=$BACKEND_DIR/venv/bin/python $BACKEND_DIR/main.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable $SERVICE_NAME
print_success "Service systemd configuré"

# 9. Configuration Nginx
print_section "🌐 Configuration Nginx"
cat > /etc/nginx/sites-available/$SERVICE_NAME << EOF
server {
    listen 80;
    server_name _;

    client_max_body_size 50M;
    
    # Logs
    access_log /var/log/nginx/$SERVICE_NAME-access.log;
    error_log /var/log/nginx/$SERVICE_NAME-error.log;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # Health check direct
    location /api/health {
        proxy_pass http://localhost:8000/api/health;
        access_log off;
    }
}
EOF

# Activer le site
if [ ! -L /etc/nginx/sites-enabled/$SERVICE_NAME ]; then
    ln -s /etc/nginx/sites-available/$SERVICE_NAME /etc/nginx/sites-enabled/
fi

# Tester la configuration
nginx -t
systemctl reload nginx
print_success "Nginx configuré"

# 10. Démarrer le service
print_section "🚀 Démarrage du service"
systemctl restart $SERVICE_NAME
sleep 5
systemctl status $SERVICE_NAME --no-pager || print_error "Le service n'a pas démarré correctement"

# 11. Vérification
print_section "✅ Vérification"
sleep 3
if curl -f http://localhost:8000/api/health > /dev/null 2>&1; then
    print_success "Serveur accessible sur http://localhost:8000"
    print_success "Serveur accessible sur http://$(hostname -I | awk '{print $1}'):8000"
else
    print_error "Le serveur ne répond pas"
    print_info "Vérifiez les logs: journalctl -u $SERVICE_NAME -f"
fi

# 12. Résumé
print_section "📊 RÉSUMÉ DU DÉPLOIEMENT"
print_success "Déploiement terminé !"
echo ""
print_info "Service: $SERVICE_NAME"
print_info "Répertoire: $BACKEND_DIR"
print_info "Environnement: $ENVIRONMENT"
print_info "URL locale: http://localhost:8000"
print_info "URL publique: http://$(hostname -I | awk '{print $1}'):8000"
echo ""
print_info "Commandes utiles:"
echo "  - Status: systemctl status $SERVICE_NAME"
echo "  - Logs: journalctl -u $SERVICE_NAME -f"
echo "  - Restart: systemctl restart $SERVICE_NAME"
echo "  - Health: curl http://localhost:8000/api/health"
echo ""

print_success "🎉 Déploiement réussi !"


