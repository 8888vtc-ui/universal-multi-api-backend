# 🚀 Guide de Déploiement - Universal Multi-API Backend

## Vue d'ensemble

Ce guide couvre le déploiement du backend sur différents environnements : développement local, VPS, et cloud.

---

## 📋 Prérequis

### Système
- Python 3.10+
- pip
- Git

### Optionnel (selon fonctionnalités)
- Redis (pour cache)
- Ollama (pour LLM local)
- PostgreSQL/MySQL (pour production, optionnel)

---

## 🔧 Installation Locale

### 1. Cloner le projet
```bash
git clone <repository-url>
cd "moteur israelien/backend"
```

### 2. Créer environnement virtuel
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Installer dépendances
```bash
pip install -r requirements.txt
```

### 4. Configuration
Créer un fichier `.env` :
```env
# AI Providers
GROQ_API_KEY=your_groq_key
MISTRAL_API_KEY=your_mistral_key
GEMINI_API_KEY=your_gemini_key
OPENROUTER_API_KEY=your_openrouter_key

# External APIs (optionnel)
NEWS_API_KEY=your_news_key
WEATHER_API_KEY=your_weather_key
D_ID_API_KEY=your_did_key

# Redis (optionnel)
REDIS_URL=redis://localhost:6379

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:8080
```

### 5. Lancer le serveur
```bash
# Développement
python main.py

# Ou avec uvicorn
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Le serveur sera accessible sur `http://localhost:8000`

---

## 🖥️ Déploiement VPS (Ubuntu/Debian)

### 1. Préparation serveur
```bash
# Mettre à jour
sudo apt update && sudo apt upgrade -y

# Installer Python et dépendances
sudo apt install python3 python3-pip python3-venv nginx git -y
```

### 2. Cloner et configurer
```bash
cd /opt
sudo git clone <repository-url> api-backend
cd api-backend/backend

# Créer environnement virtuel
python3 -m venv venv
source venv/bin/activate

# Installer dépendances
pip install -r requirements.txt
```

### 3. Configuration système
Créer fichier `.env` :
```bash
sudo nano .env
# Ajouter toutes les clés API
```

### 4. Service systemd
Créer `/etc/systemd/system/api-backend.service` :
```ini
[Unit]
Description=Universal Multi-API Backend
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/api-backend/backend
Environment="PATH=/opt/api-backend/backend/venv/bin"
ExecStart=/opt/api-backend/backend/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

Activer le service :
```bash
sudo systemctl daemon-reload
sudo systemctl enable api-backend
sudo systemctl start api-backend
sudo systemctl status api-backend
```

### 5. Configuration Nginx
Créer `/etc/nginx/sites-available/api-backend` :
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Activer :
```bash
sudo ln -s /etc/nginx/sites-available/api-backend /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 6. SSL avec Let's Encrypt
```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d your-domain.com
```

---

## ☁️ Déploiement Cloud

### Railway
1. Créer compte Railway
2. Connecter repository GitHub
3. Railway détecte automatiquement Python
4. Ajouter variables d'environnement dans dashboard
5. Déploiement automatique

### Render
1. Créer compte Render
2. New Web Service
3. Connecter repository
4. Configuration :
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Ajouter variables d'environnement

### Heroku
```bash
# Installer Heroku CLI
heroku login
heroku create your-app-name

# Déployer
git push heroku main

# Configurer variables
heroku config:set GROQ_API_KEY=your_key
```

### DigitalOcean App Platform
1. Créer nouvelle app
2. Connecter repository
3. Configuration automatique
4. Ajouter variables d'environnement

---

## 🐳 Docker (Optionnel)

### Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### docker-compose.yml
```yaml
version: '3.8'

services:
  backend:
    build: .
    ports:
      - "8000:8000"
    environment:
      - REDIS_URL=redis://redis:6379
    depends_on:
      - redis
  
  redis:
    image: redis:alpine
    ports:
      - "6379:6379"
```

Lancer :
```bash
docker-compose up -d
```

---

## 🔒 Sécurité

### Variables d'environnement
- ⚠️ **JAMAIS** commiter le fichier `.env`
- Utiliser variables d'environnement du système
- Utiliser secrets manager (AWS Secrets, etc.)

### Rate Limiting
Le rate limiting est activé par défaut. Configurer dans `services/rate_limiter.py` :
```python
ENDPOINT_LIMITS = {
    "/api/chat": ["50/hour", "10/minute"],
    # ...
}
```

### CORS
Configurer dans `.env` :
```env
CORS_ORIGINS=https://yourdomain.com,https://app.yourdomain.com
```

### Firewall
```bash
# UFW (Ubuntu)
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

---

## 📊 Monitoring

### Logs
```bash
# Voir logs systemd
sudo journalctl -u api-backend -f

# Logs Nginx
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### Analytics
Le service analytics est automatiquement activé :
- Métriques : `/api/analytics/metrics`
- Dashboard : `/api/analytics/dashboard`

### Health Check
```bash
curl http://localhost:8000/api/health
```

---

## 🔄 Mise à jour

### Développement
```bash
git pull
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart api-backend
```

### Production
1. Tester en staging d'abord
2. Backup base de données
3. Pull latest code
4. Migrations si nécessaire
5. Redémarrer service

---

## 🐛 Dépannage

### Service ne démarre pas
```bash
# Vérifier logs
sudo journalctl -u api-backend -n 50

# Vérifier permissions
sudo chown -R www-data:www-data /opt/api-backend

# Vérifier Python
which python3
python3 --version
```

### Port déjà utilisé
```bash
# Trouver processus
sudo lsof -i :8000

# Tuer processus
sudo kill -9 <PID>
```

### Erreurs d'import
```bash
# Vérifier environnement virtuel
source venv/bin/activate
pip list

# Réinstaller dépendances
pip install -r requirements.txt --force-reinstall
```

---

## 📈 Optimisation Performance

### Gunicorn (Production)
```bash
pip install gunicorn

# Lancer avec Gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Redis Cache
Installer Redis :
```bash
sudo apt install redis-server -y
sudo systemctl start redis
```

Configurer dans `.env` :
```env
REDIS_URL=redis://localhost:6379
```

### Ollama (LLM Local)
```bash
# Installer Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Lancer
ollama serve

# Télécharger modèle
ollama pull llama2
```

---

## ✅ Checklist Déploiement

- [ ] Variables d'environnement configurées
- [ ] Service systemd créé et activé
- [ ] Nginx configuré
- [ ] SSL configuré (Let's Encrypt)
- [ ] Firewall configuré
- [ ] Monitoring activé
- [ ] Backups configurés
- [ ] Tests passés
- [ ] Documentation à jour

---

**Dernière mise à jour**: Décembre 2024  
**Version**: 2.1.0



