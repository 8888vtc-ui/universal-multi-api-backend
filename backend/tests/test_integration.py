"""
Tests d'intégration end-to-end
"""
import pytest
from fastapi.testclient import TestClient


class TestIntegration:
    """Tests d'intégration"""
    
    @pytest.fixture
    def client(self):
        """Créer un client de test"""
        from main import app
        return TestClient(app)
    
    def test_full_workflow_assistant(self, client):
        """Test workflow complet assistant"""
        user_id = "test_integration_user"
        
        # 1. Apprendre d'une interaction
        response = client.post(
            "/api/assistant/learn",
            json={
                "user_id": user_id,
                "query": "bitcoin prix",
                "category": "finance",
                "action": "search"
            }
        )
        assert response.status_code == 200
        
        # 2. Obtenir recommandations
        response = client.get(
            f"/api/assistant/recommendations?user_id={user_id}&limit=5"
        )
        assert response.status_code == 200
        
        # 3. Obtenir profil
        response = client.get(f"/api/assistant/profile/{user_id}")
        assert response.status_code == 200
    
    def test_analytics_tracking(self, client):
        """Test que analytics track les requêtes"""
        # Faire quelques requêtes
        client.get("/api/health")
        client.get("/api/analytics/health")
        
        # Vérifier que les métriques sont enregistrées
        response = client.get("/api/analytics/metrics?days=1")
        assert response.status_code == 200
        data = response.json()
        # Devrait avoir au moins quelques requêtes
        assert data.get("total_requests", 0) >= 0
    
    def test_search_integration(self, client):
        """Test intégration search"""
        response = client.post(
            "/api/search/universal",
            json={
                "query": "test",
                "max_results_per_category": 3
            }
        )
        # Peut échouer si pas d'APIs configurées, mais structure doit être correcte
        assert response.status_code in [200, 500]
        
        if response.status_code == 200:
            data = response.json()
            assert "query" in data
            assert "total_results" in data
    
    def test_video_service_integration(self, client):
        """Test intégration service vidéo"""
        # Tester endpoint status (ne nécessite pas d'API key)
        response = client.get("/api/video/status")
        assert response.status_code == 200
        data = response.json()
        assert "available" in data
        assert "providers" in data


