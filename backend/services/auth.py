"""
Service d'authentification JWT
Gestion des utilisateurs, tokens JWT, et authentification
"""
import os
import logging
from jose import jwt
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr
import sqlite3
from pathlib import Path

logger = logging.getLogger(__name__)

# Configuration
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
if not SECRET_KEY:
    # En développement, utiliser une clé par défaut avec warning
    if os.getenv("ENVIRONMENT", "development") == "development":
        SECRET_KEY = "dev-secret-key-not-for-production-use"
        logger.warning(
            "⚠️  JWT_SECRET_KEY not set. Using development key. "
            "Set JWT_SECRET_KEY in production!"
        )
    else:
        raise ValueError(
            "JWT_SECRET_KEY must be set in environment variables.\n"
            "Generate a secure key with: python -c 'import secrets; print(secrets.token_urlsafe(32))'\n"
            "Or set JWT_SECRET_KEY in your .env file."
        )

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7))

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(BaseModel):
    """Modèle utilisateur"""
    id: Optional[str] = None
    email: EmailStr
    username: str
    hashed_password: str
    is_active: bool = True
    created_at: Optional[str] = None


class UserCreate(BaseModel):
    """Modèle pour création utilisateur"""
    email: EmailStr
    username: str
    password: str


class Token(BaseModel):
    """Modèle token"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Données du token"""
    user_id: Optional[str] = None
    email: Optional[str] = None


