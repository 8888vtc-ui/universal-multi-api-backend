"""
🔧 DEVOPS AGENT
Handles deployments, infrastructure, CI/CD, and cloud operations.
Uses Groq for fast responses.
"""
from typing import Dict, Any
from .base_agent import BaseAgent


class DevOpsAgent(BaseAgent):
    """Expert in DevOps, CI/CD, and infrastructure"""
    
    def __init__(self):
        super().__init__(
            name="🔧 DevOps Agent",
            model="groq-llama3",
            role="Gère les déploiements, infrastructure, CI/CD, et opérations cloud"
        )
    
    async def _do_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        action = task.get("action", "deploy")
        
        actions = {
            "deploy": self._deploy,
            "rollback": self._rollback,
            "create_pipeline": self._create_pipeline,
            "infrastructure_review": self._infrastructure_review,
            "docker_optimize": self._docker_optimize,
            "kubernetes_config": self._kubernetes_config,
            "monitoring_setup": self._monitoring_setup,
            "cost_optimization": self._cost_optimization,
        }
        
        handler = actions.get(action)
        if handler:
            return await handler(task)
        else:
            return {"success": False, "error": f"Unknown action: {action}"}
    
    async def _deploy(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Generate deployment plan"""
        environment = task.get("environment", "production")
        platform = task.get("platform", "fly.io")
        
        prompt = f"""
        Génère un plan de déploiement pour:
        
        Environment: {environment}
        Platform: {platform}
        
        Plan de déploiement:
        
        1. **PRE-DEPLOYMENT**
           - Checklist de validation
           - Tests à exécuter
           - Backups à créer
        
        2. **DEPLOYMENT STEPS**
           - Commandes exactes
           - Ordre d'exécution
           - Points de contrôle
        
        3. **POST-DEPLOYMENT**
           - Vérifications santé
           - Smoke tests
           - Monitoring à activer
        
        4. **ROLLBACK PLAN**
           - Critères de rollback
           - Procédure de rollback
           - Communications
        
        Format: Checklist actionable avec commandes
        """
        result = await self.think(prompt)
        return {"success": True, "deployment_plan": result, "environment": environment}
    
    async def _rollback(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Generate rollback procedure"""
        version = task.get("version", "previous")
        reason = task.get("reason", "")
        
        prompt = f"""
        Procédure de rollback:
        
        Version cible: {version}
        Raison: {reason}
        
        Étapes de rollback:
        1. Arrêter le trafic entrant
        2. Sauvegarder l'état actuel
        3. Restaurer version précédente
        4. Vérifier l'intégrité des données
        5. Rouvrir le trafic progressivement
        6. Post-mortem et communication
        
        Commandes spécifiques et temps estimé pour chaque étape.
        """
        result = await self.think(prompt)
        return {"success": True, "rollback_procedure": result}
    
    async def _create_pipeline(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Create CI/CD pipeline configuration"""
        platform = task.get("platform", "github-actions")
        project_type = task.get("project_type", "python")
        
        prompt = f"""
        Crée une pipeline CI/CD pour:
        
        Platform: {platform}
        Type de projet: {project_type}
        
        La pipeline doit inclure:
        
        1. **BUILD**
           - Installation dépendances
           - Compilation/Build
           - Assets statiques
        
        2. **TEST**
           - Tests unitaires
           - Tests d'intégration
           - Linting/Formatting
           - Coverage
        
        3. **SECURITY**
           - Scan vulnérabilités
           - SAST/DAST
           - Secrets detection
        
        4. **DEPLOY**
           - Staging automatique
           - Production manuelle
           - Notifications
        
        Format: Fichier YAML complet ({platform})
        """
        result = await self.think(prompt)
        return {"success": True, "pipeline": result, "platform": platform}
    
    async def _infrastructure_review(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Review infrastructure setup"""
        infra = task.get("infrastructure", "")
        
        prompt = f"""
        Review de l'infrastructure:
        
        {infra}
        
        Analyse:
        1. **ARCHITECTURE**
           - Scalabilité
           - Haute disponibilité
           - Disaster recovery
        
        2. **SÉCURITÉ**
           - Network security
           - Access management
           - Encryption
        
        3. **COÛTS**
           - Ressources sur-provisionnées
           - Optimisations possibles
        
        4. **OBSERVABILITÉ**
           - Logging
           - Monitoring
           - Alerting
        
        5. **CONFORMITÉ**
           - Best practices cloud
           - Compliance requirements
        
        Score infrastructure: X/100
        Recommandations priorisées.
        """
        result = await self.think(prompt)
        return {"success": True, "infra_review": result}
    
    async def _docker_optimize(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize Dockerfile"""
        dockerfile = task.get("dockerfile", "")
        
        prompt = f"""
        Optimise ce Dockerfile:
        
        ```dockerfile
        {dockerfile}
        ```
        
        Optimisations:
        1. Multi-stage build
        2. Layer caching
        3. Image minimale (alpine/distroless)
        4. Non-root user
        5. Health checks
        6. .dockerignore
        7. Labels et metadata
        
        Fournis:
        - Dockerfile optimisé
        - Réduction taille image estimée
        - Amélioration sécurité
        """
        result = await self.think(prompt)
        return {"success": True, "optimized_dockerfile": result}
    
    async def _kubernetes_config(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Generate Kubernetes configurations"""
        app_name = task.get("app_name", "my-app")
        requirements = task.get("requirements", {})
        
        prompt = f"""
        Génère les configurations Kubernetes pour:
        
        App: {app_name}
        Requirements: {requirements}
        
        Fichiers à générer:
        1. Deployment
        2. Service
        3. Ingress
        4. ConfigMap
        5. Secret (template)
        6. HorizontalPodAutoscaler
        7. PodDisruptionBudget
        
        Best practices:
        - Resource limits/requests
        - Liveness/Readiness probes
        - Security context
        - Pod anti-affinity
        
        Format: Fichiers YAML séparés
        """
        result = await self.think(prompt)
        return {"success": True, "k8s_config": result, "app_name": app_name}
    
    async def _monitoring_setup(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Setup monitoring and alerting"""
        stack = task.get("stack", "prometheus-grafana")
        
        prompt = f"""
        Configure le monitoring avec {stack}:
        
        1. **MÉTRIQUES**
           - Application metrics
           - Infrastructure metrics
           - Business metrics
        
        2. **DASHBOARDS**
           - Overview dashboard
           - SLI/SLO dashboard
           - Debug dashboard
        
        3. **ALERTES**
           - Alertes critiques
           - Alertes warning
           - Runbooks associés
        
        4. **LOGS**
           - Log aggregation
           - Log parsing
           - Log retention
        
        Configurations et fichiers nécessaires.
        """
        result = await self.think(prompt)
        return {"success": True, "monitoring_setup": result, "stack": stack}
    
    async def _cost_optimization(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize cloud costs"""
        cloud_provider = task.get("provider", "AWS")
        current_spend = task.get("current_spend", "")
        
        prompt = f"""
        Optimise les coûts cloud {cloud_provider}:
        
        Dépense actuelle: {current_spend}
        
        Stratégies d'optimisation:
        1. **RIGHT-SIZING**
           - Instances sur-provisionnées
           - Storage inutilisé
        
        2. **RESERVED/SPOT**
           - Reserved instances
           - Spot instances
           - Savings plans
        
        3. **AUTO-SCALING**
           - Scale down periods
           - Scheduled scaling
        
        4. **CLEANUP**
           - Ressources orphelines
           - Snapshots anciens
           - IPs non utilisées
        
        Économies potentielles estimées par catégorie.
        """
        result = await self.think(prompt)
        return {"success": True, "cost_optimization": result, "provider": cloud_provider}
