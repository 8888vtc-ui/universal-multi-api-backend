"""
Script de test automatique pour tous les experts/bots
Vérifie que tous les experts fonctionnent et produisent des réponses réalistes
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

import asyncio
import httpx
import time
from typing import Dict, List, Tuple, Optional
from datetime import datetime
import json

# Configuration
BASE_URL = "http://localhost:8000"  # Changez pour production: "https://universal-api-hub.fly.dev"
TIMEOUT = 30.0  # Timeout par requête

# Questions de test par expert
TEST_QUESTIONS = {
    "health": "Quels sont les bienfaits du sommeil ?",
    "sports": "Quels sont les derniers résultats foot ?",
    "finance": "Quel est le cours du Bitcoin ?",
    "tourism": "Quel temps fait-il à Paris ?",
    "general": "Qui a inventé Internet ?",
    "humor": "Raconte-moi une blague !",
    "cuisine": "Une recette de carbonara ?",
    "tech": "C'est quoi ChatGPT ?",
    "cinema": "Un bon film ce soir ?",
    "weather": "Météo Paris demain ?",
    "love": "Comment mieux communiquer en couple ?",
    "gaming": "Les meilleurs jeux 2024 ?",
    "news": "Actualités du jour ?",
    "horoscope": "Horoscope Bélier aujourd'hui ?",
    "prenom": "Que signifie le prénom Emma ?",
    "history": "Que s'est-il passé aujourd'hui dans l'histoire ?",
}

# Questions de test pour le chat général
GENERAL_CHAT_QUESTIONS = [
    "Bonjour, comment ça va ?",
    "Quelle est la capitale de la France ?",
    "Explique-moi l'intelligence artificielle",
]


class ExpertTester:
    """Classe pour tester tous les experts"""
    
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
        self.results: Dict[str, Dict] = {}
        self.start_time = time.time()
    
    async def test_health(self) -> bool:
        """Teste si le serveur est accessible"""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(f"{self.base_url}/api/health")
                return response.status_code == 200
        except Exception as e:
            print(f"[ERR] Serveur inaccessible: {e}")
            return False
    
    async def get_all_experts(self) -> List[Dict]:
        """Récupère la liste de tous les experts"""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(f"{self.base_url}/api/expert/list")
                if response.status_code == 200:
                    return response.json()
                return []
        except Exception as e:
            print(f"[ERR] Erreur lors de la récupération des experts: {e}")
            return []
    
    async def test_expert(
        self, 
        expert_id: str, 
        question: str,
        client: httpx.AsyncClient
    ) -> Tuple[bool, Dict[str, any]]:
        """
        Teste un expert avec une question
        
        Returns:
            (success, details)
        """
        result = {
            "expert_id": expert_id,
            "question": question,
            "success": False,
            "response": None,
            "response_length": 0,
            "processing_time_ms": 0,
            "errors": [],
            "warnings": [],
            "validation": {}
        }
        
        try:
            start_time = time.time()
            
            # Envoyer la requête
            response = await client.post(
                f"{self.base_url}/api/expert/{expert_id}/chat",
                json={"message": question, "language": "fr"},
                timeout=TIMEOUT
            )
            
            processing_time = (time.time() - start_time) * 1000
            result["processing_time_ms"] = round(processing_time, 2)
            
            if response.status_code != 200:
                result["errors"].append(f"Status code: {response.status_code}")
                result["errors"].append(f"Response: {response.text[:200]}")
                return False, result
            
            data = response.json()
            ai_response = data.get("response", "")
            
            if not ai_response:
                result["errors"].append("Réponse vide")
                return False, result
            
            result["response"] = ai_response
            result["response_length"] = len(ai_response)
            
            # Validation de la réponse
            validation = self.validate_response(ai_response, question, expert_id)
            result["validation"] = validation
            
            # Vérifications
            if len(ai_response) < 10:
                result["warnings"].append("Réponse trop courte (< 10 caractères)")
            
            if "erreur" in ai_response.lower() or "error" in ai_response.lower():
                result["warnings"].append("Réponse contient le mot 'erreur'")
            
            if processing_time > 10000:  # Plus de 10 secondes
                result["warnings"].append(f"Temps de réponse lent: {processing_time:.0f}ms")
            
            # Vérifier la cohérence avec la question
            if not self.check_relevance(ai_response, question, expert_id):
                result["warnings"].append("Réponse peut-être non pertinente")
            
            result["success"] = True
            return True, result
            
        except httpx.TimeoutException:
            result["errors"].append(f"Timeout après {TIMEOUT}s")
            return False, result
        except Exception as e:
            result["errors"].append(f"Exception: {str(e)}")
            return False, result
    
    def validate_response(self, response: str, question: str, expert_id: str) -> Dict:
        """Valide une réponse"""
        validation = {
            "is_valid": True,
            "has_content": len(response.strip()) > 0,
            "min_length_ok": len(response) >= 20,
            "no_error_keywords": not any(kw in response.lower() for kw in ["erreur", "error", "impossible", "échec"]),
            "has_expert_style": self.check_expert_style(response, expert_id),
            "score": 1.0
        }
        
        # Calculer un score
        score = 1.0
        if not validation["has_content"]:
            score = 0.0
        elif not validation["min_length_ok"]:
            score *= 0.5
        if not validation["no_error_keywords"]:
            score *= 0.3
        if not validation["has_expert_style"]:
            score *= 0.8
        
        validation["score"] = score
        validation["is_valid"] = score >= 0.5
        
        return validation
    
    def check_expert_style(self, response: str, expert_id: str) -> bool:
        """Vérifie si la réponse correspond au style de l'expert"""
        # Vérifications basiques selon l'expert
        response_lower = response.lower()
        
        style_checks = {
            "humor": any(kw in response_lower for kw in ["blague", "rire", "drôle", "😄", "😂"]),
            "health": any(kw in response_lower for kw in ["santé", "médical", "médecin", "consult"]),
            "finance": any(kw in response_lower for kw in ["finance", "investissement", "crypto", "bitcoin"]),
            "weather": any(kw in response_lower for kw in ["météo", "température", "pluie", "soleil"]),
        }
        
        # Si l'expert a un style spécifique, vérifier
        if expert_id in style_checks:
            return style_checks[expert_id]
        
        # Sinon, accepter par défaut
        return True
    
    def check_relevance(self, response: str, question: str, expert_id: str) -> bool:
        """Vérifie la pertinence de la réponse"""
        question_lower = question.lower()
        response_lower = response.lower()
        
        # Extraire les mots-clés de la question
        question_keywords = set(word for word in question_lower.split() if len(word) > 3)
        
        # Vérifier si au moins un mot-clé apparaît dans la réponse
        if question_keywords:
            matches = sum(1 for kw in question_keywords if kw in response_lower)
            relevance = matches / len(question_keywords)
            return relevance >= 0.2  # Au moins 20% des mots-clés
        
        return True  # Si pas de mots-clés, accepter
    
    async def test_general_chat(self, question: str, client: httpx.AsyncClient) -> Tuple[bool, Dict]:
        """Teste le chat général"""
        result = {
            "endpoint": "chat",
            "question": question,
            "success": False,
            "response": None,
            "processing_time_ms": 0,
            "errors": []
        }
        
        try:
            start_time = time.time()
            response = await client.post(
                f"{self.base_url}/api/chat",
                json={"message": question, "language": "fr"},
                timeout=TIMEOUT
            )
            
            processing_time = (time.time() - start_time) * 1000
            result["processing_time_ms"] = round(processing_time, 2)
            
            if response.status_code == 200:
                data = response.json()
                result["response"] = data.get("response", "")
                result["success"] = len(result["response"]) > 0
            else:
                result["errors"].append(f"Status {response.status_code}: {response.text[:200]}")
                
        except Exception as e:
            result["errors"].append(str(e))
        
        return result["success"], result
    
    async def run_all_tests(self) -> Dict:
        """Exécute tous les tests"""
        print("[ROCKET] Démarrage des tests automatiques des experts...")
        print(f"📍 Serveur: {self.base_url}\n")
        
        # Test 1: Vérifier que le serveur est accessible
        print("1️⃣ Vérification du serveur...")
        if not await self.test_health():
            print("[ERR] Le serveur n'est pas accessible. Arrêt des tests.")
            return {"error": "Serveur inaccessible"}
        print("[OK] Serveur accessible\n")
        
        # Test 2: Récupérer tous les experts
        print("2️⃣ Récupération de la liste des experts...")
        experts = await self.get_all_experts()
        if not experts:
            print("[ERR] Aucun expert trouvé")
            return {"error": "Aucun expert disponible"}
        
        print(f"[OK] {len(experts)} experts trouvés\n")
        
        # Test 3: Tester chaque expert
        print("3️⃣ Test de chaque expert...")
        print("=" * 60)
        
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            tasks = []
            
            for expert in experts:
                expert_id = expert.get("id")
                expert_name = expert.get("name", expert_id)
                question = TEST_QUESTIONS.get(expert_id, "Bonjour, comment ça va ?")
                
                print(f"\n🧪 Test: {expert_name} ({expert_id})")
                print(f"   Question: {question[:50]}...")
                
                success, result = await self.test_expert(expert_id, question, client)
                
                if success:
                    validation = result["validation"]
                    score = validation.get("score", 0)
                    print(f"   [OK] Succès (score: {score:.2f}, temps: {result['processing_time_ms']:.0f}ms)")
                    if result.get("warnings"):
                        for warning in result["warnings"]:
                            print(f"   [WARN]  {warning}")
                else:
                    print(f"   [ERR] Échec")
                    for error in result.get("errors", []):
                        print(f"   [WARN]  {error}")
                
                self.results[expert_id] = result
                await asyncio.sleep(0.5)  # Pause entre les tests
        
        # Test 4: Tester le chat général
        print("\n" + "=" * 60)
        print("4️⃣ Test du chat général...")
        
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            for question in GENERAL_CHAT_QUESTIONS[:2]:  # Tester 2 questions
                print(f"\n🧪 Question: {question[:50]}...")
                success, result = await self.test_general_chat(question, client)
                if success:
                    print(f"   [OK] Succès (temps: {result['processing_time_ms']:.0f}ms)")
                else:
                    print(f"   [ERR] Échec: {result.get('errors', [])}")
                self.results[f"chat_{question[:20]}"] = result
        
        # Générer le rapport
        return self.generate_report()
    
    def generate_report(self) -> Dict:
        """Génère un rapport détaillé"""
        total = len(self.results)
        successful = sum(1 for r in self.results.values() if r.get("success", False))
        failed = total - successful
        
        # Calculer les statistiques
        successful_results = [r for r in self.results.values() if r.get("success", False)]
        avg_time = sum(r.get("processing_time_ms", 0) for r in successful_results) / len(successful_results) if successful_results else 0
        avg_score = sum(r.get("validation", {}).get("score", 0) for r in successful_results) / len(successful_results) if successful_results else 0
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "base_url": self.base_url,
            "summary": {
                "total_tests": total,
                "successful": successful,
                "failed": failed,
                "success_rate": f"{(successful/total*100):.1f}%" if total > 0 else "0%",
                "average_response_time_ms": round(avg_time, 2),
                "average_validation_score": round(avg_score, 2),
                "total_time_seconds": round(time.time() - self.start_time, 2)
            },
            "details": self.results
        }
        
        return report
    
    def print_report(self, report: Dict):
        """Affiche le rapport de manière lisible"""
        print("\n" + "=" * 60)
        print("📊 RAPPORT DE TEST")
        print("=" * 60)
        
        summary = report.get("summary", {})
        print(f"\n[OK] Tests réussis: {summary.get('successful', 0)}/{summary.get('total_tests', 0)}")
        print(f"[ERR] Tests échoués: {summary.get('failed', 0)}")
        print(f"📈 Taux de succès: {summary.get('success_rate', '0%')}")
        print(f"⏱️  Temps moyen de réponse: {summary.get('average_response_time_ms', 0):.0f}ms")
        print(f"⭐ Score de validation moyen: {summary.get('average_validation_score', 0):.2f}")
        print(f"⏰ Temps total: {summary.get('total_time_seconds', 0):.1f}s")
        
        # Détails des échecs
        failed_tests = [
            (k, v) for k, v in report.get("details", {}).items() 
            if not v.get("success", False)
        ]
        
        if failed_tests:
            print(f"\n[ERR] Tests échoués ({len(failed_tests)}):")
            for test_id, result in failed_tests:
                print(f"   - {test_id}: {', '.join(result.get('errors', []))}")
        
        # Avertissements
        warnings_count = sum(
            len(r.get("warnings", [])) 
            for r in report.get("details", {}).values() 
            if r.get("success", False)
        )
        
        if warnings_count > 0:
            print(f"\n[WARN]  Avertissements détectés: {warnings_count}")
        
        print("\n" + "=" * 60)


