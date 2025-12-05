"""
Router d'authentification
Endpoints pour inscription, connexion, et gestion des tokens
"""
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Optional
from services.auth import (
    auth_service,
    UserCreate,
    User,
    Token,
    TokenData
)

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """Obtenir l'utilisateur actuel depuis le token"""
    payload = auth_service.verify_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
    
    user = auth_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    
    return user


@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate):
    """
    Enregistrer un nouvel utilisateur
    
    - **email**: Email de l'utilisateur
    - **username**: Nom d'utilisateur unique
    - **password**: Mot de passe (sera hashé)
    """
    try:
        user = auth_service.register_user(user_data)
        # Ne pas retourner le hash du mot de passe
        user.hashed_password = "***"
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Connexion utilisateur
    
    Retourne un access token et un refresh token
    """
    user = auth_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = auth_service.create_access_token(
        {"user_id": user.id, "email": user.email}
    )
    refresh_token = auth_service.create_refresh_token(user.id)
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.post("/refresh", response_model=Token)
async def refresh_token(refresh_token: str):
    """
    Rafraîchir un access token avec un refresh token
    """
    new_access_token = auth_service.refresh_access_token(refresh_token)
    if not new_access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    # Extraire user_id du refresh token pour créer un nouveau refresh token
    payload = auth_service.verify_token(refresh_token, token_type="refresh")
    if payload:
        user_id = payload.get("user_id")
        new_refresh_token = auth_service.create_refresh_token(user_id)
        
        return {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer"
        }
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid refresh token"
    )


@router.get("/me", response_model=User)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """
    Obtenir les informations de l'utilisateur actuel
    """
    current_user.hashed_password = "***"
    return current_user


@router.post("/logout")
async def logout(token: str = Depends(oauth2_scheme)):
    """
    Déconnexion (invalider le refresh token)
    """
    payload = auth_service.verify_token(token)
    if payload:
        user_id = payload.get("user_id")
        # Supprimer les refresh tokens de l'utilisateur
        import sqlite3
        conn = sqlite3.connect(str(auth_service.db_path), check_same_thread=False)
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM refresh_tokens WHERE user_id = ?", (user_id,))
            conn.commit()
        finally:
            conn.close()
    
    return {"message": "Logged out successfully"}

