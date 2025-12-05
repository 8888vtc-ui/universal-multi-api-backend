"""
Tests pour le service Assistant Personnel IA
"""
import pytest
from services.assistant.memory_store import MemoryStore
from services.assistant.preference_learner import PreferenceLearner
from services.assistant.assistant_router import AssistantRouter
import os
import tempfile


@pytest.fixture
def temp_db():
    """Créer une base de données temporaire pour les tests"""
    with tempfile.NamedTemporaryFile(delete=False, suffix='.db') as f:
        db_path = f.name
    
    store = MemoryStore(db_path=db_path)
    yield store
    
    # Nettoyer
    if os.path.exists(db_path):
        os.unlink(db_path)


class TestMemoryStore:
    """Tests pour MemoryStore"""
    
    def test_save_interaction(self, temp_db):
        """Test sauvegarde d'interaction"""
        temp_db.save_interaction(
            user_id="test_user",
            query="bitcoin prix",
            category="finance",
            action="search"
        )
        
        interactions = temp_db.get_user_interactions("test_user", limit=10)
        assert len(interactions) == 1
        assert interactions[0]["query"] == "bitcoin prix"
        assert interactions[0]["category"] == "finance"
    
    def test_save_preferences(self, temp_db):
        """Test sauvegarde de préférences"""
        preferences = {
            "finance": {
                "weight": 0.8,
                "keywords": ["bitcoin", "crypto"]
            }
        }
        
        temp_db.save_preferences("test_user", preferences)
        saved = temp_db.get_preferences("test_user")
        assert saved["finance"]["weight"] == 0.8
        assert "bitcoin" in saved["finance"]["keywords"]
    
    def test_get_user_stats(self, temp_db):
        """Test statistiques utilisateur"""
        # Ajouter plusieurs interactions
        for i in range(5):
            temp_db.save_interaction(
                user_id="test_user",
                query=f"query{i}",
                category="finance" if i % 2 == 0 else "news",
                action="search"
            )
        
        stats = temp_db.get_user_stats("test_user")
        assert stats["total_interactions"] == 5
        assert "finance" in stats["category_counts"]
        assert "news" in stats["category_counts"]


class TestPreferenceLearner:
    """Tests pour PreferenceLearner"""
    
    @pytest.fixture
    def learner(self, temp_db):
        """Créer un learner avec base de données temporaire"""
        from services.assistant.preference_learner import PreferenceLearner
        learner = PreferenceLearner()
        learner.memory_store = temp_db
        return learner
    
    def test_learn_from_interactions(self, learner, temp_db):
        """Test apprentissage depuis interactions"""
        # Ajouter plusieurs interactions
        for i in range(10):
            temp_db.save_interaction(
                user_id="test_user",
                query="bitcoin crypto",
                category="finance",
                action="search"
            )
        
        preferences = learner.learn_from_interactions("test_user")
        assert "finance" in preferences
        assert preferences["finance"]["weight"] > 0
        assert "bitcoin" in preferences["finance"].get("keywords", [])
    
    def test_get_user_preferences(self, learner, temp_db):
        """Test obtention préférences"""
        # Ajouter interactions
        temp_db.save_interaction(
            user_id="test_user",
            query="bitcoin",
            category="finance",
            action="search"
        )
        
        preferences = learner.get_user_preferences("test_user")
        # Devrait apprendre automatiquement
        assert isinstance(preferences, dict)


class TestAssistantRouter:
    """Tests pour AssistantRouter"""
    
    @pytest.fixture
    def router(self, temp_db):
        """Créer un router avec base de données temporaire"""
        router = AssistantRouter()
        router.memory_store = temp_db
        return router
    
    @pytest.mark.asyncio
    async def test_learn_from_interaction(self, router):
        """Test apprentissage d'interaction"""
        result = await router.learn_from_interaction(
            user_id="test_user",
            query="bitcoin prix",
            category="finance",
            action="search"
        )
        
        assert result["learned"] is True
        assert "total_interactions" in result
    
    @pytest.mark.asyncio
    async def test_get_recommendations(self, router):
        """Test recommandations"""
        # Ajouter quelques interactions d'abord
        for i in range(5):
            await router.learn_from_interaction(
                user_id="test_user",
                query="bitcoin crypto",
                category="finance",
                action="search"
            )
        
        recommendations = await router.get_recommendations(
            user_id="test_user",
            limit=5
        )
        
        assert "recommendations" in recommendations
        # Peut être vide si pas assez de données
        assert isinstance(recommendations["recommendations"], list)
    
    def test_get_user_profile(self, router):
        """Test profil utilisateur"""
        profile = router.get_user_profile("test_user")
        assert "user_id" in profile or "total_interactions" in profile


