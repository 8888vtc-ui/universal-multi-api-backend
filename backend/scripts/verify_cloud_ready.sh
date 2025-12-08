#!/bin/bash
# Script de Vérification Préalable - Cloud Prêt pour Installation
# Vérifie que le serveur peut supporter Ollama + Backend

set -e

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

errors=0
warnings=0

print_section "🔍 VÉRIFICATION PRÉALABLE - Cloud Prêt pour Installation"

# 1. Vérifier la RAM
print_section "💾 Vérification RAM"
RAM_GB=$(free -g | awk '/^Mem:/{print $2}')
RAM_AVAILABLE=$(free -g | awk '/^Mem:/{print $7}')

print_info "RAM totale: ${RAM_GB}GB"
print_info "RAM disponible: ${RAM_AVAILABLE}GB"

if [ "$RAM_GB" -ge 12 ]; then
    print_success "RAM suffisante (12GB+) - Peut faire tourner tous les modèles"
elif [ "$RAM_GB" -ge 8 ]; then
    print_success "RAM suffisante (8GB+) - Peut faire tourner modèles moyens"
elif [ "$RAM_GB" -ge 4 ]; then
    print_warning "RAM limitée (4GB) - Seulement modèles légers (1B)"
    ((warnings++))
elif [ "$RAM_GB" -ge 2 ]; then
    print_warning "RAM très limitée (2GB) - Seulement modèle 1B, performance réduite"
    ((warnings++))
else
    print_error "RAM insuffisante (<2GB) - Ne peut pas faire tourner Ollama correctement"
    ((errors++))
fi

# 2. Vérifier les CPU
print_section "⚙️  Vérification CPU"
CPU_COUNT=$(nproc)
CPU_MODEL=$(lscpu | grep "Model name" | cut -d: -f2 | xargs)

print_info "Nombre de cœurs: ${CPU_COUNT}"
print_info "Modèle: ${CPU_MODEL}"

if [ "$CPU_COUNT" -ge 4 ]; then
    print_success "CPU suffisant (4+ cœurs)"
elif [ "$CPU_COUNT" -ge 2 ]; then
    print_success "CPU acceptable (2+ cœurs)"
else
    print_warning "CPU limité (1 cœur) - Performance réduite"
    ((warnings++))
fi

# Vérifier si ARM
if echo "$CPU_MODEL" | grep -qi "arm\|aarch"; then
    print_success "Architecture ARM détectée - Parfait pour Ollama"
elif echo "$CPU_MODEL" | grep -qi "x86\|amd64\|intel"; then
    print_info "Architecture x86 détectée - Compatible"
else
    print_warning "Architecture non identifiée"
fi

# 3. Vérifier le stockage
print_section "💿 Vérification Stockage"
DISK_AVAILABLE=$(df -h / | awk 'NR==2 {print $4}')
DISK_AVAILABLE_GB=$(df -BG / | awk 'NR==2 {print $4}' | sed 's/G//')

print_info "Stockage disponible: ${DISK_AVAILABLE}"

if [ "$DISK_AVAILABLE_GB" -ge 50 ]; then
    print_success "Stockage suffisant (50GB+)"
elif [ "$DISK_AVAILABLE_GB" -ge 20 ]; then
    print_success "Stockage acceptable (20GB+)"
else
    print_warning "Stockage limité (<20GB) - Peut être insuffisant pour modèles IA"
    ((warnings++))
fi

# 4. Vérifier Ubuntu
print_section "🐧 Vérification OS"
if [ -f /etc/os-release ]; then
    OS_NAME=$(grep "^NAME=" /etc/os-release | cut -d= -f2 | tr -d '"')
    OS_VERSION=$(grep "^VERSION_ID=" /etc/os-release | cut -d= -f2 | tr -d '"')
    
    print_info "OS: ${OS_NAME}"
    print_info "Version: ${OS_VERSION}"
    
    if echo "$OS_NAME" | grep -qi "ubuntu"; then
        if echo "$OS_VERSION" | grep -qE "22\.04|20\.04"; then
            print_success "Ubuntu compatible (20.04 ou 22.04)"
        else
            print_warning "Ubuntu version non testée - Peut fonctionner"
            ((warnings++))
        fi
    else
        print_warning "OS non Ubuntu - Peut fonctionner mais non testé"
        ((warnings++))
    fi
