from datetime import timedelta

from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.auth import Token, RegisterRequest
from src.schemas.users import UserResponse
from src.services.auth import (
    AuthService,
    get_current_active_user,
    get_db,
)
from src.core.exceptions import UserAlreadyExists
from src.core.error_handlers import handle_user_already_exists
from src.core.config import settings

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    register_data: RegisterRequest,
    db: AsyncSession = Depends(get_db)
):
    """Register a new user."""
    try:
        auth_service = AuthService(db)
        return await auth_service.register(register_data)
    except UserAlreadyExists as e:
        raise handle_user_already_exists(e)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed. Please try again later."
        )


@router.post("/login", response_model=Token)
async def login(
    login_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    """Login user and return access token."""
    try:
        auth_service = AuthService(db)
        return await auth_service.login(login_data)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.get("/me", response_model=UserResponse)
async def read_users_me(
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Get current authenticated user."""
    return current_user


@router.post("/refresh", response_model=Token)
async def refresh_token(
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Refresh access token."""
    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    
    from src.core.security import create_access_token
    access_token = create_access_token(
        data={"sub": current_user.username},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }
