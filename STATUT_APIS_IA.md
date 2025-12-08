# 🤖 Statut des APIs IA Disponibles

## 📊 Total : 10 Providers IA Intégrés

### ✅ Providers Disponibles (selon configuration)

| # | Provider | Quota Gratuit | Priorité | Status |
|---|----------|---------------|----------|--------|
| 1 | **Groq** | 14,400/jour | 1 | ✅ Intégré |
| 2 | **Mistral AI** | 1M tokens/mois | 2 | ✅ Intégré |
| 3 | **Anthropic (Claude)** | 5$ crédit | 3 | ✅ Intégré |
| 4 | **Cohere Chat** | 100/jour | 4 | ✅ Intégré |
| 5 | **AI21 Labs** | 1,000/jour | 5 | ✅ Intégré |
| 6 | **Google Gemini** | 1,500/jour | 6 | ✅ Intégré |
| 7 | **Perplexity** | 5/jour (web search) | 7 | ✅ Intégré |
| 8 | **Hugging Face** | Illimité (rate limit) | 8 | ✅ Intégré |
| 9 | **OpenRouter** | 50/jour (DeepSeek) | 9 | ✅ Intégré |
| 10 | **Ollama** | Illimité (local) | 10 | ✅ Intégré |

---

## 🔧 Configuration Requise

Chaque provider nécessite une clé API dans `backend/.env` :

```env
# Providers IA
GROQ_API_KEY=votre_cle_groq
MISTRAL_API_KEY=votre_cle_mistral
ANTHROPIC_API_KEY=votre_cle_anthropic
COHERE_API_KEY=votre_cle_cohere
AI21_API_KEY=votre_cle_ai21
GEMINI_API_KEY=votre_cle_gemini
PERPLEXITY_API_KEY=votre_cle_perplexity
HUGGINGFACE_API_KEY=votre_cle_huggingface
OPENROUTER_API_KEY=votre_cle_openrouter
OLLAMA_BASE_URL=http://localhost:11434  # Pour Ollama local
```

---

## 📈 Quotas Totaux (si tous configurés)

- **Quota journalier** : ~18,000+ requêtes/jour
- **Quota mensuel** : 1M+ tokens (Mistral)
- **Illimité** : Hugging Face (rate limit), Ollama (local)

---

## 🎯 Fonctionnement

Le système utilise un **router intelligent** qui :
1. Essaie les providers par ordre de priorité
2. Vérifie les quotas disponibles
3. Fait un fallback automatique si un provider échoue
4. Utilise le circuit breaker pour éviter les providers en panne

---

## ⚠️ Status Actuel

**Groq** : ✅ Modèle mis à jour (`llama-3.1-70b-versatile`)
- Ancien modèle `llama3-70b-8192` décommissionné
- Nouveau modèle actif et fonctionnel

**Autres providers** : Dépendent de la configuration des clés API

---

**Date** : 07/12/2025  
**Total** : 10 providers IA intégrés



## 📊 Total : 10 Providers IA Intégrés

### ✅ Providers Disponibles (selon configuration)

| # | Provider | Quota Gratuit | Priorité | Status |
|---|----------|---------------|----------|--------|
| 1 | **Groq** | 14,400/jour | 1 | ✅ Intégré |
| 2 | **Mistral AI** | 1M tokens/mois | 2 | ✅ Intégré |
| 3 | **Anthropic (Claude)** | 5$ crédit | 3 | ✅ Intégré |
| 4 | **Cohere Chat** | 100/jour | 4 | ✅ Intégré |
| 5 | **AI21 Labs** | 1,000/jour | 5 | ✅ Intégré |
| 6 | **Google Gemini** | 1,500/jour | 6 | ✅ Intégré |
| 7 | **Perplexity** | 5/jour (web search) | 7 | ✅ Intégré |
| 8 | **Hugging Face** | Illimité (rate limit) | 8 | ✅ Intégré |
| 9 | **OpenRouter** | 50/jour (DeepSeek) | 9 | ✅ Intégré |
| 10 | **Ollama** | Illimité (local) | 10 | ✅ Intégré |

---

## 🔧 Configuration Requise

Chaque provider nécessite une clé API dans `backend/.env` :

```env
# Providers IA
GROQ_API_KEY=votre_cle_groq
MISTRAL_API_KEY=votre_cle_mistral
ANTHROPIC_API_KEY=votre_cle_anthropic
COHERE_API_KEY=votre_cle_cohere
AI21_API_KEY=votre_cle_ai21
GEMINI_API_KEY=votre_cle_gemini
PERPLEXITY_API_KEY=votre_cle_perplexity
HUGGINGFACE_API_KEY=votre_cle_huggingface
OPENROUTER_API_KEY=votre_cle_openrouter
OLLAMA_BASE_URL=http://localhost:11434  # Pour Ollama local
```

---

## 📈 Quotas Totaux (si tous configurés)

- **Quota journalier** : ~18,000+ requêtes/jour
- **Quota mensuel** : 1M+ tokens (Mistral)
- **Illimité** : Hugging Face (rate limit), Ollama (local)

---

## 🎯 Fonctionnement

Le système utilise un **router intelligent** qui :
1. Essaie les providers par ordre de priorité
2. Vérifie les quotas disponibles
3. Fait un fallback automatique si un provider échoue
4. Utilise le circuit breaker pour éviter les providers en panne

---

## ⚠️ Status Actuel

**Groq** : ✅ Modèle mis à jour (`llama-3.1-70b-versatile`)
- Ancien modèle `llama3-70b-8192` décommissionné
- Nouveau modèle actif et fonctionnel

**Autres providers** : Dépendent de la configuration des clés API

---

**Date** : 07/12/2025  
**Total** : 10 providers IA intégrés



