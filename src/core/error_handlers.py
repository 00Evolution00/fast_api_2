from fastapi import HTTPException, status
from src.core.exceptions import (
    UserNotFound,
    UserAlreadyExists,
    PostNotFound,
    PostCreationError,
    DatabaseError,
)


def handle_user_not_found(error: UserNotFound) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=error.message,
    )


def handle_user_already_exists(error: UserAlreadyExists) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=error.message,
    )


def handle_post_not_found(error: PostNotFound) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=error.message,
    )


def handle_post_creation_error(error: PostCreationError) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=error.message,
    )


def handle_database_error(error: DatabaseError) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=error.message,
    )
