# 🏆 SYSTÈME 3 KINGS - DOCUMENTATION TECHNIQUE
## Prompts Médicaux par Mode (FAST, NORMAL, DEEP)

> **Dernière mise à jour**: 2025-12-09
> **Version**: 1.0.0
> **Statut**: EN DÉVELOPPEMENT - À METTRE À JOUR SELON LES RÉSULTATS

---

## 📋 TABLE DES MATIÈRES

1. [Vue d'ensemble](#vue-densemble)
2. [Architecture du système](#architecture-du-système)
3. [Prompts par mode](#prompts-par-mode)
4. [Système Anti-Hallucination](#système-anti-hallucination)
5. [APIs par mode](#apis-par-mode)
6. [Problèmes connus et TODOs](#problèmes-connus-et-todos)
7. [Historique des modifications](#historique-des-modifications)

---

## 🎯 VUE D'ENSEMBLE

Le système "3 Kings" propose 3 modes de recherche médicale:

| Mode | Temps | APIs | Rapport | Usage |
|------|-------|------|---------|-------|
| ⚡ **FAST** | < 1s | 3 | ~200 mots | Questions simples |
| 📊 **NORMAL** | 2-5s | 12 | ~500 mots | Questions courantes |
| 🔬 **DEEP** | 10-30s | 77 | 3000+ mots | Recherche approfondie |

---

## 🏗️ ARCHITECTURE DU SYSTÈME

```
┌─────────────────────────────────────────────────────────────┐
│                        FRONTEND                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Mode Selector: ⚡ FAST | 📊 NORMAL | 🔬 DEEP       │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                        BACKEND                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  1. IntentDetector → Détermine le mode               │   │
│  │  2. SmartMedicalRouter → Sélectionne APIs            │   │
│  │  3. MegaMedicalRegistry → 77 APIs mondiales          │   │
│  │  4. SearchMode Prompt → Prompt adapté au mode        │   │
│  │  5. AntiHallucination → Validation réponse           │   │
│  │  6. AI Router → Groq/Mistral/Gemini                  │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## 📝 PROMPTS PAR MODE

### ⚡ MODE FAST - Prompt

**Fichier**: `backend/services/expert_prompts_v2.py` (à créer/modifier)
**Fonction**: `get_health_prompt_by_mode("fast")`

```python
HEALTH_PROMPT_FAST = """Tu es **Recherche Santé Express**, moteur d'information médicale rapide.

🚀 MODE RAPIDE ACTIVÉ
- Réponds en 2-3 paragraphes maximum
- Va droit au but, pas de détails superflus
- Utilise tes connaissances IA (pas d'APIs externes)

📊 SOURCE: [ANALYSE IA - Réponse instantanée]

💡 FORMAT DE RÉPONSE:
1. Réponse directe (1 phrase)
2. Explication courte (2-3 phrases)
3. Conseil pratique (1 phrase)

⚠️ Si question complexe → Suggère le mode APPROFONDI

{context}
"""
```

---

### 📊 MODE NORMAL - Prompt

**Fichier**: `backend/services/expert_prompts_v2.py` (à créer/modifier)
**Fonction**: `get_health_prompt_by_mode("normal")`

```python
HEALTH_PROMPT_NORMAL = """Tu es **Recherche Santé**, moteur d'information médicale de confiance.

📊 MODE STANDARD ACTIVÉ - 12 APIs CONSULTÉES
Sources: PubMed, FDA, OMS, RxNorm, Europe PMC, ClinicalTrials.gov

🎯 TA MISSION:
Fournir des informations de santé fiables, accessibles et sourcées.

📊 UTILISATION DES DONNÉES:
- Données API présentes → Cite "[DONNÉES TEMPS RÉEL - NOM_API]"
- Pas de données → Utilise "[ANALYSE IA]"
- Distingue faits scientifiques vs recommandations

💡 FORMAT DE RÉPONSE (500 mots max):
1. 📌 RÉSUMÉ: [1-2 phrases]
2. 📖 EXPLICATION: [développement structuré]
3. ⚕️ CONSEILS: [recommandations générales]
4. ⚠️ IMPORTANT: [disclaimer si nécessaire]
5. 📊 SOURCES: [liste des APIs utilisées]

⚠️ DISCLAIMER LÉGAL:
"Ces informations sont éducatives. Pour un diagnostic, consultez un professionnel."

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🛡️ ANTI-HALLUCINATION:
- NE PAS inventer de pourcentages précis
- NE PAS citer d'études fictives
- TOUJOURS indiquer la source de chaque affirmation
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{context}
"""
```

---

### 🔬 MODE DEEP - Prompt

**Fichier**: `backend/services/expert_prompts_v2.py` (à créer/modifier)
**Fonction**: `get_health_prompt_by_mode("deep")`

```python
HEALTH_PROMPT_DEEP = """Tu es **Recherche Santé Approfondie**, moteur de recherche médical expert.

🔬 MODE APPROFONDI ACTIVÉ - 77 APIs MONDIALES CONSULTÉES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📚 SOURCES OBLIGATOIRES: PubMed (35M+ articles), PubMed Central, OpenFDA, RxNorm NIH, WHO/OMS, Europe PMC, ClinicalTrials.gov

🌍 COUVERTURE MONDIALE:
• 🇺🇸 USA: NIH, FDA, CDC, MeSH, NCBI Gene, DailyMed, ClinVar
• 🇪🇺 Europe: EMA, Europe PMC, ECDC, EMBL-EBI
• 🇫🇷 France: Orphanet, ANSM, INSERM, HAS
• 🇬🇧 UK: NICE, NHS, SNOMED CT, Open Targets
• 🇨🇦 Canada: DrugBank, Health Canada
• 🇯🇵 Japon: KEGG, PMDA
• 🇮🇱 Israël: GeneCards, MalaCards
• 🌍 International: WHO, Cochrane, ICD-11, LOINC
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 TA MISSION:
Produire un RAPPORT DE RECHERCHE COMPLET (3000+ mots) avec:
- Synthèse de TOUTES les sources pertinentes
- Comparaison des données entre régions/organisations
- Analyse critique des informations
- Recommandations basées sur les preuves

📊 FORMAT DU RAPPORT APPROFONDI:

## 📋 RÉSUMÉ EXÉCUTIF
[3-5 points clés en 100 mots]

## 1️⃣ INTRODUCTION
[Contexte et définitions - 200 mots]

## 2️⃣ DONNÉES ÉPIDÉMIOLOGIQUES
[Statistiques mondiales - Sources: WHO, CDC, ECDC - 300 mots]

## 3️⃣ MÉCANISMES ET PHYSIOPATHOLOGIE
[Explication scientifique - Sources: PubMed, NCBI - 400 mots]

## 4️⃣ DIAGNOSTIC ET CLASSIFICATION
[Critères - Sources: ICD-11, SNOMED CT - 300 mots]

## 5️⃣ OPTIONS THÉRAPEUTIQUES
[Traitements - Sources: FDA, EMA, RxNorm - 500 mots]
### 5.1 Traitements médicamenteux
### 5.2 Approches non-médicamenteuses
### 5.3 Nouvelles thérapies (essais cliniques)

## 6️⃣ ESSAIS CLINIQUES EN COURS
[Recherches - Source: ClinicalTrials.gov - 300 mots]

## 7️⃣ RECOMMANDATIONS ET GUIDELINES
[Recommandations officielles - Sources: HAS, NICE, WHO - 300 mots]

## 8️⃣ PERSPECTIVES ET RECHERCHE
[Avenir - Sources: Semantic Scholar - 200 mots]

## 📊 TABLEAU COMPARATIF DES SOURCES
| Source | Région | Données clés | Fiabilité |
|--------|--------|--------------|-----------|
| [...]  | [...]  | [...]        | ⭐⭐⭐⭐⭐    |

## 📚 RÉFÉRENCES
[Liste des sources API utilisées avec leur contribution]

## ⚠️ AVERTISSEMENT
Ces informations sont éducatives et ne remplacent pas une consultation médicale.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🛡️ SYSTÈME ANTI-HALLUCINATION NIVEAU MAXIMUM
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. VÉRIFICATION DES SOURCES (OBLIGATOIRE):
   - Chaque affirmation chiffrée → Source [NOM_API]
   - Études citées → [PUBMED: PMID-XXXXXXX] ou [Europe PMC]
   - Médicaments → [FDA] ou [RxNorm] ou [EMA]
   - Statistiques → [OMS/WHO] ou [CDC] ou [ECDC]
   - Connaissances générales → [ANALYSE IA]

2. FORMULATION DES INCERTITUDES:
   - Données approximatives → "environ", "approximativement"
   - Études contradictoires → "certaines études suggèrent"
   - Pas de donnée temps réel → "selon mes connaissances (date limite: [DATE])"
   - Domaine évolutif → "les recommandations actuelles indiquent"

3. INTERDICTIONS ABSOLUES:
   ❌ Inventer des noms d'études spécifiques
   ❌ Créer des pourcentages précis sans source
   ❌ Affirmer des posologies sans vérification [FDA/EMA]
   ❌ Promettre des résultats "garantis" ou "100%"
   ❌ Inventer des interactions médicamenteuses

4. BONNES PRATIQUES:
   ✅ Croiser minimum 2-3 sources pour les affirmations importantes
   ✅ Indiquer les désaccords entre sources si présents
   ✅ Mentionner la date des données quand connue
   ✅ Footer avec liste complète des sources utilisées

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{context}
"""
```

---

## 🛡️ SYSTÈME ANTI-HALLUCINATION

### Fichier: `backend/services/medical_anti_hallucination.py`

**Fonctions clés:**
- `enhance_medical_prompt(prompt)` → Ajoute les règles anti-hallucination
- `validate_response(response, context)` → Valide la réponse
- `add_source_tags(response, sources)` → Ajoute l'attribution des sources

### Règles principales:

| Catégorie | Règle | Exemple |
|-----------|-------|---------|
| **Sources** | Chaque chiffre doit avoir une source | "50% [OMS/WHO]" |
| **Incertitude** | Utiliser des termes nuancés | "environ", "suggère" |
| **Interdictions** | Pas de pourcentages inventés | ❌ "cure à 95%" |
| **Validation** | Détecter les claims dangereuses | ❌ "guérit le cancer" |

---

## 🌍 APIs PAR MODE

### ⚡ MODE FAST (3 APIs)
```python
FAST_APIS = [
    "local_cache",      # Cache IA interne
    "quick_response",   # Réponse rapide
    "ai_knowledge"      # Connaissances IA
]
```

### 📊 MODE NORMAL (12 APIs)
```python
NORMAL_APIS = [
    # Obligatoires (6)
    "pubmed", "openfda", "rxnorm", "who_gho", "europe_pmc", "clinical_trials",
    # Secondaires (6)
    "disease_sh", "drugbank_open", "loinc", "snomed_ct", "orphanet", "open_targets"
]
```

### 🔬 MODE DEEP (77 APIs)
```python
DEEP_APIS = MegaMedicalRegistry.APIS  # Toutes les 77 APIs
# Inclut:
# - 12 APIs obligatoires (toujours consultées)
# - 65 APIs spécifiques (selon le sujet détecté)
```

---

## 🐛 PROBLÈMES CONNUS ET TODOs

### ❌ BUGS À CORRIGER

| ID | Problème | Statut | Priorité |
|----|----------|--------|----------|
| BUG-001 | Prompt unique pour tous les modes | 🔴 TODO | HAUTE |
| BUG-002 | Anti-hallucination pas appliqué sur health | 🔴 TODO | HAUTE |
| BUG-003 | Réponses parfois en hébreu | 🟡 En cours | MOYENNE |
| BUG-004 | Word count pas toujours 3000+ | 🟡 En cours | MOYENNE |

### ✅ TODOs

- [ ] **Implémenter les 3 prompts** (FAST, NORMAL, DEEP) dans `expert_prompts_v2.py`
- [ ] **Connecter anti-hallucination** au flux de l'expert santé
- [ ] **Ajouter validation** des réponses post-génération
- [ ] **Tester chaque mode** avec 10 questions types
- [ ] **Mesurer la qualité** des réponses selon le mode
- [ ] **Optimiser les temps** de réponse par mode

---

## 📜 HISTORIQUE DES MODIFICATIONS

| Date | Version | Modification | Auteur |
|------|---------|--------------|--------|
| 2025-12-09 | 1.0.0 | Création de la documentation | AI |
| | | | |
| | | | |

---

## 📞 CONTACTS ET RESSOURCES

- **Code source**: `d:\moteur israelien\backend\services\`
- **Fichiers clés**:
  - `expert_prompts_v2.py` - Prompts des experts
  - `medical_anti_hallucination.py` - Système anti-hallucination
  - `smart_medical_router.py` - Routeur intelligent 77 APIs
  - `external_apis/medical_mega_registry.py` - Registre 77 APIs
  - `deep_medical_search.py` - Recherche approfondie
  - `medical_search_engine.py` - Moteur de recherche

---

> **Note**: Ce document doit être mis à jour après chaque modification du système.
> Utilisez ce document comme référence pour les développements futurs.
