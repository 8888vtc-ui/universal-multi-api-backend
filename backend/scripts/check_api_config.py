"""
Script de vérification de configuration des APIs
Vérifie que les variables d'environnement sont correctement configurées
"""
import sys
import os
from pathlib import Path

# Ajouter le répertoire parent au path
sys.path.insert(0, str(Path(__file__).parent.parent))

from services.api_health_checker import api_health_checker
from services.api_fallback_manager import api_fallback_manager


def main():
    """Vérifier la configuration des APIs"""
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    
    print("="*60)
    print("VÉRIFICATION DE CONFIGURATION DES APIs")
    print("="*60)
    print()
    
    # Vérifier toutes les APIs
    health = api_health_checker.check_all_apis()
    missing = api_health_checker.get_missing_keys()
    recommendations = api_health_checker.get_recommendations()
    fallback_status = api_fallback_manager.check_all_categories()
    
    # Résumé
    print("📊 RÉSUMÉ")
    print("-" * 60)
    print(f"Total APIs configurées: {health['summary']['total_apis']}")
    print(f"APIs disponibles: {health['summary']['available_apis']}")
    print(f"APIs manquantes: {health['summary']['unavailable_apis']}")
    print(f"Taux de disponibilité: {health['summary']['availability_rate']}%")
    print()
    
    # APIs manquantes
    if missing:
        print("CLÉS API MANQUANTES")
        print("-" * 60)
        for item in missing:
            print(f"[X] {item['api']:20} -> {item['env_var']}")
            if item['fallback']:
                print(f"   Fallback disponible: {item['fallback']}")
        print()
    
    # Statut par catégorie
    print("STATUT PAR CATÉGORIE")
    print("-" * 60)
    for category, data in fallback_status.items():
        status_icon = "[OK]" if data["status"] == "OK" else "[!]" if data["count"] > 0 else "[X]"
        print(f"{status_icon} {category:15} → {data['count']} provider(s) disponible(s)")
        if data["available_providers"]:
            print(f"   Providers: {', '.join(data['available_providers'])}")
        print(f"   {data['recommendation']}")
        print()
    
    # Recommandations
    if recommendations:
        print("RECOMMANDATIONS")
        print("-" * 60)
        for rec in recommendations:
            print(f"   {rec}")
        print()
    
    # Vérifier fallback critique
    critical = [cat for cat, data in fallback_status.items() if data["status"] == "CRITICAL"]
    if critical:
        print("CATÉGORIES CRITIQUES (Aucun provider disponible)")
        print("-" * 60)
        for cat in critical:
            print(f"   [X] {cat}")
        print()
        print("ATTENTION: Ces catégories ne fonctionneront pas sans configuration !")
        return 1
    
    # Vérifier fallback unique
    single_fallback = [cat for cat, data in fallback_status.items() if data["count"] == 1]
    if single_fallback:
        print("CATÉGORIES AVEC UN SEUL PROVIDER (Pas de fallback)")
        print("-" * 60)
        for cat in single_fallback:
            print(f"   [!] {cat}: {fallback_status[cat]['available_providers'][0]}")
        print()
        print("ASTUCE: Ajoutez plus de providers pour avoir un fallback")
        print()
    
    print("="*60)
    print("Vérification terminée")
    print("="*60)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

