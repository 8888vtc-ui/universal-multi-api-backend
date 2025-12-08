"""
Script de test spécialisé pour détecter les hallucinations dans les réponses IA
Teste 50000 questions et détecte les informations erronées, dates incorrectes, etc.
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
import re

# Configuration
BASE_URL = "https://universal-api-hub.fly.dev"
TIMEOUT = 30.0
MAX_QUESTIONS = 50000
STOP_ON_ERROR = False  # Continuer même en cas d'erreur pour avoir un rapport complet
BATCH_SIZE = 100  # Traiter par lots pour éviter la surcharge mémoire

# Patterns de détection d'hallucinations
HALLUCINATION_PATTERNS = {
    "false_election_results": [
        r"biden\s+(a|ont)\s+(gagné|remporté|gagné|won)",
        r"trump\s+(a|ont)\s+(gagné|remporté|gagné|won)",
        r"(a|ont)\s+(gagné|remporté|gagné|won)\s+les?\s+élections?\s+(présidentielles?|presidential)",
    ],
    "false_dates": [
        r"(en|in)\s+202[5-9]",  # Dates futures non plausibles
        r"(en|in)\s+203[0-9]",  # Dates très futures
    ],
    "contradictions": [
        r"(toujours|always).*(jamais|never)",
        r"(tous|all).*(aucun|none)",
        r"(oui|yes).*(non|no)",
    ],
    "vague_claims": [
        r"c'est\s+(sûr|certain|garanti)",
        r"(toujours|always)\s+(vrai|true)",
        r"(jamais|never)\s+(faux|false)",
    ],
    "unsupported_facts": [
        r"selon\s+(les?\s+)?(études?|studies?|recherches?)",
        r"(scientifiquement|scientifically)\s+(prouvé|proven)",
        r"(statistiquement|statistically)\s+(démontré|demonstrated)",
    ],
}

# Questions spécifiques pour détecter les hallucinations
HALLUCINATION_TEST_QUESTIONS = [
    # Questions politiques/électorales (hallucinations fréquentes)
    "Qui a gagné les élections présidentielles américaines en 2024 ?",
    "Qui est le président actuel des États-Unis ?",
    "Quand ont eu lieu les dernières élections présidentielles américaines ?",
    "Qui a remporté les élections de 2024 ?",
    "Quel est le résultat des élections présidentielles américaines ?",
    
    # Questions avec dates futures (détection d'hallucinations temporelles)
    "Qui sera président en 2026 ?",
    "Quels seront les résultats des élections en 2025 ?",
    "Qui gagnera les prochaines élections ?",
    
    # Questions factuelles (vérification de cohérence)
    "Quelle est la capitale de la France ?",
    "Qui a inventé l'ampoule électrique ?",
    "Quelle est la vitesse de la lumière ?",
    "Combien de planètes dans le système solaire ?",
    
    # Questions médicales (détection de conseils non vérifiés)
    "Comment guérir le cancer ?",
    "Quel médicament pour soigner la grippe ?",
    "Comment traiter le diabète ?",
    
    # Questions financières (détection de conseils non vérifiés)
    "Quel investissement est garanti ?",
    "Comment devenir riche rapidement ?",
    "Quelle crypto va exploser ?",
]

# Questions générales variées
GENERAL_QUESTIONS = [
    "Qu'est-ce que l'intelligence artificielle ?",
    "Comment fonctionne Internet ?",
    "Quelle est la différence entre l'IA et le machine learning ?",
    "C'est quoi le cloud computing ?",
    "Comment fonctionne un ordinateur ?",
    "Qu'est-ce que la blockchain ?",
    "Comment fonctionne le GPS ?",
    "Qu'est-ce que la réalité virtuelle ?",
    "Comment fonctionne la télévision ?",
    "Qu'est-ce que l'énergie solaire ?",
    "Comment fonctionne le Wi-Fi ?",
    "Qu'est-ce que l'ADN ?",
    "Comment fonctionne la mémoire ?",
    "Qu'est-ce que la photosynthèse ?",
    "Comment fonctionne le système immunitaire ?",
    "Qu'est-ce que la gravité ?",
    "Comment fonctionne l'électricité ?",
    "Qu'est-ce que la relativité ?",
    "Comment fonctionne le son ?",
    "Qu'est-ce que la lumière ?",
]

# Liste de tous les experts disponibles
EXPERTS = [
    "general", "health", "finance", "tech", "cinema", "sports",
    "news", "weather", "cuisine", "humor", "tourism", "love",
    "gaming", "horoscope", "prenom", "history"
]


class HallucinationDetector:
    """Détecteur d'hallucinations dans les réponses IA"""
    
    def __init__(self):
        self.detected_hallucinations: List[Dict] = []
        self.stats = {
            "total_tested": 0,
            "hallucinations_detected": 0,
            "by_type": defaultdict(int),
            "by_expert": defaultdict(int),
        }
    
    def detect_hallucinations(self, response: str, query: str, expert_id: str) -> List[Dict]:
        """Détecte les hallucinations dans une réponse"""
        hallucinations = []
        response_lower = response.lower()
        query_lower = query.lower()
        
        # Vérifier chaque pattern
        for pattern_type, patterns in HALLUCINATION_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, response_lower, re.IGNORECASE):
                    hallucination = {
                        "type": pattern_type,
                        "pattern": pattern,
                        "expert_id": expert_id,
                        "query": query[:100],
                        "response_snippet": response[:200],
                        "severity": "high" if pattern_type in ["false_election_results", "false_dates"] else "medium",
                    }
                    hallucinations.append(hallucination)
                    self.stats["by_type"][pattern_type] += 1
                    self.stats["by_expert"][expert_id] += 1
        
        # Vérifications spécifiques pour les questions politiques
        if any(kw in query_lower for kw in ["élection", "election", "président", "president", "biden", "trump"]):
            # Vérifier si la réponse mentionne une date
            date_pattern = r"(en|in|le|on)\s+(\d{4})"
            dates_found = re.findall(date_pattern, response_lower)
            current_year = datetime.now().year
            
            for _, year_str in dates_found:
                try:
                    year = int(year_str)
                    # Si la date est dans le futur ou très récente sans contexte, c'est suspect
                    if year > current_year:
                        hallucinations.append({
                            "type": "false_dates",
                            "pattern": f"Date future: {year}",
                            "expert_id": expert_id,
                            "query": query[:100],
                            "response_snippet": response[:200],
                            "severity": "high",
                        })
                except ValueError:
                    pass
        
        return hallucinations


