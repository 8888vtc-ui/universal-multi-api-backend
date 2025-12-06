#!/usr/bin/env python3
"""
Script de Démarrage Amélioré
Vérifie la configuration avant de démarrer le serveur
"""
import os
import sys
import asyncio
import subprocess
from pathlib import Path

# Colors
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


def check_prerequisites():
    """Vérifier les prérequis"""
    print("\n🔍 Vérification des prérequis...")
    
    # Python version
    if sys.version_info < (3, 9):
        print_error(f"Python {sys.version_info.major}.{sys.version_info.minor} (requis: 3.9+)")
        return False
    print_success(f"Python {sys.version_info.major}.{sys.version_info.minor}")
    
    # Fichier .env
    env_path = Path(".env")
    if not env_path.exists():
        print_warning(".env n'existe pas")
        print_info("Copiez .env.example vers .env et configurez vos clés API")
    else:
        print_success(".env existe")
    
    # Répertoires
    for dir_name in ["data", "logs"]:
        dir_path = Path(dir_name)
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)
            print_success(f"Répertoire {dir_name}/ créé")
        else:
            print_success(f"Répertoire {dir_name}/ existe")
    
    return True


def check_port_available(port: int = 8000):
    """Vérifier si le port est disponible"""
    import socket
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind(('localhost', port))
        sock.close()
        return True
    except OSError:
        return False


async def check_server_health():
    """Vérifier que le serveur répond"""
    import httpx
    
    try:
        async with httpx.AsyncClient(timeout=2.0) as client:
            response = await client.get("http://localhost:8000/api/health")
            if response.status_code == 200:
                return True
    except:
        pass
    return False


def main():
    """Fonction principale"""
    print("\n" + "="*60)
    print("🚀 DÉMARRAGE DU SERVEUR - Universal Multi-API Backend")
    print("="*60)
    
    # Vérifier les prérequis
    if not check_prerequisites():
        print_error("Prérequis non satisfaits")
        sys.exit(1)
    
    # Vérifier le port
    port = int(os.getenv("API_PORT", 8000))
    if not check_port_available(port):
        print_warning(f"Port {port} déjà utilisé")
        print_info("Arrêtez l'autre instance ou changez API_PORT dans .env")
        response = input("Continuer quand même? (o/N): ")
        if response.lower() != 'o':
            sys.exit(1)
    else:
        print_success(f"Port {port} disponible")
    
    # Vérifier si le serveur est déjà démarré
    print("\n🔍 Vérification si le serveur est déjà démarré...")
    try:
        if asyncio.run(check_server_health()):
            print_warning("Le serveur semble déjà démarré sur http://localhost:8000")
            response = input("Continuer quand même? (o/N): ")
            if response.lower() != 'o':
                print_info("Arrêt")
                sys.exit(0)
    except:
        pass
    
    # Démarrer le serveur
    print("\n" + "="*60)
    print("🚀 DÉMARRAGE DU SERVEUR...")
    print("="*60)
    print(f"\n📡 Serveur: http://localhost:{port}")
    print(f"📚 Docs:    http://localhost:{port}/docs")
    print(f"❤️  Health:  http://localhost:{port}/api/health")
    print(f"\n💡 Appuyez sur Ctrl+C pour arrêter\n")
    
    # Importer et démarrer
    try:
        import uvicorn
        from dotenv import load_dotenv
        
        load_dotenv()
        
        host = os.getenv("API_HOST", "0.0.0.0")
        reload = os.getenv("API_RELOAD", "true").lower() == "true"
        log_level = os.getenv("LOG_LEVEL", "info").lower()
        
        uvicorn.run(
            "main:app",
            host=host,
            port=port,
            reload=reload,
            log_level=log_level,
            access_log=False
        )
    except KeyboardInterrupt:
        print("\n\n🛑 Arrêt du serveur...")
    except Exception as e:
        print_error(f"Erreur au démarrage: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()



