"""
🧪 TESTER AGENT
Uses GPT-4o for comprehensive testing including visual UI testing.
"""
from typing import Dict, Any
from .base_agent import BaseAgent


class TesterAgent(BaseAgent):
    """Creates and runs tests, performs QA"""
    
    def __init__(self):
        super().__init__(
            name="🧪 Tester Agent",
            model="gpt-4o",
            role="Crée et exécute les tests, vérifie la qualité, teste les UI"
        )
    
    async def _do_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        action = task.get("action", "create_tests")
        
        if action == "create_tests":
            return await self._create_tests(task)
        elif action == "qa_review":
            return await self._qa_review(task)
        elif action == "visual_testing":
            return await self._visual_testing(task)
        else:
            return {"success": False, "error": f"Unknown action: {action}"}
    
    async def _create_tests(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Generate test cases for code"""
        code = task.get("code", "")
        test_type = task.get("test_type", "unit")
        
        prompt = f"""
        Génère des tests {test_type} pour ce code:
        
        ```
        {code}
        ```
        
        Inclus:
        1. Tests des cas normaux
        2. Tests des cas limites
        3. Tests des erreurs
        4. Tests de performance (si applicable)
        
        Framework: pytest
        Format: Code Python prêt à exécuter
        """
        result = await self.think(prompt)
        return {"success": True, "tests": result}
    
    async def _qa_review(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Perform quality assurance review"""
        code = task.get("code", "")
        specs = task.get("specs", "")
        
        prompt = f"""
        Fais une revue QA complète:
        
        Spécifications:
        {specs}
        
        Code:
        ```
        {code}
        ```
        
        Vérifie:
        1. Conformité aux specs
        2. Qualité du code
        3. Gestion des erreurs
        4. Logging approprié
        5. Sécurité
        6. Performance
        
        Score chaque catégorie sur 10 et fournis des recommandations.
        """
        result = await self.think(prompt)
        return {"success": True, "qa_report": result}
    
    async def _visual_testing(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze UI screenshots for issues"""
        screenshot_description = task.get("screenshot", "")
        expected = task.get("expected", "")
        
        prompt = f"""
        Analyse cette description d'interface utilisateur:
        
        Interface observée: {screenshot_description}
        Comportement attendu: {expected}
        
        Identifie:
        1. Éléments manquants
        2. Problèmes d'alignement
        3. Problèmes de couleurs/contraste
        4. Problèmes d'accessibilité
        5. Bugs visuels
        
        Format: Liste priorisée des problèmes
        """
        result = await self.think(prompt)
        return {"success": True, "visual_issues": result}