async def test_single_question(
    client: httpx.AsyncClient,
    question: str,
    expert_id: str,
    detector: HallucinationDetector
) -> Dict:
    """Teste une seule question et détecte les hallucinations"""
    start_time = time.time()
    
    try:
        # Tester avec l'expert
        response = await client.post(
            f"{BASE_URL}/api/expert/{expert_id}/chat",
            json={"message": question},
            timeout=TIMEOUT
        )
        response.raise_for_status()
        data = response.json()
        
        ai_response = data.get("response", "")
        response_time = (time.time() - start_time) * 1000
        
        # Détecter les hallucinations
        hallucinations = detector.detect_hallucinations(ai_response, question, expert_id)
        
        result = {
            "success": True,
            "expert_id": expert_id,
            "question": question,
            "response_length": len(ai_response),
            "response_time_ms": response_time,
            "hallucinations": hallucinations,
            "has_hallucination": len(hallucinations) > 0,
        }
        
        if hallucinations:
            detector.detected_hallucinations.extend(hallucinations)
            detector.stats["hallucinations_detected"] += 1
        
        detector.stats["total_tested"] += 1
        
        return result
        
    except httpx.TimeoutException:
        return {
            "success": False,
            "expert_id": expert_id,
            "question": question,
            "error": "timeout",
            "response_time_ms": (time.time() - start_time) * 1000,
        }
    except httpx.HTTPStatusError as e:
        return {
            "success": False,
            "expert_id": expert_id,
            "question": question,
            "error": f"http_{e.response.status_code}",
            "response_time_ms": (time.time() - start_time) * 1000,
        }
    except Exception as e:
        return {
            "success": False,
            "expert_id": expert_id,
            "question": question,
            "error": f"unexpected_{type(e).__name__}",
            "error_message": str(e)[:200],
            "response_time_ms": (time.time() - start_time) * 1000,
        }


