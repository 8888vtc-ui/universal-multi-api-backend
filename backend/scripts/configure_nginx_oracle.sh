#!/bin/bash
# Configuration Nginx pour Universal API Hub sur Oracle Cloud

echo "=========================================="
echo "  Configuration Nginx"
echo "=========================================="

# Créer la configuration Nginx
sudo tee /etc/nginx/conf.d/universal-api.conf > /dev/null << 'EOF'
server {
    listen 80;
    server_name 79.72.29.109;

    # Backend API
    location /api {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
        proxy_read_timeout 300s;
        proxy_connect_timeout 75s;
    }

    # Documentation Swagger
    location /docs {
        proxy_pass http://localhost:8000/docs;
        proxy_set_header Host $host;
    }

    location /redoc {
        proxy_pass http://localhost:8000/redoc;
        proxy_set_header Host $host;
    }

    # Health check
    location /api/health {
        proxy_pass http://localhost:8000/api/health;
        proxy_set_header Host $host;
    }

    # Metrics
    location /api/metrics {
        proxy_pass http://localhost:8000/api/metrics;
        proxy_set_header Host $host;
    }

    # Root endpoint
    location / {
        proxy_pass http://localhost:8000/;
        proxy_set_header Host $host;
    }
}
EOF

# Supprimer la config par défaut si elle existe
if [ -f /etc/nginx/conf.d/default.conf ]; then
    sudo rm /etc/nginx/conf.d/default.conf
fi

# Tester la configuration
echo "Test de la configuration Nginx..."
if sudo nginx -t; then
    echo "✅ Configuration Nginx valide"
else
    echo "❌ Erreur dans la configuration Nginx"
    exit 1
fi

# Recharger Nginx
echo "Rechargement de Nginx..."
sudo systemctl reload nginx

echo ""
echo "=========================================="
echo "  ✅ Nginx configuré!"
echo "=========================================="
echo ""
echo "🌐 Votre API est accessible sur:"
echo "   http://79.72.29.109/api/health"
echo "   http://79.72.29.109/docs"
echo "   http://79.72.29.109/api/metrics"
echo ""






