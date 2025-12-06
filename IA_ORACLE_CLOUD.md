# 🤖 Modèles IA sur Oracle Cloud - Guide Complet

**Question** : Peut-on lancer des IA comme DeepSeek avec le serveur Oracle Cloud gratuit ?

**Réponse** : **OUI, plusieurs options disponibles !**

---

## 🎯 Options Disponibles

### Option 1 : DeepSeek via Ollama (Local, Gratuit) ⭐

**Avantages** :
- ✅ **100% gratuit** - Pas besoin de clé API
- ✅ **Local** - Fonctionne sur le serveur
- ✅ **Sans limites** - Pas de quotas
- ✅ **Privé** - Données restent sur le serveur

**Modèles DeepSeek disponibles via Ollama** :
- `deepseek-r1:1.5b` - Modèle léger (1.5B paramètres)
- `deepseek-r1:7b` - Modèle moyen (7B paramètres)
- `deepseek-r1:14b` - Modèle complet (14B paramètres)
- `deepseek-coder` - Spécialisé code
- `deepseek-chat` - Modèle conversationnel

**Besoins en RAM** :
- deepseek-r1:1.5b : ~2GB RAM
- deepseek-r1:7b : ~6-8GB RAM
- deepseek-r1:14b : ~14-16GB RAM

**Oracle Cloud ARM** : ✅ Peut faire tourner jusqu'à deepseek-r1:14b
**Oracle Cloud x86** : ⚠️ Seulement deepseek-r1:1.5b

---

### Option 2 : DeepSeek via API (Nécessite Clé)

**Avantages** :
- ✅ Modèles plus récents
- ✅ Meilleure performance
- ✅ Pas de ressources serveur utilisées

**Limitations** :
- ⚠️ Nécessite clé API DeepSeek
- ⚠️ Quotas/limites selon le plan
- ⚠️ Coûts possibles

**Configuration** :
```env
DEEPSEEK_API_KEY=your-api-key-here
```

---

## 🚀 Installation DeepSeek via Ollama

### Sur Oracle Cloud ARM (Recommandé)

```bash
# 1. Installer Ollama
curl -fsSL https://ollama.com/install.sh | sh

# 2. Télécharger DeepSeek (modèle 7B recommandé)
ollama pull deepseek-r1:7b

# 3. Tester
ollama run deepseek-r1:7b "Hello, how are you?"

# 4. Configurer dans .env
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=deepseek-r1:7b
```

**Résultat** : ✅ **Totalement opérationnel**

### Sur Oracle Cloud x86 (Limité)

```bash
# 1. Installer Ollama
curl -fsSL https://ollama.com/install.sh | sh

# 2. Télécharger seulement le modèle léger
ollama pull deepseek-r1:1.5b

# 3. Configurer dans .env
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=deepseek-r1:1.5b
```

**Résultat** : ✅ **Opérationnel mais limité au modèle 1.5B**

---

## 📊 Modèles IA Disponibles via Ollama

### Modèles Conversationnels

| Modèle | RAM Requise | Oracle ARM | Oracle x86 |
|--------|-------------|------------|------------|
| **deepseek-r1:1.5b** | 2GB | ✅ OUI | ✅ OUI |
| **deepseek-r1:7b** | 6-8GB | ✅ OUI | ❌ NON |
| **deepseek-r1:14b** | 14-16GB | ✅ OUI | ❌ NON |
| **llama3.2:1b** | 1-2GB | ✅ OUI | ✅ OUI |
| **llama3.2:3b** | 3-4GB | ✅ OUI | ❌ NON |
| **llama3.1:8b** | 8-10GB | ✅ OUI | ❌ NON |
| **mistral** | 4-6GB | ✅ OUI | ❌ NON |
| **phi3** | 2-3GB | ✅ OUI | ✅ OUI |

### Modèles Spécialisés

- **deepseek-coder** : Spécialisé code (6-8GB RAM)
- **codellama** : Code Llama (6-8GB RAM)
- **starcoder** : Code StarCoder (8-10GB RAM)

---

## 🔧 Configuration Complète

### Configuration .env pour DeepSeek

```env
# Ollama (gratuit, local)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=deepseek-r1:7b

# Ou DeepSeek API (si vous avez une clé)
DEEPSEEK_API_KEY=your-api-key-here

# Autres providers (optionnel)
GROQ_API_KEY=your-key
MISTRAL_API_KEY=your-key
GEMINI_API_KEY=your-key
```

### Le Backend Utilisera Automatiquement

1. **Ollama (DeepSeek)** si configuré et disponible
2. **DeepSeek API** si clé API fournie
3. **Fallback** vers d'autres providers si nécessaire

---

## ✅ Test de DeepSeek

### Test via Ollama

