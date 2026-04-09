from datetime import datetime
from typing import Optional

from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    SecretStr,
    ConfigDict,
)
from src.core.validators import UserValidators, UserPasswordValidators


class UserBase(BaseModel, UserValidators):
    first_name: str = Field(max_length=255)
    last_name: str = Field(max_length=255)
    username: str = Field(max_length=255)
    email: EmailStr


class UserCreate(UserBase):
    password: SecretStr = Field(min_length=8, max_length=255)


class UserUpdate(BaseModel):
    first_name: Optional[str] = Field(default=None, max_length=255)
    last_name: Optional[str] = Field(default=None, max_length=255)
    username: Optional[str] = Field(default=None, max_length=255)
    email: Optional[EmailStr] = None


class UserUpdatePassword(BaseModel, UserPasswordValidators):
    current_password: SecretStr = Field(min_length=8, max_length=255)
    new_password: SecretStr = Field(min_length=8, max_length=255)


class UserResponse(UserBase):
    id: str
    is_active: bool = True
    is_superuser: bool = False
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
