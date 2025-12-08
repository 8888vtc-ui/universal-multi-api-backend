"""
Script de monitoring pour le test de détection d'hallucinations
Affiche la progression en temps réel
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

import json
import os
from datetime import datetime

REPORT_FILE = "backend/hallucination_test_report.json"

def check_progress():
    """Vérifie la progression du test"""
    if not os.path.exists(REPORT_FILE):
        print("⏳ Le test est en cours de démarrage...")
        print("   Le rapport sera disponible une fois le test terminé.")
        return
    
    try:
        with open(REPORT_FILE, "r", encoding="utf-8") as f:
            report = json.load(f)
        
        print("=" * 80)
        print("📊 RAPPORT DE DÉTECTION D'HALLUCINATIONS")
        print("=" * 80)
        
        summary = report.get("summary", {})
        
        print(f"\n[OK] Questions réussies: {summary.get('successful', 0)}")
        print(f"[ERR] Questions échouées: {summary.get('failed', 0)}")
        print(f"🚨 Hallucinations détectées: {summary.get('hallucinations_detected', 0)}")
        print(f"📈 Taux d'hallucinations: {summary.get('hallucination_rate', 0):.2f}%")
        print(f"⏱️  Temps total: {summary.get('total_time_seconds', 0):.2f}s")
        print(f"⚡ Vitesse: {summary.get('questions_per_second', 0):.2f} questions/s")
        
        hall_stats = report.get("hallucination_stats", {})
        
        if hall_stats.get("by_type"):
            print("\n📋 HALLUCINATIONS PAR TYPE:")
            for hall_type, count in sorted(
                hall_stats["by_type"].items(),
                key=lambda x: x[1],
                reverse=True
            ):
                print(f"   - {hall_type}: {count}")
        
        if hall_stats.get("by_expert"):
            print("\n👤 TOP 10 EXPERTS AVEC HALLUCINATIONS:")
            for expert_id, count in sorted(
                hall_stats["by_expert"].items(),
                key=lambda x: x[1],
                reverse=True
            )[:10]:
                print(f"   - {expert_id}: {count}")
        
        # Afficher quelques exemples d'hallucinations
        hallucinations = report.get("detected_hallucinations", [])
        if hallucinations:
            print("\n🚨 EXEMPLES D'HALLUCINATIONS DÉTECTÉES:")
            for i, hall in enumerate(hallucinations[:5], 1):
                print(f"\n   {i}. Type: {hall.get('type', 'N/A')}")
                print(f"      Expert: {hall.get('expert_id', 'N/A')}")
                print(f"      Question: {hall.get('query', 'N/A')}")
                print(f"      Snippet: {hall.get('response_snippet', 'N/A')[:100]}...")
        
        print("\n" + "=" * 80)
        print(f"📅 Rapport généré le: {report.get('timestamp', 'N/A')}")
        print("=" * 80)
        
    except json.JSONDecodeError:
        print("[WARN]  Le fichier de rapport est en cours d'écriture...")
    except Exception as e:
        print(f"[ERR] Erreur lors de la lecture du rapport: {e}")

if __name__ == "__main__":
    check_progress()


Script de monitoring pour le test de détection d'hallucinations
Affiche la progression en temps réel
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

import json
import os
from datetime import datetime

REPORT_FILE = "backend/hallucination_test_report.json"

def check_progress():
    """Vérifie la progression du test"""
    if not os.path.exists(REPORT_FILE):
        print("⏳ Le test est en cours de démarrage...")
        print("   Le rapport sera disponible une fois le test terminé.")
        return
    
    try:
        with open(REPORT_FILE, "r", encoding="utf-8") as f:
            report = json.load(f)
        
        print("=" * 80)
        print("📊 RAPPORT DE DÉTECTION D'HALLUCINATIONS")
        print("=" * 80)
        
        summary = report.get("summary", {})
        
        print(f"\n[OK] Questions réussies: {summary.get('successful', 0)}")
        print(f"[ERR] Questions échouées: {summary.get('failed', 0)}")
        print(f"🚨 Hallucinations détectées: {summary.get('hallucinations_detected', 0)}")
        print(f"📈 Taux d'hallucinations: {summary.get('hallucination_rate', 0):.2f}%")
        print(f"⏱️  Temps total: {summary.get('total_time_seconds', 0):.2f}s")
        print(f"⚡ Vitesse: {summary.get('questions_per_second', 0):.2f} questions/s")
        
        hall_stats = report.get("hallucination_stats", {})
        
        if hall_stats.get("by_type"):
            print("\n📋 HALLUCINATIONS PAR TYPE:")
            for hall_type, count in sorted(
                hall_stats["by_type"].items(),
                key=lambda x: x[1],
                reverse=True
            ):
                print(f"   - {hall_type}: {count}")
        
        if hall_stats.get("by_expert"):
            print("\n👤 TOP 10 EXPERTS AVEC HALLUCINATIONS:")
            for expert_id, count in sorted(
                hall_stats["by_expert"].items(),
                key=lambda x: x[1],
                reverse=True
            )[:10]:
                print(f"   - {expert_id}: {count}")
        
        # Afficher quelques exemples d'hallucinations
        hallucinations = report.get("detected_hallucinations", [])
        if hallucinations:
            print("\n🚨 EXEMPLES D'HALLUCINATIONS DÉTECTÉES:")
            for i, hall in enumerate(hallucinations[:5], 1):
                print(f"\n   {i}. Type: {hall.get('type', 'N/A')}")
                print(f"      Expert: {hall.get('expert_id', 'N/A')}")
                print(f"      Question: {hall.get('query', 'N/A')}")
                print(f"      Snippet: {hall.get('response_snippet', 'N/A')[:100]}...")
        
        print("\n" + "=" * 80)
        print(f"📅 Rapport généré le: {report.get('timestamp', 'N/A')}")
        print("=" * 80)
        
    except json.JSONDecodeError:
        print("[WARN]  Le fichier de rapport est en cours d'écriture...")
    except Exception as e:
        print(f"[ERR] Erreur lors de la lecture du rapport: {e}")

if __name__ == "__main__":
    check_progress()