class AuthService:
    """Service d'authentification avec gestion SQLite sécurisée"""
    
    def __init__(self, db_path: str = "./data/auth.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()
    
    def _get_connection(self) -> sqlite3.Connection:
        """Obtenir une connexion SQLite avec paramètres optimisés"""
        conn = sqlite3.connect(
            str(self.db_path),
            check_same_thread=False,
            timeout=30.0
        )
        conn.row_factory = sqlite3.Row  # Accès par nom de colonne
        return conn
    
    def _init_db(self):
        """Initialiser la base de données"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id TEXT PRIMARY KEY,
                    email TEXT UNIQUE NOT NULL,
                    username TEXT UNIQUE NOT NULL,
                    hashed_password TEXT NOT NULL,
                    is_active INTEGER DEFAULT 1,
                    created_at TEXT NOT NULL
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS refresh_tokens (
                    token TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    expires_at TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            """)
            
            # Index pour performance
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_username ON users(username)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_refresh_tokens_user ON refresh_tokens(user_id)")
            
            conn.commit()
            logger.info("✅ Auth database initialized")
        except Exception as e:
            logger.error(f"❌ Auth database init failed: {e}")
            raise
        finally:
            conn.close()
    
    def hash_password(self, password: str) -> str:
        """Hasher un mot de passe"""
        return pwd_context.hash(password)
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Vérifier un mot de passe"""
        return pwd_context.verify(plain_password, hashed_password)
    
    def create_access_token(self, data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        """Créer un token JWT"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({"exp": expire, "type": "access"})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    def create_refresh_token(self, user_id: str) -> str:
        """Créer un refresh token"""
        expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        created_at = datetime.now(timezone.utc).isoformat()
        
        to_encode = {
            "user_id": user_id,
            "exp": expire,
            "type": "refresh"
        }
        token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        
        # Sauvegarder dans la DB
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO refresh_tokens (token, user_id, expires_at, created_at)
                VALUES (?, ?, ?, ?)
            """, (token, user_id, expire.isoformat(), created_at))
            conn.commit()
        except Exception as e:
            logger.error(f"Failed to save refresh token: {e}")
            raise
        finally:
            conn.close()
        
        return token
    
    def verify_token(self, token: str, token_type: str = "access") -> Optional[Dict[str, Any]]:
        """Vérifier un token JWT"""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            if payload.get("type") != token_type:
                return None
            return payload
        except jwt.ExpiredSignatureError:
            logger.debug("Token expired")
            return None
        except jwt.InvalidTokenError as e:
            logger.debug(f"Invalid token: {e}")
            return None
    
    def register_user(self, user_data: UserCreate) -> User:
        """Enregistrer un nouvel utilisateur"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            # Vérifier si l'email existe déjà
            cursor.execute("SELECT id FROM users WHERE email = ?", (user_data.email,))
            if cursor.fetchone():
                raise ValueError("Email already registered")
            
            # Vérifier si le username existe déjà
            cursor.execute("SELECT id FROM users WHERE username = ?", (user_data.username,))
            if cursor.fetchone():
                raise ValueError("Username already taken")
            
            # Créer l'utilisateur
            user_id = f"user_{datetime.now(timezone.utc).timestamp()}"
            hashed_password = self.hash_password(user_data.password)
            created_at = datetime.now(timezone.utc).isoformat()
            
            cursor.execute("""
                INSERT INTO users (id, email, username, hashed_password, is_active, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                user_id,
                user_data.email,
                user_data.username,
                hashed_password,
                1,
                created_at
            ))
            
            conn.commit()
            logger.info(f"✅ User registered: {user_data.email}")
            
            return User(
                id=user_id,
                email=user_data.email,
                username=user_data.username,
                hashed_password=hashed_password,
                is_active=True,
                created_at=created_at
            )
        except ValueError:
            raise
        except Exception as e:
            logger.error(f"❌ User registration failed: {e}")
            raise
        finally:
            conn.close()
    
    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """Authentifier un utilisateur"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT id, email, username, hashed_password, is_active, created_at
                FROM users WHERE email = ?
            """, (email,))
            
            row = cursor.fetchone()
        finally:
            conn.close()
        
        if not row:
            return None
        
        user = User(
            id=row["id"],
            email=row["email"],
            username=row["username"],
            hashed_password=row["hashed_password"],
            is_active=bool(row["is_active"]),
            created_at=row["created_at"]
        )
        
        if not self.verify_password(password, user.hashed_password):
            logger.warning(f"Failed login attempt for: {email}")
            return None
        
        if not user.is_active:
            logger.warning(f"Inactive user login attempt: {email}")
            return None
        
        logger.info(f"✅ User authenticated: {email}")
        return user
    
    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Obtenir un utilisateur par ID"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT id, email, username, hashed_password, is_active, created_at
                FROM users WHERE id = ?
            """, (user_id,))
            
            row = cursor.fetchone()
        finally:
            conn.close()
        
        if not row:
            return None
        
        return User(
            id=row["id"],
            email=row["email"],
            username=row["username"],
            hashed_password=row["hashed_password"],
            is_active=bool(row["is_active"]),
            created_at=row["created_at"]
        )
    
    def refresh_access_token(self, refresh_token: str) -> Optional[str]:
        """Rafraîchir un access token"""
        payload = self.verify_token(refresh_token, token_type="refresh")
        if not payload:
            return None
        
        user_id = payload.get("user_id")
        if not user_id:
            return None
        
        # Vérifier que le refresh token existe dans la DB
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT user_id FROM refresh_tokens WHERE token = ?", (refresh_token,))
            if not cursor.fetchone():
                return None
        finally:
            conn.close()
        
        # Créer un nouveau access token
        user = self.get_user_by_id(user_id)
        if not user:
            return None
        
        return self.create_access_token({"user_id": user_id, "email": user.email})
    
    def revoke_refresh_token(self, refresh_token: str) -> bool:
        """Révoquer un refresh token"""
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM refresh_tokens WHERE token = ?", (refresh_token,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            logger.error(f"Failed to revoke token: {e}")
            return False
        finally:
            conn.close()
    
    def revoke_all_user_tokens(self, user_id: str) -> int:
        """Révoquer tous les refresh tokens d'un utilisateur"""
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM refresh_tokens WHERE user_id = ?", (user_id,))
            conn.commit()
            count = cursor.rowcount
            logger.info(f"Revoked {count} tokens for user {user_id}")
            return count
        except Exception as e:
            logger.error(f"Failed to revoke user tokens: {e}")
            return 0
        finally:
            conn.close()
    
    def cleanup_expired_tokens(self) -> int:
        """Nettoyer les refresh tokens expirés"""
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            now = datetime.now(timezone.utc).isoformat()
            cursor.execute("DELETE FROM refresh_tokens WHERE expires_at < ?", (now,))
            conn.commit()
            count = cursor.rowcount
            if count > 0:
                logger.info(f"Cleaned up {count} expired tokens")
            return count
        except Exception as e:
            logger.error(f"Failed to cleanup tokens: {e}")
            return 0
        finally:
            conn.close()


# Singleton instance - with lazy initialization for testing
_auth_service = None

def get_auth_service() -> AuthService:
    """Get or create the auth service singleton"""
    global _auth_service
    if _auth_service is None:
        _auth_service = AuthService()
    return _auth_service

# For backward compatibility
auth_service = get_auth_service()
<<<<<<< Updated upstream
=======

# FastAPI Dependencies
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login", auto_error=False)

async def get_current_user(token: str = Depends(oauth2_scheme)) -> Dict[str, Any]:
    """Dependency to get current authenticated user"""
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    payload = auth_service.verify_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    return payload

async def get_optional_user(token: str = Depends(oauth2_scheme)) -> Optional[Dict[str, Any]]:
    """Dependency to get optional user (returns None if not auth)"""
    if not token:
        return None
    
    return auth_service.verify_token(token)

