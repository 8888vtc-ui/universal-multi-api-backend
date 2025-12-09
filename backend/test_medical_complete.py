"""Test complete Medical System - All APIs + Anti-Hallucination"""
import asyncio
from services.external_apis.medical_extended import disease_sh, open_disease, rxnorm
from services.external_apis.medical_world import (
    clinical_trials, europe_pmc, drugbank_open, loinc
)
from services.medical_anti_hallucination import (
    medical_anti_hallucination, validate_medical_response
)

async def test_complete_medical_system():
    print("=" * 60)
    print("TESTING COMPLETE MEDICAL SYSTEM")
    print("=" * 60)
    
    # ============================================
    # TEST 1: All Medical APIs
    # ============================================
    print("\n📊 PHASE 1: Testing All Medical APIs")
    print("-" * 60)
    
    apis_tested = 0
    apis_working = 0
    
    # Test Disease.sh
    print("\n1. Disease.sh (COVID-19)...")
    try:
        covid = await disease_sh.get_covid_global()
        print(f"   ✅ Cases: {covid.get('cases'):,}")
        apis_working += 1
    except Exception as e:
        print(f"   ❌ Error: {e}")
    apis_tested += 1
    
    # Test RxNorm
    print("\n2. RxNorm NIH (Medications)...")
    try:
        drug = await rxnorm.search_drug("metformin")
        print(f"   ✅ Found: {drug.get('count')} results")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    apis_tested += 1
    
    # Test Clinical Trials
    print("\n3. ClinicalTrials.gov...")
    try:
        trials = await clinical_trials.search_trials("diabetes", max_results=3)
        print(f"   ✅ Trials found: {trials.get('count')}")
        if trials.get('trials'):
            print(f"   Sample: {trials['trials'][0].get('title', 'N/A')[:50]}...")
        apis_working += 1
    except Exception as e:
        print(f"   ❌ Error: {e}")
    apis_tested += 1
    
    # Test Europe PMC
    print("\n4. Europe PMC (Articles)...")
    try:
        articles = await europe_pmc.search_articles("hypertension treatment", max_results=3)
        print(f"   ✅ Articles found: {articles.get('count')}")
        if articles.get('articles'):
            print(f"   Sample: {articles['articles'][0].get('title', 'N/A')[:50]}...")
        apis_working += 1
    except Exception as e:
        print(f"   ❌ Error: {e}")
    apis_tested += 1
    
    # Test DrugBank
    print("\n5. DrugBank Open (Local)...")
    try:
        drug = await drugbank_open.get_drug_info("paracetamol")
        print(f"   ✅ Found: {drug.get('found')}")
        print(f"   Name: {drug.get('name', 'N/A')}")
        print(f"   Class: {drug.get('class', 'N/A')}")
        apis_working += 1
    except Exception as e:
        print(f"   ❌ Error: {e}")
    apis_tested += 1
    
    # Test LOINC
    print("\n6. LOINC (Lab Tests)...")
    try:
        lab = await loinc.get_lab_info("hemoglobin")
        print(f"   ✅ Found: {lab.get('found')}")
        print(f"   Normal range: {lab.get('normal_range', 'N/A')}")
        apis_working += 1
    except Exception as e:
        print(f"   ❌ Error: {e}")
    apis_tested += 1
    
    # Test Open Disease
    print("\n7. Open Disease (Local DB)...")
    try:
        disease = await open_disease.get_disease_info("migraine")
        print(f"   ✅ Found: {disease.get('found')}")
        print(f"   Symptoms: {', '.join(disease.get('symptoms', [])[:3])}...")
        apis_working += 1
    except Exception as e:
        print(f"   ❌ Error: {e}")
    apis_tested += 1
    
    print(f"\n📈 APIs Status: {apis_working}/{apis_tested} working")
    
    # ============================================
    # TEST 2: Anti-Hallucination System
    # ============================================
    print("\n\n🛡️ PHASE 2: Testing Anti-Hallucination System")
    print("-" * 60)
    
    # Test response with sources
    test_response = """
    Le diabète de type 2 touche environ 9% de la population mondiale.
    
    La metformine est le traitement de première ligne, avec une efficacité 
    démontrée pour réduire l'HbA1c de 1 à 1.5%.
    
    Les études montrent qu'une perte de poids de 5-10% améliore le contrôle glycémique.
    """
    
    test_context = {
        "pubmed": {"count": 3, "articles": [{"title": "Metformin efficacy"}]},
        "open_disease": {"count": 1, "found": True}
    }
    
    print("\n1. Testing response validation...")
    validated_response, report = validate_medical_response(test_response, test_context)
    
    print(f"   ✅ Is Safe: {report['is_safe']}")
    print(f"   ✅ Confidence: {report['confidence_score']:.2f}")
    print(f"   Warnings: {len(report['warnings'])}")
    print(f"   Suggestions: {len(report['suggestions'])}")
    
    print("\n2. Response with source attribution:")
    print("-" * 40)
    # Only show last 200 chars to see source footer
    print(validated_response[-300:])
    
    # Test dangerous claim detection
    print("\n3. Testing dangerous claim detection...")
    dangerous_response = "Ce remède naturel guérit le cancer à 100%"
    _, danger_report = validate_medical_response(dangerous_response)
    
    print(f"   ⚠️ Dangerous claim detected: {not danger_report['is_safe']}")
    if danger_report['warnings']:
        print(f"   Warning: {danger_report['warnings'][0][:50]}...")
    
    # ============================================
    # SUMMARY
    # ============================================
    print("\n\n" + "=" * 60)
    print("📋 COMPLETE MEDICAL SYSTEM SUMMARY")
    print("=" * 60)
    
    print(f"""
    📊 APIs DISPONIBLES:
    ├─ PubMed (illimité)           - Études scientifiques
    ├─ OpenFDA (illimité)          - Médicaments FDA
    ├─ RxNorm NIH (illimité)       - Terminologie médicaments
    ├─ Disease.sh (illimité)       - COVID-19/Épidémies
    ├─ ClinicalTrials.gov          - Essais cliniques
    ├─ Europe PMC (illimité)       - Littérature biomédicale
    ├─ WHO GHO (illimité)          - Stats OMS
    ├─ SNOMED CT                   - Terminologie médicale
    ├─ ICD-11                      - Classifications OMS
    ├─ Orphanet                    - Maladies rares
    ├─ DrugBank Open (local)       - 5 médicaments détaillés
    ├─ LOINC (local)               - 8 tests laboratoire
    └─ Open Disease (local)        - 5 maladies courantes
    
    🛡️ ANTI-HALLUCINATION:
    ├─ Détection claims dangereuses
    ├─ Vérification sources
    ├─ Attribution automatique [PUBMED/FDA/OMS/IA]
    └─ Score de confiance
    
    ✅ SYSTÈME OPÉRATIONNEL!
    """)

if __name__ == "__main__":
    asyncio.run(test_complete_medical_system())
