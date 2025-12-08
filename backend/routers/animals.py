"""Animals Router - Dog and Cat images"""
from fastapi import APIRouter, HTTPException, Query
from services.external_apis.dogs.provider import DogAPIProvider, CatAPIProvider
from typing import Dict, Any, List

router = APIRouter(prefix="/api/animals", tags=["animals"])

dog_provider = DogAPIProvider()
cat_provider = CatAPIProvider()


# === Dogs ===

@router.get("/dogs/random", response_model=Dict[str, Any])
async def get_random_dog():
    """Get a random dog image"""
    try:
        return await dog_provider.get_random_image()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/dogs/random/{count}", response_model=Dict[str, Any])
async def get_random_dogs(count: int):
    """Get multiple random dog images"""
    try:
        return await dog_provider.get_random_images(min(count, 50))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/dogs/breeds", response_model=List[str])
async def get_dog_breeds():
    """Get all dog breeds"""
    try:
        return await dog_provider.get_breeds()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/dogs/breed/{breed}", response_model=Dict[str, Any])
async def get_breed_images(
    breed: str,
    count: int = Query(5, ge=1, le=50)
):
    """Get images of a specific dog breed"""
    try:
        return await dog_provider.get_breed_images(breed, count)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# === Cats ===

@router.get("/cats/random", response_model=Dict[str, Any])
async def get_random_cat():
    """Get a random cat image"""
    try:
        return await cat_provider.get_random_image()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/cats/random/{count}", response_model=Dict[str, Any])
async def get_random_cats(count: int):
    """Get multiple random cat images"""
    try:
        return await cat_provider.get_random_images(min(count, 50))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))






