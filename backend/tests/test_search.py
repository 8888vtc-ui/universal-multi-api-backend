"""
Tests unitaires pour le moteur de recherche universel
"""
import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from typing import Dict, Any

# Import du module à tester
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from routers.search import (
    detect_search_intent,
    SearchRequest,
    SearchResult,
    SearchResponse
)


class TestDetectSearchIntent:
    """Tests pour la détection d'intention de recherche"""
    
    def test_detect_finance_intent(self):
        """Test détection intention finance"""
        queries = [
            "bitcoin prix",
            "cours BTC",
            "action Apple",
            "trading crypto",
            "investissement bourse"
        ]
        for query in queries:
            intents = detect_search_intent(query)
            assert intents["finance"] == True, f"Should detect finance intent for: {query}"
    
    def test_detect_news_intent(self):
        """Test détection intention news"""
        queries = [
            "actualité France",
            "breaking news",
            "nouvelle technologie",
            "événement important"
        ]
        for query in queries:
            intents = detect_search_intent(query)
            assert intents["news"] == True, f"Should detect news intent for: {query}"
    
    def test_detect_weather_intent(self):
        """Test détection intention météo"""
        queries = [
            "météo Paris",
            "weather forecast",
            "température aujourd'hui",
            "prévision pluie"
        ]
        for query in queries:
            intents = detect_search_intent(query)
            assert intents["weather"] == True, f"Should detect weather intent for: {query}"
    
    def test_detect_medical_intent(self):
        """Test détection intention médical"""
        queries = [
            "recherche médicale",
            "médicament paracétamol",
            "symptôme grippe",
            "traitement cancer"
        ]
        for query in queries:
            intents = detect_search_intent(query)
            assert intents["medical"] == True, f"Should detect medical intent for: {query}"
    
    def test_detect_multiple_intents(self):
        """Test détection de plusieurs intentions"""
        query = "actualité bitcoin prix"
        intents = detect_search_intent(query)
        assert intents["finance"] == True
        assert intents["news"] == True
    
    def test_no_intent_detected(self):
        """Test quand aucune intention n'est détectée"""
        query = "bonjour comment allez-vous"
        intents = detect_search_intent(query)
        # Toutes les intentions devraient être False
        assert all(not intent for intent in intents.values())


class TestSearchRequest:
    """Tests pour le modèle SearchRequest"""
    
    def test_search_request_creation(self):
        """Test création SearchRequest valide"""
        request = SearchRequest(
            query="bitcoin prix",
            categories=["finance"],
            max_results_per_category=5,
            language="fr"
        )
        assert request.query == "bitcoin prix"
        assert request.categories == ["finance"]
        assert request.max_results_per_category == 5
        assert request.language == "fr"
    
    def test_search_request_defaults(self):
        """Test valeurs par défaut"""
        request = SearchRequest(query="test")
        assert request.categories is None
        assert request.max_results_per_category == 5
        assert request.language == "fr"


class TestSearchResult:
    """Tests pour le modèle SearchResult"""
    
    def test_search_result_creation(self):
        """Test création SearchResult"""
        result = SearchResult(
            category="finance",
            title="Bitcoin Price",
            content={"price": 50000},
            source="CoinGecko",
            relevance_score=0.9,
            url="https://example.com"
        )
        assert result.category == "finance"
        assert result.title == "Bitcoin Price"
        assert result.relevance_score == 0.9
        assert result.url == "https://example.com"
    
    def test_search_result_without_url(self):
        """Test SearchResult sans URL"""
        result = SearchResult(
            category="news",
            title="Article Title",
            content={"text": "content"},
            source="NewsAPI",
            relevance_score=0.8
        )
        assert result.url is None


