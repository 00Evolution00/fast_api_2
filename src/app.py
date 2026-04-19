from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.api.routes.users import router as users_router
from src.api.routes.posts import router as posts_router
from src.api.routes.auth import router as auth_router


def create_app() -> FastAPI:
    from src.main import lifespan

    app = FastAPI(
        root_path="/api/v1",
        lifespan=lifespan
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(auth_router)
    app.include_router(users_router, prefix="/users", tags=["User APIs"])
    app.include_router(posts_router, prefix="/posts", tags=["Post APIs"])

    return app
