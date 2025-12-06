# 🚀 Guide de Déploiement WikiAsk

## ✅ Domaines Disponibles

- **wikiask.net** - Domaine principal
- **wikiask.fr** - Domaine français  
- **wikiask.io** - Domaine tech

Tous expirent le **2026-12-06** ✅

## 📋 Plan de Déploiement

### 1. Frontend (Vercel) - wikiask.net

#### Installation Vercel CLI
```bash
npm install -g vercel
```

#### Déploiement
```bash
cd frontend
vercel login
vercel
```

#### Configuration Domaines
```bash
# Ajouter le domaine principal
vercel domains add wikiask.net

# Ajouter www (redirection automatique)
vercel domains add www.wikiask.net

# Ajouter les autres domaines (redirection vers .net)
vercel domains add wikiask.fr
vercel domains add wikiask.io
```

#### Configuration DNS (chez votre registrar)

Pour **wikiask.net** :
```
Type: A
Name: @
Value: 76.76.21.21 (IP Vercel - vérifier dans le dashboard)

OU

Type: CNAME
Name: @
Value: cname.vercel-dns.com
```

Pour **www.wikiask.net** :
```
Type: CNAME
Name: www
Value: cname.vercel-dns.com
```

### 2. Backend API (Fly.io) - api.wikiask.net

#### Configuration du sous-domaine
```bash
cd backend
fly certs add api.wikiask.net
```

#### Mise à jour CORS
```bash
fly secrets set CORS_ORIGINS="https://wikiask.net,https://www.wikiask.net,https://wikiask.fr,https://wikiask.io"
```

#### Configuration DNS pour API

Chez votre registrar :
```
Type: CNAME
Name: api
Value: universal-api-hub.fly.dev
```

### 3. Variables d'Environnement

#### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=https://api.wikiask.net
NEXT_PUBLIC_APP_NAME=WikiAsk
NEXT_PUBLIC_APP_SLOGAN=Ask Everything. Know Everything.
```

#### Backend (Fly.io secrets)
```bash
fly secrets set CORS_ORIGINS="https://wikiask.net,https://www.wikiask.net,https://wikiask.fr,https://wikiask.io"
```

## 🔄 Redirections

Les redirections `.fr` et `.io` → `.net` sont configurées dans `vercel.json`.

## ✅ Checklist

### Frontend
- [ ] Installer Vercel CLI
- [ ] Déployer sur Vercel
- [ ] Ajouter wikiask.net
- [ ] Ajouter www.wikiask.net
- [ ] Configurer DNS chez le registrar
- [ ] Vérifier SSL (automatique)
- [ ] Tester https://wikiask.net

### Backend
- [ ] Configurer api.wikiask.net sur Fly.io
- [ ] Ajouter le certificat SSL
- [ ] Configurer DNS CNAME
- [ ] Mettre à jour CORS_ORIGINS
- [ ] Tester https://api.wikiask.net/api/health

### Tests
- [ ] Frontend accessible sur wikiask.net
- [ ] API accessible sur api.wikiask.net
- [ ] Redirections .fr et .io fonctionnent
- [ ] SSL valide sur tous les domaines
- [ ] CORS fonctionne correctement

## 🎯 URLs Finales

- **Frontend** : https://wikiask.net
- **API** : https://api.wikiask.net
- **Redirections** : 
  - https://wikiask.fr → https://wikiask.net
  - https://wikiask.io → https://wikiask.net

## 📊 Monitoring

Après déploiement, configurer :
- **Vercel Analytics** (automatique)
- **Fly.io Metrics** (dashboard)
- **Uptime Monitoring** (UptimeRobot, Pingdom, etc.)

---

**Prêt à déployer !** 🚀

