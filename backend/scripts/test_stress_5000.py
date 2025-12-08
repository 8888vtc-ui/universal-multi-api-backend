"""
Script de test de charge et détection d'erreurs
Génère 5000 questions/réponses et détecte les erreurs
S'arrête automatiquement en cas d'erreur critique
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

import asyncio
import httpx
import time
import random
from typing import Dict, List, Tuple, Optional
from datetime import datetime
import json
from collections import defaultdict

# Configuration
BASE_URL = "http://localhost:8000"
TIMEOUT = 30.0
MAX_QUESTIONS = 5000
STOP_ON_ERROR = True  # S'arrêter dès qu'une erreur critique est détectée

# Questions variées pour tester différents scénarios
QUESTION_TEMPLATES = {
    "health": [
        "Quels sont les bienfaits du sommeil ?",
        "Comment fonctionne le système immunitaire ?",
        "C'est quoi une alimentation équilibrée ?",
        "Quels sont les symptômes du stress ?",
        "Comment améliorer sa mémoire ?",
    ],
    "finance": [
        "Quel est le cours du Bitcoin ?",
        "C'est quoi un ETF ?",
        "Comment fonctionnent les actions ?",
        "Quelle est la différence entre crypto et actions ?",
        "Comment investir en bourse ?",
    ],
    "weather": [
        "Météo Paris demain ?",
        "Il va pleuvoir ce week-end ?",
        "Quel temps à New York ?",
        "Température à Londres aujourd'hui ?",
        "Prévisions météo pour la semaine ?",
    ],
    "tech": [
        "C'est quoi ChatGPT ?",
        "Comment fonctionne l'IA ?",
        "Quel smartphone choisir ?",
        "Les dernières news tech ?",
        "C'est quoi le machine learning ?",
    ],
    "general": [
        "Qui a inventé Internet ?",
        "Pourquoi le ciel est bleu ?",
        "C'est quoi l'IA ?",
        "Quelle est la capitale de la France ?",
        "Comment fonctionne la photosynthèse ?",
    ],
    "humor": [
        "Raconte-moi une blague !",
        "Un jeu de mots ?",
        "Fais-moi rire !",
        "Une blague sur les ordinateurs ?",
        "Blague de Toto ?",
    ],
    "cuisine": [
        "Une recette de carbonara ?",
        "Idée dessert facile ?",
        "Comment réussir une omelette ?",
        "Recette de gâteau au chocolat ?",
        "Comment faire du pain ?",
    ],
    "cinema": [
        "Un bon film ce soir ?",
        "Les meilleures séries Netflix ?",
        "C'est quoi le dernier Marvel ?",
        "Film d'horreur à voir ?",
        "Meilleur film 2024 ?",
    ],
    "sports": [
        "Quels sont les derniers résultats foot ?",
        "Comment débuter la course à pied ?",
        "Quels exercices pour se muscler ?",
        "Actualités sportives ?",
        "Qui a gagné le dernier match ?",
    ],
    "news": [
        "Actualités du jour ?",
        "News tech récentes ?",
        "Quoi de neuf dans le monde ?",
        "Dernières nouvelles ?",
        "Actualités importantes ?",
    ],
    "horoscope": [
        "Horoscope Bélier aujourd'hui ?",
        "Compatibilité Lion et Scorpion ?",
        "Prédictions pour la Balance ?",
        "Horoscope du jour ?",
        "Signe astrologique ?",
    ],
    "prenom": [
        "Que signifie le prénom Emma ?",
        "Origine du prénom Lucas ?",
        "Prénoms tendance 2024 ?",
        "Signification du prénom Marie ?",
        "Histoire du prénom Jean ?",
    ],
    "history": [
        "Que s'est-il passé aujourd'hui dans l'histoire ?",
        "Célébrités nées le 15 mars ?",
        "Événements du 14 juillet ?",
        "Histoire de la Révolution française ?",
        "Qui a découvert l'Amérique ?",
    ],
    "tourism": [
        "Quel temps fait-il à Paris ?",
        "Que visiter à Tokyo ?",
        "Meilleure période pour la Thaïlande ?",
        "Conseils voyage en Italie ?",
        "Destinations à voir ?",
    ],
    "love": [
        "Comment mieux communiquer en couple ?",
        "Comment se remettre d'une rupture ?",
        "Comment se faire des amis ?",
        "Conseils pour une relation ?",
        "Comment gérer les conflits ?",
    ],
    "gaming": [
        "Les meilleurs jeux 2024 ?",
        "Tips pour Fortnite ?",
        "Actus esports ?",
        "Jeux à jouer en ce moment ?",
        "Recommandations de jeux ?",
    ],
}

# Questions pour le chat général
GENERAL_CHAT_QUESTIONS = [
    "Bonjour, comment ça va ?",
    "Quelle est la capitale de la France ?",
    "Explique-moi l'intelligence artificielle",
    "C'est quoi Python ?",
    "Comment ça marche Internet ?",
    "Qui est Einstein ?",
    "C'est quoi la photosynthèse ?",
    "Explique-moi la gravité",
    "Quelle est la différence entre HTTP et HTTPS ?",
    "C'est quoi un algorithme ?",
]


class StressTester:
    """Testeur de charge avec détection d'erreurs"""
    
    def __init__(self, base_url: str = BASE_URL, max_questions: int = MAX_QUESTIONS):
        self.base_url = base_url
        self.max_questions = max_questions
        self.results: List[Dict] = []
        self.errors: List[Dict] = []
        self.warnings: List[Dict] = []
        self.stats = {
            "total": 0,
            "successful": 0,
            "failed": 0,
            "timeouts": 0,
            "invalid_responses": 0,
            "slow_responses": 0,
            "errors_by_type": defaultdict(int),
            "errors_by_expert": defaultdict(int),
        }
        self.start_time = time.time()
        self.experts_list: List[str] = []
        self.stop_requested = False
    
    async def get_experts(self) -> List[str]:
        """Récupère la liste des experts"""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(f"{self.base_url}/api/expert/list")
                if response.status_code == 200:
                    experts = response.json()
                    return [e.get("id") for e in experts if e.get("id")]
                return []
        except Exception as e:
            print(f"[ERR] Erreur lors de la récupération des experts: {e}")
            return []
    
    def is_critical_error(self, error_type: str) -> bool:
        """Détermine si une erreur est critique"""
        critical_errors = [
            "server_unavailable",
            "timeout",
            "invalid_response_format",
            "empty_response",
            "api_error_500",
        ]
        return error_type in critical_errors
    
    async def test_expert_question(
        self,
        expert_id: str,
        question: str,
        client: httpx.AsyncClient,
        question_num: int
    ) -> Dict:
        """Teste une question avec un expert"""
        result = {
            "question_num": question_num,
            "expert_id": expert_id,
            "question": question,
            "success": False,
            "error_type": None,
            "error_message": None,
            "response_length": 0,
            "processing_time_ms": 0,
            "timestamp": datetime.now().isoformat(),
        }
        
        try:
            start_time = time.time()
            
            response = await client.post(
                f"{self.base_url}/api/expert/{expert_id}/chat",
                json={"message": question, "language": "fr"},
                timeout=TIMEOUT
            )
            
            processing_time = (time.time() - start_time) * 1000
            result["processing_time_ms"] = round(processing_time, 2)
            
            # Vérifier le status code
            if response.status_code != 200:
                result["error_type"] = f"http_error_{response.status_code}"
                result["error_message"] = response.text[:200]
                result["success"] = False
                self.stats["errors_by_type"][result["error_type"]] += 1
                self.stats["errors_by_expert"][expert_id] += 1
                
                if response.status_code == 500:
                    result["error_type"] = "api_error_500"
                    if STOP_ON_ERROR and self.is_critical_error("api_error_500"):
                        self.stop_requested = True
                
                return result
            
            # Parser la réponse
            try:
                data = response.json()
            except Exception as e:
                result["error_type"] = "invalid_response_format"
                result["error_message"] = f"JSON parse error: {str(e)}"
                result["success"] = False
                self.stats["errors_by_type"]["invalid_response_format"] += 1
                
                if STOP_ON_ERROR and self.is_critical_error("invalid_response_format"):
                    self.stop_requested = True
                
                return result
            
            ai_response = data.get("response", "")
            
            # Vérifier si la réponse est vide
            if not ai_response or len(ai_response.strip()) == 0:
                result["error_type"] = "empty_response"
                result["error_message"] = "Réponse vide reçue"
                result["success"] = False
                self.stats["errors_by_type"]["empty_response"] += 1
                
                if STOP_ON_ERROR and self.is_critical_error("empty_response"):
                    self.stop_requested = True
                
                return result
            
            # Vérifier la longueur minimale
            if len(ai_response) < 10:
                result["error_type"] = "response_too_short"
                result["error_message"] = f"Réponse trop courte: {len(ai_response)} caractères"
                result["success"] = False
                self.stats["errors_by_type"]["response_too_short"] += 1
                return result
            
            # Vérifier les mots d'erreur
            response_lower = ai_response.lower()
            error_keywords = ["erreur", "error", "impossible", "échec", "failed", "exception"]
            if any(kw in response_lower for kw in error_keywords):
                result["error_type"] = "error_in_response"
                result["error_message"] = "Réponse contient des mots d'erreur"
                result["warnings"] = True
                # Non critique mais à noter
            
            # Vérifier le temps de réponse
            if processing_time > 15000:  # Plus de 15 secondes
                result["error_type"] = "slow_response"
                result["warnings"] = True
                self.stats["slow_responses"] += 1
            
            result["response_length"] = len(ai_response)
            result["success"] = True
            
        except httpx.TimeoutException:
            result["error_type"] = "timeout"
            result["error_message"] = f"Timeout après {TIMEOUT}s"
            result["success"] = False
            self.stats["timeouts"] += 1
            self.stats["errors_by_type"]["timeout"] += 1
            self.stats["errors_by_expert"][expert_id] += 1
            
            if STOP_ON_ERROR and self.is_critical_error("timeout"):
                self.stop_requested = True
        
        except httpx.ConnectError:
            result["error_type"] = "server_unavailable"
            result["error_message"] = "Serveur inaccessible"
            result["success"] = False
            self.stats["errors_by_type"]["server_unavailable"] += 1
            
            if STOP_ON_ERROR and self.is_critical_error("server_unavailable"):
                self.stop_requested = True
        
        except Exception as e:
            result["error_type"] = "unexpected_error"
            result["error_message"] = str(e)
            result["success"] = False
            self.stats["errors_by_type"]["unexpected_error"] += 1
        
        return result
    
    async def test_general_chat(
        self,
        question: str,
        client: httpx.AsyncClient,
        question_num: int
    ) -> Dict:
        """Teste le chat général"""
        result = {
            "question_num": question_num,
            "endpoint": "chat",
            "question": question,
            "success": False,
            "error_type": None,
            "error_message": None,
            "processing_time_ms": 0,
            "timestamp": datetime.now().isoformat(),
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
                ai_response = data.get("response", "")
                if ai_response and len(ai_response) > 10:
                    result["success"] = True
                    result["response_length"] = len(ai_response)
                else:
                    result["error_type"] = "empty_response"
                    result["error_message"] = "Réponse vide ou trop courte"
            else:
                result["error_type"] = f"http_error_{response.status_code}"
                result["error_message"] = response.text[:200]
        
        except Exception as e:
            result["error_type"] = "unexpected_error"
            result["error_message"] = str(e)
        
        return result
    
    async def run_stress_test(self):
        """Exécute le test de charge"""
        print("[ROCKET] Démarrage du test de charge (5000 questions)...")
        print(f"📍 Serveur: {self.base_url}")
        print(f"⏱️  Timeout: {TIMEOUT}s")
        print(f"[STOP] Arrêt sur erreur critique: {'Oui' if STOP_ON_ERROR else 'Non'}\n")
        
        # Récupérer les experts
        print("📋 Récupération de la liste des experts...")
        self.experts_list = await self.get_experts()
        if not self.experts_list:
            print("[ERR] Aucun expert trouvé. Arrêt du test.")
            return {
                "error": "Aucun expert disponible",
                "timestamp": datetime.now().isoformat(),
                "base_url": self.base_url,
                "summary": {
                    "total_questions": 0,
                    "successful": 0,
                    "failed": 0,
                    "success_rate": "0%",
                }
            }
        
        print(f"[OK] {len(self.experts_list)} experts trouvés\n")
        print("=" * 70)
        print("🧪 DÉBUT DES TESTS")
        print("=" * 70)
        
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            question_num = 0
            
            # Test avec les experts
            for i in range(self.max_questions):
                if self.stop_requested:
                    print(f"\n[STOP] ARRÊT DEMANDÉ - Erreur critique détectée à la question {question_num}")
                    break
                
                question_num += 1
                self.stats["total"] += 1
                
                # Choisir un expert aléatoire
                expert_id = random.choice(self.experts_list)
                
                # Choisir une question aléatoire pour cet expert
                if expert_id in QUESTION_TEMPLATES:
                    question = random.choice(QUESTION_TEMPLATES[expert_id])
                else:
                    question = "Bonjour, comment ça va ?"
                
                # Tester
                result = await self.test_expert_question(
                    expert_id, question, client, question_num
                )
                
                self.results.append(result)
                
                if result["success"]:
                    self.stats["successful"] += 1
                    if question_num % 100 == 0:
                        print(f"[OK] Question {question_num}: {expert_id} - OK (temps: {result['processing_time_ms']:.0f}ms)")
                else:
                    self.stats["failed"] += 1
                    self.errors.append(result)
                    print(f"\n[ERR] ERREUR Question {question_num}:")
                    print(f"   Expert: {expert_id}")
                    print(f"   Question: {question[:50]}...")
                    print(f"   Type: {result['error_type']}")
                    print(f"   Message: {result.get('error_message', 'N/A')[:100]}")
                    
                    if STOP_ON_ERROR and result.get("error_type") and self.is_critical_error(result["error_type"]):
                        print(f"\n[STOP] ERREUR CRITIQUE DÉTECTÉE - Arrêt du test")
                        break
                
                # Pause minimale pour ne pas surcharger
                if question_num % 10 == 0:
                    await asyncio.sleep(0.1)
                
                # Afficher progression
                if question_num % 50 == 0:
                    success_rate = (self.stats["successful"] / self.stats["total"] * 100) if self.stats["total"] > 0 else 0
                    print(f"\n📊 Progression: {question_num}/{self.max_questions} | "
                          f"Succès: {self.stats['successful']} | "
                          f"Échecs: {self.stats['failed']} | "
                          f"Taux: {success_rate:.1f}%")
        
        # Générer le rapport
        return self.generate_report()
    
    def generate_report(self) -> Dict:
        """Génère un rapport détaillé"""
        total_time = time.time() - self.start_time
        
        # Statistiques de temps
        successful_results = [r for r in self.results if r.get("success", False)]
        avg_time = sum(r.get("processing_time_ms", 0) for r in successful_results) / len(successful_results) if successful_results else 0
        
        # Taux de succès
        success_rate = (self.stats["successful"] / self.stats["total"] * 100) if self.stats["total"] > 0 else 0
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "base_url": self.base_url,
            "summary": {
                "total_questions": self.stats["total"],
                "successful": self.stats["successful"],
                "failed": self.stats["failed"],
                "success_rate": f"{success_rate:.2f}%",
                "timeouts": self.stats["timeouts"],
                "invalid_responses": self.stats["invalid_responses"],
                "slow_responses": self.stats["slow_responses"],
                "average_response_time_ms": round(avg_time, 2),
                "total_time_seconds": round(total_time, 2),
                "questions_per_second": round(self.stats["total"] / total_time, 2) if total_time > 0 else 0,
            },
            "errors_by_type": dict(self.stats["errors_by_type"]),
            "errors_by_expert": dict(self.stats["errors_by_expert"]),
            "critical_errors": [
                r for r in self.errors 
                if r.get("error_type") and self.is_critical_error(r["error_type"])
            ],
            "all_errors": self.errors[:100],  # Limiter à 100 erreurs pour le rapport
            "stop_requested": self.stop_requested,
        }
        
        return report
    
    def print_report(self, report: Dict):
        """Affiche le rapport"""
        print("\n" + "=" * 70)
        print("📊 RAPPORT DE TEST DE CHARGE")
        print("=" * 70)
        
        summary = report.get("summary", {})
        print(f"\n📈 STATISTIQUES GÉNÉRALES")
        print(f"   Total de questions: {summary.get('total_questions', 0)}")
        print(f"   [OK] Réussies: {summary.get('successful', 0)}")
        print(f"   [ERR] Échouées: {summary.get('failed', 0)}")
        print(f"   📊 Taux de succès: {summary.get('success_rate', '0%')}")
        print(f"   ⏱️  Temps moyen: {summary.get('average_response_time_ms', 0):.0f}ms")
        print(f"   ⏰ Temps total: {summary.get('total_time_seconds', 0):.1f}s")
        print(f"   [ROCKET] Questions/seconde: {summary.get('questions_per_second', 0):.2f}")
        
        print(f"\n[WARN]  ERREURS DÉTECTÉES")
        print(f"   Timeouts: {summary.get('timeouts', 0)}")
        print(f"   Réponses invalides: {summary.get('invalid_responses', 0)}")
        print(f"   Réponses lentes (>15s): {summary.get('slow_responses', 0)}")
        
        errors_by_type = report.get("errors_by_type", {})
        if errors_by_type:
            print(f"\n📋 ERREURS PAR TYPE:")
            for error_type, count in sorted(errors_by_type.items(), key=lambda x: x[1], reverse=True):
                print(f"   - {error_type}: {count}")
        
        errors_by_expert = report.get("errors_by_expert", {})
        if errors_by_expert:
            print(f"\n👤 ERREURS PAR EXPERT:")
            for expert_id, count in sorted(errors_by_expert.items(), key=lambda x: x[1], reverse=True):
                print(f"   - {expert_id}: {count}")
        
        critical_errors = report.get("critical_errors", [])
        if critical_errors:
            print(f"\n🚨 ERREURS CRITIQUES ({len(critical_errors)}):")
            for error in critical_errors[:10]:  # Afficher les 10 premières
                print(f"   Question {error.get('question_num')}: {error.get('error_type')} - {error.get('error_message', '')[:80]}")
        
        if report.get("stop_requested"):
            print(f"\n[STOP] TEST ARRÊTÉ - Erreur critique détectée")
        
        print("\n" + "=" * 70)


