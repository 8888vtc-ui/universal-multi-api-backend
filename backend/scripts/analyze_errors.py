"""
Analyse des erreurs détectées et recommandations pour les corriger
"""
import json
import sys
from collections import defaultdict

sys.stdout.reconfigure(encoding='utf-8')

def analyze_report(report_file="backend/stress_test_report.json"):
    """Analyse le rapport et génère des recommandations"""
    
    try:
        with open(report_file, "r", encoding="utf-8") as f:
            report = json.load(f)
    except FileNotFoundError:
        print("[ERR] Rapport non trouvé. Lancez d'abord le test.")
        return
    except Exception as e:
        print(f"[ERR] Erreur: {e}")
        return
    
    print("\n" + "=" * 70)
    print("[INFO] ANALYSE DES ERREURS ET RECOMMANDATIONS")
    print("=" * 70)
    
    summary = report.get("summary", {})
    total = summary.get("total_questions", 0)
    successful = summary.get("successful", 0)
    failed = summary.get("failed", 0)
    
    print(f"\n📊 RÉSUMÉ")
    print(f"   Questions testées: {total}")
    print(f"   [OK] Réussies: {successful} ({successful/total*100:.2f}%)")
    print(f"   [ERR] Échouées: {failed} ({failed/total*100:.2f}%)")
    
    # Analyser les erreurs
    errors_by_type = report.get("errors_by_type", {})
    critical_errors = report.get("critical_errors", [])
    all_errors = report.get("all_errors", [])
    
    if not errors_by_type and not critical_errors:
        print("\n[OK] AUCUNE ERREUR DÉTECTÉE !")
        print("   Tous les experts fonctionnent correctement.")
        return
    
    print(f"\n🚨 ERREURS DÉTECTÉES")
    print(f"   Erreurs critiques: {len(critical_errors)}")
    print(f"   Total d'erreurs: {len(all_errors)}")
    
    # Analyser chaque type d'erreur
    print(f"\n📋 ANALYSE PAR TYPE D'ERREUR")
    print("-" * 70)
    
    recommendations = []
    
    for error_type, count in sorted(errors_by_type.items(), key=lambda x: x[1], reverse=True):
        print(f"\n🔴 {error_type.upper()} ({count} occurrence(s))")
        
        # Trouver les exemples
        examples = [e for e in all_errors if e.get("error_type") == error_type][:3]
        
        for example in examples:
            print(f"   - Question {example.get('question_num')}: {example.get('expert_id')}")
            print(f"     Question: {example.get('question', '')[:60]}...")
            if example.get('error_message'):
                print(f"     Message: {example.get('error_message')[:80]}")
        
        # Recommandations par type
        if error_type == "server_unavailable":
            print(f"\n   💡 RECOMMANDATIONS:")
            print(f"      1. Vérifier que le serveur backend est lancé")
            print(f"      2. Vérifier la connectivité réseau")
            print(f"      3. Vérifier les logs du serveur pour des erreurs")
            print(f"      4. Implémenter un système de retry avec backoff")
            recommendations.append({
                "type": error_type,
                "priority": "HIGH",
                "action": "Vérifier la disponibilité du serveur et implémenter retry"
            })
        
        elif error_type == "timeout":
            print(f"\n   💡 RECOMMANDATIONS:")
            print(f"      1. Augmenter le timeout (actuellement 30s)")
            print(f"      2. Optimiser les requêtes API lentes")
            print(f"      3. Implémenter un cache pour les réponses fréquentes")
            print(f"      4. Paralléliser les appels API quand possible")
            recommendations.append({
                "type": error_type,
                "priority": "MEDIUM",
                "action": "Optimiser les temps de réponse et augmenter timeout si nécessaire"
            })
        
        elif error_type == "empty_response":
            print(f"\n   💡 RECOMMANDATIONS:")
            print(f"      1. Vérifier que les providers IA sont configurés")
            print(f"      2. Ajouter des logs pour comprendre pourquoi la réponse est vide")
            print(f"      3. Implémenter un fallback si l'IA ne répond pas")
            recommendations.append({
                "type": error_type,
                "priority": "HIGH",
                "action": "Vérifier la configuration des providers IA et ajouter fallback"
            })
        
        elif error_type == "invalid_response_format":
            print(f"\n   💡 RECOMMANDATIONS:")
            print(f"      1. Vérifier le format de réponse des providers IA")
            print(f"      2. Ajouter une validation JSON stricte")
            print(f"      3. Logger les réponses invalides pour debug")
            recommendations.append({
                "type": error_type,
                "priority": "MEDIUM",
                "action": "Valider le format JSON et logger les erreurs"
            })
        
        elif error_type == "unexpected_error":
            print(f"\n   💡 RECOMMANDATIONS:")
            print(f"      1. Examiner les logs détaillés")
            print(f"      2. Ajouter plus de gestion d'erreurs")
            print(f"      3. Implémenter un système de monitoring")
            recommendations.append({
                "type": error_type,
                "priority": "MEDIUM",
                "action": "Améliorer la gestion d'erreurs et le logging"
            })
        
        elif error_type == "response_too_short":
            print(f"\n   💡 RECOMMANDATIONS:")
            print(f"      1. Vérifier les prompts système")
            print(f"      2. S'assurer que l'IA génère des réponses complètes")
            print(f"      3. Ajouter une validation de longueur minimale")
            recommendations.append({
                "type": error_type,
                "priority": "LOW",
                "action": "Améliorer les prompts pour obtenir des réponses plus longues"
            })
    
    # Recommandations globales
    print(f"\n" + "=" * 70)
    print("[NOTE] PLAN D'ACTION RECOMMANDÉ")
    print("=" * 70)
    
    # Trier par priorité
    high_priority = [r for r in recommendations if r["priority"] == "HIGH"]
    medium_priority = [r for r in recommendations if r["priority"] == "MEDIUM"]
    low_priority = [r for r in recommendations if r["priority"] == "LOW"]
    
    if high_priority:
        print(f"\n🔴 PRIORITÉ HAUTE:")
        for i, rec in enumerate(high_priority, 1):
            print(f"   {i}. {rec['type']}: {rec['action']}")
    
    if medium_priority:
        print(f"\n🟡 PRIORITÉ MOYENNE:")
        for i, rec in enumerate(medium_priority, 1):
            print(f"   {i}. {rec['type']}: {rec['action']}")
    
    if low_priority:
        print(f"\n🟢 PRIORITÉ BASSE:")
        for i, rec in enumerate(low_priority, 1):
            print(f"   {i}. {rec['type']}: {rec['action']}")
    
    # Statistiques de performance
    if summary.get('slow_responses', 0) > 0:
        print(f"\n[WARN]  PERFORMANCE:")
        print(f"   Réponses lentes (>15s): {summary.get('slow_responses', 0)}")
        print(f"   Temps moyen: {summary.get('average_response_time_ms', 0):.0f}ms")
        print(f"   💡 Recommandation: Optimiser les appels API et implémenter un cache")
    
    print(f"\n" + "=" * 70)
    
    # Sauvegarder les recommandations
    recommendations_file = "backend/error_recommendations.json"
    with open(recommendations_file, "w", encoding="utf-8") as f:
        json.dump({
            "timestamp": report.get("timestamp"),
            "total_errors": len(all_errors),
            "critical_errors": len(critical_errors),
            "recommendations": recommendations,
            "summary": summary
        }, f, ensure_ascii=False, indent=2)
    
    print(f"💾 Recommandations sauvegardées dans: {recommendations_file}")
    print("")


