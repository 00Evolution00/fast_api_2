from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.api.routes.users import router as users_router
from src.api.routes.posts import router as posts_router
from src.api.routes.auth import router as auth_router
from src.core.config import settings
from src.core.request_logging import log_user_action_middleware


def create_app() -> FastAPI:
    from src.main import lifespan

    app = FastAPI(
        lifespan=lifespan
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.middleware("http")(log_user_action_middleware)

    app.include_router(auth_router)
    app.include_router(users_router, prefix="/users", tags=["User APIs"])
    app.include_router(posts_router, prefix="/posts", tags=["Post APIs"])

    return app
