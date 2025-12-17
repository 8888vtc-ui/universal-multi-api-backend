"""
⚡ PERFORMANCE AGENT
Analyzes and optimizes performance, finds bottlenecks.
Uses Groq for fast analysis.
"""
from typing import Dict, Any
from .base_agent import BaseAgent


class PerformanceAgent(BaseAgent):
    """Expert in performance optimization and analysis"""
    
    def __init__(self):
        super().__init__(
            name="⚡ Performance Agent",
            model="groq-llama3",
            role="Analyse les performances, trouve les bottlenecks, optimise le code"
        )
    
    async def _do_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        action = task.get("action", "analyze_performance")
        
        actions = {
            "analyze_performance": self._analyze_performance,
            "find_bottlenecks": self._find_bottlenecks,
            "optimize_code": self._optimize_code,
            "benchmark": self._benchmark,
            "memory_analysis": self._memory_analysis,
            "database_optimization": self._database_optimization,
        }
        
        handler = actions.get(action)
        if handler:
            return await handler(task)
        else:
            return {"success": False, "error": f"Unknown action: {action}"}
    
    async def _analyze_performance(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze overall performance"""
        metrics = task.get("metrics", {})
        code = task.get("code", "")
        
        prompt = f"""
        Analyse les performances de ce système:
        
        Métriques: {metrics}
        Code: {code[:3000] if code else "Non fourni"}
        
        Analyse:
        1. **Temps de réponse** - Latence moyenne, P95, P99
        2. **Throughput** - Requêtes/seconde
        3. **Utilisation ressources** - CPU, Mémoire, I/O
        4. **Concurrence** - Gestion des threads/async
        5. **Caching** - Efficacité du cache
        
        Score de performance: X/100
        
        Recommandations priorisées avec impact estimé.
        """
        result = await self.think(prompt)
        return {"success": True, "performance_analysis": result}
    
    async def _find_bottlenecks(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Find performance bottlenecks"""
        code = task.get("code", "")
        profile_data = task.get("profile_data", "")
        
        prompt = f"""
        Identifie les bottlenecks de performance:
        
        Code: {code[:4000] if code else "Non fourni"}
        Données de profiling: {profile_data}
        
        Cherche:
        1. **N+1 Queries** - Requêtes DB excessives
        2. **Boucles inefficaces** - Complexité O(n²) ou pire
        3. **Blocking I/O** - Opérations synchrones bloquantes
        4. **Memory leaks** - Fuites mémoire
        5. **Mauvaise utilisation du cache**
        6. **Sérialisation/Désérialisation coûteuse**
        
        Pour chaque bottleneck:
        - Localisation
        - Impact (HIGH/MEDIUM/LOW)
        - Solution proposée
        - Gain estimé
        """
        result = await self.think(prompt)
        return {"success": True, "bottlenecks": result}
    
    async def _optimize_code(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize code for better performance"""
        code = task.get("code", "")
        language = task.get("language", "python")
        
        prompt = f"""
        Optimise ce code {language}:
        
        ```{language}
        {code[:5000]}
        ```
        
        Techniques d'optimisation à appliquer:
        1. Algorithmes plus efficaces
        2. Structures de données optimales
        3. Lazy evaluation
        4. Caching/Memoization
        5. Vectorization (si applicable)
        6. Async/parallelisme
        
        Fournis:
        1. Code optimisé complet
        2. Explication de chaque optimisation
        3. Benchmarks avant/après estimés
        """
        result = await self.think(prompt)
        return {"success": True, "optimized_code": result, "language": language}
    
    async def _benchmark(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Create benchmark tests"""
        code = task.get("code", "")
        functions = task.get("functions", [])
        
        prompt = f"""
        Crée des benchmarks pour ce code:
        
        Code: {code[:3000] if code else "Non fourni"}
        Fonctions à benchmarker: {functions}
        
        Génère:
        1. Tests de benchmark (pytest-benchmark style)
        2. Scénarios de charge
        3. Métriques à collecter
        4. Baseline attendue
        5. Seuils d'alerte
        
        Format: Code Python avec pytest-benchmark
        """
        result = await self.think(prompt)
        return {"success": True, "benchmarks": result}
    
    async def _memory_analysis(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze memory usage"""
        code = task.get("code", "")
        memory_profile = task.get("memory_profile", "")
        
        prompt = f"""
        Analyse l'utilisation mémoire:
        
        Code: {code[:3000] if code else "Non fourni"}
        Profile mémoire: {memory_profile}
        
        Analyse:
        1. **Allocations excessives** - Objets créés en boucle
        2. **Références circulaires** - Objets non libérés
        3. **Grands objets** - Structures de données volumineuses
        4. **Copies inutiles** - Duplication de données
        5. **Generators vs Lists** - Lazy vs Eager evaluation
        
        Recommandations avec économie mémoire estimée.
        """
        result = await self.think(prompt)
        return {"success": True, "memory_analysis": result}
    
    async def _database_optimization(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize database queries and schema"""
        queries = task.get("queries", [])
        schema = task.get("schema", "")
        
        prompt = f"""
        Optimise les requêtes et le schéma DB:
        
        Requêtes: {queries}
        Schéma: {schema}
        
        Analyse:
        1. **Index manquants** - Colonnes à indexer
        2. **Requêtes N+1** - Joins à utiliser
        3. **Full table scans** - Requêtes à optimiser
        4. **Normalisation** - Sur/sous-normalisation
        5. **Pagination** - Offset vs Cursor
        
        Pour chaque optimisation:
        - Requête optimisée
        - Index à créer
        - Gain de performance estimé
        """
        result = await self.think(prompt)
        return {"success": True, "db_optimization": result}
