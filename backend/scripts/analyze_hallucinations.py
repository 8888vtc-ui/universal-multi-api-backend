"""
Script d'analyse des hallucinations détectées
Génère des recommandations pour corriger les problèmes
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

import json
from typing import Dict, Any, List
from datetime import datetime
from collections import defaultdict

REPORT_FILE = "backend/hallucination_test_report.json"
RECOMMENDATIONS_FILE = "backend/hallucination_recommendations.json"

def analyze_hallucinations(report: Dict[str, Any]) -> Dict[str, Any]:
    """Analyse les hallucinations et génère des recommandations"""
    
    print("\n" + "=" * 80)
    print("[INFO] ANALYSE DES HALLUCINATIONS DÉTECTÉES")
    print("=" * 80)
    
    summary = report.get("summary", {})
    hallucinations = report.get("detected_hallucinations", [])
    hall_stats = report.get("hallucination_stats", {})
    
    print(f"\n📊 STATISTIQUES GLOBALES")
    print(f"   Total de questions testées: {summary.get('total_questions', 0)}")
    print(f"   [OK] Réussies: {summary.get('successful', 0)}")
    print(f"   🚨 Hallucinations détectées: {summary.get('hallucinations_detected', 0)}")
    print(f"   📈 Taux d'hallucinations: {summary.get('hallucination_rate', 0):.2f}%")
    
    if summary.get('hallucinations_detected', 0) == 0:
        print("\n[OK] EXCELLENT! Aucune hallucination détectée!")
        return {
            "status": "success",
            "recommendations": []
        }
    
    # Analyser par type
    print("\n📋 ANALYSE PAR TYPE D'HALLUCINATION")
    print("-" * 80)
    
    recommendations = []
    
    by_type = hall_stats.get("by_type", {})
    for hall_type, count in sorted(by_type.items(), key=lambda x: x[1], reverse=True):
        print(f"\n🔴 {hall_type.upper()} ({count} occurrence(s))")
        
        # Exemples
        examples = [h for h in hallucinations if h.get("type") == hall_type][:3]
        for i, ex in enumerate(examples, 1):
            print(f"   Exemple {i}:")
            print(f"      Question: {ex.get('query', 'N/A')}")
            print(f"      Expert: {ex.get('expert_id', 'N/A')}")
            print(f"      Snippet: {ex.get('response_snippet', 'N/A')[:150]}...")
        
        # Recommandations spécifiques
        if hall_type == "false_election_results":
            print("\n   💡 RECOMMANDATIONS:")
            print("      1. Renforcer les prompts système pour les informations politiques/électorales")
            print("      2. Ajouter une vérification de date obligatoire avant de mentionner des résultats")
            print("      3. Implémenter un système de vérification de date dans ai_response_validator")
            print("      4. Ajouter un disclaimer automatique pour les informations électorales")
            recommendations.append({
                "type": hall_type,
                "priority": "CRITICAL",
                "action": "Renforcer la validation des informations politiques/électorales",
                "details": [
                    "Améliorer les prompts système pour inclure la date actuelle",
                    "Ajouter une vérification de date avant de mentionner des résultats",
                    "Implémenter un système de vérification dans ai_response_validator",
                ]
            })
        
        elif hall_type == "false_dates":
            print("\n   💡 RECOMMANDATIONS:")
            print("      1. Ajouter une vérification de date dans les réponses")
            print("      2. Rejeter les réponses contenant des dates futures non plausibles")
            print("      3. Améliorer les prompts pour demander à l'IA de vérifier les dates")
            recommendations.append({
                "type": hall_type,
                "priority": "HIGH",
                "action": "Vérifier les dates dans les réponses",
                "details": [
                    "Ajouter une vérification de date dans ai_response_validator",
                    "Rejeter les réponses avec dates futures non plausibles",
                    "Améliorer les prompts pour vérifier les dates",
                ]
            })
        
        elif hall_type == "contradictions":
            print("\n   💡 RECOMMANDATIONS:")
            print("      1. Améliorer la détection de contradictions dans ai_response_validator")
            print("      2. Rejeter les réponses avec contradictions internes")
            print("      3. Ajouter une vérification de cohérence logique")
            recommendations.append({
                "type": hall_type,
                "priority": "MEDIUM",
                "action": "Améliorer la détection de contradictions",
                "details": [
                    "Renforcer la détection de contradictions dans ai_response_validator",
                    "Rejeter les réponses avec contradictions internes",
                    "Ajouter une vérification de cohérence logique",
                ]
            })
        
        elif hall_type == "vague_claims":
            print("\n   💡 RECOMMANDATIONS:")
            print("      1. Améliorer les prompts pour éviter les affirmations trop catégoriques")
            print("      2. Ajouter des nuances dans les réponses")
            print("      3. Vérifier que les affirmations sont justifiées")
            recommendations.append({
                "type": hall_type,
                "priority": "MEDIUM",
                "action": "Réduire les affirmations trop catégoriques",
                "details": [
                    "Améliorer les prompts pour éviter les affirmations trop catégoriques",
                    "Ajouter des nuances dans les réponses",
                    "Vérifier que les affirmations sont justifiées",
                ]
            })
        
        elif hall_type == "unsupported_facts":
            print("\n   💡 RECOMMANDATIONS:")
            print("      1. Vérifier que les sources sont mentionnées")
            print("      2. Rejeter les réponses avec affirmations non sourcées")
            print("      3. Améliorer les prompts pour demander des sources")
            recommendations.append({
                "type": hall_type,
                "priority": "MEDIUM",
                "action": "Vérifier les sources dans les réponses",
                "details": [
                    "Vérifier que les sources sont mentionnées",
                    "Rejeter les réponses avec affirmations non sourcées",
                    "Améliorer les prompts pour demander des sources",
                ]
            })
    
    # Analyser par expert
    print("\n👤 ANALYSE PAR EXPERT")
    print("-" * 80)
    
    by_expert = hall_stats.get("by_expert", {})
    if by_expert:
        print("\n🔴 TOP 10 EXPERTS AVEC LE PLUS D'HALLUCINATIONS:")
        for expert_id, count in sorted(by_expert.items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f"   - {expert_id}: {count} hallucination(s)")
        
        # Recommandation pour les experts problématiques
        top_problematic = sorted(by_expert.items(), key=lambda x: x[1], reverse=True)[:5]
        if top_problematic:
            recommendations.append({
                "type": "expert_specific",
                "priority": "HIGH",
                "action": "Réviser les prompts des experts problématiques",
                "details": [
                    f"Experts les plus problématiques: {', '.join([e[0] for e in top_problematic])}",
                    "Réviser les prompts système de ces experts",
                    "Ajouter des validations spécifiques pour ces experts",
                ]
            })
    
    # Générer le rapport de recommandations
    analysis = {
        "timestamp": datetime.now().isoformat(),
        "total_hallucinations": summary.get("hallucinations_detected", 0),
        "hallucination_rate": summary.get("hallucination_rate", 0),
        "recommendations": recommendations,
        "summary": summary,
        "hallucination_stats": hall_stats,
    }
    
    print("\n" + "=" * 80)
    print("[NOTE] PLAN D'ACTION RECOMMANDÉ")
    print("=" * 80)
    
    critical_recs = [r for r in recommendations if r.get("priority") == "CRITICAL"]
    high_recs = [r for r in recommendations if r.get("priority") == "HIGH"]
    medium_recs = [r for r in recommendations if r.get("priority") == "MEDIUM"]
    
    if critical_recs:
        print("\n🔴 PRIORITÉ CRITIQUE:")
        for i, rec in enumerate(critical_recs, 1):
            print(f"   {i}. {rec['action']}")
            for detail in rec.get("details", []):
                print(f"      - {detail}")
    
    if high_recs:
        print("\n🟠 PRIORITÉ HAUTE:")
        for i, rec in enumerate(high_recs, 1):
            print(f"   {i}. {rec['action']}")
            for detail in rec.get("details", []):
                print(f"      - {detail}")
    
    if medium_recs:
        print("\n🟡 PRIORITÉ MOYENNE:")
        for i, rec in enumerate(medium_recs, 1):
            print(f"   {i}. {rec['action']}")
            for detail in rec.get("details", []):
                print(f"      - {detail}")
    
    print("\n" + "=" * 80)
    
    return analysis


if __name__ == "__main__":
    try:
        with open(REPORT_FILE, "r", encoding="utf-8") as f:
            report_data = json.load(f)
        
        analysis_result = analyze_hallucinations(report_data)
        
        with open(RECOMMENDATIONS_FILE, "w", encoding="utf-8") as f:
            json.dump(analysis_result, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 Recommandations sauvegardées dans: {RECOMMENDATIONS_FILE}")
        
    except FileNotFoundError:
        print(f"[ERR] Erreur: Le fichier de rapport '{REPORT_FILE}' est introuvable.")
        print("   Lancez d'abord le test de détection d'hallucinations.")
    except json.JSONDecodeError:
        print(f"[ERR] Erreur: Le fichier de rapport '{REPORT_FILE}' est invalide.")
        print("   Vérifiez son contenu.")
    except Exception as e:
        print(f"[ERR] Une erreur inattendue est survenue: {e}")


Script d'analyse des hallucinations détectées
Génère des recommandations pour corriger les problèmes
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

import json
from typing import Dict, Any, List
from datetime import datetime
from collections import defaultdict

REPORT_FILE = "backend/hallucination_test_report.json"
RECOMMENDATIONS_FILE = "backend/hallucination_recommendations.json"

def analyze_hallucinations(report: Dict[str, Any]) -> Dict[str, Any]:
    """Analyse les hallucinations et génère des recommandations"""
    
    print("\n" + "=" * 80)
    print("[INFO] ANALYSE DES HALLUCINATIONS DÉTECTÉES")
    print("=" * 80)
    
    summary = report.get("summary", {})
    hallucinations = report.get("detected_hallucinations", [])
    hall_stats = report.get("hallucination_stats", {})
    
    print(f"\n📊 STATISTIQUES GLOBALES")
    print(f"   Total de questions testées: {summary.get('total_questions', 0)}")
    print(f"   [OK] Réussies: {summary.get('successful', 0)}")
    print(f"   🚨 Hallucinations détectées: {summary.get('hallucinations_detected', 0)}")
    print(f"   📈 Taux d'hallucinations: {summary.get('hallucination_rate', 0):.2f}%")
    
    if summary.get('hallucinations_detected', 0) == 0:
        print("\n[OK] EXCELLENT! Aucune hallucination détectée!")
        return {
            "status": "success",
            "recommendations": []
        }
    
    # Analyser par type
    print("\n📋 ANALYSE PAR TYPE D'HALLUCINATION")
    print("-" * 80)
    
    recommendations = []
    
    by_type = hall_stats.get("by_type", {})
    for hall_type, count in sorted(by_type.items(), key=lambda x: x[1], reverse=True):
        print(f"\n🔴 {hall_type.upper()} ({count} occurrence(s))")
        
        # Exemples
        examples = [h for h in hallucinations if h.get("type") == hall_type][:3]
        for i, ex in enumerate(examples, 1):
            print(f"   Exemple {i}:")
            print(f"      Question: {ex.get('query', 'N/A')}")
            print(f"      Expert: {ex.get('expert_id', 'N/A')}")
            print(f"      Snippet: {ex.get('response_snippet', 'N/A')[:150]}...")
        
        # Recommandations spécifiques
        if hall_type == "false_election_results":
            print("\n   💡 RECOMMANDATIONS:")
            print("      1. Renforcer les prompts système pour les informations politiques/électorales")
            print("      2. Ajouter une vérification de date obligatoire avant de mentionner des résultats")
            print("      3. Implémenter un système de vérification de date dans ai_response_validator")
            print("      4. Ajouter un disclaimer automatique pour les informations électorales")
            recommendations.append({
                "type": hall_type,
                "priority": "CRITICAL",
                "action": "Renforcer la validation des informations politiques/électorales",
                "details": [
                    "Améliorer les prompts système pour inclure la date actuelle",
                    "Ajouter une vérification de date avant de mentionner des résultats",
                    "Implémenter un système de vérification dans ai_response_validator",
                ]
            })
        
        elif hall_type == "false_dates":
            print("\n   💡 RECOMMANDATIONS:")
            print("      1. Ajouter une vérification de date dans les réponses")
            print("      2. Rejeter les réponses contenant des dates futures non plausibles")
            print("      3. Améliorer les prompts pour demander à l'IA de vérifier les dates")
            recommendations.append({
                "type": hall_type,
                "priority": "HIGH",
                "action": "Vérifier les dates dans les réponses",
                "details": [
                    "Ajouter une vérification de date dans ai_response_validator",
                    "Rejeter les réponses avec dates futures non plausibles",
                    "Améliorer les prompts pour vérifier les dates",
                ]
            })
        
        elif hall_type == "contradictions":
            print("\n   💡 RECOMMANDATIONS:")
            print("      1. Améliorer la détection de contradictions dans ai_response_validator")
            print("      2. Rejeter les réponses avec contradictions internes")
            print("      3. Ajouter une vérification de cohérence logique")
            recommendations.append({
                "type": hall_type,
                "priority": "MEDIUM",
                "action": "Améliorer la détection de contradictions",
                "details": [
                    "Renforcer la détection de contradictions dans ai_response_validator",
                    "Rejeter les réponses avec contradictions internes",
                    "Ajouter une vérification de cohérence logique",
                ]
            })
        
        elif hall_type == "vague_claims":
            print("\n   💡 RECOMMANDATIONS:")
            print("      1. Améliorer les prompts pour éviter les affirmations trop catégoriques")
            print("      2. Ajouter des nuances dans les réponses")
            print("      3. Vérifier que les affirmations sont justifiées")
            recommendations.append({
                "type": hall_type,
                "priority": "MEDIUM",
                "action": "Réduire les affirmations trop catégoriques",
                "details": [
                    "Améliorer les prompts pour éviter les affirmations trop catégoriques",
                    "Ajouter des nuances dans les réponses",
                    "Vérifier que les affirmations sont justifiées",
                ]
            })
        
        elif hall_type == "unsupported_facts":
            print("\n   💡 RECOMMANDATIONS:")
            print("      1. Vérifier que les sources sont mentionnées")
            print("      2. Rejeter les réponses avec affirmations non sourcées")
            print("      3. Améliorer les prompts pour demander des sources")
            recommendations.append({
                "type": hall_type,
                "priority": "MEDIUM",
                "action": "Vérifier les sources dans les réponses",
                "details": [
                    "Vérifier que les sources sont mentionnées",
                    "Rejeter les réponses avec affirmations non sourcées",
                    "Améliorer les prompts pour demander des sources",
                ]
            })
    
    # Analyser par expert
    print("\n👤 ANALYSE PAR EXPERT")
    print("-" * 80)
    
    by_expert = hall_stats.get("by_expert", {})
    if by_expert:
        print("\n🔴 TOP 10 EXPERTS AVEC LE PLUS D'HALLUCINATIONS:")
        for expert_id, count in sorted(by_expert.items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f"   - {expert_id}: {count} hallucination(s)")
        
        # Recommandation pour les experts problématiques
        top_problematic = sorted(by_expert.items(), key=lambda x: x[1], reverse=True)[:5]
        if top_problematic:
            recommendations.append({
                "type": "expert_specific",
                "priority": "HIGH",
                "action": "Réviser les prompts des experts problématiques",
                "details": [
                    f"Experts les plus problématiques: {', '.join([e[0] for e in top_problematic])}",
                    "Réviser les prompts système de ces experts",
                    "Ajouter des validations spécifiques pour ces experts",
                ]
            })
    
    # Générer le rapport de recommandations
    analysis = {
        "timestamp": datetime.now().isoformat(),
        "total_hallucinations": summary.get("hallucinations_detected", 0),
        "hallucination_rate": summary.get("hallucination_rate", 0),
        "recommendations": recommendations,
        "summary": summary,
        "hallucination_stats": hall_stats,
    }
    
    print("\n" + "=" * 80)
    print("[NOTE] PLAN D'ACTION RECOMMANDÉ")
    print("=" * 80)
    
    critical_recs = [r for r in recommendations if r.get("priority") == "CRITICAL"]
    high_recs = [r for r in recommendations if r.get("priority") == "HIGH"]
    medium_recs = [r for r in recommendations if r.get("priority") == "MEDIUM"]
    
    if critical_recs:
        print("\n🔴 PRIORITÉ CRITIQUE:")
        for i, rec in enumerate(critical_recs, 1):
            print(f"   {i}. {rec['action']}")
            for detail in rec.get("details", []):
                print(f"      - {detail}")
    
    if high_recs:
        print("\n🟠 PRIORITÉ HAUTE:")
        for i, rec in enumerate(high_recs, 1):
            print(f"   {i}. {rec['action']}")
            for detail in rec.get("details", []):
                print(f"      - {detail}")
    
    if medium_recs:
        print("\n🟡 PRIORITÉ MOYENNE:")
        for i, rec in enumerate(medium_recs, 1):
            print(f"   {i}. {rec['action']}")
            for detail in rec.get("details", []):
                print(f"      - {detail}")
    
    print("\n" + "=" * 80)
    
    return analysis


if __name__ == "__main__":
    try:
        with open(REPORT_FILE, "r", encoding="utf-8") as f:
            report_data = json.load(f)
        
        analysis_result = analyze_hallucinations(report_data)
        
        with open(RECOMMENDATIONS_FILE, "w", encoding="utf-8") as f:
            json.dump(analysis_result, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 Recommandations sauvegardées dans: {RECOMMENDATIONS_FILE}")
        
    except FileNotFoundError:
        print(f"[ERR] Erreur: Le fichier de rapport '{REPORT_FILE}' est introuvable.")
        print("   Lancez d'abord le test de détection d'hallucinations.")
    except json.JSONDecodeError:
        print(f"[ERR] Erreur: Le fichier de rapport '{REPORT_FILE}' est invalide.")
        print("   Vérifiez son contenu.")
    except Exception as e:
        print(f"[ERR] Une erreur inattendue est survenue: {e}")