else
    print_warning "Impossible de détecter l'OS"
    ((warnings++))
fi

# 5. Vérifier Python
print_section "🐍 Vérification Python"
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | awk '{print $2}')
    PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
    PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)
    
    print_info "Python version: ${PYTHON_VERSION}"
    
    if [ "$PYTHON_MAJOR" -ge 3 ] && [ "$PYTHON_MINOR" -ge 9 ]; then
        print_success "Python 3.9+ détecté - Compatible"
    else
        print_error "Python 3.9+ requis - Version actuelle: ${PYTHON_VERSION}"
        print_info "Installer avec: sudo apt install python3.9"
        ((errors++))
    fi
else
    print_error "Python3 non installé"
    print_info "Installer avec: sudo apt install python3 python3-pip"
    ((errors++))
fi

# 6. Vérifier les ports
print_section "🔌 Vérification Ports"
if command -v netstat &> /dev/null; then
    PORT_8000=$(netstat -tlnp 2>/dev/null | grep :8000 || true)
    PORT_11434=$(netstat -tlnp 2>/dev/null | grep :11434 || true)
    
    if [ -z "$PORT_8000" ]; then
        print_success "Port 8000 disponible (Backend)"
    else
        print_warning "Port 8000 déjà utilisé"
        ((warnings++))
    fi
    
    if [ -z "$PORT_11434" ]; then
        print_success "Port 11434 disponible (Ollama)"
    else
        print_warning "Port 11434 déjà utilisé (Ollama peut-être déjà installé)"
        ((warnings++))
    fi
else
    print_info "netstat non disponible - Impossible de vérifier les ports"
fi

# 7. Test de performance
print_section "⚡ Test de Performance"
print_info "Test de performance Python..."

START_TIME=$(date +%s)
python3 -c "import sys; print('OK')" > /dev/null 2>&1
END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))

if [ "$DURATION" -le 2 ]; then
    print_success "Performance Python OK (${DURATION}s)"
else
    print_warning "Performance Python lente (${DURATION}s)"
    ((warnings++))
fi

# 8. Résumé
print_section "📊 RÉSUMÉ"

if [ $errors -eq 0 ] && [ $warnings -eq 0 ]; then
    print_success "✅ SERVEUR 100% PRÊT POUR INSTALLATION"
    echo ""
    print_info "Toutes les vérifications sont passées"
    print_info "Vous pouvez installer Ollama + Backend en toute confiance"
    echo ""
    print_info "Prochaines étapes:"
    echo "  1. Installer Ollama: curl -fsSL https://ollama.com/install.sh | sh"
    echo "  2. Télécharger modèle: ollama pull deepseek-r1:7b"
    echo "  3. Déployer backend: sudo bash scripts/deploy.sh production"
    exit 0
elif [ $errors -eq 0 ]; then
    print_warning "⚠️  SERVEUR PRÊT AVEC AVERTISSEMENTS"
    echo ""
    print_info "Le serveur peut fonctionner mais avec des limitations:"
    if [ "$RAM_GB" -lt 8 ]; then
        print_warning "- RAM limitée: Utiliser seulement modèles légers (1B)"
    fi
    if [ "$CPU_COUNT" -lt 2 ]; then
        print_warning "- CPU limité: Performance réduite"
    fi
    echo ""
    print_info "Vous pouvez continuer mais avec des modèles plus petits"
    exit 0
else
    print_error "❌ SERVEUR NON PRÊT"
    echo ""
    print_error "Problèmes détectés qui empêchent l'installation:"
    echo ""
    if [ "$RAM_GB" -lt 2 ]; then
        print_error "- RAM insuffisante (<2GB) - Ne peut pas faire tourner Ollama"
    fi
    if ! command -v python3 &> /dev/null; then
        print_error "- Python3 non installé"
    fi
    echo ""
    print_info "Corrigez les problèmes ci-dessus avant de continuer"
    exit 1
fi






