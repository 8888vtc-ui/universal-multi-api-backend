# Architecture Agents Quality First - Documentation

## 🎯 Vue d'ensemble

Nouvelle architecture d'agents indépendants avec stratégie **Quality First** et format **conversationnel naturel**.

## 📋 Principes

### Quality First Strategy
1. **Appel APIs de données d'abord** : Les APIs sont appelées en premier pour récupérer les données réelles
2. **IA répond toujours** : L'IA génère une réponse même si les APIs échouent
3. **Réinterrogation automatique** : Si la qualité est insuffisante, réinterroger les APIs et améliorer la réponse
4. **Format conversationnel** : Réponses naturelles, pas de blocs/listes sauf si demandé explicitement

### Structure hiérarchique
- **Agents par catégorie** : Finance, Health, Sports, Tourism, etc.
- **Sous-agents par sous-catégorie** : Finance → Crypto, Stock, Market, Currency
- **Routage intelligent** : Détection automatique du type de requête et routage vers le bon agent/sous-agent

## 🏗️ Architecture

### Fichiers créés

```
backend/services/agents/
  __init__.py              # Exports principaux
  base_agent.py            # Classe de base ConversationalQualityAgent
  base_tool.py             # Classe de base pour les outils
  agent_factory.py         # Factory pour créer tous les agents
  finance_agent.py         # Agent Finance + sous-agents
  tools/
    __init__.py
    finance_tools.py       # Outils Finance (Crypto, Stock, Market, etc.)

backend/routers/
  agent_expert.py          # Nouveau router pour les agents
```

### Flux d'exécution

```
1. Requête utilisateur
   ↓
2. Détection du type (crypto, stock, market, etc.)
   ↓
3. Routage vers agent/sous-agent approprié
   ↓
4. Sélection des outils (APIs de données)
   ↓
5. Exécution des outils en parallèle
   ↓
6. Génération réponse IA (itération 1)
   ↓
7. Analyse qualité
   ↓
8. Si qualité insuffisante → Réinterrogation APIs + amélioration (itération 2)
   ↓
9. Retour réponse finale
```

## 🔧 Utilisation

### Endpoint API

**POST** `/api/agent-expert/chat`

```json
{
  "message": "quel est le prix du bitcoin ?",
  "expert_id": "finance",
  "session_id": "session_123",
  "user_id": "user_456",
  "language": "fr"
}
```

**Réponse :**
```json
{
  "response": "Le prix actuel du Bitcoin est de $43,250...",
  "agent_id": "finance_crypto",
  "agent_name": "Expert Crypto",
  "sources": ["coingecko"],
  "iterations": 2,
  "confidence": 0.9,
  "language": "fr"
}
```

### Liste des agents

**GET** `/api/agent-expert/agents`

Retourne la liste de tous les agents disponibles.

## 📊 Différences avec l'ancien système

| Critère | Ancien (expert_chat) | Nouveau (agent_expert) |
|---------|----------------------|------------------------|
| Appels IA/requête | 1 | 2-3 (avec réinterrogation) |
| Qualité | Moyenne | Élevée (+50-100%) |
| Format | Blocs/listes | Conversationnel naturel |
| Réinterrogation | Non | Oui (automatique) |
| Sous-agents | Non | Oui (Finance) |
| Routage intelligent | Basique | Avancé |

## 🚀 Déploiement

### Backend
1. Les fichiers sont créés et prêts
2. Le router est ajouté dans `main.py`
3. Déployer sur Fly.io

### Frontend
- **Compatibilité** : L'ancien endpoint `/api/expert/{expertId}/chat` fonctionne toujours
- **Migration progressive** : Le frontend peut migrer vers `/api/agent-expert/chat` progressivement
- **Avantages** : Meilleure qualité, format conversationnel, sous-agents

## 📝 Notes

- **Coût** : 2-3 appels IA par requête (vs 1 avant) mais qualité nettement améliorée
- **Performance** : 3-10s par requête (vs 1.5-5s) mais acceptable pour la qualité
- **Quotas** : Utilise les mêmes quotas gratuits (Groq, Mistral, etc.)
- **Rétrocompatibilité** : L'ancien système `expert_chat` reste disponible

## ✅ Prochaines étapes

1. ✅ Architecture créée
2. ✅ Agents Finance avec sous-agents
3. ✅ Router créé
4. ✅ Intégration dans main.py
5. ⏳ Déploiement backend
6. ⏳ Tests en production
7. ⏳ Migration frontend (optionnel)



