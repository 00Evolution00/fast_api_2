import re
from typing import Any

from pydantic import field_validator


class PostValidators:
    @field_validator('title', mode='before')
    @classmethod
    def validate_title(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('Title cannot be empty')
        if len(v.strip()) < 3:
            raise ValueError('Title must be at least 3 characters long')
        if len(v) > 255:
            raise ValueError('Title cannot exceed 255 characters')
        return v.strip()

    @field_validator('text', mode='before')
    @classmethod
    def validate_text(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('Text cannot be empty')
        if len(v.strip()) < 10:
            raise ValueError('Text must be at least 10 characters long')
        return v.strip()

    @field_validator('author_id', mode='before')
    @classmethod
    def validate_author_id(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('Author ID cannot be empty')
        
        # Basic UUID format validation
        uuid_pattern = re.compile(
            r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$',
            re.IGNORECASE
        )
        
        if not uuid_pattern.match(v):
            raise ValueError('Author ID must be a valid UUID')
        return v.strip()


class UserValidators:
    @field_validator('email', mode='before')
    @classmethod
    def validate_email(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('Email cannot be empty')
        
        email_pattern = re.compile(
            r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        )
        
        if not email_pattern.match(v):
            raise ValueError('Invalid email format')
        return v.strip().lower()

    @field_validator('username', mode='before')
    @classmethod
    def validate_username(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('Username cannot be empty')
        if len(v.strip()) < 3:
            raise ValueError('Username must be at least 3 characters long')
        if len(v) > 50:
            raise ValueError('Username cannot exceed 50 characters')
        
        # Only allow alphanumeric characters, underscores, and hyphens
        username_pattern = re.compile(r'^[a-zA-Z0-9_-]+$')
        if not username_pattern.match(v.strip()):
            raise ValueError('Username can only contain letters, numbers, underscores, and hyphens')
        
        return v.strip()


class UserPasswordValidators:
    @field_validator('password', mode='before', check_fields=False)
    @classmethod
    def validate_password(cls, v: Any) -> str:
        password_str = str(v) if v else ""
        if not password_str:
            raise ValueError('Password cannot be empty')
        if len(password_str) < 8:
            raise ValueError('Password must be at least 8 characters long')
        
        # Check for at least one uppercase letter
        if not re.search(r'[A-Z]', password_str):
            raise ValueError('Password must contain at least one uppercase letter')
        
        # Check for at least one lowercase letter
        if not re.search(r'[a-z]', password_str):
            raise ValueError('Password must contain at least one lowercase letter')
        
        # Check for at least one digit
        if not re.search(r'\d', password_str):
            raise ValueError('Password must contain at least one digit')
        
        return password_str
