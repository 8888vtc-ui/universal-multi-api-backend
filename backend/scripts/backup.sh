#!/bin/bash
# Script de Backup Automatique
# Sauvegarde la configuration et les données

set -e

BACKEND_DIR="${BACKEND_DIR:-/opt/universal-api/backend}"
BACKUP_DIR="${BACKUP_DIR:-/opt/backups/universal-api}"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_NAME="backup_${DATE}"

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

# Créer le répertoire de backup
mkdir -p "$BACKUP_DIR"

print_section "💾 BACKUP - Universal Multi-API Backend"

# 1. Backup .env (sans les secrets sensibles)
print_info "Sauvegarde de .env..."
if [ -f "$BACKEND_DIR/.env" ]; then
    # Créer une copie masquée
    sed 's/=.*/=***MASKED***/' "$BACKEND_DIR/.env" > "$BACKUP_DIR/.env.masked"
    print_success ".env sauvegardé (masqué)"
else
    print_error ".env non trouvé"
fi

# 2. Backup de la base de données SQLite
print_info "Sauvegarde de la base de données..."
if [ -f "$BACKEND_DIR/data/users.db" ]; then
    cp "$BACKEND_DIR/data/users.db" "$BACKUP_DIR/users.db.$DATE"
    print_success "Base de données sauvegardée"
else
    print_info "Pas de base de données à sauvegarder"
fi

# 3. Backup de la configuration
print_info "Sauvegarde de la configuration..."
mkdir -p "$BACKUP_DIR/$BACKUP_NAME"
cp -r "$BACKEND_DIR"/*.py "$BACKUP_DIR/$BACKUP_NAME/" 2>/dev/null || true
cp -r "$BACKEND_DIR/routers" "$BACKUP_DIR/$BACKUP_NAME/" 2>/dev/null || true
cp -r "$BACKEND_DIR/services" "$BACKUP_DIR/$BACKUP_NAME/" 2>/dev/null || true
cp -r "$BACKEND_DIR/models" "$BACKUP_DIR/$BACKUP_NAME/" 2>/dev/null || true
print_success "Configuration sauvegardée"

# 4. Backup des logs récents
print_info "Sauvegarde des logs récents..."
if [ -d "$BACKEND_DIR/logs" ]; then
    tar -czf "$BACKUP_DIR/logs_$DATE.tar.gz" -C "$BACKEND_DIR" logs/ 2>/dev/null || true
    print_success "Logs sauvegardés"
fi

# 5. Créer une archive complète
print_info "Création de l'archive complète..."
cd "$BACKUP_DIR"
tar -czf "$BACKUP_NAME.tar.gz" "$BACKUP_NAME" .env.masked users.db.$DATE logs_$DATE.tar.gz 2>/dev/null || true
print_success "Archive créée: $BACKUP_NAME.tar.gz"

# 6. Nettoyer les anciens backups (garder les 7 derniers)
print_info "Nettoyage des anciens backups..."
ls -t "$BACKUP_DIR"/*.tar.gz 2>/dev/null | tail -n +8 | xargs rm -f 2>/dev/null || true
print_success "Anciens backups nettoyés"

# 7. Résumé
print_section "📊 RÉSUMÉ DU BACKUP"
print_success "Backup terminé !"
echo ""
print_info "Archive: $BACKUP_DIR/$BACKUP_NAME.tar.gz"
print_info "Taille: $(du -h "$BACKUP_DIR/$BACKUP_NAME.tar.gz" | cut -f1)"
echo ""
print_info "Pour restaurer:"
echo "  tar -xzf $BACKUP_DIR/$BACKUP_NAME.tar.gz -C /tmp/restore"

<<<<<<< Updated upstream
=======





>>>>>>> Stashed changes
