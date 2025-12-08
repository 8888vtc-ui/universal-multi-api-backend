"""
Script de monitoring pour suivre la progression du test de charge
"""
import json
import time
import os
from datetime import datetime

REPORT_FILE = "stress_test_report.json"

def monitor_test():
    """Surveille le fichier de rapport"""
    print("[INFO] Monitoring du test de charge...")
    print("Appuyez sur Ctrl+C pour arrêter\n")
    
    last_size = 0
    iteration = 0
    
    try:
        while True:
            if os.path.exists(REPORT_FILE):
                try:
                    with open(REPORT_FILE, "r", encoding="utf-8") as f:
                        report = json.load(f)
                    
                    summary = report.get("summary", {})
                    total = summary.get("total_questions", 0)
                    successful = summary.get("successful", 0)
                    failed = summary.get("failed", 0)
                    success_rate = summary.get("success_rate", "0%")
                    
                    if total > 0:
                        print(f"\r📊 Progression: {total} questions | "
                              f"[OK] {successful} | [ERR] {failed} | "
                              f"Taux: {success_rate} | "
                              f"Erreurs critiques: {len(report.get('critical_errors', []))}", 
                              end="", flush=True)
                    
                    # Vérifier si le test est terminé
                    if report.get("stop_requested"):
                        print("\n\n[STOP] Test arrêté - Erreur critique détectée!")
                        break
                    
                except (json.JSONDecodeError, KeyError):
                    # Fichier en cours d'écriture
                    pass
            
            time.sleep(2)
            iteration += 1
            
            if iteration % 30 == 0:
                print(f"\n⏳ En attente... ({iteration * 2}s écoulés)")
    
    except KeyboardInterrupt:
        print("\n\n⏹️  Monitoring arrêté")
    
    # Afficher le rapport final
    if os.path.exists(REPORT_FILE):
        print("\n📄 Rapport final disponible dans:", REPORT_FILE)

if __name__ == "__main__":
    monitor_test()


Script de monitoring pour suivre la progression du test de charge
"""
import json
import time
import os
from datetime import datetime

REPORT_FILE = "stress_test_report.json"

def monitor_test():
    """Surveille le fichier de rapport"""
    print("[INFO] Monitoring du test de charge...")
    print("Appuyez sur Ctrl+C pour arrêter\n")
    
    last_size = 0
    iteration = 0
    
    try:
        while True:
            if os.path.exists(REPORT_FILE):
                try:
                    with open(REPORT_FILE, "r", encoding="utf-8") as f:
                        report = json.load(f)
                    
                    summary = report.get("summary", {})
                    total = summary.get("total_questions", 0)
                    successful = summary.get("successful", 0)
                    failed = summary.get("failed", 0)
                    success_rate = summary.get("success_rate", "0%")
                    
                    if total > 0:
                        print(f"\r📊 Progression: {total} questions | "
                              f"[OK] {successful} | [ERR] {failed} | "
                              f"Taux: {success_rate} | "
                              f"Erreurs critiques: {len(report.get('critical_errors', []))}", 
                              end="", flush=True)
                    
                    # Vérifier si le test est terminé
                    if report.get("stop_requested"):
                        print("\n\n[STOP] Test arrêté - Erreur critique détectée!")
                        break
                    
                except (json.JSONDecodeError, KeyError):
                    # Fichier en cours d'écriture
                    pass
            
            time.sleep(2)
            iteration += 1
            
            if iteration % 30 == 0:
                print(f"\n⏳ En attente... ({iteration * 2}s écoulés)")
    
    except KeyboardInterrupt:
        print("\n\n⏹️  Monitoring arrêté")
    
    # Afficher le rapport final
    if os.path.exists(REPORT_FILE):
        print("\n📄 Rapport final disponible dans:", REPORT_FILE)

if __name__ == "__main__":
    monitor_test()



