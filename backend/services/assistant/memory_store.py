"""
Memory Store - Stockage mémoire utilisateur
Stockage local avec SQLite pour MVP
"""
import sqlite3
import json
from typing import Dict, Any, Optional, List
from datetime import datetime
from pathlib import Path
import os


class MemoryStore:
    """Gestionnaire de stockage mémoire utilisateur"""
    
    def __init__(self, db_path: str = "./data/assistant.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_database()
    
    def _init_database(self):
        """Initialiser la base de données"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Table utilisateurs
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                preferences TEXT,
                learned_patterns TEXT,
                created_at TEXT,
                last_updated TEXT
            )
        """)
        
        # Table interactions
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS interactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                timestamp TEXT,
                query TEXT,
                category TEXT,
                action TEXT,
                result_id TEXT,
                feedback TEXT,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)
        
        # Index pour performance
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_user_interactions 
            ON interactions(user_id, timestamp)
        """)
        
        conn.commit()
        conn.close()
    
    def save_interaction(
        self,
        user_id: str,
        query: str,
        category: str,
        action: str = "search",
        result_id: Optional[str] = None,
        feedback: Optional[str] = None
    ) -> None:
        """Sauvegarder une interaction utilisateur"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Créer utilisateur si n'existe pas
        cursor.execute("""
            INSERT OR IGNORE INTO users (user_id, preferences, learned_patterns, created_at, last_updated)
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, "{}", "{}", datetime.now().isoformat(), datetime.now().isoformat()))
        
        # Sauvegarder interaction
        cursor.execute("""
            INSERT INTO interactions (user_id, timestamp, query, category, action, result_id, feedback)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            user_id,
            datetime.now().isoformat(),
            query,
            category,
            action,
            result_id,
            feedback
        ))
        
        # Mettre à jour last_updated
        cursor.execute("""
            UPDATE users SET last_updated = ? WHERE user_id = ?
        """, (datetime.now().isoformat(), user_id))
        
        conn.commit()
        conn.close()
    
    def get_user_interactions(
        self,
        user_id: str,
        limit: int = 100,
        category: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Obtenir les interactions d'un utilisateur"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        if category:
            cursor.execute("""
                SELECT * FROM interactions
                WHERE user_id = ? AND category = ?
                ORDER BY timestamp DESC
                LIMIT ?
            """, (user_id, category, limit))
        else:
            cursor.execute("""
                SELECT * FROM interactions
                WHERE user_id = ?
                ORDER BY timestamp DESC
                LIMIT ?
            """, (user_id, limit))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def save_preferences(
        self,
        user_id: str,
        preferences: Dict[str, Any]
    ) -> None:
        """Sauvegarder les préférences utilisateur"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        preferences_json = json.dumps(preferences)
        
        cursor.execute("""
            INSERT OR REPLACE INTO users (user_id, preferences, last_updated)
            VALUES (?, ?, ?)
        """, (user_id, preferences_json, datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
    
    def get_preferences(self, user_id: str) -> Dict[str, Any]:
        """Obtenir les préférences utilisateur"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT preferences FROM users WHERE user_id = ?
        """, (user_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row and row[0]:
            return json.loads(row[0])
        return {}
    
    def save_learned_patterns(
        self,
        user_id: str,
        patterns: Dict[str, Any]
    ) -> None:
        """Sauvegarder les patterns appris"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        patterns_json = json.dumps(patterns)
        
        cursor.execute("""
            UPDATE users SET learned_patterns = ?, last_updated = ?
            WHERE user_id = ?
        """, (patterns_json, datetime.now().isoformat(), user_id))
        
        conn.commit()
        conn.close()
    
    def get_learned_patterns(self, user_id: str) -> Dict[str, Any]:
        """Obtenir les patterns appris"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT learned_patterns FROM users WHERE user_id = ?
        """, (user_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row and row[0]:
            return json.loads(row[0])
        return {}
    
    def get_user_stats(self, user_id: str) -> Dict[str, Any]:
        """Obtenir les statistiques d'un utilisateur"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Nombre total d'interactions
        cursor.execute("""
            SELECT COUNT(*) FROM interactions WHERE user_id = ?
        """, (user_id,))
        total_interactions = cursor.fetchone()[0]
        
        # Interactions par catégorie
        cursor.execute("""
            SELECT category, COUNT(*) as count
            FROM interactions
            WHERE user_id = ?
            GROUP BY category
            ORDER BY count DESC
        """, (user_id,))
        category_counts = {row[0]: row[1] for row in cursor.fetchall()}
        
        # Dernière interaction
        cursor.execute("""
            SELECT timestamp FROM interactions
            WHERE user_id = ?
            ORDER BY timestamp DESC
            LIMIT 1
        """, (user_id,))
        last_interaction = cursor.fetchone()
        
        conn.close()
        
        return {
            "user_id": user_id,
            "total_interactions": total_interactions,
            "category_counts": category_counts,
            "last_interaction": last_interaction[0] if last_interaction else None
        }


# Singleton instance
memory_store = MemoryStore()


