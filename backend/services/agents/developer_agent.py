"""
👨‍💻 DEVELOPER AGENT
Uses Claude 3.5 Sonnet for precise code generation.
"""
from typing import Dict, Any
from .base_agent import BaseAgent


class DeveloperAgent(BaseAgent):
    """Writes code, implements features, fixes bugs"""
    
    def __init__(self):
        super().__init__(
            name="👨‍💻 Developer Agent",
            model="claude-3.5-sonnet",
            role="Écrit le code, implémente les features, refactore"
        )
    
    async def _do_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        action = task.get("action", "write_code")
        
        if action == "write_code":
            return await self._write_code(task)
        elif action == "implement_feature":
            return await self._implement_feature(task)
        elif action == "fix_bug":
            return await self._fix_bug(task)
        elif action == "refactor":
            return await self._refactor(task)
        else:
            return {"success": False, "error": f"Unknown action: {action}"}
    
    async def _write_code(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Generate code based on specifications"""
        specs = task.get("specs", "")
        language = task.get("language", "python")
        
        prompt = f"""
        Génère le code suivant les spécifications:
        
        Specifications:
        {specs}
        
        Language: {language}
        
        Règles:
        - Code propre et lisible
        - Commentaires en français
        - Gestion d'erreurs robuste
        - Tests unitaires inclus
        - Type hints (si Python)
        
        Fournis le code complet, prêt à être utilisé.
        """
        result = await self.think(prompt)
        return {"success": True, "code": result}
    
    async def _implement_feature(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Implement a complete feature"""
        feature = task.get("feature", "")
        existing_code = task.get("existing_code", "")
        
        prompt = f"""
        Implémente cette feature:
        Feature: {feature}
        
        Code existant:
        ```
        {existing_code}
        ```
        
        Fournis:
        1. Le code modifié/ajouté
        2. Les tests pour la feature
        3. La documentation
        """
        result = await self.think(prompt)
        return {"success": True, "implementation": result}
    
    async def _fix_bug(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Fix a bug in existing code"""
        bug_description = task.get("bug", "")
        code = task.get("code", "")
        error_log = task.get("error_log", "")
        
        prompt = f"""
        Corrige ce bug:
        
        Description: {bug_description}
        
        Code actuel:
        ```
        {code}
        ```
        
        Logs d'erreur:
        {error_log}
        
        Fournis:
        1. Explication de la cause
        2. Code corrigé
        3. Test pour éviter la régression
        """
        result = await self.think(prompt)
        return {"success": True, "fix": result}
    
    async def _refactor(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Refactor code for better quality"""
        code = task.get("code", "")
        goals = task.get("goals", "improve readability and performance")
        
        prompt = f"""
        Refactore ce code:
        
        Objectifs: {goals}
        
        Code:
        ```
        {code}
        ```
        
        Fournis:
        1. Code refactoré
        2. Liste des changements
        3. Justification de chaque changement
        """
        result = await self.think(prompt)
        return {"success": True, "refactored": result}
