"""
Logging Configuration
Configuration centralisée des logs pour tout le backend
"""
import os
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional


def setup_logging(
    level: str = None,
    log_file: str = None,
    json_format: bool = False
) -> None:
    """
    Configure le logging pour l'application
    
    Args:
        level: Niveau de log (DEBUG, INFO, WARNING, ERROR)
        log_file: Chemin du fichier de log (optionnel)
        json_format: Si True, utilise le format JSON pour les logs
    """
    # Niveau de log depuis env ou paramètre
    log_level = level or os.getenv("LOG_LEVEL", "INFO")
    
    # Format des logs
    if json_format:
        try:
            import json
            
            class JSONFormatter(logging.Formatter):
                def format(self, record):
                    log_obj = {
                        "timestamp": datetime.utcnow().isoformat(),
                        "level": record.levelname,
                        "logger": record.name,
                        "message": record.getMessage(),
                        "module": record.module,
                        "function": record.funcName,
                        "line": record.lineno
                    }
                    if record.exc_info:
                        log_obj["exception"] = self.formatException(record.exc_info)
                    return json.dumps(log_obj)
            
            formatter = JSONFormatter()
        except ImportError:
            json_format = False
    
    if not json_format:
        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)-8s | %(name)s:%(lineno)d | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
    
    # Configuration du root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level.upper()))
    
    # Handler console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, log_level.upper()))
    console_handler.setFormatter(formatter)
    
    # Supprimer les handlers existants pour éviter les doublons
    root_logger.handlers = []
    root_logger.addHandler(console_handler)
    
    # Handler fichier (optionnel)
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(log_path, encoding="utf-8")
        file_handler.setLevel(getattr(logging, log_level.upper()))
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
    
    # Réduire le bruit des librairies tierces
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("yfinance").setLevel(logging.WARNING)
    
    # Log de démarrage
    logger = logging.getLogger(__name__)
    logger.info(f"🚀 Logging configured: level={log_level}, json={json_format}")
    
    if log_file:
        logger.info(f"📝 Log file: {log_file}")


def get_logger(name: str) -> logging.Logger:
    """
    Obtenir un logger configuré
    
    Usage:
        from services.logging_config import get_logger
        logger = get_logger(__name__)
    """
    return logging.getLogger(name)


# Auto-configure logging when module is imported
_configured = False

def ensure_logging_configured():
    """Ensure logging is configured (call once at startup)"""
    global _configured
    if not _configured:
        log_file = os.getenv("LOG_FILE")
        json_logs = os.getenv("JSON_LOGS", "false").lower() == "true"
        setup_logging(log_file=log_file, json_format=json_logs)
        _configured = True


