#!/usr/bin/env python3
"""
Script de Préparation Production
Génère les configurations nécessaires pour le déploiement
"""
import os
import sys
import secrets
from pathlib import Path
from datetime import datetime

# Colors
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"
RESET = "\033[0m"
BOLD = "\033[1m"

def print_success(msg):
    print(f"{GREEN}✅ {msg}{RESET}")

def print_error(msg):
    print(f"{RED}❌ {msg}{RESET}")

def print_warning(msg):
    print(f"{YELLOW}⚠️  {msg}{RESET}")

def print_info(msg):
    print(f"{BLUE}ℹ️  {msg}{RESET}")

def print_section(msg):
    print(f"\n{CYAN}{BOLD}{'='*70}{RESET}")
    print(f"{CYAN}{BOLD}{msg}{RESET}")
    print(f"{CYAN}{BOLD}{'='*70}{RESET}\n")


def generate_jwt_secret():
    """Générer un JWT_SECRET_KEY sécurisé"""
    return secrets.token_urlsafe(32)


def check_env_file():
    """Vérifier si .env existe"""
    env_path = Path(".env")
    env_example_path = Path(".env.example")
    
    if not env_path.exists():
        if env_example_path.exists():
            print_warning(".env n'existe pas")
            print_info("Copiez .env.example vers .env")
            return False
        else:
            print_error(".env.example n'existe pas")
            return False
    
    return True


def read_env_file():
    """Lire le fichier .env"""
    env_path = Path(".env")
    if not env_path.exists():
        return {}
    
    env_vars = {}
    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                env_vars[key.strip()] = value.strip()
    
    return env_vars


def update_env_file(updates: dict):
    """Mettre à jour le fichier .env"""
    env_path = Path(".env")
    env_example_path = Path(".env.example")
    
    # Si .env n'existe pas, copier depuis .env.example
    if not env_path.exists() and env_example_path.exists():
        import shutil
        shutil.copy(env_example_path, env_path)
        print_success(".env créé depuis .env.example")
    
    # Lire le contenu actuel
    lines = []
    if env_path.exists():
        with open(env_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    
    # Mettre à jour les variables
    updated = set()
    new_lines = []
    
    for line in lines:
        stripped = line.strip()
        if stripped and not stripped.startswith('#') and '=' in stripped:
            key = stripped.split('=', 1)[0].strip()
            if key in updates:
                new_lines.append(f"{key}={updates[key]}\n")
                updated.add(key)
                continue
        
        new_lines.append(line)
    
    # Ajouter les nouvelles variables
    for key, value in updates.items():
        if key not in updated:
            new_lines.append(f"{key}={value}\n")
    
    # Écrire le fichier
    with open(env_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    return len(updates)


def main():
    """Fonction principale"""
    print_section("🚀 PRÉPARATION PRODUCTION")
    
    # Vérifier qu'on est dans le bon répertoire
    if not Path("main.py").exists() and not Path(".env.example").exists():
        print_error("Ce script doit être exécuté depuis le répertoire backend/")
        print_info("Usage: cd backend && python scripts/prepare_production.py")
        return 1
    
    # Vérifier .env
    if not check_env_file():
        response = input("Créer .env depuis .env.example ? (o/N): ")
        if response.lower() == 'o':
            import shutil
            shutil.copy(".env.example", ".env")
            print_success(".env créé")
        else:
            print_warning("Continuez sans .env (non recommandé)")
    
    # Lire les variables actuelles
    env_vars = read_env_file()
    
    # Générer JWT_SECRET_KEY si nécessaire
    print_section("🔐 Configuration JWT_SECRET_KEY")
    
    jwt_secret = env_vars.get("JWT_SECRET_KEY", "")
    if not jwt_secret or jwt_secret == "your-secret-key-here" or len(jwt_secret) < 32:
        new_jwt = generate_jwt_secret()
        print_success(f"JWT_SECRET_KEY généré: {new_jwt[:20]}...")
        
        response = input("Mettre à jour .env avec ce JWT_SECRET_KEY ? (o/N): ")
        if response.lower() == 'o':
            update_env_file({"JWT_SECRET_KEY": new_jwt})
            print_success("JWT_SECRET_KEY mis à jour dans .env")
        else:
            print_info("JWT_SECRET_KEY non mis à jour")
            print_info(f"Copiez cette valeur dans .env: {new_jwt}")
    else:
        print_success("JWT_SECRET_KEY déjà configuré")
    
    # Configuration ENVIRONMENT
    print_section("🌍 Configuration ENVIRONMENT")
    
    current_env = env_vars.get("ENVIRONMENT", "development")
    print_info(f"Environnement actuel: {current_env}")
    
    if current_env != "production":
        response = input("Passer en mode production ? (o/N): ")
        if response.lower() == 'o':
            update_env_file({"ENVIRONMENT": "production"})
            print_success("ENVIRONMENT mis à jour: production")
        else:
            print_info("ENVIRONMENT reste en développement")
    else:
        print_success("ENVIRONMENT déjà en production")
    
    # Checklist des clés API
    print_section("🔑 Checklist Clés API")
    
    api_keys = {
        "AI": [
            "GROQ_API_KEY",
            "MISTRAL_API_KEY",
            "GEMINI_API_KEY",
            "COHERE_API_KEY",
            "HUGGINGFACE_API_KEY"
        ],
        "Finance": [
            "ALPHA_VANTAGE_API_KEY",
            "COINGECKO_API_KEY"
        ],
        "News": [
            "NEWS_API_KEY",
            "NEWSDATA_API_KEY"
        ],
        "Weather": [
            "WEATHER_API_KEY"
        ],
        "Other": [
            "OPENAI_API_KEY",
            "ANTHROPIC_API_KEY",
            "DEEPSEEK_API_KEY"
        ]
    }
    
    print_info("Vérification des clés API...")
    
    missing = []
    configured = []
    
    for category, keys in api_keys.items():
        print(f"\n{category}:")
        for key in keys:
            value = env_vars.get(key, "")
            if value and value not in ["", "your-api-key-here"]:
                print_success(f"  {key}: Configuré")
                configured.append(key)
            else:
                print_warning(f"  {key}: Non configuré")
                missing.append(key)
    
    # Résumé
    print_section("📊 Résumé")
    
    print(f"Clés API configurées: {len(configured)}/{len(sum(api_keys.values(), []))}")
    
    if missing:
        print_warning(f"Clés API manquantes: {len(missing)}")
        print_info("Configurez-les dans .env pour activer toutes les fonctionnalités")
    else:
        print_success("Toutes les clés API sont configurées !")
    
    # Recommandations
    print_section("💡 Recommandations")
    
    print("Avant le déploiement en production:")
    print("  1. ✅ JWT_SECRET_KEY généré et configuré")
    print("  2. ⏳ Configurer toutes les clés API nécessaires")
    print("  3. ⏳ Vérifier ENVIRONMENT=production")
    print("  4. ⏳ Configurer Redis (optionnel mais recommandé)")
    print("  5. ⏳ Configurer SSL/HTTPS")
    print("  6. ⏳ Configurer monitoring (Prometheus)")
    
    print("\nVoir DEPLOYMENT_GUIDE.md pour les détails complets")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

