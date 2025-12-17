"""
🏭 BUILDER AGENT - Automated Application Construction Pipeline
Orchestrates the complete construction of applications using all agents.
A slow but thorough process for optimal quality.
"""
import os
import json
import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime
from .base_agent import BaseAgent
import logging

logger = logging.getLogger(__name__)


class BuildPhase:
    """Represents a phase in the build pipeline"""
    PLANNING = "planning"
    ARCHITECTURE = "architecture"
    SECURITY_REVIEW = "security_review"
    DEVELOPMENT = "development"
    TESTING = "testing"
    DOCUMENTATION = "documentation"
    PERFORMANCE = "performance"
    DEPLOYMENT = "deployment"
    MONITORING = "monitoring"


class BuilderAgent(BaseAgent):
    """
    Automated Application Construction Pipeline
    
    A comprehensive, slow-but-thorough process that uses ALL agents
    to build an application with maximum quality.
    """
    
    def __init__(self):
        super().__init__(
            name="🏭 Builder Agent",
            model="gpt-4o",
            role="Orchestre la construction complète d'applications de manière automatique et optimale"
        )
        self.current_build: Optional[Dict] = None
        self.build_history: List[Dict] = []
        self.phase_results: Dict[str, Any] = {}
    
    async def _do_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        action = task.get("action", "start_build")
        
        actions = {
            "start_build": self._start_build,
            "execute_phase": self._execute_phase,
            "get_build_status": self._get_build_status,
            "generate_plan": self._generate_plan,
            "create_project_structure": self._create_project_structure,
            "full_build": self._full_build,
            "resume_build": self._resume_build,
            "validate_phase": self._validate_phase,
        }
        
        handler = actions.get(action)
        if handler:
            return await handler(task)
        else:
            return {"success": False, "error": f"Unknown action: {action}"}
    
    async def _generate_plan(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a complete build plan for an application"""
        app_description = task.get("description", "")
        app_type = task.get("type", "web")  # web, api, mobile, cli, etc.
        technologies = task.get("technologies", [])
        requirements = task.get("requirements", [])
        
        prompt = f"""
        Génère un plan de construction complet pour cette application:
        
        Description: {app_description}
        Type: {app_type}
        Technologies souhaitées: {technologies}
        Requirements: {requirements}
        
        Crée un plan détaillé en 9 phases:
        
        ## PHASE 1: PLANNING (Architect Agent)
        - Analyse des besoins
        - Définition du scope
        - Estimation du temps
        - Identification des risques
        
        ## PHASE 2: ARCHITECTURE (Architect Agent)
        - Design de l'architecture
        - Choix des technologies finales
        - Structure des dossiers
        - Design patterns à utiliser
        - Diagrammes (décris-les textuellement)
        
        ## PHASE 3: SECURITY REVIEW (Security Agent)
        - Threat modeling
        - Security requirements
        - Authentication/Authorization design
        - Data protection strategy
        
        ## PHASE 4: DEVELOPMENT (Developer Agent)
        - Setup du projet
        - Core features (liste ordonnée)
        - Intégrations
        - Error handling
        
        ## PHASE 5: TESTING (Tester Agent)
        - Unit tests
        - Integration tests
        - E2E tests
        - Test coverage targets
        
        ## PHASE 6: DOCUMENTATION (Documenter Agent)
        - README
        - API documentation
        - User guide
        - Developer guide
        
        ## PHASE 7: PERFORMANCE (Performance Agent)
        - Performance benchmarks
        - Optimizations
        - Load testing
        
        ## PHASE 8: DEPLOYMENT (DevOps Agent)
        - CI/CD pipeline
        - Environment setup
        - Deployment strategy
        - Rollback plan
        
        ## PHASE 9: MONITORING (Monitor Agent)
        - Logging setup
        - Metrics collection
        - Alerting rules
        - Health checks
        
        Pour chaque phase:
        - Durée estimée
        - Agents impliqués
        - Livrables attendus
        - Critères de validation
        - Dépendances
        
        Format: JSON structuré avec toutes les phases
        """
        
        result = await self.think(prompt)
        
        build_plan = {
            "id": f"build_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "description": app_description,
            "type": app_type,
            "technologies": technologies,
            "requirements": requirements,
            "plan": result,
            "created_at": datetime.now().isoformat(),
            "status": "planned",
            "current_phase": None,
            "completed_phases": []
        }
        
        self.current_build = build_plan
        
        return {
            "success": True,
            "build_id": build_plan["id"],
            "plan": result
        }
    
    async def _start_build(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Start the automated build process"""
        plan = task.get("plan") or self.current_build
        
        if not plan:
            return {"success": False, "error": "No build plan found. Generate a plan first."}
        
        self.current_build = plan if isinstance(plan, dict) else {"plan": plan}
        self.current_build["status"] = "in_progress"
        self.current_build["started_at"] = datetime.now().isoformat()
        self.phase_results = {}
        
        return {
            "success": True,
            "message": "Build started",
            "build_id": self.current_build.get("id", "current"),
            "status": "in_progress"
        }
    
    async def _execute_phase(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a specific build phase"""
        phase = task.get("phase", BuildPhase.PLANNING)
        context = task.get("context", {})
        
        # Add previous phase results to context
        context["previous_phases"] = self.phase_results
        
        phase_handlers = {
            BuildPhase.PLANNING: self._phase_planning,
            BuildPhase.ARCHITECTURE: self._phase_architecture,
            BuildPhase.SECURITY_REVIEW: self._phase_security,
            BuildPhase.DEVELOPMENT: self._phase_development,
            BuildPhase.TESTING: self._phase_testing,
            BuildPhase.DOCUMENTATION: self._phase_documentation,
            BuildPhase.PERFORMANCE: self._phase_performance,
            BuildPhase.DEPLOYMENT: self._phase_deployment,
            BuildPhase.MONITORING: self._phase_monitoring,
        }
        
        handler = phase_handlers.get(phase)
        if not handler:
            return {"success": False, "error": f"Unknown phase: {phase}"}
        
        logger.info(f"🏭 Executing phase: {phase}")
        
        try:
            result = await handler(context)
            self.phase_results[phase] = result
            
            if self.current_build:
                if "completed_phases" not in self.current_build:
                    self.current_build["completed_phases"] = []
                self.current_build["completed_phases"].append(phase)
                self.current_build["current_phase"] = phase
            
            return {
                "success": True,
                "phase": phase,
                "result": result
            }
        except Exception as e:
            logger.error(f"Phase {phase} failed: {e}")
            return {"success": False, "phase": phase, "error": str(e)}
    
    async def _phase_planning(self, context: Dict) -> Dict[str, Any]:
        """Phase 1: Planning"""
        prompt = f"""
        PHASE 1: PLANNING
        
        Contexte du build: {context}
        
        Effectue la planification détaillée:
        
        1. **ANALYSE DES BESOINS**
           - Users/Personas
           - Use cases principaux
           - Contraintes techniques
           - Contraintes business
        
        2. **SCOPE DEFINITION**
           - Features MVP (must have)
           - Features V1 (should have)
           - Features futures (nice to have)
        
        3. **ESTIMATION**
           - Temps par feature
           - Complexité (1-10)
           - Ressources nécessaires
        
        4. **RISQUES**
           - Risques techniques
           - Risques business
           - Mitigation strategies
        
        5. **MILESTONES**
           - Jalons clés
           - Dates cibles
           - Critères de succès
        
        Format: Plan structuré actionnable
        """
        return {"phase": "planning", "output": await self.think(prompt)}
    
    async def _phase_architecture(self, context: Dict) -> Dict[str, Any]:
        """Phase 2: Architecture Design"""
        planning_result = context.get("previous_phases", {}).get("planning", {})
        
        prompt = f"""
        PHASE 2: ARCHITECTURE
        
        Résultat planning: {planning_result}
        
        Conçois l'architecture:
        
        1. **ARCHITECTURE GLOBALE**
           - Pattern (monolith, microservices, serverless)
           - Layers (frontend, backend, data)
           - Communication (REST, GraphQL, gRPC)
        
        2. **STACK TECHNIQUE**
           - Frontend: framework, state management, styling
           - Backend: language, framework, ORM
           - Database: type, engine
           - Cache: strategy, tool
           - Queue: if needed
        
        3. **STRUCTURE DU PROJET**
           - Arborescence des dossiers
           - Naming conventions
           - Module organization
        
        4. **DESIGN PATTERNS**
           - Patterns à utiliser
           - Anti-patterns à éviter
        
        5. **DIAGRAMMES (description textuelle)**
           - Architecture diagram
           - Data flow diagram
           - Entity relationship diagram
        
        6. **API DESIGN**
           - Endpoints principaux
           - Request/Response formats
           - Versioning strategy
        
        Format: Document d'architecture complet
        """
        return {"phase": "architecture", "output": await self.think(prompt)}
    
    async def _phase_security(self, context: Dict) -> Dict[str, Any]:
        """Phase 3: Security Review"""
        arch_result = context.get("previous_phases", {}).get("architecture", {})
        
        prompt = f"""
        PHASE 3: SECURITY REVIEW
        
        Architecture proposée: {arch_result}
        
        Effectue la review sécurité:
        
        1. **THREAT MODELING**
           - Attack surface
           - Threat actors
           - Attack vectors
           - STRIDE analysis
        
        2. **AUTHENTICATION**
           - Méthode (JWT, OAuth, etc.)
           - MFA requirements
           - Session management
        
        3. **AUTHORIZATION**
           - RBAC/ABAC design
           - Permission model
           - Resource protection
        
        4. **DATA PROTECTION**
           - Encryption at rest
           - Encryption in transit
           - PII handling
           - GDPR compliance
        
        5. **SECURE CODING**
           - Input validation rules
           - Output encoding
           - SQL injection prevention
           - XSS prevention
        
        6. **SECURITY CONTROLS**
           - Rate limiting
           - CORS policy
           - CSP headers
           - Audit logging
        
        7. **SECRETS MANAGEMENT**
           - How to store secrets
           - Rotation strategy
        
        Format: Security requirements document
        """
        return {"phase": "security", "output": await self.think(prompt)}
    
    async def _phase_development(self, context: Dict) -> Dict[str, Any]:
        """Phase 4: Development"""
        all_phases = context.get("previous_phases", {})
        
        prompt = f"""
        PHASE 4: DEVELOPMENT
        
        Phases précédentes: 
        - Planning: {all_phases.get('planning', {}).get('output', '')[:1000]}
        - Architecture: {all_phases.get('architecture', {}).get('output', '')[:1000]}
        - Security: {all_phases.get('security', {}).get('output', '')[:1000]}
        
        Génère le plan de développement:
        
        1. **PROJECT SETUP**
           - Commands d'initialisation
           - Dependencies à installer
           - Configuration files
        
        2. **CORE STRUCTURE**
           - Fichiers de base à créer
           - Boilerplate code
           - Configuration
        
        3. **FEATURES DEVELOPMENT ORDER**
           Pour chaque feature:
           - Nom
           - Description
           - Fichiers à créer/modifier
           - Tests associés
           - Durée estimée
        
        4. **INTEGRATIONS**
           - APIs tierces
           - Services externes
           - Configurations
        
        5. **ERROR HANDLING**
           - Strategy globale
           - Error types
           - User feedback
        
        6. **CODE SAMPLES**
           - Exemples de code pour les patterns clés
           - Best practices à suivre
        
        Format: Development roadmap avec code snippets
        """
        return {"phase": "development", "output": await self.think(prompt)}
    
    async def _phase_testing(self, context: Dict) -> Dict[str, Any]:
        """Phase 5: Testing"""
        dev_result = context.get("previous_phases", {}).get("development", {})
        
        prompt = f"""
        PHASE 5: TESTING
        
        Development plan: {dev_result}
        
        Crée la stratégie de test:
        
        1. **TEST STRATEGY**
           - Test pyramid
           - Coverage targets
           - Testing tools
        
        2. **UNIT TESTS**
           - Components à tester
           - Mocks/Stubs needed
           - Sample test cases
        
        3. **INTEGRATION TESTS**
           - Flows à tester
           - Setup/Teardown
           - Test data
        
        4. **E2E TESTS**
           - User journeys
           - Critical paths
           - Browser/Device matrix
        
        5. **PERFORMANCE TESTS**
           - Load test scenarios
           - Stress test scenarios
           - Benchmarks
        
        6. **SECURITY TESTS**
           - Vulnerability scans
           - Penetration test scenarios
        
        7. **CI INTEGRATION**
           - Test commands
           - Coverage reports
           - Quality gates
        
        Format: Test plan complet avec exemples de code
        """
        return {"phase": "testing", "output": await self.think(prompt)}
    
    async def _phase_documentation(self, context: Dict) -> Dict[str, Any]:
        """Phase 6: Documentation"""
        all_phases = context.get("previous_phases", {})
        
        prompt = f"""
        PHASE 6: DOCUMENTATION
        
        Génère la documentation complète:
        
        1. **README.md**
           - Project description
           - Features
           - Getting started
           - Installation
           - Usage examples
           - Contributing
           - License
        
        2. **API DOCUMENTATION**
           - OpenAPI/Swagger spec
           - Endpoints documentation
           - Authentication
           - Examples
        
        3. **DEVELOPER GUIDE**
           - Architecture overview
           - Code structure
           - Conventions
           - Development setup
           - Debugging
        
        4. **USER GUIDE**
           - Features walkthrough
           - Screenshots descriptions
           - FAQ
           - Troubleshooting
        
        5. **CHANGELOG**
           - Version format
           - Initial release notes
        
        6. **DEPLOYMENT GUIDE**
           - Environment setup
           - Configuration
           - Deployment steps
        
        Format: Documents Markdown complets
        """
        return {"phase": "documentation", "output": await self.think(prompt)}
    
    async def _phase_performance(self, context: Dict) -> Dict[str, Any]:
        """Phase 7: Performance Optimization"""
        prompt = f"""
        PHASE 7: PERFORMANCE
        
        Planifie les optimisations de performance:
        
        1. **PERFORMANCE BASELINE**
           - Métriques clés à mesurer
           - Targets (response time, throughput)
           - Tools de mesure
        
        2. **FRONTEND OPTIMIZATION**
           - Bundle size optimization
           - Lazy loading
           - Caching strategy
           - Image optimization
        
        3. **BACKEND OPTIMIZATION**
           - Query optimization
           - Caching (Redis strategies)
           - Connection pooling
           - Async processing
        
        4. **DATABASE OPTIMIZATION**
           - Indexing strategy
           - Query optimization
           - Denormalization if needed
        
        5. **LOAD TESTING**
           - Scenarios
           - Expected load
           - Breaking points
        
        6. **MONITORING**
           - APM setup
           - Key metrics
           - Alerts
        
        Format: Performance optimization plan
        """
        return {"phase": "performance", "output": await self.think(prompt)}
    
    async def _phase_deployment(self, context: Dict) -> Dict[str, Any]:
        """Phase 8: Deployment"""
        prompt = f"""
        PHASE 8: DEPLOYMENT
        
        Crée la stratégie de déploiement:
        
        1. **CI/CD PIPELINE**
           - Pipeline stages
           - Build process
           - Test automation
           - Deployment triggers
        
        2. **ENVIRONMENTS**
           - Development
           - Staging
           - Production
           - Configuration par env
        
        3. **INFRASTRUCTURE**
           - Cloud provider setup
           - Container configuration (Dockerfile)
           - Orchestration (K8s/Fly.io)
        
        4. **DEPLOYMENT PROCESS**
           - Blue/Green or Rolling
           - Health checks
           - Smoke tests
        
        5. **ROLLBACK PLAN**
           - Triggers
           - Process
           - Communication
        
        6. **SECRETS MANAGEMENT**
           - How to inject
           - Rotation process
        
        Format: Deployment runbook avec scripts
        """
        return {"phase": "deployment", "output": await self.think(prompt)}
    
    async def _phase_monitoring(self, context: Dict) -> Dict[str, Any]:
        """Phase 9: Monitoring Setup"""
        prompt = f"""
        PHASE 9: MONITORING
        
        Configure le monitoring:
        
        1. **LOGGING**
           - Log format
           - Log levels
           - Log aggregation
           - Log retention
        
        2. **METRICS**
           - Business metrics
           - Technical metrics
           - Custom metrics
        
        3. **ALERTING**
           - Critical alerts
           - Warning alerts
           - Notification channels
           - Escalation policy
        
        4. **DASHBOARDS**
           - Overview dashboard
           - Technical dashboard
           - Business dashboard
        
        5. **HEALTH CHECKS**
           - Endpoints
           - Frequency
           - Timeout handling
        
        6. **INCIDENT RESPONSE**
           - Playbooks
           - On-call setup
           - Post-mortem template
        
        Format: Monitoring configuration guide
        """
        return {"phase": "monitoring", "output": await self.think(prompt)}
    
    async def _full_build(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the complete build pipeline"""
        # First generate the plan
        plan_result = await self._generate_plan(task)
        if not plan_result.get("success"):
            return plan_result
        
        # Start the build
        await self._start_build({})
        
        # Execute all phases in order
        phases = [
            BuildPhase.PLANNING,
            BuildPhase.ARCHITECTURE,
            BuildPhase.SECURITY_REVIEW,
            BuildPhase.DEVELOPMENT,
            BuildPhase.TESTING,
            BuildPhase.DOCUMENTATION,
            BuildPhase.PERFORMANCE,
            BuildPhase.DEPLOYMENT,
            BuildPhase.MONITORING,
        ]
        
        results = {}
        for phase in phases:
            logger.info(f"🏭 Starting phase: {phase}")
            result = await self._execute_phase({"phase": phase, "context": task})
            results[phase] = result
            
            if not result.get("success"):
                logger.error(f"Phase {phase} failed, stopping build")
                break
            
            # Small delay between phases for rate limiting
            await asyncio.sleep(2)
        
        self.current_build["status"] = "completed"
        self.current_build["completed_at"] = datetime.now().isoformat()
        self.build_history.append(self.current_build)
        
        return {
            "success": True,
            "build_id": self.current_build.get("id"),
            "phases_completed": list(results.keys()),
            "results": results
        }
    
    async def _get_build_status(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Get current build status"""
        if not self.current_build:
            return {"success": False, "error": "No active build"}
        
        return {
            "success": True,
            "build": self.current_build,
            "phase_results": self.phase_results,
            "history": len(self.build_history)
        }
    
    async def _resume_build(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Resume a build from a specific phase"""
        from_phase = task.get("from_phase", BuildPhase.PLANNING)
        
        phases = [
            BuildPhase.PLANNING,
            BuildPhase.ARCHITECTURE,
            BuildPhase.SECURITY_REVIEW,
            BuildPhase.DEVELOPMENT,
            BuildPhase.TESTING,
            BuildPhase.DOCUMENTATION,
            BuildPhase.PERFORMANCE,
            BuildPhase.DEPLOYMENT,
            BuildPhase.MONITORING,
        ]
        
        start_idx = phases.index(from_phase) if from_phase in phases else 0
        remaining = phases[start_idx:]
        
        results = {}
        for phase in remaining:
            result = await self._execute_phase({"phase": phase, "context": task})
            results[phase] = result
            
            if not result.get("success"):
                break
            
            await asyncio.sleep(2)
        
        return {"success": True, "resumed_from": from_phase, "results": results}
    
    async def _validate_phase(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Validate a completed phase"""
        phase = task.get("phase", "")
        phase_output = task.get("output", "")
        
        prompt = f"""
        Valide le résultat de la phase '{phase}':
        
        Output: {phase_output[:3000]}
        
        Critères de validation:
        1. Completeness - Tous les éléments requis sont présents
        2. Quality - Le contenu est de haute qualité
        3. Actionability - Les outputs sont actionnables
        4. Consistency - Cohérent avec les phases précédentes
        
        Donne:
        - Score: X/100
        - Issues trouvées
        - Recommendations
        - Ready for next phase: Oui/Non
        """
        
        validation = await self.think(prompt)
        return {"success": True, "phase": phase, "validation": validation}
    
    async def _create_project_structure(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Generate the project file structure"""
        architecture = task.get("architecture", "")
        project_type = task.get("type", "web")
        
        prompt = f"""
        Génère la structure de fichiers du projet:
        
        Type: {project_type}
        Architecture: {architecture}
        
        Fournis:
        1. Arborescence complète des dossiers/fichiers
        2. Contenu initial de chaque fichier de configuration
        3. Commands pour créer la structure
        
        Format:
        ```
        project/
        ├── src/
        │   ├── ...
        ├── tests/
        │   ├── ...
        ├── docs/
        ├── package.json / requirements.txt
        ├── README.md
        └── ...
        ```
        
        Avec le contenu de chaque fichier important.
        """
        
        result = await self.think(prompt)
        return {"success": True, "structure": result}
