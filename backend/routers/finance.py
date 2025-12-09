"""
Finance API Router
Endpoints for crypto, stocks, and market data
"""
from fastapi import APIRouter, HTTPException
from typing import Optional
from services.external_apis import coingecko, alphavantage, yahoo_finance

router = APIRouter(prefix="/api/finance", tags=["finance"])


@router.get("/crypto/price/{coin_id}")
async def get_crypto_price(coin_id: str, vs_currency: str = "usd"):
    """Get cryptocurrency price from CoinGecko"""
    # Sanitize input
    from services.sanitizer import sanitize
    coin_id = sanitize(coin_id.lower(), max_length=50)
    vs_currency = sanitize(vs_currency.lower(), max_length=10)
    
    # Vérifier qu'au moins un provider est disponible
    if not coingecko.available and not alphavantage.available and not yahoo_finance.available:
        raise HTTPException(
            status_code=503,
            detail="Finance service unavailable. No providers configured."
        )
    
    try:
        data = await coingecko.get_crypto_price(coin_id, vs_currency)
        return {"success": True, "data": data, "source": "coingecko"}
    except HTTPException:
        raise
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Crypto price fetch failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Finance service temporarily unavailable. Please try again later."
        )


@router.get("/crypto/trending")
async def get_trending_crypto():
    """Get trending cryptocurrencies"""
    try:
        data = await coingecko.get_trending()
        return {"success": True, "data": data, "source": "coingecko"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stock/quote/{symbol}")
async def get_stock_quote(symbol: str):
    """Get stock quote (tries Alpha Vantage first, falls back to Yahoo Finance)"""
    # Sanitize input
    from services.sanitizer import sanitize
    symbol = sanitize(symbol.upper(), max_length=10)
    
    # Vérifier qu'au moins un provider est disponible
    if not alphavantage.available and not yahoo_finance.available:
        raise HTTPException(
            status_code=503,
            detail="Finance service unavailable. No providers configured."
        )
    
    # Try Alpha Vantage first
    if alphavantage.available:
        try:
            data = await alphavantage.get_stock_quote(symbol)
            return {"success": True, "data": data, "source": "alphavantage"}
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f"Alpha Vantage failed: {e}, trying Yahoo Finance...")
    
    # Fallback to Yahoo Finance
    try:
        data = await yahoo_finance.get_stock_info(symbol)
        return {"success": True, "data": data, "source": "yahoo_finance"}
    except HTTPException:
        raise
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Stock quote fetch failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Finance service temporarily unavailable. Please try again later."
        )


@router.get("/market/summary")
async def get_market_summary():
    """Get market summary (major indices)"""
# Try Yahoo Finance first (most reliable)
    if yahoo_finance and yahoo_finance.available:
        try:
            data = await yahoo_finance.get_market_summary()
            if data and isinstance(data, dict) and len(data) > 0:
                # Update fallback cache with real data
                if finance_fallback:
                    finance_fallback.update_from_external("market", "summary", data)
                return {"success": True, "data": data, "source": "yahoo_finance"}
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f"Yahoo Finance market summary failed: {e}", exc_info=True)
    
    # Try fallback provider
    if finance_fallback and finance_fallback.available:
        try:
            import logging
            logger = logging.getLogger(__name__)
            logger.info("Using fallback for market summary")
            
            data = await finance_fallback.get_market_summary()
            if data and isinstance(data, dict) and len(data) > 0:
                return {
                    "success": True,
                    "data": data,
                    "source": "fallback",
                    "note": "Using cached/static data - external APIs unavailable"
                }
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f"Fallback market summary failed: {e}")
    
    # Return a helpful response instead of raising an error
    return {
        "success": False,
        "error": "Market summary temporarily unavailable",
        "detail": "Unable to fetch market data at this time. Please try again later.",
        "data": {}  # Empty data instead of error
    }


@router.get("/stock/company/{symbol}")
async def get_company_info(symbol: str):
    """Get company profile information"""
    from services.sanitizer import sanitize
    symbol = sanitize(symbol.upper(), max_length=10)
    
    if finnhub and finnhub.available:
        try:
            data = await finnhub.get_company_profile(symbol)
            return {"success": True, "data": data, "source": "finnhub"}
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f"Finnhub company info failed: {e}")
    
    raise HTTPException(
        status_code=503,
        detail="Company info service temporarily unavailable."
    )


@router.get("/stock/news/{symbol}")
async def get_stock_news(symbol: str, limit: int = 10):
    """Get news for a specific stock"""
    from services.sanitizer import sanitize
    symbol = sanitize(symbol.upper(), max_length=10)
    
    if finnhub and finnhub.available:
        try:
            data = await finnhub.get_company_news(symbol, limit=limit)
            return {"success": True, "data": data, "source": "finnhub"}
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f"Finnhub news failed: {e}")
    
    raise HTTPException(
        status_code=503,
        detail="Stock news service temporarily unavailable."
    )


@router.get("/market/news")
async def get_market_news(category: str = "general", limit: int = 10):
    """Get general market news"""
    if finnhub and finnhub.available:
        try:
            data = await finnhub.get_market_news(category=category, limit=limit)
            return {"success": True, "data": data, "source": "finnhub"}
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f"Finnhub market news failed: {e}")
    
    raise HTTPException(
        status_code=503,
        detail="Market news service temporarily unavailable."
    )