async def main():
    """Fonction principale"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Test automatique de tous les experts")
    parser.add_argument(
        "--url",
        default=BASE_URL,
        help=f"URL du serveur (défaut: {BASE_URL})"
    )
    parser.add_argument(
        "--output",
        help="Fichier JSON pour sauvegarder le rapport"
    )
    
    args = parser.parse_args()
    
    tester = ExpertTester(base_url=args.url)
    report = await tester.run_all_tests()
    
    if "error" in report:
        print(f"\n[ERR] Erreur: {report['error']}")
        return 1
    
    tester.print_report(report)
    
    # Sauvegarder le rapport si demandé
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"\n💾 Rapport sauvegardé dans: {args.output}")
    
    # Code de retour
    summary = report.get("summary", {})
    if summary.get("failed", 0) > 0:
        return 1
    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)


Script de test automatique pour tous les experts/bots
Vérifie que tous les experts fonctionnent et produisent des réponses réalistes
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

import asyncio
import httpx
import time
from typing import Dict, List, Tuple, Optional
from datetime import datetime
import json

# Configuration
BASE_URL = "http://localhost:8000"  # Changez pour production: "https://universal-api-hub.fly.dev"
TIMEOUT = 30.0  # Timeout par requête

# Questions de test par expert
TEST_QUESTIONS = {
    "health": "Quels sont les bienfaits du sommeil ?",
    "sports": "Quels sont les derniers résultats foot ?",
    "finance": "Quel est le cours du Bitcoin ?",
    "tourism": "Quel temps fait-il à Paris ?",
    "general": "Qui a inventé Internet ?",
    "humor": "Raconte-moi une blague !",
    "cuisine": "Une recette de carbonara ?",
    "tech": "C'est quoi ChatGPT ?",
    "cinema": "Un bon film ce soir ?",
    "weather": "Météo Paris demain ?",
    "love": "Comment mieux communiquer en couple ?",
    "gaming": "Les meilleurs jeux 2024 ?",
    "news": "Actualités du jour ?",
    "horoscope": "Horoscope Bélier aujourd'hui ?",
    "prenom": "Que signifie le prénom Emma ?",
    "history": "Que s'est-il passé aujourd'hui dans l'histoire ?",
}

# Questions de test pour le chat général
GENERAL_CHAT_QUESTIONS = [
    "Bonjour, comment ça va ?",
    "Quelle est la capitale de la France ?",
    "Explique-moi l'intelligence artificielle",
]


class ExpertTester:
    """Classe pour tester tous les experts"""
    
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
        self.results: Dict[str, Dict] = {}
        self.start_time = time.time()
    
    async def test_health(self) -> bool:
        """Teste si le serveur est accessible"""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(f"{self.base_url}/api/health")
                return response.status_code == 200
        except Exception as e:
            print(f"[ERR] Serveur inaccessible: {e}")
            return False
    
    async def get_all_experts(self) -> List[Dict]:
        """Récupère la liste de tous les experts"""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(f"{self.base_url}/api/expert/list")
                if response.status_code == 200:
                    return response.json()
                return []
        except Exception as e:
            print(f"[ERR] Erreur lors de la récupération des experts: {e}")
            return []
    
    async def test_expert(
        self, 
        expert_id: str, 
        question: str,
        client: httpx.AsyncClient
    ) -> Tuple[bool, Dict[str, any]]:
        """
        Teste un expert avec une question
        
        Returns:
            (success, details)
        """
        result = {
            "expert_id": expert_id,
            "question": question,
            "success": False,
            "response": None,
            "response_length": 0,
            "processing_time_ms": 0,
            "errors": [],
            "warnings": [],
            "validation": {}
        }
        
        try:
            start_time = time.time()
            
            # Envoyer la requête
            response = await client.post(
                f"{self.base_url}/api/expert/{expert_id}/chat",
                json={"message": question, "language": "fr"},
                timeout=TIMEOUT
            )
            
            processing_time = (time.time() - start_time) * 1000
            result["processing_time_ms"] = round(processing_time, 2)
            
            if response.status_code != 200:
                result["errors"].append(f"Status code: {response.status_code}")
                result["errors"].append(f"Response: {response.text[:200]}")
                return False, result
            
            data = response.json()
            ai_response = data.get("response", "")
            
            if not ai_response:
                result["errors"].append("Réponse vide")
                return False, result
            
            result["response"] = ai_response
            result["response_length"] = len(ai_response)
            
            # Validation de la réponse
            validation = self.validate_response(ai_response, question, expert_id)
            result["validation"] = validation
            
            # Vérifications
            if len(ai_response) < 10:
                result["warnings"].append("Réponse trop courte (< 10 caractères)")
            
            if "erreur" in ai_response.lower() or "error" in ai_response.lower():
                result["warnings"].append("Réponse contient le mot 'erreur'")
            
            if processing_time > 10000:  # Plus de 10 secondes
                result["warnings"].append(f"Temps de réponse lent: {processing_time:.0f}ms")
            
            # Vérifier la cohérence avec la question
            if not self.check_relevance(ai_response, question, expert_id):
                result["warnings"].append("Réponse peut-être non pertinente")
            
            result["success"] = True
            return True, result
            
        except httpx.TimeoutException:
            result["errors"].append(f"Timeout après {TIMEOUT}s")
            return False, result
        except Exception as e:
            result["errors"].append(f"Exception: {str(e)}")
            return False, result
    
    def validate_response(self, response: str, question: str, expert_id: str) -> Dict:
        """Valide une réponse"""
        validation = {
            "is_valid": True,
            "has_content": len(response.strip()) > 0,
            "min_length_ok": len(response) >= 20,
            "no_error_keywords": not any(kw in response.lower() for kw in ["erreur", "error", "impossible", "échec"]),
            "has_expert_style": self.check_expert_style(response, expert_id),
            "score": 1.0
        }
        
        # Calculer un score
        score = 1.0
        if not validation["has_content"]:
            score = 0.0
        elif not validation["min_length_ok"]:
            score *= 0.5
        if not validation["no_error_keywords"]:
            score *= 0.3
        if not validation["has_expert_style"]:
            score *= 0.8
        
        validation["score"] = score
        validation["is_valid"] = score >= 0.5
        
        return validation
    
    def check_expert_style(self, response: str, expert_id: str) -> bool:
        """Vérifie si la réponse correspond au style de l'expert"""
        # Vérifications basiques selon l'expert
        response_lower = response.lower()
        
        style_checks = {
            "humor": any(kw in response_lower for kw in ["blague", "rire", "drôle", "😄", "😂"]),
            "health": any(kw in response_lower for kw in ["santé", "médical", "médecin", "consult"]),
            "finance": any(kw in response_lower for kw in ["finance", "investissement", "crypto", "bitcoin"]),
            "weather": any(kw in response_lower for kw in ["météo", "température", "pluie", "soleil"]),
        }
        
        # Si l'expert a un style spécifique, vérifier
        if expert_id in style_checks:
            return style_checks[expert_id]
        
        # Sinon, accepter par défaut
        return True
    
    def check_relevance(self, response: str, question: str, expert_id: str) -> bool:
        """Vérifie la pertinence de la réponse"""
        question_lower = question.lower()
        response_lower = response.lower()
        
        # Extraire les mots-clés de la question
        question_keywords = set(word for word in question_lower.split() if len(word) > 3)
        
        # Vérifier si au moins un mot-clé apparaît dans la réponse
        if question_keywords:
            matches = sum(1 for kw in question_keywords if kw in response_lower)
            relevance = matches / len(question_keywords)
            return relevance >= 0.2  # Au moins 20% des mots-clés
        
        return True  # Si pas de mots-clés, accepter
    
    async def test_general_chat(self, question: str, client: httpx.AsyncClient) -> Tuple[bool, Dict]:
        """Teste le chat général"""
        result = {
            "endpoint": "chat",
            "question": question,
            "success": False,
            "response": None,
            "processing_time_ms": 0,
            "errors": []
        }
        
        try:
            start_time = time.time()
            response = await client.post(
                f"{self.base_url}/api/chat",
                json={"message": question, "language": "fr"},
                timeout=TIMEOUT
            )
            
            processing_time = (time.time() - start_time) * 1000
            result["processing_time_ms"] = round(processing_time, 2)
            
            if response.status_code == 200:
                data = response.json()
                result["response"] = data.get("response", "")
                result["success"] = len(result["response"]) > 0
            else:
                result["errors"].append(f"Status {response.status_code}: {response.text[:200]}")
                
        except Exception as e:
            result["errors"].append(str(e))
        
        return result["success"], result
    
    async def run_all_tests(self) -> Dict:
        """Exécute tous les tests"""
        print("[ROCKET] Démarrage des tests automatiques des experts...")
        print(f"📍 Serveur: {self.base_url}\n")
        
        # Test 1: Vérifier que le serveur est accessible
        print("1️⃣ Vérification du serveur...")
        if not await self.test_health():
            print("[ERR] Le serveur n'est pas accessible. Arrêt des tests.")
            return {"error": "Serveur inaccessible"}
        print("[OK] Serveur accessible\n")
        
        # Test 2: Récupérer tous les experts
        print("2️⃣ Récupération de la liste des experts...")
        experts = await self.get_all_experts()
        if not experts:
            print("[ERR] Aucun expert trouvé")
            return {"error": "Aucun expert disponible"}
        
        print(f"[OK] {len(experts)} experts trouvés\n")
        
        # Test 3: Tester chaque expert
        print("3️⃣ Test de chaque expert...")
        print("=" * 60)
        
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            tasks = []
            
            for expert in experts:
                expert_id = expert.get("id")
                expert_name = expert.get("name", expert_id)
                question = TEST_QUESTIONS.get(expert_id, "Bonjour, comment ça va ?")
                
                print(f"\n🧪 Test: {expert_name} ({expert_id})")
                print(f"   Question: {question[:50]}...")
                
                success, result = await self.test_expert(expert_id, question, client)
                
                if success:
                    validation = result["validation"]
                    score = validation.get("score", 0)
                    print(f"   [OK] Succès (score: {score:.2f}, temps: {result['processing_time_ms']:.0f}ms)")
                    if result.get("warnings"):
                        for warning in result["warnings"]:
                            print(f"   [WARN]  {warning}")
                else:
                    print(f"   [ERR] Échec")
                    for error in result.get("errors", []):
                        print(f"   [WARN]  {error}")
                
                self.results[expert_id] = result
                await asyncio.sleep(0.5)  # Pause entre les tests
        
        # Test 4: Tester le chat général
        print("\n" + "=" * 60)
        print("4️⃣ Test du chat général...")
        
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            for question in GENERAL_CHAT_QUESTIONS[:2]:  # Tester 2 questions
                print(f"\n🧪 Question: {question[:50]}...")
                success, result = await self.test_general_chat(question, client)
                if success:
                    print(f"   [OK] Succès (temps: {result['processing_time_ms']:.0f}ms)")
                else:
                    print(f"   [ERR] Échec: {result.get('errors', [])}")
                self.results[f"chat_{question[:20]}"] = result
        
        # Générer le rapport
        return self.generate_report()
    
    def generate_report(self) -> Dict:
        """Génère un rapport détaillé"""
        total = len(self.results)
        successful = sum(1 for r in self.results.values() if r.get("success", False))
        failed = total - successful
        
        # Calculer les statistiques
        successful_results = [r for r in self.results.values() if r.get("success", False)]
        avg_time = sum(r.get("processing_time_ms", 0) for r in successful_results) / len(successful_results) if successful_results else 0
        avg_score = sum(r.get("validation", {}).get("score", 0) for r in successful_results) / len(successful_results) if successful_results else 0
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "base_url": self.base_url,
            "summary": {
                "total_tests": total,
                "successful": successful,
                "failed": failed,
                "success_rate": f"{(successful/total*100):.1f}%" if total > 0 else "0%",
                "average_response_time_ms": round(avg_time, 2),
                "average_validation_score": round(avg_score, 2),
                "total_time_seconds": round(time.time() - self.start_time, 2)
            },
            "details": self.results
        }
        
        return report
    
    def print_report(self, report: Dict):
        """Affiche le rapport de manière lisible"""
        print("\n" + "=" * 60)
        print("📊 RAPPORT DE TEST")
        print("=" * 60)
        
        summary = report.get("summary", {})
        print(f"\n[OK] Tests réussis: {summary.get('successful', 0)}/{summary.get('total_tests', 0)}")
        print(f"[ERR] Tests échoués: {summary.get('failed', 0)}")
        print(f"📈 Taux de succès: {summary.get('success_rate', '0%')}")
        print(f"⏱️  Temps moyen de réponse: {summary.get('average_response_time_ms', 0):.0f}ms")
        print(f"⭐ Score de validation moyen: {summary.get('average_validation_score', 0):.2f}")
        print(f"⏰ Temps total: {summary.get('total_time_seconds', 0):.1f}s")
        
        # Détails des échecs
        failed_tests = [
            (k, v) for k, v in report.get("details", {}).items() 
            if not v.get("success", False)
        ]
        
        if failed_tests:
            print(f"\n[ERR] Tests échoués ({len(failed_tests)}):")
            for test_id, result in failed_tests:
                print(f"   - {test_id}: {', '.join(result.get('errors', []))}")
        
        # Avertissements
        warnings_count = sum(
            len(r.get("warnings", [])) 
            for r in report.get("details", {}).values() 
            if r.get("success", False)
        )
        
        if warnings_count > 0:
            print(f"\n[WARN]  Avertissements détectés: {warnings_count}")
        
        print("\n" + "=" * 60)


async def main():
    """Fonction principale"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Test automatique de tous les experts")
    parser.add_argument(
        "--url",
        default=BASE_URL,
        help=f"URL du serveur (défaut: {BASE_URL})"
    )
    parser.add_argument(
        "--output",
        help="Fichier JSON pour sauvegarder le rapport"
    )
    
    args = parser.parse_args()
    
    tester = ExpertTester(base_url=args.url)
    report = await tester.run_all_tests()
    
    if "error" in report:
        print(f"\n[ERR] Erreur: {report['error']}")
        return 1
    
    tester.print_report(report)
    
    # Sauvegarder le rapport si demandé
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"\n💾 Rapport sauvegardé dans: {args.output}")
    
    # Code de retour
    summary = report.get("summary", {})
    if summary.get("failed", 0) > 0:
        return 1
    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)



