"""
Metrics Router
Endpoints pour Prometheus et monitoring
"""
import os
import time
import logging
from datetime import datetime, timezone
from typing import Dict, Any
from fastapi import APIRouter, Response
from collections import defaultdict

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/metrics", tags=["Metrics"])


class MetricsCollector:
    """Collecteur de métriques simple"""
    
    def __init__(self):
        self.request_count = defaultdict(int)
        self.request_duration = defaultdict(list)
        self.error_count = defaultdict(int)
        self.start_time = time.time()
    
    def record_request(self, endpoint: str, method: str, status: int, duration_ms: float):
        """Enregistrer une requête"""
        key = f"{method}_{endpoint}"
        self.request_count[key] += 1
        self.request_duration[key].append(duration_ms)
        
        if status >= 400:
            self.error_count[f"{key}_{status}"] += 1
    
    def get_metrics(self) -> Dict[str, Any]:
        """Obtenir toutes les métriques"""
        uptime = time.time() - self.start_time
        
        # Calculer les moyennes
        avg_durations = {}
        for key, durations in self.request_duration.items():
            if durations:
                avg_durations[key] = sum(durations) / len(durations)
        
        return {
            "uptime_seconds": round(uptime, 2),
            "total_requests": sum(self.request_count.values()),
            "requests_by_endpoint": dict(self.request_count),
            "errors_by_type": dict(self.error_count),
            "avg_response_time_ms": avg_durations
        }
    
    def to_prometheus(self) -> str:
        """Exporter au format Prometheus"""
        lines = []
        
        # Uptime
        uptime = time.time() - self.start_time
        lines.append(f"# HELP api_uptime_seconds Total uptime in seconds")
        lines.append(f"# TYPE api_uptime_seconds gauge")
        lines.append(f"api_uptime_seconds {uptime:.2f}")
        
        # Request count
        lines.append(f"# HELP api_requests_total Total number of requests")
        lines.append(f"# TYPE api_requests_total counter")
        for key, count in self.request_count.items():
            method, endpoint = key.split("_", 1)
            lines.append(f'api_requests_total{{method="{method}",endpoint="{endpoint}"}} {count}')
        
        # Error count
        lines.append(f"# HELP api_errors_total Total number of errors")
        lines.append(f"# TYPE api_errors_total counter")
        for key, count in self.error_count.items():
            lines.append(f'api_errors_total{{type="{key}"}} {count}')
        
        # Response time
        lines.append(f"# HELP api_response_time_ms Average response time in milliseconds")
        lines.append(f"# TYPE api_response_time_ms gauge")
        for key, durations in self.request_duration.items():
            if durations:
                avg = sum(durations) / len(durations)
                method, endpoint = key.split("_", 1)
                lines.append(f'api_response_time_ms{{method="{method}",endpoint="{endpoint}"}} {avg:.2f}')
        
        return "\n".join(lines)


# Instance globale
metrics_collector = MetricsCollector()


@router.get("")
async def get_metrics():
    """
    📊 Obtenir les métriques JSON
    
    Returns:
        uptime, requests, errors, response times
    """
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        **metrics_collector.get_metrics()
    }


@router.get("/prometheus")
async def get_prometheus_metrics():
    """
    📊 Métriques au format Prometheus
    
    Pour scraping par Prometheus
    """
    return Response(
        content=metrics_collector.to_prometheus(),
        media_type="text/plain"
    )


@router.get("/summary")
async def get_metrics_summary():
    """
    📊 Résumé des métriques
    """
    metrics = metrics_collector.get_metrics()
    
    total_requests = metrics["total_requests"]
    total_errors = sum(metrics["errors_by_type"].values())
    error_rate = (total_errors / total_requests * 100) if total_requests > 0 else 0
    
    # Top 5 endpoints
    top_endpoints = sorted(
        metrics["requests_by_endpoint"].items(),
        key=lambda x: x[1],
        reverse=True
    )[:5]
    
    return {
        "uptime_hours": round(metrics["uptime_seconds"] / 3600, 2),
        "total_requests": total_requests,
        "total_errors": total_errors,
        "error_rate_percent": round(error_rate, 2),
        "top_endpoints": dict(top_endpoints),
        "avg_response_time_ms": round(
            sum(sum(d) for d in metrics_collector.request_duration.values()) /
            max(sum(len(d) for d in metrics_collector.request_duration.values()), 1),
            2
        )
    }


<<<<<<< Updated upstream
=======





>>>>>>> Stashed changes
