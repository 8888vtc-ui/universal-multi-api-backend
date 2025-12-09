"""
Production API Tester & Optimizer
Tests the health expert API in 3 modes: FAST, STANDARD, LONG
Checks response quality, disclaimers, and provides optimization recommendations
"""
import httpx
import asyncio
import time
import json
from typing import Dict, Any, List, Tuple
from dataclasses import dataclass
from enum import Enum


# ============================================
# CONFIGURATION
# ============================================

PRODUCTION_URL = "https://universal-api-hub.fly.dev"
API_URL = f"{PRODUCTION_URL}/api"

# Test queries for each mode
TEST_QUERIES = {
    "fast": [
        # Quick chat queries - should respond in <2s
        {"message": "Bonjour", "expected": "greeting"},
        {"message": "C'est quoi un rhume ?", "expected": "simple_info"},
        {"message": "Merci pour l'info", "expected": "acknowledgment"},
    ],
    "standard": [
        # Standard queries - should respond in 2-5s with good info
        {"message": "Quels sont les symptomes du diabete type 2 ?", "expected": "symptoms_list"},
        {"message": "Comment fonctionne le paracetamol ?", "expected": "drug_info"},
        {"message": "Quelle est la difference entre grippe et covid ?", "expected": "comparison"},
    ],
    "long": [
        # Deep queries - can take 5-15s but must be comprehensive
        {"message": "Je suis etudiant en medecine. Explique-moi le mecanisme complet de l'hypertension arterielle, ses causes, consequences et traitements.", "expected": "comprehensive"},
        {"message": "Fais-moi un rapport complet sur le diabete de type 2 avec les dernieres etudes.", "expected": "report"},
    ]
}

# Required disclaimer keywords (at least one must be present)
DISCLAIMER_KEYWORDS = [
    "medecin",
    "professionnel de sante",
    "consultation",
    "avis medical",
    "consulter",
    "nous ne remplacons pas",
    "information",
    "ne constitue pas un avis",
    "diagnostic"
]


@dataclass
class TestResult:
    """Result of a single test"""
    mode: str
    query: str
    response_time_ms: float
    response_length: int
    has_disclaimer: bool
    quality_score: float
    sources_mentioned: List[str]
    error: str = None
    response_preview: str = ""


class ResponseQualityChecker:
    """Check quality of medical responses"""
    
    def __init__(self):
        # Keywords that indicate quality content
        self.quality_indicators = {
            "symptoms_list": ["symptome", "signe", "manifestation"],
            "drug_info": ["posologie", "effet", "contre-indication", "mecanisme"],
            "comparison": ["difference", "contrairement", "tandis que", "alors que"],
            "comprehensive": ["mecanisme", "cause", "consequence", "traitement", "physiopathologie"],
            "report": ["etude", "recherche", "statistique", "selon", "donnees"],
            "simple_info": ["definit", "caracterise", "consiste"],
            "greeting": ["bonjour", "bienvenue", "aide"],
            "acknowledgment": ["plaisir", "questions", "hesitez"]
        }
        
        # Source tags to look for
        self.source_tags = ["[PUBMED]", "[FDA]", "[OMS]", "[WHO]", "[ANALYSE IA]", "[RxNorm]", "Source:"]
    
    def check_quality(self, response: str, expected_type: str) -> Tuple[float, List[str]]:
        """
        Check response quality and return score (0-1) + issues found
        """
        issues = []
        score = 1.0
        response_lower = response.lower()
        
        # Check 1: Response not too short
        if len(response) < 100:
            issues.append("Reponse trop courte")
            score -= 0.3
        
        # Check 2: Expected content present
        indicators = self.quality_indicators.get(expected_type, [])
        found_indicators = sum(1 for ind in indicators if ind in response_lower)
        if indicators and found_indicators == 0:
            issues.append(f"Contenu attendu absent ({expected_type})")
            score -= 0.2
        
        # Check 3: No "I don't know" phrases
        negative_phrases = ["je ne sais pas", "je ne peux pas", "impossible de", "aucune information"]
        if any(phrase in response_lower for phrase in negative_phrases):
            issues.append("Phrase negative detectee")
            score -= 0.3
        
        # Check 4: Sources mentioned (bonus)
        sources_found = [s for s in self.source_tags if s.lower() in response_lower or s in response]
        if sources_found:
            score += 0.1  # Bonus for citing sources
        
        # Check 5: Structure (for long responses)
        if expected_type in ["comprehensive", "report"]:
            if "**" in response or "##" in response or "- " in response:
                score += 0.1  # Bonus for structured response
            else:
                issues.append("Manque de structure (titres, listes)")
        
        return min(1.0, max(0.0, score)), issues
    
    def extract_sources(self, response: str) -> List[str]:
        """Extract mentioned sources from response"""
        sources = []
        for tag in self.source_tags:
            if tag.lower() in response.lower() or tag in response:
                sources.append(tag)
        return sources
    
    def check_disclaimer(self, response: str) -> bool:
        """Check if medical disclaimer is present"""
        response_lower = response.lower()
        return any(kw in response_lower for kw in DISCLAIMER_KEYWORDS)