if __name__ == "__main__":
    analyze_report()


Analyse des erreurs détectées et recommandations pour les corriger
"""
import json
import sys
from collections import defaultdict

sys.stdout.reconfigure(encoding='utf-8')

def analyze_report(report_file="backend/stress_test_report.json"):
    """Analyse le rapport et génère des recommandations"""
    
    try:
        with open(report_file, "r", encoding="utf-8") as f:
            report = json.load(f)
    except FileNotFoundError:
        print("[ERR] Rapport non trouvé. Lancez d'abord le test.")
        return
    except Exception as e:
        print(f"[ERR] Erreur: {e}")
        return
    
    print("\n" + "=" * 70)
    print("[INFO] ANALYSE DES ERREURS ET RECOMMANDATIONS")
    print("=" * 70)
    
    summary = report.get("summary", {})
    total = summary.get("total_questions", 0)
    successful = summary.get("successful", 0)
    failed = summary.get("failed", 0)
    
    print(f"\n📊 RÉSUMÉ")
    print(f"   Questions testées: {total}")
    print(f"   [OK] Réussies: {successful} ({successful/total*100:.2f}%)")
    print(f"   [ERR] Échouées: {failed} ({failed/total*100:.2f}%)")
    
    # Analyser les erreurs
    errors_by_type = report.get("errors_by_type", {})
    critical_errors = report.get("critical_errors", [])
    all_errors = report.get("all_errors", [])
    
    if not errors_by_type and not critical_errors:
        print("\n[OK] AUCUNE ERREUR DÉTECTÉE !")
        print("   Tous les experts fonctionnent correctement.")
        return
    
    print(f"\n🚨 ERREURS DÉTECTÉES")
    print(f"   Erreurs critiques: {len(critical_errors)}")
    print(f"   Total d'erreurs: {len(all_errors)}")
    
    # Analyser chaque type d'erreur
    print(f"\n📋 ANALYSE PAR TYPE D'ERREUR")
    print("-" * 70)
    
    recommendations = []
    
    for error_type, count in sorted(errors_by_type.items(), key=lambda x: x[1], reverse=True):
        print(f"\n🔴 {error_type.upper()} ({count} occurrence(s))")
        
        # Trouver les exemples
        examples = [e for e in all_errors if e.get("error_type") == error_type][:3]
        
        for example in examples:
            print(f"   - Question {example.get('question_num')}: {example.get('expert_id')}")
            print(f"     Question: {example.get('question', '')[:60]}...")
            if example.get('error_message'):
                print(f"     Message: {example.get('error_message')[:80]}")
        
        # Recommandations par type
        if error_type == "server_unavailable":
            print(f"\n   💡 RECOMMANDATIONS:")
            print(f"      1. Vérifier que le serveur backend est lancé")
            print(f"      2. Vérifier la connectivité réseau")
            print(f"      3. Vérifier les logs du serveur pour des erreurs")
            print(f"      4. Implémenter un système de retry avec backoff")
            recommendations.append({
                "type": error_type,
                "priority": "HIGH",
                "action": "Vérifier la disponibilité du serveur et implémenter retry"
            })
        
        elif error_type == "timeout":
            print(f"\n   💡 RECOMMANDATIONS:")
            print(f"      1. Augmenter le timeout (actuellement 30s)")
            print(f"      2. Optimiser les requêtes API lentes")
            print(f"      3. Implémenter un cache pour les réponses fréquentes")
            print(f"      4. Paralléliser les appels API quand possible")
            recommendations.append({
                "type": error_type,
                "priority": "MEDIUM",
                "action": "Optimiser les temps de réponse et augmenter timeout si nécessaire"
            })
        
        elif error_type == "empty_response":
            print(f"\n   💡 RECOMMANDATIONS:")
            print(f"      1. Vérifier que les providers IA sont configurés")
            print(f"      2. Ajouter des logs pour comprendre pourquoi la réponse est vide")
            print(f"      3. Implémenter un fallback si l'IA ne répond pas")
            recommendations.append({
                "type": error_type,
                "priority": "HIGH",
                "action": "Vérifier la configuration des providers IA et ajouter fallback"
            })
        
        elif error_type == "invalid_response_format":
            print(f"\n   💡 RECOMMANDATIONS:")
            print(f"      1. Vérifier le format de réponse des providers IA")
            print(f"      2. Ajouter une validation JSON stricte")
            print(f"      3. Logger les réponses invalides pour debug")
            recommendations.append({
                "type": error_type,
                "priority": "MEDIUM",
                "action": "Valider le format JSON et logger les erreurs"
            })
        
        elif error_type == "unexpected_error":
            print(f"\n   💡 RECOMMANDATIONS:")
            print(f"      1. Examiner les logs détaillés")
            print(f"      2. Ajouter plus de gestion d'erreurs")
            print(f"      3. Implémenter un système de monitoring")
            recommendations.append({
                "type": error_type,
                "priority": "MEDIUM",
                "action": "Améliorer la gestion d'erreurs et le logging"
            })
        
        elif error_type == "response_too_short":
            print(f"\n   💡 RECOMMANDATIONS:")
            print(f"      1. Vérifier les prompts système")
            print(f"      2. S'assurer que l'IA génère des réponses complètes")
            print(f"      3. Ajouter une validation de longueur minimale")
            recommendations.append({
                "type": error_type,
                "priority": "LOW",
                "action": "Améliorer les prompts pour obtenir des réponses plus longues"
            })
    
    # Recommandations globales
    print(f"\n" + "=" * 70)
    print("[NOTE] PLAN D'ACTION RECOMMANDÉ")
    print("=" * 70)
    
    # Trier par priorité
    high_priority = [r for r in recommendations if r["priority"] == "HIGH"]
    medium_priority = [r for r in recommendations if r["priority"] == "MEDIUM"]
    low_priority = [r for r in recommendations if r["priority"] == "LOW"]
    
    if high_priority:
        print(f"\n🔴 PRIORITÉ HAUTE:")
        for i, rec in enumerate(high_priority, 1):
            print(f"   {i}. {rec['type']}: {rec['action']}")
    
    if medium_priority:
        print(f"\n🟡 PRIORITÉ MOYENNE:")
        for i, rec in enumerate(medium_priority, 1):
            print(f"   {i}. {rec['type']}: {rec['action']}")
    
    if low_priority:
        print(f"\n🟢 PRIORITÉ BASSE:")
        for i, rec in enumerate(low_priority, 1):
            print(f"   {i}. {rec['type']}: {rec['action']}")
    
    # Statistiques de performance
    if summary.get('slow_responses', 0) > 0:
        print(f"\n[WARN]  PERFORMANCE:")
        print(f"   Réponses lentes (>15s): {summary.get('slow_responses', 0)}")
        print(f"   Temps moyen: {summary.get('average_response_time_ms', 0):.0f}ms")
        print(f"   💡 Recommandation: Optimiser les appels API et implémenter un cache")
    
    print(f"\n" + "=" * 70)
    
    # Sauvegarder les recommandations
    recommendations_file = "backend/error_recommendations.json"
    with open(recommendations_file, "w", encoding="utf-8") as f:
        json.dump({
            "timestamp": report.get("timestamp"),
            "total_errors": len(all_errors),
            "critical_errors": len(critical_errors),
            "recommendations": recommendations,
            "summary": summary
        }, f, ensure_ascii=False, indent=2)
    
    print(f"💾 Recommandations sauvegardées dans: {recommendations_file}")
    print("")


if __name__ == "__main__":
    analyze_report()



