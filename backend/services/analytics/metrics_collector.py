"""
Metrics Collector - Collecteur de métriques
Collecte les métriques d'utilisation de l'API
"""
from typing import Dict, Any, List
from datetime import datetime, timedelta
from collections import defaultdict, Counter
import sqlite3
from pathlib import Path


class MetricsCollector:
    """Collecteur de métriques d'utilisation"""
    
    def __init__(self, db_path: str = "./data/analytics.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_database()
    
    def _init_database(self):
        """Initialiser la base de données analytics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Table métriques
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                endpoint TEXT,
                method TEXT,
                status_code INTEGER,
                response_time_ms REAL,
                user_id TEXT,
                ip_address TEXT
            )
        """)
        
        # Table erreurs
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS errors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                endpoint TEXT,
                error_type TEXT,
                error_message TEXT,
                user_id TEXT
            )
        """)
        
        # Index pour performance
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_metrics_timestamp 
            ON metrics(timestamp)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_metrics_endpoint 
            ON metrics(endpoint)
        """)
        
        conn.commit()
        conn.close()
    
    def record_request(
        self,
        endpoint: str,
        method: str = "GET",
        status_code: int = 200,
        response_time_ms: float = 0.0,
        user_id: str = None,
        ip_address: str = None
    ) -> None:
        """Enregistrer une requête"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO metrics (timestamp, endpoint, method, status_code, response_time_ms, user_id, ip_address)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            datetime.now().isoformat(),
            endpoint,
            method,
            status_code,
            response_time_ms,
            user_id,
            ip_address
        ))
        
        conn.commit()
        conn.close()
    
    def record_error(
        self,
        endpoint: str,
        error_type: str,
        error_message: str,
        user_id: str = None
    ) -> None:
        """Enregistrer une erreur"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO errors (timestamp, endpoint, error_type, error_message, user_id)
            VALUES (?, ?, ?, ?, ?)
        """, (
            datetime.now().isoformat(),
            endpoint,
            error_type,
            error_message,
            user_id
        ))
        
        conn.commit()
        conn.close()
    
    def get_metrics(
        self,
        days: int = 7,
        endpoint: str = None
    ) -> Dict[str, Any]:
        """Obtenir les métriques"""
        cutoff_date = datetime.now() - timedelta(days=days)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if endpoint:
            cursor.execute("""
                SELECT * FROM metrics
                WHERE timestamp > ? AND endpoint = ?
                ORDER BY timestamp DESC
            """, (cutoff_date.isoformat(), endpoint))
        else:
            cursor.execute("""
                SELECT * FROM metrics
                WHERE timestamp > ?
                ORDER BY timestamp DESC
            """, (cutoff_date.isoformat(),))
        
        rows = cursor.fetchall()
        conn.close()
        
        # Analyser les métriques
        total_requests = len(rows)
        status_codes = Counter([row[4] for row in rows])  # status_code
        endpoints = Counter([row[2] for row in rows])  # endpoint
        methods = Counter([row[3] for row in rows])  # method
        
        # Temps de réponse moyen
        response_times = [row[5] for row in rows if row[5] and row[5] > 0]
        avg_response_time = sum(response_times) / len(response_times) if response_times else 0
        
        # Requêtes par jour
        requests_by_day = defaultdict(int)
        for row in rows:
            timestamp = datetime.fromisoformat(row[1])
            day = timestamp.date().isoformat()
            requests_by_day[day] += 1
        
        return {
            "period_days": days,
            "total_requests": total_requests,
            "avg_response_time_ms": round(avg_response_time, 2),
            "status_codes": dict(status_codes),
            "endpoints": dict(endpoints.most_common(10)),
            "methods": dict(methods),
            "requests_by_day": dict(requests_by_day),
            "requests_per_day": round(total_requests / days, 2) if days > 0 else 0
        }
    
    def get_errors(
        self,
        days: int = 7
    ) -> Dict[str, Any]:
        """Obtenir les erreurs"""
        cutoff_date = datetime.now() - timedelta(days=days)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM errors
            WHERE timestamp > ?
            ORDER BY timestamp DESC
        """, (cutoff_date.isoformat(),))
        
        rows = cursor.fetchall()
        conn.close()
        
        # Analyser les erreurs
        total_errors = len(rows)
        # Structure: (id, timestamp, endpoint, error_type, error_message, user_id)
        error_types = Counter([row[3] for row in rows if len(row) > 3])  # error_type (index 3)
        error_endpoints = Counter([row[2] for row in rows if len(row) > 2])  # endpoint (index 2)
        
        # Erreurs par jour
        errors_by_day = defaultdict(int)
        for row in rows:
            timestamp = datetime.fromisoformat(row[1])
            day = timestamp.date().isoformat()
            errors_by_day[day] += 1
        
        return {
            "period_days": days,
            "total_errors": total_errors,
            "error_types": dict(error_types),
            "error_endpoints": dict(error_endpoints.most_common(10)),
            "errors_by_day": dict(errors_by_day),
            "errors_per_day": round(total_errors / days, 2) if days > 0 else 0
        }
    
    def get_top_endpoints(
        self,
        days: int = 7,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Obtenir les endpoints les plus utilisés"""
        metrics = self.get_metrics(days=days)
        endpoints = metrics.get("endpoints", {})
        
        return [
            {
                "endpoint": endpoint,
                "requests": count,
                "percentage": round((count / metrics["total_requests"]) * 100, 2) if metrics["total_requests"] > 0 else 0
            }
            for endpoint, count in list(endpoints.items())[:limit]
        ]
    
    def get_performance_stats(
        self,
        days: int = 7
    ) -> Dict[str, Any]:
        """Obtenir les statistiques de performance"""
        cutoff_date = datetime.now() - timedelta(days=days)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                AVG(response_time_ms) as avg_time,
                MIN(response_time_ms) as min_time,
                MAX(response_time_ms) as max_time,
                COUNT(*) as total
            FROM metrics
            WHERE timestamp > ? AND response_time_ms > 0
        """, (cutoff_date.isoformat(),))
        
        row = cursor.fetchone()
        conn.close()
        
        if row and row[3] > 0:
            return {
                "avg_response_time_ms": round(row[0], 2),
                "min_response_time_ms": round(row[1], 2),
                "max_response_time_ms": round(row[2], 2),
                "total_requests": row[3]
            }
        
        return {
            "avg_response_time_ms": 0,
            "min_response_time_ms": 0,
            "max_response_time_ms": 0,
            "total_requests": 0
        }


# Singleton instance
metrics_collector = MetricsCollector()