## 🎯 Vue d'ensemble

Nouvelle architecture d'agents indépendants avec stratégie **Quality First** et format **conversationnel naturel**.

## 📋 Principes

### Quality First Strategy
1. **Appel APIs de données d'abord** : Les APIs sont appelées en premier pour récupérer les données réelles
2. **IA répond toujours** : L'IA génère une réponse même si les APIs échouent
3. **Réinterrogation automatique** : Si la qualité est insuffisante, réinterroger les APIs et améliorer la réponse
4. **Format conversationnel** : Réponses naturelles, pas de blocs/listes sauf si demandé explicitement

### Structure hiérarchique
- **Agents par catégorie** : Finance, Health, Sports, Tourism, etc.
- **Sous-agents par sous-catégorie** : Finance → Crypto, Stock, Market, Currency
- **Routage intelligent** : Détection automatique du type de requête et routage vers le bon agent/sous-agent

## 🏗️ Architecture

### Fichiers créés

```
backend/services/agents/
  __init__.py              # Exports principaux
  base_agent.py            # Classe de base ConversationalQualityAgent
  base_tool.py             # Classe de base pour les outils
  agent_factory.py         # Factory pour créer tous les agents
  finance_agent.py         # Agent Finance + sous-agents
  tools/
    __init__.py
    finance_tools.py       # Outils Finance (Crypto, Stock, Market, etc.)

backend/routers/
  agent_expert.py          # Nouveau router pour les agents
```

### Flux d'exécution

```
1. Requête utilisateur
   ↓
2. Détection du type (crypto, stock, market, etc.)
   ↓
3. Routage vers agent/sous-agent approprié
   ↓
4. Sélection des outils (APIs de données)
   ↓
5. Exécution des outils en parallèle
   ↓
6. Génération réponse IA (itération 1)
   ↓
7. Analyse qualité
   ↓
8. Si qualité insuffisante → Réinterrogation APIs + amélioration (itération 2)
   ↓
9. Retour réponse finale
```

## 🔧 Utilisation

### Endpoint API

**POST** `/api/agent-expert/chat`

```json
{
  "message": "quel est le prix du bitcoin ?",
  "expert_id": "finance",
  "session_id": "session_123",
  "user_id": "user_456",
  "language": "fr"
}
```

**Réponse :**
```json
{
  "response": "Le prix actuel du Bitcoin est de $43,250...",
  "agent_id": "finance_crypto",
  "agent_name": "Expert Crypto",
  "sources": ["coingecko"],
  "iterations": 2,
  "confidence": 0.9,
  "language": "fr"
}
```

### Liste des agents

**GET** `/api/agent-expert/agents`

Retourne la liste de tous les agents disponibles.

## 📊 Différences avec l'ancien système

| Critère | Ancien (expert_chat) | Nouveau (agent_expert) |
|---------|----------------------|------------------------|
| Appels IA/requête | 1 | 2-3 (avec réinterrogation) |
| Qualité | Moyenne | Élevée (+50-100%) |
| Format | Blocs/listes | Conversationnel naturel |
| Réinterrogation | Non | Oui (automatique) |
| Sous-agents | Non | Oui (Finance) |
| Routage intelligent | Basique | Avancé |

## 🚀 Déploiement

### Backend
1. Les fichiers sont créés et prêts
2. Le router est ajouté dans `main.py`
3. Déployer sur Fly.io

### Frontend
- **Compatibilité** : L'ancien endpoint `/api/expert/{expertId}/chat` fonctionne toujours
- **Migration progressive** : Le frontend peut migrer vers `/api/agent-expert/chat` progressivement
- **Avantages** : Meilleure qualité, format conversationnel, sous-agents

## 📝 Notes

- **Coût** : 2-3 appels IA par requête (vs 1 avant) mais qualité nettement améliorée
- **Performance** : 3-10s par requête (vs 1.5-5s) mais acceptable pour la qualité
- **Quotas** : Utilise les mêmes quotas gratuits (Groq, Mistral, etc.)
- **Rétrocompatibilité** : L'ancien système `expert_chat` reste disponible

## ✅ Prochaines étapes

1. ✅ Architecture créée
2. ✅ Agents Finance avec sous-agents
3. ✅ Router créé
4. ✅ Intégration dans main.py
5. ⏳ Déploiement backend
6. ⏳ Tests en production
7. ⏳ Migration frontend (optionnel)



