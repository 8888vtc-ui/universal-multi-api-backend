# 🔐 Authentification - Universal Multi-API Backend

## Vue d'ensemble

Système d'authentification JWT complet avec :
- Inscription/Connexion
- Tokens JWT (access + refresh)
- Protection des endpoints
- Gestion des utilisateurs

---

## 🚀 Endpoints

### POST `/api/auth/register`
Enregistrer un nouvel utilisateur

**Body**:
```json
{
  "email": "user@example.com",
  "username": "johndoe",
  "password": "securepassword123"
}
```

**Response**:
```json
{
  "id": "user_1234567890",
  "email": "user@example.com",
  "username": "johndoe",
  "is_active": true,
  "created_at": "2024-12-01T10:00:00"
}
```

---

### POST `/api/auth/login`
Connexion utilisateur

**Body** (form-data):
- `username`: Email de l'utilisateur
- `password`: Mot de passe

**Response**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

---

### POST `/api/auth/refresh`
Rafraîchir un access token

**Body**:
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response**:
```json
{
  "access_token": "nouveau_token...",
  "refresh_token": "nouveau_refresh_token...",
  "token_type": "bearer"
}
```

---

### GET `/api/auth/me`
Obtenir les informations de l'utilisateur actuel

**Headers**:
```
Authorization: Bearer <access_token>
```

**Response**:
```json
{
  "id": "user_1234567890",
  "email": "user@example.com",
  "username": "johndoe",
  "is_active": true,
  "created_at": "2024-12-01T10:00:00"
}
```

---

### POST `/api/auth/logout`
Déconnexion (invalider les refresh tokens)

**Headers**:
```
Authorization: Bearer <access_token>
```

**Response**:
```json
{
  "message": "Logged out successfully"
}
```

---

## 🔒 Protection des Endpoints

Pour protéger un endpoint, utilisez `Depends(get_current_user)`:

```python
from routers.auth import get_current_user
from services.auth import User

@router.get("/protected")
async def protected_endpoint(current_user: User = Depends(get_current_user)):
    return {"message": f"Hello {current_user.username}"}
```

---

## ⚙️ Configuration

### Variables d'environnement

Ajouter dans `.env`:
```env
JWT_SECRET_KEY=your-secret-key-change-in-production
```

### Durée des tokens

- **Access token**: 30 minutes (par défaut)
- **Refresh token**: 7 jours (par défaut)

Modifiable dans `services/auth.py`:
```python
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7
```

---

## 📝 Exemples d'utilisation

### Python

```python
import httpx

# Inscription
response = httpx.post(
    "http://localhost:8000/api/auth/register",
    json={
        "email": "user@example.com",
        "username": "johndoe",
        "password": "securepassword123"
    }
)
user = response.json()

# Connexion
response = httpx.post(
    "http://localhost:8000/api/auth/login",
    data={
        "username": "user@example.com",
        "password": "securepassword123"
    }
)
tokens = response.json()
access_token = tokens["access_token"]

# Requête protégée
response = httpx.get(
    "http://localhost:8000/api/auth/me",
    headers={"Authorization": f"Bearer {access_token}"}
)
user_info = response.json()
```

### cURL

```bash
# Inscription
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "johndoe",
    "password": "securepassword123"
  }'

# Connexion
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user@example.com&password=securepassword123"

# Requête protégée
curl -X GET http://localhost:8000/api/auth/me \
  -H "Authorization: Bearer <access_token>"
```

---

## 🔐 Sécurité

- ✅ Mots de passe hashés avec bcrypt
- ✅ Tokens JWT signés avec HS256
- ✅ Refresh tokens stockés en base de données
- ✅ Expiration automatique des tokens
- ✅ Validation des emails

---

## 📊 Base de données

Les utilisateurs sont stockés dans `data/auth.db` (SQLite) avec :
- Table `users` : Informations utilisateurs
- Table `refresh_tokens` : Refresh tokens actifs

---

**Dernière mise à jour** : Décembre 2024


<<<<<<< Updated upstream
=======





>>>>>>> Stashed changes
