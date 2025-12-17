"""
ARCHITECT AGENT
Uses GPT-4o for complex reasoning and planning.
Now with GitHub integration to fetch actual code.
"""
import os
import httpx
from typing import Dict, Any, List
from .base_agent import BaseAgent


class ArchitectAgent(BaseAgent):
    """Plans projects, creates specifications, designs architecture"""
    
    def __init__(self):
        super().__init__(
            name="Architect Agent",
            model="gpt-4o",
            role="Analyse les projets, crée les spécifications techniques, planifie les tâches"
        )
        self.github_token = os.getenv("GITHUB_TOKEN")
    
    async def _fetch_repo_structure(self, owner: str, repo: str) -> str:
        """Fetch repository structure from GitHub"""
        if not self.github_token:
            return "ERROR: No GitHub token available"
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                # Get repo info
                headers = {"Authorization": f"Bearer {self.github_token}"}
                
                # Get repo details
                repo_resp = await client.get(
                    f"https://api.github.com/repos/{owner}/{repo}",
                    headers=headers
                )
                repo_info = repo_resp.json()
                
                # Get file tree (root level)
                tree_resp = await client.get(
                    f"https://api.github.com/repos/{owner}/{repo}/contents",
                    headers=headers
                )
                tree = tree_resp.json()
                
                # Build structure summary
                structure = f"""
Repository: {repo_info.get('full_name', repo)}
Description: {repo_info.get('description', 'N/A')}
Language: {repo_info.get('language', 'Unknown')}
Stars: {repo_info.get('stargazers_count', 0)}
Last Updated: {repo_info.get('updated_at', 'Unknown')}

Files and Folders:
"""
                if isinstance(tree, list):
                    for item in tree[:30]:  # Limit to 30 items
                        icon = "[DIR]" if item.get("type") == "dir" else "[FILE]"
                        structure += f"  {icon} {item.get('name', 'unknown')}\n"
                
                # Try to get README
                try:
                    readme_resp = await client.get(
                        f"https://api.github.com/repos/{owner}/{repo}/readme",
                        headers=headers
                    )
                    if readme_resp.status_code == 200:
                        readme_data = readme_resp.json()
                        import base64
                        readme_content = base64.b64decode(readme_data.get("content", "")).decode("utf-8")[:2000]
                        structure += f"\n\nREADME (excerpt):\n{readme_content}"
                except:
                    pass
                
                return structure
                
        except Exception as e:
            return f"Error fetching repo: {str(e)}"
    
    async def _do_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        action = task.get("action", "analyze")
        
        if action == "analyze_codebase":
            return await self._analyze_codebase(task)
        elif action == "create_specs":
            return await self._create_specs(task)
        elif action == "plan_tasks":
            return await self._plan_tasks(task)
        else:
            return {"success": False, "error": f"Unknown action: {action}"}
    
    async def _analyze_codebase(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze a codebase and provide insights"""
        repo_full = task.get("repo", "")
        
        # Parse owner/repo
        parts = repo_full.split("/")
        if len(parts) != 2:
            return {"success": False, "error": f"Invalid repo format: {repo_full}. Use owner/repo"}
        
        owner, repo = parts
        
        # Fetch actual code structure from GitHub
        code_structure = await self._fetch_repo_structure(owner, repo)
        
        prompt = f"""
        Analyse ce projet GitHub et fournis un rapport détaillé.
        
        INFORMATIONS DU REPOSITORY:
        {code_structure}
        
        Fournis une analyse complète avec:
        1. Architecture globale du projet
        2. Technologies utilisées (frameworks, libs)
        3. Points forts du projet
        4. Points à améliorer / Bugs potentiels
        5. Risques de sécurité
        6. Recommandations prioritaires (top 5)
        
        Sois précis et actionnable dans tes recommandations.
        Format: Markdown structuré
        """
        result = await self.think(prompt)
        return {"success": True, "analysis": result, "repo": repo_full}
    
    async def _create_specs(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Create technical specifications for a feature"""
        feature = task.get("feature", "")
        context = task.get("context", "")
        
        prompt = f"""
        Crée une spécification technique complète pour:
        Feature: {feature}
        Contexte: {context}
        
        Inclus:
        1. Description détaillée
        2. User stories
        3. Critères d'acceptation
        4. Architecture technique
        5. Endpoints API (si applicable)
        6. Modèles de données
        7. Tests requis
        8. Estimation de temps
        
        Format: Markdown structuré
        """
        result = await self.think(prompt)
        return {"success": True, "specs": result}
    
    async def _plan_tasks(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Break down a project into actionable tasks"""
        project = task.get("project", "")
        
        prompt = f"""
        Décompose ce projet en tâches actionables:
        Projet: {project}
        
        Pour chaque tâche, indique:
        - ID unique
        - Description
        - Agent responsable (developer, tester, deployer)
        - Dépendances
        - Priorité (1-5)
        - Estimation (heures)
        
        Format: JSON array
        """
        result = await self.think(prompt)
        return {"success": True, "tasks": result}
