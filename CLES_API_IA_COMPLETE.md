# 🤖 Clés API IA - Configuration Complète

**Date** : Décembre 2024  
**Status** : ⚠️ Clés manquantes - À ajouter sur le serveur

---

## 📋 TOUTES LES CLÉS API IA À AJOUTER

### Configuration pour le fichier `.env` du serveur

```env
# ============================================
# 🤖 INTELLIGENCE ARTIFICIELLE - APIs
# ============================================

# Chat & LLM (Priorité 1 - Essentiel)
GROQ_API_KEY=votre_cle_groq
MISTRAL_API_KEY=votre_cle_mistral
GEMINI_API_KEY=votre_cle_gemini

# Chat & LLM (Priorité 2 - Recommandé)
OPENROUTER_API_KEY=votre_cle_openrouter
ANTHROPIC_API_KEY=votre_cle_anthropic
PERPLEXITY_API_KEY=votre_cle_perplexity
AI21_API_KEY=votre_cle_ai21

# Embeddings & Vectorisation
COHERE_API_KEY=votre_cle_cohere
HUGGINGFACE_API_TOKEN=votre_cle_huggingface

# Ollama (Local - Optionnel)
OLLAMA_BASE_URL=http://localhost:11434

# Anthropic Model (Optionnel)
ANTHROPIC_MODEL=claude-3-haiku-20240307

# Hugging Face Model (Optionnel)
HUGGINGFACE_MODEL=meta-llama/Llama-3-8B-Instruct
```

---

## 📊 DÉTAILS PAR PROVIDER

### 1. **Groq** ⭐ PRIORITÉ 1
- **Variable** : `GROQ_API_KEY`
- **Quota** : 14,400 requêtes/jour (gratuit)
- **Modèle** : `llama-3.3-70b-versatile`
- **Lien** : https://console.groq.com/
- **Status** : ✅ Intégré, nécessite clé

### 2. **Mistral AI** ⭐ PRIORITÉ 1
- **Variable** : `MISTRAL_API_KEY`
- **Quota** : 1 million tokens/mois (gratuit)
- **Modèle** : `mistral-small-latest`
- **Lien** : https://console.mistral.ai/
- **Status** : ✅ Intégré, nécessite clé

### 3. **Google Gemini** ⭐ PRIORITÉ 1
- **Variable** : `GEMINI_API_KEY`
- **Quota** : 1,500 requêtes/jour (gratuit)
- **Modèle** : `gemini-1.5-flash`
- **Lien** : https://makersuite.google.com/app/apikey
- **Status** : ✅ Intégré, nécessite clé

### 4. **OpenRouter** ⭐ PRIORITÉ 2
- **Variable** : `OPENROUTER_API_KEY`
- **Quota** : 50 requêtes/jour (gratuit)
- **Modèle** : `deepseek/deepseek-chat` + 67 autres modèles
- **Lien** : https://openrouter.ai/keys
- **Status** : ✅ Intégré, nécessite clé
- **Note** : Clé doit commencer par `sk-or-`

### 5. **Anthropic Claude** ⭐ PRIORITÉ 2
- **Variable** : `ANTHROPIC_API_KEY`
- **Quota** : 5$ crédit gratuit
- **Modèle** : `claude-3-haiku-20240307` (par défaut)
- **Variable Optionnelle** : `ANTHROPIC_MODEL`
- **Lien** : https://console.anthropic.com/
- **Status** : ✅ Intégré, nécessite clé

### 6. **Perplexity** ⭐ PRIORITÉ 2
- **Variable** : `PERPLEXITY_API_KEY`
- **Quota** : 5 requêtes/jour (gratuit, avec web search)
- **Modèle** : `sonar`
- **Lien** : https://www.perplexity.ai/settings/api
- **Status** : ✅ Intégré, nécessite clé

### 7. **AI21 Labs** ⭐ PRIORITÉ 2
- **Variable** : `AI21_API_KEY`
- **Quota** : 1,000 requêtes/jour (gratuit)
- **Modèle** : `j2-ultra`
- **Lien** : https://studio.ai21.com/
- **Status** : ✅ Intégré, nécessite clé

