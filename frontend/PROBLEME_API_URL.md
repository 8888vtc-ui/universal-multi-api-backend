# 🔍 Problème : Variable API_URL

## ❌ Le Problème

La variable `NEXT_PUBLIC_API_URL` est configurée pour pointer vers :
```
https://api.wikiask.net
```

**MAIS** ce sous-domaine n'est probablement pas encore configuré ou accessible !

## 🔍 Pourquoi ça ne fonctionne pas ?

1. **Le backend est sur Fly.io** : `https://universal-api-hub.fly.dev`
2. **Le sous-domaine `api.wikiask.net`** doit être configuré pour pointer vers Fly.io
3. **Si le DNS n'est pas configuré**, `api.wikiask.net` ne fonctionne pas
4. **Le frontend essaie d'appeler** `https://api.wikiask.net/api/...` → **ERREUR**

## ✅ Solutions

### Solution 1 : Utiliser directement Fly.io (TEMPORAIRE)

**Dans Netlify Dashboard → Environment variables :**

Changer :
```
NEXT_PUBLIC_API_URL = https://universal-api-hub.fly.dev
```

**Avantages :**
- ✅ Fonctionne immédiatement
- ✅ Pas besoin de configurer DNS

**Inconvénients :**
- ⚠️ URL moins "propre"
- ⚠️ Solution temporaire

### Solution 2 : Configurer le sous-domaine (DÉFINITIF)

**Étape 1 : Configurer sur Fly.io**
```bash
cd backend
fly certs add api.wikiask.net
```

**Étape 2 : Configurer DNS chez votre registrar**

Chez votre registrar (où vous avez acheté wikiask.net) :
```
Type: CNAME
Name: api
Value: universal-api-hub.fly.dev
```

**Étape 3 : Mettre à jour CORS sur Fly.io**
```bash
fly secrets set CORS_ORIGINS="https://wikiask.net,https://www.wikiask.net"
```

**Étape 4 : Attendre la propagation DNS (15 min - 48h)**

**Étape 5 : Vérifier que ça fonctionne**
```bash
curl https://api.wikiask.net/api/health
```

## 🎯 Recommandation

**Pour tester rapidement :**
1. Utilisez la **Solution 1** (Fly.io directement)
2. Une fois que tout fonctionne, configurez le sous-domaine (Solution 2)

## 📝 Variables à mettre dans Netlify

### Option A : Direct Fly.io (pour tester)
```
NEXT_PUBLIC_API_URL=https://universal-api-hub.fly.dev
```

### Option B : Sous-domaine (une fois configuré)
```
NEXT_PUBLIC_API_URL=https://api.wikiask.net
```

## 🔧 Vérification

Pour vérifier si `api.wikiask.net` fonctionne :
```bash
# Dans un terminal
curl https://api.wikiask.net/api/health

# Si ça retourne une erreur DNS → Le sous-domaine n'est pas configuré
# Si ça retourne du JSON → Ça fonctionne !
```

## ⚠️ Erreurs courantes

1. **CORS Error** : Le backend n'autorise pas votre domaine
   - Solution : Mettre à jour `CORS_ORIGINS` sur Fly.io

2. **DNS Error** : Le sous-domaine ne résout pas
   - Solution : Vérifier la configuration DNS

3. **SSL Error** : Certificat non valide
   - Solution : `fly certs add api.wikiask.net`

---

**Action immédiate** : Changez la variable dans Netlify vers `https://universal-api-hub.fly.dev` pour que ça fonctionne tout de suite !

