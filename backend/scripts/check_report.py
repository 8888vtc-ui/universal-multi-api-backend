"""Script simple pour vérifier le rapport de test"""
import json
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

report_file = "backend/stress_test_report.json"

if not os.path.exists(report_file):
    print("\n⏳ Test en cours... Le rapport n'est pas encore disponible.")
    print("💡 Le test peut prendre 30-60 minutes pour 5000 questions.")
    print("   Vérifiez à nouveau dans quelques instants.\n")
    sys.exit(0)

try:
    with open(report_file, "r", encoding="utf-8") as f:
        report = json.load(f)
    
    summary = report.get("summary", {})
    
    print("\n📊 RAPPORT DE TEST")
    print("=" * 60)
    print(f"Questions testées: {summary.get('total_questions', 0)}/5000")
    print(f"[OK] Réussies: {summary.get('successful', 0)}")
    print(f"[ERR] Échouées: {summary.get('failed', 0)}")
    print(f"📈 Taux de succès: {summary.get('success_rate', '0%')}")
    
    if summary.get('average_response_time_ms'):
        print(f"⏱️  Temps moyen: {summary.get('average_response_time_ms', 0):.0f}ms")
    
    if summary.get('questions_per_second'):
        print(f"[ROCKET] Vitesse: {summary.get('questions_per_second', 0):.2f} questions/s")
    
    # Erreurs critiques
    critical_errors = report.get("critical_errors", [])
    if critical_errors:
        print(f"\n🚨 ERREURS CRITIQUES DÉTECTÉES: {len(critical_errors)}")
        for error in critical_errors[:5]:
            print(f"   - Question {error.get('question_num')}: {error.get('error_type')}")
            print(f"     Expert: {error.get('expert_id')}")
            print(f"     Message: {error.get('error_message', '')[:80]}")
    
    # Erreurs par type
    errors_by_type = report.get("errors_by_type", {})
    if errors_by_type:
        print(f"\n[WARN]  ERREURS PAR TYPE:")
        for error_type, count in sorted(errors_by_type.items(), key=lambda x: x[1], reverse=True):
            print(f"   - {error_type}: {count}")
    
    # Statut
    if report.get("stop_requested"):
        print("\n[STOP] TEST ARRÊTÉ - Erreur critique détectée")
    elif summary.get('total_questions', 0) >= 5000:
        print("\n[OK] TEST TERMINÉ - 5000 questions complétées")
    else:
        remaining = 5000 - summary.get('total_questions', 0)
        print(f"\n⏳ TEST EN COURS - {remaining} questions restantes")
    
    print("\n" + "=" * 60)
    
except json.JSONDecodeError:
    print("\n[WARN]  Le rapport est en cours d'écriture...")
except Exception as e:
    print(f"\n[ERR] Erreur lors de la lecture du rapport: {e}")


import json
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

report_file = "backend/stress_test_report.json"

if not os.path.exists(report_file):
    print("\n⏳ Test en cours... Le rapport n'est pas encore disponible.")
    print("💡 Le test peut prendre 30-60 minutes pour 5000 questions.")
    print("   Vérifiez à nouveau dans quelques instants.\n")
    sys.exit(0)

try:
    with open(report_file, "r", encoding="utf-8") as f:
        report = json.load(f)
    
    summary = report.get("summary", {})
    
    print("\n📊 RAPPORT DE TEST")
    print("=" * 60)
    print(f"Questions testées: {summary.get('total_questions', 0)}/5000")
    print(f"[OK] Réussies: {summary.get('successful', 0)}")
    print(f"[ERR] Échouées: {summary.get('failed', 0)}")
    print(f"📈 Taux de succès: {summary.get('success_rate', '0%')}")
    
    if summary.get('average_response_time_ms'):
        print(f"⏱️  Temps moyen: {summary.get('average_response_time_ms', 0):.0f}ms")
    
    if summary.get('questions_per_second'):
        print(f"[ROCKET] Vitesse: {summary.get('questions_per_second', 0):.2f} questions/s")
    
    # Erreurs critiques
    critical_errors = report.get("critical_errors", [])
    if critical_errors:
        print(f"\n🚨 ERREURS CRITIQUES DÉTECTÉES: {len(critical_errors)}")
        for error in critical_errors[:5]:
            print(f"   - Question {error.get('question_num')}: {error.get('error_type')}")
            print(f"     Expert: {error.get('expert_id')}")
            print(f"     Message: {error.get('error_message', '')[:80]}")
    
    # Erreurs par type
    errors_by_type = report.get("errors_by_type", {})
    if errors_by_type:
        print(f"\n[WARN]  ERREURS PAR TYPE:")
        for error_type, count in sorted(errors_by_type.items(), key=lambda x: x[1], reverse=True):
            print(f"   - {error_type}: {count}")
    
    # Statut
    if report.get("stop_requested"):
        print("\n[STOP] TEST ARRÊTÉ - Erreur critique détectée")
    elif summary.get('total_questions', 0) >= 5000:
        print("\n[OK] TEST TERMINÉ - 5000 questions complétées")
    else:
        remaining = 5000 - summary.get('total_questions', 0)
        print(f"\n⏳ TEST EN COURS - {remaining} questions restantes")
    
    print("\n" + "=" * 60)
    
except json.JSONDecodeError:
    print("\n[WARN]  Le rapport est en cours d'écriture...")
except Exception as e:
    print(f"\n[ERR] Erreur lors de la lecture du rapport: {e}")



