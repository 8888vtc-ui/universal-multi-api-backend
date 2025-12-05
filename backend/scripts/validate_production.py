#!/usr/bin/env python3
"""
Script de Validation Production
Teste tous les aspects critiques avant déploiement
"""
import asyncio
import sys
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple

# Ajouter le répertoire parent au path
sys.path.insert(0, str(Path(__file__).parent.parent))

import httpx
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

BASE_URL = os.getenv("API_URL", "http://localhost:8000")

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


class ProductionValidator:
    """Validateur pour la production"""
    
    def __init__(self):
        self.results: List[Tuple[str, bool, str, str]] = []  # (category, success, test, details)
        self.start_time = datetime.now()
        self.critical_failures = []
    
    def add_result(self, category: str, success: bool, test: str, details: str = ""):
        """Ajouter un résultat"""
        self.results.append((category, success, test, details))
        if not success and category in ["Sécurité", "Santé", "Endpoints Critiques"]:
            self.critical_failures.append(f"{category}: {test}")
    
    async def check_server_accessible(self) -> bool:
        """Vérifier que le serveur est accessible"""
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{BASE_URL}/api/health")
                return response.status_code == 200
        except:
            return False
    
    async def validate_security(self):
        """Valider la sécurité"""
        print_section("🔐 VALIDATION SÉCURITÉ")
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                response = await client.get(f"{BASE_URL}/api/health")
                headers = response.headers
                
                # Security headers
                required_headers = {
                    "X-Content-Type-Options": "nosniff",
                    "X-Frame-Options": ["DENY", "SAMEORIGIN"],
                    "X-XSS-Protection": "1; mode=block",
                    "Referrer-Policy": ["no-referrer", "strict-origin-when-cross-origin"],
                    "X-API-Version": None,  # Juste présent
                    "X-Request-ID": None
                }
                
                missing = []
                for header, expected in required_headers.items():
                    if header not in headers:
                        missing.append(header)
                        self.add_result("Sécurité", False, f"Header {header} manquant", "")
                    else:
                        if expected and isinstance(expected, list):
                            if headers[header] not in expected:
                                self.add_result("Sécurité", False, f"Header {header} invalide", 
                                              f"Reçu: {headers[header]}")
                            else:
                                self.add_result("Sécurité", True, f"Header {header}", "")
                        elif expected and headers[header] != expected:
                            self.add_result("Sécurité", False, f"Header {header} invalide", 
                                          f"Reçu: {headers[header]}, Attendu: {expected}")
                        else:
                            self.add_result("Sécurité", True, f"Header {header}", "")
                
                if not missing:
                    print_success("Tous les security headers présents")
                
                # JWT Secret Key (vérification séparée)
                jwt_secret = os.getenv("JWT_SECRET_KEY", "")
                env_check = os.getenv("ENVIRONMENT", "development")
                if env_check == "production":
                    if not jwt_secret or jwt_secret == "your-secret-key-here" or len(jwt_secret) < 32:
                        print_error("JWT_SECRET_KEY non configuré ou trop court (CRITIQUE en production)")
                        self.add_result("Sécurité", False, "JWT_SECRET_KEY", "Non configuré ou invalide")
                    else:
                        print_success("JWT_SECRET_KEY configuré")
                        self.add_result("Sécurité", True, "JWT_SECRET_KEY", "")
                else:
                    if not jwt_secret or jwt_secret == "your-secret-key-here":
                        print_warning("JWT_SECRET_KEY non configuré (OK en développement)")
                        self.add_result("Sécurité", True, "JWT_SECRET_KEY", "Non configuré (dev)")
                    else:
                        print_success("JWT_SECRET_KEY configuré")
                        self.add_result("Sécurité", True, "JWT_SECRET_KEY", "")
                
            except Exception as e:
                print_error(f"Erreur validation sécurité: {e}")
                import traceback
                print_error(f"Traceback: {traceback.format_exc()}")
                self.add_result("Sécurité", False, "Validation sécurité", str(e))
    
    async def validate_health(self):
        """Valider les health checks"""
        print_section("🏥 VALIDATION HEALTH CHECKS")
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            endpoints = [
                ("/api/health", "Health Simple"),
                ("/api/health/deep", "Deep Health"),
                ("/api/health/ready", "Kubernetes Ready"),
                ("/api/health/live", "Kubernetes Live")
            ]
            
            for endpoint, name in endpoints:
                try:
                    response = await client.get(f"{BASE_URL}{endpoint}")
                    if response.status_code == 200:
                        data = response.json() if response.headers.get("content-type", "").startswith("application/json") else {}
                        status = data.get("status", "ok")
                        print_success(f"{name}: {status}")
                        self.add_result("Santé", True, name, status)
                    elif response.status_code == 503:
                        print_warning(f"{name}: Service unavailable")
                        self.add_result("Santé", False, name, "Service unavailable")
                    else:
                        print_error(f"{name}: {response.status_code}")
                        self.add_result("Santé", False, name, f"Status {response.status_code}")
                except Exception as e:
                    print_error(f"{name}: {e}")
                    self.add_result("Santé", False, name, str(e))
    
    async def validate_metrics(self):
        """Valider les métriques"""
        print_section("📊 VALIDATION MÉTRIQUES")
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            endpoints = [
                ("/api/metrics", "JSON Metrics"),
                ("/api/metrics/prometheus", "Prometheus Metrics"),
                ("/api/metrics/summary", "Summary Metrics")
            ]
            
            for endpoint, name in endpoints:
                try:
                    response = await client.get(f"{BASE_URL}{endpoint}")
                    if response.status_code == 200:
                        if endpoint == "/api/metrics/prometheus":
                            # Vérifier le format Prometheus
                            content = response.text
                            if "# TYPE" in content and "# HELP" in content:
                                print_success(f"{name}: Format Prometheus valide")
                                self.add_result("Métriques", True, name, "")
                            else:
                                print_warning(f"{name}: Format Prometheus suspect")
                                self.add_result("Métriques", False, name, "Format invalide")
                        else:
                            data = response.json()
                            print_success(f"{name}: OK")
                            self.add_result("Métriques", True, name, "")
                    else:
                        print_error(f"{name}: {response.status_code}")
                        self.add_result("Métriques", False, name, f"Status {response.status_code}")
                except Exception as e:
                    print_error(f"{name}: {e}")
                    self.add_result("Métriques", False, name, str(e))
    
    async def validate_critical_endpoints(self):
        """Valider les endpoints critiques"""
        print_section("🔌 VALIDATION ENDPOINTS CRITIQUES")
        
        async with httpx.AsyncClient(timeout=15.0) as client:
            # Root
            try:
                response = await client.get(f"{BASE_URL}/")
                if response.status_code == 200:
                    data = response.json()
                    version = data.get("version", "unknown")
                    print_success(f"Root endpoint: v{version}")
                    self.add_result("Endpoints Critiques", True, "Root", version)
                else:
                    print_error(f"Root: {response.status_code}")
                    self.add_result("Endpoints Critiques", False, "Root", f"Status {response.status_code}")
            except Exception as e:
                print_error(f"Root: {e}")
                self.add_result("Endpoints Critiques", False, "Root", str(e))
            
            # API Info
            try:
                response = await client.get(f"{BASE_URL}/api/info")
                if response.status_code == 200:
                    data = response.json()
                    env = data.get("environment", "unknown")
                    print_success(f"API Info: {env}")
                    self.add_result("Endpoints Critiques", True, "API Info", env)
                else:
                    print_error(f"API Info: {response.status_code}")
                    self.add_result("Endpoints Critiques", False, "API Info", f"Status {response.status_code}")
            except Exception as e:
                print_error(f"API Info: {e}")
                self.add_result("Endpoints Critiques", False, "API Info", str(e))
            
            # Chat (si disponible)
            try:
                response = await client.post(
                    f"{BASE_URL}/api/chat",
                    json={"message": "test", "language": "en"},
                    timeout=30.0
                )
                if response.status_code == 200:
                    print_success("Chat endpoint: OK")
                    self.add_result("Endpoints Critiques", True, "Chat", "")
                elif response.status_code == 503:
                    print_warning("Chat: Service unavailable (pas de providers AI)")
                    self.add_result("Endpoints Critiques", False, "Chat", "No AI providers")
                else:
                    print_warning(f"Chat: {response.status_code}")
                    self.add_result("Endpoints Critiques", False, "Chat", f"Status {response.status_code}")
            except Exception as e:
                print_warning(f"Chat: {e}")
                self.add_result("Endpoints Critiques", False, "Chat", str(e))
    
    async def validate_error_handling(self):
        """Valider la gestion d'erreurs"""
        print_section("⚠️  VALIDATION ERROR HANDLING")
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            # 404
            try:
                response = await client.get(f"{BASE_URL}/api/nonexistent")
                if response.status_code == 404:
                    data = response.json()
                    if "request_id" in data:
                        print_success("404 avec request_id: OK")
                        self.add_result("Error Handling", True, "404 Handler", "")
                    else:
                        print_warning("404 sans request_id")
                        self.add_result("Error Handling", False, "404 Handler", "No request_id")
                else:
                    print_warning(f"404 test: {response.status_code}")
                    self.add_result("Error Handling", False, "404 Handler", f"Status {response.status_code}")
            except Exception as e:
                print_error(f"404 test: {e}")
                self.add_result("Error Handling", False, "404 Handler", str(e))
    
    async def validate_environment(self):
        """Valider l'environnement"""
        print_section("🌍 VALIDATION ENVIRONNEMENT")
        
        # Variables critiques
        critical_vars = {
            "JWT_SECRET_KEY": "Obligatoire en production",
            "API_PORT": "Port du serveur",
            "ENVIRONMENT": "Environnement (development/production)"
        }
        
        for var, desc in critical_vars.items():
            value = os.getenv(var)
            if not value:
                print_warning(f"{var}: Non défini - {desc}")
                self.add_result("Environnement", False, var, "Non défini")
            elif var == "JWT_SECRET_KEY" and (value == "your-secret-key-here" or len(value) < 32):
                print_error(f"{var}: Invalide (trop court ou valeur par défaut)")
                self.add_result("Environnement", False, var, "Invalide")
            else:
                masked = value[:8] + "..." if len(value) > 8 else "***"
                print_success(f"{var}: {masked}")
                self.add_result("Environnement", True, var, "")
        
        # Variables optionnelles mais recommandées
        optional_vars = ["REDIS_HOST", "REDIS_PORT", "REDIS_PASSWORD"]
        for var in optional_vars:
            value = os.getenv(var)
            if value:
                print_info(f"{var}: Configuré")
            else:
                print_warning(f"{var}: Non configuré (optionnel)")
    
    def print_summary(self):
        """Afficher le résumé"""
        print_section("📊 RÉSUMÉ DE VALIDATION")
        
        # Grouper par catégorie
        categories = {}
        for category, success, test, details in self.results:
            if category not in categories:
                categories[category] = {"total": 0, "passed": 0, "failed": 0, "tests": []}
            categories[category]["total"] += 1
            if success:
                categories[category]["passed"] += 1
            else:
                categories[category]["failed"] += 1
            categories[category]["tests"].append((test, success, details))
        
        # Afficher par catégorie
        total_passed = 0
        total_failed = 0
        
        for category, stats in categories.items():
            print(f"\n{category}:")
            print(f"  ✅ Réussis: {stats['passed']}/{stats['total']}")
            if stats['failed'] > 0:
                print(f"  ❌ Échoués: {stats['failed']}/{stats['total']}")
            
            for test, success, details in stats["tests"]:
                if success:
                    print_success(f"    {test}" + (f" - {details}" if details else ""))
                else:
                    print_error(f"    {test}" + (f" - {details}" if details else ""))
            
            total_passed += stats['passed']
            total_failed += stats['failed']
        
        # Résumé global
        total = total_passed + total_failed
        success_rate = (total_passed / total * 100) if total > 0 else 0
        
        print(f"\n{'='*70}")
        print(f"Total: {total} tests")
        print_success(f"Réussis: {total_passed}")
        if total_failed > 0:
            print_error(f"Échoués: {total_failed}")
        print(f"Taux de réussite: {success_rate:.1f}%")
        
        duration = (datetime.now() - self.start_time).total_seconds()
        print(f"\n⏱️  Durée: {duration:.2f}s")
        
        # Verdict
        print(f"\n{'='*70}")
        env = os.getenv("ENVIRONMENT", "development")
        
        # Filtrer les échecs critiques selon l'environnement
        real_critical = []
        for failure in self.critical_failures:
            # JWT_SECRET_KEY n'est critique qu'en production
            if "JWT_SECRET_KEY" in failure and env != "production":
                continue
            real_critical.append(failure)
        
        if real_critical:
            print_error("❌ VALIDATION ÉCHOUÉE - Problèmes critiques détectés:")
            for failure in real_critical:
                print_error(f"  - {failure}")
            print_warning("\n⚠️  Ne pas déployer en production avant correction")
            return 1
        elif total_failed > 0:
            print_warning("⚠️  VALIDATION AVEC AVERTISSEMENTS")
            print_warning("Certains tests ont échoué mais ne sont pas critiques")
            if env == "development":
                print_info("Environnement développement - certains avertissements sont normaux")
            return 0
        else:
            print_success("✅ VALIDATION RÉUSSIE - Prêt pour production")
            return 0


async def main():
    """Fonction principale"""
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    
    print(f"\n{'='*70}")
    print(f"{BOLD}🧪 VALIDATION PRODUCTION - Universal Multi-API Backend v2.3.0{RESET}")
    print(f"{'='*70}\n")
    
    validator = ProductionValidator()
    
    # Vérifier que le serveur est accessible
    print_info("Vérification du serveur...")
    if not await validator.check_server_accessible():
        print_error(f"Le serveur n'est pas accessible sur {BASE_URL}")
        print_info("Démarrez le serveur avec: cd backend && python scripts/start_server.py")
        return 1
    
    print_success(f"Serveur accessible sur {BASE_URL}\n")
    
    # Exécuter toutes les validations
    await validator.validate_environment()
    await validator.validate_security()
    await validator.validate_health()
    await validator.validate_metrics()
    await validator.validate_critical_endpoints()
    await validator.validate_error_handling()
    
    # Résumé
    return validator.print_summary()


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)

