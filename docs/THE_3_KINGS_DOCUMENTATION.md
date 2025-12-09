# 👑👑👑 THE 3 KINGS - Medical Search System Documentation

## Complete Guide for the World's Best Medical AI Searcher

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [The 3 Search Modes](#the-3-search-modes)
3. [API Registry (77 APIs)](#api-registry)
4. [Source Transparency](#source-transparency)
5. [Deep Research Reports](#deep-research-reports)
6. [API Endpoints](#api-endpoints)
7. [Deployment](#deployment)
8. [Testing](#testing)

---

## Overview

The **3 Kings Medical Search System** is the world's most comprehensive medical information retrieval system, featuring:

- **77 Medical APIs** from trusted institutions worldwide
- **3 Search Modes** optimized for different use cases
- **Intelligent Topic Detection** for smart routing
- **Full Source Transparency** for legal compliance
- **3000+ Word Research Reports** for academic use

### Countries Covered
🇺🇸 USA | 🇪🇺 Europe | 🇬🇧 UK | 🇫🇷 France | 🇨🇦 Canada | 🇯🇵 Japan | 🇮🇱 Israel | 🇪🇸 Spain | 🌍 International

---

## The 3 Search Modes

### ⚡ KING #1: FAST Mode

| Attribute | Value |
|-----------|-------|
| **Response Time** | < 100ms |
| **APIs Used** | 3 (local databases) |
| **Best For** | Real-time chat, instant responses |
| **Data Sources** | Local disease DB, DrugBank, LOINC |

```python
from services.medical_search_engine import fast_medical_search

result = await fast_medical_search("diabetes", "disease")
```

### 📊 KING #2: NORMAL (Standard) Mode

| Attribute | Value |
|-----------|-------|
| **Response Time** | 1-3 seconds |
| **APIs Used** | 6 (local + main APIs) |
| **Best For** | Standard queries, balanced speed/quality |
| **Data Sources** | Local + PubMed, FDA, RxNorm, Europe PMC |

```python
from services.medical_search_engine import standard_medical_search

result = await standard_medical_search("hypertension treatment", "disease")
```

### 🔬 KING #3: DEEP Mode

| Attribute | Value |
|-----------|-------|
| **Response Time** | 5-20 seconds |
| **APIs Used** | 10-22 (intelligent routing from 77) |
| **Best For** | Research, academic analysis, detailed reports |
| **Data Sources** | All 77 APIs with smart topic routing |
| **Output** | 3000+ word comprehensive report |

```python
from services.smart_medical_router import smart_medical_search
from services.deep_research_report import generate_deep_research_report

# Get data from smart router
context, result = await smart_medical_search("cancer du sein HER2")

# Generate 3000+ word report
report = await generate_deep_research_report("cancer du sein HER2", result)
```

---

## API Registry

### Complete List of 77 APIs

#### 📚 Scientific Literature (5 APIs)
| API | Organization | Country |
|-----|--------------|---------|
| PubMed / MEDLINE | NIH/NLM | 🇺🇸 USA |
| PubMed Central (PMC) | NIH | 🇺🇸 USA |
| Europe PMC | EMBL-EBI | 🇪🇺 Europe |
| Cochrane Library | Cochrane | 🌍 International |
| Semantic Scholar | Allen AI | 🇺🇸 USA |

#### 💊 Drug Databases (8 APIs)
| API | Organization | Country |
|-----|--------------|---------|
| OpenFDA | FDA | 🇺🇸 USA |
| RxNorm | NLM | 🇺🇸 USA |
| DailyMed | NIH/NLM | 🇺🇸 USA |
| DrugBank | U. Alberta | 🇨🇦 Canada |
| EMA | European Medicines Agency | 🇪🇺 Europe |
| ANSM | ANSM | 🇫🇷 France |
| ChEMBL | EMBL-EBI | 🇪🇺 Europe |
| DGIdb | Washington U. | 🇺🇸 USA |

#### 🏥 Clinical Guidelines (4 APIs)
| API | Organization | Country |
|-----|--------------|---------|
| NICE Guidelines | NICE | 🇬🇧 UK |
| HAS | Haute Autorité de Santé | 🇫🇷 France |
| CDC | Centers for Disease Control | 🇺🇸 USA |
| UpToDate | Wolters Kluwer | 🌍 International |

#### 🧬 Genomics & Genetics (7 APIs)
| API | Organization | Country |
|-----|--------------|---------|
| NCBI Gene | NIH | 🇺🇸 USA |
| OMIM | Johns Hopkins | 🇺🇸 USA |
| ClinVar | NIH | 🇺🇸 USA |
| gnomAD | Broad Institute | 🇺🇸 USA |
| Ensembl | EBI/Sanger | 🇪🇺 Europe |
| COSMIC | Sanger Institute | 🇬🇧 UK |
| PharmGKB | Stanford | 🇺🇸 USA |

#### 🦠 Disease Databases (5 APIs)
| API | Organization | Country |
|-----|--------------|---------|
| Orphanet | INSERM | 🇫🇷 France |
| GARD | NIH | 🇺🇸 USA |
| Disease Ontology | U. Maryland | 🇺🇸 USA |
| MalaCards | Weizmann Institute | 🇮🇱 Israel |
| DisGeNET | IMIM | 🇪🇸 Spain |

#### 🌍 Epidemiology (5 APIs)
| API | Organization | Country |
|-----|--------------|---------|
| WHO GHO | World Health Organization | 🌍 International |
| Disease.sh | Open Source | 🌍 International |
| ECDC | European CDC | 🇪🇺 Europe |
| GBD | IHME | 🇺🇸 USA |
| Santé Publique France | SPF | 🇫🇷 France |

#### 📋 Medical Terminology (6 APIs)
| API | Organization | Country |
|-----|--------------|---------|
| SNOMED CT | SNOMED International | 🌍 International |
| ICD-11 | WHO | 🌍 International |
| MeSH | NLM | 🇺🇸 USA |
| LOINC | Regenstrief | 🇺🇸 USA |
| UMLS | NLM | 🇺🇸 USA |
| ATC/DDD | WHO | 🌍 International |

#### 🔬 Clinical Trials (3 APIs)
| API | Organization | Country |
|-----|--------------|---------|
| ClinicalTrials.gov | NIH/NLM | 🇺🇸 USA |
| WHO ICTRP | WHO | 🌍 International |
| EU Clinical Trials Register | EMA | 🇪🇺 Europe |

#### 🔄 Biological Pathways (4 APIs)
| API | Organization | Country |
|-----|--------------|---------|
| KEGG | Kyoto University | 🇯🇵 Japan |
| Reactome | EMBL-EBI/OICR | 🌍 International |
| UniProt | UniProt Consortium | 🌍 International |
| STRING | EMBL | 🇪🇺 Europe |

#### 🥗 Nutrition (3 APIs)
| API | Organization | Country |
|-----|--------------|---------|
| USDA FoodData Central | USDA | 🇺🇸 USA |
| CIQUAL | ANSES | 🇫🇷 France |
| Open Food Facts | Open Source | 🌍 International |

---

## Source Transparency

### Why Source Transparency Matters

1. **Legal Compliance**: Clear attribution protects against plagiarism claims
2. **Academic Standards**: Students can cite original sources
3. **Trust Building**: Users can verify information
4. **Quality Assurance**: Official sources = reliable data

### How Sources Are Displayed

Every response includes:
- Name of the data source
- Organization responsible
- Country of origin
- Type of data provided
- Timestamp of retrieval

Example:
```
📚 SOURCES UTILISÉES:
├─ 📖 PubMed / NCBI (NIH, 🇺🇸 USA)
├─ 🇺🇸 OpenFDA (FDA, 🇺🇸 USA)
├─ 🇪🇺 Europe PMC (EMBL-EBI, 🇪🇺 Europe)
└─ 🔬 ClinicalTrials.gov (NIH, 🇺🇸 USA)
```

---

## Deep Research Reports

### Specifications

| Attribute | Requirement |
|-----------|-------------|
| **Minimum Length** | 3000 words |
| **Sections** | 7 mandatory sections |
| **AI Analysis** | Included |
| **Source Comparison** | Table format |
| **Confidence Score** | Calculated automatically |

### Report Structure

1. **📋 Introduction** - Query context, methodology, sources consulted
2. **📚 Literature Review** - PubMed, Europe PMC articles
3. **💊 Pharmacology** - Drug data, treatment comparison
4. **🔬 Clinical Trials** - Active trials, phases, status
5. **🌍 Epidemiology** - WHO data, prevalence, trends
6. **🧠 AI Analysis** - Synthesis, comparison table, confidence
7. **📝 Conclusion** - Recommendations, sources, disclaimer

### Usage

```python
from services.smart_medical_router import smart_medical_search
from services.deep_research_report import generate_deep_research_report
from services.ai_router import ai_router

# Step 1: Get medical data
context, search_result = await smart_medical_search(query)

# Step 2: Get AI analysis
ai_result = await ai_router.route(
    prompt=f"Analyze: {query}\n\nContext:\n{context}",
    system_prompt="You are a medical research analyst..."
)

# Step 3: Generate report
report = await generate_deep_research_report(
    query=query,
    search_result=search_result,
    ai_response=ai_result['response']
)

# report is now a 3000+ word markdown document
```

---

## API Endpoints

### Medical Search Endpoints

#### POST /api/medical/search
```json
{
  "query": "diabetes type 2 treatment",
  "mode": "deep",  // "fast", "normal", "deep"
  "language": "fr"
}
```

#### Response
```json
{
  "success": true,
  "mode": "deep",
  "query": "diabetes type 2 treatment",
  "topics_detected": ["diabetes", "drugs"],
  "apis_called": 10,
  "apis_with_data": 4,
  "sources": ["pubmed", "openfda", "europe_pmc", "clinical_trials"],
  "report": "# RAPPORT DE RECHERCHE...",
  "word_count": 3247,
  "processing_time_ms": 18532
}
```

### AI Chat with Medical Context

#### POST /api/chat
```json
{
  "message": "Quels sont les traitements du diabète de type 2?",
  "expert": "sante",
  "mode": "deep"
}
```

---

## Deployment

### Deploy to Fly.io

```powershell
# From project root
cd backend
flyctl deploy --remote-only
```

### Environment Variables Required

```env
# AI Providers
GROQ_API_KEY=your_key
MISTRAL_API_KEY=your_key
GEMINI_API_KEY=your_key
OPENROUTER_API_KEY=your_key

# Redis (for caching)
REDIS_URL=redis://...

# App
APP_URL=https://your-app.fly.dev
```

---

## Testing

### Run All Tests

```powershell
cd backend

# Test 3 Kings comparison
python test_search_modes.py

# Test with all 77 APIs
python test_3_kings_complete.py

# Quick summary test
python test_summary.py

# Medical system complete test
python test_medical_complete.py

# Smart router test
python test_mega_registry.py
```

### Web API Test

```powershell
# Test FAST mode
curl -X POST https://your-app.fly.dev/api/medical/search -d '{"query":"diabetes","mode":"fast"}'

# Test DEEP mode
curl -X POST https://your-app.fly.dev/api/medical/search -d '{"query":"cancer treatment","mode":"deep"}'
```

---

## Quick Reference

### Search Mode Selection Guide

| Use Case | Mode | Why |
|----------|------|-----|
| Real-time chat | ⚡ FAST | Instant response < 100ms |
| General questions | 📊 NORMAL | Balanced (1-3s) |
| Academic research | 🔬 DEEP | Comprehensive (5-20s) |
| Student projects | 🔬 DEEP | 3000+ word report |
| Legal/medical documentation | 🔬 DEEP | Full source transparency |

### Key Files

| File | Purpose |
|------|---------|
| `services/medical_search_engine.py` | FAST and NORMAL modes |
| `services/smart_medical_router.py` | Intelligent routing for DEEP |
| `services/deep_research_report.py` | 3000+ word report generator |
| `services/external_apis/medical_mega_registry.py` | 77 APIs registry |
| `services/external_apis/medical_ultimate.py` | Premium APIs |

---

## 📝 Summary

The **3 Kings Medical Search System** provides:

✅ **77 APIs** from trusted medical institutions  
✅ **3 Search Modes** (FAST, NORMAL, DEEP)  
✅ **Intelligent Topic Routing** (diabetes, cancer, genetics, etc.)  
✅ **Full Source Transparency** (legal compliance)  
✅ **3000+ Word Reports** (academic standard)  
✅ **AI-Powered Analysis** (synthesis and comparison)  
✅ **Global Coverage** (9+ countries)  

---

*Documentation last updated: 2024-12-09*
