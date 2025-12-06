# ================================
# Universal Multi-API Backend
# Dockerfile simplifié pour Fly.io
# ================================

FROM python:3.11-slim

WORKDIR /app

# Installer les dépendances système
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copier et installer les dépendances Python (version allégée pour Fly.io)
COPY requirements-fly.txt .
RUN pip install --no-cache-dir -r requirements-fly.txt

# Copier le code source
COPY . .

# Variables d'environnement
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

# Exposer le port
EXPOSE 8000

# Commande de démarrage
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]
