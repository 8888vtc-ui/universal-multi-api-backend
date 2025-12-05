#!/usr/bin/env python3
"""
Script de Vérification Complète
Vérifie que tout est correctement configuré et fonctionnel
"""
import os
import sys
import asyncio
import httpx
from pathlib import Path

# Colors for terminal
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"

def print_success(msg):
    print(f"{GREEN}✅ {msg}{RESET}")

def print_error(msg):
    print(f"{RED}❌ {msg}{RESET}")

def print_warning(msg):
    print(f"{YELLOW}⚠️  {msg}{RESET}")

def print_info(msg):
    print(f"{BLUE}ℹ️  {msg}{RESET}")


def check_python_version():
    """Vérifier la version Python"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 9:
        print_success(f"Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print_error(f"Python {version.major}.{version.minor} (requis: 3.9+)")
        return False


def check_dependencies():
    """Vérifier les dépendances critiques"""
    required = [
        "fastapi",
        "uvicorn",
        "httpx",
        "pydantic",
        "jose",
        "passlib",
        "redis",
    ]
    
    missing = []
    for dep in required:
        try:
            __import__(dep.replace("-", "_"))
            print_success(f"{dep} installé")
        except ImportError:
            if dep == "redis":
                print_warning(f"{dep} non installé (cache mémoire en fallback)")
            else:
                print_error(f"{dep} non installé")
                missing.append(dep)
    
    return len(missing) == 0


def check_env_file():
    """Vérifier le fichier .env"""
    env_path = Path(".env")
    if env_path.exists():
        print_success(".env existe")
        
        # Vérifier JWT_SECRET_KEY
        from dotenv import load_dotenv
        load_dotenv()
        
        jwt_key = os.getenv("JWT_SECRET_KEY")
        if jwt_key and jwt_key != "your-secret-key-change-in-production":
            print_success("JWT_SECRET_KEY configuré")
        else:
            print_warning("JWT_SECRET_KEY non configuré ou valeur par défaut")
        
        return True
    else:
        print_error(".env n'existe pas (copier .env.example)")
        return False


def check_directories():
    """Vérifier les répertoires nécessaires"""
    dirs = ["data", "logs"]
    all_ok = True
    
    for dir_name in dirs:
        dir_path = Path(dir_name)
        if dir_path.exists():
            print_success(f"Répertoire {dir_name}/ existe")
        else:
            try:
                dir_path.mkdir(parents=True, exist_ok=True)
                print_success(f"Répertoire {dir_name}/ créé")
            except Exception as e:
                print_error(f"Impossible de créer {dir_name}/: {e}")
                all_ok = False
    
    return all_ok


async def check_server_running():
    """Vérifier si le serveur est en cours d'exécution"""
    port = int(os.getenv("API_PORT", 8000))
    url = f"http://localhost:{port}"
    
    try:
        async with httpx.AsyncClient(timeout=2.0) as client:
            response = await client.get(f"{url}/api/health")
            if response.status_code == 200:
                print_success(f"Serveur accessible sur {url}")
                return True
            else:
                print_warning(f"Serveur répond avec {response.status_code}")
                return False
    except httpx.ConnectError:
        print_warning(f"Serveur non démarré sur {url}")
        print_info("Démarrer avec: python main.py")
        return False
    except Exception as e:
        print_error(f"Erreur de connexion: {e}")
        return False


def check_ai_providers():
    """Vérifier les providers AI configurés"""
    from dotenv import load_dotenv
    load_dotenv()
    
    providers = {
        "GROQ_API_KEY": "Groq",
        "MISTRAL_API_KEY": "Mistral",
        "GEMINI_API_KEY": "Gemini",
        "OPENROUTER_API_KEY": "OpenRouter",
        "OPENAI_API_KEY": "OpenAI",
    }
    
    configured = []
    for key, name in providers.items():
        if os.getenv(key):
            configured.append(name)
            print_success(f"{name} configuré")
    
    if not configured:
        print_warning("Aucun provider AI configuré")
        print_info("Configurer au moins une clé API ou installer Ollama")
    else:
        print_success(f"{len(configured)} provider(s) AI configuré(s)")
    
    return len(configured) > 0


def check_redis():
    """Vérifier Redis"""
    try:
        import sys
        from pathlib import Path
        # Ajouter le répertoire parent au path
        sys.path.insert(0, str(Path(__file__).parent.parent))
        
        from services.cache import cache_service
        if cache_service.available:
            print_success("Redis connecté")
            return True
        else:
            print_warning("Redis non disponible (cache mémoire actif)")
            return False
    except Exception as e:
        print_warning(f"Redis: {e}")
        return False


async def main():
    """Fonction principale"""
    import sys
    import io
    # Forcer UTF-8 pour Windows
    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    
    print("\n" + "="*60)
    print("VÉRIFICATION COMPLÈTE DU SETUP")
    print("="*60 + "\n")
    
    checks = {
        "Python Version": check_python_version(),
        "Dépendances": check_dependencies(),
        "Fichier .env": check_env_file(),
        "Répertoires": check_directories(),
        "Providers AI": check_ai_providers(),
        "Redis": check_redis(),
        "Serveur": await check_server_running(),
    }
    
    print("\n" + "="*60)
    print("📊 RÉSUMÉ")
    print("="*60)
    
    passed = sum(1 for v in checks.values() if v)
    total = len(checks)
    
    for name, result in checks.items():
        status = "✅" if result else "⚠️"
        print(f"{status} {name}")
    
    print(f"\n{passed}/{total} vérifications passées")
    
    if passed == total:
        print_success("\n🎉 Tout est configuré correctement !")
        return 0
    elif passed >= total - 2:
        print_warning("\n⚠️  Configuration presque complète (warnings acceptables)")
        return 0
    else:
        print_error("\n❌ Des problèmes critiques doivent être résolus")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