Gestion des utilisateurs, tokens JWT, et authentification
"""
import os
import logging
from jose import jwt
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr
import sqlite3
from pathlib import Path
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

logger = logging.getLogger(__name__)

# Configuration
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
if not SECRET_KEY:
    # En développement, utiliser une clé par défaut avec warning
    if os.getenv("ENVIRONMENT", "development") == "development":
        SECRET_KEY = "dev-secret-key-not-for-production-use"
        logger.warning(
            "[WARN]  JWT_SECRET_KEY not set. Using development key. "
            "Set JWT_SECRET_KEY in production!"
        )
    else:
        raise ValueError(
            "JWT_SECRET_KEY must be set in environment variables.\n"
            "Generate a secure key with: python -c 'import secrets; print(secrets.token_urlsafe(32))'\n"
            "Or set JWT_SECRET_KEY in your .env file."
        )

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7))

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(BaseModel):
    """Modèle utilisateur"""
    id: Optional[str] = None
    email: EmailStr
    username: str
    hashed_password: str
    is_active: bool = True
    created_at: Optional[str] = None


class UserCreate(BaseModel):
    """Modèle pour création utilisateur"""
    email: EmailStr
    username: str
    password: str


class Token(BaseModel):
    """Modèle token"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Données du token"""
    user_id: Optional[str] = None
    email: Optional[str] = None


