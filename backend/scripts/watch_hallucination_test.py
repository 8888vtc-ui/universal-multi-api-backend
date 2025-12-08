"""
Script de surveillance en temps réel du test de détection d'hallucinations
Affiche les logs et la progression en direct
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

import json
import os
import time
from datetime import datetime
from collections import defaultdict

REPORT_FILE = "backend/hallucination_test_report.json"

def format_time(seconds):
    """Formate le temps en format lisible"""
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        return f"{int(seconds // 60)}m {int(seconds % 60)}s"
    else:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        return f"{hours}h {minutes}m"

def display_progress(report):
    """Affiche la progression du test"""
    # Effacer l'écran (fonctionne sur Windows et Unix)
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print("=" * 80)
    print("[INFO] MONITORING EN TEMPS RÉEL - TEST DE DÉTECTION D'HALLUCINATIONS")
    print("=" * 80)
    print(f"📅 Dernière mise à jour: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    summary = report.get("summary", {})
    
    # Statistiques principales
    total = summary.get("total_questions", 0)
    successful = summary.get("successful", 0)
    failed = summary.get("failed", 0)
    hallucinations = summary.get("hallucinations_detected", 0)
    total_time = summary.get("total_time_seconds", 0)
    qps = summary.get("questions_per_second", 0)
    
    # Calculer les pourcentages
    if total > 0:
        success_rate = (successful / total) * 100
        fail_rate = (failed / total) * 100
        hall_rate = (hallucinations / successful) * 100 if successful > 0 else 0
    else:
        success_rate = fail_rate = hall_rate = 0
    
    # Afficher les statistiques
    print("📊 STATISTIQUES GLOBALES")
    print("-" * 80)
    print(f"[OK] Questions réussies: {successful:,} / {total:,} ({success_rate:.2f}%)")
    print(f"[ERR] Questions échouées: {failed:,} ({fail_rate:.2f}%)")
    print(f"🚨 Hallucinations détectées: {hallucinations:,} ({hall_rate:.2f}% des réponses)")
    print()
    
    if total_time > 0:
        print(f"⏱️  Temps écoulé: {format_time(total_time)}")
        print(f"⚡ Vitesse: {qps:.2f} questions/seconde")
        
        # Estimer le temps restant
        if qps > 0 and total > 0:
            remaining = (total - successful - failed) / qps if (total - successful - failed) > 0 else 0
            if remaining > 0:
                print(f"⏳ Temps estimé restant: {format_time(remaining)}")
        print()
    
    # Hallucinations par type
    hall_stats = report.get("hallucination_stats", {})
    by_type = hall_stats.get("by_type", {})
    
    if by_type:
        print("🚨 HALLUCINATIONS PAR TYPE")
        print("-" * 80)
        for hall_type, count in sorted(by_type.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / hallucinations * 100) if hallucinations > 0 else 0
            bar_length = int(percentage / 2)  # Barre de 50 caractères max
            bar = "█" * bar_length + "░" * (50 - bar_length)
            print(f"   {hall_type:30s} {count:5d} ({percentage:5.2f}%) {bar}")
        print()
    
    # Top experts avec hallucinations
    by_expert = hall_stats.get("by_expert", {})
    if by_expert:
        print("👤 TOP 10 EXPERTS AVEC HALLUCINATIONS")
        print("-" * 80)
        for i, (expert_id, count) in enumerate(sorted(by_expert.items(), key=lambda x: x[1], reverse=True)[:10], 1):
            print(f"   {i:2d}. {expert_id:20s} {count:5d} hallucination(s)")
        print()
    
    # Dernières hallucinations détectées
    hallucinations_list = report.get("detected_hallucinations", [])
    if hallucinations_list:
        print("🔴 DERNIÈRES HALLUCINATIONS DÉTECTÉES")
        print("-" * 80)
        for i, hall in enumerate(hallucinations_list[-5:], 1):  # 5 dernières
            print(f"\n   {i}. Type: {hall.get('type', 'N/A')}")
            print(f"      Expert: {hall.get('expert_id', 'N/A')}")
            print(f"      Question: {hall.get('query', 'N/A')[:70]}...")
            print(f"      Snippet: {hall.get('response_snippet', 'N/A')[:100]}...")
        print()
    
    # Barre de progression
    if total > 0:
        progress = ((successful + failed) / total) * 100
        bar_length = 50
        filled = int(bar_length * progress / 100)
        bar = "█" * filled + "░" * (bar_length - filled)
        print("📈 PROGRESSION")
        print("-" * 80)
        print(f"   [{bar}] {progress:.1f}% ({successful + failed:,} / {total:,})")
        print()
    
    print("=" * 80)
    print("💡 Appuyez sur Ctrl+C pour arrêter le monitoring")
    print("=" * 80)

def watch_test():
    """Surveille le test en temps réel"""
    print("[INFO] Démarrage du monitoring en temps réel...")
    print("   Recherche du fichier de rapport...")
    print()
    
    last_size = 0
    last_hallucinations = 0
    
    try:
        while True:
            if os.path.exists(REPORT_FILE):
                try:
                    # Lire le fichier
                    with open(REPORT_FILE, "r", encoding="utf-8") as f:
                        content = f.read()
                    
                    if content.strip():
                        report = json.loads(content)
                        display_progress(report)
                        
                        # Détecter les nouvelles hallucinations
                        current_hallucinations = report.get("summary", {}).get("hallucinations_detected", 0)
                        if current_hallucinations > last_hallucinations:
                            new_hallucinations = current_hallucinations - last_hallucinations
                            print(f"\n🚨 ALERTE: {new_hallucinations} nouvelle(s) hallucination(s) détectée(s)!")
                            time.sleep(2)  # Pause pour voir l'alerte
                        
                        last_hallucinations = current_hallucinations
                    else:
                        print("⏳ Le fichier de rapport est vide, le test démarre...")
                        time.sleep(2)
                        
                except json.JSONDecodeError:
                    # Le fichier est en cours d'écriture
                    print("⏳ Le fichier de rapport est en cours d'écriture...")
                    time.sleep(1)
                except Exception as e:
                    print(f"[ERR] Erreur lors de la lecture: {e}")
                    time.sleep(2)
            else:
                print("⏳ En attente du fichier de rapport...")
                print("   Le test devrait démarrer bientôt...")
                time.sleep(2)
            
            # Attendre avant la prochaine mise à jour
            time.sleep(3)  # Mise à jour toutes les 3 secondes
            
    except KeyboardInterrupt:
        print("\n\n[OK] Monitoring arrêté par l'utilisateur")
        print("   Le test continue en arrière-plan")
        print("   Utilisez 'python backend/scripts/monitor_hallucination_test.py' pour voir le rapport final")

if __name__ == "__main__":
    watch_test()


Script de surveillance en temps réel du test de détection d'hallucinations
Affiche les logs et la progression en direct
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

import json
import os
import time
from datetime import datetime
from collections import defaultdict

REPORT_FILE = "backend/hallucination_test_report.json"

def format_time(seconds):
    """Formate le temps en format lisible"""
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        return f"{int(seconds // 60)}m {int(seconds % 60)}s"
    else:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        return f"{hours}h {minutes}m"

def display_progress(report):
    """Affiche la progression du test"""
    # Effacer l'écran (fonctionne sur Windows et Unix)
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print("=" * 80)
    print("[INFO] MONITORING EN TEMPS RÉEL - TEST DE DÉTECTION D'HALLUCINATIONS")
    print("=" * 80)
    print(f"📅 Dernière mise à jour: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    summary = report.get("summary", {})
    
    # Statistiques principales
    total = summary.get("total_questions", 0)
    successful = summary.get("successful", 0)
    failed = summary.get("failed", 0)
    hallucinations = summary.get("hallucinations_detected", 0)
    total_time = summary.get("total_time_seconds", 0)
    qps = summary.get("questions_per_second", 0)
    
    # Calculer les pourcentages
    if total > 0:
        success_rate = (successful / total) * 100
        fail_rate = (failed / total) * 100
        hall_rate = (hallucinations / successful) * 100 if successful > 0 else 0
    else:
        success_rate = fail_rate = hall_rate = 0
    
    # Afficher les statistiques
    print("📊 STATISTIQUES GLOBALES")
    print("-" * 80)
    print(f"[OK] Questions réussies: {successful:,} / {total:,} ({success_rate:.2f}%)")
    print(f"[ERR] Questions échouées: {failed:,} ({fail_rate:.2f}%)")
    print(f"🚨 Hallucinations détectées: {hallucinations:,} ({hall_rate:.2f}% des réponses)")
    print()
    
    if total_time > 0:
        print(f"⏱️  Temps écoulé: {format_time(total_time)}")
        print(f"⚡ Vitesse: {qps:.2f} questions/seconde")
        
        # Estimer le temps restant
        if qps > 0 and total > 0:
            remaining = (total - successful - failed) / qps if (total - successful - failed) > 0 else 0
            if remaining > 0:
                print(f"⏳ Temps estimé restant: {format_time(remaining)}")
        print()
    
    # Hallucinations par type
    hall_stats = report.get("hallucination_stats", {})
    by_type = hall_stats.get("by_type", {})
    
    if by_type:
        print("🚨 HALLUCINATIONS PAR TYPE")
        print("-" * 80)
        for hall_type, count in sorted(by_type.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / hallucinations * 100) if hallucinations > 0 else 0
            bar_length = int(percentage / 2)  # Barre de 50 caractères max
            bar = "█" * bar_length + "░" * (50 - bar_length)
            print(f"   {hall_type:30s} {count:5d} ({percentage:5.2f}%) {bar}")
        print()
    
    # Top experts avec hallucinations
    by_expert = hall_stats.get("by_expert", {})
    if by_expert:
        print("👤 TOP 10 EXPERTS AVEC HALLUCINATIONS")
        print("-" * 80)
        for i, (expert_id, count) in enumerate(sorted(by_expert.items(), key=lambda x: x[1], reverse=True)[:10], 1):
            print(f"   {i:2d}. {expert_id:20s} {count:5d} hallucination(s)")
        print()
    
    # Dernières hallucinations détectées
    hallucinations_list = report.get("detected_hallucinations", [])
    if hallucinations_list:
        print("🔴 DERNIÈRES HALLUCINATIONS DÉTECTÉES")
        print("-" * 80)
        for i, hall in enumerate(hallucinations_list[-5:], 1):  # 5 dernières
            print(f"\n   {i}. Type: {hall.get('type', 'N/A')}")
            print(f"      Expert: {hall.get('expert_id', 'N/A')}")
            print(f"      Question: {hall.get('query', 'N/A')[:70]}...")
            print(f"      Snippet: {hall.get('response_snippet', 'N/A')[:100]}...")
        print()
    
    # Barre de progression
    if total > 0:
        progress = ((successful + failed) / total) * 100
        bar_length = 50
        filled = int(bar_length * progress / 100)
        bar = "█" * filled + "░" * (bar_length - filled)
        print("📈 PROGRESSION")
        print("-" * 80)
        print(f"   [{bar}] {progress:.1f}% ({successful + failed:,} / {total:,})")
        print()
    
    print("=" * 80)
    print("💡 Appuyez sur Ctrl+C pour arrêter le monitoring")
    print("=" * 80)

def watch_test():
    """Surveille le test en temps réel"""
    print("[INFO] Démarrage du monitoring en temps réel...")
    print("   Recherche du fichier de rapport...")
    print()
    
    last_size = 0
    last_hallucinations = 0
    
    try:
        while True:
            if os.path.exists(REPORT_FILE):
                try:
                    # Lire le fichier
                    with open(REPORT_FILE, "r", encoding="utf-8") as f:
                        content = f.read()
                    
                    if content.strip():
                        report = json.loads(content)
                        display_progress(report)
                        
                        # Détecter les nouvelles hallucinations
                        current_hallucinations = report.get("summary", {}).get("hallucinations_detected", 0)
                        if current_hallucinations > last_hallucinations:
                            new_hallucinations = current_hallucinations - last_hallucinations
                            print(f"\n🚨 ALERTE: {new_hallucinations} nouvelle(s) hallucination(s) détectée(s)!")
                            time.sleep(2)  # Pause pour voir l'alerte
                        
                        last_hallucinations = current_hallucinations
                    else:
                        print("⏳ Le fichier de rapport est vide, le test démarre...")
                        time.sleep(2)
                        
                except json.JSONDecodeError:
                    # Le fichier est en cours d'écriture
                    print("⏳ Le fichier de rapport est en cours d'écriture...")
                    time.sleep(1)
                except Exception as e:
                    print(f"[ERR] Erreur lors de la lecture: {e}")
                    time.sleep(2)
            else:
                print("⏳ En attente du fichier de rapport...")
                print("   Le test devrait démarrer bientôt...")
                time.sleep(2)
            
            # Attendre avant la prochaine mise à jour
            time.sleep(3)  # Mise à jour toutes les 3 secondes
            
    except KeyboardInterrupt:
        print("\n\n[OK] Monitoring arrêté par l'utilisateur")
        print("   Le test continue en arrière-plan")
        print("   Utilisez 'python backend/scripts/monitor_hallucination_test.py' pour voir le rapport final")

if __name__ == "__main__":
    watch_test()