class TestSearchFunctions:
    """Tests pour les fonctions de recherche individuelles"""
    
    @pytest.mark.asyncio
    async def test_search_finance_crypto(self):
        """Test recherche finance crypto"""
        from routers.search import search_finance
        
        # Mock des APIs finance
        with patch('routers.search.coingecko') as mock_coingecko:
            mock_coingecko.get_crypto_price = AsyncMock(return_value={
                "bitcoin": {"usd": 50000}
            })
            
            results = await search_finance("bitcoin prix", max_results=5)
            assert isinstance(results, list)
            # Si bitcoin est détecté, on devrait avoir des résultats
            if results:
                assert all(isinstance(r, SearchResult) for r in results)
    
    @pytest.mark.asyncio
    async def test_search_finance_stock(self):
        """Test recherche finance stock"""
        from routers.search import search_finance
        
        # Mock des APIs finance
        with patch('routers.search.yahoo_finance') as mock_yahoo:
            mock_yahoo.get_stock_info = AsyncMock(return_value={
                "symbol": "AAPL",
                "price": 150
            })
            
            results = await search_finance("AAPL stock", max_results=5)
            assert isinstance(results, list)
    
    @pytest.mark.asyncio
    async def test_search_news(self):
        """Test recherche news"""
        from routers.search import search_news
        
        # Mock de l'API news
        with patch('routers.search.news_router') as mock_news:
            mock_news.search = AsyncMock(return_value={
                "articles": [
                    {
                        "title": "Test Article",
                        "description": "Test description",
                        "publishedAt": "2024-01-01",
                        "source": {"name": "Test Source"},
                        "url": "https://example.com"
                    }
                ]
            })
            
            results = await search_news("test query", "fr", max_results=5)
            assert isinstance(results, list)
            if results:
                assert all(isinstance(r, SearchResult) for r in results)
                assert all(r.category == "news" for r in results)
    
    @pytest.mark.asyncio
    async def test_search_weather(self):
        """Test recherche météo"""
        from routers.search import search_weather
        
        # Mock géocoding et weather
        with patch('routers.search.geocoding_router') as mock_geo, \
             patch('routers.search.weather_router') as mock_weather:
            
            mock_geo.geocode = AsyncMock(return_value={
                "results": [{
                    "name": "Paris",
                    "latitude": 48.8566,
                    "longitude": 2.3522
                }]
            })
            
            mock_weather.get_current_weather = AsyncMock(return_value={
                "temperature": 15,
                "provider": "Open-Meteo"
            })
            
            results = await search_weather("météo Paris", max_results=5)
            assert isinstance(results, list)
            if results:
                assert all(isinstance(r, SearchResult) for r in results)
                assert all(r.category == "weather" for r in results)
    
    @pytest.mark.asyncio
    async def test_search_error_handling(self):
        """Test gestion d'erreurs"""
        from routers.search import search_finance
        
        # Mock pour simuler une erreur API
        with patch('routers.search.coingecko') as mock_coingecko:
            mock_coingecko.get_crypto_price = AsyncMock(side_effect=Exception("API Error"))
            
            # Ne devrait pas crasher, mais retourner liste vide
            results = await search_finance("bitcoin", max_results=5)
            assert isinstance(results, list)
            # Peut être vide en cas d'erreur


class TestSearchPerformance:
    """Tests de performance"""
    
    @pytest.mark.asyncio
    async def test_parallel_search_performance(self):
        """Test que les recherches parallèles sont rapides"""
        import time
        from routers.search import universal_search
        
        request = SearchRequest(
            query="bitcoin actualité",
            categories=["finance", "news"],
            max_results_per_category=3
        )
        
        # Mock toutes les APIs pour éviter les vrais appels
        with patch('routers.search.search_finance') as mock_finance, \
             patch('routers.search.search_news') as mock_news:
            
            mock_finance.return_value = []
            mock_news.return_value = []
            
            start_time = time.time()
            result = await universal_search(request)
            elapsed = time.time() - start_time
            
            # Devrait être rapide même avec mocks (pas de vraies APIs)
            assert elapsed < 1.0, f"Search took {elapsed}s, should be < 1s"


class TestSearchEdgeCases:
    """Tests pour cas limites"""
    
    def test_empty_query(self):
        """Test avec requête vide"""
        intents = detect_search_intent("")
        # Devrait retourner toutes les intentions à False
        assert all(not intent for intent in intents.values())
    
    def test_very_long_query(self):
        """Test avec requête très longue"""
        long_query = "bitcoin " * 100
        intents = detect_search_intent(long_query)
        # Devrait toujours détecter finance
        assert intents["finance"] == True
    
    def test_special_characters(self):
        """Test avec caractères spéciaux"""
        query = "bitcoin @#$% prix !!!"
        intents = detect_search_intent(query)
        assert intents["finance"] == True
    
    @pytest.mark.asyncio
    async def test_no_categories_specified(self):
        """Test sans catégories spécifiées"""
        from routers.search import universal_search
        
        request = SearchRequest(
            query="test query",
            categories=None,  # Auto-détection
            max_results_per_category=2
        )
        
        # Devrait utiliser auto-détection
        # Mock pour éviter vrais appels
        with patch('routers.search.search_finance') as mock_finance, \
             patch('routers.search.search_news') as mock_news:
            
            mock_finance.return_value = []
            mock_news.return_value = []
            
            result = await universal_search(request)
            assert isinstance(result, SearchResponse)
            assert result.query == "test query"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])


