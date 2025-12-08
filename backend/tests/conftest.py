"""
Configuration pytest globale
"""
import pytest
import os
import sys

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


@pytest.fixture(scope="session")
def test_env():
    """Configuration environnement de test"""
    # Variables d'environnement pour tests
    os.environ.setdefault("TESTING", "true")
    os.environ.setdefault("REDIS_URL", "")  # Désactiver Redis pour tests
    yield
    # Cleanup après tests
    if "TESTING" in os.environ:
        del os.environ["TESTING"]


<<<<<<< Updated upstream
=======





>>>>>>> Stashed changes