@router.get("/crypto/trending")
async def get_trending_crypto():
    """Get trending cryptocurrencies"""
    try:
        data = await coingecko.get_trending()
        return {"success": True, "data": data, "source": "coingecko"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stock/quote/{symbol}")
async def get_stock_quote(symbol: str):
    """Get stock quote (tries multiple providers with fallback)"""
    # Sanitize input
    from services.sanitizer import sanitize
    symbol = sanitize(symbol.upper(), max_length=10)
    
    # Vérifier qu'au moins un provider est disponible (incluant fallback)
    available_providers = [
        alphavantage.available if alphavantage else False,
        yahoo_finance.available if yahoo_finance else False,
        finnhub.available if finnhub else False,
        twelve_data.available if twelve_data else False,
        polygon.available if polygon else False,
        finance_fallback.available if finance_fallback else False  # Fallback toujours disponible
    ]
    
    if not any(available_providers):
        raise HTTPException(
            status_code=503,
            detail="Finance service unavailable. No providers configured."
        )
    
    # Try providers in order of preference (with fallback)
    providers = [
        ("alphavantage", alphavantage, lambda p: p.get_stock_quote(symbol) if alphavantage and alphavantage.available else None),
        ("finnhub", finnhub, lambda p: p.get_stock_quote(symbol) if finnhub and finnhub.available else None),
        ("polygon", polygon, lambda p: p.get_stock_quote(symbol) if polygon and polygon.available else None),
        ("twelve_data", twelve_data, lambda p: p.get_stock_quote(symbol) if twelve_data and twelve_data.available else None),
        ("yahoo_finance", yahoo_finance, lambda p: p.get_stock_info(symbol) if yahoo_finance and yahoo_finance.available else None),
    ]
    
    last_error = None
    errors = []
    for provider_name, provider, fetch_func in providers:
        if not provider or not provider.available:
            continue
        
        try:
            data = await fetch_func(provider)
            if data and (isinstance(data, dict) and len(data) > 0):
                # Update fallback cache with real data when successful
                if finance_fallback and provider_name != "fallback":
                    try:
                        finance_fallback.update_from_external("stock", symbol, data)
                    except:
                        pass  # Don't fail if cache update fails
                
                return {"success": True, "data": data, "source": provider_name}
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            error_msg = str(e)[:200]
            logger.warning(f"{provider_name} failed: {error_msg}, trying next provider...")
            errors.append(f"{provider_name}: {error_msg}")
            last_error = e
            continue
    
    # All providers failed - try fallback provider
    if finance_fallback and finance_fallback.available:
        try:
            import logging
            logger = logging.getLogger(__name__)
            logger.info(f"All external providers failed, using fallback for {symbol}")
            
            data = await finance_fallback.get_stock_info(symbol)
            if data:
                return {
                    "success": True,
                    "data": data,
                    "source": "fallback",
                    "note": "Using cached/static data - external APIs unavailable"
                }
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f"Fallback provider also failed: {e}")
    
    # All providers including fallback failed
    import logging
    logger = logging.getLogger(__name__)
    logger.error(f"All stock quote providers failed. Errors: {errors}", exc_info=True)
    
    # Return a structured error response instead of raising
    return {
        "success": False,
        "error": "Finance service temporarily unavailable",
        "detail": "All providers failed. Please try again later.",
        "errors": errors[:3]  # Limit to 3 errors
    }


@router.get("/market/summary")
async def get_market_summary():
    """Get market summary (major indices)"""
    # Try Yahoo Finance first (most reliable)
    if yahoo_finance and yahoo_finance.available:
        try:
            data = await yahoo_finance.get_market_summary()
            if data and isinstance(data, dict) and len(data) > 0:
                # Update fallback cache with real data
                if finance_fallback:
                    finance_fallback.update_from_external("market", "summary", data)
                return {"success": True, "data": data, "source": "yahoo_finance"}
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f"Yahoo Finance market summary failed: {e}", exc_info=True)
    
    # Try fallback provider
    if finance_fallback and finance_fallback.available:
        try:
            import logging
            logger = logging.getLogger(__name__)
            logger.info("Using fallback for market summary")
            
            data = await finance_fallback.get_market_summary()
            if data and isinstance(data, dict) and len(data) > 0:
                return {
                    "success": True,
                    "data": data,
                    "source": "fallback",
                    "note": "Using cached/static data - external APIs unavailable"
                }
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f"Fallback market summary failed: {e}")
    
    # Return a helpful response instead of raising an error
    return {
        "success": False,
        "error": "Market summary temporarily unavailable",
        "detail": "Unable to fetch market data at this time. Please try again later.",
        "data": {}  # Empty data instead of error
    }


@router.get("/stock/company/{symbol}")
async def get_company_info(symbol: str):
    """Get company profile information"""
    from services.sanitizer import sanitize
    symbol = sanitize(symbol.upper(), max_length=10)
    
    if finnhub and finnhub.available:
        try:
            data = await finnhub.get_company_profile(symbol)
            return {"success": True, "data": data, "source": "finnhub"}
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f"Finnhub company info failed: {e}")
    
    raise HTTPException(
        status_code=503,
        detail="Company info service temporarily unavailable."
    )


@router.get("/stock/news/{symbol}")
async def get_stock_news(symbol: str, limit: int = 10):
    """Get news for a specific stock"""
    from services.sanitizer import sanitize
    symbol = sanitize(symbol.upper(), max_length=10)
    
    if finnhub and finnhub.available:
        try:
            data = await finnhub.get_company_news(symbol, limit=limit)
            return {"success": True, "data": data, "source": "finnhub"}
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f"Finnhub news failed: {e}")
    
    raise HTTPException(
        status_code=503,
        detail="Stock news service temporarily unavailable."
    )


@router.get("/market/news")
async def get_market_news(category: str = "general", limit: int = 10):
    """Get general market news"""
    if finnhub and finnhub.available:
        try:
            data = await finnhub.get_market_news(category=category, limit=limit)
            return {"success": True, "data": data, "source": "finnhub"}
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f"Finnhub market news failed: {e}")
    
    raise HTTPException(
        status_code=503,
        detail="Market news service temporarily unavailable."
    )