async def main():
    """Fonction principale"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Test de charge avec détection d'erreurs")
    parser.add_argument("--url", default=BASE_URL, help=f"URL du serveur (défaut: {BASE_URL})")
    parser.add_argument("--max", type=int, default=MAX_QUESTIONS, help=f"Nombre max de questions (défaut: {MAX_QUESTIONS})")
    parser.add_argument("--output", help="Fichier JSON pour sauvegarder le rapport")
    parser.add_argument("--no-stop", action="store_true", help="Ne pas s'arrêter sur erreur critique")
    
    args = parser.parse_args()
    
    global STOP_ON_ERROR
    STOP_ON_ERROR = not args.no_stop
    
    tester = StressTester(base_url=args.url, max_questions=args.max)
    report = await tester.run_stress_test()
    
    if report and isinstance(report, dict):
        tester.print_report(report)
    else:
        print("\n[ERR] Le test n'a pas pu générer de rapport.")
        print("   Vérifiez que le serveur est accessible et que les experts sont disponibles.")
        return 1
    
    # Sauvegarder le rapport
    if args.output and report and isinstance(report, dict):
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"\n💾 Rapport sauvegardé dans: {args.output}")
    
    # Code de retour
    if not report or not isinstance(report, dict):
        return 1
    if report.get("critical_errors") or report.get("stop_requested"):
        return 1
    if report.get("summary", {}).get("failed", 0) > 0:
        return 1
    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)


Génère 5000 questions/réponses et détecte les erreurs
S'arrête automatiquement en cas d'erreur critique
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

import asyncio
import httpx
import time
import random
from typing import Dict, List, Tuple, Optional
from datetime import datetime
import json
from collections import defaultdict

# Configuration
BASE_URL = "http://localhost:8000"
TIMEOUT = 30.0
MAX_QUESTIONS = 5000
STOP_ON_ERROR = True  # S'arrêter dès qu'une erreur critique est détectée

# Questions variées pour tester différents scénarios
QUESTION_TEMPLATES = {
    "health": [
        "Quels sont les bienfaits du sommeil ?",
        "Comment fonctionne le système immunitaire ?",
        "C'est quoi une alimentation équilibrée ?",
        "Quels sont les symptômes du stress ?",
        "Comment améliorer sa mémoire ?",
    ],
    "finance": [
        "Quel est le cours du Bitcoin ?",
        "C'est quoi un ETF ?",
        "Comment fonctionnent les actions ?",
        "Quelle est la différence entre crypto et actions ?",
        "Comment investir en bourse ?",
    ],
    "weather": [
        "Météo Paris demain ?",
        "Il va pleuvoir ce week-end ?",
        "Quel temps à New York ?",
        "Température à Londres aujourd'hui ?",
        "Prévisions météo pour la semaine ?",
    ],
    "tech": [
        "C'est quoi ChatGPT ?",
        "Comment fonctionne l'IA ?",
        "Quel smartphone choisir ?",
        "Les dernières news tech ?",
        "C'est quoi le machine learning ?",
    ],
    "general": [
        "Qui a inventé Internet ?",
        "Pourquoi le ciel est bleu ?",
        "C'est quoi l'IA ?",
        "Quelle est la capitale de la France ?",
        "Comment fonctionne la photosynthèse ?",
    ],
    "humor": [
        "Raconte-moi une blague !",
        "Un jeu de mots ?",
        "Fais-moi rire !",
        "Une blague sur les ordinateurs ?",
        "Blague de Toto ?",
    ],
    "cuisine": [
        "Une recette de carbonara ?",
        "Idée dessert facile ?",
        "Comment réussir une omelette ?",
        "Recette de gâteau au chocolat ?",
        "Comment faire du pain ?",
    ],
    "cinema": [
        "Un bon film ce soir ?",
        "Les meilleures séries Netflix ?",
        "C'est quoi le dernier Marvel ?",
        "Film d'horreur à voir ?",
        "Meilleur film 2024 ?",
    ],
    "sports": [
        "Quels sont les derniers résultats foot ?",
        "Comment débuter la course à pied ?",
        "Quels exercices pour se muscler ?",
        "Actualités sportives ?",
        "Qui a gagné le dernier match ?",
    ],
    "news": [
        "Actualités du jour ?",
        "News tech récentes ?",
        "Quoi de neuf dans le monde ?",
        "Dernières nouvelles ?",
        "Actualités importantes ?",
    ],
    "horoscope": [
        "Horoscope Bélier aujourd'hui ?",
        "Compatibilité Lion et Scorpion ?",
        "Prédictions pour la Balance ?",
        "Horoscope du jour ?",
        "Signe astrologique ?",
    ],
    "prenom": [
        "Que signifie le prénom Emma ?",
        "Origine du prénom Lucas ?",
        "Prénoms tendance 2024 ?",
        "Signification du prénom Marie ?",
        "Histoire du prénom Jean ?",
    ],
    "history": [
        "Que s'est-il passé aujourd'hui dans l'histoire ?",
        "Célébrités nées le 15 mars ?",
        "Événements du 14 juillet ?",
        "Histoire de la Révolution française ?",
        "Qui a découvert l'Amérique ?",
    ],
    "tourism": [
        "Quel temps fait-il à Paris ?",
        "Que visiter à Tokyo ?",
        "Meilleure période pour la Thaïlande ?",
        "Conseils voyage en Italie ?",
        "Destinations à voir ?",
    ],
    "love": [
        "Comment mieux communiquer en couple ?",
        "Comment se remettre d'une rupture ?",
        "Comment se faire des amis ?",
        "Conseils pour une relation ?",
        "Comment gérer les conflits ?",
    ],
    "gaming": [
        "Les meilleurs jeux 2024 ?",
        "Tips pour Fortnite ?",
        "Actus esports ?",
        "Jeux à jouer en ce moment ?",
        "Recommandations de jeux ?",
    ],
}

# Questions pour le chat général
GENERAL_CHAT_QUESTIONS = [
    "Bonjour, comment ça va ?",
    "Quelle est la capitale de la France ?",
    "Explique-moi l'intelligence artificielle",
    "C'est quoi Python ?",
    "Comment ça marche Internet ?",
    "Qui est Einstein ?",
    "C'est quoi la photosynthèse ?",
    "Explique-moi la gravité",
    "Quelle est la différence entre HTTP et HTTPS ?",
    "C'est quoi un algorithme ?",
]


class StressTester:
    """Testeur de charge avec détection d'erreurs"""
    
    def __init__(self, base_url: str = BASE_URL, max_questions: int = MAX_QUESTIONS):
        self.base_url = base_url
        self.max_questions = max_questions
        self.results: List[Dict] = []
        self.errors: List[Dict] = []
        self.warnings: List[Dict] = []
        self.stats = {
            "total": 0,
            "successful": 0,
            "failed": 0,
            "timeouts": 0,
            "invalid_responses": 0,
            "slow_responses": 0,
            "errors_by_type": defaultdict(int),
            "errors_by_expert": defaultdict(int),
        }
        self.start_time = time.time()
        self.experts_list: List[str] = []
        self.stop_requested = False
    
    async def get_experts(self) -> List[str]:
        """Récupère la liste des experts"""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(f"{self.base_url}/api/expert/list")
                if response.status_code == 200:
                    experts = response.json()
                    return [e.get("id") for e in experts if e.get("id")]
                return []
        except Exception as e:
            print(f"[ERR] Erreur lors de la récupération des experts: {e}")
            return []
    
    def is_critical_error(self, error_type: str) -> bool:
        """Détermine si une erreur est critique"""
        critical_errors = [
            "server_unavailable",
            "timeout",
            "invalid_response_format",
            "empty_response",
            "api_error_500",
        ]
        return error_type in critical_errors
    
    async def test_expert_question(
        self,
        expert_id: str,
        question: str,
        client: httpx.AsyncClient,
        question_num: int
    ) -> Dict:
        """Teste une question avec un expert"""
        result = {
            "question_num": question_num,
            "expert_id": expert_id,
            "question": question,
            "success": False,
            "error_type": None,
            "error_message": None,
            "response_length": 0,
            "processing_time_ms": 0,
            "timestamp": datetime.now().isoformat(),
        }
        
        try:
            start_time = time.time()
            
            response = await client.post(
                f"{self.base_url}/api/expert/{expert_id}/chat",
                json={"message": question, "language": "fr"},
                timeout=TIMEOUT
            )
            
            processing_time = (time.time() - start_time) * 1000
            result["processing_time_ms"] = round(processing_time, 2)
            
            # Vérifier le status code
            if response.status_code != 200:
                result["error_type"] = f"http_error_{response.status_code}"
                result["error_message"] = response.text[:200]
                result["success"] = False
                self.stats["errors_by_type"][result["error_type"]] += 1
                self.stats["errors_by_expert"][expert_id] += 1
                
                if response.status_code == 500:
                    result["error_type"] = "api_error_500"
                    if STOP_ON_ERROR and self.is_critical_error("api_error_500"):
                        self.stop_requested = True
                
                return result
            
            # Parser la réponse
            try:
                data = response.json()
            except Exception as e:
                result["error_type"] = "invalid_response_format"
                result["error_message"] = f"JSON parse error: {str(e)}"
                result["success"] = False
                self.stats["errors_by_type"]["invalid_response_format"] += 1
                
                if STOP_ON_ERROR and self.is_critical_error("invalid_response_format"):
                    self.stop_requested = True
                
                return result
            
            ai_response = data.get("response", "")
            
            # Vérifier si la réponse est vide
            if not ai_response or len(ai_response.strip()) == 0:
                result["error_type"] = "empty_response"
                result["error_message"] = "Réponse vide reçue"
                result["success"] = False
                self.stats["errors_by_type"]["empty_response"] += 1
                
                if STOP_ON_ERROR and self.is_critical_error("empty_response"):
                    self.stop_requested = True
                
                return result
            
            # Vérifier la longueur minimale
            if len(ai_response) < 10:
                result["error_type"] = "response_too_short"
                result["error_message"] = f"Réponse trop courte: {len(ai_response)} caractères"
                result["success"] = False
                self.stats["errors_by_type"]["response_too_short"] += 1
                return result
            
            # Vérifier les mots d'erreur
            response_lower = ai_response.lower()
            error_keywords = ["erreur", "error", "impossible", "échec", "failed", "exception"]
            if any(kw in response_lower for kw in error_keywords):
                result["error_type"] = "error_in_response"
                result["error_message"] = "Réponse contient des mots d'erreur"
                result["warnings"] = True
                # Non critique mais à noter
            
            # Vérifier le temps de réponse
            if processing_time > 15000:  # Plus de 15 secondes
                result["error_type"] = "slow_response"
                result["warnings"] = True
                self.stats["slow_responses"] += 1
            
            result["response_length"] = len(ai_response)
            result["success"] = True
            
        except httpx.TimeoutException:
            result["error_type"] = "timeout"
            result["error_message"] = f"Timeout après {TIMEOUT}s"
            result["success"] = False
            self.stats["timeouts"] += 1
            self.stats["errors_by_type"]["timeout"] += 1
            self.stats["errors_by_expert"][expert_id] += 1
            
            if STOP_ON_ERROR and self.is_critical_error("timeout"):
                self.stop_requested = True
        
        except httpx.ConnectError:
            result["error_type"] = "server_unavailable"
            result["error_message"] = "Serveur inaccessible"
            result["success"] = False
            self.stats["errors_by_type"]["server_unavailable"] += 1
            
            if STOP_ON_ERROR and self.is_critical_error("server_unavailable"):
                self.stop_requested = True
        
        except Exception as e:
            result["error_type"] = "unexpected_error"
            result["error_message"] = str(e)
            result["success"] = False
            self.stats["errors_by_type"]["unexpected_error"] += 1
        
        return result
    
    async def test_general_chat(
        self,
        question: str,
        client: httpx.AsyncClient,
        question_num: int
    ) -> Dict:
        """Teste le chat général"""
        result = {
            "question_num": question_num,
            "endpoint": "chat",
            "question": question,
            "success": False,
            "error_type": None,
            "error_message": None,
            "processing_time_ms": 0,
            "timestamp": datetime.now().isoformat(),
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
                ai_response = data.get("response", "")
                if ai_response and len(ai_response) > 10:
                    result["success"] = True
                    result["response_length"] = len(ai_response)
                else:
                    result["error_type"] = "empty_response"
                    result["error_message"] = "Réponse vide ou trop courte"
            else:
                result["error_type"] = f"http_error_{response.status_code}"
                result["error_message"] = response.text[:200]
        
        except Exception as e:
            result["error_type"] = "unexpected_error"
            result["error_message"] = str(e)
        
        return result
    
    async def run_stress_test(self):
        """Exécute le test de charge"""
        print("[ROCKET] Démarrage du test de charge (5000 questions)...")
        print(f"📍 Serveur: {self.base_url}")
        print(f"⏱️  Timeout: {TIMEOUT}s")
        print(f"[STOP] Arrêt sur erreur critique: {'Oui' if STOP_ON_ERROR else 'Non'}\n")
        
        # Récupérer les experts
        print("📋 Récupération de la liste des experts...")
        self.experts_list = await self.get_experts()
        if not self.experts_list:
            print("[ERR] Aucun expert trouvé. Arrêt du test.")
            return {
                "error": "Aucun expert disponible",
                "timestamp": datetime.now().isoformat(),
                "base_url": self.base_url,
                "summary": {
                    "total_questions": 0,
                    "successful": 0,
                    "failed": 0,
                    "success_rate": "0%",
                }
            }
        
        print(f"[OK] {len(self.experts_list)} experts trouvés\n")
        print("=" * 70)
        print("🧪 DÉBUT DES TESTS")
        print("=" * 70)
        
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            question_num = 0
            
            # Test avec les experts
            for i in range(self.max_questions):
                if self.stop_requested:
                    print(f"\n[STOP] ARRÊT DEMANDÉ - Erreur critique détectée à la question {question_num}")
                    break
                
                question_num += 1
                self.stats["total"] += 1
                
                # Choisir un expert aléatoire
                expert_id = random.choice(self.experts_list)
                
                # Choisir une question aléatoire pour cet expert
                if expert_id in QUESTION_TEMPLATES:
                    question = random.choice(QUESTION_TEMPLATES[expert_id])
                else:
                    question = "Bonjour, comment ça va ?"
                
                # Tester
                result = await self.test_expert_question(
                    expert_id, question, client, question_num
                )
                
                self.results.append(result)
                
                if result["success"]:
                    self.stats["successful"] += 1
                    if question_num % 100 == 0:
                        print(f"[OK] Question {question_num}: {expert_id} - OK (temps: {result['processing_time_ms']:.0f}ms)")
                else:
                    self.stats["failed"] += 1
                    self.errors.append(result)
                    print(f"\n[ERR] ERREUR Question {question_num}:")
                    print(f"   Expert: {expert_id}")
                    print(f"   Question: {question[:50]}...")
                    print(f"   Type: {result['error_type']}")
                    print(f"   Message: {result.get('error_message', 'N/A')[:100]}")
                    
                    if STOP_ON_ERROR and result.get("error_type") and self.is_critical_error(result["error_type"]):
                        print(f"\n[STOP] ERREUR CRITIQUE DÉTECTÉE - Arrêt du test")
                        break
                
                # Pause minimale pour ne pas surcharger
                if question_num % 10 == 0:
                    await asyncio.sleep(0.1)
                
                # Afficher progression
                if question_num % 50 == 0:
                    success_rate = (self.stats["successful"] / self.stats["total"] * 100) if self.stats["total"] > 0 else 0
                    print(f"\n📊 Progression: {question_num}/{self.max_questions} | "
                          f"Succès: {self.stats['successful']} | "
                          f"Échecs: {self.stats['failed']} | "
                          f"Taux: {success_rate:.1f}%")
        
        # Générer le rapport
        return self.generate_report()
    
    def generate_report(self) -> Dict:
        """Génère un rapport détaillé"""
        total_time = time.time() - self.start_time
        
        # Statistiques de temps
        successful_results = [r for r in self.results if r.get("success", False)]
        avg_time = sum(r.get("processing_time_ms", 0) for r in successful_results) / len(successful_results) if successful_results else 0
        
        # Taux de succès
        success_rate = (self.stats["successful"] / self.stats["total"] * 100) if self.stats["total"] > 0 else 0
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "base_url": self.base_url,
            "summary": {
                "total_questions": self.stats["total"],
                "successful": self.stats["successful"],
                "failed": self.stats["failed"],
                "success_rate": f"{success_rate:.2f}%",
                "timeouts": self.stats["timeouts"],
                "invalid_responses": self.stats["invalid_responses"],
                "slow_responses": self.stats["slow_responses"],
                "average_response_time_ms": round(avg_time, 2),
                "total_time_seconds": round(total_time, 2),
                "questions_per_second": round(self.stats["total"] / total_time, 2) if total_time > 0 else 0,
            },
            "errors_by_type": dict(self.stats["errors_by_type"]),
            "errors_by_expert": dict(self.stats["errors_by_expert"]),
            "critical_errors": [
                r for r in self.errors 
                if r.get("error_type") and self.is_critical_error(r["error_type"])
            ],
            "all_errors": self.errors[:100],  # Limiter à 100 erreurs pour le rapport
            "stop_requested": self.stop_requested,
        }
        
        return report
    
    def print_report(self, report: Dict):
        """Affiche le rapport"""
        print("\n" + "=" * 70)
        print("📊 RAPPORT DE TEST DE CHARGE")
        print("=" * 70)
        
        summary = report.get("summary", {})
        print(f"\n📈 STATISTIQUES GÉNÉRALES")
        print(f"   Total de questions: {summary.get('total_questions', 0)}")
        print(f"   [OK] Réussies: {summary.get('successful', 0)}")
        print(f"   [ERR] Échouées: {summary.get('failed', 0)}")
        print(f"   📊 Taux de succès: {summary.get('success_rate', '0%')}")
        print(f"   ⏱️  Temps moyen: {summary.get('average_response_time_ms', 0):.0f}ms")
        print(f"   ⏰ Temps total: {summary.get('total_time_seconds', 0):.1f}s")
        print(f"   [ROCKET] Questions/seconde: {summary.get('questions_per_second', 0):.2f}")
        
        print(f"\n[WARN]  ERREURS DÉTECTÉES")
        print(f"   Timeouts: {summary.get('timeouts', 0)}")
        print(f"   Réponses invalides: {summary.get('invalid_responses', 0)}")
        print(f"   Réponses lentes (>15s): {summary.get('slow_responses', 0)}")
        
        errors_by_type = report.get("errors_by_type", {})
        if errors_by_type:
            print(f"\n📋 ERREURS PAR TYPE:")
            for error_type, count in sorted(errors_by_type.items(), key=lambda x: x[1], reverse=True):
                print(f"   - {error_type}: {count}")
        
        errors_by_expert = report.get("errors_by_expert", {})
        if errors_by_expert:
            print(f"\n👤 ERREURS PAR EXPERT:")
            for expert_id, count in sorted(errors_by_expert.items(), key=lambda x: x[1], reverse=True):
                print(f"   - {expert_id}: {count}")
        
        critical_errors = report.get("critical_errors", [])
        if critical_errors:
            print(f"\n🚨 ERREURS CRITIQUES ({len(critical_errors)}):")
            for error in critical_errors[:10]:  # Afficher les 10 premières
                print(f"   Question {error.get('question_num')}: {error.get('error_type')} - {error.get('error_message', '')[:80]}")
        
        if report.get("stop_requested"):
            print(f"\n[STOP] TEST ARRÊTÉ - Erreur critique détectée")
        
        print("\n" + "=" * 70)


