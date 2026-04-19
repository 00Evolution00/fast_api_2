from typing import Final

from fastapi import HTTPException, status


class UserNotFound(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "User with id {id} not found"
    message: str

    def __init__(self, _id: int | str) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(id=_id)
        super().__init__(self.message)


class UserAlreadyExists(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[
        str
    ] = "User with email {email} already exists"

    def __init__(self, email: str) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(email=email)
        super().__init__(self.message)


class PostNotFound(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Post with id {id} not found"
    message: str

    def __init__(self, _id: int | str) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(id=_id)
        super().__init__(self.message)


class PostCreationError(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Failed to create post: {message}"

    def __init__(self, message: str) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(message=message)
        super().__init__(self.message)


class DatabaseError(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Database error: {message}"

    def __init__(self, message: str) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(message=message)
        super().__init__(self.message)


class AuthenticationError(HTTPException):
    """Unified authentication exception for all auth-related errors."""
    
    def __init__(self, detail: str, status_code: int = status.HTTP_401_UNAUTHORIZED) -> None:
        super().__init__(
            status_code=status_code,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )
