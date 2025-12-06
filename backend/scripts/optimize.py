"""
Script d'optimisation
Analyse et suggère des optimisations
"""
import sqlite3
from pathlib import Path
from collections import Counter
from datetime import datetime, timedelta


def analyze_database_performance(db_path: str = "./data/analytics.db"):
    """Analyser la performance de la base de données"""
    if not Path(db_path).exists():
        print("⚠️  Base de données analytics non trouvée")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Vérifier les index
    cursor.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='index' AND tbl_name='metrics'
    """)
    indexes = [row[0] for row in cursor.fetchall()]
    
    print("📊 Analyse Base de Données Analytics")
    print("="*60)
    print(f"\n✅ Index existants: {len(indexes)}")
    for idx in indexes:
        print(f"   - {idx}")
    
    # Compter les enregistrements
    cursor.execute("SELECT COUNT(*) FROM metrics")
    total_metrics = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM errors")
    total_errors = cursor.fetchone()[0]
    
    print(f"\n📈 Statistiques:")
    print(f"   Métriques: {total_metrics:,}")
    print(f"   Erreurs: {total_errors:,}")
    
    # Analyser la taille
    cursor.execute("SELECT page_count * page_size as size FROM pragma_page_count(), pragma_page_size()")
    size_bytes = cursor.fetchone()[0]
    size_mb = size_bytes / (1024 * 1024)
    
    print(f"   Taille: {size_mb:.2f} MB")
    
    # Vérifier les requêtes lentes (si possible)
    if total_metrics > 0:
        cursor.execute("""
            SELECT endpoint, AVG(response_time_ms) as avg_time, COUNT(*) as count
            FROM metrics
            WHERE timestamp > datetime('now', '-7 days')
            GROUP BY endpoint
            ORDER BY avg_time DESC
            LIMIT 10
        """)
        
        slow_endpoints = cursor.fetchall()
        if slow_endpoints:
            print(f"\n🐌 Endpoints les plus lents (7 derniers jours):")
            for endpoint, avg_time, count in slow_endpoints:
                print(f"   {endpoint}: {avg_time:.2f} ms ({count} requêtes)")
    
    conn.close()


def suggest_optimizations():
    """Suggérer des optimisations"""
    print("\n" + "="*60)
    print("💡 SUGGESTIONS D'OPTIMISATION")
    print("="*60)
    
    suggestions = [
        {
            "category": "Cache",
            "suggestion": "Utiliser Redis pour cache des réponses fréquentes",
            "impact": "high",
            "effort": "medium"
        },
        {
            "category": "Database",
            "suggestion": "Nettoyer les anciennes métriques (> 30 jours)",
            "impact": "medium",
            "effort": "low"
        },
        {
            "category": "API Calls",
            "suggestion": "Implémenter batch requests pour réduire appels externes",
            "impact": "high",
            "effort": "high"
        },
        {
            "category": "Async",
            "suggestion": "Vérifier que tous les appels API sont asynchrones",
            "impact": "medium",
            "effort": "low"
        },
        {
            "category": "Rate Limiting",
            "suggestion": "Ajuster les limites selon l'utilisation réelle",
            "impact": "low",
            "effort": "low"
        }
    ]
    
    for i, sug in enumerate(suggestions, 1):
        print(f"\n{i}. [{sug['category']}] {sug['suggestion']}")
        print(f"   Impact: {sug['impact']} | Effort: {sug['effort']}")


def check_health():
    """Vérifier la santé du système"""
    print("\n" + "="*60)
    print("❤️  VÉRIFICATION SANTÉ")
    print("="*60)
    
    checks = []
    
    # Vérifier base de données analytics
    if Path("./data/analytics.db").exists():
        checks.append(("Base de données Analytics", "✅ OK"))
    else:
        checks.append(("Base de données Analytics", "⚠️  Non trouvée"))
    
    # Vérifier base de données assistant
    if Path("./data/assistant.db").exists():
        checks.append(("Base de données Assistant", "✅ OK"))
    else:
        checks.append(("Base de données Assistant", "⚠️  Non trouvée"))
    
    # Vérifier répertoire storage
    if Path("./storage/videos").exists():
        checks.append(("Répertoire Storage", "✅ OK"))
    else:
        checks.append(("Répertoire Storage", "⚠️  Non trouvé"))
    
    for check, status in checks:
        print(f"   {check}: {status}")
    
    return all("✅" in status for _, status in checks)


if __name__ == "__main__":
    print("🔧 OPTIMISATION - Universal Multi-API Backend")
    print("="*60)
    
    # Vérifier santé
    health_ok = check_health()
    
    # Analyser performance
    analyze_database_performance()
    
    # Suggestions
    suggest_optimizations()
    
    print("\n" + "="*60)
    if health_ok:
        print("✅ Système en bonne santé")
    else:
        print("⚠️  Certains composants nécessitent attention")
    print("="*60)



