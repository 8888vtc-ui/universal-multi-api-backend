#!/bin/bash
# Script de Vérification Post-Déploiement
# Vérifie que tout fonctionne correctement après le déploiement

set -e

BASE_URL="${BASE_URL:-http://localhost:8000}"
SERVICE_NAME="${SERVICE_NAME:-universal-api}"

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

check_service() {
    print_section "🔍 Vérification du Service"
    
    if systemctl is-active --quiet $SERVICE_NAME; then
        print_success "Service $SERVICE_NAME est actif"
    else
        print_error "Service $SERVICE_NAME n'est pas actif"
        return 1
    fi
    
    if systemctl is-enabled --quiet $SERVICE_NAME; then
        print_success "Service $SERVICE_NAME est activé au démarrage"
    else
        print_warning "Service $SERVICE_NAME n'est pas activé au démarrage"
    fi
}

check_health() {
    print_section "🏥 Vérification Health Checks"
    
    endpoints=(
        "/api/health"
        "/api/health/deep"
        "/api/health/ready"
        "/api/health/live"
    )
    
    for endpoint in "${endpoints[@]}"; do
        if curl -f -s "$BASE_URL$endpoint" > /dev/null 2>&1; then
            print_success "$endpoint: OK"
        else
            print_error "$endpoint: FAILED"
            return 1
        fi
    done
}

check_metrics() {
    print_section "📊 Vérification Metrics"
    
    endpoints=(
        "/api/metrics"
        "/api/metrics/prometheus"
        "/api/metrics/summary"
    )
    
    for endpoint in "${endpoints[@]}"; do
        if curl -f -s "$BASE_URL$endpoint" > /dev/null 2>&1; then
            print_success "$endpoint: OK"
        else
            print_error "$endpoint: FAILED"
            return 1
        fi
    done
}

check_security_headers() {
    print_section "🔐 Vérification Security Headers"
    
    headers=$(curl -s -I "$BASE_URL/api/health" | grep -i "x-content-type-options\|x-frame-options\|x-xss-protection\|x-request-id")
    
    if echo "$headers" | grep -q "X-Content-Type-Options"; then
        print_success "X-Content-Type-Options présent"
    else
        print_warning "X-Content-Type-Options manquant"
    fi
    
    if echo "$headers" | grep -q "X-Request-ID"; then
        print_success "X-Request-ID présent"
    else
        print_warning "X-Request-ID manquant"
    fi
}

check_endpoints() {
    print_section "🔌 Vérification Endpoints"
    
    # Root
    if curl -f -s "$BASE_URL/" > /dev/null 2>&1; then
        print_success "Root endpoint: OK"
    else
        print_error "Root endpoint: FAILED"
    fi
    
    # API Info
    if curl -f -s "$BASE_URL/api/info" > /dev/null 2>&1; then
        print_success "API Info: OK"
    else
        print_error "API Info: FAILED"
    fi
    
    # Chat (peut échouer si pas de providers AI)
    response=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$BASE_URL/api/chat" \
        -H "Content-Type: application/json" \
        -d '{"message":"test","language":"en"}')
    
    if [ "$response" = "200" ] || [ "$response" = "503" ]; then
        print_success "Chat endpoint: OK (status: $response)"
    else
        print_warning "Chat endpoint: Status $response"
    fi
}

check_nginx() {
    print_section "🌐 Vérification Nginx"
    
    if systemctl is-active --quiet nginx; then
        print_success "Nginx est actif"
    else
        print_error "Nginx n'est pas actif"
        return 1
    fi
    
    if nginx -t > /dev/null 2>&1; then
        print_success "Configuration Nginx valide"
    else
        print_error "Configuration Nginx invalide"
        return 1
    fi
}

check_ssl() {
    print_section "🔒 Vérification SSL"
    
    # Vérifier si HTTPS est configuré
    if curl -k -s "https://localhost" > /dev/null 2>&1 || curl -k -s "https://$(hostname)" > /dev/null 2>&1; then
        print_success "SSL/HTTPS configuré"
    else
        print_warning "SSL/HTTPS non configuré (normal si pas de domaine)"
    fi
}

check_logs() {
    print_section "📝 Vérification Logs"
    
    if journalctl -u $SERVICE_NAME --since "5 minutes ago" --no-pager | grep -q "ERROR\|CRITICAL"; then
        print_warning "Erreurs détectées dans les logs récents"
        print_info "Vérifiez: journalctl -u $SERVICE_NAME -f"
    else
        print_success "Pas d'erreurs critiques dans les logs récents"
    fi
}

main() {
    print_section "🧪 VÉRIFICATION POST-DÉPLOIEMENT"
    
    errors=0
    
    check_service || ((errors++))
    check_nginx || ((errors++))
    check_health || ((errors++))
    check_metrics || ((errors++))
    check_security_headers
    check_endpoints
    check_ssl
    check_logs
    
    print_section "📊 RÉSUMÉ"
    
    if [ $errors -eq 0 ]; then
        print_success "✅ Toutes les vérifications critiques sont passées !"
        echo ""
        print_info "Le déploiement est réussi et opérationnel."
        return 0
    else
        print_error "❌ $errors vérification(s) critique(s) ont échoué"
        echo ""
        print_warning "Vérifiez les erreurs ci-dessus avant de continuer."
        return 1
    fi
}

main "$@"


