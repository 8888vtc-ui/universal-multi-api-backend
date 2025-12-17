"""
📊 MONITOR AGENT
Uses Groq (fast) for real-time monitoring and alerting.
"""
from typing import Dict, Any
from .base_agent import BaseAgent


class MonitorAgent(BaseAgent):
    """Watches logs, detects anomalies, sends alerts"""
    
    def __init__(self):
        super().__init__(
            name="📊 Monitor Agent",
            model="groq-llama3",
            role="Surveille les logs, détecte les anomalies, alerte en temps réel"
        )
    
    async def _do_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        action = task.get("action", "watch_logs")
        
        if action == "watch_logs":
            return await self._watch_logs(task)
        elif action == "detect_anomalies":
            return await self._detect_anomalies(task)
        elif action == "health_check":
            return await self._health_check(task)
        elif action == "report":
            return await self._generate_report(task)
        else:
            return {"success": False, "error": f"Unknown action: {action}"}
    
    async def _watch_logs(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze logs for issues"""
        logs = task.get("logs", "")
        
        prompt = f"""
        Analyse ces logs et identifie les problèmes:
        
        {logs}
        
        Catégorise chaque problème:
        - ERROR: Erreurs critiques
        - WARNING: Avertissements
        - ANOMALY: Comportement inhabituel
        - PERFORMANCE: Problèmes de performance
        
        Format: JSON avec niveau, message, timestamp, action_recommandée
        """
        result = await self.think(prompt)
        return {"success": True, "log_analysis": result}
    
    async def _detect_anomalies(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Detect anomalies in metrics or behavior"""
        metrics = task.get("metrics", {})
        baseline = task.get("baseline", {})
        
        prompt = f"""
        Détecte les anomalies dans ces métriques:
        
        Métriques actuelles: {metrics}
        Baseline normal: {baseline}
        
        Identifie:
        1. Déviations significatives
        2. Tendances inquiétantes
        3. Patterns inhabituels
        4. Actions recommandées
        
        Seuil d'alerte: deviation > 20%
        """
        result = await self.think(prompt)
        return {"success": True, "anomalies": result}
    
    async def _health_check(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Perform health check on all systems"""
        systems = task.get("systems", [])
        
        prompt = f"""
        Effectue un health check des systèmes suivants:
        
        Systèmes: {systems}
        
        Pour chaque système, vérifie:
        1. Disponibilité (UP/DOWN)
        2. Latence
        3. Taux d'erreur
        4. Utilisation ressources
        5. Statut global
        
        Format: JSON avec status global et détails par système
        """
        result = await self.think(prompt)
        return {"success": True, "health": result}
    
    async def _generate_report(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a summary report"""
        data = task.get("data", {})
        period = task.get("period", "last 24 hours")
        
        prompt = f"""
        Génère un rapport de monitoring pour: {period}
        
        Données: {data}
        
        Inclus:
        1. Résumé exécutif
        2. Incidents majeurs
        3. Métriques clés
        4. Tendances
        5. Recommandations
        
        Format: Markdown structuré
        """
        result = await self.think(prompt)
        return {"success": True, "report": result}