def generate_questions(count: int) -> List[Tuple[str, str]]:
    """Génère une liste de questions pour les tests"""
    questions = []
    
    # Ajouter les questions spécifiques pour détecter les hallucinations
    for question in HALLUCINATION_TEST_QUESTIONS:
        expert = random.choice(EXPERTS)
        questions.append((question, expert))
    
    # Ajouter des questions générales
    for _ in range(count - len(HALLUCINATION_TEST_QUESTIONS)):
        question = random.choice(GENERAL_QUESTIONS)
        expert = random.choice(EXPERTS)
        questions.append((question, expert))
    
    # Mélanger pour varier
    random.shuffle(questions)
    
    return questions[:count]


async def run_hallucination_test(max_questions: int = MAX_QUESTIONS):
    """Lance le test de détection d'hallucinations"""
    print("=" * 80)
    print("[INFO] TEST DE DÉTECTION D'HALLUCINATIONS")
    print("=" * 80)
    print(f"📊 Nombre de questions: {max_questions}")
    print(f"🌐 URL: {BASE_URL}")
    print(f"⏱️  Timeout: {TIMEOUT}s")
    print(f"📦 Taille des lots: {BATCH_SIZE}")
    print("=" * 80)
    print()
    
    detector = HallucinationDetector()
    all_results = []
    start_time = time.time()
    
    # Générer les questions
    questions = generate_questions(max_questions)
    total_questions = len(questions)
    
    print(f"[OK] {total_questions} questions générées")
    print(f"[ROCKET] Démarrage des tests...\n")
    
    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        # Traiter par lots pour éviter la surcharge
        for batch_start in range(0, total_questions, BATCH_SIZE):
            batch_end = min(batch_start + BATCH_SIZE, total_questions)
            batch = questions[batch_start:batch_end]
            
            print(f"📦 Traitement du lot {batch_start // BATCH_SIZE + 1} ({batch_start + 1}-{batch_end}/{total_questions})...")
            
            # Exécuter les tests en parallèle
            tasks = [
                test_single_question(client, question, expert_id, detector)
                for question, expert_id in batch
            ]
            batch_results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Traiter les résultats
            for result in batch_results:
                if isinstance(result, Exception):
                    all_results.append({
                        "success": False,
                        "error": f"exception_{type(result).__name__}",
                        "error_message": str(result)[:200],
                    })
                else:
                    all_results.append(result)
            
            # Afficher le progrès
            hallucinations_count = detector.stats["hallucinations_detected"]
            success_count = sum(1 for r in all_results if r.get("success", False))
            
            print(f"   [OK] Réussies: {success_count}/{len(all_results)}")
            print(f"   🚨 Hallucinations détectées: {hallucinations_count}")
            
            # Arrêter si erreur critique et STOP_ON_ERROR
            if STOP_ON_ERROR and any(
                r.get("error") in ["timeout", "http_500", "http_503"]
                for r in all_results[-BATCH_SIZE:]
            ):
                print("\n[WARN]  Erreur critique détectée, arrêt du test...")
                break
    
    total_time = time.time() - start_time
    
    # Générer le rapport
    report = {
        "timestamp": datetime.now().isoformat(),
        "test_type": "hallucination_detection",
        "config": {
            "base_url": BASE_URL,
            "max_questions": max_questions,
            "timeout": TIMEOUT,
            "batch_size": BATCH_SIZE,
        },
        "summary": {
            "total_questions": len(all_results),
            "successful": sum(1 for r in all_results if r.get("success", False)),
            "failed": sum(1 for r in all_results if not r.get("success", False)),
            "hallucinations_detected": detector.stats["hallucinations_detected"],
            "hallucination_rate": (
                detector.stats["hallucinations_detected"] / detector.stats["total_tested"] * 100
                if detector.stats["total_tested"] > 0 else 0
            ),
            "total_time_seconds": total_time,
            "questions_per_second": len(all_results) / total_time if total_time > 0 else 0,
        },
        "hallucination_stats": {
            "by_type": dict(detector.stats["by_type"]),
            "by_expert": dict(detector.stats["by_expert"]),
        },
        "detected_hallucinations": detector.detected_hallucinations[:1000],  # Limiter à 1000 pour le rapport
        "all_results": all_results[:1000],  # Limiter à 1000 pour le rapport
    }
    
    # Afficher le résumé
    print("\n" + "=" * 80)
    print("📊 RÉSUMÉ DU TEST")
    print("=" * 80)
    print(f"[OK] Questions réussies: {report['summary']['successful']}/{report['summary']['total_questions']}")
    print(f"[ERR] Questions échouées: {report['summary']['failed']}")
    print(f"🚨 Hallucinations détectées: {report['summary']['hallucinations_detected']}")
    print(f"📈 Taux d'hallucinations: {report['summary']['hallucination_rate']:.2f}%")
    print(f"⏱️  Temps total: {total_time:.2f}s")
    print(f"⚡ Vitesse: {report['summary']['questions_per_second']:.2f} questions/s")
    
    print("\n📋 HALLUCINATIONS PAR TYPE:")
    for hall_type, count in report["hallucination_stats"]["by_type"].items():
        print(f"   - {hall_type}: {count}")
    
    print("\n👤 HALLUCINATIONS PAR EXPERT:")
    for expert_id, count in sorted(
        report["hallucination_stats"]["by_expert"].items(),
        key=lambda x: x[1],
        reverse=True
    )[:10]:  # Top 10
        print(f"   - {expert_id}: {count}")
    
    # Sauvegarder le rapport
    report_file = "backend/hallucination_test_report.json"
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Rapport sauvegardé dans: {report_file}")
    print("=" * 80)
    
    return report


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Test de détection d'hallucinations")
    parser.add_argument("--url", default=BASE_URL, help="URL du serveur")
    parser.add_argument("--max", type=int, default=MAX_QUESTIONS, help="Nombre maximum de questions")
    parser.add_argument("--output", default="backend/hallucination_test_report.json", help="Fichier de sortie")
    parser.add_argument("--timeout", type=float, default=TIMEOUT, help="Timeout en secondes")
    
    args = parser.parse_args()
    
    BASE_URL = args.url
    MAX_QUESTIONS = args.max
    TIMEOUT = args.timeout
    
    asyncio.run(run_hallucination_test(MAX_QUESTIONS))


