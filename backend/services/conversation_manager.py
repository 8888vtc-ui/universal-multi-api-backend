"""
Service de gestion des conversations pour les experts IA
Stocke et récupère l'historique de conversation
"""
import json
import sqlite3
from typing import List, Dict, Optional
from datetime import datetime
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class ConversationManager:
    """Gère l'historique de conversation par session"""
    
    def __init__(self, db_path: str = "./data/conversations.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_database()
    
    def _init_database(self):
        """Initialiser la base de données"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    expert_id TEXT NOT NULL,
                    user_id TEXT,
                    role TEXT NOT NULL,
                    message TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    metadata TEXT
                )
            """)
            
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_session_expert 
                ON conversations(session_id, expert_id, timestamp)
            """)
            
            conn.commit()
        logger.info("[OK] ConversationManager initialized")
    
    def add_message(
        self,
        session_id: str,
        expert_id: str,
        role: str,
        message: str,
        user_id: Optional[str] = None,
        metadata: Optional[Dict] = None
    ):
        """Ajouter un message à la conversation"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT INTO conversations 
                    (session_id, expert_id, user_id, role, message, timestamp, metadata)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    session_id,
                    expert_id,
                    user_id,
                    role,
                    message,
                    datetime.now().isoformat(),
                    json.dumps(metadata or {})
                ))
                
                conn.commit()
        except Exception as e:
            logger.error(f"Error adding message to conversation: {e}", exc_info=True)
    
    def get_conversation_history(
        self,
        session_id: str,
        expert_id: str,
        limit: int = 10
    ) -> List[Dict]:
        """Récupérer l'historique de conversation"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT role, message, timestamp
                    FROM conversations
                    WHERE session_id = ? AND expert_id = ?
                    ORDER BY timestamp DESC
                    LIMIT ?
                """, (session_id, expert_id, limit))
                
                rows = cursor.fetchall()
                
                # Inverser pour avoir l'ordre chronologique
                return [dict(row) for row in reversed(rows)]
        except Exception as e:
            logger.error(f"Error getting conversation history: {e}", exc_info=True)
            return []
    
    def format_history_for_prompt(self, history: List[Dict]) -> str:
        """Formater l'historique pour injection dans le prompt"""
        if not history:
            return ""
        
        formatted = "\n\n[HISTORIQUE DE LA CONVERSATION]\n"
        for msg in history[-5:]:  # Derniers 5 messages
            role = "Utilisateur" if msg["role"] == "user" else "Assistant"
            formatted += f"{role}: {msg['message']}\n"
        
        formatted += "\n[FIN DE L'HISTORIQUE]\n"
        formatted += "IMPORTANT: Utilise cet historique pour comprendre le contexte. Ne répète pas exactement les mêmes informations déjà données. Ne répète JAMAIS le message d'introduction ou de bienvenue.\n"
        return formatted

# Singleton
conversation_manager = ConversationManager()


Stocke et récupère l'historique de conversation
"""
import json
import sqlite3
from typing import List, Dict, Optional
from datetime import datetime
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class ConversationManager:
    """Gère l'historique de conversation par session"""
    
    def __init__(self, db_path: str = "./data/conversations.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_database()
    
    def _init_database(self):
        """Initialiser la base de données"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    expert_id TEXT NOT NULL,
                    user_id TEXT,
                    role TEXT NOT NULL,
                    message TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    metadata TEXT
                )
            """)
            
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_session_expert 
                ON conversations(session_id, expert_id, timestamp)
            """)
            
            conn.commit()
        logger.info("[OK] ConversationManager initialized")
    
    def add_message(
        self,
        session_id: str,
        expert_id: str,
        role: str,
        message: str,
        user_id: Optional[str] = None,
        metadata: Optional[Dict] = None
    ):
        """Ajouter un message à la conversation"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT INTO conversations 
                    (session_id, expert_id, user_id, role, message, timestamp, metadata)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    session_id,
                    expert_id,
                    user_id,
                    role,
                    message,
                    datetime.now().isoformat(),
                    json.dumps(metadata or {})
                ))
                
                conn.commit()
        except Exception as e:
            logger.error(f"Error adding message to conversation: {e}", exc_info=True)
    
    def get_conversation_history(
        self,
        session_id: str,
        expert_id: str,
        limit: int = 10
    ) -> List[Dict]:
        """Récupérer l'historique de conversation"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT role, message, timestamp
                    FROM conversations
                    WHERE session_id = ? AND expert_id = ?
                    ORDER BY timestamp DESC
                    LIMIT ?
                """, (session_id, expert_id, limit))
                
                rows = cursor.fetchall()
                
                # Inverser pour avoir l'ordre chronologique
                return [dict(row) for row in reversed(rows)]
        except Exception as e:
            logger.error(f"Error getting conversation history: {e}", exc_info=True)
            return []
    
    def format_history_for_prompt(self, history: List[Dict]) -> str:
        """Formater l'historique pour injection dans le prompt"""
        if not history:
            return ""
        
        formatted = "\n\n[HISTORIQUE DE LA CONVERSATION]\n"
        for msg in history[-5:]:  # Derniers 5 messages
            role = "Utilisateur" if msg["role"] == "user" else "Assistant"
            formatted += f"{role}: {msg['message']}\n"
        
        formatted += "\n[FIN DE L'HISTORIQUE]\n"
        formatted += "IMPORTANT: Utilise cet historique pour comprendre le contexte. Ne répète pas exactement les mêmes informations déjà données. Ne répète JAMAIS le message d'introduction ou de bienvenue.\n"
        return formatted

# Singleton
conversation_manager = ConversationManager()

