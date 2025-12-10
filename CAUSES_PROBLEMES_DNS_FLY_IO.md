# 🔍 Causes des Problèmes DNS sur Fly.io

**Date** : Décembre 2024  
**Contexte** : Problèmes de résolution DNS pour les domaines personnalisés sur Fly.io

---

## ❌ PROBLÈMES IDENTIFIÉS

### 1. **Sous-domaine non configuré dans le DNS** ⚠️ PRINCIPAL

**Symptôme** :
```
Erreur DNS : "Le nom distant n'a pas pu être résolu: 'api.wikiask.net'"
```

**Cause** :
- Le sous-domaine `api.wikiask.net` n'a **pas été configuré** chez le registrar (où vous avez acheté le domaine)
- Aucun enregistrement CNAME ou A n'existe pour pointer vers Fly.io

**Solution** :
```bash
# Chez votre registrar (ex: Namecheap, GoDaddy, etc.)
Type: CNAME
Name: api
Value: universal-api-hub.fly.dev
TTL: 3600 (ou automatique)
```

---

### 2. **Certificat SSL non ajouté sur Fly.io** ⚠️ CRITIQUE

**Symptôme** :
```
SSL Error : "Certificate not valid"
Erreur : "ERR_SSL_PROTOCOL_ERROR"
```

**Cause** :
- Le certificat SSL n'a **pas été généré** sur Fly.io
- Fly.io ne peut pas créer le certificat tant que le DNS n'est pas configuré

**Solution** :
```bash
cd backend
fly certs add api.wikiask.net
```

**Important** : Cette commande doit être exécutée **APRÈS** avoir configuré le DNS, car Fly.io doit vérifier la propriété du domaine.

---

### 3. **Propagation DNS en cours** ⏳ TEMPORAIRE

**Symptôme** :
```
Le domaine fonctionne parfois, parfois non
Erreur intermittente
```

**Cause** :
- La propagation DNS peut prendre **15 minutes à 48 heures**
- Les serveurs DNS du monde entier doivent mettre à jour leurs caches
- Certains serveurs DNS peuvent avoir des valeurs en cache obsolètes

**Solution** :
- **Attendre** : La propagation est automatique
- **Vérifier** : Utiliser `dig api.wikiask.net` ou `nslookup api.wikiask.net`
- **Forcer** : Vider le cache DNS local (`ipconfig /flushdns` sur Windows)

---

### 4. **Configuration CNAME incorrecte** ⚠️ FRÉQUENT

**Symptôme** :
```
Le domaine ne résout pas vers Fly.io
Erreur : "CNAME record not found"
```

**Causes possibles** :
- **Mauvaise valeur** : CNAME pointe vers une mauvaise URL
- **Mauvais nom** : Le nom du sous-domaine est incorrect
- **Type incorrect** : Utilisation d'un enregistrement A au lieu de CNAME
- **Point final** : Certains registrars nécessitent un point final (`.`) dans la valeur

**Solution correcte** :
```
Type: CNAME
Name: api                    # Sans le domaine complet
Value: universal-api-hub.fly.dev    # Avec le point final si requis
```

**Erreurs courantes** :
```
❌ Name: api.wikiask.net     # TROP LONG
❌ Value: https://universal-api-hub.fly.dev  # AVEC PROTOCOLE
❌ Type: A                   # MAUVAIS TYPE
```

---

### 5. **Domaine non ajouté sur Fly.io** ⚠️ OUBLI FRÉQUENT

**Symptôme** :
```
Le DNS est configuré mais Fly.io ne répond pas
Erreur : "Host not found"
```

**Cause** :
- Le domaine n'a **jamais été ajouté** sur Fly.io
- Fly.io ne sait pas qu'il doit gérer ce domaine

**Solution** :
```bash
cd backend
fly certs add api.wikiask.net
```

