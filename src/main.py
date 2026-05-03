import os
import sys
from contextlib import asynccontextmanager

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
)

from src.app import create_app


@asynccontextmanager
async def lifespan(app):
    os.makedirs("/app/logs", exist_ok=True)
    yield


app = create_app()


# Add health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint for Docker."""
    return {"status": "healthy", "service": "fastapi-backend"}
