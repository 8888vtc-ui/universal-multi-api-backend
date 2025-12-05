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
    try:
        data = await yahoo_finance.get_market_summary()
        return {"success": True, "data": data, "source": "yahoo_finance"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
