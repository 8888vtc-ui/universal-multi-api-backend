"""FakeStore Router - Free fake e-commerce API"""
from fastapi import APIRouter, HTTPException, Query
from services.external_apis.fakestore.provider import FakeStoreProvider
from typing import List, Dict, Any, Optional

router = APIRouter(prefix="/api/fakestore", tags=["fakestore"])

provider = FakeStoreProvider()

@router.get("/products", response_model=List[Dict[str, Any]])
async def get_products(
    limit: Optional[int] = Query(None, ge=1, le=100),
    sort: Optional[str] = Query(None, description="Sort order (asc, desc)")
):
    """Get all products"""
    try:
        return await provider.get_products(limit, sort)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/products/{product_id}", response_model=Dict[str, Any])
async def get_product(product_id: int):
    """Get a specific product by ID"""
    try:
        return await provider.get_product(product_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/categories", response_model=List[str])
async def get_categories():
    """Get all product categories"""
    try:
        return await provider.get_categories()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/category/{category}", response_model=List[Dict[str, Any]])
async def get_products_by_category(category: str):
    """Get products by category"""
    try:
        return await provider.get_products_by_category(category)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/users", response_model=List[Dict[str, Any]])
async def get_users(limit: Optional[int] = Query(None, ge=1, le=100)):
    """Get all users"""
    try:
        return await provider.get_users(limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/carts", response_model=List[Dict[str, Any]])
async def get_carts(limit: Optional[int] = Query(None, ge=1, le=100)):
    """Get all carts"""
    try:
        return await provider.get_carts(limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))






