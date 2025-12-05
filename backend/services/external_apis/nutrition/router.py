"""
Nutrition Router
"""
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)


class NutritionRouter:
    """Router for nutrition APIs"""
    
    def __init__(self):
        self.providers = []
        self._init_providers()
    
    def _init_providers(self):
        """Initialize nutrition providers"""
        from .providers import Spoonacular, Edamam, USDAFoodData
        import os
        
        # Spoonacular
        if os.getenv('SPOONACULAR_API_KEY'):
            try:
                self.providers.append({
                    'name': 'spoonacular',
                    'instance': Spoonacular(),
                    'type': 'recipes'
                })
                logger.info("✅ Spoonacular initialized")
            except Exception as e:
                logger.warning(f"⚠️ Spoonacular failed: {e}")
        
        # Edamam
        if os.getenv('EDAMAM_APP_ID') and os.getenv('EDAMAM_APP_KEY'):
            try:
                self.providers.append({
                    'name': 'edamam',
                    'instance': Edamam(),
                    'type': 'recipes'
                })
                logger.info("✅ Edamam initialized")
            except Exception as e:
                logger.warning(f"⚠️ Edamam failed: {e}")
        
        # USDA (always available with DEMO_KEY)
        try:
            self.providers.append({
                'name': 'usda',
                'instance': USDAFoodData(),
                'type': 'foods'
            })
            logger.info("✅ USDA FoodData initialized")
        except Exception as e:
            logger.warning(f"⚠️ USDA failed: {e}")
    
    async def search_recipes(self, query: str, number: int = 10) -> Dict[str, Any]:
        """Search recipes with fallback"""
        errors = []
        
        recipe_providers = [p for p in self.providers if p['type'] == 'recipes']
        
        for provider in recipe_providers:
            name = provider['name']
            instance = provider['instance']
            
            try:
                logger.info(f"🔄 Searching recipes with {name}...")
                result = await instance.search_recipes(query, number)
                
                logger.info(f"✅ Recipes found with {name}")
                return {
                    **result,
                    "provider": name
                }
            
            except Exception as e:
                logger.warning(f"⚠️ {name} failed: {str(e)}")
                errors.append(f"{name}: {str(e)}")
                continue
        
        error_msg = f"All recipe providers failed. Errors: {'; '.join(errors)}"
        logger.error(f"❌ {error_msg}")
        raise Exception(error_msg)
    
    async def search_foods(self, query: str, page_size: int = 10) -> Dict[str, Any]:
        """Search foods (USDA)"""
        usda = next((p for p in self.providers if p['name'] == 'usda'), None)
        
        if not usda:
            raise Exception("USDA provider not available")
        
        try:
            result = await usda['instance'].search_foods(query, page_size)
            return {
                **result,
                "provider": "usda"
            }
        except Exception as e:
            logger.error(f"❌ USDA search failed: {e}")
            raise
    
    def get_status(self) -> Dict[str, Any]:
        """Get router status"""
        return {
            "providers": len(self.providers),
            "details": [
                {"name": p['name'], "type": p['type'], "available": True}
                for p in self.providers
            ]
        }
