from datetime import timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import settings
from src.core.security import verify_password, create_access_token, verify_token
from src.core.db import database
from src.repositories.users import UserRepository
from src.schemas.auth import LoginRequest, RegisterRequest
from src.schemas.users import UserCreate, UserResponse
from src.core.exceptions import UserAlreadyExists, AuthenticationError

# OAuth2 scheme for token extraction
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


async def get_db():
    async with database.session() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise


class AuthService:
    """Service for handling authentication operations."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repo = UserRepository(db)

    async def authenticate_user(self, username: str, password: str) -> Optional[UserResponse]:
        """Authenticate user with username and password."""
        user = await self.user_repo.get_by_username(username)
        if not user:
            return None

        if not verify_password(password, user.password_hash):
            return None

        return user

    async def login(self, login_data: LoginRequest) -> dict:
        """Login user and return access token."""
        user = await self.authenticate_user(
            login_data.username,
            login_data.password
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token_expires = timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        access_token = create_access_token(
            data={"sub": user.username},
            expires_delta=access_token_expires
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        }

    async def register(self, register_data: RegisterRequest) -> UserResponse:
        """Register a new user."""
        # Check if user already exists
        existing_user = await self.user_repo.get_by_username(
            register_data.username
        )
        if existing_user:
            raise UserAlreadyExists(register_data.username)

        existing_email = await self.user_repo.get_by_email(
            register_data.email
        )
        if existing_email:
            raise UserAlreadyExists(register_data.email)

        # Create new user
        user_create = UserCreate(
            first_name=register_data.first_name,
            last_name=register_data.last_name,
            username=register_data.username,
            email=register_data.email,
            password=register_data.password,
        )

        # Convert SecretStr to string for password hashing
        user_data = user_create.model_dump()
        if "password" in user_data and hasattr(user_data["password"], "get_secret_value"):
            user_data["password"] = user_data["password"].get_secret_value()

        return await self.user_repo.create(user_data)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> UserResponse:
    """Get current authenticated user from token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    username = verify_token(token)
    if username is None:
        raise AuthenticationError(
            detail="Could not validate credentials"
        )

    user = await UserRepository(db).get_by_username(username)
    if user is None:
        raise AuthenticationError(
            detail="Could not validate credentials"
        )

    return user


async def get_current_active_user(
    current_user: UserResponse = Depends(get_current_user)
) -> UserResponse:
    """Get current active user."""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user
