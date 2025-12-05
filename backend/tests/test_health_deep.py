"""
Tests pour les health checks approfondis
"""
import pytest
from fastapi.testclient import TestClient
from routers.health_deep import router, check_redis, check_database, check_ai_providers


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


def test_health_deep_endpoint(client):
    """Tester l'endpoint /api/health/deep"""
    response = client.get("/api/health/deep")
    
    assert response.status_code == 200
    data = response.json()
    
    # Vérifier la structure de la réponse
    assert "status" in data
    assert "timestamp" in data
    assert "duration_ms" in data
    assert "checks" in data
    
    # Status doit être healthy, degraded ou unhealthy
    assert data["status"] in ["healthy", "degraded", "unhealthy"]


def test_health_ready_endpoint(client):
    """Tester l'endpoint /api/health/ready"""
    response = client.get("/api/health/ready")
    
    # Peut être 200 ou 503 selon la configuration
    assert response.status_code in [200, 503]
    
    if response.status_code == 200:
        data = response.json()
        assert "status" in data
        assert data["status"] == "ready"


def test_health_live_endpoint(client):
    """Tester l'endpoint /api/health/live"""
    response = client.get("/api/health/live")
    
    assert response.status_code == 200
    data = response.json()
    
    assert "status" in data
    assert data["status"] == "alive"
    assert "timestamp" in data


@pytest.mark.asyncio
async def test_check_redis():
    """Tester la fonction check_redis"""
    result = await check_redis()
    
    assert "status" in result
    assert "type" in result
    assert result["type"] == "redis"
    assert result["status"] in ["healthy", "unavailable", "error"]


@pytest.mark.asyncio
async def test_check_database():
    """Tester la fonction check_database"""
    result = await check_database()
    
    assert "status" in result
    assert "type" in result
    assert result["type"] == "sqlite"
    assert result["status"] in ["healthy", "error"]


@pytest.mark.asyncio
async def test_check_ai_providers():
    """Tester la fonction check_ai_providers"""
    result = await check_ai_providers()
    
    assert "status" in result
    assert result["status"] in ["healthy", "degraded", "error"]
    
    if "available_count" in result:
        assert isinstance(result["available_count"], int)