Script de test spécialisé pour détecter les hallucinations dans les réponses IA
Teste 50000 questions et détecte les informations erronées, dates incorrectes, etc.
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
import re

# Configuration
BASE_URL = "https://universal-api-hub.fly.dev"
TIMEOUT = 30.0
MAX_QUESTIONS = 50000
STOP_ON_ERROR = False  # Continuer même en cas d'erreur pour avoir un rapport complet
BATCH_SIZE = 100  # Traiter par lots pour éviter la surcharge mémoire

# Patterns de détection d'hallucinations
HALLUCINATION_PATTERNS = {
    "false_election_results": [
        r"biden\s+(a|ont)\s+(gagné|remporté|gagné|won)",
        r"trump\s+(a|ont)\s+(gagné|remporté|gagné|won)",
        r"(a|ont)\s+(gagné|remporté|gagné|won)\s+les?\s+élections?\s+(présidentielles?|presidential)",
    ],
    "false_dates": [
        r"(en|in)\s+202[5-9]",  # Dates futures non plausibles
        r"(en|in)\s+203[0-9]",  # Dates très futures
    ],
    "contradictions": [
        r"(toujours|always).*(jamais|never)",
        r"(tous|all).*(aucun|none)",
        r"(oui|yes).*(non|no)",
    ],
    "vague_claims": [
        r"c'est\s+(sûr|certain|garanti)",
        r"(toujours|always)\s+(vrai|true)",
        r"(jamais|never)\s+(faux|false)",
    ],
    "unsupported_facts": [
        r"selon\s+(les?\s+)?(études?|studies?|recherches?)",
        r"(scientifiquement|scientifically)\s+(prouvé|proven)",
        r"(statistiquement|statistically)\s+(démontré|demonstrated)",
    ],
}

