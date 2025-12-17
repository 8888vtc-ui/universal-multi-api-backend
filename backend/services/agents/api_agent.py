"""
🌐 API AGENT
Tests APIs, validates endpoints, monitors integrations.
Uses Groq for fast analysis.
"""
import httpx
import asyncio
from typing import Dict, Any, List
from .base_agent import BaseAgent
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class ApiAgent(BaseAgent):
    """Tests and monitors API endpoints"""
    
    def __init__(self):
        super().__init__(
            name="🌐 API Agent",
            model="groq-llama3",
            role="Teste les APIs, valide les endpoints, monitore les intégrations"
        )
    
    async def _do_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        action = task.get("action", "test_endpoint")
        
        actions = {
            "test_endpoint": self._test_endpoint,
            "test_endpoints": self._test_endpoints,
            "validate_response": self._validate_response,
            "load_test": self._load_test,
            "health_check": self._health_check,
            "generate_tests": self._generate_tests,
            "compare_responses": self._compare_responses,
        }
        
        handler = actions.get(action)
        if handler:
            return await handler(task)
        else:
            return {"success": False, "error": f"Unknown action: {action}"}
    
    async def _test_endpoint(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Test a single API endpoint"""
        url = task.get("url", "")
        method = task.get("method", "GET").upper()
        headers = task.get("headers", {})
        body = task.get("body")
        expected_status = task.get("expected_status", 200)
        timeout = task.get("timeout", 30)
        
        if not url:
            return {"success": False, "error": "URL is required"}
        
        try:
            start_time = datetime.now()
            
            async with httpx.AsyncClient(timeout=timeout) as client:
                if method == "GET":
                    response = await client.get(url, headers=headers)
                elif method == "POST":
                    response = await client.post(url, headers=headers, json=body)
                elif method == "PUT":
                    response = await client.put(url, headers=headers, json=body)
                elif method == "DELETE":
                    response = await client.delete(url, headers=headers)
                else:
                    return {"success": False, "error": f"Unsupported method: {method}"}
            
            response_time = (datetime.now() - start_time).total_seconds()
            
            # Try to get JSON response
            try:
                json_response = response.json()
            except:
                json_response = None
            
            result = {
                "success": True,
                "url": url,
                "method": method,
                "status_code": response.status_code,
                "expected_status": expected_status,
                "status_match": response.status_code == expected_status,
                "response_time": f"{response_time:.3f}s",
                "response_size": len(response.content),
                "headers": dict(response.headers),
                "body_preview": str(json_response)[:500] if json_response else response.text[:500]
            }
            
            return result
            
        except httpx.TimeoutException:
            return {"success": False, "url": url, "error": "Timeout", "response_time": f">{timeout}s"}
        except Exception as e:
            return {"success": False, "url": url, "error": str(e)}
    
    async def _test_endpoints(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Test multiple endpoints in parallel"""
        endpoints = task.get("endpoints", [])
        
        if not endpoints:
            return {"success": False, "error": "No endpoints provided"}
        
        tasks = []
        for endpoint in endpoints:
            if isinstance(endpoint, str):
                endpoint = {"url": endpoint, "method": "GET"}
            tasks.append(self._test_endpoint(endpoint))
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        successful = sum(1 for r in results if isinstance(r, dict) and r.get("status_match"))
        failed = len(results) - successful
        
        return {
            "success": failed == 0,
            "total": len(results),
            "successful": successful,
            "failed": failed,
            "results": results
        }
    
    async def _validate_response(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Validate API response against schema or expectations"""
        response = task.get("response", {})
        schema = task.get("schema", {})
        expected_fields = task.get("expected_fields", [])
        
        prompt = f"""
        Valide cette réponse API:
        
        Response: {response}
        
        Schema attendu: {schema if schema else "Non spécifié"}
        Champs attendus: {expected_fields if expected_fields else "Non spécifié"}
        
        Vérifie:
        1. Structure de la réponse
        2. Types de données
        3. Champs manquants
        4. Valeurs nulles inattendues
        5. Format des dates/IDs
        
        Retourne un rapport de validation avec:
        - valid: true/false
        - errors: liste des erreurs
        - warnings: liste des warnings
        """
        
        analysis = await self.think(prompt)
        return {"success": True, "validation": analysis}
    
    async def _load_test(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Simple load test on an endpoint"""
        url = task.get("url", "")
        method = task.get("method", "GET")
        concurrent_requests = task.get("concurrent", 10)
        total_requests = task.get("total", 50)
        
        if not url:
            return {"success": False, "error": "URL is required"}
        
        results = {
            "response_times": [],
            "status_codes": {},
            "errors": 0
        }
        
        async def make_request():
            try:
                start = datetime.now()
                async with httpx.AsyncClient(timeout=30) as client:
                    if method.upper() == "GET":
                        response = await client.get(url)
                    else:
                        response = await client.post(url)
                    
                    response_time = (datetime.now() - start).total_seconds()
                    return {"time": response_time, "status": response.status_code}
            except:
                return {"error": True}
        
        # Execute in batches
        for batch_start in range(0, total_requests, concurrent_requests):
            batch_size = min(concurrent_requests, total_requests - batch_start)
            batch_results = await asyncio.gather(*[make_request() for _ in range(batch_size)])
            
            for r in batch_results:
                if r.get("error"):
                    results["errors"] += 1
                else:
                    results["response_times"].append(r["time"])
                    status = str(r["status"])
                    results["status_codes"][status] = results["status_codes"].get(status, 0) + 1
        
        if results["response_times"]:
            times = results["response_times"]
            stats = {
                "min": f"{min(times):.3f}s",
                "max": f"{max(times):.3f}s",
                "avg": f"{sum(times)/len(times):.3f}s",
                "p95": f"{sorted(times)[int(len(times)*0.95)]:.3f}s" if len(times) > 20 else "N/A"
            }
        else:
            stats = {}
        
        return {
            "success": True,
            "url": url,
            "total_requests": total_requests,
            "concurrent": concurrent_requests,
            "successful": len(results["response_times"]),
            "errors": results["errors"],
            "status_codes": results["status_codes"],
            "response_times": stats
        }
    
    async def _health_check(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Health check multiple services"""
        services = task.get("services", [])
        
        if not services:
            # Default services to check
            services = [
                {"name": "Google", "url": "https://www.google.com"},
                {"name": "GitHub", "url": "https://api.github.com"},
                {"name": "OpenAI", "url": "https://api.openai.com/v1/models"},
            ]
        
        results = {}
        for service in services:
            name = service.get("name", service.get("url", "Unknown"))
            url = service.get("url", "")
            
            if url:
                try:
                    start = datetime.now()
                    async with httpx.AsyncClient(timeout=10) as client:
                        response = await client.get(url)
                        latency = (datetime.now() - start).total_seconds()
                        
                        results[name] = {
                            "status": "healthy" if response.status_code < 400 else "unhealthy",
                            "status_code": response.status_code,
                            "latency": f"{latency:.3f}s"
                        }
                except Exception as e:
                    results[name] = {
                        "status": "down",
                        "error": str(e)
                    }
        
        healthy = sum(1 for r in results.values() if r.get("status") == "healthy")
        
        return {
            "success": True,
            "total_services": len(results),
            "healthy": healthy,
            "unhealthy": len(results) - healthy,
            "services": results
        }
    
    async def _generate_tests(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Generate API test cases using AI"""
        api_spec = task.get("api_spec", "")
        endpoint = task.get("endpoint", "")
        
        prompt = f"""
        Génère des cas de test API pour:
        
        Endpoint: {endpoint}
        Spec: {api_spec}
        
        Génère:
        1. Tests de succès (happy path)
        2. Tests d'erreur (validation, auth, not found)
        3. Tests de limites (edge cases)
        4. Tests de performance
        
        Format: JSON array avec:
        - name: nom du test
        - method: HTTP method
        - url: URL avec paramètres
        - headers: headers requis
        - body: body si applicable
        - expected_status: code attendu
        - assertions: validations à faire
        """
        
        tests = await self.think(prompt)
        return {"success": True, "generated_tests": tests}
    
    async def _compare_responses(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Compare two API responses"""
        response1 = task.get("response1", {})
        response2 = task.get("response2", {})
        
        prompt = f"""
        Compare ces deux réponses API:
        
        Response 1: {response1}
        Response 2: {response2}
        
        Analyse:
        1. Différences structurelles
        2. Différences de valeurs
        3. Champs ajoutés/supprimés
        4. Changements de types
        
        Format: Rapport de comparaison détaillé
        """
        
        comparison = await self.think(prompt)
        return {"success": True, "comparison": comparison}
