"""
🧬 META AGENT - The Agent Creator
Creates, modifies, and optimizes other agents dynamically.
Uses GPT-4o for complex reasoning about agent architectures.
"""
import os
import json
from typing import Dict, Any, List
from .base_agent import BaseAgent
import logging

logger = logging.getLogger(__name__)


class MetaAgent(BaseAgent):
    """Creates and manages other agents - The Agent Factory"""
    
    def __init__(self):
        super().__init__(
            name="🧬 Meta Agent",
            model="gpt-4o",
            role="Crée, modifie et optimise les autres agents dynamiquement"
        )
        self.created_agents: List[Dict] = []
        self.agent_templates: Dict[str, str] = {}
    
    async def _do_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        action = task.get("action", "create_agent")
        
        actions = {
            "create_agent": self._create_agent,
            "modify_agent": self._modify_agent,
            "optimize_agent": self._optimize_agent,
            "analyze_agents": self._analyze_agents,
            "suggest_agents": self._suggest_agents,
            "create_workflow": self._create_workflow,
            "generate_agent_code": self._generate_agent_code,
            "plan_agent_system": self._plan_agent_system,
        }
        
        handler = actions.get(action)
        if handler:
            return await handler(task)
        else:
            return {"success": False, "error": f"Unknown action: {action}"}
    
    async def _create_agent(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new agent based on requirements"""
        agent_name = task.get("name", "")
        purpose = task.get("purpose", "")
        capabilities = task.get("capabilities", [])
        model_preference = task.get("model", "groq-llama3")  # Default to free model
        
        prompt = f"""
        Crée un nouvel agent IA avec ces spécifications:
        
        Nom: {agent_name}
        Objectif: {purpose}
        Capabilities requises: {capabilities}
        Modèle préféré: {model_preference}
        
        Génère:
        1. **DÉFINITION DE L'AGENT**
           - Nom complet avec emoji
           - Rôle détaillé
           - Modèle IA optimal (privilégier les gratuits: groq, gemini, mistral)
           - Fallbacks chain
        
        2. **CAPABILITIES**
           - Liste des actions supportées
           - Description de chaque action
           - Paramètres requis
        
        3. **CODE PYTHON COMPLET**
           - Classe héritant de BaseAgent
           - Méthodes _do_task et actions
           - Prompts optimisés pour chaque action
           - Gestion d'erreurs
        
        4. **CONFIGURATION**
           - Entrée pour config.py (AGENTS dict)
           - Quick actions suggérées
        
        5. **TESTS**
           - Cas de test pour chaque action
        
        Format: Code Python complet prêt à utiliser
        """
        
        result = await self.think(prompt)
        
        agent_spec = {
            "name": agent_name,
            "purpose": purpose,
            "capabilities": capabilities,
            "model": model_preference,
            "code": result,
            "created_at": str(self.last_action)
        }
        self.created_agents.append(agent_spec)
        
        return {
            "success": True,
            "agent": agent_spec,
            "message": f"Agent '{agent_name}' créé avec succès"
        }
    
    async def _modify_agent(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Modify an existing agent"""
        agent_name = task.get("agent_name", "")
        current_code = task.get("current_code", "")
        modifications = task.get("modifications", [])
        
        prompt = f"""
        Modifie l'agent existant:
        
        Agent: {agent_name}
        Code actuel:
        ```python
        {current_code[:5000]}
        ```
        
        Modifications demandées:
        {modifications}
        
        Génère:
        1. Code modifié complet
        2. Liste des changements effectués
        3. Tests mis à jour
        4. Suggestions d'améliorations supplémentaires
        """
        
        result = await self.think(prompt)
        return {"success": True, "modified_code": result, "agent": agent_name}
    
    async def _optimize_agent(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize an agent for better performance"""
        agent_code = task.get("code", "")
        metrics = task.get("metrics", {})
        
        prompt = f"""
        Optimise cet agent pour de meilleures performances:
        
        Code actuel:
        ```python
        {agent_code[:5000]}
        ```
        
        Métriques actuelles: {metrics}
        
        Optimisations à considérer:
        1. Réduire les appels API (prompts plus courts)
        2. Améliorer le caching
        3. Optimiser les fallbacks
        4. Réduire la latence
        5. Améliorer le taux de succès
        
        Génère:
        - Code optimisé
        - Gains de performance estimés
        - Nouvelles métriques attendues
        """
        
        result = await self.think(prompt)
        return {"success": True, "optimized_code": result}
    
    async def _analyze_agents(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze the current agent ecosystem"""
        agents_info = task.get("agents", {})
        
        prompt = f"""
        Analyse l'écosystème d'agents actuel:
        
        Agents disponibles: {json.dumps(agents_info, indent=2) if agents_info else "13 agents standards"}
        
        Analyse:
        1. **COUVERTURE**
           - Domaines bien couverts
           - Domaines manquants
           - Redondances
        
        2. **EFFICACITÉ**
           - Agents les plus utilisés
           - Agents sous-utilisés
           - Bottlenecks potentiels
        
        3. **COÛTS**
           - Répartition modèles payants/gratuits
           - Optimisations de coûts possibles
        
        4. **RECOMMANDATIONS**
           - Nouveaux agents à créer
           - Agents à fusionner
           - Améliorations prioritaires
        
        Score global de l'écosystème: X/100
        """
        
        result = await self.think(prompt)
        return {"success": True, "analysis": result}
    
    async def _suggest_agents(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Suggest new agents based on project needs"""
        project_type = task.get("project_type", "")
        current_agents = task.get("current_agents", [])
        requirements = task.get("requirements", [])
        
        prompt = f"""
        Suggère de nouveaux agents pour ce projet:
        
        Type de projet: {project_type}
        Agents actuels: {current_agents}
        Besoins spécifiques: {requirements}
        
        Pour chaque agent suggéré:
        1. Nom et emoji
        2. Rôle spécifique
        3. Modèle IA recommandé (privilégier gratuits)
        4. Capabilities
        5. Intégration avec agents existants
        6. Priorité (haute/moyenne/basse)
        
        Maximum 5 suggestions, ordonnées par impact.
        """
        
        result = await self.think(prompt)
        return {"success": True, "suggestions": result}
    
    async def _create_workflow(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new workflow combining multiple agents"""
        workflow_name = task.get("name", "")
        objective = task.get("objective", "")
        available_agents = task.get("agents", [])
        
        prompt = f"""
        Crée un nouveau workflow:
        
        Nom: {workflow_name}
        Objectif: {objective}
        Agents disponibles: {available_agents}
        
        Génère:
        1. **WORKFLOW DEFINITION**
           - Description
           - Steps ordonnés (agent + action)
           - Parallel ou séquentiel
           - Conditions de succès/échec
        
        2. **DATA FLOW**
           - Données passées entre steps
           - Transformations nécessaires
        
        3. **ERROR HANDLING**
           - Rollback strategy
           - Retry policy
           - Notifications
        
        4. **CODE CONFIG.PY**
           - Entrée WORKFLOWS dict
           - Quick actions associées
        
        Format: JSON config + description
        """
        
        result = await self.think(prompt)
        return {"success": True, "workflow": result, "name": workflow_name}
    
    async def _generate_agent_code(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Generate complete agent code file"""
        spec = task.get("spec", {})
        
        name = spec.get("name", "CustomAgent")
        model = spec.get("model", "groq-llama3")
        role = spec.get("role", "Agent personnalisé")
        capabilities = spec.get("capabilities", ["execute"])
        
        prompt = f"""
        Génère le code Python complet pour cet agent:
        
        Nom: {name}
        Modèle: {model}
        Rôle: {role}
        Capabilities: {capabilities}
        
        Le code doit:
        1. Hériter de BaseAgent
        2. Implémenter _do_task avec dispatch des actions
        3. Avoir une méthode pour chaque capability
        4. Inclure des prompts optimisés
        5. Gérer les erreurs proprement
        6. Utiliser le logging
        
        Template de base à suivre:
        ```python
        from typing import Dict, Any
        from .base_agent import BaseAgent
        import logging
        
        logger = logging.getLogger(__name__)
        
        class {name.replace(' ', '')}Agent(BaseAgent):
            def __init__(self):
                super().__init__(
                    name="...",
                    model="{model}",
                    role="{role}"
                )
            
            async def _do_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
                action = task.get("action", "...")
                # dispatch actions
        ```
        
        Génère le code complet et fonctionnel.
        """
        
        result = await self.think(prompt)
        return {"success": True, "code": result, "agent_name": name}
    
    async def _plan_agent_system(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Plan a complete agent system for a project"""
        project_description = task.get("project", "")
        constraints = task.get("constraints", [])
        
        prompt = f"""
        Planifie un système d'agents complet pour ce projet:
        
        Projet: {project_description}
        Contraintes: {constraints}
        
        Crée un plan détaillé:
        
        1. **ARCHITECTURE**
           - Vue d'ensemble du système
           - Agents nécessaires (existants + nouveaux)
           - Relations entre agents
        
        2. **AGENTS À CRÉER**
           - Pour chaque nouvel agent:
             * Nom, modèle, rôle
             * Capabilities
             * Intégrations
        
        3. **WORKFLOWS**
           - Workflows principaux
           - Workflows de support
           - Automatisations
        
        4. **PHASES DE DÉVELOPPEMENT**
           - Phase 1: Setup de base
           - Phase 2: Agents core
           - Phase 3: Intégrations
           - Phase 4: Optimisation
        
        5. **ESTIMATION**
           - Temps par phase
           - Ressources (modèles IA, APIs)
           - Coûts estimés
        
        Format: Plan structuré avec priorités
        """
        
        result = await self.think(prompt)
        return {"success": True, "plan": result}
