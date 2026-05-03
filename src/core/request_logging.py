import logging
import os
import time
from typing import Callable

from fastapi import Request, Response

from src.core.config import settings
from src.core.security import verify_token


def get_user_action_logger() -> logging.Logger:
    os.makedirs("/app/logs", exist_ok=True)

    logger = logging.getLogger("user_actions")
    if logger.handlers:
        return logger

    log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)
    logger.setLevel(log_level)
    logger.propagate = False

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    file_handler = logging.FileHandler("/app/logs/user_actions.log")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger


async def log_user_action_middleware(
    request: Request, call_next: Callable
) -> Response:
    logger = get_user_action_logger()
    started_at = time.perf_counter()

    username = "anonymous"
    auth_header = request.headers.get("authorization")
    if auth_header and auth_header.lower().startswith("bearer "):
        token = auth_header.split(" ", 1)[1]
        resolved_user = verify_token(token)
        if resolved_user:
            username = resolved_user

    status_code = 500
    try:
        response = await call_next(request)
        status_code = response.status_code
        return response
    finally:
        duration_ms = (time.perf_counter() - started_at) * 1000
        client_ip = request.client.host if request.client else "-"
        logger.info(
            "user=%s method=%s path=%s status=%s ip=%s duration_ms=%.2f",
            username,
            request.method,
            request.url.path,
            status_code,
            client_ip,
            duration_ms,
        )
