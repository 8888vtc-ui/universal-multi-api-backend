"""
Enhanced Conversation Memory System V2
Intelligent memory with summarization, user profiling, and topic tracking
"""
import json
import sqlite3
from typing import List, Dict, Optional, Any
from datetime import datetime, timedelta
from pathlib import Path
import logging
import hashlib

logger = logging.getLogger(__name__)


class EnhancedConversationMemory:
    """
    Advanced conversation memory with:
    - Smart summarization (reduces token usage)
    - User profiling (remembers preferences)
    - Topic tracking (knows what was discussed)
    - Long-term memory (persists across sessions)
    """
    
    def __init__(self, db_path: str = "./data/conversations_v2.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_database()
        
        # In-memory cache for fast access
        self._session_cache = {}
        self._user_profile_cache = {}
    
    def _init_database(self):
        """Initialize enhanced database schema"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Main conversations table (unchanged for compatibility)
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
            
            # User profiles table (NEW - long-term memory)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_profiles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL UNIQUE,
                    user_type TEXT,
                    language TEXT DEFAULT 'fr',
                    interests TEXT,
                    medical_context TEXT,
                    preferences TEXT,
                    first_seen TEXT,
                    last_seen TEXT,
                    total_messages INTEGER DEFAULT 0
                )
            """)
            
            # Conversation summaries table (NEW - smart summarization)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS conversation_summaries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    expert_id TEXT NOT NULL,
                    summary TEXT NOT NULL,
                    topics TEXT,
                    key_facts TEXT,
                    created_at TEXT NOT NULL,
                    message_count INTEGER DEFAULT 0,
                    UNIQUE(session_id, expert_id)
                )
            """)
            
            # Topics discussed table (NEW - topic tracking)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS topics_discussed (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    expert_id TEXT NOT NULL,
                    topic TEXT NOT NULL,
                    first_mentioned TEXT,
                    last_mentioned TEXT,
                    mention_count INTEGER DEFAULT 1,
                    details TEXT
                )
            """)
            
            # Indexes for performance
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_conv_session_expert 
                ON conversations(session_id, expert_id, timestamp)
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_topics_session 
                ON topics_discussed(session_id, expert_id)
            """)
            
            conn.commit()
        logger.info("[OK] EnhancedConversationMemory initialized")
    
    # ============================================
    # USER PROFILE MANAGEMENT
    # ============================================
    
    def get_or_create_profile(self, session_id: str) -> Dict[str, Any]:
        """Get or create user profile for session"""
        # Check cache first
        if session_id in self._user_profile_cache:
            return self._user_profile_cache[session_id]
        
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT * FROM user_profiles WHERE session_id = ?
            """, (session_id,))
            
            row = cursor.fetchone()
            
            if row:
                profile = dict(row)
                profile["interests"] = json.loads(profile.get("interests") or "[]")
                profile["preferences"] = json.loads(profile.get("preferences") or "{}")
            else:
                # Create new profile
                now = datetime.now().isoformat()
                cursor.execute("""
                    INSERT INTO user_profiles (session_id, first_seen, last_seen)
                    VALUES (?, ?, ?)
                """, (session_id, now, now))
                conn.commit()
                
                profile = {
                    "session_id": session_id,
                    "user_type": None,
                    "language": "fr",
                    "interests": [],
                    "medical_context": None,
                    "preferences": {},
                    "first_seen": now,
                    "last_seen": now,
                    "total_messages": 0
                }
            
            self._user_profile_cache[session_id] = profile
            return profile
    
    def update_profile(self, session_id: str, **kwargs):
        """Update user profile with new information"""
        profile = self.get_or_create_profile(session_id)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Build update query dynamically
            updates = []
            values = []
            
            for key, value in kwargs.items():
                if key in ["user_type", "language", "medical_context"]:
                    updates.append(f"{key} = ?")
                    values.append(value)
                elif key == "interests":
                    updates.append("interests = ?")
                    values.append(json.dumps(value))
                elif key == "preferences":
                    updates.append("preferences = ?")
                    values.append(json.dumps(value))
            
            if updates:
                updates.append("last_seen = ?")
                values.append(datetime.now().isoformat())
                values.append(session_id)
                
                cursor.execute(f"""
                    UPDATE user_profiles 
                    SET {', '.join(updates)}
                    WHERE session_id = ?
                """, values)
                conn.commit()
                
                # Update cache
                profile.update(kwargs)
                self._user_profile_cache[session_id] = profile
    
    def detect_and_save_user_type(self, session_id: str, message: str, expert_id: str):
        """Auto-detect user type from message and save to profile"""
        user_type = None
        
        # Detection patterns
        student_patterns = ["étudiant", "student", "cours", "examen", "fac", "université", "médecine", "infirmier"]
        patient_patterns = ["j'ai mal", "symptôme", "douleur", "malade", "médicament", "traitement", "diagnostic"]
        caregiver_patterns = ["mon père", "ma mère", "mon enfant", "proche", "aider", "accompagner", "famille"]
        professional_patterns = ["médecin", "infirmière", "pharmacien", "soignant", "clinique", "hôpital", "professionnel"]
        
        message_lower = message.lower()
        
        if any(p in message_lower for p in student_patterns):
            user_type = "student"
        elif any(p in message_lower for p in caregiver_patterns):
            user_type = "caregiver"
        elif any(p in message_lower for p in professional_patterns):
            user_type = "professional"
        elif any(p in message_lower for p in patient_patterns):
            user_type = "patient"
        
        if user_type:
            self.update_profile(session_id, user_type=user_type)
            logger.info(f"Detected user type '{user_type}' for session {session_id[:8]}...")
        
        return user_type
    
    # ============================================
    # MESSAGE MANAGEMENT
    # ============================================
    
    def add_message(
        self,
        session_id: str,
        expert_id: str,
        role: str,
        message: str,
        user_id: Optional[str] = None,
        metadata: Optional[Dict] = None
    ):
        """Add message and update related data"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Add message
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
                
                # Update message count in profile
                cursor.execute("""
                    UPDATE user_profiles 
                    SET total_messages = total_messages + 1, last_seen = ?
                    WHERE session_id = ?
                """, (datetime.now().isoformat(), session_id))
                
                conn.commit()
            
            # Auto-detect user type for user messages
            if role == "user":
                self.detect_and_save_user_type(session_id, message, expert_id)
                self._extract_and_save_topics(session_id, expert_id, message)
            
        except Exception as e:
            logger.error(f"Error adding message: {e}", exc_info=True)
    
    def get_conversation_history(
        self,
        session_id: str,
        expert_id: str,
        limit: int = 20
    ) -> List[Dict]:
        """Get recent conversation history"""
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
                return [dict(row) for row in reversed(rows)]
        except Exception as e:
            logger.error(f"Error getting history: {e}", exc_info=True)
            return []
    
    # ============================================
    # TOPIC TRACKING
    # ============================================
    
    def _extract_and_save_topics(self, session_id: str, expert_id: str, message: str):
        """Extract and save topics from message"""
        # Simple topic extraction based on keywords
        topic_keywords = {
            "health": {
                "diabetes": ["diabète", "diabetes", "glycémie", "insuline"],
                "hypertension": ["hypertension", "tension", "pression artérielle"],
                "medication": ["médicament", "traitement", "posologie", "effets secondaires"],
                "symptoms": ["symptôme", "douleur", "fièvre", "fatigue"],
                "nutrition": ["alimentation", "régime", "nutrition", "vitamines"]
            },
            "finance": {
                "crypto": ["bitcoin", "ethereum", "crypto", "blockchain"],
                "stocks": ["action", "bourse", "cac", "nasdaq"],
                "investment": ["investir", "placement", "épargne"]
            }
        }
        
        message_lower = message.lower()
        
        for category, topics in topic_keywords.items():
            for topic, keywords in topics.items():
                if any(kw in message_lower for kw in keywords):
                    self._save_topic(session_id, expert_id, topic)
    
    def _save_topic(self, session_id: str, expert_id: str, topic: str):
        """Save or update a topic"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                now = datetime.now().isoformat()
                
                # Try update first
                cursor.execute("""
                    UPDATE topics_discussed 
                    SET mention_count = mention_count + 1, last_mentioned = ?
                    WHERE session_id = ? AND expert_id = ? AND topic = ?
                """, (now, session_id, expert_id, topic))
                
                if cursor.rowcount == 0:
                    # Insert new
                    cursor.execute("""
                        INSERT INTO topics_discussed 
                        (session_id, expert_id, topic, first_mentioned, last_mentioned)
                        VALUES (?, ?, ?, ?, ?)
                    """, (session_id, expert_id, topic, now, now))
                
                conn.commit()
        except Exception as e:
            logger.debug(f"Error saving topic: {e}")
    
    def get_topics_discussed(self, session_id: str, expert_id: str) -> List[Dict]:
        """Get all topics discussed in this conversation"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT topic, mention_count, first_mentioned, last_mentioned
                    FROM topics_discussed
                    WHERE session_id = ? AND expert_id = ?
                    ORDER BY mention_count DESC
                """, (session_id, expert_id))
                
                return [dict(row) for row in cursor.fetchall()]
        except:
            return []
    
    # ============================================
    # SMART CONTEXT BUILDING
    # ============================================
    
    def build_smart_context(
        self,
        session_id: str,
        expert_id: str,
        include_profile: bool = True,
        include_topics: bool = True,
        max_messages: int = 10
    ) -> str:
        """
        Build intelligent context for the AI prompt.
        Optimized for token efficiency.
        """
        context_parts = []
        
        # 1. User Profile (if available)
        if include_profile:
            profile = self.get_or_create_profile(session_id)
            profile_context = self._format_profile_context(profile)
            if profile_context:
                context_parts.append(profile_context)
        
        # 2. Topics discussed (summary)
        if include_topics:
            topics = self.get_topics_discussed(session_id, expert_id)
            if topics:
                topic_list = ", ".join([t["topic"] for t in topics[:5]])
                context_parts.append(f"[SUJETS ABORDÉS]: {topic_list}")
        
        # 3. Recent conversation history (last N messages)
        history = self.get_conversation_history(session_id, expert_id, limit=max_messages)
        if history:
            history_context = self._format_history_compact(history)
            context_parts.append(history_context)
        
        return "\n\n".join(context_parts) if context_parts else ""
    
    def _format_profile_context(self, profile: Dict) -> str:
        """Format user profile for AI context"""
        parts = []
        
        if profile.get("user_type"):
            type_names = {
                "student": "Étudiant en santé",
                "patient": "Patient/Particulier",
                "caregiver": "Aidant/Proche",
                "professional": "Professionnel de santé"
            }
            parts.append(f"Profil: {type_names.get(profile['user_type'], profile['user_type'])}")
        
        if profile.get("language") and profile["language"] != "fr":
            parts.append(f"Langue: {profile['language']}")
        
        if profile.get("medical_context"):
            parts.append(f"Contexte médical: {profile['medical_context']}")
        
        if parts:
            return "[PROFIL UTILISATEUR]: " + " | ".join(parts)
        return ""
    
    def _format_history_compact(self, history: List[Dict]) -> str:
        """Format history in a compact, token-efficient way"""
        if not history:
            return ""
        
        # Take last 10 messages max
        recent = history[-10:]
        
        formatted = "[HISTORIQUE CONVERSATION]\n"
        for msg in recent:
            role = "U" if msg["role"] == "user" else "A"
            # Truncate long messages
            text = msg["message"][:200] + "..." if len(msg["message"]) > 200 else msg["message"]
            formatted += f"{role}: {text}\n"
        
        formatted += "[FIN HISTORIQUE]\n"
        formatted += "INSTRUCTIONS: Utilise cet historique. Ne répète pas les infos déjà données."
        
        return formatted
    
    # ============================================
    # MEMORY STATISTICS
    # ============================================
    
    def get_session_stats(self, session_id: str) -> Dict[str, Any]:
        """Get statistics for a session"""
        profile = self.get_or_create_profile(session_id)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Count messages per expert
            cursor.execute("""
                SELECT expert_id, COUNT(*) as count
                FROM conversations
                WHERE session_id = ?
                GROUP BY expert_id
            """, (session_id,))
            
            expert_counts = {row[0]: row[1] for row in cursor.fetchall()}
            
            # Count topics
            cursor.execute("""
                SELECT COUNT(DISTINCT topic) FROM topics_discussed
                WHERE session_id = ?
            """, (session_id,))
            
            topic_count = cursor.fetchone()[0]
        
        return {
            "session_id": session_id,
            "user_type": profile.get("user_type"),
            "total_messages": profile.get("total_messages", 0),
            "experts_used": expert_counts,
            "topics_discussed": topic_count,
            "first_seen": profile.get("first_seen"),
            "last_seen": profile.get("last_seen")
        }


# ============================================
# SINGLETON INSTANCE
# ============================================

enhanced_memory = EnhancedConversationMemory()


def get_smart_context(session_id: str, expert_id: str) -> str:
    """Convenience function to get smart context"""
    return enhanced_memory.build_smart_context(session_id, expert_id)


def add_message_with_memory(
    session_id: str,
    expert_id: str,
    role: str,
    message: str,
    user_id: Optional[str] = None
):
    """Convenience function to add message with full memory tracking"""
    enhanced_memory.add_message(session_id, expert_id, role, message, user_id)
