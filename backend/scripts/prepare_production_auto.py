#!/usr/bin/env python3
"""
Script de Préparation Production (Version Automatique)
Génère automatiquement tout ce qui est nécessaire sans interaction
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
    if not env_path.exists():
        if env_example_path.exists():
            import shutil
            shutil.copy(env_example_path, env_path)
            print_success(".env créé depuis .env.example")
        else:
            print_error(".env.example non trouvé")
            return False
    
    # Lire le contenu actuel
    lines = []
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
    
    return True


def main():
    """Fonction principale"""
    print_section("🚀 PRÉPARATION PRODUCTION (AUTOMATIQUE)")
    
    # Vérifier qu'on est dans le bon répertoire
    if not Path("main.py").exists() and not Path(".env.example").exists():
        print_error("Ce script doit être exécuté depuis le répertoire backend/")
        print_info("Usage: cd backend && python scripts/prepare_production_auto.py")
        return 1
    
    updates = {}
    
    # Vérifier .env
    env_path = Path(".env")
    env_example_path = Path(".env.example")
    
    if not env_path.exists():
        if env_example_path.exists():
            import shutil
            shutil.copy(env_example_path, env_path)
            print_success(".env créé depuis .env.example")
        else:
            print_error(".env.example non trouvé")
            return 1
    
    # Lire les variables actuelles
    env_vars = read_env_file()
    
    # Générer JWT_SECRET_KEY si nécessaire
    print_section("🔐 Configuration JWT_SECRET_KEY")
    
    jwt_secret = env_vars.get("JWT_SECRET_KEY", "")
    if not jwt_secret or jwt_secret == "your-secret-key-here" or len(jwt_secret) < 32:
        new_jwt = generate_jwt_secret()
        updates["JWT_SECRET_KEY"] = new_jwt
        print_success(f"JWT_SECRET_KEY généré: {new_jwt[:20]}...")
        print_info("JWT_SECRET_KEY sera mis à jour dans .env")
    else:
        print_success("JWT_SECRET_KEY déjà configuré")
    
    # Configuration ENVIRONMENT
    print_section("🌍 Configuration ENVIRONMENT")
    
    current_env = env_vars.get("ENVIRONMENT", "development")
    print_info(f"Environnement actuel: {current_env}")
    
    # Ne pas forcer production, juste s'assurer qu'il est défini
    if "ENVIRONMENT" not in env_vars:
        updates["ENVIRONMENT"] = "development"
        print_info("ENVIRONMENT défini: development (changez en 'production' pour la prod)")
    else:
        print_success(f"ENVIRONMENT déjà configuré: {current_env}")
    
    # Mettre à jour .env
    if updates:
        print_section("💾 Mise à jour de .env")
        if update_env_file(updates):
            print_success(f"{len(updates)} variable(s) mise(s) à jour dans .env")
        else:
            print_error("Erreur lors de la mise à jour de .env")
            return 1
    
    # Checklist des clés API
    print_section("🔑 Checklist Clés API")
    
    api_keys = {
        "AI": [
            "GROQ_API_KEY",
            "MISTRAL_API_KEY",
            "GEMINI_API_KEY",
            "ANTHROPIC_API_KEY",
            "COHERE_API_KEY",
            "AI21_API_KEY",
            "HUGGINGFACE_API_TOKEN",
            "PERPLEXITY_API_KEY"
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
    
    total_keys = len(sum(api_keys.values(), []))
    print(f"Clés API configurées: {len(configured)}/{total_keys}")
    
    if missing:
        print_warning(f"Clés API manquantes: {len(missing)}")
        print_info("Configurez-les dans .env pour activer toutes les fonctionnalités")
        print_info("Note: Vous n'avez pas besoin de toutes les clés, seulement celles que vous utilisez")
    else:
        print_success("Toutes les clés API sont configurées !")
    
    # Générer un fichier de configuration production
    print_section("📝 Génération Configuration Production")
    
    prod_config = f"""
# Configuration Production - Générée le {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Variables Configurées
- JWT_SECRET_KEY: {'✅ Configuré' if 'JWT_SECRET_KEY' in updates or (env_vars.get('JWT_SECRET_KEY') and len(env_vars.get('JWT_SECRET_KEY', '')) >= 32) else '❌ Non configuré'}
- ENVIRONMENT: {env_vars.get('ENVIRONMENT', 'development')}

## Clés API
- Configurées: {len(configured)}/{total_keys}
- Manquantes: {len(missing)}

## Prochaines Étapes
1. Vérifier que JWT_SECRET_KEY est sécurisé (32+ caractères)
2. Configurer les clés API nécessaires dans .env
3. Changer ENVIRONMENT=production pour la production
4. Exécuter: sudo bash backend/scripts/deploy.sh production
5. Vérifier: sudo bash backend/scripts/verify_deployment.sh
"""
    
    config_path = Path("PRODUCTION_CONFIG.txt")
    with open(config_path, 'w', encoding='utf-8') as f:
        f.write(prod_config)
    
    print_success(f"Configuration sauvegardée dans {config_path}")
    
    # Recommandations
    print_section("💡 Recommandations")
    
    print("Avant le déploiement en production:")
    print("  1. ✅ JWT_SECRET_KEY généré et configuré")
    if current_env != "production":
        print("  2. ⏳ Changer ENVIRONMENT=production dans .env")
    print("  3. ⏳ Configurer les clés API nécessaires dans .env")
    print("  4. ⏳ Vérifier la configuration avec: python scripts/check_api_config.py")
    print("  5. ⏳ Déployer avec: sudo bash scripts/deploy.sh production")
    print("  6. ⏳ Vérifier avec: sudo bash scripts/verify_deployment.sh")
    
    print("\nVoir MIGRATION_COMPLETE.md pour les détails complets")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

