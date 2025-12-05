"""
Tests pour le service Analytics
"""
import pytest
from fastapi.testclient import TestClient
from services.analytics.metrics_collector import MetricsCollector
import os
import tempfile


@pytest.fixture
def temp_db():
    """Créer une base de données temporaire pour les tests"""
    with tempfile.NamedTemporaryFile(delete=False, suffix='.db') as f:
        db_path = f.name
    
    collector = MetricsCollector(db_path=db_path)
    yield collector
    
    # Nettoyer
    if os.path.exists(db_path):
        os.unlink(db_path)


class TestMetricsCollector:
    """Tests pour MetricsCollector"""
    
    def test_record_request(self, temp_db):
        """Test enregistrement d'une requête"""
        temp_db.record_request(
            endpoint="/api/test",
            method="GET",
            status_code=200,
            response_time_ms=100.5
        )
        
        metrics = temp_db.get_metrics(days=1)
        assert metrics["total_requests"] == 1
        assert metrics["avg_response_time_ms"] == 100.5
    
    def test_record_error(self, temp_db):
        """Test enregistrement d'une erreur"""
        temp_db.record_error(
            endpoint="/api/test",
            error_type="ValueError",
            error_message="Test error"
        )
        
        errors = temp_db.get_errors(days=1)
        assert errors["total_errors"] == 1
        assert "ValueError" in errors["error_types"]
    
    def test_get_top_endpoints(self, temp_db):
        """Test top endpoints"""
        # Enregistrer plusieurs requêtes
        for i in range(5):
            temp_db.record_request(
                endpoint=f"/api/endpoint{i}",
                method="GET",
                status_code=200,
                response_time_ms=50.0
            )
        
        # Plus de requêtes pour endpoint0
        for i in range(3):
            temp_db.record_request(
                endpoint="/api/endpoint0",
                method="GET",
                status_code=200,
                response_time_ms=50.0
            )
        
        top = temp_db.get_top_endpoints(days=1, limit=3)
        assert len(top) == 3
        assert top[0]["endpoint"] == "/api/endpoint0"
        assert top[0]["requests"] == 4  # 1 + 3
    
    def test_get_performance_stats(self, temp_db):
        """Test statistiques de performance"""
        # Enregistrer plusieurs requêtes avec différents temps
        times = [50.0, 100.0, 150.0, 200.0]
        for time in times:
            temp_db.record_request(
                endpoint="/api/test",
                method="GET",
                status_code=200,
                response_time_ms=time
            )
        
        stats = temp_db.get_performance_stats(days=1)
        assert stats["total_requests"] == 4
        assert stats["min_response_time_ms"] == 50.0
        assert stats["max_response_time_ms"] == 200.0
        assert stats["avg_response_time_ms"] == 125.0


class TestAnalyticsEndpoints:
    """Tests pour les endpoints analytics"""
    
    @pytest.fixture
    def client(self):
        """Créer un client de test"""
        from main import app
        return TestClient(app)
    
    def test_get_metrics(self, client):
        """Test endpoint /api/analytics/metrics"""
        response = client.get("/api/analytics/metrics?days=7")
        assert response.status_code == 200
        data = response.json()
        assert "success" in data
        assert "total_requests" in data
        assert "period_days" in data
    
    def test_get_errors(self, client):
        """Test endpoint /api/analytics/errors"""
        response = client.get("/api/analytics/errors?days=7")
        assert response.status_code == 200
        data = response.json()
        assert "success" in data
        assert "total_errors" in data
    
    def test_get_top_endpoints(self, client):
        """Test endpoint /api/analytics/endpoints/top"""
        response = client.get("/api/analytics/endpoints/top?days=7&limit=10")
        assert response.status_code == 200
        data = response.json()
        assert "success" in data
        assert "endpoints" in data
    
    def test_get_performance(self, client):
        """Test endpoint /api/analytics/performance"""
        response = client.get("/api/analytics/performance?days=7")
        assert response.status_code == 200
        data = response.json()
        assert "success" in data
        assert "avg_response_time_ms" in data
    
    def test_get_dashboard(self, client):
        """Test endpoint /api/analytics/dashboard"""
        response = client.get("/api/analytics/dashboard?days=7")
        assert response.status_code == 200
        data = response.json()
        assert "success" in data
        assert "summary" in data
        assert "metrics" in data
        assert "errors" in data
    
    def test_health_check(self, client):
        """Test endpoint /api/analytics/health"""
        response = client.get("/api/analytics/health")
        assert response.status_code == 200
        data = response.json()
        assert "success" in data
        assert "status" in data


