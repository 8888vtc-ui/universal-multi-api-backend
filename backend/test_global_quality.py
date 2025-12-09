"""
GLOBAL QUALITY TEST - World's Best Medical Search Engine
Tests ALL aspects until 100% quality is achieved
"""
import httpx
import asyncio
import time
import re
import sys
import io
from typing import Dict, List, Any

# Force UTF-8 output
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Production server
BASE_URL = "https://universal-api-hub.fly.dev"


class QualityChecker:
    """Comprehensive quality checking for medical responses"""
    
    @staticmethod
    def check_structure(text: str) -> Dict[str, Any]:
        """Check if response has proper structure"""
        checks = {
            "has_headers": bool(re.search(r'##\s+', text) or re.search(r'\*\*[A-Z]', text)),
            "has_lists": bool(re.search(r'^[-*]\s', text, re.MULTILINE)),
            "has_sections": len(re.findall(r'##|###', text)) >= 3,
            "proper_length": len(text) > 1000,
            "has_formatting": bool(re.search(r'\*\*|\#\#|\|', text))
        }
        score = sum(checks.values()) / len(checks) * 100
        return {"checks": checks, "score": score}
    
    @staticmethod
    def check_sources(text: str) -> Dict[str, Any]:
        """Check if sources are properly cited"""
        source_patterns = [
            r'\[PUBMED\]', r'\[FDA\]', r'\[OMS\]', r'\[WHO\]',
            r'\[ANALYSE IA\]', r'\[Source:', r'Source:',
            r'PubMed', r'FDA', r'OMS',
            r'\[HAS\]', r'\[NICE\]', r'\[KEGG\]'
        ]
        
        found_sources = []
        for pattern in source_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                found_sources.append(pattern.replace('\\', '').replace('[', '').replace(']', ''))
        
        has_sources_section = bool(re.search(r'SOURCES|Sources consult', text, re.IGNORECASE))
        
        return {
            "sources_found": found_sources,
            "count": len(found_sources),
            "has_sources_section": has_sources_section,
            "score": min(100, len(found_sources) * 15 + (30 if has_sources_section else 0))
        }
    
    @staticmethod
    def check_disclaimer(text: str) -> Dict[str, Any]:
        """Check for medical disclaimer"""
        patterns = [
            r'consultez.*m.decin',
            r'professionnel.*sant',
            r'avertissement',
            r'titre.*ducatif',
            r'ne.*remplace.*consultation',
            r'AVERTISSEMENT',
            r'DISCLAIMER'
        ]
        
        found = False
        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                found = True
                break
        
        return {"present": found, "score": 100 if found else 0}
    
    @staticmethod
    def check_data_quality(text: str) -> Dict[str, Any]:
        """Check for numerical data and statistics"""
        checks = {
            "has_percentages": bool(re.search(r'\d+\s*%', text)),
            "has_numbers": bool(re.search(r'\d+', text)),
            "has_statistics": bool(re.search(r'pr.valence|incidence|millions?|milliards?', text, re.IGNORECASE)),
            "has_comparisons": bool(re.search(r'comparaison|versus|vs\.?|contre', text, re.IGNORECASE)),
            "has_tables": bool(re.search(r'\|.*\|.*\|', text))
        }
        score = sum(checks.values()) / len(checks) * 100
        return {"checks": checks, "score": score}
    
    @staticmethod
    def check_research_log(text: str) -> Dict[str, Any]:
        """Check if research log is displayed"""
        patterns = [
            r'APIs?.*consult',
            r'RECHERCHE.*EFFECTU',
            r'Phase\s*\d',
            r'temps.*total.*\d+',
            r'sources.*consult'
        ]
        
        found = sum(1 for p in patterns if re.search(p, text, re.IGNORECASE))
        return {"patterns_found": found, "score": min(100, found * 25)}
    
    @staticmethod
    def check_analysis(text: str) -> Dict[str, Any]:
        """Check for AI analysis section"""
        patterns = [
            r'ANALYSE.*IA',
            r'synth.se',
            r'points.*cl.s',
            r'perspective',
            r'en r.sum.'
        ]
        
        found = sum(1 for p in patterns if re.search(p, text, re.IGNORECASE))
        return {"patterns_found": found, "score": min(100, found * 25)}
    
    @classmethod
    def full_quality_check(cls, text: str, mode: str = "long") -> Dict[str, Any]:
        """Complete quality assessment"""
        structure = cls.check_structure(text)
        sources = cls.check_sources(text)
        disclaimer = cls.check_disclaimer(text)
        data = cls.check_data_quality(text)
        research_log = cls.check_research_log(text)
        analysis = cls.check_analysis(text)
        
        if mode == "long":
            weights = {
                "structure": 0.15,
                "sources": 0.20,
                "disclaimer": 0.15,
                "data": 0.15,
                "research_log": 0.20,
                "analysis": 0.15
            }
        else:
            weights = {
                "structure": 0.30,
                "sources": 0.10,
                "disclaimer": 0.30,
                "data": 0.10,
                "research_log": 0.05,
                "analysis": 0.15
            }
        
        total_score = (
            structure["score"] * weights["structure"] +
            sources["score"] * weights["sources"] +
            disclaimer["score"] * weights["disclaimer"] +
            data["score"] * weights["data"] +
            research_log["score"] * weights["research_log"] +
            analysis["score"] * weights["analysis"]
        )
        
        return {
            "total_score": round(total_score, 1),
            "structure": structure,
            "sources": sources,
            "disclaimer": disclaimer,
            "data_quality": data,
            "research_log": research_log,
            "analysis": analysis,
            "grade": "A+" if total_score >= 95 else "A" if total_score >= 85 else "B" if total_score >= 70 else "C" if total_score >= 50 else "F"
        }