class AuthService:
    """Service d'authentification avec gestion SQLite sécurisée"""
    
    def __init__(self, db_path: str = "./data/auth.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()
    
    def _get_connection(self) -> sqlite3.Connection:
        """Obtenir une connexion SQLite avec paramètres optimisés
        
        Note: check_same_thread=False est nécessaire pour FastAPI (async),
        mais on utilise des context managers pour garantir la fermeture.
        """
        conn = sqlite3.connect(
            str(self.db_path),
            check_same_thread=False,  # Nécessaire pour FastAPI async
            timeout=30.0,
            isolation_level=None  # Autocommit mode pour meilleure performance
        )
        conn.row_factory = sqlite3.Row  # Accès par nom de colonne
        # Activer WAL mode pour meilleure concurrence
        conn.execute("PRAGMA journal_mode=WAL")
        return conn
    
    def _init_db(self):
        """Initialiser la base de données"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id TEXT PRIMARY KEY,
                    email TEXT UNIQUE NOT NULL,
                    username TEXT UNIQUE NOT NULL,
                    hashed_password TEXT NOT NULL,
                    is_active INTEGER DEFAULT 1,
                    created_at TEXT NOT NULL
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS refresh_tokens (
                    token TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    expires_at TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            """)
            
            # Index pour performance
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_username ON users(username)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_refresh_tokens_user ON refresh_tokens(user_id)")
            
            conn.commit()
            logger.info("[OK] Auth database initialized")
        except Exception as e:
            logger.error(f"[ERR] Auth database init failed: {e}")
            raise
        finally:
            conn.close()
    
    def hash_password(self, password: str) -> str:
        """Hasher un mot de passe"""
        return pwd_context.hash(password)
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Vérifier un mot de passe"""
        return pwd_context.verify(plain_password, hashed_password)
    
    def create_access_token(self, data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        """Créer un token JWT"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({"exp": expire, "type": "access"})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    def create_refresh_token(self, user_id: str) -> str:
        """Créer un refresh token"""
        expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        created_at = datetime.now(timezone.utc).isoformat()
        
        to_encode = {
            "user_id": user_id,
            "exp": expire,
            "type": "refresh"
        }
        token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        
        # Sauvegarder dans la DB
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO refresh_tokens (token, user_id, expires_at, created_at)
                VALUES (?, ?, ?, ?)
            """, (token, user_id, expire.isoformat(), created_at))
            conn.commit()
        except Exception as e:
            logger.error(f"Failed to save refresh token: {e}")
            raise
        finally:
            conn.close()
        
        return token
    
    def verify_token(self, token: str, token_type: str = "access") -> Optional[Dict[str, Any]]:
        """Vérifier un token JWT"""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            if payload.get("type") != token_type:
                return None
            return payload
        except jwt.ExpiredSignatureError:
            logger.debug("Token expired")
            return None
        except jwt.InvalidTokenError as e:
            logger.debug(f"Invalid token: {e}")
            return None
    
    def register_user(self, user_data: UserCreate) -> User:
        """Enregistrer un nouvel utilisateur"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            # Vérifier si l'email existe déjà
            cursor.execute("SELECT id FROM users WHERE email = ?", (user_data.email,))
            if cursor.fetchone():
                raise ValueError("Email already registered")
            
            # Vérifier si le username existe déjà
            cursor.execute("SELECT id FROM users WHERE username = ?", (user_data.username,))
            if cursor.fetchone():
                raise ValueError("Username already taken")
            
            # Créer l'utilisateur
            user_id = f"user_{datetime.now(timezone.utc).timestamp()}"
            hashed_password = self.hash_password(user_data.password)
            created_at = datetime.now(timezone.utc).isoformat()
            
            cursor.execute("""
                INSERT INTO users (id, email, username, hashed_password, is_active, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                user_id,
                user_data.email,
                user_data.username,
                hashed_password,
                1,
                created_at
            ))
            
            conn.commit()
            logger.info(f"[OK] User registered: {user_data.email}")
            
            return User(
                id=user_id,
                email=user_data.email,
                username=user_data.username,
                hashed_password=hashed_password,
                is_active=True,
                created_at=created_at
            )
        except ValueError:
            raise
        except Exception as e:
            logger.error(f"[ERR] User registration failed: {e}")
            raise
        finally:
            conn.close()
    
    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """Authentifier un utilisateur"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT id, email, username, hashed_password, is_active, created_at
                FROM users WHERE email = ?
            """, (email,))
            
            row = cursor.fetchone()
        finally:
            conn.close()
        
        if not row:
            return None
        
        user = User(
            id=row["id"],
            email=row["email"],
            username=row["username"],
            hashed_password=row["hashed_password"],
            is_active=bool(row["is_active"]),
            created_at=row["created_at"]
        )
        
        if not self.verify_password(password, user.hashed_password):
            logger.warning(f"Failed login attempt for: {email}")
            return None
        
        if not user.is_active:
            logger.warning(f"Inactive user login attempt: {email}")
            return None
        
        logger.info(f"[OK] User authenticated: {email}")
        return user
    
    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Obtenir un utilisateur par ID"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT id, email, username, hashed_password, is_active, created_at
                FROM users WHERE id = ?
            """, (user_id,))
            
            row = cursor.fetchone()
        finally:
            conn.close()
        
        if not row:
            return None
        
        return User(
            id=row["id"],
            email=row["email"],
            username=row["username"],
            hashed_password=row["hashed_password"],
            is_active=bool(row["is_active"]),
            created_at=row["created_at"]
        )
    
    def refresh_access_token(self, refresh_token: str) -> Optional[str]:
        """Rafraîchir un access token"""
        payload = self.verify_token(refresh_token, token_type="refresh")
        if not payload:
            return None
        
        user_id = payload.get("user_id")
        if not user_id:
            return None
        
        # Vérifier que le refresh token existe dans la DB
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT user_id FROM refresh_tokens WHERE token = ?", (refresh_token,))
            if not cursor.fetchone():
                return None
        finally:
            conn.close()
        
        # Créer un nouveau access token
        user = self.get_user_by_id(user_id)
        if not user:
            return None
        
        return self.create_access_token({"user_id": user_id, "email": user.email})
    
    def revoke_refresh_token(self, refresh_token: str) -> bool:
        """Révoquer un refresh token"""
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM refresh_tokens WHERE token = ?", (refresh_token,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            logger.error(f"Failed to revoke token: {e}")
            return False
        finally:
            conn.close()
    
    def revoke_all_user_tokens(self, user_id: str) -> int:
        """Révoquer tous les refresh tokens d'un utilisateur"""
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM refresh_tokens WHERE user_id = ?", (user_id,))
            conn.commit()
            count = cursor.rowcount
            logger.info(f"Revoked {count} tokens for user {user_id}")
            return count
        except Exception as e:
            logger.error(f"Failed to revoke user tokens: {e}")
            return 0
        finally:
            conn.close()
    
    def cleanup_expired_tokens(self) -> int:
        """Nettoyer les refresh tokens expirés"""
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            now = datetime.now(timezone.utc).isoformat()
            cursor.execute("DELETE FROM refresh_tokens WHERE expires_at < ?", (now,))
            conn.commit()
            count = cursor.rowcount
            if count > 0:
                logger.info(f"Cleaned up {count} expired tokens")
            return count
        except Exception as e:
            logger.error(f"Failed to cleanup tokens: {e}")
            return 0
        finally:
            conn.close()


# Singleton instance - with lazy initialization for testing
_auth_service = None

def get_auth_service() -> AuthService:
    """Get or create the auth service singleton"""
    global _auth_service
    if _auth_service is None:
        _auth_service = AuthService()
    return _auth_service

# For backward compatibility
auth_service = get_auth_service()

# FastAPI Dependencies
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login", auto_error=False)

async def get_current_user(token: str = Depends(oauth2_scheme)) -> Dict[str, Any]:
    """Dependency to get current authenticated user"""
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    payload = auth_service.verify_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    return payload

async def get_optional_user(token: str = Depends(oauth2_scheme)) -> Optional[Dict[str, Any]]:
    """Dependency to get optional user (returns None if not auth)"""
    if not token:
        return None
    
    return auth_service.verify_token(token)
>>>>>>> Stashed changes
