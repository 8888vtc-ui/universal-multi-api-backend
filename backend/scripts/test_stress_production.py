"""
Script de test de charge pour le serveur de production
Teste directement sur le serveur déployé
"""
import sys
import subprocess

# URL du serveur de production
PRODUCTION_URL = "https://universal-api-hub.fly.dev"

print("[ROCKET] Lancement du test de charge sur le serveur de production...")
print(f"📍 URL: {PRODUCTION_URL}\n")

# Lancer le test avec l'URL de production
result = subprocess.run([
    sys.executable,
    "backend/scripts/test_stress_5000.py",
    "--url", PRODUCTION_URL,
    "--max", "5000",
    "--output", "backend/stress_test_report.json"
], cwd=".")

sys.exit(result.returncode)


Script de test de charge pour le serveur de production
Teste directement sur le serveur déployé
"""
import sys
import subprocess

# URL du serveur de production
PRODUCTION_URL = "https://universal-api-hub.fly.dev"

print("[ROCKET] Lancement du test de charge sur le serveur de production...")
print(f"📍 URL: {PRODUCTION_URL}\n")

# Lancer le test avec l'URL de production
result = subprocess.run([
    sys.executable,
    "backend/scripts/test_stress_5000.py",
    "--url", PRODUCTION_URL,
    "--max", "5000",
    "--output", "backend/stress_test_report.json"
], cwd=".")

sys.exit(result.returncode)