async def test_query(query: str, mode: str = "long") -> Dict[str, Any]:
    """Test a single query"""
    start = time.time()
    
    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                f"{BASE_URL}/api/experts/chat",
                json={
                    "expert_id": "HEALTH",
                    "message": query,
                    "conversation_id": f"quality_test_{int(time.time())}"
                }
            )
            
            if response.status_code != 200:
                return {"error": f"HTTP {response.status_code}", "query": query}
            
            data = response.json()
            text = data.get("response", "")
            elapsed = (time.time() - start) * 1000
            
            quality = QualityChecker.full_quality_check(text, mode)
            
            return {
                "query": query[:50] + "..." if len(query) > 50 else query,
                "mode": mode,
                "response_length": len(text),
                "time_ms": round(elapsed),
                "quality": quality,
                "response_preview": text[:500] + "..." if len(text) > 500 else text
            }
            
    except Exception as e:
        return {"error": str(e), "query": query}


async def run_global_tests():
    """Run comprehensive tests"""
    print("=" * 80)
    print("TEST GLOBAL QUALITE - MEILLEUR MOTEUR MEDICAL DU MONDE")
    print("=" * 80)
    print()
    
    # Check server health
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            health = await client.get(f"{BASE_URL}/api/health")
            if health.status_code == 200:
                print("[OK] Serveur accessible")
            else:
                print("[ERREUR] Serveur inaccessible")
                return
    except Exception as e:
        print(f"[ERREUR] Connexion: {e}")
        return
    
    # Test cases by mode
    test_cases = [
        # MODE FAST
        ("Bonjour", "fast"),
        ("Merci beaucoup", "fast"),
        ("C'est quoi un rhume ?", "fast"),
        
        # MODE STANDARD  
        ("Quels sont les symptomes du diabete type 2 ?", "standard"),
        ("Comment fonctionne le paracetamol ?", "standard"),
        ("Difference entre grippe et rhume ?", "standard"),
        
        # MODE LONG (QUALITE MAXIMALE)
        ("Je suis etudiant en medecine. Fais-moi un rapport complet sur le diabete de type 2 avec physiopathologie, diagnostic et traitement.", "long"),
        ("Donne-moi une analyse approfondie de l'hypertension arterielle avec les donnees epidemiologiques et les comparaisons de traitements.", "long"),
        ("Rapport detaille sur la maladie d'Alzheimer avec les dernieres recherches et essais cliniques.", "long"),
    ]
    
    results = {"fast": [], "standard": [], "long": []}
    
    for query, mode in test_cases:
        print(f"\n[TEST] [{mode.upper()}]: {query[:50]}...")
        result = await test_query(query, mode)
        
        if "error" in result:
            print(f"   [ERREUR]: {result['error']}")
            results[mode].append({"error": True, "query": query})
            continue
        
        quality = result["quality"]
        grade = quality["grade"]
        score = quality["total_score"]
        
        grade_symbol = {"A+": "[A+]", "A": "[A]", "B": "[B]", "C": "[C]", "F": "[F]"}.get(grade, "[?]")
        
        print(f"   {grade_symbol} Grade: {grade} ({score}%)")
        print(f"   Temps: {result['time_ms']}ms | Longueur: {result['response_length']} chars")
        print(f"   Structure: {quality['structure']['score']:.0f}% | Sources: {quality['sources']['score']:.0f}% | Disclaimer: {quality['disclaimer']['score']:.0f}%")
        
        if mode == "long":
            print(f"   Research Log: {quality['research_log']['score']:.0f}% | Analyse IA: {quality['analysis']['score']:.0f}%")
            print(f"   Data Quality: {quality['data_quality']['score']:.0f}%")
            
            if score < 85:
                print(f"   [!] AMELIORATIONS NECESSAIRES:")
                if quality['sources']['score'] < 50:
                    print(f"      - Ajouter plus de citations [SOURCE]")
                if quality['research_log']['score'] < 50:
                    print(f"      - Afficher le log de recherche")
                if quality['disclaimer']['score'] < 100:
                    print(f"      - Disclaimer manquant!")
                if quality['data_quality']['score'] < 50:
                    print(f"      - Ajouter des donnees chiffrees")
        
        results[mode].append(result)
        await asyncio.sleep(2)  # Rate limiting
    
    # Summary
    print("\n" + "=" * 80)
    print("RESUME GLOBAL")
    print("=" * 80)
    
    for mode in ["fast", "standard", "long"]:
        mode_results = [r for r in results[mode] if "error" not in r]
        if not mode_results:
            print(f"\n{mode.upper()}: Aucun resultat valide")
            continue
        
        avg_score = sum(r["quality"]["total_score"] for r in mode_results) / len(mode_results)
        avg_time = sum(r["time_ms"] for r in mode_results) / len(mode_results)
        disclaimer_rate = sum(1 for r in mode_results if r["quality"]["disclaimer"]["score"] == 100) / len(mode_results) * 100
        
        grade = "A+" if avg_score >= 95 else "A" if avg_score >= 85 else "B" if avg_score >= 70 else "C"
        
        print(f"\nMODE {mode.upper()}:")
        print(f"   Score moyen: {avg_score:.1f}% (Grade: {grade})")
        print(f"   Temps moyen: {avg_time:.0f}ms")
        print(f"   Disclaimer: {disclaimer_rate:.0f}%")
    
    # Global score
    all_results = [r for m in results.values() for r in m if "error" not in r]
    if all_results:
        global_score = sum(r["quality"]["total_score"] for r in all_results) / len(all_results)
        print(f"\n{'=' * 80}")
        print(f"SCORE GLOBAL: {global_score:.1f}%")
        
        if global_score >= 95:
            print("QUALITE EXCEPTIONNELLE - Meilleur moteur medical du monde!")
        elif global_score >= 85:
            print("EXCELLENTE QUALITE - Tres bon niveau")
        elif global_score >= 70:
            print("BONNE QUALITE - Ameliorations possibles")
        else:
            print("QUALITE INSUFFISANTE - Optimisations requises")
    
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(run_global_tests())
