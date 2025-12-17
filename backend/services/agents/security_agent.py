"""
🔐 SECURITY AGENT
Performs security audits, vulnerability scanning, and compliance checks.
Uses Claude for deep security analysis.
"""
from typing import Dict, Any, List
from .base_agent import BaseAgent


class SecurityAgent(BaseAgent):
    """Expert in security analysis and vulnerability detection"""
    
    def __init__(self):
        super().__init__(
            name="🔐 Security Agent",
            model="claude-3.5-sonnet",
            role="Analyse la sécurité, détecte les vulnérabilités, vérifie la conformité"
        )
    
    async def _do_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        action = task.get("action", "security_audit")
        
        actions = {
            "security_audit": self._security_audit,
            "vulnerability_scan": self._vulnerability_scan,
            "dependency_check": self._dependency_check,
            "compliance_check": self._compliance_check,
            "penetration_test": self._penetration_test,
            "secrets_scan": self._secrets_scan,
        }
        
        handler = actions.get(action)
        if handler:
            return await handler(task)
        else:
            return {"success": False, "error": f"Unknown action: {action}"}
    
    async def _security_audit(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Complete security audit of code/project"""
        code = task.get("code", "")
        project_info = task.get("project_info", "")
        
        prompt = f"""
        Effectue un audit de sécurité complet:
        
        Projet: {project_info}
        Code: {code[:5000] if code else "Non fourni"}
        
        Analyse les aspects suivants:
        
        1. **AUTHENTICATION & AUTHORIZATION**
           - Mécanismes d'authentification
           - Gestion des sessions/tokens
           - Contrôle d'accès (RBAC)
        
        2. **DATA PROTECTION**
           - Chiffrement des données sensibles
           - Protection contre les fuites
           - Gestion des secrets (API keys, passwords)
        
        3. **INPUT VALIDATION**
           - Injection SQL
           - XSS (Cross-Site Scripting)
           - CSRF (Cross-Site Request Forgery)
           - Command Injection
        
        4. **API SECURITY**
           - Rate limiting
           - Validation des entrées
           - Headers de sécurité
        
        5. **DEPENDENCIES**
           - Packages vulnérables
           - Versions obsolètes
        
        6. **CONFIGURATION**
           - Mode debug en production
           - Exposition d'informations sensibles
        
        Pour chaque vulnérabilité trouvée:
        - Sévérité (CRITICAL/HIGH/MEDIUM/LOW)
        - Description
        - Impact potentiel
        - Recommandation de correction
        
        Format: Markdown structuré
        """
        result = await self.think(prompt)
        return {"success": True, "audit": result, "type": "security_audit"}
    
    async def _vulnerability_scan(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Scan for common vulnerabilities"""
        code = task.get("code", "")
        language = task.get("language", "python")
        
        prompt = f"""
        Scan ce code {language} pour les vulnérabilités connues:
        
        ```{language}
        {code[:8000]}
        ```
        
        Cherche spécifiquement:
        - OWASP Top 10 2021
        - CWE Top 25
        - Vulnérabilités spécifiques à {language}
        
        Pour chaque vulnérabilité:
        1. CVE/CWE ID si applicable
        2. Ligne(s) de code concernée(s)
        3. Type de vulnérabilité
        4. Exploit possible
        5. Code corrigé
        
        Format: JSON array avec les vulnérabilités
        """
        result = await self.think(prompt)
        return {"success": True, "vulnerabilities": result, "language": language}
    
    async def _dependency_check(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Check dependencies for known vulnerabilities"""
        dependencies = task.get("dependencies", "")
        
        prompt = f"""
        Analyse ces dépendances pour des vulnérabilités connues:
        
        {dependencies}
        
        Pour chaque dépendance:
        1. Version actuelle vs dernière version
        2. CVE connues
        3. Niveau de risque
        4. Action recommandée
        
        Priorise par criticité.
        Format: Tableau markdown
        """
        result = await self.think(prompt)
        return {"success": True, "dependency_report": result}
    
    async def _compliance_check(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Check compliance with security standards"""
        standard = task.get("standard", "GDPR")
        project_info = task.get("project_info", "")
        
        prompt = f"""
        Vérifie la conformité au standard {standard}:
        
        Projet: {project_info}
        
        Checklist de conformité {standard}:
        
        Pour chaque point:
        - ✅ Conforme
        - ⚠️ Partiellement conforme
        - ❌ Non conforme
        
        Inclus:
        1. Points de conformité vérifiés
        2. Gaps identifiés
        3. Actions correctives requises
        4. Priorités
        """
        result = await self.think(prompt)
        return {"success": True, "compliance_report": result, "standard": standard}
    
    async def _penetration_test(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate penetration test scenarios"""
        target = task.get("target", "")
        scope = task.get("scope", "web application")
        
        prompt = f"""
        Simule un test de pénétration pour:
        
        Cible: {target}
        Scope: {scope}
        
        Phases du pentest:
        
        1. **RECONNAISSANCE**
           - Informations publiques
           - Points d'entrée identifiés
        
        2. **SCANNING**
           - Ports/services exposés
           - Technologies détectées
        
        3. **EXPLOITATION**
           - Vecteurs d'attaque possibles
           - Techniques d'exploit
        
        4. **POST-EXPLOITATION**
           - Données accessibles
           - Possibilités de pivot
        
        5. **RAPPORT**
           - Vulnérabilités exploitables
           - Preuves de concept (PoC)
           - Recommandations
        
        Format: Rapport de pentest professionnel
        """
        result = await self.think(prompt)
        return {"success": True, "pentest_report": result, "target": target}
    
    async def _secrets_scan(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Scan for exposed secrets and credentials"""
        code = task.get("code", "")
        files = task.get("files", [])
        
        prompt = f"""
        Scan pour détecter les secrets exposés:
        
        Code/Fichiers à analyser:
        {code[:5000] if code else str(files)}
        
        Cherche:
        - API Keys (AWS, GCP, Azure, etc.)
        - Tokens (JWT, OAuth, etc.)
        - Mots de passe hardcodés
        - Connexions DB
        - Clés privées
        - URLs avec credentials
        - Variables d'environnement sensibles
        
        Pour chaque secret trouvé:
        1. Type de secret
        2. Localisation
        3. Risque
        4. Action immédiate requise
        
        Format: Liste priorisée
        """
        result = await self.think(prompt)
        return {"success": True, "secrets_found": result}