async def main():
    """Fonction principale"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Test de charge avec détection d'erreurs")
    parser.add_argument("--url", default=BASE_URL, help=f"URL du serveur (défaut: {BASE_URL})")
    parser.add_argument("--max", type=int, default=MAX_QUESTIONS, help=f"Nombre max de questions (défaut: {MAX_QUESTIONS})")
    parser.add_argument("--output", help="Fichier JSON pour sauvegarder le rapport")
    parser.add_argument("--no-stop", action="store_true", help="Ne pas s'arrêter sur erreur critique")
    
    args = parser.parse_args()
    
    global STOP_ON_ERROR
    STOP_ON_ERROR = not args.no_stop
    
    tester = StressTester(base_url=args.url, max_questions=args.max)
    report = await tester.run_stress_test()
    
    if report and isinstance(report, dict):
        tester.print_report(report)
    else:
        print("\n[ERR] Le test n'a pas pu générer de rapport.")
        print("   Vérifiez que le serveur est accessible et que les experts sont disponibles.")
        return 1
    
    # Sauvegarder le rapport
    if args.output and report and isinstance(report, dict):
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"\n💾 Rapport sauvegardé dans: {args.output}")
    
    # Code de retour
    if not report or not isinstance(report, dict):
        return 1
    if report.get("critical_errors") or report.get("stop_requested"):
        return 1
    if report.get("summary", {}).get("failed", 0) > 0:
        return 1
    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)

