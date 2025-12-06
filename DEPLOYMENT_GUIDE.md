# 🚀 Guide de Déploiement

**Version** : 2.3.0  
**Environnements** : Local, VPS, Cloud (AWS/GCP/Azure), Kubernetes, Docker

---

## 📋 Table des Matières

1. [Déploiement Local](#déploiement-local)
2. [Déploiement VPS](#déploiement-vps)
3. [Déploiement Docker](#déploiement-docker)
4. [Déploiement Kubernetes](#déploiement-kubernetes)
5. [Déploiement Cloud](#déploiement-cloud)
6. [Monitoring & Maintenance](#monitoring--maintenance)

---

## 🏠 Déploiement Local

### Prérequis
- Python 3.9+
- Redis (optionnel)
- Variables d'environnement configurées

### Étapes

```bash
# 1. Cloner et installer
git clone <repo>
cd backend
pip install -r requirements.txt

# 2. Configuration
cp .env.example .env
# Éditer .env avec vos clés API

# 3. Démarrer
python main.py
```

**Accès** : http://localhost:8000

---

## 🖥️ Déploiement VPS

### Option 1 : Systemd Service

#### 1. Créer le service

```bash
sudo nano /etc/systemd/system/universal-api.service
```

Contenu :
```ini
[Unit]
Description=Universal Multi-API Backend
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/universal-api/backend
Environment="PATH=/opt/universal-api/venv/bin"
ExecStart=/opt/universal-api/venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

#### 2. Activer et démarrer

```bash
sudo systemctl daemon-reload
sudo systemctl enable universal-api
sudo systemctl start universal-api
sudo systemctl status universal-api
```

#### 3. Logs

```bash
sudo journalctl -u universal-api -f
```

### Option 2 : Gunicorn + Nginx

#### 1. Installer Gunicorn

```bash
pip install gunicorn
```

#### 2. Créer le script de démarrage

```bash
# gunicorn_config.py
bind = "127.0.0.1:8000"
workers = 4
worker_class = "uvicorn.workers.UvicornWorker"
timeout = 120
keepalive = 5
```

#### 3. Démarrer avec Gunicorn

```bash
gunicorn -c gunicorn_config.py main:app
```

#### 4. Configuration Nginx

```nginx
# /etc/nginx/sites-available/universal-api
server {
    listen 80;
    server_name api.votredomaine.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Request-ID $request_id;
    }
}
```

---

## 🐳 Déploiement Docker

### 1. Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Installer les dépendances système
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copier requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code
COPY . .

# Variables d'environnement
ENV PYTHONUNBUFFERED=1
ENV API_HOST=0.0.0.0
ENV API_PORT=8000

# Exposer le port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD python -c "import httpx; httpx.get('http://localhost:8000/api/health/live')"

# Commande de démarrage
CMD ["python", "main.py"]
```

### 2. Docker Compose

```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - JWT_SECRET_KEY=${JWT_SECRET_KEY}
      - REDIS_HOST=redis
      - GROQ_API_KEY=${GROQ_API_KEY}
    env_file:
      - .env
    depends_on:
      - redis
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    restart: unless-stopped

volumes:
  redis_data:
```

### 3. Déploiement

```bash
# Build
docker-compose build

# Démarrer
docker-compose up -d

# Logs
docker-compose logs -f api

# Arrêter
docker-compose down
```

---

## ☸️ Déploiement Kubernetes

### 1. Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: universal-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: universal-api
  template:
    metadata:
      labels:
        app: universal-api
    spec:
      containers:
      - name: api
        image: your-registry/universal-api:2.3.0
        ports:
        - containerPort: 8000
        env:
        - name: JWT_SECRET_KEY
          valueFrom:
            secretKeyRef:
              name: api-secrets
              key: jwt-secret-key
        - name: REDIS_HOST
          value: "redis-service"
        livenessProbe:
          httpGet:
            path: /api/health/live
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /api/health/ready
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 5
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
```

### 2. Service

```yaml
apiVersion: v1
kind: Service
metadata:
  name: universal-api-service
spec:
  selector:
    app: universal-api
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  type: LoadBalancer
```

### 3. Ingress

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: universal-api-ingress
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
spec:
  tls:
  - hosts:
    - api.votredomaine.com
    secretName: api-tls
  rules:
  - host: api.votredomaine.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: universal-api-service
            port:
              number: 80
```

### 4. Secrets

```bash
kubectl create secret generic api-secrets \
  --from-literal=jwt-secret-key=$(python -c "import secrets; print(secrets.token_urlsafe(32))")
```

---

## ☁️ Déploiement Cloud

### AWS (Elastic Beanstalk)

```bash
# 1. Installer EB CLI
pip install awsebcli

# 2. Initialiser
eb init -p python-3.11 universal-api

# 3. Créer l'environnement
eb create universal-api-prod

# 4. Déployer
eb deploy
```

### Google Cloud Run

```bash
# 1. Build l'image
gcloud builds submit --tag gcr.io/PROJECT_ID/universal-api

# 2. Déployer
gcloud run deploy universal-api \
  --image gcr.io/PROJECT_ID/universal-api \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### Azure App Service

```bash
# 1. Créer l'app
az webapp create \
  --resource-group myResourceGroup \
  --plan myAppServicePlan \
  --name universal-api \
  --runtime "PYTHON|3.11"

# 2. Déployer
az webapp up \
  --resource-group myResourceGroup \
  --name universal-api
```

---

## 📊 Monitoring & Maintenance

### Métriques Prometheus

```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'universal-api'
    static_configs:
      - targets: ['localhost:8000']
    metrics_path: '/api/metrics/prometheus'
    scrape_interval: 15s
```

### Alertes

```yaml
# alerts.yml
groups:
  - name: universal_api
    rules:
      - alert: HighErrorRate
        expr: rate(api_errors_total[5m]) > 0.1
        for: 5m
        annotations:
          summary: "High error rate detected"
      
      - alert: SlowResponseTime
        expr: api_response_time_ms > 5000
        for: 10m
        annotations:
          summary: "Response time is slow"
```

### Logs

```bash
# Logs système (systemd)
sudo journalctl -u universal-api -f

# Logs Docker
docker-compose logs -f api

# Logs Kubernetes
kubectl logs -f deployment/universal-api
```

### Backup

```bash
# Backup base de données
cp ./data/auth.db ./backups/auth-$(date +%Y%m%d).db

# Backup Redis
redis-cli --rdb ./backups/redis-$(date +%Y%m%d).rdb
```

---

## 🔒 Sécurité Production

### Checklist

- [ ] `JWT_SECRET_KEY` fort et unique
- [ ] HTTPS activé (certificat SSL)
- [ ] CORS configuré correctement
- [ ] Rate limiting activé
- [ ] Firewall configuré
- [ ] Secrets dans variables d'environnement (pas dans le code)
- [ ] Logs ne contiennent pas de données sensibles
- [ ] Mises à jour de sécurité régulières

### Variables d'Environnement Critiques

```env
ENVIRONMENT=production
JWT_SECRET_KEY=<généré avec secrets.token_urlsafe(32)>
CORS_ORIGINS=https://votredomaine.com
REDIS_PASSWORD=<mot de passe fort>
```

---

## 🆘 Dépannage

### Problème : Service ne démarre pas

```bash
# Vérifier les logs
sudo journalctl -u universal-api -n 50

# Vérifier les permissions
ls -la /opt/universal-api/backend

# Tester manuellement
cd /opt/universal-api/backend
python main.py
```

### Problème : Redis non connecté

```bash
# Vérifier Redis
redis-cli ping

# Vérifier la configuration
grep REDIS .env
```

### Problème : Port déjà utilisé

```bash
# Trouver le processus
sudo lsof -i :8000

# Tuer le processus
sudo kill -9 <PID>
```

---

## 📚 Ressources

- **Documentation API** : `/docs` (Swagger)
- **Health Checks** : `/api/health/deep`
- **Métriques** : `/api/metrics`
- **Guide de démarrage** : `QUICK_START.md`

---

*Dernière mise à jour : v2.3.0*