### 8. **Cohere** (Embeddings & Chat)
- **Variable** : `COHERE_API_KEY`
- **Quota** : 100 requêtes/jour (gratuit pour chat)
- **Modèle** : `command-r-plus`
- **Lien** : https://dashboard.cohere.com/
- **Status** : ✅ Intégré, nécessite clé

### 9. **Hugging Face**
- **Variable** : `HUGGINGFACE_API_TOKEN`
- **Quota** : Illimité (rate limit ~30 req/min)
- **Modèle** : `meta-llama/Llama-3-8B-Instruct` (par défaut)
- **Variable Optionnelle** : `HUGGINGFACE_MODEL`
- **Lien** : https://huggingface.co/settings/tokens
- **Status** : ✅ Intégré, nécessite clé

### 10. **Ollama** (Local)
- **Variable** : `OLLAMA_BASE_URL` (optionnel)
- **Valeur par défaut** : `http://localhost:11434`
- **Quota** : Illimité (local)
- **Status** : ✅ Intégré, fonctionne sans clé si Ollama installé localement

---

## 🔗 LIENS POUR OBTENIR LES CLÉS

### Priorité 1 (Minimum pour fonctionner)
1. **Groq** : https://console.groq.com/
2. **Mistral AI** : https://console.mistral.ai/
3. **Google Gemini** : https://makersuite.google.com/app/apikey

### Priorité 2 (Recommandé)
4. **OpenRouter** : https://openrouter.ai/keys
5. **Anthropic** : https://console.anthropic.com/
6. **Perplexity** : https://www.perplexity.ai/settings/api
7. **AI21** : https://studio.ai21.com/

### Embeddings
8. **Cohere** : https://dashboard.cohere.com/
9. **Hugging Face** : https://huggingface.co/settings/tokens

---

## 📊 PRIORITÉS RECOMMANDÉES

### Minimum (1 clé suffit)
- **Groq** ⭐ (14,400/jour - le plus généreux)

### Recommandé (3 clés)
- **Groq** ⭐
- **Mistral AI** ⭐ (1M tokens/mois)
- **Google Gemini** ⭐ (1,500/jour)

### Optimal (Toutes les clés)
- Toutes les 9 clés configurées = **~18,000+ requêtes/jour**

---

## ⚠️ IMPORTANT

### Ollama (Local)
- **Fonctionne sans clé** si Ollama est installé localement
- Variable `OLLAMA_BASE_URL` optionnelle (défaut : `http://localhost:11434`)
- **Illimité** mais nécessite installation locale

### Hugging Face
- Variable : `HUGGINGFACE_API_TOKEN` (pas `HUGGINGFACE_API_KEY`)
- Variable optionnelle : `HUGGINGFACE_MODEL` pour changer le modèle

### OpenRouter
- Clé doit commencer par `sk-or-`
- Accès à 67+ modèles différents

---

## 📝 CONFIGURATION MINIMALE POUR DÉMARRER

Si vous voulez démarrer rapidement avec **1 seule clé** :

```env
# Minimum requis (1 clé)
GROQ_API_KEY=votre_cle_groq
```

Cela donne **14,400 requêtes/jour** gratuitement.

---

## 📈 QUOTAS TOTAUX (si toutes configurées)

- **Quota journalier** : ~18,000+ requêtes/jour
- **Quota mensuel** : 1M+ tokens (Mistral)
- **Illimité** : Hugging Face (rate limit), Ollama (local)

---

## ✅ CHECKLIST

- [ ] Obtenir clé Groq (priorité 1)
- [ ] Obtenir clé Mistral (priorité 1)
- [ ] Obtenir clé Gemini (priorité 1)
- [ ] Obtenir clé OpenRouter (priorité 2)
- [ ] Obtenir clé Anthropic (priorité 2)
- [ ] Obtenir clé Perplexity (priorité 2)
- [ ] Obtenir clé AI21 (priorité 2)
- [ ] Obtenir clé Cohere (embeddings)
- [ ] Obtenir token Hugging Face (embeddings)
- [ ] Configurer Ollama (optionnel, local)

---

**Total Clés IA** : **9 clés API** (Ollama optionnel, fonctionne sans clé)

**Dernière mise à jour** : Décembre 2024

