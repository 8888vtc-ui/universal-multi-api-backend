# 🧪 Tests Techniques du Site WikiAsk

## 📋 Tests à Effectuer

### 1. Backend API (Fly.io)

#### Test Health Check
```bash
curl https://universal-api-hub.fly.dev/api/health
```

#### Test Chat Endpoint
```bash
curl -X POST https://universal-api-hub.fly.dev/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"Hello","language":"fr"}'
```

#### Test Search Endpoint
```bash
curl "https://universal-api-hub.fly.dev/api/search?q=test"
```

### 2. Sous-domaine API (si configuré)

```bash
curl https://api.wikiask.net/api/health
```

### 3. Frontend (Netlify)

#### Trouver l'URL Netlify
- Aller dans Netlify Dashboard
- L'URL est du type : `https://wikiask-XXXX.netlify.app`

#### Test de la page d'accueil
```bash
curl https://VOTRE-URL-NETLIFY.netlify.app
```

#### Test des appels API depuis le frontend
- Ouvrir la console du navigateur
- Vérifier les erreurs CORS
- Vérifier les appels API

### 4. Variables d'Environnement

Vérifier dans Netlify Dashboard :
- `NEXT_PUBLIC_API_URL` est bien configurée
- La valeur pointe vers le bon backend

### 5. CORS

Vérifier que le backend autorise le frontend :
- Backend doit avoir `CORS_ORIGINS` avec l'URL Netlify
- Ou utiliser `https://universal-api-hub.fly.dev` directement

## 🔍 Diagnostic des Erreurs

### Erreur CORS
- **Symptôme** : "CORS policy" dans la console
- **Solution** : Mettre à jour `CORS_ORIGINS` sur Fly.io

### Erreur 404
- **Symptôme** : "Not Found"
- **Solution** : Vérifier l'URL de l'API

### Erreur DNS
- **Symptôme** : "Failed to fetch" ou timeout
- **Solution** : Le sous-domaine n'est pas configuré

### Erreur 500
- **Symptôme** : "Internal Server Error"
- **Solution** : Vérifier les logs du backend

## ✅ Checklist

- [ ] Backend répond sur Fly.io
- [ ] Frontend déployé sur Netlify
- [ ] Variables d'environnement configurées
- [ ] CORS configuré correctement
- [ ] Pas d'erreurs dans la console
- [ ] Les appels API fonctionnent

