"""
Nutrition Providers
Spoonacular, Edamam, USDA FoodData
"""
import os
import httpx
from typing import Dict, Any, Optional, List
from services.http_client import http_client


class Spoonacular:
    """Spoonacular - 3,000 req/month, 365k recipes"""
    
    def __init__(self):
        self.api_key = os.getenv('SPOONACULAR_API_KEY')
        if not self.api_key:
            raise ValueError("SPOONACULAR_API_KEY not found")
        
        self.base_url = "https://api.spoonacular.com"
        self.available = True
    
    async def search_recipes(
        self,
        query: str,
        number: int = 10
    ) -> Dict[str, Any]:
        """Search recipes"""
        url = f"{self.base_url}/recipes/complexSearch"
        params = {
            'apiKey': self.api_key,
            'query': query,
            'number': number
        }
        
        response = await http_client.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        return {
            'recipes': data.get('results', []),
            'total': data.get('totalResults', 0)
        }
    
    async def get_recipe_info(self, recipe_id: int) -> Dict[str, Any]:
        """Get detailed recipe information"""
        url = f"{self.base_url}/recipes/{recipe_id}/information"
        params = {'apiKey': self.api_key}
        
        response = await http_client.get(url, params=params)
        response.raise_for_status()
        
        return response.json()
    
    async def analyze_nutrition(self, text: str) -> Dict[str, Any]:
        """Analyze nutrition from text"""
        url = f"{self.base_url}/recipes/analyzeInstructions"
        params = {'apiKey': self.api_key}
        data = {'text': text}
        
        response = await http_client.post(url, params=params, data=data)
        response.raise_for_status()
        
        return response.json()


class Edamam:
    """Edamam - 2.3M recipes, free tier"""
    
    def __init__(self):
        self.app_id = os.getenv('EDAMAM_APP_ID')
        self.app_key = os.getenv('EDAMAM_APP_KEY')
        
        if not self.app_id or not self.app_key:
            raise ValueError("EDAMAM_APP_ID and EDAMAM_APP_KEY required")
        
        self.base_url = "https://api.edamam.com"
        self.available = True
    
    async def search_recipes(
        self,
        query: str,
        number: int = 10
    ) -> Dict[str, Any]:
        """Search recipes"""
        url = f"{self.base_url}/api/recipes/v2"
        params = {
            'type': 'public',
            'app_id': self.app_id,
            'app_key': self.app_key,
            'q': query,
            'to': number
        }
        
        response = await http_client.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        return {
            'recipes': data.get('hits', []),
            'total': data.get('count', 0)
        }
    
    async def analyze_nutrition(self, ingredients: List[str]) -> Dict[str, Any]:
        """Analyze nutrition from ingredients"""
        url = f"{self.base_url}/api/nutrition-details"
        params = {
            'app_id': self.app_id,
            'app_key': self.app_key
        }
        data = {
            'title': 'Recipe',
            'ingr': ingredients
        }
        
        response = await http_client.post(url, params=params, json=data)
        response.raise_for_status()
        
        return response.json()


class USDAFoodData:
    """USDA FoodData Central - 1,000 req/hour, free"""
    
    def __init__(self):
        self.api_key = os.getenv('USDA_API_KEY', 'DEMO_KEY')
        self.base_url = "https://api.nal.usda.gov/fdc/v1"
        self.available = True
    
    async def search_foods(
        self,
        query: str,
        page_size: int = 10
    ) -> Dict[str, Any]:
        """Search food database"""
        url = f"{self.base_url}/foods/search"
        params = {
            'api_key': self.api_key,
            'query': query,
            'pageSize': page_size
        }
        
        response = await http_client.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        return {
            'foods': data.get('foods', []),
            'total': data.get('totalHits', 0)
        }
    
    async def get_food_details(self, fdc_id: int) -> Dict[str, Any]:
        """Get detailed food information"""
        url = f"{self.base_url}/food/{fdc_id}"
        params = {'api_key': self.api_key}
        
        response = await http_client.get(url, params=params)
        response.raise_for_status()
        
        return response.json()
