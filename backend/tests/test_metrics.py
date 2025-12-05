"""
Tests pour les endpoints de métriques
"""
import pytest
from fastapi.testclient import TestClient
from routers.metrics import router, metrics_collector


@pytest.fixture
def app():
    """App de test"""
    from fastapi import FastAPI
    app = FastAPI()
    app.include_router(router)
    return app


@pytest.fixture
def client(app):
    """Client de test"""
    return TestClient(app)


def test_metrics_endpoint(client):
    """Tester l'endpoint /api/metrics"""
    response = client.get("/api/metrics")
    
    assert response.status_code == 200
    data = response.json()
    
    # Vérifier la structure
    assert "timestamp" in data
    assert "uptime_seconds" in data
    assert "total_requests" in data
    assert "requests_by_endpoint" in data
    assert "errors_by_type" in data


def test_prometheus_endpoint(client):
    """Tester l'endpoint /api/metrics/prometheus"""
    response = client.get("/api/metrics/prometheus")
    
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/plain; charset=utf-8"
    
    # Vérifier le format Prometheus
    content = response.text
    assert "# HELP" in content
    assert "# TYPE" in content
    assert "api_uptime_seconds" in content


def test_metrics_summary_endpoint(client):
    """Tester l'endpoint /api/metrics/summary"""
    response = client.get("/api/metrics/summary")
    
    assert response.status_code == 200
    data = response.json()
    
    # Vérifier la structure
    assert "uptime_hours" in data
    assert "total_requests" in data
    assert "total_errors" in data
    assert "error_rate_percent" in data
    assert "top_endpoints" in data


def test_metrics_collector():
    """Tester le collecteur de métriques"""
    # Enregistrer une requête
    metrics_collector.record_request("GET", "/test", 200, 50.0)
    
    metrics = metrics_collector.get_metrics()
    
    assert "uptime_seconds" in metrics
    assert "total_requests" in metrics
    assert metrics["total_requests"] >= 1


def test_prometheus_format():
    """Tester le format Prometheus"""
    # Enregistrer quelques métriques
    metrics_collector.record_request("GET", "/test", 200, 50.0)
    metrics_collector.record_request("POST", "/api/chat", 200, 100.0)
    
    prometheus_output = metrics_collector.to_prometheus()
    
    # Vérifier les éléments essentiels
    assert "# HELP" in prometheus_output
    assert "# TYPE" in prometheus_output
    assert "api_uptime_seconds" in prometheus_output
    assert "api_requests_total" in prometheus_output


