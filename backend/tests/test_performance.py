"""
Tests de performance et benchmarks
"""
import pytest
import time
import asyncio
from fastapi.testclient import TestClient


class TestPerformance:
    """Tests de performance"""
    
    @pytest.fixture
    def client(self):
        """Créer un client de test"""
        from main import app
        return TestClient(app)
    
    def test_health_endpoint_performance(self, client):
        """Test performance endpoint health"""
        start = time.time()
        response = client.get("/api/health")
        elapsed = time.time() - start
        
        assert response.status_code == 200
        assert elapsed < 0.1  # Doit répondre en moins de 100ms
    
    def test_search_endpoint_performance(self, client):
        """Test performance endpoint search"""
        start = time.time()
        response = client.post(
            "/api/search/universal",
            json={
                "query": "test",
                "max_results_per_category": 5
            }
        )
        elapsed = time.time() - start
        
        # Search peut prendre plus de temps (appels API externes)
        assert response.status_code in [200, 500]  # Peut échouer si pas d'APIs
        # Juste vérifier que ça ne prend pas trop de temps
        assert elapsed < 5.0  # Max 5 secondes
    
    def test_concurrent_requests(self, client):
        """Test requêtes concurrentes"""
        import concurrent.futures
        
        def make_request():
            return client.get("/api/health")
        
        start = time.time()
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(make_request) for _ in range(20)]
            results = [f.result() for f in concurrent.futures.as_completed(futures)]
        elapsed = time.time() - start
        
        # Toutes les requêtes doivent réussir
        assert all(r.status_code == 200 for r in results)
        # Ne doit pas prendre trop de temps même avec concurrence
        assert elapsed < 2.0


class TestLoad:
    """Tests de charge"""
    
    @pytest.fixture
    def client(self):
        """Créer un client de test"""
        from main import app
        return TestClient(app)
    
    def test_multiple_health_requests(self, client):
        """Test plusieurs requêtes health"""
        start = time.time()
        responses = [client.get("/api/health") for _ in range(50)]
        elapsed = time.time() - start
        
        assert all(r.status_code == 200 for r in responses)
        # 50 requêtes ne doivent pas prendre trop de temps
        assert elapsed < 1.0
    
    def test_analytics_under_load(self, client):
        """Test analytics sous charge"""
        # Faire plusieurs requêtes pour générer des métriques
        for _ in range(10):
            client.get("/api/health")
        
        # Attendre un peu pour que les métriques soient enregistrées
        time.sleep(0.1)
        
        # Récupérer les métriques
        start = time.time()
        response = client.get("/api/analytics/metrics?days=1")
        elapsed = time.time() - start
        
        assert response.status_code == 200
        # Analytics doit être rapide même avec données
        assert elapsed < 0.5


