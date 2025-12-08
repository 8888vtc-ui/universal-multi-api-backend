"""
Startup Validator
Vérifie la configuration au démarrage de l'application
"""
import os
import logging
import sys
from typing import List, Tuple, Dict, Any

logger = logging.getLogger(__name__)


class StartupValidator:
    """Validates configuration on startup"""
    
    # Variables d'environnement critiques (production)
    CRITICAL_VARS = [
        ("JWT_SECRET_KEY", "Authentication will fail without this"),
    ]
    
    # Variables recommandées (warning si manquantes)
    RECOMMENDED_VARS = [
        ("REDIS_URL", "Caching disabled - performance impact"),
        ("CORS_ORIGINS", "Using default localhost:3000"),
    ]
    
    # Au moins une de ces variables pour chaque catégorie
    AI_PROVIDER_VARS = [
        "GROQ_API_KEY",
        "MISTRAL_API_KEY",
        "GEMINI_API_KEY",
        "OPENAI_API_KEY",
        "OPENROUTER_API_KEY",
        # Ollama n'a pas besoin de clé
    ]
    
    @classmethod
    def validate_environment(cls) -> Tuple[bool, List[str]]:
        """
        Valide les variables d'environnement
        Returns: (is_valid, list_of_errors)
        """
        errors = []
        warnings = []
        
        is_production = os.getenv("ENVIRONMENT", "development") == "production"
        
        # Vérifier les variables critiques en production
        if is_production:
            for var_name, description in cls.CRITICAL_VARS:
                if not os.getenv(var_name):
                    errors.append(f"❌ CRITICAL: {var_name} not set - {description}")
        
        # Vérifier les variables recommandées
        for var_name, description in cls.RECOMMENDED_VARS:
            if not os.getenv(var_name):
                warnings.append(f"⚠️  {var_name} not set - {description}")
        
        # Vérifier qu'au moins un provider AI est disponible
        has_ai_provider = any(os.getenv(var) for var in cls.AI_PROVIDER_VARS)
        if not has_ai_provider:
            warnings.append(
                "⚠️  No AI provider configured. "
                "Set at least one of: GROQ_API_KEY, MISTRAL_API_KEY, etc. "
                "Or install Ollama locally for free AI."
            )
        
        return len(errors) == 0, errors + warnings
    
    @classmethod
    def validate_dependencies(cls) -> Tuple[bool, List[str]]:
        """
        Vérifie les dépendances Python requises
        Returns: (is_valid, list_of_errors)
        """
        errors = []
        
        required_packages = [
            ("fastapi", "Core framework"),
            ("pydantic", "Data validation"),
            ("httpx", "HTTP client"),
            ("redis", "Caching (optional)"),
            ("jose", "JWT tokens"),
            ("passlib", "Password hashing"),
        ]
        
        for package, description in required_packages:
            try:
                __import__(package)
            except ImportError:
                if package == "redis":
                    logger.warning(f"⚠️  {package} not installed - {description}")
                else:
                    errors.append(f"❌ {package} not installed - {description}")
        
        return len(errors) == 0, errors
    
    @classmethod
    def validate_directories(cls) -> Tuple[bool, List[str]]:
        """
        Vérifie que les répertoires nécessaires existent
        """
        errors = []
        
        required_dirs = [
            "./data",
            "./logs",
        ]
        
        for dir_path in required_dirs:
            try:
                os.makedirs(dir_path, exist_ok=True)
            except Exception as e:
                errors.append(f"❌ Cannot create directory {dir_path}: {e}")
        
        return len(errors) == 0, errors
    
    @classmethod
    def run_all_validations(cls, fail_on_error: bool = True) -> Dict[str, Any]:
        """
        Exécute toutes les validations
        
        Args:
            fail_on_error: Si True, lève une exception en cas d'erreur critique
        
        Returns:
            Dict avec les résultats de validation
        """
        results = {
            "environment": {"valid": True, "messages": []},
            "dependencies": {"valid": True, "messages": []},
            "directories": {"valid": True, "messages": []},
            "overall_valid": True
        }
        
        logger.info("🔍 Running startup validations...")
        
        # Environment
        valid, messages = cls.validate_environment()
        results["environment"] = {"valid": valid, "messages": messages}
        for msg in messages:
            if "CRITICAL" in msg:
                logger.error(msg)
            else:
                logger.warning(msg)
        
        # Dependencies
        valid, messages = cls.validate_dependencies()
        results["dependencies"] = {"valid": valid, "messages": messages}
        for msg in messages:
            logger.error(msg)
        
        # Directories
        valid, messages = cls.validate_directories()
        results["directories"] = {"valid": valid, "messages": messages}
        for msg in messages:
            logger.error(msg)
        
        # Overall status
        results["overall_valid"] = all([
            results["environment"]["valid"],
            results["dependencies"]["valid"],
            results["directories"]["valid"]
        ])
        
        if results["overall_valid"]:
            logger.info("✅ All startup validations passed")
        else:
            logger.error("❌ Some startup validations failed")
            
            if fail_on_error and os.getenv("ENVIRONMENT") == "production":
                logger.error("Refusing to start in production with validation errors")
                sys.exit(1)
        
        return results


def validate_startup(fail_on_error: bool = True) -> Dict[str, Any]:
    """Helper function to run startup validation"""
    return StartupValidator.run_all_validations(fail_on_error)


<<<<<<< Updated upstream
=======





>>>>>>> Stashed changes