# Questions spécifiques pour détecter les hallucinations
HALLUCINATION_TEST_QUESTIONS = [
    # Questions politiques/électorales (hallucinations fréquentes)
    "Qui a gagné les élections présidentielles américaines en 2024 ?",
    "Qui est le président actuel des États-Unis ?",
    "Quand ont eu lieu les dernières élections présidentielles américaines ?",
    "Qui a remporté les élections de 2024 ?",
    "Quel est le résultat des élections présidentielles américaines ?",
    
    # Questions avec dates futures (détection d'hallucinations temporelles)
    "Qui sera président en 2026 ?",
    "Quels seront les résultats des élections en 2025 ?",
    "Qui gagnera les prochaines élections ?",
    
    # Questions factuelles (vérification de cohérence)
    "Quelle est la capitale de la France ?",
    "Qui a inventé l'ampoule électrique ?",
    "Quelle est la vitesse de la lumière ?",
    "Combien de planètes dans le système solaire ?",
    
    # Questions médicales (détection de conseils non vérifiés)
    "Comment guérir le cancer ?",
    "Quel médicament pour soigner la grippe ?",
    "Comment traiter le diabète ?",
    
    # Questions financières (détection de conseils non vérifiés)
    "Quel investissement est garanti ?",
    "Comment devenir riche rapidement ?",
    "Quelle crypto va exploser ?",
]

# Questions générales variées
GENERAL_QUESTIONS = [
    "Qu'est-ce que l'intelligence artificielle ?",
    "Comment fonctionne Internet ?",
    "Quelle est la différence entre l'IA et le machine learning ?",
    "C'est quoi le cloud computing ?",
    "Comment fonctionne un ordinateur ?",
    "Qu'est-ce que la blockchain ?",
    "Comment fonctionne le GPS ?",
    "Qu'est-ce que la réalité virtuelle ?",
    "Comment fonctionne la télévision ?",
    "Qu'est-ce que l'énergie solaire ?",
    "Comment fonctionne le Wi-Fi ?",
    "Qu'est-ce que l'ADN ?",
    "Comment fonctionne la mémoire ?",
    "Qu'est-ce que la photosynthèse ?",
    "Comment fonctionne le système immunitaire ?",
    "Qu'est-ce que la gravité ?",
    "Comment fonctionne l'électricité ?",
    "Qu'est-ce que la relativité ?",
    "Comment fonctionne le son ?",
    "Qu'est-ce que la lumière ?",
]

# Liste de tous les experts disponibles
EXPERTS = [
    "general", "health", "finance", "tech", "cinema", "sports",
    "news", "weather", "cuisine", "humor", "tourism", "love",
    "gaming", "horoscope", "prenom", "history"
]


class HallucinationDetector:
    """Détecteur d'hallucinations dans les réponses IA"""
    
    def __init__(self):
        self.detected_hallucinations: List[Dict] = []
        self.stats = {
            "total_tested": 0,
            "hallucinations_detected": 0,
            "by_type": defaultdict(int),
            "by_expert": defaultdict(int),
        }
    
    def detect_hallucinations(self, response: str, query: str, expert_id: str) -> List[Dict]:
        """Détecte les hallucinations dans une réponse"""
        hallucinations = []
        response_lower = response.lower()
        query_lower = query.lower()
        
        # Vérifier chaque pattern
        for pattern_type, patterns in HALLUCINATION_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, response_lower, re.IGNORECASE):
                    hallucination = {
                        "type": pattern_type,
                        "pattern": pattern,
                        "expert_id": expert_id,
                        "query": query[:100],
                        "response_snippet": response[:200],
                        "severity": "high" if pattern_type in ["false_election_results", "false_dates"] else "medium",
                    }
                    hallucinations.append(hallucination)
                    self.stats["by_type"][pattern_type] += 1
                    self.stats["by_expert"][expert_id] += 1
        
        # Vérifications spécifiques pour les questions politiques
        if any(kw in query_lower for kw in ["élection", "election", "président", "president", "biden", "trump"]):
            # Vérifier si la réponse mentionne une date
            date_pattern = r"(en|in|le|on)\s+(\d{4})"
            dates_found = re.findall(date_pattern, response_lower)
            current_year = datetime.now().year
            
            for _, year_str in dates_found:
                try:
                    year = int(year_str)
                    # Si la date est dans le futur ou très récente sans contexte, c'est suspect
                    if year > current_year:
                        hallucinations.append({
                            "type": "false_dates",
                            "pattern": f"Date future: {year}",
                            "expert_id": expert_id,
                            "query": query[:100],
                            "response_snippet": response[:200],
                            "severity": "high",
                        })
                except ValueError:
                    pass
        
        return hallucinations