Cette commande :
1. Ajoute le domaine à votre app Fly.io
2. Génère le certificat SSL (Let's Encrypt)
3. Configure le routage

---

### 6. **Ordre de configuration incorrect** ⚠️ ERREUR DE PROCESSUS

**Symptôme** :
```
Le certificat ne peut pas être généré
Erreur : "DNS verification failed"
```

**Cause** :
- Tentative d'ajouter le certificat **AVANT** de configurer le DNS
- Fly.io ne peut pas vérifier la propriété du domaine si le DNS ne pointe pas encore vers Fly.io

**Ordre correct** :
1. ✅ **D'abord** : Configurer le DNS chez le registrar
2. ✅ **Ensuite** : Attendre la propagation (15 min minimum)
3. ✅ **Enfin** : Ajouter le certificat sur Fly.io

**Ordre incorrect** :
```
❌ 1. fly certs add api.wikiask.net  # TROP TÔT
❌ 2. Configurer DNS                 # TROP TARD
```

---

### 7. **CORS non configuré** ⚠️ PROBLÈME DE SÉCURITÉ

**Symptôme** :
```
Le domaine fonctionne mais les requêtes sont bloquées
Erreur : "CORS policy blocked"
```

**Cause** :
- Le domaine n'est **pas autorisé** dans les origines CORS
- Fly.io bloque les requêtes depuis des domaines non autorisés

**Solution** :
```bash
fly secrets set CORS_ORIGINS="https://wikiask.net,https://www.wikiask.net,https://api.wikiask.net"
```

---

### 8. **App Fly.io incorrecte** ⚠️ MAUVAISE CONFIGURATION

**Symptôme** :
```
Le domaine pointe vers la mauvaise app
Erreur : "App not found"
```

**Cause** :
- Le CNAME pointe vers une **mauvaise app** Fly.io
- L'app a été supprimée ou renommée

**Vérification** :
```bash
cd backend
fly status
# Vérifier que l'app s'appelle bien "universal-api-hub"
```

**Solution** :
- Vérifier le nom de l'app dans `fly.toml`
- Mettre à jour le CNAME si nécessaire

---

### 9. **TTL DNS trop élevé** ⚠️ PROPAGATION LENTE

**Symptôme** :
```
Les changements DNS prennent très longtemps
Propagation > 48 heures
```

**Cause** :
- Le TTL (Time To Live) est **trop élevé** (ex: 86400 = 24h)
- Les serveurs DNS gardent l'ancienne valeur en cache trop longtemps

**Solution** :
- **Réduire le TTL** avant de faire des changements (ex: 300 = 5 min)
- **Attendre** que le TTL expire
- **Faire le changement** DNS
- **Remettre le TTL** à une valeur normale (3600 = 1h)

---

### 10. **Firewall ou Proxy bloquant** ⚠️ PROBLÈME RÉSEAU

**Symptôme** :
```
Le DNS fonctionne mais la connexion échoue
Timeout ou erreur de connexion
```

**Cause** :
- Firewall d'entreprise bloquant Fly.io
- Proxy interceptant les requêtes
- DNS local (ex: Pi-hole) bloquant certains domaines

**Solution** :
- Tester depuis un autre réseau
- Vérifier les règles de firewall
- Désactiver temporairement le proxy

---

## 📋 CHECKLIST DE DIAGNOSTIC

### Étape 1 : Vérifier le DNS
```bash
# Windows
nslookup api.wikiask.net

# Linux/Mac
dig api.wikiask.net
```

**Résultat attendu** :
```
api.wikiask.net → universal-api-hub.fly.dev
```

### Étape 2 : Vérifier le certificat Fly.io
```bash
cd backend
fly certs show
```

**Résultat attendu** :
```
api.wikiask.net : Valid (Let's Encrypt)
```

### Étape 3 : Tester la connexion
```bash
curl https://api.wikiask.net/api/health
```

**Résultat attendu** :
```json
{"status": "healthy", "version": "2.3.0"}
```

### Étape 4 : Vérifier CORS
```bash
fly secrets list | grep CORS
```

**Résultat attendu** :
```
CORS_ORIGINS=https://wikiask.net,https://www.wikiask.net
```

---

## ✅ SOLUTION COMPLÈTE (Ordre Correct)

### 1. Configurer le DNS chez le registrar
```
Type: CNAME
Name: api
Value: universal-api-hub.fly.dev
TTL: 3600
```

### 2. Attendre la propagation (15 min minimum)
```bash
# Vérifier la propagation
nslookup api.wikiask.net
# Doit retourner : universal-api-hub.fly.dev
```

### 3. Ajouter le certificat sur Fly.io
```bash
cd backend
fly certs add api.wikiask.net
```

### 4. Configurer CORS
```bash
fly secrets set CORS_ORIGINS="https://wikiask.net,https://www.wikiask.net,https://api.wikiask.net"
```

### 5. Vérifier que tout fonctionne
```bash
curl https://api.wikiask.net/api/health
```

---

## 🔧 COMMANDES DE DÉPANNAGE

### Vérifier le statut de l'app
```bash
cd backend
fly status
```

### Voir les certificats
```bash
fly certs show
```

### Voir les logs
```bash
fly logs
```

### Vérifier les secrets
```bash
fly secrets list
```

### Tester la résolution DNS
```bash
# Windows
nslookup api.wikiask.net 8.8.8.8

# Linux/Mac
dig @8.8.8.8 api.wikiask.net
```

### Vider le cache DNS local
```bash
# Windows
ipconfig /flushdns

# Linux
sudo systemd-resolve --flush-caches

# Mac
sudo dscacheutil -flushcache
```

---

## 📊 RÉSUMÉ DES CAUSES

| # | Cause | Fréquence | Impact | Solution |
|---|-------|-----------|--------|----------|
| 1 | DNS non configuré | ⭐⭐⭐⭐⭐ | Critique | Configurer CNAME |
| 2 | Certificat non ajouté | ⭐⭐⭐⭐ | Critique | `fly certs add` |
| 3 | Propagation DNS | ⭐⭐⭐ | Moyen | Attendre 15-48h |
| 4 | CNAME incorrect | ⭐⭐⭐ | Critique | Vérifier format |
| 5 | Domaine non ajouté | ⭐⭐ | Critique | `fly certs add` |
| 6 | Ordre incorrect | ⭐⭐ | Critique | Suivre l'ordre |
| 7 | CORS non configuré | ⭐⭐ | Moyen | Configurer CORS |
| 8 | Mauvaise app | ⭐ | Critique | Vérifier app |
| 9 | TTL trop élevé | ⭐ | Faible | Réduire TTL |
| 10 | Firewall/Proxy | ⭐ | Moyen | Vérifier réseau |

---

## 🎯 SOLUTION RAPIDE (Temporaire)

Si vous avez besoin que ça fonctionne **immédiatement** :

**Utiliser directement l'URL Fly.io** :
```env
NEXT_PUBLIC_API_URL=https://universal-api-hub.fly.dev
```

**Avantages** :
- ✅ Fonctionne immédiatement
- ✅ Pas de configuration DNS nécessaire
- ✅ SSL déjà configuré

**Inconvénients** :
- ⚠️ URL moins "propre"
- ⚠️ Solution temporaire

---

## 📚 RESSOURCES

- **Documentation Fly.io DNS** : https://fly.io/docs/app-guides/custom-domains-with-fly/
- **Documentation Fly.io SSL** : https://fly.io/docs/app-guides/custom-domains-with-fly/#adding-an-ssl-certificate
- **Vérificateur DNS** : https://dnschecker.org/
- **Test SSL** : https://www.ssllabs.com/ssltest/

---

**Dernière mise à jour** : Décembre 2024  
**Status** : ⚠️ Problèmes DNS identifiés - Solutions documentées

