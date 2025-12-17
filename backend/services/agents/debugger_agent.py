"""
🔧 DEBUGGER AGENT
Uses DeepSeek for code analysis and bug detection.
"""
from typing import Dict, Any
from .base_agent import BaseAgent


class DebuggerAgent(BaseAgent):
    """Analyzes errors, finds bugs, suggests fixes"""
    
    def __init__(self):
        super().__init__(
            name="🔧 Debugger Agent",
            model="deepseek-coder",
            role="Analyse les erreurs, trouve les bugs, propose des corrections"
        )
    
    async def _do_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        action = task.get("action", "analyze_error")
        
        if action == "analyze_error":
            return await self._analyze_error(task)
        elif action == "find_bugs":
            return await self._find_bugs(task)
        elif action == "trace_issue":
            return await self._trace_issue(task)
        else:
            return {"success": False, "error": f"Unknown action: {action}"}
    
    async def _analyze_error(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze an error and find root cause"""
        error_log = task.get("error_log", "")
        code = task.get("code", "")
        
        prompt = f"""
        Analyse cette erreur et trouve la cause:
        
        Log d'erreur:
        {error_log}
        
        Code concerné:
        ```
        {code}
        ```
        
        Fournis:
        1. Cause racine identifiée
        2. Ligne(s) problématique(s)
        3. Solution proposée
        4. Code corrigé
        """
        result = await self.think(prompt)
        return {"success": True, "analysis": result}
    
    async def _find_bugs(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Scan code for potential bugs"""
        code = task.get("code", "")
        
        prompt = f"""
        Analyse ce code et trouve tous les bugs potentiels:
        
        ```
        {code}
        ```
        
        Pour chaque bug trouvé:
        1. Ligne concernée
        2. Type de bug (logic, security, performance, etc.)
        3. Sévérité (critical, high, medium, low)
        4. Description du problème
        5. Solution recommandée
        
        Format: JSON array
        """
        result = await self.think(prompt)
        return {"success": True, "bugs": result}
    
    async def _trace_issue(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Trace an issue through the codebase"""
        issue = task.get("issue", "")
        codebase = task.get("codebase", "")
        
        prompt = f"""
        Trace ce problème à travers le code:
        
        Problème: {issue}
        
        Codebase:
        {codebase}
        
        Fournis:
        1. Chemin d'exécution qui mène au problème
        2. Variables/états impliqués
        3. Point exact de défaillance
        4. Correctif minimal
        """
        result = await self.think(prompt)
        return {"success": True, "trace": result}
