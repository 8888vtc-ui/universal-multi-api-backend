"""Exchange Rate Router"""
from fastapi import APIRouter, HTTPException, Query
from services.external_apis.exchange.provider import ExchangeRateProvider
from typing import Dict, Any, List

router = APIRouter(prefix="/api/exchange", tags=["exchange"])

exchange_provider = ExchangeRateProvider()


@router.get("/rates/{base}", response_model=Dict[str, Any])
async def get_exchange_rates(base: str = "USD"):
    """Get exchange rates for a base currency"""
    try:
        return await exchange_provider.get_rates(base.upper())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/convert", response_model=Dict[str, Any])
async def convert_currency(
    amount: float = Query(..., description="Amount to convert"),
    from_currency: str = Query("USD", description="Source currency"),
    to_currency: str = Query("EUR", description="Target currency")
):
    """Convert amount between currencies"""
    try:
        return await exchange_provider.convert(
            amount,
            from_currency.upper(),
            to_currency.upper()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/currencies", response_model=List[str])
async def get_currencies():
    """Get list of supported currencies"""
    try:
        return await exchange_provider.get_supported_currencies()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))






