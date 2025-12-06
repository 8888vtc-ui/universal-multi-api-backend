"""
Script de benchmark et optimisation
"""
import asyncio
import time
import httpx
from typing import Dict, List
import statistics


BASE_URL = "http://localhost:8000"


async def benchmark_endpoint(
    endpoint: str,
    method: str = "GET",
    payload: dict = None,
    iterations: int = 100
) -> Dict:
    """Benchmark un endpoint"""
    times = []
    errors = 0
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        for i in range(iterations):
            try:
                start = time.time()
                
                if method == "GET":
                    response = await client.get(endpoint)
                elif method == "POST":
                    response = await client.post(endpoint, json=payload)
                else:
                    raise ValueError(f"Unsupported method: {method}")
                
                elapsed = (time.time() - start) * 1000  # ms
                times.append(elapsed)
                
                if response.status_code >= 400:
                    errors += 1
                    
            except Exception as e:
                errors += 1
                print(f"Error on iteration {i}: {e}")
    
    if not times:
        return {
            "endpoint": endpoint,
            "iterations": iterations,
            "errors": errors,
            "success_rate": 0
        }
    
    return {
        "endpoint": endpoint,
        "method": method,
        "iterations": iterations,
        "errors": errors,
        "success_rate": ((iterations - errors) / iterations) * 100,
        "avg_time_ms": statistics.mean(times),
        "median_time_ms": statistics.median(times),
        "min_time_ms": min(times),
        "max_time_ms": max(times),
        "p95_time_ms": statistics.quantiles(times, n=20)[18] if len(times) > 20 else max(times),
        "p99_time_ms": statistics.quantiles(times, n=100)[98] if len(times) > 100 else max(times),
        "std_dev_ms": statistics.stdev(times) if len(times) > 1 else 0
    }


async def benchmark_concurrent(
    endpoint: str,
    method: str = "GET",
    payload: dict = None,
    concurrent: int = 10,
    iterations: int = 100
) -> Dict:
    """Benchmark avec requêtes concurrentes"""
    times = []
    errors = 0
    
    async def make_request():
        nonlocal errors
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                start = time.time()
                
                if method == "GET":
                    response = await client.get(endpoint)
                elif method == "POST":
                    response = await client.post(endpoint, json=payload)
                
                elapsed = (time.time() - start) * 1000
                times.append(elapsed)
                
                if response.status_code >= 400:
                    errors += 1
        except Exception:
            errors += 1
    
    # Créer toutes les tâches
    tasks = [make_request() for _ in range(iterations)]
    
    # Exécuter avec limite de concurrence
    start = time.time()
    for i in range(0, len(tasks), concurrent):
        batch = tasks[i:i+concurrent]
        await asyncio.gather(*batch)
    total_time = (time.time() - start) * 1000
    
    if not times:
        return {
            "endpoint": endpoint,
            "concurrent": concurrent,
            "iterations": iterations,
            "errors": errors,
            "success_rate": 0
        }
    
    return {
        "endpoint": endpoint,
        "method": method,
        "concurrent": concurrent,
        "iterations": iterations,
        "total_time_ms": total_time,
        "requests_per_second": (iterations / (total_time / 1000)) if total_time > 0 else 0,
        "errors": errors,
        "success_rate": ((iterations - errors) / iterations) * 100,
        "avg_time_ms": statistics.mean(times),
        "median_time_ms": statistics.median(times),
        "min_time_ms": min(times),
        "max_time_ms": max(times)
    }


async def run_benchmarks():
    """Exécuter tous les benchmarks"""
    print("="*60)
    print("🚀 BENCHMARKS - Universal Multi-API Backend")
    print("="*60)
    print("\n⚠️  Assurez-vous que le serveur est démarré!\n")
    
    benchmarks = [
        # Health check (le plus rapide)
        ("/api/health", "GET", None, 100),
        
        # Analytics (rapide, local)
        ("/api/analytics/health", "GET", None, 50),
        ("/api/analytics/metrics?days=1", "GET", None, 50),
        
        # Assistant (local)
        ("/api/assistant/status", "GET", None, 50),
        
        # Search (peut être plus lent avec APIs externes)
        ("/api/search/universal", "POST", {"query": "test", "max_results_per_category": 3}, 20),
    ]
    
    results = []
    
    for endpoint, method, payload, iterations in benchmarks:
        print(f"\n📊 Benchmark: {method} {endpoint}")
        print(f"   Iterations: {iterations}")
        
        result = await benchmark_endpoint(
            endpoint=endpoint,
            method=method,
            payload=payload,
            iterations=iterations
        )
        
        results.append(result)
        
        print(f"   ✅ Succès: {result['success_rate']:.1f}%")
        print(f"   ⏱️  Temps moyen: {result['avg_time_ms']:.2f} ms")
        print(f"   📈 P95: {result.get('p95_time_ms', 0):.2f} ms")
        print(f"   ⚠️  Erreurs: {result['errors']}")
    
    # Benchmark concurrent
    print(f"\n\n🔄 Benchmark Concurrent:")
    print(f"   Endpoint: /api/health")
    print(f"   Concurrence: 10")
    print(f"   Iterations: 100")
    
    concurrent_result = await benchmark_concurrent(
        endpoint="/api/health",
        method="GET",
        concurrent=10,
        iterations=100
    )
    
    print(f"   ✅ Succès: {concurrent_result['success_rate']:.1f}%")
    print(f"   🚀 Requêtes/seconde: {concurrent_result['requests_per_second']:.1f}")
    print(f"   ⏱️  Temps total: {concurrent_result['total_time_ms']:.2f} ms")
    
    # Résumé
    print("\n" + "="*60)
    print("📊 RÉSUMÉ")
    print("="*60)
    
    for result in results:
        print(f"\n{result['endpoint']}:")
        print(f"  Temps moyen: {result['avg_time_ms']:.2f} ms")
        print(f"  Succès: {result['success_rate']:.1f}%")
    
    return results


if __name__ == "__main__":
    asyncio.run(run_benchmarks())



