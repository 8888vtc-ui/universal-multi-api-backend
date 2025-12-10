"""
Countries API Router
REST Countries - Free unlimited country information
"""
from fastapi import APIRouter, HTTPException, Query
from services.external_apis.countries.provider import RestCountriesProvider
from typing import List, Optional

router = APIRouter(prefix="/api/countries", tags=["countries"])

provider = RestCountriesProvider()


@router.get("/all")
async def get_all_countries():
    """Get all countries information"""
    try:
        countries = await provider.get_all_countries()
        return {
            "success": True,
            "count": len(countries),
            "countries": countries
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/search")
async def search_countries(
    query: str = Query(None, description="Country name to search"),
    q: str = Query(None, description="Alias for query")
):
    """Search countries by name"""
    search_term = query or q
    if not search_term:
        raise HTTPException(status_code=400, detail="Query parameter 'q' or 'query' is required")
    try:
        countries = await provider.search_countries(search_term)
        return {
            "success": True,
            "count": len(countries),
            "countries": countries
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/name/{name}")
async def get_country_by_name(name: str):
    """Get country by name"""
    try:
        country = await provider.get_country_by_name(name)
        if country:
            return {"success": True, "country": country}
        else:
            raise HTTPException(status_code=404, detail="Country not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/code/{code}")
async def get_country_by_code(code: str):
    """Get country by alpha code (2 or 3 letters, e.g., FR, USA)"""
    try:
        country = await provider.get_country_by_code(code.upper())
        if country:
            return {"success": True, "country": country}
        else:
            raise HTTPException(status_code=404, detail="Country not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/region/{region}")
async def get_countries_by_region(region: str):
    """Get countries by region (e.g., Europe, Asia, Africa)"""
    try:
        countries = await provider.get_countries_by_region(region)
        return {
            "success": True,
            "count": len(countries),
            "region": region,
            "countries": countries
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/currency/{currency}")
async def get_countries_by_currency(currency: str):
    """Get countries by currency code (e.g., EUR, USD)"""
    try:
        countries = await provider.get_countries_by_currency(currency.upper())
        return {
            "success": True,
            "count": len(countries),
            "currency": currency.upper(),
            "countries": countries
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))