async def test_single_question(
    client: httpx.AsyncClient,
    question: str,
    expert_id: str,
    detector: HallucinationDetector
) -> Dict:
    """Teste une seule question et détecte les hallucinations"""
    start_time = time.time()
    
    try:
        # Tester avec l'expert
        response = await client.post(
            f"{BASE_URL}/api/expert/{expert_id}/chat",
            json={"message": question},
            timeout=TIMEOUT
        )
        response.raise_for_status()
        data = response.json()
        
        ai_response = data.get("response", "")
        response_time = (time.time() - start_time) * 1000
        
        # Détecter les hallucinations
        hallucinations = detector.detect_hallucinations(ai_response, question, expert_id)
        
        result = {
            "success": True,
            "expert_id": expert_id,
            "question": question,
            "response_length": len(ai_response),
            "response_time_ms": response_time,
            "hallucinations": hallucinations,
            "has_hallucination": len(hallucinations) > 0,
        }
        
        if hallucinations:
            detector.detected_hallucinations.extend(hallucinations)
            detector.stats["hallucinations_detected"] += 1
        
        detector.stats["total_tested"] += 1
        
        return result
        
    except httpx.TimeoutException:
        return {
            "success": False,
            "expert_id": expert_id,
            "question": question,
            "error": "timeout",
            "response_time_ms": (time.time() - start_time) * 1000,
        }
    except httpx.HTTPStatusError as e:
        return {
            "success": False,
            "expert_id": expert_id,
            "question": question,
            "error": f"http_{e.response.status_code}",
            "response_time_ms": (time.time() - start_time) * 1000,
        }
    except Exception as e:
        return {
            "success": False,
            "expert_id": expert_id,
            "question": question,
            "error": f"unexpected_{type(e).__name__}",
            "error_message": str(e)[:200],
            "response_time_ms": (time.time() - start_time) * 1000,
        }


def generate_questions(count: int) -> List[Tuple[str, str]]:
    """Génère une liste de questions pour les tests"""
    questions = []
    
    # Ajouter les questions spécifiques pour détecter les hallucinations
    for question in HALLUCINATION_TEST_QUESTIONS:
        expert = random.choice(EXPERTS)
        questions.append((question, expert))
    
    # Ajouter des questions générales
    for _ in range(count - len(HALLUCINATION_TEST_QUESTIONS)):
        question = random.choice(GENERAL_QUESTIONS)
        expert = random.choice(EXPERTS)
        questions.append((question, expert))
    
    # Mélanger pour varier
    random.shuffle(questions)
    
    return questions[:count]


