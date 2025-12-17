"""
📚 DOCUMENTER AGENT
Generates documentation, READMEs, API docs, and user guides.
Uses Groq for fast generation.
"""
from typing import Dict, Any
from .base_agent import BaseAgent


class DocumenterAgent(BaseAgent):
    """Generates all types of documentation"""
    
    def __init__(self):
        super().__init__(
            name="📚 Documenter Agent",
            model="groq-llama3",
            role="Génère la documentation, README, guides utilisateur, changelog"
        )
    
    async def _do_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        action = task.get("action", "generate_readme")
        
        actions = {
            "generate_readme": self._generate_readme,
            "api_docs": self._generate_api_docs,
            "user_guide": self._generate_user_guide,
            "changelog": self._generate_changelog,
            "tutorials": self._generate_tutorials,
            "generate_docs": self._generate_readme,  # Alias
            "generate_report": self._generate_report
        }
        
        handler = actions.get(action)
        if handler:
            return await handler(task)
        else:
            return {"success": False, "error": f"Unknown action: {action}"}
    
    async def _generate_readme(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a comprehensive README"""
        project_info = task.get("project_info", task.get("analysis", ""))
        project_name = task.get("project_name", "Project")
        
        prompt = f"""
        Génère un README.md professionnel et complet pour ce projet:
        
        Nom: {project_name}
        Informations: {project_info}
        
        Le README doit inclure:
        1. 🎯 Description du projet (avec badges)
        2. ✨ Features principales
        3. 🚀 Getting Started
           - Prérequis
           - Installation
           - Configuration
        4. 📖 Usage / Exemples de code
        5. 🏗️ Architecture
        6. 🔧 Configuration
        7. 📊 API Reference (si applicable)
        8. 🧪 Tests
        9. 📈 Roadmap
        10. 🤝 Contributing
        11. 📄 License
        
        Utilise des emojis, du markdown riche, et des blocs de code.
        Format: Markdown complet prêt à utiliser
        """
        result = await self.think(prompt)
        return {"success": True, "readme": result, "format": "markdown"}
    
    async def _generate_api_docs(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Generate API documentation"""
        endpoints = task.get("endpoints", [])
        api_info = task.get("api_info", "")
        
        prompt = f"""
        Génère une documentation API complète au format OpenAPI/Swagger-like:
        
        API Info: {api_info}
        Endpoints: {endpoints}
        
        Pour chaque endpoint, documente:
        1. HTTP Method + Path
        2. Description
        3. Parameters (query, path, body)
        4. Request body schema
        5. Response schemas (success + erreurs)
        6. Exemples curl/JavaScript
        7. Authorization requise
        
        Format: Markdown structuré avec code blocks
        """
        result = await self.think(prompt)
        return {"success": True, "api_docs": result, "format": "markdown"}
    
    async def _generate_user_guide(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Generate user guide"""
        product = task.get("product", "")
        features = task.get("features", [])
        
        prompt = f"""
        Crée un guide utilisateur complet pour:
        
        Produit: {product}
        Features: {features}
        
        Structure du guide:
        1. Introduction
        2. Premiers pas
        3. Interface utilisateur (avec descriptions visuelles)
        4. Fonctionnalités principales
           - Pour chaque feature: description, étapes, conseils
        5. Cas d'usage courants
        6. Dépannage / FAQ
        7. Raccourcis clavier (si applicable)
        8. Glossaire
        
        Style: Clair, accessible, avec des captures d'écran suggérées
        """
        result = await self.think(prompt)
        return {"success": True, "user_guide": result, "format": "markdown"}
    
    async def _generate_changelog(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Generate changelog from commits or changes"""
        version = task.get("version", "1.0.0")
        changes = task.get("changes", [])
        previous_version = task.get("previous_version", "")
        
        prompt = f"""
        Génère un CHANGELOG.md professionnel:
        
        Version: {version}
        Version précédente: {previous_version}
        Changements: {changes}
        
        Format (Keep a Changelog):
        
        ## [{version}] - YYYY-MM-DD
        
        ### Added
        - Nouvelles fonctionnalités
        
        ### Changed
        - Modifications
        
        ### Deprecated
        - Fonctionnalités dépréciées
        
        ### Removed
        - Fonctionnalités supprimées
        
        ### Fixed
        - Corrections de bugs
        
        ### Security
        - Corrections de sécurité
        
        Sois précis et professionnel.
        """
        result = await self.think(prompt)
        return {"success": True, "changelog": result, "version": version}
    
    async def _generate_tutorials(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Generate step-by-step tutorials"""
        topic = task.get("topic", "")
        level = task.get("level", "beginner")
        
        prompt = f"""
        Crée un tutoriel détaillé:
        
        Sujet: {topic}
        Niveau: {level}
        
        Structure:
        1. Objectifs d'apprentissage
        2. Prérequis
        3. Durée estimée
        4. Étapes détaillées
           - Chaque étape avec:
             * Explication
             * Code / Commandes
             * Résultat attendu
             * Points d'attention
        5. Exercices pratiques
        6. Pour aller plus loin
        7. Ressources complémentaires
        
        Style: Pédagogique, progressif, avec exemples concrets
        """
        result = await self.think(prompt)
        return {"success": True, "tutorial": result, "topic": topic, "level": level}
    
    async def _generate_report(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Generate analysis report from collected data"""
        data = task.get("data", task)
        report_type = task.get("report_type", "analysis")
        
        prompt = f"""
        Génère un rapport {report_type} professionnel:
        
        Données: {data}
        
        Structure du rapport:
        1. Résumé exécutif
        2. Contexte et objectifs
        3. Méthodologie
        4. Résultats principaux
           - Points forts
           - Points d'amélioration
           - Risques identifiés
        5. Recommandations prioritaires
        6. Plan d'action suggéré
        7. Conclusion
        8. Annexes (si données supplémentaires)
        
        Style: Professionnel, actionnable, avec métriques si disponibles
        """
        result = await self.think(prompt)
        return {"success": True, "report": result, "type": report_type}