class ProductionTester:
    """Test production API and collect results"""
    
    def __init__(self):
        self.quality_checker = ResponseQualityChecker()
        self.results: List[TestResult] = []
        self.session_id = f"test_{int(time.time())}"
    
    async def test_health_check(self) -> bool:
        """Check if server is healthy"""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(f"{API_URL}/health")
                if response.status_code == 200:
                    data = response.json()
                    print(f"[OK] Server healthy: {data.get('status')}")
                    print(f"    AI Providers: {list(data.get('ai_providers', {}).keys())}")
                    return True
        except Exception as e:
            print(f"[ERROR] Server not reachable: {e}")
            return False
        return False
    
    async def test_query(self, mode: str, query_data: Dict) -> TestResult:
        """Test a single query"""
        query = query_data["message"]
        expected = query_data["expected"]
        
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                start_time = time.time()
                
                response = await client.post(
                    f"{API_URL}/expert/health/chat",
                    json={
                        "message": query,
                        "session_id": self.session_id
                    }
                )
                
                elapsed_ms = (time.time() - start_time) * 1000
                
                if response.status_code == 200:
                    data = response.json()
                    response_text = data.get("response", "")
                    
                    # Check quality
                    quality_score, issues = self.quality_checker.check_quality(response_text, expected)
                    has_disclaimer = self.quality_checker.check_disclaimer(response_text)
                    sources = self.quality_checker.extract_sources(response_text)
                    
                    return TestResult(
                        mode=mode,
                        query=query[:50] + "..." if len(query) > 50 else query,
                        response_time_ms=elapsed_ms,
                        response_length=len(response_text),
                        has_disclaimer=has_disclaimer,
                        quality_score=quality_score,
                        sources_mentioned=sources,
                        response_preview=response_text[:200] + "..." if len(response_text) > 200 else response_text
                    )
                else:
                    return TestResult(
                        mode=mode,
                        query=query[:50],
                        response_time_ms=elapsed_ms,
                        response_length=0,
                        has_disclaimer=False,
                        quality_score=0,
                        sources_mentioned=[],
                        error=f"HTTP {response.status_code}: {response.text[:100]}"
                    )
                    
        except Exception as e:
            return TestResult(
                mode=mode,
                query=query[:50],
                response_time_ms=0,
                response_length=0,
                has_disclaimer=False,
                quality_score=0,
                sources_mentioned=[],
                error=str(e)
            )
    
    async def run_all_tests(self):
        """Run all tests for all modes"""
        print("\n" + "=" * 70)
        print("🧪 PRODUCTION API TESTER - Expert Sante")
        print("=" * 70)
        
        # Health check first
        if not await self.test_health_check():
            print("[ABORT] Server not healthy")
            return
        
        # Test each mode
        for mode, queries in TEST_QUERIES.items():
            print(f"\n{'=' * 70}")
            print(f"📋 Mode: {mode.upper()}")
            print("=" * 70)
            
            for query_data in queries:
                print(f"\n🔍 Testing: {query_data['message'][:40]}...")
                result = await self.test_query(mode, query_data)
                self.results.append(result)
                
                # Print result
                if result.error:
                    print(f"   ❌ ERROR: {result.error}")
                else:
                    status = "✅" if result.quality_score >= 0.7 else "⚠️"
                    disclaimer_status = "✅" if result.has_disclaimer else "⚠️"
                    
                    print(f"   {status} Time: {result.response_time_ms:.0f}ms | Length: {result.response_length} chars")
                    print(f"   {disclaimer_status} Disclaimer: {'Present' if result.has_disclaimer else 'MISSING!'}")
                    print(f"   📊 Quality: {result.quality_score:.1%}")
                    if result.sources_mentioned:
                        print(f"   📚 Sources: {', '.join(result.sources_mentioned)}")
        
        # Generate report
        self.generate_report()
    
    def generate_report(self):
        """Generate optimization report"""
        print("\n" + "=" * 70)
        print("📊 RAPPORT D'OPTIMISATION")
        print("=" * 70)
        
        # Group by mode
        by_mode = {}
        for r in self.results:
            if r.mode not in by_mode:
                by_mode[r.mode] = []
            by_mode[r.mode].append(r)
        
        # Analyze each mode
        recommendations = []
        
        for mode, results in by_mode.items():
            valid_results = [r for r in results if not r.error]
            
            if not valid_results:
                print(f"\n❌ {mode.upper()}: Tous les tests ont echoue!")
                continue
            
            avg_time = sum(r.response_time_ms for r in valid_results) / len(valid_results)
            avg_quality = sum(r.quality_score for r in valid_results) / len(valid_results)
            disclaimer_rate = sum(1 for r in valid_results if r.has_disclaimer) / len(valid_results)
            avg_length = sum(r.response_length for r in valid_results) / len(valid_results)
            
            print(f"\n📌 {mode.upper()}:")
            print(f"   Temps moyen: {avg_time:.0f}ms")
            print(f"   Qualite moyenne: {avg_quality:.1%}")
            print(f"   Taux disclaimer: {disclaimer_rate:.0%}")
            print(f"   Longueur moyenne: {avg_length:.0f} chars")
            
            # Mode-specific recommendations
            if mode == "fast":
                if avg_time > 3000:
                    recommendations.append(f"FAST: Temps trop long ({avg_time:.0f}ms). Objectif: <2000ms")
                if avg_length > 500:
                    recommendations.append(f"FAST: Reponses trop longues ({avg_length:.0f} chars). Objectif: <400 chars")
                    
            elif mode == "standard":
                if avg_time > 5000:
                    recommendations.append(f"STANDARD: Temps trop long ({avg_time:.0f}ms). Objectif: 2-5s")
                if avg_quality < 0.7:
                    recommendations.append(f"STANDARD: Qualite insuffisante ({avg_quality:.1%}). Objectif: >70%")
                    
            elif mode == "long":
                if avg_quality < 0.8:
                    recommendations.append(f"LONG: Qualite insuffisante ({avg_quality:.1%}). Objectif: >80%")
                if avg_length < 1000:
                    recommendations.append(f"LONG: Reponses trop courtes ({avg_length:.0f} chars). Objectif: >1000 chars")
            
            # Disclaimer check
            if disclaimer_rate < 1.0:
                recommendations.append(f"{mode.upper()}: Disclaimer manquant dans {(1-disclaimer_rate)*100:.0f}% des reponses!")
        
        # Print recommendations
        if recommendations:
            print("\n" + "=" * 70)
            print("⚠️  ACTIONS REQUISES:")
            print("=" * 70)
            for rec in recommendations:
                print(f"   • {rec}")
        else:
            print("\n✅ Tous les criteres sont satisfaits!")
        
        # Return summary
        return {
            "total_tests": len(self.results),
            "errors": sum(1 for r in self.results if r.error),
            "avg_quality": sum(r.quality_score for r in self.results if not r.error) / max(1, len([r for r in self.results if not r.error])),
            "recommendations": recommendations
        }


async def main():
    tester = ProductionTester()
    await tester.run_all_tests()


if __name__ == "__main__":
    asyncio.run(main())
