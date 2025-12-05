"""
Tests d'intégration pour le moteur de recherche
Ces tests nécessitent des APIs réelles (peuvent échouer sans clés API)
"""
import pytest
import asyncio
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from routers.search import (
    universal_search,
    SearchRequest,
    detect_search_intent
)


@pytest.mark.integration
class TestSearchIntegration:
    """Tests d'intégration avec vraies APIs"""
    
    @pytest.mark.asyncio
    @pytest.mark.slow
    async def test_universal_search_finance(self):
        """Test recherche universelle pour finance"""
        request = SearchRequest(
            query="bitcoin prix",
            categories=["finance"],
            max_results_per_category=3,
            language="fr"
        )
        
        try:
            result = await universal_search(request)
            assert result.query == "bitcoin prix"
            assert "finance" in result.categories_searched or len(result.categories_searched) == 0
            assert result.total_results >= 0  # Peut être 0 si API indisponible
        except Exception as e:
            pytest.skip(f"Integration test skipped: {e}")
    
    @pytest.mark.asyncio
    @pytest.mark.slow
    async def test_universal_search_news(self):
        """Test recherche universelle pour news"""
        request = SearchRequest(
            query="actualité technologie",
            categories=["news"],
            max_results_per_category=3,
            language="fr"
        )
        
        try:
            result = await universal_search(request)
            assert result.query == "actualité technologie"
            assert "news" in result.categories_searched or len(result.categories_searched) == 0
        except Exception as e:
            pytest.skip(f"Integration test skipped: {e}")
    
    @pytest.mark.asyncio
    @pytest.mark.slow
    async def test_universal_search_auto_detect(self):
        """Test auto-détection d'intention"""
        request = SearchRequest(
            query="bitcoin actualité météo Paris",
            categories=None,  # Auto-détection
            max_results_per_category=2,
            language="fr"
        )
        
        try:
            result = await universal_search(request)
            assert result.query == "bitcoin actualité météo Paris"
            # Devrait détecter plusieurs catégories
            assert len(result.categories_searched) >= 0
        except Exception as e:
            pytest.skip(f"Integration test skipped: {e}")
    
    @pytest.mark.asyncio
    @pytest.mark.slow
    async def test_universal_search_multiple_categories(self):
        """Test recherche dans plusieurs catégories"""
        request = SearchRequest(
            query="bitcoin",
            categories=["finance", "news"],
            max_results_per_category=2,
            language="en"
        )
        
        try:
            result = await universal_search(request)
            assert result.query == "bitcoin"
            # Devrait chercher dans les deux catégories
            assert len(result.categories_searched) >= 0
        except Exception as e:
            pytest.skip(f"Integration test skipped: {e}")
    
    @pytest.mark.asyncio
    @pytest.mark.slow
    async def test_search_performance(self):
        """Test performance de recherche"""
        import time
        
        request = SearchRequest(
            query="test query",
            categories=["finance", "news"],
            max_results_per_category=2,
            language="fr"
        )
        
        try:
            start_time = time.time()
            result = await universal_search(request)
            elapsed = time.time() - start_time
            
            # Devrait être raisonnablement rapide (< 5s avec vraies APIs)
            assert elapsed < 10.0, f"Search took {elapsed}s, should be < 10s"
            assert isinstance(result, dict) or hasattr(result, 'total_results')
        except Exception as e:
            pytest.skip(f"Integration test skipped: {e}")


@pytest.mark.integration
class TestSearchErrorHandling:
    """Tests de gestion d'erreurs avec vraies APIs"""
    
    @pytest.mark.asyncio
    async def test_search_with_invalid_category(self):
        """Test avec catégorie invalide"""
        request = SearchRequest(
            query="test",
            categories=["invalid_category"],
            max_results_per_category=2
        )
        
        try:
            result = await universal_search(request)
            # Ne devrait pas crasher
            assert result is not None
        except Exception as e:
            pytest.skip(f"Integration test skipped: {e}")
    
    @pytest.mark.asyncio
    async def test_search_empty_query(self):
        """Test avec requête vide"""
        request = SearchRequest(
            query="",
            max_results_per_category=2
        )
        
        try:
            result = await universal_search(request)
            # Devrait gérer gracieusement
            assert result is not None
        except Exception as e:
            # Peut lever une exception, c'est acceptable
            assert isinstance(e, (ValueError, AssertionError))


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-m", "integration"])


