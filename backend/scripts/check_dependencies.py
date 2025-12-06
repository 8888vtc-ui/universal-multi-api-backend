"""
Script de vérification des dépendances
Vérifie que toutes les dépendances sont installées
"""
import sys
import importlib
from typing import List, Tuple


REQUIRED_PACKAGES = [
    # Core
    ("fastapi", "FastAPI"),
    ("uvicorn", "Uvicorn"),
    ("pydantic", "Pydantic"),
    ("httpx", "HTTPX"),
    
    # AI
    ("groq", "Groq"),
    ("cohere", "Cohere"),
    
    # Database & Cache
    ("redis", "Redis (optionnel)"),
    
    # External APIs
    ("yfinance", "Yahoo Finance"),
    
    # Testing
    ("pytest", "Pytest (optionnel)"),
    
    # Rate Limiting
    ("slowapi", "SlowAPI (optionnel)"),
    
    # Circuit Breaker
    ("circuitbreaker", "Circuit Breaker"),
    
    # Email
    ("email_validator", "Email Validator"),
]


def check_package(package_name: str, display_name: str) -> Tuple[bool, str]:
    """Vérifier si un package est installé"""
    try:
        importlib.import_module(package_name)
        return True, "✅"
    except ImportError:
        return False, "❌"


def main():
    """Vérifier toutes les dépendances"""
    print("="*60)
    print("🔍 VÉRIFICATION DES DÉPENDANCES")
    print("="*60)
    print()
    
    missing = []
    optional_missing = []
    
    for package, display_name in REQUIRED_PACKAGES:
        installed, status = check_package(package, display_name)
        
        if not installed:
            if "optionnel" in display_name.lower():
                optional_missing.append((package, display_name))
                print(f"{status} {display_name:40} (optionnel)")
            else:
                missing.append((package, display_name))
                print(f"{status} {display_name:40} MANQUANT")
        else:
            print(f"{status} {display_name:40}")
    
    print()
    print("="*60)
    
    if missing:
        print(f"\n❌ {len(missing)} dépendance(s) REQUISE(S) manquante(s):")
        for package, display_name in missing:
            print(f"   - {package} ({display_name})")
        print("\n💡 Installez avec: pip install -r requirements.txt")
        return 1
    
    if optional_missing:
        print(f"\n⚠️  {len(optional_missing)} dépendance(s) OPTIONNELLE(S) manquante(s):")
        for package, display_name in optional_missing:
            print(f"   - {package} ({display_name})")
        print("\n💡 Ces dépendances sont optionnelles mais recommandées")
    
    print("\n✅ Toutes les dépendances requises sont installées!")
    return 0


if __name__ == "__main__":
    sys.exit(main())



