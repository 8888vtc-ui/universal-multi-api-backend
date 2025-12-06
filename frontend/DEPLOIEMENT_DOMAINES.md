# 🌐 Configuration des Domaines WikiAsk

## ✅ Domaines Enregistrés

- **wikiask.net** - Domaine principal (recommandé)
- **wikiask.fr** - Domaine français
- **wikiask.io** - Domaine tech/startup

Tous expirent le **2026-12-06** ✅

## 🚀 Stratégie de Déploiement

### Option 1 : Vercel (Recommandé pour Next.js)

**Frontend** : `wikiask.net` ou `www.wikiask.net`
**Backend API** : `api.wikiask.net` (sous-domaine)

#### Étapes :

1. **Installer Vercel CLI** :
```bash
npm i -g vercel
```

2. **Se connecter** :
```bash
vercel login
```

3. **Déployer le frontend** :
```bash
cd frontend
vercel
```

4. **Ajouter le domaine** :
```bash
vercel domains add wikiask.net
vercel domains add www.wikiask.net
```

5. **Configurer DNS** (chez votre registrar) :
```
Type: CNAME
Name: @ (ou www)
Value: cname.vercel-dns.com
```

6. **SSL automatique** : Vercel configure SSL automatiquement ✅

### Option 2 : Netlify (Alternative)

Même processus, mais avec Netlify CLI :
```bash
npm i -g netlify-cli
netlify deploy --prod
netlify domains add wikiask.net
```

## 🔧 Configuration Backend (Fly.io)

### Configurer le sous-domaine API

1. **Créer un sous-domaine** : `api.wikiask.net`

2. **Configurer DNS** :
```
Type: CNAME
Name: api
Value: universal-api-hub.fly.dev
```

3. **Mettre à jour Fly.io** :
```bash
cd backend
fly certs add api.wikiask.net
```

4. **Mettre à jour les variables d'environnement** :
```bash
fly secrets set CORS_ORIGINS="https://wikiask.net,https://www.wikiask.net"
```

## 📝 Variables d'Environnement

### Frontend (.env.local)

```env
NEXT_PUBLIC_API_URL=https://api.wikiask.net
NEXT_PUBLIC_APP_NAME=WikiAsk
NEXT_PUBLIC_APP_SLOGAN=Ask Everything. Know Everything.
```

### Backend (Fly.io secrets)

```bash
fly secrets set CORS_ORIGINS="https://wikiask.net,https://www.wikiask.net,https://wikiask.fr,https://wikiask.io"
```

## 🌍 Configuration Multi-Domaines

### Redirection wikiask.fr → wikiask.net

Si vous voulez rediriger `.fr` et `.io` vers `.net` :

1. **Vercel** : Ajouter les domaines et configurer des redirects
2. **Ou** : Configurer des redirects au niveau DNS

### Configuration Vercel pour multi-domaines

Dans `vercel.json` :
```json
{
  "redirects": [
    {
      "source": "/(.*)",
      "has": [
        {
          "type": "host",
          "value": "wikiask.fr"
        }
      ],
      "destination": "https://wikiask.net/$1",
      "permanent": true
    },
    {
      "source": "/(.*)",
      "has": [
        {
          "type": "host",
          "value": "wikiask.io"
        }
      ],
      "destination": "https://wikiask.net/$1",
      "permanent": true
    }
  ]
}
```

## ✅ Checklist Déploiement

- [ ] Déployer le frontend sur Vercel
- [ ] Configurer `wikiask.net` comme domaine principal
- [ ] Configurer `www.wikiask.net` (redirection vers wikiask.net)
- [ ] Configurer `api.wikiask.net` pour le backend
- [ ] Mettre à jour les variables d'environnement
- [ ] Vérifier SSL (automatique avec Vercel)
- [ ] Tester les endpoints API
- [ ] Configurer les redirects pour .fr et .io (optionnel)

## 🔒 Sécurité

1. **HTTPS** : Automatique avec Vercel et Fly.io
2. **CORS** : Configuré pour les domaines autorisés
3. **Rate Limiting** : Déjà implémenté dans le backend

## 📊 Monitoring

- **Vercel Analytics** : Activé automatiquement
- **Fly.io Metrics** : Disponible dans le dashboard
- **Uptime Monitoring** : Configurer avec UptimeRobot ou similaire

---

**Prochaines étapes** : Déployer sur Vercel et configurer les DNS ! 🚀