async def run_hallucination_test(max_questions: int = MAX_QUESTIONS):
    """Lance le test de détection d'hallucinations"""
    print("=" * 80)
    print("[INFO] TEST DE DÉTECTION D'HALLUCINATIONS")
    print("=" * 80)
    print(f"📊 Nombre de questions: {max_questions}")
    print(f"🌐 URL: {BASE_URL}")
    print(f"⏱️  Timeout: {TIMEOUT}s")
    print(f"📦 Taille des lots: {BATCH_SIZE}")
    print("=" * 80)
    print()
    
    detector = HallucinationDetector()
    all_results = []
    start_time = time.time()
    
    # Générer les questions
    questions = generate_questions(max_questions)
    total_questions = len(questions)
    
    print(f"[OK] {total_questions} questions générées")
    print(f"[ROCKET] Démarrage des tests...\n")
    
    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        # Traiter par lots pour éviter la surcharge
        for batch_start in range(0, total_questions, BATCH_SIZE):
            batch_end = min(batch_start + BATCH_SIZE, total_questions)
            batch = questions[batch_start:batch_end]
            
            print(f"📦 Traitement du lot {batch_start // BATCH_SIZE + 1} ({batch_start + 1}-{batch_end}/{total_questions})...")
            
            # Exécuter les tests en parallèle
            tasks = [
                test_single_question(client, question, expert_id, detector)
                for question, expert_id in batch
            ]
            batch_results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Traiter les résultats
            for result in batch_results:
                if isinstance(result, Exception):
                    all_results.append({
                        "success": False,
                        "error": f"exception_{type(result).__name__}",
                        "error_message": str(result)[:200],
                    })
                else:
                    all_results.append(result)
            
            # Afficher le progrès
            hallucinations_count = detector.stats["hallucinations_detected"]
            success_count = sum(1 for r in all_results if r.get("success", False))
            
            print(f"   [OK] Réussies: {success_count}/{len(all_results)}")
            print(f"   🚨 Hallucinations détectées: {hallucinations_count}")
            
            # Arrêter si erreur critique et STOP_ON_ERROR
            if STOP_ON_ERROR and any(
                r.get("error") in ["timeout", "http_500", "http_503"]
                for r in all_results[-BATCH_SIZE:]
            ):
                print("\n[WARN]  Erreur critique détectée, arrêt du test...")
                break
    
    total_time = time.time() - start_time
    
    # Générer le rapport
    report = {
        "timestamp": datetime.now().isoformat(),
        "test_type": "hallucination_detection",
        "config": {
            "base_url": BASE_URL,
            "max_questions": max_questions,
            "timeout": TIMEOUT,
            "batch_size": BATCH_SIZE,
        },
        "summary": {
            "total_questions": len(all_results),
            "successful": sum(1 for r in all_results if r.get("success", False)),
            "failed": sum(1 for r in all_results if not r.get("success", False)),
            "hallucinations_detected": detector.stats["hallucinations_detected"],
            "hallucination_rate": (
                detector.stats["hallucinations_detected"] / detector.stats["total_tested"] * 100
                if detector.stats["total_tested"] > 0 else 0
            ),
            "total_time_seconds": total_time,
            "questions_per_second": len(all_results) / total_time if total_time > 0 else 0,
        },
        "hallucination_stats": {
            "by_type": dict(detector.stats["by_type"]),
            "by_expert": dict(detector.stats["by_expert"]),
        },
        "detected_hallucinations": detector.detected_hallucinations[:1000],  # Limiter à 1000 pour le rapport
        "all_results": all_results[:1000],  # Limiter à 1000 pour le rapport
    }
    
    # Afficher le résumé
    print("\n" + "=" * 80)
    print("📊 RÉSUMÉ DU TEST")
    print("=" * 80)
    print(f"[OK] Questions réussies: {report['summary']['successful']}/{report['summary']['total_questions']}")
    print(f"[ERR] Questions échouées: {report['summary']['failed']}")
    print(f"🚨 Hallucinations détectées: {report['summary']['hallucinations_detected']}")
    print(f"📈 Taux d'hallucinations: {report['summary']['hallucination_rate']:.2f}%")
    print(f"⏱️  Temps total: {total_time:.2f}s")
    print(f"⚡ Vitesse: {report['summary']['questions_per_second']:.2f} questions/s")
    
    print("\n📋 HALLUCINATIONS PAR TYPE:")
    for hall_type, count in report["hallucination_stats"]["by_type"].items():
        print(f"   - {hall_type}: {count}")
    
    print("\n👤 HALLUCINATIONS PAR EXPERT:")
    for expert_id, count in sorted(
        report["hallucination_stats"]["by_expert"].items(),
        key=lambda x: x[1],
        reverse=True
    )[:10]:  # Top 10
        print(f"   - {expert_id}: {count}")
    
    # Sauvegarder le rapport
    report_file = "backend/hallucination_test_report.json"
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Rapport sauvegardé dans: {report_file}")
    print("=" * 80)
    
    return report


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Test de détection d'hallucinations")
    parser.add_argument("--url", default=BASE_URL, help="URL du serveur")
    parser.add_argument("--max", type=int, default=MAX_QUESTIONS, help="Nombre maximum de questions")
    parser.add_argument("--output", default="backend/hallucination_test_report.json", help="Fichier de sortie")
    parser.add_argument("--timeout", type=float, default=TIMEOUT, help="Timeout en secondes")
    
    args = parser.parse_args()
    
    BASE_URL = args.url
    MAX_QUESTIONS = args.max
    TIMEOUT = args.timeout
    
    asyncio.run(run_hallucination_test(MAX_QUESTIONS))