```bash
# Tester directement
ollama run deepseek-r1:7b "Explique-moi l'intelligence artificielle"

# Tester via le backend
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Explique-moi l intelligence artificielle",
    "language": "fr"
  }'
```

### Vérifier les Modèles Disponibles

```bash
# Lister les modèles Ollama installés
ollama list

# Vérifier que DeepSeek est disponible
ollama list | grep deepseek
```

---

## 🎯 Recommandations par Cas d'Usage

### Pour le Développement/Test

**Oracle Cloud ARM + DeepSeek 7B** :
- ✅ Performance correcte
- ✅ Gratuit
- ✅ Suffisant pour tester

### Pour la Production (Test)

**Oracle Cloud ARM + DeepSeek 14B** :
- ✅ Meilleure qualité
- ✅ Gratuit
- ✅ Parfait pour valider

### Pour la Production (Finale)

**VPS Payant (Hetzner) + DeepSeek API** :
- ✅ Meilleure performance
- ✅ Modèles plus récents
- ✅ Pas de ressources serveur utilisées

---

## 📋 Checklist DeepSeek

### Installation
- [ ] Ollama installé sur le serveur
- [ ] DeepSeek téléchargé (deepseek-r1:7b recommandé)
- [ ] Ollama fonctionne (testé avec `ollama list`)

### Configuration
- [ ] .env configuré avec OLLAMA_BASE_URL
- [ ] .env configuré avec OLLAMA_MODEL=deepseek-r1:7b
- [ ] Backend redémarré

### Test
- [ ] DeepSeek répond via Ollama
- [ ] Backend utilise DeepSeek
- [ ] Chat fonctionne avec DeepSeek

---

## 🆚 Comparaison DeepSeek vs Autres

### DeepSeek vs Llama

| Aspect | DeepSeek | Llama |
|--------|----------|-------|
| **Performance** | ✅ Excellente | ✅ Très bonne |
| **Disponibilité Ollama** | ✅ OUI | ✅ OUI |
| **Modèles disponibles** | 1.5B, 7B, 14B | 1B, 3B, 7B, 8B |
| **Spécialisation code** | ✅ OUI (deepseek-coder) | ✅ OUI (codellama) |

### DeepSeek vs API Cloud

| Aspect | DeepSeek Ollama | DeepSeek API |
|--------|-----------------|--------------|
| **Coût** | ✅ Gratuit | ⚠️ Payant |
| **Performance** | ✅ Bonne | ✅ Excellente |
| **Ressources serveur** | ⚠️ Utilise RAM/CPU | ✅ Pas de ressources |
| **Limites** | ✅ Aucune | ⚠️ Quotas |

---

## 💡 Astuces

### Optimiser DeepSeek sur Oracle Cloud

```bash
# Utiliser le modèle adapté à la RAM disponible
# Oracle ARM (12GB RAM) : deepseek-r1:7b
# Oracle x86 (1GB RAM) : deepseek-r1:1.5b

# Limiter les ressources utilisées
export OLLAMA_NUM_GPU=0  # Pas de GPU
export OLLAMA_MAX_LOADED_MODELS=1  # Un seul modèle
```

### Utiliser Plusieurs Modèles

```bash
# Télécharger plusieurs modèles
ollama pull deepseek-r1:7b
ollama pull llama3.2:3b
ollama pull mistral

# Changer dans .env selon les besoins
OLLAMA_MODEL=deepseek-r1:7b  # Pour code
OLLAMA_MODEL=llama3.2:3b     # Pour conversation
```

---

## ✅ Réponse Finale

**OUI, vous pouvez lancer DeepSeek avec Oracle Cloud gratuit !**

### Oracle Cloud ARM
- ✅ **Totalement opérationnel**
- ✅ Peut faire tourner deepseek-r1:7b ou 14b
- ✅ Performance correcte
- ✅ Gratuit à vie

### Oracle Cloud x86
- ✅ **Opérationnel mais limité**
- ✅ Seulement deepseek-r1:1.5b
- ⚠️ Performance limitée

### Alternatives
- ✅ DeepSeek via API (si vous avez une clé)
- ✅ Autres modèles Ollama (Llama, Mistral, etc.)

---

## 🎯 Prochaines Étapes

1. **Créer instance Oracle Cloud ARM** (recommandé)
2. **Installer Ollama**
3. **Télécharger DeepSeek** : `ollama pull deepseek-r1:7b`
4. **Configurer .env** avec OLLAMA_MODEL=deepseek-r1:7b
5. **Tester** : Le backend utilisera automatiquement DeepSeek

---

**DeepSeek est totalement compatible avec Oracle Cloud gratuit ! 🚀**

*Dernière mise à jour : Décembre 2024*


